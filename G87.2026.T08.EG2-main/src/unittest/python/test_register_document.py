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

    # VALID TESTS

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

    # INPUT FILE NOT FOUND

    def test_register_document_input_file_not_found(self):
        with self.assertRaises(EnterpriseManagementException) as context:
            self.manager.register_document("missing.json")
        self.assertEqual(str(context.exception), "Input file not found.")

    # THE FILE IS NOT JSON FORMATTED

    def test_register_document_tc04_delete_root_node(self):
        self._assert_exception_message(
            '',
            "The file is not JSON formatted."
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

    def test_register_document_tc12_modify_starting_bracket(self):
        self._assert_exception_message(
            '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc13_delete_field1(self):
        self._assert_exception_message(
            '{,"FILENAME":"ABC12345.docx"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc14_duplicate_field1(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"'
            '"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.docx"}',
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

    def test_register_document_tc17_delete_field2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc18_duplicate_field2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.xlsx"'
            '"FILENAME":"ABC12345.xlsx"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc19_modify_ending_bracket(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.xlsx"',
            "The file is not JSON formatted."
        )

    def test_register_document_tc20_delete_labelfield1(self):
        self._assert_exception_message(
            '{:"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc21_duplicate_labelfield1(self):
        self._assert_exception_message(
            '{"PROJECT_ID""PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
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

    def test_register_document_tc24_delete_valuefield1(self):
        self._assert_exception_message(
            '{"PROJECT_ID":,"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc25_duplicate_valuefield1(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7""84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc26_modify_comma(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7""FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc27_delete_labelfield2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",:"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc28_duplicate_labelfield2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME""FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc29_delete_colon_field2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc30_duplicate_colon_field2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME"::"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc31_delete_valuefield2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc32_duplicate_valuefield2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc33_delete_start_quotation(self):
        self._assert_exception_message(
            '{PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc34_duplicate_start_quotation(self):
        self._assert_exception_message(
            '{""PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc37_delete_labelfield1_end_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID:"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc38_duplicate_labelfield1_end_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID"":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc39_modify_colon_field1(self):
        self._assert_exception_message(
            '{"PROJECT_ID""84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc40_delete_valuefield1_starting_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc41_duplicate_valuefield1_starting_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":""84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc44_delete_valuefield1_ending_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7,"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc45_duplicate_valuefield1_ending_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7"","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc46_delete_labelfield2_starting_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc47_duplicate_labelfield2_starting_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",""FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc50_delete_labelfield2_ending_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME:"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc51_duplicate_labelfield2_ending_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME"":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc52_modify_colon_field2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc53_delete_valuefield2_starting_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc54_duplicate_valuefield2_starting_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":""ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc57_delete_valuefield2_ending_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc58_duplicate_valuefield2_ending_quotation(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf""}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc59_modify_quotation_31(self):
        self._assert_exception_message(
            '{PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc61_modify_quotation_33(self):
        self._assert_exception_message(
            '{"PROJECT_ID:"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc62_modify_quotation_34(self):
        self._assert_exception_message(
            '{"PROJECT_ID":84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc64_modify_quotation_36(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7,"FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc65_modify_quotation_37(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7",FILENAME":"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc67_modify_quotation_39(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME:"ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc68_modify_quotation_40(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":ABC12345.pdf"}',
            "The file is not JSON formatted."
        )

    def test_register_document_tc73_modify_quotation_43(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf}',
            "The file is not JSON formatted."
        )

    # JSON DOES NOT HAVE THE EXPECTED STRUCTURE

    def test_register_document_tc08_delete_fields(self):
        self._assert_exception_message(
            '{}',
            "JSON does not have the expected structure."
        )

    def test_register_document_tc35_delete_project_id(self):
        self._assert_exception_message(
            '{"":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_register_document_tc36_duplicate_project_id(self):
        self._assert_exception_message(
            '{"PROJECT_IDPROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_register_document_tc48_delete_filename(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_register_document_tc49_duplicate_filename(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAMEFILENAME":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_register_document_tc60_modify_project_id_label(self):
        self._assert_exception_message(
            '{"PROJ_CT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    def test_register_document_tc66_modify_filename_label(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILE_NAM":"ABC12345.pdf"}',
            "JSON does not have the expected structure."
        )

    # JSON DATA HAS NO VALID VALUES

    def test_register_document_tc42_delete_value1(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"","FILENAME":"ABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc43_duplicate_value1(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee784a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc55_delete_value2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":""}',
            "JSON data has no valid values."
        )

    def test_register_document_tc56_duplicate_value2(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdfABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc63_modify_project_id_value(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5_bfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc69_delete_name(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":".pdf"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc70_duplicate_name(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345ABC12345.pdf"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc71_delete_extension(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc72_duplicate_extension(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pdf.pdf"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc74_modify_name(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12-45.pdf"}',
            "JSON data has no valid values."
        )

    def test_register_document_tc75_modify_extension(self):
        self._assert_exception_message(
            '{"PROJECT_ID":"84a2b5abfa27576259e41a033d07cee7","FILENAME":"ABC12345.pd_"}',
            "JSON data has no valid values."
        )