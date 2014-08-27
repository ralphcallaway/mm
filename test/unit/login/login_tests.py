import os
import unittest
import test.lib.test_helper as test_helper
from test.lib.test_helper import MavensMateTest
import test.lib.mock_helper as mock_helper
base_test_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

project_name = 'unit test project'

class LoginUnitTest(MavensMateTest):

    def test_should_get_active_session(self): 
        stdin = {
            "username" : test_helper.get_creds()['username'],
            "password" : test_helper.get_creds()['password'],
            "org_type" : test_helper.get_creds()['org_type']
        }
        
        mock_helper.mock_login_and_describe()

        mm_response = self.runCommand('get_active_session', stdin)
        self.assertEqual(mm_response['success'], True)
        self.assertEqual(len(mm_response['user_id']), 18)

    def test_should_prompt_for_password(self): 
        stdin = {
            "username" : test_helper.get_creds()['username']
        }
        
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertEqual(mm_response['success'], False) 
        self.assertTrue('Please enter a Salesforce.com password' in mm_response['body'])

    def test_should_prompt_for_username(self): 
        stdin = {
            "password" : test_helper.get_creds()['password']
        }
        
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertEqual(mm_response['success'], False) 
        self.assertTrue('Please enter a Salesforce.com username' in mm_response['body'])

    def test_should_prompt_for_org_type(self): 
        stdin = {
            "username" : test_helper.get_creds()['username'],
            "password" : test_helper.get_creds()['password']
        }
        
        mm_response = self.runCommand('get_active_session', stdin)
        self.assertEqual(mm_response['success'], False) 
        self.assertEqual(mm_response['body'], 'Please select an org type')

    def test_should_return_bad_creds_message(self): 
        stdin = {
            "username" : 'thiswontwork@foo.com',
            "password" : 'boobarbat',
            "org_type" : test_helper.get_creds()['org_type']
        }
        
        mock_helper.mock_invalid_login()

        mm_response = self.runCommand('get_active_session', stdin)
        self.assertEqual(mm_response['success'], False)

if __name__ == '__main__':
    unittest.main()