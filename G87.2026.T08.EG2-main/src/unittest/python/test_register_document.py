import os
from unittest import TestCase
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterDocument(TestCase):
    def setUp(self):
        self.file_path = "mytest.json"
        self.manager = EnterpriseManager()

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if os.path.exists("all_documents.json"):
            os.remove("all_documents.json")

    def _write_file(self, content: str):
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(content)

    def _assert_exception_message(self, content: str, expected_message: str):
        self._write_file(content)
        with self.assertRaises(EnterpriseManagementException) as context:
            self.manager.register_document(self.file_path)
        self.assertEqual(str(context.exception), expected_message)

    def test_register_document_tc01_valid_pdf(self):
        self._write_file(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}'
        )
        value = self.manager.register_document(self.file_path)
        self.assertIsNotNone(value)

    def test_register_document_tc02_valid_docx(self):
        self._write_file(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.docx"}'
        )
        value = self.manager.register_document(self.file_path)
        self.assertIsNotNone(value)

    def test_register_document_tc03_valid_xlsx(self):
        self._write_file(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.xlsx"}'
        )
        value = self.manager.register_document(self.file_path)
        self.assertIsNotNone(value)

    def test_register_document_input_file_not_found(self):
        with self.assertRaises(EnterpriseManagementException) as context:
            self.manager.register_document("missing.json")
        self.assertEqual(str(context.exception), "Input file not found.")

    def test_register_document_tc04_delete_root_node(self):
        self._assert_exception_message(
            '',
            "The file is not JSON formatted."
        )

    def test_register_document_tc08_delete_fields(self):
        self._assert_exception_message(
            '{}',
            "JSON does not have the expected structure."
        )

    def test_register_document_tc48_delete_filename(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_register_document_tc63_modify_project_id_value(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5_bfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc74_modify_name(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12-45.pdf"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc05_duplicate_root_node(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.xlsx"}'
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc06_delete_first_bracket(self):
        self._assert_exception_message(
            '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc07_duplicate_first_bracket(self):
        self._assert_exception_message(
            '{{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc09_duplicate_fields(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"'
            '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc10_delete_ending_bracket(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.xlsx"',
            "The file is not JSON formatted."
        )

    def test_register_document_tc11_duplicate_ending_bracket(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.xlsx"}}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc15_delete_comma(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7""FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc16_duplicate_comma(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",,"FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc22_delete_colon_field1(self):
        self._assert_exception_message(
            '{"PROJECT_ID""84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc23_duplicate_colon_field1(self):
        self._assert_exception_message(
            '{"PROJECT_ID"::"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc29_delete_colon_field2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc37_delete_label_field1_end_quote(self):
        self._assert_exception_message(
            '{"PROJECT_ID:"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )