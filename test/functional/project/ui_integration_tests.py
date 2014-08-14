#TO RUN: joey2 project_operation_tests.py
import os
import unittest
import shutil
import test.lib.test_helper as test_helper
from test.lib.test_helper import MavensMateTest

base_test_directory = test_helper.base_test_directory

class ProjectUiIntegrationTest(MavensMateTest):
        
    def test_01_should_not_get_active_session_bc_bad_creds(self): 
        stdin = {
            "username" : "mm2@force.commm",
            "password" : "forceee",
            "org_type" : "developer"
        }
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertEqual(mm_response['success'], False)
        self.assertEqual(mm_response['body'], "Server raised fault: 'INVALID_LOGIN: Invalid username, password, security token; or user locked out.'")

    def test_02_should_not_get_active_session_bc_bad_request(self): 
        stdin = {
            "username" : "mm2@force.com"
        }
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertEqual(mm_response['success'], False)
        self.assertEqual(mm_response['body'], "Please enter a Salesforce.com password")

    def test_03_should_get_active_session_good_creds(self): 
        stdin = {
            "username" : "mm2@force.com",
            "password" : "force",
            "org_type" : "developer"
        }
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(len(mm_response['user_id']), 18)

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))
    unittest.main()