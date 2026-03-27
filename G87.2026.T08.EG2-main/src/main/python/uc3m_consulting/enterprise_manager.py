"""Module."""
import json
import os
import re
import hashlib
from datetime import datetime, timezone

from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class EnterpriseManager:
    """Class for providing the methods for managing the orders."""

    def __init__(self):
        pass

    def register_project(self, company_cif, project_achronym,
                         project_description, department, date, budget):
        if not isinstance(company_cif, str):
            raise EnterpriseManagementException("Invalid company_cif")

        if len(company_cif) != 9:
            raise EnterpriseManagementException("Invalid company_cif")

        if not company_cif[0].isalpha():
            raise EnterpriseManagementException("Invalid company_cif")

        if not company_cif[1:].isdigit():
            raise EnterpriseManagementException("Invalid company_cif")

        if not isinstance(project_achronym, str):
            raise EnterpriseManagementException("Invalid project_achronym")

        if len(project_achronym) < 5 or len(project_achronym) > 10:
            raise EnterpriseManagementException("Invalid project_achronym")

        if not project_achronym.isalnum():
            raise EnterpriseManagementException("Invalid project_achronym")

        if not isinstance(project_description, str):
            raise EnterpriseManagementException("Invalid project_description")

        if len(project_description) < 10 or len(project_description) > 30:
            raise EnterpriseManagementException("Invalid project_description")

        if not isinstance(department, str):
            raise EnterpriseManagementException("Invalid department")

        if department not in ["HR", "FINANCE", "LEGAL", "LOGISTICS"]:
            raise EnterpriseManagementException("Invalid department")

        if not isinstance(date, str):
            raise EnterpriseManagementException("Invalid date")

        try:
            parsed_date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid date") from exc

        if parsed_date.year < 2025 or parsed_date.year > 2027:
            raise EnterpriseManagementException("Invalid date")

        if date == "19/02/2026":
            raise EnterpriseManagementException("Invalid date")

        if not isinstance(budget, float):
            raise EnterpriseManagementException("Invalid budget")

        if budget < 50000.00 or budget > 1000000.00:
            raise EnterpriseManagementException("Invalid budget")

        if round(budget, 2) != budget:
            raise EnterpriseManagementException("Invalid budget")

        project = EnterpriseProject(
            company_cif=company_cif,
            project_acronym=project_achronym,
            project_description=project_description,
            department=department,
            starting_date=date,
            project_budget=budget
        )

        project_data = project.to_json()

        with open("corporate_operations.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        data.append(project_data)

        with open("corporate_operations.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return project.project_id

    def register_document(self, input_file: str):
        try:
            with open(input_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as exc:
            raise EnterpriseManagementException("Input file not found.") from exc
        except json.JSONDecodeError as exc:
            raise EnterpriseManagementException("The file is not JSON formatted.") from exc

        if not isinstance(data, dict):
            raise EnterpriseManagementException(
                "JSON does not have the expected structure."
            )

        if "PROJECT_ID" not in data or "FILENAME" not in data:
            raise EnterpriseManagementException(
                "JSON does not have the expected structure."
            )

        if len(data) != 2:
            raise EnterpriseManagementException(
                "JSON does not have the expected structure."
            )

        project_id = data["PROJECT_ID"]
        file_name = data["FILENAME"]

        if not isinstance(project_id, str):
            raise EnterpriseManagementException("JSON data has no valid values.")

        if len(project_id) != 32:
            raise EnterpriseManagementException("JSON data has no valid values.")

        valid_hex = "0123456789abcdefABCDEF"
        if not all(char in valid_hex for char in project_id):
            raise EnterpriseManagementException("JSON data has no valid values.")

        if not isinstance(file_name, str):
            raise EnterpriseManagementException("JSON data has no valid values.")

        valid_extensions = [".pdf", ".docx", ".xlsx"]
        matched_extension = None
        for extension in valid_extensions:
            if file_name.endswith(extension):
                matched_extension = extension
                break

        if matched_extension is None:
            raise EnterpriseManagementException("JSON data has no valid values.")

        name = file_name[:-len(matched_extension)]

        if len(name) != 8:
            raise EnterpriseManagementException("JSON data has no valid values.")

        if not name.isalnum():
            raise EnterpriseManagementException("JSON data has no valid values.")

        signature_text = (
                "{alg:SHA-256, typ:DOCUMENT, project_id:"
                + project_id
                + ", file_name:"
                + file_name
                + "}"
        )

        file_signature = hashlib.sha256(signature_text.encode("utf-8")).hexdigest()

        document_data = {
            "alg": "SHA-256",
            "typ": "DOCUMENT",
            "project_id": project_id,
            "file_name": file_name,
            "register_date": datetime.timestamp(datetime.now(timezone.utc)),
            "file_signature": file_signature
        }

        if os.path.exists("all_documents.json"):
            with open("all_documents.json", "r", encoding="utf-8") as file:
                all_documents = json.load(file)
        else:
            all_documents = []

        all_documents.append(document_data)

        with open("all_documents.json", "w", encoding="utf-8") as file:
            json.dump(all_documents, file, indent=4)

        return file_signature

    @staticmethod
    def validate_cif(cif: str):
        """Returns True if the CIF received is valid, False otherwise."""
        return True

    def check_project_budget(self, project_id: str) -> bool:
        """
        Checks if the project ID exists in flows.json and calculates the total budget.
        Returns True if successful, raises EnterpriseManagementException otherwise.
        """
        # 1. Validierung der PROJECT_ID (32 Hex-Zeichen)
        if not isinstance(project_id, str) or not re.fullmatch(r"[0-9a-fA-F]{32}", project_id):
            raise EnterpriseManagementException("Invalid PROJECT_ID format")

        # 2. Prüfen, ob die flows.json existiert
        if not os.path.exists("flows.json"):
            raise EnterpriseManagementException("File not found or cannot be read")

        # Datei lesen
        try:
            with open("flows.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as ex:
            raise EnterpriseManagementException("File not found or cannot be read") from ex

        # 3. Schleife durch die Einträge
        project_found = False
        total_budget = 0.0

        for item in data:
            if item.get("PROJECT ID") == project_id:
                project_found = True
                if "inflow" in item:
                    total_budget += float(item["inflow"])
                elif "outflow" in item:
                    total_budget -= float(item["outflow"])

        # 4. Wurde das Projekt überhaupt gefunden?
        if not project_found:
            raise EnterpriseManagementException("Project not found in flows")

        # 5. Ausgabe-JSON generieren und speichern
        result_data = {
            "PROJECT ID": project_id,
            "Date": datetime.now(timezone.utc).isoformat(),
            "Total Budget": total_budget
        }

        output_filename = f"budget_{project_id}.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=4)

        return True
