import mock
from test.lib.fixtures.login import MockLoginDeveloperOrgSuccess
import test.lib.fixtures.describe as mock_describe
from mm.sforce.metadata import SforceMetadataClient
from mm.sforce.base import SforceBaseClient
from mm.exceptions import *

def mock_login_and_describe():
    SforceBaseClient.login = mock.Mock(return_value=MockLoginDeveloperOrgSuccess())
    SforceMetadataClient.describeMetadata = mock.Mock(side_effect=mock_describe.get_org_metadata)
    SforceMetadataClient.getOrgNamespace = mock.Mock(return_value='')

def mock_invalid_login():
    SforceBaseClient.login = mock.Mock(side_effect=MMException("Server raised fault: 'INVALID_LOGIN: Invalid username, password, security token; or user locked out.'")) 