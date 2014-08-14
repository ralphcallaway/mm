import os
import unittest
import shutil
import test.lib.test_helper as test_helper
from test.lib.test_helper import MavensMateTest

class ApexUnitTestCoverageTest(MavensMateTest):
        
    def test_01_should_get_coverage(self): 
        test_helper.create_project(self, "unit test project", package={ "ApexClass" : "*" })
        stdin = {
            "project_name"  : "unit test project"
        }
        mm_response = self.runCommand('code_coverage_report', stdin)
        self.assertTrue('NumLinesCovered' in mm_response[0])

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project"))
    unittest.main()
