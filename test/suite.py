import unittest
import sys

from functional.project.project_tests import ProjectTest
from functional.project.project_create_tests import ProjectCreateTest
from functional.project.credentials_tests import CredentialsTest
from functional.unit_test.async_test_api import ApexUnitTestingTest
from functional.metadata.create_tests import MetadataOperationTest
from functional.debug.checkpoint_tests import CheckpointTests
from functional.debug.log_tests import StackTraceAndLogsTest
from functional.metadata.refresh_tests import MetadataRefreshTest
from functional.project.ui_integration_test import ProjectUiIntegrationTest
from functional.metadata.compilation_tests import CompilationTests


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

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    test_results = runner.run (test_suite)
    print test_results
    if len(test_results.errors) > 0 or len(test_results.failures) > 0:
        sys.exit('Test suite failed')

