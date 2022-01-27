# Author Name: Hanqing Liu 
# Andrew ID: hanqing2 

# References: 
# Some information such as calories and the basal metabolisms are webscrapped from web. 
# Note that the basal metabolism calculation is controlled bu Selenium as different 
# people has different basalMetabolism. 
# Calorie table: 'http://www.myfoodbuddy.com/foodCalorieTable.htm'
# Basal Metabolism: 'https://www.calculator.net/calorie-calculator.html?ctype=standard&cage=25&csex=m&cheightfeet=5&cheightinch=10&cpound=165&cheightmeter=180&ckg=65&cactivity=1.465&cmop=0&coutunit=c&cformula=m&cfatpct=20&printit=0#'
# rgbString function: copied from course note 
# data about standard nutrients needs extract from an App called 'Mint'
# more data extracted from: 
# https://www.healthline.com/nutrition/how-much-protein-per-day
# https://www.omnicalculator.com/health/meal-calorie

############################################################
from cmu_112_graphics import *
from datetime import date 
import random
import copy

############################################################
#################### Helper Functions ######################
############################################################

def getAge(bornD, bornM, bornY): 
        [bornY, bornM, bornD] = [(int)(bornY), (int)(bornM), (int)(bornD)]
        today = date.today()
        (todayY, todayM, todayD) = (today.year, today.month, today.day)
        if (bornM < todayM): hasBirth = True 
        elif (bornM == todayM): 
            if (bornD < todayD): hasBirth = True 
            else: hasBirth = False 
        else: hasBirth = False 
        if (hasBirth): 
            return (todayY-bornY)
        else: 
            return (todayY-bornY-1)


def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'



def convertDtoL(d): 
    result = []
    for v in d: 
        result.append([v]+d[v])
    return result 


def convertLtoD(l): 
    n = len(l)
    d = dict()
    for i in range(n): 
        each = l[i]
        name = each[0]
        values = each[1:]
        d[name] = values
    return d


def divide(l, step): 
    resultL = []
    resultL.append(l[0:step])
    startIndex, endIndex = step, step
    while (resultL[-1][-1] != l[-1]): 
        endIndex = min(startIndex+step, len(l))
        resultL.append(l[startIndex: endIndex])
        startIndex = endIndex
    return resultL


def convertDtoL(d): 
    result = []
    for v in d: 
        result.append([v]+d[v])
    return result 


# 0: Calories, 1:Protein, 2:Fat, 3:Carbo
def calculateNutrients(whichNutrient, dictoryDict, foodList, foodQuant): 
    if (foodList != []): 
        total = 0 
        for i in range(len(foodList)): 
            nutrientInfo = dictoryDict.get(foodList[i], [])
            total += (int)(foodQuant[i]) * (int)(nutrientInfo[whichNutrient])
        return total
    else: 
        return 0 
    
        
    

############################################################
#################### Webscrapping Part #####################
############################################################

import requests, bs4, urllib, re, string
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from urllib.request import Request, urlopen 

##################  Helper Functions #######################

# get food calories in string 
calorieUrl = 'http://www.myfoodbuddy.com/foodCalorieTable.htm'

def getFoodCalories(url): 
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    target = soup.find('table')
    result = target.get_text()
    return result 

def deleteTitles(iniList):
    i = 0 
    while i < len(iniList): 
        if (iniList[i] != '100% NATURAL CEREAL 1 OZ'): 
            iniList.pop(i)
        else: 
            return iniList

def foodCalorDict(l): 
    result = dict()
    for i in range(0, len(l), 7): 
        if (l[i] != ''): 
            result[ l[i] ] = []
            for j in range(i+1, i+5): 
                result[ l[i] ].append(l[j])
    return result

################# Wrap Webscrapping #######################

def webScrapCalorie(calorieUrl): 
    foodCalorStr = getFoodCalories(calorieUrl)
    foodCalorList = foodCalorStr.splitlines()
    foodCalorList = deleteTitles(foodCalorList)
    foodDict = foodCalorDict(foodCalorList)
    return foodDict

def findMatchFood(directory, word): 
    word = word.upper()
    result = dict()
    for v in directory:
        if (word in v[0]): 
            result[v[0]] = v[1:]
    return result 

############################################################
####################   Selenium Part   #####################
############################################################

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
import time

import requests, bs4, urllib, re, string
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from urllib.request import Request, urlopen 

##################   Helper Functions    ####################

def getGender(): 
    gender = 'female'
    return gender 

def getHeight(): 
    (feet, inches) = (6, 10)
    return (feet, inches)

def getWeight(): 
    weight = 130
    return weight

def getActivity(): 
    activityLevel = 3
    return activityLevel

################## Start from Here  ####################

metaUrl = 'https://www.calculator.net/calorie-calculator.html?ctype=standard&cage=25&csex=m&cheightfeet=5&cheightinch=10&cpound=165&cheightmeter=180&ckg=65&cactivity=1.465&cmop=0&coutunit=c&cformula=m&cfatpct=20&printit=0#'

def calculateMeta(metaUrl, infoList): 
    driver.get(metaUrl)
    # Age 
    age = driver.find_element_by_name('cage') 
    age.clear()
    age.send_keys(infoList[5])
    # Gender
    if (infoList[1] == 'M'):
        driver.find_element_by_id('csex1').click()
    else: 
        female = driver.find_element_by_id('csex2')
        female.click()
    # Height
    (feetH, inchH) = (infoList[3], infoList[4])
    feet = driver.find_element_by_name('cheightfeet')
    feet.clear()
    feet.send_keys(feetH)
    inch = driver.find_element_by_name('cheightinch')
    inch.clear()
    inch.send_keys(inchH)
    # weight 
    weight = driver.find_element_by_name('cpound')
    weight.clear()
    weight.send_keys(infoList[2])
    # activityLevel
    activityLevel = getActivity()
    activity = driver.find_element_by_id('cactivity')
    options = [x for x in activity.find_elements_by_tag_name('option')]
    options[activityLevel].click()
    # calculate 
    calculate = driver.find_element_by_xpath("//input[@src='//d26tpo4cm8sb6k.cloudfront.net/img/svg/calculate.svg']")
    calculate.click()
    return (driver.current_url)

def getBasalMeta(current_url): 
    r = requests.get(current_url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    target = soup.find_all('b')
    result = []
    for i in range(4): 
        result.append(target[i].get_text())
    print('yeah')
    return result

# print(getBasalMeta(calculateMeta(metaUrl, ...)))




############################################################
#################### Meal Plan Generator ###################
############################################################


# refresh food directory 
# delete food that start with digits 
# assign this function to a new list and a new dictionary
def refreshLandD(directoryL, directoryD): 
    resultL = directoryL
    resultD = directoryD
    for i in range(5): 
        name = resultL.pop(0)[0]
        del resultD[name]
    return (resultL, resultD)


def digitInName(name): 
    for i in range(len(name)): 
        if (name[i].isdigit()): 
            if (i > 0): 
                if (name[i-1] == ' ') or (name[i-1].isalpha()): 
                    return True 
    return False 


def deleteAfterDigit(name): 
    for i in range(len(name)): 
        if (name[i].isdigit()): 
            name = name[:i]
            return name 

# given a list. delete parts after ;, delete parts after digits
# return newList
def filtNames(old): 
    new = []
    for v in old: 
        # process
        if (';' in v): v = v[:v.index(';')] # delete after ;
        if (digitInName(v)):   # has digit, delete after digit
            v = deleteAfterDigit(v)
        # add to newList
        new.append(v)
    return new

def noRepeatName(l): 
    # a list of names without useless info
    target = filtNames(l)
    if (len(l) == 1): return True 
    # break names into a whole 1d list 
    target2 = []
    for v in target: target2 += v.split()
    # check repeats 
    for v in target2: 
        if (target2.count(v) >= 2): return False  # repeated words
    # repeated occurence inside words
    for i in range(len(target2)): 
        for j in range(len(target2)): 
            if (i != j) and (target2[i] in target2[j]): 
                return False 
    return True 


def getNameList(foodList): 
    result = []
    for v in foodList: result.append(v[0])
    return result 


def getNutrientA(visited,foodDict): 
    sum = [0, 0, 0, 0]
    for v in visited: 
        sum[0] += (int)(foodDict[v][0])
        sum[1] += (int)(foodDict[v][1])
        sum[2] += (int)(foodDict[v][2])
        sum[3] += (int)(foodDict[v][3])
    return sum 


def nutrientMeetRequire(targetList, standard): 
    return (standard[0][0] < targetList[0] < standard[0][1]) and (standard[1][0] < targetList[1] < standard[1][1]) and (standard[2][0] < targetList[2] < standard[2][1]) and (standard[3][0] < targetList[3] < standard[3][1])



def getSubsets(foodList, foodDict, nutrientRequirement, numOptions): 
    visited = []
    l = getNameList(foodList)
    return (getSubsetsHelper(l, visited, foodDict, nutrientRequirement, numOptions))



def getSubsetsHelper(l, visited, foodDict, nutrientRequirement, numOptions): 
    visitedOwn = copy.copy(visited)
    #print(visitedOwn)
    if (len(visitedOwn)==numOptions): 
        nutriens = getNutrientA(visitedOwn, foodDict)
        if (nutrientMeetRequire(nutriens, nutrientRequirement)):return visitedOwn
        else: return False
    for i in range(len(l)): 
        v = l[i]
        temp = visitedOwn + [v]
        if (noRepeatName(temp)): 
            visitedOwn.append(v)
            solution = getSubsetsHelper(l[i+1:], visitedOwn, foodDict, nutrientRequirement, numOptions)
            if (solution != False): return solution 
            else: visitedOwn.pop()
    return False 



def divide(l, step): 
    resultL = []
    resultL.append(l[0:step])
    startIndex, endIndex = step, step
    while (resultL[-1][-1] != l[-1]): 
        endIndex = min(startIndex+step, len(l))
        resultL.append(l[startIndex: endIndex])
        startIndex = endIndex
    return resultL


# need nutrient list 
# need number of options 
# need targetList 
# need targetDict

nutri = [ (200, 300), (20, 30), (0, 10), (40, 70) ]
numOptions = 3


# first shuffle 
# than divide foodList into small parts and create separate dictionary for each part 
# run getsubsets on each part 
# collect result and return them in a list 

def mealPlan(nutri, foodList, foodDict, numOptions): 
    foodList = random.sample(foodList, len(foodList)) # shuffle 
    wrapList = divide(foodList, 30)
    resultL = []
    for smallTargetL in wrapList: 
        smallTargetD = convertLtoD(smallTargetL)
        solution = getSubsets(smallTargetL, smallTargetD, nutri, numOptions)
        if (solution != False):
            resultL.append(solution)
    return resultL 


############################################################
#################### Start from Here  ######################
############################################################

class WelcomeMode(Mode): 
    def appStarted(mode): 
        mode.directoryDict = webScrapCalorie(calorieUrl) # directory
        mode.app.directoryDict = mode.directoryDict
        mode.app.completefoodList = convertDtoL(mode.app.directoryDict)
        mode.app.refreshedL, mode.app.refreshedD = refreshLandD(mode.app.completefoodList, mode.app.directoryDict)


    def drawUniverse(mode, canvas): 
        # Draw the universe
        canvas.create_oval(75, 100, 425, 450, fill='black' )
        canvas.create_arc(75, 100, 425, 450, start=90, extent=-180, fill="white")
        canvas.create_arc(162.5, 100, 337.5, 275, start=90, extent=180, fill='white')
        canvas.create_arc(162.5, 275, 337.5, 450, start=90, extent=-180, fill='black')
        canvas.create_line(250, 100, 250, 275, fill='white')
        r = 20
        canvas.create_oval(250-r, 187.5-r, 250+r, 187.5+r, fill='black')
        canvas.create_oval(250-r, 362.5-r, 250+r, 362.5+r, fill='white')
        pass 

    def drawWelcome(mode, canvas): 
        (w, h) = (200, 50)
        canvas.create_rectangle(250-w, 600-h, 250+w, 600+h, fill='white')
        canvas.create_text(250, 600, text="Welcome",
                       fill="darkBlue", font="Times 50 bold italic")

    def mousePressed(mode, event): 
        (w, h) = (200, 50)
        if (250-w < event.x < 250+w) and (600-h < event.y < 600+h):
            mode.app.setActiveMode(mode.app.infoPage)
       

    def keyPressed(mode, event): 
        if (event.key == 'Enter'): 
            mode.app.setActiveMode(mode.app.infoPage)
        elif (event.key == 'f'): 
            mode.app.setActiveMode(mode.app.foodPage)
        if (event.key == 'i'): 
            mode.app.setActiveMode(mode.app.infoPage)
        elif (event.key == 'h'): 
            mode.app.setActiveMode(mode.app.homePage)

    
    def redrawAll(mode, canvas): 
        mode.drawUniverse(canvas)
        mode.drawWelcome(canvas)
        






    
class MealPlanMode(Mode): 
    def appStarted(mode): 
        [mode.breakfast, mode.lunch, mode.dinner] = [[], [], []]
        [mode.protein, mode.fat, mode.carbo] = [80, 35, 160]
        mode.nutrients = mode.get4NutriRequirements()  # 2d list. [breakFastRequire, lunchRequire, ...] 
        mode.generateMealPlan()

    def generateMealPlan(mode): 
        mode.currentMealPlans = []
        [mode.breakfastPlan, mode.lunchPlan, mode.dinnerPlan] = [[], [], []]
        [mode.breakFastWindowOpen, mode.lunchWindowOpen, mode.dinnerWindowOpen] = [False, False, False]

    def get4NutriRequirements(mode): 
        result = []
        totalCalorie = mode.app.totalCalorieNeed
        #breakfast
        breakFastRequirement = [(totalCalorie*0.3, totalCalorie*0.4), (mode.protein*0.2, mode.protein*0.35), (0, mode.fat*0.4), (mode.carbo*0.25, mode.carbo*0.4)]
        result.append(breakFastRequirement)
        #lunch 
        lunchRequirement = [(totalCalorie*0.3, totalCalorie*0.5), (mode.protein*0.25, mode.protein*0.4), (0, mode.fat*0.4), (mode.carbo*0.3, mode.carbo*0.5)]
        result.append(lunchRequirement)
        #dinner 
        dinnerRequirement = [(totalCalorie*0.2, totalCalorie*0.4), (mode.protein*0.2, mode.protein*0.35), (0, mode.fat*0.4), (mode.carbo*0.5, mode.carbo*0.4)]
        result.append(dinnerRequirement)
        return result 


    # 0: breakfast, 1: lunch, 2: dinner
    def disPlayMealPlans(mode, canvas, whichMeal): 
        mealPlans = mode.currentMealPlans
        if (mealPlans == []): 
            canvas.create_text(250, 225+225*whichMeal, text='Please Click Again', font='Calibri 20 bold', fill='grey')
        else: 
            canvas.create_rectangle(50, 100, 450, 600, fill='white', outline='grey', width=5)
            if (len(mealPlans) >= 3): 
                for i in range(3): 
                    mode.drawEachPlan(canvas, i)
            else: 
                for i in range(len(mealPlans)): 
                    mode.drawEachPlan(canvas, i)


    def drawEachPlan(mode, canvas, whichPlan): 
        planName = ['A', 'B', 'C']
        canvas.create_line(75, 250+whichPlan*150, 425, 250+whichPlan*150, fill='grey', width=2)
        canvas.create_text(100, 150+150*whichPlan, text=f'Plan {planName[whichPlan]}', font='Calibri 20 bold', fill='grey')
        # display information: 
        mealPlan = mode.currentMealPlans[whichPlan]
        for i in range(3): 
            canvas.create_text(100, 180+i*30+150*whichPlan, text=f'· {mealPlan[i]}: {mode.app.refreshedD[mealPlan[i]]}', font='Calibri 10', fill='grey', anchor='sw')
        

    def mousePressed(mode, event): 
        if ( 0 < event.x < 80) and (0 < event.y < 80): 
            mode.app.setActiveMode(mode.app.homePage)
        
        # select mealPlan
        if (mode.breakFastWindowOpen or mode.lunchWindowOpen or mode.dinnerWindowOpen): 
            if ( 80<event.y<170): 
                if (mode.breakFastWindowOpen): 
                    mode.breakfastPlan = mode.currentMealPlans[0]
                    mode.breakFastWindowOpen = False 
                    mode.currentMealPlans = []
                elif (mode.lunchWindowOpen): 
                    mode.lunchPlan = mode.currentMealPlans[0]
                    mode.lunchWindowOpen = False 
                    mode.currentMealPlans = []
                else: 
                    mode.dinnerPlan = mode.currentMealPlans[0]
                    mode.dinnerWindowOpen = False 
                    mode.currentMealPlans = []

            elif ( 200 < event.y < 350): 
                if (mode.breakFastWindowOpen): 
                    mode.breakfastPlan = mode.currentMealPlans[1]
                    mode.breakFastWindowOpen = False 
                    mode.currentMealPlans = []
                elif (mode.lunchWindowOpen): 
                    mode.lunchPlan = mode.currentMealPlans[1]
                    mode.lunchWindowOpen = False 
                    mode.currentMealPlans = []
                else: 
                    mode.dinnerPlan = mode.currentMealPlans[1]
                    mode.dinnerWindowOpen = False 
                    mode.currentMealPlans = []

            elif ( 350 < event.y < 500): 
                if (mode.breakFastWindowOpen): 
                    mode.breakfastPlan = mode.currentMealPlans[2]
                    mode.breakFastWindowOpen = False 
                    mode.currentMealPlans = []
                elif (mode.lunchWindowOpen): 
                    mode.lunchPlan = mode.currentMealPlans[2]
                    mode.lunchWindowOpen = False 
                    mode.currentMealPlans = []
                else: 
                    mode.dinnerPlan = mode.currentMealPlans[2]
                    mode.dinnerWindowOpen = False 
                    mode.currentMealPlans = []


        if (341<event.x<353) and (119<event.y<131): 
            mode.breakFastWindowOpen = True 
            print('breakFast')
            for i in range(3): 
                mealPlans = mealPlan(mode.nutrients[0], mode.app.refreshedL, mode.app.refreshedD, 3)
                if (mealPlans != None): 
                    mode.currentMealPlans += mealPlans
            print(mode.currentMealPlans)

        elif (304<event.x<316) and (344<event.y<354): 
            mode.lunchWindowOpen = True 
            print('lunch')
            for i in range(3): 
                mealPlans = mealPlan(mode.nutrients[1], mode.app.refreshedL, mode.app.refreshedD, 3)
                if (mealPlans != None): 
                    mode.currentMealPlans += mealPlans
            print(mode.currentMealPlans)

        elif (308<event.x<320) and (569<event.y<581): 
            mode.dinnerWindowOpen = True 
            print('dinner')
            for i in range(3): 
                mealPlans = mealPlan(mode.nutrients[2], mode.app.refreshedL, mode.app.refreshedD, 3)
                if (mealPlans != None): 
                    mode.currentMealPlans += mealPlans
            print(mode.currentMealPlans)


    
    def drawBreakFastBoard(mode, canvas): 
        canvas.create_rectangle(25, 100, 475, 300, fill='white', outline='grey')
        canvas.create_text(50, 125, text='· Breakfast.  30% ~ 35%', font='Chalkduster 20 bold', fill='grey', anchor='w')
        canvas.create_text(475, 125, text='**kcal >', anchor='e', fill='grey', font='Chalkduster 20 bold')
        r = 6
        canvas.create_oval(347-r, 125-r, 347+r, 125+r, fill='white', outline='grey', width=4)
        # draw mealPlan 
        if (mode.breakfastPlan != []): 
            for i in range(3): 
                values = mode.app.refreshedD[mode.breakfastPlan[i]]
                canvas.create_text(50, 180+i*50, text=f'· {mode.breakfastPlan[0]}: {values[0]} kcal, {values[1]}g, {values[2]}g, {values[3]}g', anchor='sw', fill='grey')


    def drawLunchBoard(mode, canvas): 
        canvas.create_rectangle(25, 325, 475, 525, fill='white', outline='grey')
        canvas.create_text(50, 350, text='· Lunch.  35% ~ 40%', font='Chalkduster 20 bold', fill='grey', anchor='w')
        canvas.create_text(475, 350, text='**kcal >', anchor='e', fill='grey', font='Chalkduster 20 bold')
        r = 6
        canvas.create_oval(310-r, 350-r, 310+r, 350+r, fill='white', outline='grey', width=4)
        if (mode.lunchPlan != []): 
            for i in range(3): 
                values = mode.app.refreshedD[mode.lunchPlan[i]]
                canvas.create_text(50, 405+i*50, text=f'· {mode.lunchPlan[0]}: {values[0]} kcal, {values[1]}g, {values[2]}g, {values[3]}g', anchor='sw', fill='grey')
                
  

    def drawDinnerBoard(mode, canvas): 
        canvas.create_rectangle(25, 550, 475, 750, fill='white', outline='grey')
        canvas.create_text(50, 575, text='· Dinner.  25% ~ 35%', font='Chalkduster 20 bold', fill='grey', anchor='w')
        canvas.create_text(475, 575, text='**kcal >', anchor='e', fill='grey', font='Chalkduster 20 bold')
        r = 6
        canvas.create_oval(314-r, 575-r, 314+r, 575+r, fill='white', outline='grey', width=4)
        if (mode.dinnerPlan != []): 
            for i in range(3): 
                values = mode.app.refreshedD[mode.dinnerPlan[i]]
                canvas.create_text(50, 630+i*50, text=f'· {mode.dinnerPlan[0]}: {values[0]} kcal, {values[1]}g, {values[2]}g, {values[3]}g', anchor='sw', fill='grey')
        

    def redrawAll(mode, canvas): 
        canvas.create_text(25, 25, text='<', font='Chalkduster 30 bold', fill='grey')
        canvas.create_text(mode.width/2, 50, text='Meal Plan Generator', font='Chalkduster 30 bold', fill='grey' )
        mode.drawBreakFastBoard(canvas)
        mode.drawLunchBoard(canvas)
        mode.drawDinnerBoard(canvas)
        if (mode.breakFastWindowOpen): 
            mode.disPlayMealPlans(canvas, 0)
        elif (mode.lunchWindowOpen): 
            mode.disPlayMealPlans(canvas, 1)
        elif (mode.dinnerWindowOpen): 
            mode.disPlayMealPlans(canvas, 2)
    











class HomeMode(Mode): 
    
    def appStarted(mode): 
        # info Part 
        mode.metas = [0, 0, 0, 0] 
        mode.metaWindowOpen = False 
        mode.color = ['white', 'white', 'white', 'white']  # select metabolism
        pass 

    def keyPressed(mode, event): 
        if (event.key == 'f'): 
            mode.app.setActiveMode(mode.app.foodPage)


    def mousePressed(mode, event): 

        # get Metabolism 
        infoList = [mode.app.name, mode.app.gender, mode.app.weight, mode.app.HF, mode.app.HI, mode.app.age]
        if (300<event.x<450) and (75<event.y<110): 
            mode.metas = mode.calculateEatenCalorie(metaUrl, infoList)
            mode.metaWindowOpen = True 
        
        # select metabolism 
        if (mode.metaWindowOpen): 
            if (200 < event.x < 220): 
                if (110 < event.y < 120): 
                    mode.app.totalCalorieNeed = mode.metas[0]
                    mode.color[0] = 'grey'
                    mode.metaWindowOpen = False 
                elif (135 < event.y < 145): 
                    mode.app.totalCalorieNeed = mode.metas[1]
                    mode.color[0] = 'grey'
                    mode.metaWindowOpen = False 
                elif (160 < event.y < 170): 
                    mode.app.totalCalorieNeed = mode.metas[2]
                    mode.color[0] = 'grey'
                    mode.metaWindowOpen = False 
                elif (185 < event.y < 195): 
                    mode.app.totalCalorieNeed = mode.metas[3]
                    mode.color[0] = 'grey'
                    mode.metaWindowOpen = False 
                if (mode.app.totalCalorieNeed.find(',') != -1): 
                    index = mode.app.totalCalorieNeed.index(',')
                    newStr = mode.app.totalCalorieNeed[:index] + mode.app.totalCalorieNeed[index+1:]
                    mode.app.totalCalorieNeed = (int)(newStr)
                else: 
                    mode.app.totalCalorieNeed = (int)(mode.app.totalCalorieNeed)
        
        # Shift to MealPlan 
        if ((340< event.x <455) and (535< event.y <568)):
            mode.app.setActiveMode(mode.app.mealPlanPage)
            

    def calculateEatenCalorie(mode, metaUrl, infoList): 
        bsMetas = getBasalMeta(calculateMeta(metaUrl, infoList))
        return bsMetas

    def drawInfoBoard(mode, canvas): 
        # draw Info 
        canvas.create_rectangle(25, 50, 475, 250, fill='white', outline='grey')
        canvas.create_text(50, 100, text=f'{mode.app.name}', font='Chalkduster 30 bold', fill='grey', anchor='sw')
        canvas.create_text(50, 150, text=f'* Current Goal:  {mode.app.totalCalorieNeed} kcal', font='Chalkduster 15 bold', fill='grey', anchor='sw')
        canvas.create_text(50, 180, text=f'* Current Weight:  {mode.app.weight}', font='Chalkduster 15 bold', fill='grey', anchor='sw')
        canvas.create_text(35, 225, anchor='sw', text=f'^ Maintain: {mode.metas[0]} kcal, Mild: {mode.metas[1]} kcal', font='Times 13 bold', fill=f'{rgbString(200, 200, 200)}')
        canvas.create_text(35, 246, anchor='sw', text=f'^ WeightL: {mode.metas[2]} kcal, Extreme: {mode.metas[3]} kcal', font='Times 13 bold', fill=f'{rgbString(200, 200, 200)}')
        # draw calculate Icon 
        canvas.create_rectangle(300, 75, 450, 110, fill=f'{rgbString(175, 175, 175)}', width=0)
        canvas.create_text(375, 92.5, text='Get Your Metabolism', fill='white', font='Calibri 12 bold')
        

    def drawMetabolismSelectWindow(mode, canvas): 
        if (mode.metaWindowOpen): 
            # info 
            width, height = 250, 100
            canvas.create_rectangle(200, 100, 200+width, 100+height, fill='white', outline='grey', width=3)
            canvas.create_text(220, 125, text=f'Maintain Your Weight: {mode.metas[0]} kcal', font='Chalkduster 10 bold', anchor='sw')
            canvas.create_text(220, 150, text=f'Mild Weight Loss: {mode.metas[1]} kcal', font='Chalkduster 10 bold', anchor='sw')
            canvas.create_text(220, 175, text=f'Weight Loss: {mode.metas[2]} kcal', font='Chalkduster 10 bold', anchor='sw')
            canvas.create_text(220, 200, text=f'Extreme Weight Loss: {mode.metas[3]} kcal', font='Chalkduster 10 bold', anchor='sw')
            # select circle 
            r = 2.5
            canvas.create_oval(210-r, 115-r, 210+r, 115+r, fill=f'{mode.color[0]}', outline='grey', width=2)
            canvas.create_oval(210-r, 140-r, 210+r, 140+r, fill=f'{mode.color[1]}', outline='grey', width=2)
            canvas.create_oval(210-r, 165-r, 210+r, 165+r, fill=f'{mode.color[2]}', outline='grey', width=2)
            canvas.create_oval(210-r, 190-r, 210+r, 190+r, fill=f'{mode.color[3]}', outline='grey', width=2)



    def drawFoodDisplayBoard(mode, canvas): 
        canvas.create_rectangle(25, 275, 475, 475, fill='white', outline='grey')
       

    def drawMealPlanBoard(mode, canvas): 
        # board, Title, Generate Icon
        canvas.create_rectangle(25, 525, 475, 775, fill='white', outline='grey')
        canvas.create_text(35, 535, anchor='nw', text='· Suggested Meal Plan', font='Chalkduster 22 bold', fill='grey')
        canvas.create_rectangle(340, 535, 455, 568, fill='grey', width=0)
        canvas.create_text(397, 550, text='Generate', font='Calibri 20 bold', fill='white')
        

    def redrawAll(mode, canvas): 
        mode.drawInfoBoard(canvas)
        mode.drawMetabolismSelectWindow(canvas)
        mode.drawFoodDisplayBoard(canvas)
        mode.drawMealPlanBoard(canvas)
        pass 
   
    
            
        
   












class FoodMode(Mode): 
    def appStarted(mode): 
        mode.initializeEdges()
        mode.searchBoardOpened = False 
        mode.searchData(calorieUrl)
        pass 

    def searchData(mode, calorieUrl): 
        mode.directory = mode.getFoodData(calorieUrl)
        mode.isTyping, mode.isTypingQuant = False, False 
        mode.keyWord = ''
        mode.textTyping = ''
        mode.quant = ''
        mode.typingQuant = ''
        mode.directoryDict = webScrapCalorie(calorieUrl) # directory
        mode.app.directoryDict = mode.directoryDict

        # displaying searched results 
        mode.matchedOptionsList = None
        mode.showFoodDetail = None 
        # store eaten data 
        [mode.breakFast, mode.lunch, mode.dinner, mode.extra] = [ [] for i in range(4) ]
        mode.meals = [mode.breakFast, mode.lunch, mode.dinner, mode.extra]
        [mode.breakFastQuant, mode.lunchQuant, mode.dinnerQuant, mode.extraQuant] = [ [] for i in range(4)]
        mode.mealsQuant = [mode.breakFastQuant, mode.lunchQuant, mode.dinnerQuant, mode.extraQuant] 
        (mode.currentMeal, mode.currentMealQuant) = (None, None)
        mode.editingWhichMeal = None
        
        mode.intakeCalorie = mode.getTotalCalorie()
        if (mode.app.totalCalorieNeed != 0): 
            mode.leftCalorie = mode.app.totalCalorieNeed-mode.intakeCalorie
        else: 
            mode.leftCalorie = '**'

    def getTotalCalorie(mode): 
        foods = mode.breakFast + mode.lunch + mode.dinner + mode.extra
        if (foods != []): 
            total = 0 
            for i in range(len(food)): 
                calorie = mode.directoryDict[foods[i]]
                total += calorie
            return total 
        else: 
            return 0


    def getFoodData(mode, calorieUrl): 
        resultDict = webScrapCalorie(calorieUrl)
        optionList = []
        for v in resultDict: 
            eachList = [v] + resultDict[v]
            optionList.append(eachList)
        return optionList

    def initializeEdges(mode): 
        mode.margin = 50
        [mode.dashBLen, mode.dashBHei, mode.dashR] = [300, 50, 50]
        mode.bottomBarWidth = 75
        pass 

    def mousePressed(mode, event): 
        if ((0 < event.x < 30) and (0 < event.y < 30) ):
            mode.app.setActiveMode(mode.app.homePage)
            mode.app.directoryDict = mode.directoryDict

        # select which meal 
        if (mode.height-mode.bottomBarWidth < event.y < mode.height): 
            mode.currentMeal, mode.currentMealQuant = [], []
            mode.editingWhichMeal = event.x//125
            mode.searchBoardOpened = True 

        # search board opened 
        if (mode.searchBoardOpened): 
            if (mode.showFoodDetail != None): 
                # Exit detailed window 
                if (420<event.x<450) and (500<event.y<530): 
                    mode.showFoodDetail=None
                # add current food
                elif (50<event.x<450) and (650<event.y<700) and (mode.quant != ''): 
                        mode.currentMeal.append(mode.matchedOptionsList[mode.showFoodDetail][0])
                        mode.currentMealQuant.append(mode.quant)
                        mode.quant=''
                # input quant
                elif (300<event.x<450) and (600<event.y<630): 
                    mode.isTypingQuant=True
                    mode.typingQuant = ''
            else: 
                # select food 
                if (75<event.x<425): 
                    mode.showFoodDetail = (int)((event.y-200)/50)
        

            # type to search food           
            if (100<event.x<400) and (125<event.y<175): 
                mode.isTyping = True 
                mode.keyWord, mode.textTyping = '', ''
                mode.matchedOptionsList = None 
                mode.showFoodDetail = None 
            # Exit search board 
            elif (400<event.x<450) and (125<event.y<175): 
                mode.searchBoardOpened=False
                which = mode.editingWhichMeal
                mode.meals[which] += mode.currentMeal
                mode.mealsQuant[which] += mode.currentMealQuant
                #print(mode.meals[which], mode.mealsQuant[which])
                (mode.currentMeal, mode.currentMealQuant) = (None, None)
            
            
                       

    def keyPressed(mode, event): 
        if (event.key == 'i'): 
            mode.app.setActiveMode(mode.app.infoPage)
        elif (event.key == 'h'): 
            mode.app.setActiveMode(mode.app.homePage)

        # if searchBoard if open 
        if (mode.searchBoardOpened): 
            if (mode.isTyping): 
                # typing keyword 
                if (len(event.key)==1): mode.textTyping += event.key
                elif (event.key == 'Space'): mode.textTyping += ' '
                elif (event.key == 'Delete'): mode.textTyping = mode.textTyping[0:-1]
                elif (event.key == 'Enter'): 
                    mode.isTyping=False 
                    # search for matched food options
                    mode.matchedOptionsList = findMatchFood(mode.directory,mode.keyWord)
                    mode.matchedOptionsList = convertDtoL(mode.matchedOptionsList)
                mode.keyWord=mode.textTyping

            elif (mode.isTypingQuant): 
                #print(event.key)
                if (event.key.isdigit()): mode.typingQuant += event.key
                elif (event.key == 'Delete'): mode.textTyping = mode.textTyping[0:-1]
                elif (event.key == 'Enter'): 
                    mode.isTypingQuant=False 
                mode.quant = mode.typingQuant

            if (mode.showFoodDetail != None): 
                if (event.key=='Down'): mode.showFoodDetail += 1
                elif(event.key=='Up'): mode.showFoodDetail -= 1


    def drawReturn(mode, canvas): 
        canvas.create_text(25, 25, text='<', fill='grey', font='Chalkduster 40 bold')
            
    def drawDashboard(mode, canvas): 
        # draw four lines 
        for i in [1, 3]: 
            canvas.create_line(mode.margin+mode.dashR-25, mode.margin*i, 
                                mode.width-mode.margin-mode.dashR+25, mode.margin*i, fill='grey')
            canvas.create_line(mode.margin, mode.margin*1.5, mode.margin, mode.margin*2.5, fill='grey')
            canvas.create_line(mode.width-mode.margin, mode.margin*1.5, mode.width-mode.margin, mode.margin*2.5, fill='grey')
        # draw four arc
        canvas.create_arc(50, 50, 100, 100, start=90, extent=90, fill='white', outline='grey')
        canvas.create_arc(50, 100, 100, 150, start=180, extent=90, fill='white', outline='grey')
        canvas.create_arc(400, 50, 450, 100, start=0, extent=90, fill='white', outline='grey')
        canvas.create_arc(400, 100, 450, 150, start=0, extent=-90, fill='white', outline='grey')
        # draw Intake and Left
        canvas.create_text(125, 80, text='Intake', fill='grey', font='Chalkduster 20 bold')
        canvas.create_text(mode.width-50-75, 80, text='Left', fill='grey', font='Chalkduster 20 bold')
        canvas.create_text(125, 115, text=f'{mode.intakeCalorie}kCal', fill='grey', font='Chalkduster 20 bold')
        canvas.create_text(mode.width-50-75, 115, text=f'{mode.leftCalorie}kCal', fill='grey', font='Chalkduster 20 bold')
        # draw progress Bar 
        rOut, rIns = 40, 30
        if (mode.app.totalCalorieNeed != 0): 
            percent = mode.intakeCalorie//mode.app.totalCalorieNeed
        else: 
            percent = '**'
        canvas.create_oval(250-rOut, 100-rOut, 250+rOut, 100+rOut, fill='white', outline='grey')
        canvas.create_oval(250-rIns, 100-rIns, 250+rIns, 100+rIns, fill='white', outline='grey')
        canvas.create_text(250, 100, text=f'{percent}%', fill='grey', font='Chalkduster 20 bold')

    def drawTitle(mode, canvas): 
        # draw four lines
        for i in range(1, 5): 
            canvas.create_line(25, 200+i*125, mode.width-25, 200+i*125, fill='grey')
        # draw four titles
        names =  ['Breakfast', 'Lunch', 'Dinner', 'Extra']
        for i in range(4):
            canvas.create_text(25, 210+125*i, text=f'{names[i]}', anchor='nw', font='Chalkduster 20 bold', fill='grey') 
            # calculate and draw calories 
            calories = calculateNutrients(0, mode.directoryDict, mode.meals[i], mode.mealsQuant[i])
            protein = calculateNutrients(1, mode.directoryDict, mode.meals[i], mode.mealsQuant[i])
            fat = calculateNutrients(2, mode.directoryDict, mode.meals[i], mode.mealsQuant[i])
            carbohy = calculateNutrients(3, mode.directoryDict, mode.meals[i], mode.mealsQuant[i])
            canvas.create_text(mode.width-25, 210+125*i, text=f'{calories}kcal>', anchor='ne', font='Chalkduster 20 bold', fill='grey')
            canvas.create_text(mode.width-25, 210+125*i+50, text=f'Prot: {protein}g>', anchor='ne', font='Chalkduster 10 bold', fill='grey')
            canvas.create_text(mode.width-25, 210+125*i+60, text=f'Fat: {fat}g>', anchor='ne', font='Chalkduster 10 bold', fill='grey')
            canvas.create_text(mode.width-25, 210+125*i+70, text=f'Carbo: {carbohy}g>', anchor='ne', font='Chalkduster 10 bold', fill='grey')

        for i in range(4): 
            if (mode.meals[i] != []): 
                for j in range(len(mode.meals[i])): 
                    canvas.create_text(25, 250+125*i+20*j, text=f'{mode.meals[i][j]}, {mode.mealsQuant[i][j]} units', anchor='nw')

    

    def drawBottomBar(mode, canvas): 
        # draw outline 
        canvas.create_rectangle(0, mode.height-mode.bottomBarWidth, mode.width, mode.height, fill='grey')
        # draw text 
        titles = ['BreakFast', 'Lunch', 'Dinner', 'Extra']
        pivots = [i*125 for i in range(5)]
        for i in range(0, 4): 
            canvas.create_text(pivots[i]+125/2, mode.height-20, text=f'{titles[i]}', 
                                fill='white', font='Chalkduster 15 bold')


    def drawSearchResult(mode, canvas): 
        foodList = mode.matchedOptionsList[:9]
        margin, startY = 75, 250
        for i in range(len(foodList)): 
            posiY = startY + 50*i
            canvas.create_line(margin, posiY, mode.width-margin, posiY)
            canvas.create_text(margin, posiY, text=f'{foodList[i][0]}', anchor='sw')
            canvas.create_text(mode.width-margin, posiY, text=f'{foodList[i][1]} kcal', anchor='se')
    
    def drawFoodDetail(mode, canvas, which): 
        if (mode.matchedOptionsList!=None): 
            canvas.create_rectangle(50, 500, 450, 700, width=2, fill='white', outline='grey')
            # Exit Icon 
            canvas.create_rectangle(420, 500, 450, 530, fill=f'{rgbString(220, 220, 220)}', width=0)
            canvas.create_text(435, 515, text='<', font='Chalkduster 20 bold', fill='grey')
            # ADD Icon
            canvas.create_rectangle(50, 650, 450, 700, fill='grey')
            canvas.create_text(250, 675, text='Add', font='Chalkduster 20 bold')
            # Draw Info 
            canvas.create_text(50, 500, anchor='nw', text=f'{mode.matchedOptionsList[which][0]}', font='Chalkduster 20 bold')
            length = (450-50)/3
            nutrients = [mode.matchedOptionsList[which][i] for i in range(2, 5)]
            canvas.create_text(50, 650, anchor='sw', text=f'Protein(g):{nutrients[0]}', font='Chalkduster 15', fill='grey')
            canvas.create_text(50+length, 650, anchor='sw', text=f'Fat(g):{nutrients[1]}', font='Chalkduster 15', fill='grey')
            canvas.create_text(50+2*length, 650, anchor='sw', text=f'Carbo(g):{nutrients[2]}', font='Chalkduster 15', fill='grey')
            # Draw quantity box 
            canvas.create_rectangle(300, 600, 450, 630, fill=f'{rgbString(200, 200, 200)}', width=1, outline='grey')
            canvas.create_text(450, 630, text='units', anchor='se', font='Chalkduster 20 bold', fill='white')
            canvas.create_text(300, 630, anchor='sw', fill='white', font='Chalkduster 20 bold', text=f'{mode.quant}')
        

    def drawFoodSearchBoard(mode, canvas): 
        # border
        if (mode.isTyping): bWidth = 8
        else: bWidth = 5
        canvas.create_rectangle(50, 100, 450, 700, fill='white', outline='grey', width=5)
        # search Area and Exit key 
        canvas.create_rectangle(100, 125, 400, 175, fill=f'{rgbString(240, 240, 240)}', outline='grey', width=bWidth)
        canvas.create_text(425, 150, text='<', font='Chalkduster 30 bold')
        # search Icon and print keyword
        canvas.create_oval(375-13, 150-13, 375+13, 150+13, outline='white', fill=f'{rgbString(240, 240, 240)}', width=5)
        canvas.create_line(375, 150, 390, 165, width=5, fill='white')
        canvas.create_text(100, 170, text=f'{mode.keyWord}', font='Chalkduster 30 bold', fill='black', anchor='sw')
        if (mode.matchedOptionsList != None): 
            mode.drawSearchResult(canvas)
        if (mode.showFoodDetail != None): 
            mode.drawFoodDetail(canvas, mode.showFoodDetail)

    def redrawAll(mode, canvas): 
        mode.drawReturn(canvas)
        mode.drawTitle(canvas)
        mode.drawBottomBar(canvas)
        mode.drawDashboard(canvas)
        if (mode.searchBoardOpened): 
            mode.drawFoodSearchBoard(canvas)
            
















class InfoMode(Mode): 
    def appStarted(mode): 
        # initialize
        mode.text = ''
        mode.hText = ''
        mode.bornText = ''
        [mode.name, mode.weight, mode.heightF, mode.heightI, mode.bornD, mode.bornM, mode.bornY, mode.gender] = ['' for i in range(8)]
        [mode.typeName, mode.typeW, mode.typeHF, mode.typeHI, mode.typeBD, mode.typeBM, mode.typeBY] = [False for i in range(7)]
        (mode.chooseFem, mode.chooseMa) = (False, False)
        mode.initializeEdges()
        pass 

    def initializeEdges(mode): 
        mode.titlePivot = (50, 50)
        mode.completeWidth = 50 
        mode.margin = 25 
        mode.eachWidth = 125 
        (mode.hBoxHei, mode.hBoxLen) = (40, 125)
        (mode.bornHei, mode.bornLen) = (40, 70)
        (mode.genH, mode.genL) = (40, 100)
    
    def getLine(mode, place): 
        upMargin = mode.titlePivot[1] + mode.margin 
        downMargin = mode.completeWidth + mode.margin 
        eachHeight = (mode.height-upMargin-downMargin)/5
        return upMargin + eachHeight*place

    def keyPressed(mode, event): 
        # if key should be in Name or Weight
        if (mode.typeName or mode.typeW): 
            key = str(event.key)
            if (len(key)==1): mode.text += key
            elif (key == 'Space'): mode.text += ' '
            elif (key == 'Delete'): mode.text = mode.text[0:-1]
            if (mode.typeName): 
                mode.name = mode.text
                if (key == 'Enter'): mode.typeName = False 
            elif (mode.typeW): 
                mode.weight = mode.text
                if (key == 'Enter'): mode.typeW = False 

        # if key should be in Height 
        if mode.typeHI or mode.typeHF: 
            if (str(event.key).isdigit()): mode.hText += str(event.key)
            elif (event.key == 'Delete'): mode.hText = mode.hText[0:-1]
            if (mode.typeHI): 
                mode.heightI = mode.hText
                if (event.key == 'Enter'): mode.typeHI = False 
            else: 
                mode.heightF = mode.hText
                if (event.key == 'Enter'): mode.typeHF = False 

        # if key should be in Birthday 
        if (mode.typeBD or mode.typeBM or mode.typeBY): 
            if (str(event.key).isdigit()): mode.bornText += str(event.key)
            elif (event.key == 'Delete'): mode.bornText = mode.bornText[0:-1]
            if (mode.typeBD): 
                mode.bornD = mode.bornText 
                if (event.key == 'Enter'): mode.typeBD = False 
            elif (mode.typeBM): 
                mode.bornM = mode.bornText 
                if (event.key == 'Enter'): mode.typeBM = False 
            else: 
                mode.bornY = mode.bornText 
                if (event.key == 'Enter'): mode.typeBY = False 

    def mousePressed(mode, event): 
        print(event.x, event.y)
        # back to homePage 
        if (0<event.x<50) and (0<event.y<50): 
            mode.app.setActiveMode(mode.app.homePage)
        # click complete 
        elif (0<event.x<mode.width) and (mode.height-mode.completeWidth < event.y < mode.height): 
            mode.app.setActiveMode(mode.app.homePage)
            [mode.app.name, mode.app.weight, mode.app.HF, mode.app.HI, mode.app.gender] = [mode.name, mode.weight, mode.heightF, mode.heightI, mode.gender]
            mode.app.age = getAge(mode.bornD, mode.bornM, mode.bornY)

        # select area to print Name or Weight 
        if (300 < event.x < 475) and (75 < event.y < 200): 
            mode.typeName = True 
            mode.typeW = False 
            mode.text = ''
        elif (300 < event.x < 475) and ( 452.4 < event.y < 578.2): 
            mode.typeW = True 
            mode.typeName = False 
            mode.text = ''
        # select area to print Height 
        posiY = mode.getLine(3)
        if (mode.width-mode.margin-mode.hBoxLen*2 < event.x < mode.width-mode.margin-mode.hBoxLen) and (posiY-mode.hBoxHei < event.y < posiY): 
                mode.typeHF = True 
                mode.typeHI = False 
                mode.hText=''
        elif (mode.width-mode.margin-mode.hBoxLen < event.x < mode.width-mode.margin) and (posiY-mode.hBoxHei < event.y < posiY): 
                mode.typeHI = True 
                mode.typeHF = False 
                mode.hText = ''
        # select birthday part 
        posiY = mode.getLine(2) 
        if (posiY-mode.bornHei < event.y < posiY): 
            if (mode.width-mode.margin-mode.bornLen*3 < event.x < mode.width-mode.margin-mode.bornLen*2): 
                mode.typeBD = True 
                mode.typeBM = mode.typeBY = False 
                mode.bornText = ''
            elif (mode.width-mode.margin-mode.bornLen*2 < event.x < mode.width-mode.margin-mode.bornLen*1): 
                mode.typeBM = True 
                mode.typeBD = mode.typeBY = False 
                mode.bornText = ''
            elif (mode.width-mode.margin-mode.bornLen*1 < event.x < mode.width-mode.margin): 
                mode.typeBY = True 
                mode.typeBD = mode.typeBM = False 
                mode.bornText = ''
        # select Gender 
        posiY = mode.getLine(5)
        if (posiY-mode.genH < event.y < posiY): 
            if (mode.width-mode.margin-mode.genL*2 < event.x < mode.width-mode.margin-mode.genL*1): 
                mode.chooseFem = True 
                mode.chooseMa = False 
                mode.gender = 'F'
            elif (mode.width-mode.margin-mode.genL*1 < event.x < mode.width-mode.margin-mode.genL*0): 
                mode.chooseFem = False 
                mode.chooseMa = True 
                mode.gender='M'

    
    def drawTitleAndComplete(mode, canvas): 
        # draw title 
        (pivotX, pivotY) = mode.titlePivot
        canvas.create_text(pivotX/2, pivotY/2, text='<', font="Times 50 bold", fill='grey')
        canvas.create_text(pivotX+(mode.width-pivotX)/2, pivotY/2, text='Create Your Own Profile', 
                            font='Times 30 bold', fill='grey')
        # draw complete 
        canvas.create_rectangle(0, mode.height-mode.completeWidth, mode.width, mode.height, 
                                fill='grey')
        canvas.create_text(mode.width/2, mode.height-mode.completeWidth/2, text='Complete',
                            font='Times 30 bold', fill='white' )
       

    def drawInputName(mode, canvas): 
        # draw line 
        posiY = mode.getLine(1)
        canvas.create_line(mode.margin, posiY, mode.width-mode.margin, posiY, width=5, fill='grey') 
        canvas.create_text(mode.margin, posiY, text='Name', font='Chalkduster 40 bold',  anchor='sw', fill='grey')
        # input area
        if (not mode.typeName) and (mode.name == ''): 
            canvas.create_text(mode.width-mode.margin, posiY, text='input here -->', font='Calibri 30', 
                                anchor='se', fill=rgbString(175, 175, 175))
        else: 
            canvas.create_text(mode.width-mode.margin, posiY, text=f'{mode.name}', font='Calibri 30', 
                                anchor='se', fill='grey')


    def drawBirthDay(mode, canvas): 
        # draw line 
        posiY = mode.getLine(2)
        canvas.create_line(mode.margin, posiY, mode.width-mode.margin, posiY, width=5, fill='grey') 
        canvas.create_text(mode.margin, posiY, text='Birthday', font='Chalkduster 40 bold',  anchor='sw', fill='grey')
        # control width 
        if (mode.typeBD): widthD=4
        else: widthD = 2.5
        if (mode.typeBM): widthM=4
        else: widthM = 2.5
        if (mode.typeBY): widthY=4
        else: widthY = 2.5
        # draw input area
        canvas.create_rectangle(mode.width-mode.margin-mode.bornLen*3, posiY-mode.bornHei, mode.width-mode.margin-mode.bornLen*2, posiY, 
                        fill='white', width=widthD, )
        canvas.create_rectangle(mode.width-mode.margin-mode.bornLen*2, posiY-mode.bornHei, mode.width-mode.margin-mode.bornLen*1, posiY, 
                        fill='white', width=widthM)
        canvas.create_rectangle(mode.width-mode.margin-mode.bornLen*1, posiY-mode.bornHei, mode.width-mode.margin, posiY, 
                        fill='white', width=widthY)
        canvas.create_text(mode.width-mode.margin-mode.bornLen*2, posiY, text='D', fill='grey', anchor='se', font='Calibri 23')
        canvas.create_text(mode.width-mode.margin-mode.bornLen*1, posiY, text='M', fill='grey', anchor='se', font='Calibri 23')
        canvas.create_text(mode.width-mode.margin-mode.bornLen*0, posiY, text='Y', fill='grey', anchor='se', font='Calibri 23')
        # draw input 
        canvas.create_text(mode.width-mode.margin-mode.bornLen*3+5, posiY, text=f'{mode.bornD}',fill='grey', anchor='sw', font='Calibri 23')
        canvas.create_text(mode.width-mode.margin-mode.bornLen*2+5, posiY, text=f'{mode.bornM}',fill='grey', anchor='sw', font='Calibri 23')
        canvas.create_text(mode.width-mode.margin-mode.bornLen*1+5, posiY, text=f'{mode.bornY}',fill='grey', anchor='sw', font='Calibri 23')


    def drawHeight(mode, canvas): 
        # draw line 
        posiY = mode.getLine(3)
        canvas.create_line(mode.margin, posiY, mode.width-mode.margin, posiY, width=5, fill='grey') 
        canvas.create_text(mode.margin, posiY, text='Height', font='Chalkduster 40 bold',  anchor='sw', fill='grey')
        # draw input area 
        if (mode.typeHF): widthF = 4
        else: widthF = 2.5
        if (mode.typeHI): widthI = 4 
        else: widthI = 2.5
        canvas.create_rectangle(mode.width-mode.margin-mode.hBoxLen*2, posiY-mode.hBoxHei, mode.width-mode.margin-mode.hBoxLen, posiY, 
                                    fill='white', outline='grey', width=widthF)
        canvas.create_text(mode.width-mode.margin-mode.hBoxLen, posiY, text='feet', fill='grey', anchor='se', font='Calibri 23')
        canvas.create_rectangle(mode.width-mode.margin-mode.hBoxLen, posiY-mode.hBoxHei, mode.width-mode.margin, posiY, 
                                    fill='white', outline='grey', width=widthI)
        canvas.create_text(mode.width-mode.margin, posiY, text='inches', fill='grey', anchor='se', font='Calibri 22')
        # draw input 
        canvas.create_text(mode.width-mode.margin-mode.hBoxLen*2+5, posiY, text=f'{mode.heightF}', fill='grey', anchor='sw', font='Calibri 22')
        canvas.create_text(mode.width-mode.margin-mode.hBoxLen+5, posiY, text=f'{mode.heightI}', fill='grey', anchor='sw', font='Calibri 22')


    def drawWeight(mode, canvas): 
        # draw line 
        posiY = mode.getLine(4)
        canvas.create_line(mode.margin, posiY, mode.width-mode.margin, posiY, width=5, fill='grey') 
        canvas.create_text(mode.margin, posiY, text='Weight', font='Chalkduster 40 bold',  anchor='sw', fill='grey')
        # input area
        if (not mode.typeW) and (mode.weight==''): 
            canvas.create_text(mode.width-mode.margin, posiY, text='input here (in pounds)', font='Calibri 30', anchor='se', fill=rgbString(175, 175, 175)) 
        else: 
            canvas.create_text(mode.width-mode.margin, posiY, text=f'{mode.weight}', font='Calibri 30', anchor='se', fill='grey')


    def drawGender(mode, canvas): 
        # draw line 
        posiY = mode.getLine(5)
        canvas.create_line(mode.margin, posiY, mode.width-mode.margin, posiY, width=5, fill='grey') 
        canvas.create_text(mode.margin, posiY, text='Gender', font='Chalkduster 40 bold',  anchor='sw', fill='grey')
        # draw hint 
        canvas.create_rectangle(mode.width-mode.margin-mode.genL*2, posiY-mode.genH, mode.width-mode.margin-mode.genL*1, posiY, fill='white')
        canvas.create_rectangle(mode.width-mode.margin-mode.genL*1, posiY-mode.genH, mode.width-mode.margin-mode.genL*0, posiY, fill='white')
        canvas.create_text(mode.width-mode.margin-mode.genL*1, posiY, text='F', font='Calibri 20', anchor='se', fill='grey')
        canvas.create_text(mode.width-mode.margin-mode.genL*0, posiY, text='M', font='Calibri 20', anchor='se', fill='grey')
        # draw select circle 
        if (mode.chooseFem): colorF = rgbString(100, 100, 100)
        else: colorF = 'white'
        if (mode.chooseMa): colorM = rgbString(100, 100, 100)
        else: colorM = 'white'
        (cMarg, diameter) = (75, 15)
        startPoint = mode.width-mode.margin-mode.genL*2+cMarg
        canvas.create_oval(startPoint, posiY-diameter-5, startPoint-diameter, posiY-5, width=5, fill=colorF, outline='grey')
        canvas.create_oval(startPoint+mode.genL, posiY-diameter-5, startPoint-diameter+mode.genL, posiY-5, width=5, fill=colorM, outline='grey')
        pass 


    def redrawAll(mode, canvas): 
        mode.drawTitleAndComplete(canvas)
        mode.drawInputName(canvas)
        mode.drawBirthDay(canvas)
        mode.drawHeight(canvas)
        mode.drawWeight(canvas)
        mode.drawGender(canvas)
    

class ReportMode(Mode): 
    pass 


class MyModalApp(ModalApp): 
    def appStarted(app): 
        # declare shared data 
        [app.name, app.gender]=['Hanqing Liu', '']
        [app.weight, app.HF, app.HI, app.age]=[1000000, 0, 0, 0]
        app.directoryDict, app.completefoodList = '', []
        app.totalCalorieNeed = 0
        app.refreshedL, app.refreshedD = None, None
        
   
        app.welcomePage = WelcomeMode()
        app.homePage = HomeMode()
        app.foodPage = FoodMode()
        app.infoPage = InfoMode()
        app.report = ReportMode()
        app.mealPlanPage = MealPlanMode()
        app.setActiveMode(app.welcomePage)



app = MyModalApp(width=500, height=900)


