import os
import unittest
import shutil
import mock
import test.lib.test_helper as test_helper
import test.lib.mock_helper as mock_helper
from test.lib.test_helper import MavensMateTest
from test.lib.fixtures.retrieve import MockRetrieveResponse
from mm.sfdc_client import MavensMateClient

base_test_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

project_name = 'unit test project'

class ProjectCreateTest(MavensMateTest):

    def test_should_create_new_project(self): 
        package = {
            "ApexClass" : "*",
            "ApexPage"  : "*",
        }
        mock_helper.mock_login_and_describe()
        
        # mock retrieve call
        MavensMateClient.retrieve = mock.Mock(return_value=MockRetrieveResponse())
        MavensMateClient.get_metadata_container_id = mock.Mock(return_value='12345')

        mm_response = test_helper.create_project(self, project_name, package)
        self.assertEquals(True, mm_response['success'])
        self.assertEquals('Project Retrieved and Created Successfully', mm_response['body'])
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