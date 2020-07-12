from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from PIL import Image
from secrets import username, password

import os
import random
import requests

class TinderAutomator():
  def __init__(self): 
    self.driver = webdriver.Chrome()

  def login_fb(self):
    self.driver.get("https://tinder.com/")

    sleep(5)

    login_fb = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[2]/button')
    login_fb.click()

    # switch to login popup
    base_window = self.driver.window_handles[0]
    self.driver.switch_to.window(self.driver.window_handles[1])

    login_input = self.driver.find_element_by_xpath('//*[@id="email"]')
    password_input = self.driver.find_element_by_xpath('//*[@id="pass"]')
    login_input.send_keys(username)
    password_input.send_keys(password)

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
    name = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/div/span').text
    age = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/span').text
    print("like ["+name+":"+age+"]")
    self.driver.find_element_by_tag_name('body').send_keys(Keys.RIGHT)
    sleep(1)

  def dislike(self):
    name = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/div/span').text
    age = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/span').text
    print("dislike ["+name+":"+age+"]")
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
      sleep(0.5+random.randint(0,2))

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

  def close_any_popup(self):
    self.driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    sleep(0.5)

  def download_image(self, name, idx, path):

    sleep(1)
    sequence = idx + 1
    web_element = """//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[""" + str(sequence) + """]/div/div"""
    style_string = self.driver.find_element_by_xpath(web_element).get_attribute("style")
    
    # parse style element
    style_string = style_string.split(' url("')[1].replace('");', '')
    image_url = style_string.split(' ')[0]
    # print(image_url)
    
    # download image, convert as jpg
    img_data = requests.get(image_url).content
    with open(path + '/' + name + '_' + str(sequence) + '.jpg', 'wb') as handler:
      handler.write(img_data)


  def save_biodata(self):
    name = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/div/span').text
    age = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/span').text

    path = "pics/"+name+"-"+age
    os.mkdir(path)
    number_of_photos = len(self.driver.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/*'))
    print(number_of_photos)

    for idx in range (number_of_photos):
      self.download_image(name, idx, path)
      # next photo
      self.driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)


  def auto_swipe(self):
    while True:
      sleep(2)
      # self.show_profile()
      # self.hide_profile()
      # self.save_card_to_photo()
      # self.next_photo()
      self.save_biodata()
      try:
        if random.randint(0,99) > 10:  
          self.dislike()
        else:
          self.like()
      except Exception as err:
        self.close_any_popup()
        print("Error: {0}".format(err))      

  def run(self): 
    self.login_fb()
    self.clear_notification()
    self.auto_swipe()


bot = TinderAutomator()
bot.run()