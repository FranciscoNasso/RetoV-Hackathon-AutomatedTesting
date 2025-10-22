Feature: Download File

  Scenario: User downloads a file successfully
    Given the user is on the home page
    When the user navigates to the download page
    And the user initiates the file download
    Then the file should be downloaded successfully

  Scenario: User verifies the downloaded file
    Given the user has downloaded a file
    When the user checks the download location
    Then the downloaded file should be present in the specified location

  Scenario: User cancels the file download
    Given the user is on the download page
    When the user initiates a file download
    And the user cancels the download
    Then the file should not be present in the download location
