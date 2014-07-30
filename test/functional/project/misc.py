#TO RUN: joey2 project_operation_tests.py
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

class ProjectTest(MavensMateTest):
        
    def test_01_create_new_project(self): 
        package = {
            "ApexComponent" : "*"
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
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'components')))
       
    def test_02_compile_project(self):
        os.remove(os.path.join(base_test_directory,"test_workspace","unit test project","config",".session"))
        atom_settings = util.parse_json_from_file(os.path.join(base_test_directory,"user_client_settings.json"))
        stdin = {
            'settings' : atom_settings   
        }
        request.get_request_payload = mock.Mock(return_value=stdin)
        sys.argv = ['mm.py', '-o', 'compile_project', '-c', 'ATOM']
        os.chdir(os.path.join(base_test_directory,"test_workspace","unit test project"))
        MavensMateRequestHandler().execute()

        mm_response = self.output.getvalue()
        sys.stdout = self.saved_stdout
        print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == True)

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))
    unittest.main()