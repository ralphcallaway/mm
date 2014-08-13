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

class CompilationTests(MavensMateTest):
    
    def test_01_should_compile_with_tooling_api(self): 
        client_settings = mmutil.parse_json_from_file(os.path.join(test_helper.base_test_directory, "user_client_settings.json"))
        
        test_helper.create_project(self, "unit test metadata project")
        test_helper.create_apex_metadata(self, "unit test metadata project", "ApexClass", "unittestapexclass")
        mm_response = test_helper.compile(self, "unit test metadata project", [os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project","src","classes","unittestapexclass.cls")])
        
        self.assertTrue(mm_response['State'] == 'Completed')
        self.assertTrue(mm_response['CompilerErrors'] == '[]')

    def test_02_should_be_a_bad_compile(self):
        client_settings = mmutil.parse_json_from_file(os.path.join(test_helper.base_test_directory, "user_client_settings.json"))
        src = open(os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project","src","classes","unittestapexclass.cls"), "w")
        src.write('public class unittestapexclass { public unittestapexclass() { String foo } }')
        src.close()

        mm_response = test_helper.compile(self, "unit test metadata project", [os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project","src","classes","unittestapexclass.cls")])
        self.assertTrue(mm_response['State'] == 'Failed')
        result = test_helper.delete_apex_metadata(self, "unit test metadata project", [os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project","src","classes","unittestapexclass.cls")])
        
    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project")):
           shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project"))
        #pass

if __name__ == '__main__':
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project")):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project"))
    unittest.main()