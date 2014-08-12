import os
import sys
import unittest
import mock
import shutil
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
import lib.util as util
from lib.request import MavensMateRequestHandler
import test_util as util
import test_helper
from test_helper import MavensMateTest
import lib.request as request


base_test_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class CredentialsTest(MavensMateTest):
        
    def test_01_create_new_project(self): 
        package = {
            "ApexClass" : "*",
            "ApexPage"  : "*",
            "Report"    : [],
            "Document"  : []
        }
        stdin = test_helper.create_project("unit test project", package=package)
        mm_response = self.output.getvalue()
        sys.stdout = self.saved_stdout
        print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == True)
        self.assertTrue(mm_json_response['body'] == 'Project Retrieved and Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'])))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'classes')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'pages')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'reports')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'documents')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'documents', 'MavensMate_Documents')))

    def test_02_update_project_credentials_bad_creds(self):
        commandOut = self.redirectStdOut()
        stdin = {
            "project_name" : "unit test project",
            "username" : "mm@thiswontwork.com",
            "password" : "foobarbat"
        }
        request.get_request_payload = mock.Mock(return_value=stdin)
        sys.argv = ['mm.py', '-o', 'update_credentials']
        MavensMateRequestHandler().execute()
        mm_response = commandOut.getvalue()
        sys.stdout = self.saved_stdout
        print 'test_02_update_project_credentials_bad_creds --->'
        print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == False)
        self.assertTrue(mm_json_response['body'] == 'Please provide an org_type (developer, production, sandbox, prerelease)')

    def test_03_update_project_credentials_no_username(self):
        commandOut = self.redirectStdOut()
        stdin = {
            "project_name" : "unit test project",
            "username" : "mm@thiswontwork.com",
        }
        request.get_request_payload = mock.Mock(return_value=stdin)
        sys.argv = ['mm.py', '-o', 'update_credentials']
        MavensMateRequestHandler().execute()
        mm_response = commandOut.getvalue()
        sys.stdout = self.saved_stdout
        print 'test_03_update_project_credentials_no_username --->'
        print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == False)
        self.assertTrue(mm_json_response['body'] == 'Please provide username and password')

    def test_04_update_project_credentials(self):
        commandOut = self.redirectStdOut()
        stdin = {
            "project_name" : "unit test project",
            "username" : "mm@force.com",
            "password" : "force",
            "org_type" : "developer"
        }
        request.get_request_payload = mock.Mock(return_value=stdin)
        sys.argv = ['mm.py', '-o', 'update_credentials']
        MavensMateRequestHandler().execute()
        mm_response = commandOut.getvalue()
        sys.stdout = self.saved_stdout
        print 'test_04_update_project_credentials_no_u --->'
        print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == True)
        self.assertTrue(mm_json_response['body'] == 'Your credentials were updated successfully')


    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))
    unittest.main()