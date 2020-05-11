# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import json
from pymongo import MongoClient
import sys
import time
sys.stdout = open('file', 'w', encoding="utf-8")

url = "https://www.underarmour.com/en-us/new-arrivals/footwear/g/3r272"

# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox()

# get web page
driver.get(url)
driver.maximize_window()

time.sleep(5)

# execute script to slowly scroll down the page
length = 8442
scrollVal = 250
while scrollVal <= length:
    driver.execute_script("scrollBy(0,250);")
    scrollVal = scrollVal + 250


#connect to database
client = MongoClient("mongodb+srv://rjain9:Ilikepie16%21@cluster0-wgm3y.mongodb.net/test?retryWrites=true&w=majority")
db = client["Shoes"]
mycol = db["underarmour"]

aTagsInLi = driver.find_elements_by_xpath("//li[contains(@class,'tile tile')]")
imgTags = driver.find_elements_by_xpath("//img[@class='product-img']")
line_items=[]

x=0
while x < len(aTagsInLi):

    #containers for information
    a = aTagsInLi[x]
    imgTag = imgTags[x]

    #container for site
    aTag = a.find_element_by_tag_name('a')

    #get name of shoe
    name = a.find_element_by_class_name('title').text
    #get site link
    site = aTag.get_attribute('href')
    #get img_url
    image_url = imgTag.get_attribute('src')

    #determine category
    if "Cleat" in name or "Golf" in name:
        category = "Cleates/Spikes"
    elif "Slides" in name:
        category = "Slides"
    else:
        category = "Athletic Shoes"

    #determine gender
    if "Men" in name:
        gender = "Male"
    elif "Women" in name:
        gender = "Female"
    elif "Adult" in name:
        gender = "Unisex"
    else:
        gender = "Kid"

    #create json object for database
    myjson3 = {
                'name': name,
                'image_url': image_url,
                'site': site,
                'category': category,
                'gender': gender
            }
    line_items.append(myjson3)

    x = x+1

#clear existing db
mycol.delete_many({})
#insert new elements into db
mycol.insert_many(line_items)