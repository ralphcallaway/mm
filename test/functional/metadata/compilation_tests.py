#TO RUN: joey2 project_operation_tests.py
import os
import unittest
import shutil
import test.lib.test_helper as test_helper
from test.lib.test_helper import MavensMateTest

class CompilationTests(MavensMateTest):
    
    def test_01_should_compile_with_tooling_api(self):         
        test_helper.create_project(self, "unit test metadata project")
        test_helper.create_apex_metadata(self, "unit test metadata project", "ApexClass", "unittestapexclass")
        mm_response = test_helper.compile(self, "unit test metadata project", [os.path.join(test_helper.base_test_directory,"test_workspace","unit test metadata project","src","classes","unittestapexclass.cls")])
        
        self.assertTrue(mm_response['State'] == 'Completed')
        if self.getTestApiVersion() <= 30:
            self.assertTrue(mm_response['CompilerErrors'] == '[]')
        else:
            self.assertTrue('DeployDetails' in mm_response)
            self.assertTrue(mm_response['DeployDetails']['componentSuccesses'] == [])

    def test_02_should_be_a_bad_compile(self):
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