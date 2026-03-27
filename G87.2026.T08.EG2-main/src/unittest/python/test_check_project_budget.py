import unittest
import os
import json
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class TestCheckProjectBudget(unittest.TestCase):
    """Test cases for Method 3: check_project_budget"""

    def test_m3_path1_invalid_id(self):
        """Path 1: Invalid project_id format."""
        em = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            em.check_project_budget("invalid_id_123")
        self.assertEqual(context.exception.message, "Invalid PROJECT_ID format")

    def test_m3_path2_file_not_found(self):
        """Path 2: flows.json is missing."""
        if os.path.exists("flows.json"):
            os.remove("flows.json")
        em = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            em.check_project_budget("11111111111111111111111111111111")
        self.assertEqual(context.exception.message, "File not found or cannot be read")

    def test_m3_path3_empty_list_loop_bypass(self):
        """Path 3 & Loop (0 iter): File exists but contains an empty list."""
        with open("flows.json", "w", encoding="utf-8") as f:
            json.dump([], f)
        em = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            em.check_project_budget("11111111111111111111111111111111")
        self.assertEqual(context.exception.message, "Project not found in flows")
        if os.path.exists("flows.json"):
            os.remove("flows.json")

    def test_m3_path4_id_not_found(self):
        """Path 4: File contains data, but requested ID is not in the file."""
        data = [{"PROJECT ID": "22222222222222222222222222222222", "inflow": "100.00"}]
        with open("flows.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        em = EnterpriseManager()
        with self.assertRaises(EnterpriseManagementException) as context:
            em.check_project_budget("11111111111111111111111111111111")
        self.assertEqual(context.exception.message, "Project not found in flows")
        if os.path.exists("flows.json"):
            os.remove("flows.json")

    def test_m3_path7_valid_mixed_operations(self):
        """Path 7 & Loop (n iter): Valid ID with multiple inflows/outflows."""
        data = [
            {"PROJECT ID": "22222222222222222222222222222222", "inflow": "500.00"},
            {"PROJECT ID": "11111111111111111111111111111111", "inflow": "100.00"},
            {"PROJECT ID": "11111111111111111111111111111111", "outflow": "30.00"}
        ]
        with open("flows.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        em = EnterpriseManager()
        result = em.check_project_budget("11111111111111111111111111111111")
        self.assertTrue(result)
        if os.path.exists("flows.json"):
            os.remove("flows.json")
        # Clean up the generated output file
        output_file = "budget_11111111111111111111111111111111.json"
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == '__main__':
    unittest.main()