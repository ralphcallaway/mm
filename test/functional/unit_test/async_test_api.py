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

class ApexUnitTestingTest(MavensMateTest):
        
    def test_01_should_run_tests_async(self): 
        test_helper.create_project(self, "unit test project", package={ "ApexClass" : ["CompileAndTest"] })
        stdin = {
            "project_name"  : "unit test project",
            "classes"       : ["CompileAndTest"]
        }
        mm_response = self.runCommand('test_async', stdin)
        self.assertTrue(len(mm_response) == 1)
        self.assertTrue(mm_response[0]['Status'] == 'Completed')

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project"))
    unittest.main()
