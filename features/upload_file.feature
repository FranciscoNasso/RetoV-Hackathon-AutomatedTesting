Feature: Upload File

  Scenario: User uploads a file successfully
    Given the user is on the upload page
    When the user selects a file to upload
    And the user clicks the upload button
    Then the user should see a success message

  Scenario: User attempts to upload an invalid file type
    Given the user is on the upload page
    When the user selects an invalid file type to upload
    And the user clicks the upload button
    Then the user should see an error message

  Scenario: User uploads a file and cancels the upload
    Given the user is on the upload page
    When the user selects a file to upload
    And the user clicks the cancel button
    Then the user should not see the file in the upload list
