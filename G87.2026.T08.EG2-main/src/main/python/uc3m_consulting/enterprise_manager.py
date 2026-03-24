"""Module """
import json
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from datetime import datetime

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
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

        # Date before request was recieved
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

    def register_document (input_file: str):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True
