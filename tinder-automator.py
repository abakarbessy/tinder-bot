from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from PIL import Image

import os

class TinderAutomator():
  def __init__(self, username, password): 
    self.driver = webdriver.Chrome()

  def login_fb(self):
    self.driver.get("https://tinder.com/")

    sleep(5)

    login_fb = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button')
    login_fb.click()

    base_window = self.driver.window_handles[0]
    self.driver.switch_to.window(self.driver.window_handles[1])

    login_input = self.driver.find_element_by_xpath('//*[@id="email"]')
    password_input = self.driver.find_element_by_xpath('//*[@id="pass"]')
    login_input.send_keys('<your-fb-username>')
    password_input.send_keys('<your-fb-password')

    login_btn = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
    login_btn.click()
    sleep(2)

    # switch back to main window after login from fb
    self.driver.switch_to.window(base_window)
    sleep(2)

  def clear_notification(self):
    allow_location_button = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
    allow_location_button.click()
    sleep(2)

    confirm_notification = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
    confirm_notification.click()
    sleep(5)
  
  def like(self):
    self.driver.find_element_by_tag_name('body').send_keys(Keys.RIGHT)
    sleep(1)

  def dislike(self):
    self.driver.find_element_by_tag_name('body').send_keys(Keys.LEFT)
    sleep(1)
  
  def show_profile(self):
    self.driver.find_element_by_tag_name('body').send_keys(Keys.UP)
    sleep(1)

  def hide_profile(self):
    self.driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
    sleep(1)

  def next_photo(self):
    number_of_photos = len(self.driver.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/*'))
    for idx in range (number_of_photos):
      self.driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)
      sleep(0.5)

  def save_card_to_photo(self):
    name = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/div/span').text
    age = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/span').text

    path = "pics/"+name+"-"+age
    os.mkdir(path)

    card = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]')    
    location = card.location
    size = card.size

    self.driver.save_screenshot(path+"/"+"tmp_shot.png")

    x = location['x']
    y = location['y']
    w = size['width']
    h = size['height']
    width = x + w
    height = y + h

    im = Image.open(path+"/"+"tmp_shot.png")
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(path+"/"+"photo.png")
    os.remove(path+"/"+"tmp_shot.png")


  def swipe_left_forever(self):
    while True:
      sleep(1)
      self.show_profile()
      self.hide_profile()
      self.save_card_to_photo()
      self.next_photo()
      self.dislike()

  def run(self): 
    self.login_fb()
    self.clear_notification()
    self.swipe_left_forever()


