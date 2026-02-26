from unittest import TestCase
from uc3m_consulting import EnterpriseManager

class TestEnterpriseManager(TestCase):
    def test_register_project(self):
        obj=EnterpriseManager()
        obj.register_project('PRO01', '')
        self.fail()
