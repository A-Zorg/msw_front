@manager_1
Feature: Index page
  # Enter feature description here
  Background: click on ST button


#  Scenario Outline: check look of the contest images
#    Given click on the icone: <icone>
#    When make screenshot of the image: <icone>
#     And get image from api: <icone>
#    Then compare images: <icone>
#  Examples: icons
#        |  icone         |
#        |  smartheat    |
#        |  top30        |



  Scenario Outline: check look of the contest icons
    Given make screenshot of the icone: <icone>
    When get icone from api: <icone>
    Then compare icones: <icone>
  Examples: icons
        |  icone         |
        |  smartheat    |
        |  top30        |






  Scenario Outline: check look of the contest icons
    Given  click on the icone: <icone>
    Then compare current url with expected: <page>
  Examples: icons
        |  icone             |  page           |
        |  reconciliation    | /reconciliation |
        |  accounting        | /accounting     |
        |  dr                | /daily-review   |



















































