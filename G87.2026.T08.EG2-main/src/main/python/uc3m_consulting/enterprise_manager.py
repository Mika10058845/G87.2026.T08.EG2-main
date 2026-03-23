"""Module """
import json
from uc3m_consulting.enterprise_project import EnterpriseProject

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def register_project(self, company_cif, project_achronym,
                         project_description, department, date, budget):
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

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True
