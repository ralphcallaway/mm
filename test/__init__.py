import unittest
import sys
import os
import argparse
import shutil
import lib.test_helper as test_helper

from functional.project.project_tests import ProjectTest
from functional.project.project_create_tests import ProjectCreateTest
from functional.project.credentials_tests import CredentialsTest
from functional.unit_test.async_unit_test_api_tests import ApexUnitTestingTest
from functional.metadata.create_tests import MetadataOperationTest
from functional.debug.checkpoint_tests import CheckpointTests
from functional.debug.log_tests import StackTraceAndLogsTest
from functional.metadata.refresh_tests import MetadataRefreshTest
from functional.project.ui_integration_tests import ProjectUiIntegrationTest
from functional.metadata.compilation_tests import CompilationTests

# to run a specific test method in one of the test suite classes:
#     $ python -m unittest project_tests.ProjectTest.test_01_should_create_new_project

def suite():
    test_classes = [
        ApexUnitTestingTest,
        ProjectTest, 
        ProjectCreateTest,
        CredentialsTest,
        MetadataOperationTest,
        MetadataRefreshTest,
        CheckpointTests,
        StackTraceAndLogsTest,
        ProjectUiIntegrationTest,
        CompilationTests
    ]
    suite = unittest.TestSuite()
    for unit_test_class in test_classes:
        for method in dir(unit_test_class):
            if method.startswith("test"):
                suite.addTest(unit_test_class(method))
    return suite

def cleanup_workspaces():
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace")):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace"))

def main():
    cleanup_workspaces()
    
    supported_sfdc_api_versions = ['31.0', '30.0', '29.0']
    testing_api_versions = []

    parser = argparse.ArgumentParser()
    parser.add_argument('--api', help='Salesforce.com API version') # run tests for specific version
    args, unknown = parser.parse_known_args()
    if args.api == None:
        testing_api_versions = supported_sfdc_api_versions
    else:
        testing_api_versions = [args.api]

    results = {}
    for api_version in testing_api_versions:
        os.environ['SFDC_API_VERSION'] = api_version

        runner = unittest.TextTestRunner()
        test_suite = suite()
        test_results = runner.run (test_suite)
        print '===> TEST RESULTS FOR SALESFORCE.COM API VERSION: '+str(api_version)
        print test_results
        if len(test_results.errors) > 0 or len(test_results.failures) > 0:
            results[api_version] = 'failed'

    print '==========> AGGREGATE TEST RESULTS'
    print results

    for key, value in results.iteritems():
        if value == 'failed':
            sys.exit('Test suite for Salesforce.com API version '+str(key)+' failed')


if  __name__ == '__main__':
    main()