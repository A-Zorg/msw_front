@manager_1
Feature: Index page books, holidays and news

#  Scenario: check holiday days
#    Given get next 5 holidays
#    Then compare actual holidays name_list with expected
#     And compare actual holidays date_list with expected
#     And click on ST button
#     And pause 1 sec

#  Scenario: check holiday days
#    Given check sevices field
#     And check compensations field
#     And check total
#     And click on ST button
#     And pause 1 sec
#
#  Scenario: check library(genres)
#    Given make general select of books
#     And get all genres
#     And choose category on the Index page
#    When make select with chosen category
#    Then check selected books on the index page
#    And pause 1 sec
#
#  Scenario: check library(search)
#    Given make general select of books
#     And refresh index page
#     And get some search random phrase
#     And perform search by the random phrase
#    When make select with chosen search_text
#    Then check selected books on the index page
#     And pause 1 sec
#
#  Scenario: check news - likes
#    Given get initial number of likes
#     And click the like button from index page
#     And get intermediate number of likes
#    When open news
#     And compare number of likes with intermediate number
#     And click the like button from news page
#    Then compare number of likes with initial number
#     And Exit the news block
#     And pause 1 sec
#
#  Scenario: check news - views
#    Given delete all views
#     And refresh index page
#     And get initial number of views
#    When open news
#    Then compare number of views with initial number
#     And Exit the news block
#     And pause 1 sec
#
  Scenario: check news - text
    Given get news from db
     And take text_news from index page
    When open news
    Then take text_news from news page
     And compare news from index_page and news_page
     And Exit the news block
     And pause 1 sec

#  Scenario: check news - text
#    Given get news from db
#     And check that all news are shown on index page
#     And pause 1 sec

  Scenario: check news - image
    Given get news from db(image)
     And get the id of the news being checked
     And open news
     And get image from api
     When make screenshot of the news_image
     Then compare news_images
      And pause 1 sec


#
#
#
#
#
#






