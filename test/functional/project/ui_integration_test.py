#TO RUN: joey2 project_operation_tests.py
import os
import sys
import unittest
import mock
import shutil
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
import test_util as util
from lib.request import MavensMateRequestHandler
import test_helper
from test_helper import MavensMateTest
import lib.request as request

base_test_directory = test_helper.base_test_directory

class ProjectUiIntegrationTest(MavensMateTest):
        
    def test_01_should_not_get_active_session_bc_bad_creds(self): 
        stdin = {
            "username" : "mm2@force.commm",
            "password" : "forceee",
            "org_type" : "developer"
        }
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertTrue(mm_response['success'] == False)
        self.assertTrue(mm_response['body'] == "Server raised fault: 'INVALID_LOGIN: Invalid username, password, security token; or user locked out.'")

    def test_02_should_not_get_active_session_bc_bad_request(self): 
        stdin = {
            "username" : "mm2@force.com"
        }
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertTrue(mm_response['success'] == False)
        self.assertTrue(mm_response['body'] == "Please enter a Salesforce.com password")

    def test_03_should_get_active_session_good_creds(self): 
        stdin = {
            "username" : "mm2@force.com",
            "password" : "force",
            "org_type" : "developer"
        }
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(len(mm_response['user_id']) is 18)

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))
    unittest.main()