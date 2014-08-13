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

class ProjectCreateTest(MavensMateTest):
        
    def test_should_create_new_project(self): 
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

    def test_should_except_for_bad_package(self): 
        package = {}
        mm_response = test_helper.create_project(self, "unit test project", package=package)
        self.assertTrue(mm_response['success'] == False)
        self.assertTrue(mm_response['body'] == 'Invalid package')

    def test_should_create_new_project_with_all_objects(self): 
        package = {
            "CustomObject" : "*"
        }
        project_name = 'unit test project'
        mm_response = test_helper.create_project(self, project_name, package=package)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(mm_response['body'] == 'Project Retrieved and Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name)))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'objects')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'objects', 'Account.object')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'objects', 'Opportunity.object')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'objects', 'Lead.object')))

    def test_should_create_new_project_based_on_package_xml_file(self): 
        package = os.path.join(base_test_directory, 'functional', 'project', 'package.xml')
        project_name = 'unit test project'
        mm_response = test_helper.create_project(self, project_name, package=package)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(mm_response['body'] == 'Project Retrieved and Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name)))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'classes')))

    def test_should_create_project_from_existing_directory(self): 
        if os.path.exists(os.path.join(base_test_directory,"functional","project","existing-project-copy")):
            shutil.rmtree(os.path.join(base_test_directory,"functional","project","existing-project-copy"))

        if not os.path.exists(os.path.join(base_test_directory, 'functional', 'project', 'existing-project-copy')):
            shutil.copytree(os.path.join(base_test_directory, 'functional', 'project', 'existing-project'), os.path.join(base_test_directory, 'functional', 'project', 'existing-project-copy'))

        stdin = {
            "project_name"  : "existing-project-copy",
            "username"      : "mm@force.com",
            "password"      : "force",
            "org_type"      : "developer",
            "directory"     : os.path.join(base_test_directory, 'functional', 'project', 'existing-project-copy'),
            "action"        : "new",
            "workspace"     : os.path.join(base_test_directory, 'test_workspace'),
            "action"        : "existing"
        }
        project_name = 'existing-project-copy'
        mm_response = self.runCommand('new_project_from_existing_directory', stdin)
        self.assertTrue(mm_response['success'] == True)
        self.assertTrue(mm_response['body'] == 'Project Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name)))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'classes')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'objects')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', project_name, 'config')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.session')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', project_name, 'config', '.settings')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', project_name, 'src', 'package.xml')))


    def tearDown(self):
        super(ProjectCreateTest, self).tearDown()
        if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))

        if os.path.exists(os.path.join(base_test_directory,"test_workspace","existing-project-copy")):
            shutil.rmtree(os.path.join(base_test_directory,"test_workspace","existing-project-copy"))

        if os.path.exists(os.path.join(base_test_directory,"functional","project","existing-project-copy")):
            shutil.rmtree(os.path.join(base_test_directory,"functional","project","existing-project-copy"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(base_test_directory,"test_workspace","unit test project"))
    unittest.main()