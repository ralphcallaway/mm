import os
import unittest
import shutil
import test.lib.test_helper as test_helper
from test.lib.test_helper import MavensMateTest

class ApexUnitTestingTest(MavensMateTest):
        
    def test_01_should_run_tests_async(self): 
        project_name = 'unit test project'
        test_helper.create_project(self, project_name, package={ "ApexClass" : ["CompileAndTest"] })
        
        apex_class_name =  "unittestapexclass"
        files = [os.path.join(test_helper.base_test_directory,"test_workspace",project_name,"src","classes",apex_class_name+".cls")]
        template = {
            'author': 'MavensMate', 
            'name': 'Unit Test', 
            'description': 'Unit test class', 
            'file_name': 'UnitTestApexClass.cls', 
            'params': [
                {
                    'default': 'MyApexClass', 
                    'name': 'api_name', 
                    'description': 'Apex Class API Name'
                }
            ]
        }
        test_helper.create_apex_metadata(self, project_name, "ApexClass", apex_class_name, template)
        stdin = {
            "project_name"  : project_name,
            "classes"       : ["unittestapexclass"]
        }
        mm_response = self.runCommand('test_async', stdin)
        self.assertTrue(len(mm_response) == 1)
        self.assertTrue(mm_response[0]['Status'] == 'Completed')
        self.assertTrue('ExtendedStatus' in mm_response[0])
        test_helper.delete_apex_metadata(self, project_name, files=files)

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project")):
            shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project"))

if __name__ == '__main__':
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project")):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace","unit test project"))
    unittest.main()
