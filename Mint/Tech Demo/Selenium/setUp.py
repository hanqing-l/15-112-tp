import module_manager
module_manager.review()

from selenium import webdriver

# Make sure you install the right webdriver for your Chrome version
# You can check version number of Chrome by typing chrome://version
# https://chromedriver.storage.googleapis.com/index.html?path=86.0.4240.22/

# Replace file path where you store your webdriver
searchQuery = input("What do you want to search up? ")
driver = webdriver.Edge("/Users/roxena/Documents/CMU Academic Fall 2020/15-112/Mint/Tech Demo/Selenium")

driver.get("https://www.bing.com/")
element = driver.find_element_by_class_name("sb_form_q")
element.send_keys(f"{searchQuery}\n")
