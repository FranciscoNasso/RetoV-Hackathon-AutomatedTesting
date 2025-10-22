Feature: Explore Pages

  Scenario: Navigate to the Home Page
    Given I am on the home page
    When I navigate to the explore page
    Then I should see the explore page title

  Scenario: Navigate to the Download Page
    Given I am on the home page
    When I navigate to the download page
    Then I should see the download page title

  Scenario: Navigate to the Upload Page
    Given I am on the home page
    When I navigate to the upload page
    Then I should see the upload page title
