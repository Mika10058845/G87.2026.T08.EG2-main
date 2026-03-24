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