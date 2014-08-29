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
            "username" : test_helper.get_creds()['username']
        }
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertEqual(mm_response['success'], False)
        self.assertEqual(mm_response['body'], "Please enter a Salesforce.com password")

    def test_03_should_get_active_session_and_list_apex_classes(self): 
        stdin = {
            "username" : test_helper.get_creds()['username'],
            "password" : test_helper.get_creds()['password'],
            "org_type" : test_helper.get_creds()['org_type']
        }
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(len(mm_response['user_id']), 18)

        stdin = {
            'sid' : mm_response['sid'],
            'metadata_server_url' : mm_response['metadata_server_url'],
            'metadata_type' : 'ApexClass',
            'server_url' : mm_response['server_url'],
            'defer_connection' : True
        }
        mm_response = self.runCommand('list_metadata', stdin, return_format='json')
        self.assertEqual(type(mm_response), list)

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))
    unittest.main()