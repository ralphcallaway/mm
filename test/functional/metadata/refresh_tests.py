import os
import sys
import unittest
import mock
import shutil
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
import test_util as util
from lib.request import MavensMateRequestHandler
import test_helper
from test_helper import MavensMateTest
import lib.request as request

base_test_directory = os.path.dirname(os.path.dirname(__file__))
project_name = "unit test metadata refresh project"

class MetadataRefreshTest(MavensMateTest):
    
    def test_01_should_refresh_apex_class(self): 
        apex_class_name =  "unittestapexclass"
        files = [os.path.join(test_helper.base_test_directory,"test_workspace",project_name,"src","classes",apex_class_name+".cls")]

        test_helper.create_project(self, project_name)
        test_helper.create_apex_metadata(self, project_name, "ApexClass", apex_class_name)

        stdin = {
            "project_name"  : project_name, 
            "directories"   : [], 
            "files"         : files
        }
        mm_response = self.runCommand('refresh', stdin)
        self.assertTrue(mm_response['success'] == True)
        self.assertEqual("Refresh Completed Successfully",mm_response['body'])
        test_helper.delete_apex_metadata(self, project_name, files=files)

    @classmethod    
    def tearDownClass(self):
        if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace",project_name)):
           shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace",project_name))

if __name__ == '__main__':
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace",project_name)):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace",project_name))
    unittest.main()