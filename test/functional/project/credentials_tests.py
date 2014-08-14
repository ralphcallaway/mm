import os
import unittest
import shutil
import test.lib.test_helper as test_helper
from test.lib.test_helper import MavensMateTest

base_test_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class CredentialsTest(MavensMateTest):
        
    def test_01_should_create_new_project(self): 
        package = {
            "ApexClass" : "*",
            "ApexPage"  : "*",
            "Report"    : [],
            "Document"  : []
        }
        mm_response = test_helper.create_project(self, "unit test project", package=package)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(mm_response['body'] == 'Project Retrieved and Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', 'unit test project')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', 'unit test project', 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', 'unit test project', 'src', 'classes')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', 'unit test project', 'src', 'pages')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', 'unit test project', 'src', 'reports')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', 'unit test project', 'src', 'documents')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', 'unit test project', 'src', 'documents', 'MavensMate_Documents')))

    def test_02_should_not_update_project_credentials_bc_bad_creds(self):
        stdin = {
            "project_name" : "unit test project",
            "username" : "mm2@thiswontwork.com",
            "password" : "foobarbat"
        }
        mm_response = self.runCommand('update_credentials', stdin)
        self.assertTrue(mm_response['success'] == False)
        self.assertTrue(mm_response['body'] == 'Please provide an org_type (developer, production, sandbox, prerelease)')

    def test_03_should_not_update_project_credentials_bc_no_username(self):
        stdin = {
            "project_name" : "unit test project",
            "username" : "mm2@thiswontwork.com",
        }
        mm_response = self.runCommand('update_credentials', stdin)
        self.assertTrue(mm_response['success'] == False)
        self.assertTrue(mm_response['body'] == 'Please provide username and password')

    def test_04_should_update_project_credentials(self):
        stdin = {
            "project_name" : "unit test project",
            "username" : "mm2@force.com",
            "password" : "force",
            "org_type" : "developer"
        }
        mm_response = self.runCommand('update_credentials', stdin)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(mm_response['body'] == 'Your credentials were updated successfully')


    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))
    unittest.main()