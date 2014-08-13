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

class CheckpointTests(MavensMateTest):
 
    def test_01_should_create_new_stack_trace(self): 
        test_helper.create_project(self, "unit test tooling project")
        stdin = {
            "project_name"      : "unit test tooling project",
            "type"              : "user",
            "debug_categories"  : {
                "ApexCode"      : "DEBUG",
                "Visualforce"   : "DEBUG"
            }
        }
        mm_response = self.runCommand('new_log', stdin)        
        self.assertEqual(mm_response['success'],True)
        self.assertTrue('id' in mm_response and len(mm_response['id']) is 18)

    def test_02_should_delete_all_apex_checkpoints(self):
        stdin = {
            "project_name"      : "unit test tooling project",
        }
        mm_response = self.runCommand('delete_all_apex_checkpoints', stdin)
        self.assertEqual(mm_response['success'],True)

    def test_03_should_create_new_apex_checkpoint(self): 
        ###CREATE APEX CLASS
        stdin = {
            'project_name' : 'unit test tooling project',
            'metadata_type': 'ApexClass', 
            'params': {'api_name': 'unittesttoolingapexclass'}, 
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
        
        if 'success' in mm_response and mm_response['success']:
            self.assertTrue(mm_response['success'] == True)
            self.assertTrue('id' in mm_response and len(mm_response['id']) is 18)
        elif 'success' in mm_response and not mm_response['success']:
            if 'body' in mm_response and mm_response['body'] == 'This API name is already in use in your org.':
                # probably by accident, this is ok bc we clean it up at the end
                pass
        
        ###CREATE CHECKPOINT
        stdin = {
            "project_name"      : "unit test tooling project",
            "IsDumpingHeap"     : True, 
            "Iteration"         : 1, 
            "Object_Type"       : "ApexClass", 
            "Line"              : 1,
            "ActionScriptType"  : "None", 
            "API_Name"          : "unittesttoolingapexclass"
        }
        mm_response = self.runCommand('new_apex_overlay', stdin)        
        self.assertEqual(mm_response['success'],True)

        ###DELETE CLASS
        client_settings = util.parse_json_from_file(os.path.join(test_helper.base_test_directory, "user_client_settings.json"))
        stdin = {
            "files": [os.path.join(client_settings["mm_workspace"],"unit test tooling project","src","classes","unittesttoolingapexclass.cls")], 
            "project_name": "unit test tooling project"
        }
        mm_response = self.runCommand('delete', stdin)        
        self.assertEqual(mm_response['success'],True)

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test tooling project")):
            shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test tooling project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test tooling project")):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test tooling project"))
    unittest.main()