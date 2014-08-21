import os
import unittest
import shutil
import test.lib.test_helper as test_helper
from test.lib.test_helper import MavensMateTest
from test.lib.fixtures.retrieve import MockRetrieveResponse
base_test_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

project_name = 'unit test project'

class ProjectCreateTest(MavensMateTest):

    def test_01_should_create_new_project(self): 
        package = {
            "ApexClass" : "*",
            "ApexPage"  : "*",
        }
        mm_response = test_helper.create_project(
            self, 
            project_name, 
            package, 
            sfdc_client_function='retrieve', 
            sfdc_client_function_response=MockRetrieveResponse())
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(mm_response['body'] == 'Project Retrieved and Created Successfully')
        self.assertTrue(mm_response['body'] == 'Project Retrieved and Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name)))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'components')))

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace",project_name)):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace",project_name))

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace",project_name)):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace",project_name))
    unittest.main()