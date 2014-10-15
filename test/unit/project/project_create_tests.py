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

    def test_should_notify_user_of_duplicate_project_name_in_workspace(self):
        os.mkdir(os.path.join(base_test_directory, 'test_workspace', 'test_should_notify_user_of_duplicate_project_name_in_workspace'))

        package = { "ApexClass" : "*" }
        mock_helper.mock_login_and_describe()
        
        mm_response = test_helper.create_project(self, 'test_should_notify_user_of_duplicate_project_name_in_workspace', package)
        self.assertEquals(False, mm_response['success'])
        self.assertTrue('A project with this name already exists in your workspace' in mm_response['body'])

        shutil.rmtree(os.path.join(base_test_directory,"test_workspace",'test_should_notify_user_of_duplicate_project_name_in_workspace'))

    def test_should_prompt_for_username(self):
        stdin = {
            "project_name"  : 'foo'
        }
        mm_response = self.runCommand('new_project', stdin)
        self.assertEquals(False, mm_response['success'])
        self.assertTrue('Please specify a username' in mm_response['body'])

    def test_should_prompt_for_password(self):
        stdin = {
            "project_name"  : 'foo',
            "username" : 'foo'
        }
        mm_response = self.runCommand('new_project', stdin)
        self.assertEquals(False, mm_response['success'])
        self.assertTrue('Please specify a password' in mm_response['body'])

    def test_should_prompt_for_org_type(self):
        stdin = {
            "project_name"  : project_name,
            "username" : 'foo',
            "password" : 'foo'
        }
        mm_response = self.runCommand('new_project', stdin)
        self.assertEquals(False, mm_response['success'])
        self.assertTrue('Please specify org_type' in mm_response['body'])

    def test_should_except_for_empty_package_dict(self): 
        package = {}
        mock_helper.mock_login_and_describe()
        mm_response = test_helper.create_project(self, "test_should_except_for_empty_package_dict", package=package)
        self.assertTrue(mm_response['success'] == False)
        self.assertTrue(mm_response['body'] == 'Invalid package')

    def test_should_retrieve_empty_project(self): 
        package = os.path.join(os.path.join(base_test_directory, 'unit', 'project', 'empty_package.xml'))
        mock_helper.mock_login_and_describe()
        mm_response = test_helper.create_project(self, "test_should_retrieve_empty_project", package=package)
        self.assertTrue(mm_response['success'] == True)

    def test_should_create_project_with_default_metadata(self):
        stdin = {
            "project_name"  : project_name,
            "username" : 'mm@force.com',
            "password" : 'force',
            "org_type" : 'developer'
        }

        mock_helper.mock_login_and_describe()

        # mock retrieve call
        MavensMateClient.retrieve = mock.Mock(return_value=MockRetrieveResponse())
        MavensMateClient.get_metadata_container_id = mock.Mock(return_value='12345')

        mm_response = self.runCommand('new_project', stdin)
        self.assertEquals(True, mm_response['success'])
        self.assertEquals('Project Retrieved and Created Successfully', mm_response['body'])
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name)))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'components')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.settings')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.session')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.describe')))

        shutil.rmtree(os.path.join(base_test_directory,"test_workspace",project_name))
    
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
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.settings')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.session')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.describe')))

        shutil.rmtree(os.path.join(base_test_directory,"test_workspace",project_name))

    def test_should_create_new_project_from_existing_directory(self): 
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
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.settings')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.session')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.describe')))

        shutil.rmtree(os.path.join(base_test_directory,"test_workspace",project_name))

    def test_should_create_project_from_existing_directory(self): 
        if os.path.exists(os.path.join(base_test_directory,"unit","project","existing-project-copy")):
            shutil.rmtree(os.path.join(base_test_directory,"unit","project","existing-project-copy"))

        if not os.path.exists(os.path.join(base_test_directory, 'unit', 'project', 'existing-project-copy')):
            shutil.copytree(os.path.join(base_test_directory, 'unit', 'project', 'existing-project'), os.path.join(base_test_directory, 'unit', 'project', 'existing-project-copy'))

        stdin = {
            "project_name"  : "existing-project-copy",
            "username"      : test_helper.get_creds()['username'],
            "password"      : test_helper.get_creds()['password'],
            "org_type"      : test_helper.get_creds()['org_type'],
            "directory"     : os.path.join(base_test_directory, 'unit', 'project', 'existing-project-copy'),
            "workspace"     : os.path.join(base_test_directory, 'test_workspace'),
            "action"        : "existing"
        }

        mock_helper.mock_login_and_describe()

        MavensMateClient.retrieve = mock.Mock(return_value=MockRetrieveResponse())
        MavensMateClient.get_metadata_container_id = mock.Mock(return_value='12345')

        pn = 'existing-project-copy'
        mm_response = self.runCommand('new_project_from_existing_directory', stdin)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(mm_response['body'] == 'Project Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', pn)))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', pn, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', pn, 'src', 'classes')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', pn, 'src', 'objects')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', pn, 'config')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', pn, 'config', '.session')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', pn, 'config', '.settings')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', pn, 'src', 'package.xml')))

        shutil.rmtree(os.path.join(base_test_directory,"test_workspace","existing-project-copy"))

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace",project_name)):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace",project_name))

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace",project_name)):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace",project_name))
    unittest.main()