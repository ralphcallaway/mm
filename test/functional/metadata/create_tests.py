#TO RUN: joey2 project_operation_tests.py
import os
import sys
import unittest
import mock
import shutil
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
import test_util as test_util
import test_helper
from test_helper import MavensMateTest
from lib.request import MavensMateRequestHandler
import lib.request as request
import lib.util as mmutil

class MetadataOperationTest(MavensMateTest):
    
    def test_01_should_create_new_apex_class(self): 
        test_helper.create_project(self, "unit test metadata project")        
        stdin = {
            'project_name' : 'unit test metadata project',
            'metadata_type': 'ApexClass', 
            'params': {'api_name': 'unittestapexclass'}, 
            'github_template': {
                'author': 'MavensMate', 
                'name': 'Default', 
                'description': 'The default template for an Apex Class', 
                'file_name': 'ApexClass.cls', 
                'params': [
                    {
                        'default': 'MyApexClass', 
                        'name': 'api_name', 
                        'description': 'Apex Class API Name'
                    }
                ]
            }
        }
        mm_response = self.runCommand('new_metadata', stdin)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue('id' in mm_response and len(mm_response['id']) is 18)

    def test_02_should_compile_apex_class(self): 
        test_helper.create_project(self, "unit test metadata project")
        client_settings = mmutil.parse_json_from_file(os.path.join(test_helper.base_test_directory, "user_client_settings.json"))
        stdin = {
            "project_name": "unit test metadata project", 
            "files": [os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project","src","classes","unittestapexclass.cls")] 
        }
        mm_response = self.runCommand('compile', stdin)
        self.assertTrue(mm_response['State'] == "Completed")
        self.assertTrue(mm_response['ErrorMsg'] == None)

    def test_03_should_delete_apex_class(self): 
        client_settings = mmutil.parse_json_from_file(os.path.join(test_helper.base_test_directory, "user_client_settings.json"))
        stdin = {
            "files": [os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project","src","classes","unittestapexclass.cls")], 
            "project_name": "unit test metadata project"
        }
        mm_response = self.runCommand('delete', stdin)
        self.assertTrue(mm_response['success'] == True)

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project")):
           shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project"))
        #pass

if __name__ == '__main__':
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project")):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project"))
    unittest.main()