import unittest
import sys
import os
import argparse
import shutil
import lib.test_helper as test_helper
import inspect

# ALL TEST COMMANDS SHOULD BE RUN FROM PROJECT ROOT
#
# to run test suite:
#   $ python test
# to run test suite for a particular api version:
#   $ python test --api=31.0
# to run all test methods in one of the test suite classes:
#   $ python test ProjectTest
# to run a specific test method in one of the test suite classes:
#   $ python test ProjectTest.test_01_should_create_new_project

def suite(clz=None,tst=None):
    
    if os.getenv('MM_TEST_TYPE', 'functional') == 'functional':
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
        from functional.deploy.deploy_tests import DeployTest

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
            CompilationTests,
            DeployTest
        ]
    else:
        from unit.project.project_create_tests import ProjectCreateTest
        from unit.login.login_tests import LoginUnitTest

        test_classes = [
            ProjectCreateTest,
            LoginUnitTest
        ]

    suite = unittest.TestSuite()
    for unit_test_class in test_classes:
        # print unit_test_class.__module__
        if clz != None:
            if unit_test_class.__name__ != clz:
                continue
        for method in dir(unit_test_class):
            if method.startswith("test"):
                if tst != None and method != tst:
                    continue
                suite.addTest(unit_test_class(method))

    return suite

def cleanup_workspaces():
    if os.path.exists(os.path.join(test_helper.base_test_directory,"test_workspace")):
        shutil.rmtree(os.path.join(test_helper.base_test_directory,"test_workspace"))

def create_workspace():
    os.mkdir(os.path.join(test_helper.base_test_directory,"test_workspace"))

def main():
    cleanup_workspaces()
    create_workspace()

    os.environ['MM_TESTING'] = 'true'

    supported_sfdc_api_versions = ['31.0', '30.0', '29.0']
    testing_api_versions = []

    parser = argparse.ArgumentParser()
    parser.add_argument('--api', help='Salesforce.com API version') # run tests for specific version
    parser.add_argument('--unit', action='store_true', default=False, help='Whether this test should be run using fixtures')
    args, unknown_args = parser.parse_known_args()

    if args.unit == None or args.unit == False:
        os.environ['MM_TEST_TYPE'] = 'functional'
    else:
        os.environ['MM_TEST_TYPE'] = 'unit'

    clz = None
    tst = None
    if unknown_args != [] and unknown_args[0]:
        unknown_class_arg = unknown_args[0]
        if '.' in unknown_class_arg:
            clz = unknown_class_arg.split('.')[0]
            tst = unknown_class_arg.split('.')[1] 
        else:
            clz = unknown_class_arg

    if args.api == None:
        testing_api_versions = supported_sfdc_api_versions
    else:
        testing_api_versions = [args.api]

    results = {}
    for api_version in testing_api_versions:
        os.environ['SFDC_API_VERSION'] = api_version

        runner = unittest.TextTestRunner(verbosity=2)
        test_suite = suite(clz, tst)
        test_results = runner.run (test_suite)
        print '===> TEST RESULTS FOR SALESFORCE.COM API VERSION: '+str(api_version)
        print test_results
        if len(test_results.errors) > 0 or len(test_results.failures) > 0:
            results[api_version] = 'failed'
        else:
            results[api_version] = 'passed'

    print '==========> AGGREGATE TEST RESULTS'
    print results

    for key, value in results.iteritems():
        if value == 'failed':
            sys.exit('Test suite for Salesforce.com API version '+str(key)+' failed')


if  __name__ == '__main__':
    main()