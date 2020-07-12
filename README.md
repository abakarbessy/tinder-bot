## How to run

Prerequisites:
* Selenium webdriver
* Add the following library (possibly to your local-env)
  ```
  # create local-env first
  pip install selenium
  pip install Pillow
  ```
* Run it
  ```
  python tinder-automator.py
  ```
To Do:
* Make the username and password not hardcoded
  * start the program by putting username and password in the console
* Better strategy to swipe, now only using simple randomizer. It goes to left mostly to keep the quota.
* store username of the swiped card somewhere
* send default message to matches
* stop when there is no one in the area
* simple ai
