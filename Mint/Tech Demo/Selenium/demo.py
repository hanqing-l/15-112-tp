from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options 

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
import time


'''
##Demo1
driver.get("http://www.duo.com") 
print("Chrome Browser Initialized in Headless Mode")
driver.quit()
print("Driver Exited")


## Demo2: 
driver.get('http://www.python.org')
assert 'Python' in driver.title
elem = driver.find_element_by_name('q')
elem.clear() # clear the 'search' area 
elem.send_keys('pycon')
elem.send_keys(Keys.RETURN)
assert 'No results found.' not in driver.page_source 
'''


## Demo3: 
def getAge(): 
    return 18
def getGender(): 
    return False 
url = 'https://www.calculator.net/calorie-calculator.html?ctype=standard&cage=25&csex=m&cheightfeet=5&cheightinch=10&cpound=165&cheightmeter=180&ckg=65&cactivity=1.465&cmop=0&coutunit=c&cformula=m&cfatpct=20&printit=0#'
driver.get(url)
age = driver.find_element_by_name('cage')
age.clear()
age.send_keys(getAge())
time.sleep(3)

if (getGender()): 
    male = driver.find_element_by_id('csex1')
    male.click()
    time.sleep(3)
else: 
    female = driver.find_element_by_id('csex2')
    female.click()
    time.sleep(3)

calculate = driver.find_element_by_xpath("//input[@src='//d26tpo4cm8sb6k.cloudfront.net/img/svg/calculate.svg']")
calculate.click()