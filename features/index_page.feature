@manager_1
Feature: Index page
   Enter feature description here
  Background: click on ST button


  Scenario Outline: check look of the contest images
    Given click on the icone: <icon>
    When make screenshot of the image: <icon>
     And get image from api: <icon>
    Then compare images: <icon>
  Examples: icons
        |  icon         |
        |  smartheat    |
        |  top30        |



#  Scenario Outline: check look of the contest icons
#    Given make screenshot of the icone: <icon>
#    When get icone from api: <icon>
#    Then compare icons: <icon>
#  Examples: icons
#        |  icon         |
#        |  smartheat    |
#        |  top30        |




#  Scenario Outline: check look of the contest icons
#    Given  click on the icone: <icon>
#    Then compare current url with expected: <page>
#    And click on ST button
#  Examples: icons
#        |  icon              |  page              |
#        |  reconciliation    | /reconciliation    |
#        |  accounting        | /accounting-system |
#        |  dr                | /daily-review      |
#
#
#
















































