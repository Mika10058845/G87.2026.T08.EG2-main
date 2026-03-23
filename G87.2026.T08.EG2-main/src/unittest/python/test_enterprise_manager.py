import json
import os
from unittest import TestCase
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestEnterpriseManager(TestCase):
    def setUp(self):
        self.file_path = "corporate_operations.json"
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([], file)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_register_project_tc01_valid_case(self):
        obj = EnterpriseManager()

        value = obj.register_project(
            "B12345678",
            "ABC123",
            "aaaaaaaaaa",
            "HR",
            "01/01/2025",
            50000.00
        )

        self.assertEqual(value, "84a2b5abfa27576259e41a033d07cee7")

        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["company_cif"], "B12345678")
        self.assertEqual(data[0]["project_acronym"], "ABC123")
        self.assertEqual(data[0]["project_description"], "aaaaaaaaaa")
        self.assertEqual(data[0]["department"], "HR")
        self.assertEqual(data[0]["starting_date"], "01/01/2025")
        self.assertEqual(data[0]["project_budget"], 50000.00)
        self.assertEqual(data[0]["project_id"], "84a2b5abfa27576259e41a033d07cee7")

    def test_register_project_tc02_valid_case(self):
        obj = EnterpriseManager()

        value = obj.register_project(
            "B12345678",
            "ABC12",
            "aaaaaaaaaaa",
            "FINANCE",
            "02/02/2026",
            50000.01
        )

        self.assertEqual(value, "b32db90448bfbc3e0137062cbf2e05e3")

    def test_register_project_tc03_valid_case(self):
        obj = EnterpriseManager()

        value = obj.register_project(
            "B12345678",
            "ABCDE1234",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "LEGAL",
            "31/12/2027",
            1000000.00
        )

        self.assertEqual(value, "1ba88c786f8590a76a16826d4eeea5e3")

    def test_register_project_tc04_valid_case(self):
        obj = EnterpriseManager()

        value = obj.register_project(
            "B12345678",
            "ABCDE12345",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "LOGISTICS",
            "30/11/2025",
            999999.99
        )

        self.assertEqual(value, "91e070cf7fb4765ce4c9598116463215")

    def test_register_project_tc05_company_cif_integer(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                12345,
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc06_company_cif_length_10(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B123456789",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc07_company_cif_length_8(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B1234567",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc08_company_cif_invalid_content(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "1B234567B",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc09_project_achronym_length_4(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABC1",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc10_project_achronym_length_11(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABC12345678",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc11_project_achronym_invalid_tokens(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "A,C1!3",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc12_project_description_integer(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                1234567890,
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc13_project_description_length_9(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc14_project_description_length_31(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc15_department_integer(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                1234,
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc16_department_not_valid(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "HI",
                "30/11/2025",
                999999.99
            )

    def test_register_project_tc17_date_integer(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                112025,
                999999.99
            )

    def test_register_project_tc18_date_invalid_format(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "01/11/25",
                999999.99
            )

    def test_register_project_tc19_date_day_00(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "00/11/2025",
                999999.99
            )

    def test_register_project_tc20_date_day_32(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "31/11/2025",
                999999.99
            )

    def test_register_project_tc21_date_month_00(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "01/00/2025",
                999999.99
            )

    def test_register_project_tc22_date_month_13(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "01/13/2025",
                999999.99
            )

    def test_register_project_tc23_date_year_2024(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "01/11/2024",
                999999.99
            )

    def test_register_project_tc24_date_year_2028(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "01/11/2028",
                999999.99
            )

    def test_register_project_tc25_date_request_date_minus_1(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "19/02/2026",
                999999.99
            )

    def test_register_project_tc26_budget_string(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                "999999.99"
            )

    def test_register_project_tc27_budget_one_decimal(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.971
            )

    def test_register_project_tc28_budget_above_maximum(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                1000000.01
            )

    def test_register_project_tc29_budget_below_minimum(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                "ABCDE12345",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                49999.99
            )

    def test_register_project_tc30_project_achronym_not_string(self):
        obj = EnterpriseManager()

        with self.assertRaises(EnterpriseManagementException):
            obj.register_project(
                "B12345678",
                123455,
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "LOGISTICS",
                "30/11/2025",
                999999.99
            )