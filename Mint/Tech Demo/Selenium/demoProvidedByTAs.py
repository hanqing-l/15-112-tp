###############################################################################
#
# Selenium Demo: Canvas Download
# Written by: David Topping
# Modified by: Elisa Ma
#
###############################################################################
#
# Selenium Demo: Canvas Download
# Written by: David Topping
# Modified by: Elisa Ma
#
###############################################################################

def mypw():
    return "no <3"

import time 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Edge
with Edge(executable_path= 'C:\\Users\\elisa\\msedgedriver.exe' ) as driver:
    url  = 'login.cmu.edu'
    driver.get("https://" + url) # You need the https:// or else Selenium will error saying it isn't a url
    driver.find_element_by_name('j_username').send_keys("ezm")    # Put your AndrewID and Passwords in the send_keys function as a string
    driver.find_element_by_name('j_password').send_keys(mypw())    
    driver.find_element_by_name('_eventId_proceed').send_keys(Keys.ENTER) # This presses the enter button to log in
    time.sleep(10) # We sleep to allow the password to be verified 10 seconds is a little long but better safe than sorry
    url = 'canvas.cmu.edu/courses/19385/modules' # Replace this with one of your courses modules pages
    driver.get("https://" + url)
    time.sleep(5)
    links = driver.find_elements_by_partial_link_text(".pdf") # Replace this with any piece of text all the relevant pages names share

    # The demo was previously len(links), but my Chinese class has many pdfs, so I shortened it
    for i in range(5, 13, 2):
        links = driver.find_elements_by_partial_link_text(".pdf") # This should be a copy of line 36
                                    # We keep generating a new list from the current page otherwise we error because when you reload a page old
                                    # elements that selenium found stop being valid
        elm = links[i]
        elm.click()
        driver.find_element_by_partial_link_text("Down").click() # Replace with any piece of text in all of the download links
        time.sleep(7) # This is to give the file time to download, not the most elegant but it works        
        driver.back()
' ) as driver:
    url  = 'login.cmu.edu'
    driver.get("https://" + url) # You need the https:// or else Selenium will error saying it isn't a url
    driver.find_element_by_name('j_username').send_keys("ezm")    # Put your AndrewID and Passwords in the send_keys function as a string
    driver.find_element_by_name('j_password').send_keys(mypw())    
    driver.find_element_by_name('_eventId_proceed').send_keys(Keys.ENTER) # This presses the enter button to log in
    time.sleep(10) # We sleep to allow the password to be verified 10 seconds is a little long but better safe than sorry
    url = 'canvas.cmu.edu/courses/19385/modules' # Replace this with one of your courses modules pages
    driver.get("https://" + url)
    time.sleep(5)
    links = driver.find_elements_by_partial_link_text(".pdf") # Replace this with any piece of text all the relevant pages names share

    # The demo was previously len(links), but my Chinese class has many pdfs, so I shortened it
    for i in range(5, 13, 2):
        links = driver.find_elements_by_partial_link_text(".pdf") # This should be a copy of line 36
                                    # We keep generating a new list from the current page otherwise we error because when you reload a page old
                                    # elements that selenium found stop being valid
        elm = links[i]
        elm.click()
        driver.find_element_by_partial_link_text("Down").click() # Replace with any piece of text in all of the download links
        time.sleep(7) # This is to give the file time to download, not the most elegant but it works        
        driver.back()
