import requests, bs4, urllib, re, string
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from urllib.request import Request, urlopen 

##############################################
# BS4 Web Scrapping Tech Demo 
##############################################
# Author: Roxena Liu 
'''
# rewrite demo presented by mini-lecture 
r = requests.get('http://www.kosbie.net/cmu/spring-17/15-112/syllabus.html')
soup = bs4.BeautifulSoup(r.text, 'html.parser')
paragraphs = soup.find_all('p')
article = ''
for paragraph in paragraphs: 
    article = article + paragraph.get_text() + '\n'
print(article)

r = requests.get('https://www.momsteam.com/nutrition/sports-nutrition-basics/nutritional-needs-guidelines/carbohydrate-and-calorie-content-of-foods')
soup = bs4.BeautifulSoup(r.text, 'html.parser')



##### My Own Documentation #####
soup.find_all('b') # find all <b> tags in document 
soup.find_all(['a', 'b']) # find all <a>, <b> tags in document 

for tag in soup.find_all(True):
    print(tag.name)    # find all tags but none of the text strings


# Extract information from spring-17/15-112 syllabus 
r = requests.get('http://www.kosbie.net/cmu/spring-17/15-112/syllabus.html')
soup = bs4.BeautifulSoup(r.text, 'html.parser')
table = soup.find('table')
text = ''
for ele in table: 
    text = text + table.get_text() + '\n'
print(text)
'''

# Extract from the web I need for tp
r = requests.get('https://www.momsteam.com/nutrition/sports-nutrition-basics/nutritional-needs-guidelines/carbohydrate-and-calorie-content-of-foods')
soup = bs4.BeautifulSoup(r.text, 'html.parser')
text = soup.find_all('div')  # list
result = ''
for ele in text: 
    if ele.get('class') == ['field-items']: 
        result = result + ele.get_text()
print(result)



# extract info from table
# should be combined with selenium 

url = 'https://caloriecontrol.org/healthy-weight-tool-kit/food-calorie-calculator/?'
req = Request(url, headers={'User-Agent':'Chrome/5.0'})
r = urlopen(req).read()
soup = bs4.BeautifulSoup(r, 'html.parser')
##target = soup.find('table')
#print(target) # None 

table_body = soup.find('tbody')  # body of the whole list of options and corresponding data 
print(table_body)
optionsList = table_body.find_all('tr')
print(optionsList)
result = []
for each in optionsList: 
    print(each, each.find_all('td'))

result = []
for option in optionsList:  # each table of certain food 
    cols = option.find_all('td')
    food = []
    for col in cols: 
        data = str(col.get_text())
        food.append(data)
    result.append(food)
print(result)




        
    