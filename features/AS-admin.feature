@super_user
Feature: Accounting system
#
  Scenario: Preparing user Accounting data
    Given delete old urers's data
     And create manager_user bills: account and withdrawal
     And create default ENTRIES with parameters
            | amount | user_bill | day | month      |
            |  -12   |  Account  |  15 | before last|
            |   9.5  |  Account  |  26 | before last|
            | -152.1 |  Account  |  15 | last       |
            |   10   |  Account  |  26 | last       |
            |   12.55|  Account  |  1  | this       |
            |   1234 | Withdrawal|  26 | before last|
            |  -12   | Withdrawal|  15 | before last|
            |   9.99 | Withdrawal|  26 | last       |
            |  -11.49| Withdrawal|  15 | last       |
            |   5    | Withdrawal|  1  | this       |
      And create PROPREPORTS ENTRIES

#  Scenario: check Accounting by admin
#    Given Admin goes to the AS page -> Accounting
#    And User checks his Accounting data
#    And get users's Accounting data through api
#    Then compare user's accounting data from UI and API

#  Scenario Outline: check creation of transactions
#    Given Admin goes to the AS page -> Create transaction
#    When Create <tr_type> transaction: <from_acc>, <to_acc>, <amount>
#    Then Admin checks that entry and related transactions are created: <tr_type>, <from_acc>, <to_acc>, <amount>
#     And [Create transaction] compare actual with expected result
#    Examples: icons
#        | tr_type    | from_acc    | to_acc       | amount |
#        | Multiple   | Withdrawal  |  Operational | 345.67 |
##  | NET Buyout | Withdrawal  |  Current Net balance | 1000 |
#        | Default    | Withdrawal  |  Operational | 35.67  |
#


