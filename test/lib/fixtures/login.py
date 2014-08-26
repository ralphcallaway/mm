class MockLoginDeveloperOrgSuccess:
    metadataServerUrl = ''
    sessionId = ''
    passwordExpired = ''
    serverUrl = ''
    userId = ''
    userInfo = ''
    def __init__(self):
        self.metadataServerUrl = "https://na14.salesforce.com/services/Soap/m/30.0/00Dd0000000cRQK"
        self.passwordExpired = False
        self.sandbox = False
        self.serverUrl = "https://na14.salesforce.com/services/Soap/u/30.0/00Dd0000000cRQK"
        self.sessionId = "00Dd0000000cRQK!AQR6GdAvFIYaI2xcTotxH5XIEUpCQaY0UOZ2IwkwVYY.EQ87ZN09E1yW2zAM76qD65dXD4J.1E384wWO.BHahDJk2HNLfRV4vlO"
        self.userId = "005d0000000xxzsBBB"
        self.userInfo = MockGetUserInfoResult()

class MockGetUserInfoResult:
    def __init__(self):
        self.accessibilityMode = False
        self.currencySymbol = "$"
        self.orgAttachmentFileSizeLimit = 5242880
        self.orgDefaultCurrencyIsoCode = "USD"
        self.orgDisallowHtmlAttachments = False
        self.orgHasPersonAccounts = False
        self.organizationId = "00Dd0000000cRQKEV8"
        self.organizationMultiCurrency = False
        self.organizationName = "Force"
        self.profileId = "00ed0000000w0N2AAP"
        self.roleId = "00Ed0000000qglkEAF"
        self.sessionSecondsValid = 7200
        self.userDefaultCurrencyIsoCode = None
        self.userEmail = "mm@force.com"
        self.userFullName = "Mavens Tester"
        self.userId = "005d0000000xxzsAAB"
        self.userLanguage = "en_US"
        self.userLocale = "en_US"
        self.userName = "mm@force.com"
        self.userTimeZone = "America/Los_Angeles"
        self.userType = "Standard"
        self.userUiSkin = "Theme3"