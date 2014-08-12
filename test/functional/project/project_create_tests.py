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
        stdin = test_helper.create_project("unit test project", package=package)
        mm_response = self.output.getvalue()
        sys.stdout = self.saved_stdout
        print 'test_should_create_new_project ----->'
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

    def test_should_except_for_bad_package(self): 
        package = {}
        stdin = test_helper.create_project("unit test project", package=package)
        mm_response = self.output.getvalue()
        sys.stdout = self.saved_stdout
        print 'test_should_except_for_bad_package ------>'
        print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == False)
        self.assertTrue(mm_json_response['body'] == 'Invalid package')

    def test_should_create_new_project_with_all_objects(self): 
        package = {
            "CustomObject" : "*"
        }
        stdin = test_helper.create_project("unit test project", package=package)
        mm_response = self.output.getvalue()
        sys.stdout = self.saved_stdout
        print 'test_should_create_new_project_with_all_objects ----->'
        print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == True)
        self.assertTrue(mm_json_response['body'] == 'Project Retrieved and Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'])))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'objects')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'objects', 'Account.object')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'objects', 'Opportunity.object')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'objects', 'Lead.object')))

    def test_should_create_new_project_based_on_package_xml_file(self): 
        package = os.path.join(base_test_directory, 'functional', 'project', 'package.xml')
        stdin = test_helper.create_project("unit test project", package=package)
        mm_response = self.output.getvalue()
        sys.stdout = self.saved_stdout
        print 'test_should_create_new_project_based_on_package_xml_file ----->'
        print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == True)
        self.assertTrue(mm_json_response['body'] == 'Project Retrieved and Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'])))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'classes')))

    def test_should_create_project_from_existing_directory(self): 
        if os.path.exists(os.path.join(base_test_directory,"functional","project","existing-project-copy")):
            shutil.rmtree(os.path.join(base_test_directory,"functional","project","existing-project-copy"))

        if not os.path.exists(os.path.join(base_test_directory, 'functional', 'project', 'existing-project-copy')):
            shutil.copytree(os.path.join(base_test_directory, 'functional', 'project', 'existing-project'), os.path.join(base_test_directory, 'functional', 'project', 'existing-project-copy'))

        commandOut = self.redirectStdOut()
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
        request.get_request_payload = mock.Mock(return_value=stdin)
        sys.argv = ['mm.py', '-o', 'new_project_from_existing_directory']
        MavensMateRequestHandler().execute()
        mm_response = commandOut.getvalue()
        sys.stdout = self.saved_stdout

        print 'test_should_create_project_from_existing_directory ----->'
        print mm_response
        mm_json_response = util.parse_mm_response(mm_response)
        self.assertTrue(mm_json_response['success'] == True)
        self.assertTrue(mm_json_response['body'] == 'Project Created Successfully')
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'])))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'classes')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'objects')))
        self.assertTrue(os.path.exists(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'config')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'config', '.session')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'config', '.settings')))
        self.assertTrue(os.path.isfile(os.path.join(base_test_directory, 'test_workspace', stdin['project_name'], 'src', 'package.xml')))


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