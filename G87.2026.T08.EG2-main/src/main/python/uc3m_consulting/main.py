import enterprise_project

def showMD5():  # usage

    obj = enterprise_project.EnterpriseProject(
        company_cif='B12345678',
        project_acronym='ABC123',
        project_description='aaaaaaaaaa',
        department='HR',
        starting_date='01/01/2025',
        project_budget=50000.00
    )

    print(obj.project_id)
    obj = enterprise_project.EnterpriseProject(
        company_cif='B12345678',
        project_acronym='ABC12',
        project_description='aaaaaaaaaaa',
        department='FINANCE',
        starting_date='02/02/2026',
        project_budget=50000.01
    )

    print(obj.project_id)
    obj = enterprise_project.EnterpriseProject(
        company_cif='B12345678',
        project_acronym='ABCDE1234',
        project_description='aaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        department='LEGAL',
        starting_date='31/12/2027',
        project_budget=1000000.00
    )

    print(obj.project_id)
    obj = enterprise_project.EnterpriseProject(
        company_cif='B12345678',
        project_acronym='ABCDE12345',
        project_description='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        department='LOGISTICS',
        starting_date='30/11/2025',
        project_budget=999999.99
    )

    print(obj.project_id)


if __name__ == "__main__":
    showMD5()
