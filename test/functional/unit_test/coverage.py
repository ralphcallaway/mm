import os
import sys
import unittest
import mock
import shutil
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
import lib.util as util
import test_util as test_util
import test_helper
from test_helper import MavensMateTest
from lib.request import MavensMateRequestHandler
import lib.request as request

class ApexUnitTestCoverageTest(MavensMateTest):
        
    def test_01_should_get_coverage(self): 
        test_helper.create_project(self, "unit test project", package={ "ApexClass" : "*" })
        stdin = {
            "project_name"  : "unit test project"
        }
        mm_response = self.runCommand('code_coverage_report', stdin)
        self.assertTrue(mm_json_response['totalSize'] > 0)
        self.assertTrue(mm_json_response['done'] == True)
        self.assertTrue(mm_json_response['entityTypeName'] == "ApexCodeCoverageAggregate")

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project"))
    unittest.main()
