#TO RUN: joey2 project_operation_tests.py
import os
import unittest
import shutil
import test.lib.test_util as test_util
import test.lib.test_helper as test_helper
from test.lib.test_helper import MavensMateTest
import mm.util as mmutil

class DeployTest(MavensMateTest):
    
    def test_01_should_create_new_org_connection(self): 
        test_helper.create_project(self, "unit test deploy project")
        stdin = {
            "username"      : test_helper.get_creds()['username'],
            "password"      : test_helper.get_creds()['password'],
            "org_type"      : test_helper.get_creds()['org_type'],
            "project_name"  : "unit test deploy project"
        }
        mm_response = self.runCommand('new_connection', stdin)        
        self.assertTrue(mm_response['success'] == True)

    def test_02_should_unsuccessfully_try_to_create_new_org_connection(self): 
        stdin = {
            "username"      : "mm22222222@force.com",
            "password"      : "force",
            "org_type"      : "developer",
            "project_name"  : "unit test deploy project"
        }
        mm_response = self.runCommand('new_connection', stdin)        
        self.assertTrue(mm_response['success'] == False)
        self.assertTrue('INVALID_LOGIN' in mm_response['body'])

    # dependent on test 1 completing for org connections to be present
    def test_03_should_try_deploy_receive_compare_result(self): 
        test_helper.create_apex_metadata(self, "unit test deploy project", "ApexClass", "test_deployapexclass")
        org_connections = test_util.parse_json_from_file(os.path.join(self.settings['user']['mm_workspace'],"unit test deploy project","config",".org_connections"))
        stdin = {
            "project_name"      :   "unit test deploy project",
            "destinations"      :   [
                {
                    "id"            : org_connections[0]["id"],
                    "username"      : org_connections[0]["username"],
                    "org_type"      : org_connections[0]["environment"]
                }
            ],
            "check_only"        :   True,
            "run_tests"         :   False,
            "rollback_on_error" :   True,
            "package"           :   {
                "ApexClass" : ["test_deployapexclass"]
            },
            "debug_categories"  :   ""
        }
        mm_response = self.runCommand(['mm.py', '-o', 'deploy'], stdin)        
        self.assertTrue(test_helper.get_creds()['username'] in mm_response)
        self.assertTrue('unpackaged/classes/test_deployapexclass.cls' in mm_response[test_helper.get_creds()['username']])

    # dependent on test 1 completing for org connections to be present
    def test_04_should_attempt_deploy_to_bad_org_connection(self): 
        org_connections = test_util.parse_json_from_file(os.path.join(self.settings['user']['mm_workspace'],"unit test deploy project","config",".org_connections"))
        stdin = {
            "project_name"      :   "unit test deploy project",
            "destinations"      :   [
                {
                    "id"            : org_connections[0]["id"],
                    "username"      : "thiswontwork@foo.com",
                    "org_type"      : org_connections[0]["environment"]
                }
            ],
            "check_only"        :   True,
            "run_tests"         :   False,
            "rollback_on_error" :   True,
            "package"           :   {
                "ApexClass" : ["test_deployapexclass"]
            },
            "debug_categories"  :   ""
        }
        mm_response = self.runCommand(['mm.py', '-o', 'deploy'], stdin)        
        self.assertTrue('thiswontwork@foo.com' in mm_response)
        self.assertEquals(False, mm_response['thiswontwork@foo.com']['success'])
        result = test_helper.delete_apex_metadata(self, "unit test deploy project", [os.path.join(test_helper.base_test_directory,"test_workspace","unit test deploy project","src","classes","test_deployapexclass.cls")])

    # dependent on test 1 completing for org connections to be present
    def test_05_should_delete_org_connection(self): 
        org_connections = test_util.parse_json_from_file(os.path.join(self.settings['user']['mm_workspace'],"unit test deploy project","config",".org_connections"))
        stdin = {
            "id"            : org_connections[0]["id"],
            "project_name"  : "unit test deploy project"
        }
        mm_response = self.runCommand('delete_connection', stdin)        
        self.assertTrue(mm_response['success'] == True)

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test deploy project")):
           shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test deploy project"))
        #pass

if __name__ == '__main__':
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test deploy project")):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test deploy project"))
    unittest.main()