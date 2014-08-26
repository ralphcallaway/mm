#from __future__ import absolute_import
import os.path
import sys
import unittest
import mock
from mock import patch
from StringIO import StringIO
import test_util as util
import json

import mm.request as request
from mm.request import MavensMateRequestHandler
from mm.connection import PluginConnection
import mm.util as mmutil

base_test_directory = os.path.dirname(os.path.dirname(__file__))

class MavensMateTest(unittest.TestCase):

    # redirects standard out to a new target
    def redirectStdOut(self):
        new_target = StringIO()
        sys.stdout = new_target
        return new_target

    # runs an mm command, prints to command-specific stdout
    def runCommand(self, command_name_or_argv, stdin, as_json=True, print_before_deserialization=True, **kwargs):
        commandOut = self.redirectStdOut()
        request.get_request_payload = mock.Mock(return_value=stdin)
        if type(command_name_or_argv) is list:
            sys.argv = command_name_or_argv
        else:
            sys.argv = ['mm.py', '-o', command_name_or_argv]
        
        MavensMateRequestHandler().execute()
        mm_response = commandOut.getvalue()

        sys.stdout = self.saved_stdout

        if print_before_deserialization:
            if type(command_name_or_argv) is list:
                print '\n\n['+str(command_name_or_argv[2])+'] ------->\n'
            else:
                print '\n\n['+str(command_name_or_argv)+'] ------->\n'

            print '\n[STDIN] -->\n'
            print json.dumps(stdin)
            print '\n[STDOUT] -->\n'
            print mm_response
        if as_json:
            mm_response = util.parse_mm_response(mm_response)
        return mm_response

    # runs before every test method
    def setUp(self):
        # self.commandStdOut = StringIO();

        self.output = StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.output

        # get settings from test client settings (modeled after ST3 settings)
        # found in default_client_settings.json and user_client_settings.json
        self.settings = util.get_plugin_client_settings()
        
        # test suite runs for each supported version of the api
        api_version = os.environ.get('SFDC_API_VERSION', 30.0)
        self.settings['user']['mm_api_version'] = api_version
        
        # set up CI-specific settings
        is_ci = os.environ.get('CI') == 'true' or os.environ.get('CI') == True or os.environ.get('MM_TESTING') == True or os.environ.get('MM_TESTING') == 'true'
        if is_ci:
            self.settings['user']['mm_workspace'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_workspace')
            self.settings['user']['mm_use_keyring'] = False
        PluginConnection.get_plugin_client_settings = mock.Mock(return_value=self.settings)

    def tearDown(self):
        self.output.close()
        sys.stdout = self.saved_stdout

    def getTestApiVersion(self):
        test_api_version = os.environ.get('SFDC_API_VERSION', '30.0')
        return int(float(test_api_version))

def get_creds():
    return {
        'username': os.getenv('SFDC_USERNAME', 'mm@force.com'),
        'password': os.getenv('SFDC_PASSWORD', 'force'),
        'org_type': os.getenv('SFDC_ORG_TYPE', 'developer'),
    }

def get_fixture_response(command_name_or_argv):
    if type(command_name_or_argv) is list:
        command_name = command_name_or_argv[2]
    else:
        command_name = command_name_or_argv 
    try:
        return util.parse_json_file(os.path.join(base_test_directory,'lib','fixtures',command_name+'.json'))
    except:
        return mmutil.generate_error_response('Could not find test fixture response for command: '+command_name)

def create_project(clz, name="unit test project", package=None, **kwargs):
    if package is None:
        package = { "ApexClass" : "*" } 
    stdin = {
        "project_name"  : name,
        "username"      : get_creds()['username'],
        "password"      : get_creds()['password'],
        "org_type"      : get_creds()['org_type'],
        "action"        : "new",
        "package"       : package
    }
    return clz.runCommand(['mm.py', '-o', 'new_project', '-f', 'json'], stdin, **kwargs)

def edit_project(clz, name="unit test project", package=None):
    if package is None:
        package = { "ApexClass" : "*" } 
    stdin = {
        "project_name"  : name,
        "package"       : package
    }
    return clz.runCommand(['mm.py', '-o', 'edit_project', '-f', 'json'], stdin)


def clean_project(clz, name="unit test project"): 
    stdin = {
        "project_name"  : name
    }
    return clz.runCommand(['mm.py', '-o', 'clean_project', '-f', 'json'], stdin)

def compile(clz, name="unit test project", files=[]): 
    stdin = {
        "project_name"  : name,
        "files"         : files
    }
    return clz.runCommand(['mm.py', '-o', 'compile', '-f', 'json'], stdin)
    
def compile_project(clz, name="unit test project"): 
    stdin = {
        "project_name"  : name
    }
    return clz.runCommand(['mm.py', '-o', 'compile_project', '-f', 'json'], stdin)
   
def create_apex_metadata(clz, project_name, metadata_type="ApexClass", api_name="unittestapexclass", template=None, params=None):
    if template == None:
        template = {
            'author': 'MavensMate', 
            'name': 'Default', 
            'description': 'The default template for an Apex Class', 
            'file_name': 'ApexClass.cls', 
            'params': [
                {
                    'default': 'MyApexClass', 
                    'name': 'api_name', 
                    'description': 'Apex Class API Name'
                }
            ]
        } 
    if params == None:
        params = {'api_name': api_name}  
    stdin = {
        'project_name' : project_name,
        'metadata_type': metadata_type, 
        'apex_trigger_object_api_name' : None, 
        'apex_class_type' : None, 
        'params': params, 
        'github_template': template
    }
    return clz.runCommand(['mm.py', '-o', 'new_metadata', '-f', 'json'], stdin)
   
def delete_apex_metadata(clz, project_name, files=[], dirs=[]):
   stdin = {
       "files": files, 
       "project_name": project_name
   }
   return clz.runCommand(['mm.py', '-o', 'delete', '-f', 'json'], stdin)