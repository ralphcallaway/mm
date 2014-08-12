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
        
    def test_01_should_create_new_project(self): 
        package = {
            "ApexClass" : "*",
            "ApexPage"  : "*",
            "Report"    : [],
            "Document"  : []
        }
        project_name = 'unit test project'
        mm_response = test_helper.create_project(self, project_name, package=package)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(mm_response['body'] == 'Project Retrieved and Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name)))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'classes')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'pages')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'reports')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'documents')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'documents', 'MavensMate_Documents')))

    def test_02_should_edit_project(self): 
        project_name = 'unit test project'
        mm_response = test_helper.edit_project(self, project_name, package={ "ApexClass" : "*" } )
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(mm_response['body'] == 'Project Edited Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name)))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'classes')))
        self.assertFalse(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'pages')))
        self.assertFalse(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'reports')))
        self.assertFalse(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'documents')))

    def test_03_should_clean_project(self):
        project_name = 'unit test project'
        mm_response = test_helper.clean_project(self, project_name)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(mm_response['body'] == 'Project Cleaned Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name)))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'classes')))
        self.assertFalse(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'pages')))
        self.assertFalse(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'reports')))
        self.assertFalse(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'documents')))

    def test_04_should_compile_project(self):
        project_name = 'unit test project'
        mm_response = test_helper.compile_project(self, project_name)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name)))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'classes')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'package.xml')))

    def test_05_should_update_project_subscription(self):
        stdin = {
            "subscription" : ["ApexPage","ApexComponent"], 
            "project_name" : "unit test project" 
        }
        mm_response = self.runCommand('update_subscription', stdin)
        self.assertTrue(mm_response['success'] == True)
        project_settings = util.parse_json_file(os.path.join(base_test_directory, 'test_workspace', 'unit test project', 'config', '.settings'))
        self.assertTrue(type(project_settings['subscription']) is list and len(project_settings['subscription']) == 2)
        self.assertTrue(project_settings['subscription'][0] == "ApexPage")
        self.assertTrue(project_settings['subscription'][1] == "ApexComponent")

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))
    unittest.main()