## How to run

Prerequisites:
* Selenium webdriver
* Add the following library (possibly to your local-env)
  ```
  # create local-env first
  pip install selenium
  pip install Pillow
  ```
* Run it in python interactive mode
  ```
  python -i tinder-automator.py
  bot = TinderAutomator()
  bot.run()
  ```
To Do:
* Make the username and password not hardcoded
* Make strategy to swipe. At the moment only swipe left
