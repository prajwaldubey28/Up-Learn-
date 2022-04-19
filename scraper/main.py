from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

import time
import requests
import sqlite3

URL = "https://www.shiksha.com/b-tech-bachelor-of-technology-chp"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome("driver\chromedriver.exe", options = options)
driver.get(URL)

body = driver.find_element_by_css_selector('body')
for i in range(9):
    body.send_keys(Keys.PAGE_DOWN)

########################################################## api
def data(id):
    API = "https://apis.shiksha.com/apigateway/instituteapi/v4/info/getInstituteData?instituteId={}".format(id)
    response = requests.get(API).json()
    return response
########################################################## api

########################################################## sqlite
conn = sqlite3.connect('college_data.db')
conn.execute('''CREATE TABLE engineering_colleges(id INT NOT NULL PRIMARY KEY, abbrevation VARCHAR(20), name TEXT NOT NULL, about TEXT, rating VARCHAR(5), location VARCHAR(30), image TEXT, link TEXT);''')
conn.close()
########################################################## sqlite

time.sleep(2)

ctr = 1
arr = []
for i in range(1, 71):
    print("________ Page No. {} ________".format(i))
    content = driver.page_source
    soup = BeautifulSoup(content, features = "html.parser")
    for j in soup.findAll('a', href = True, attrs = {'class':'lnk ripple dark'}):
        link = "https://www.shiksha.com" + j["href"]

        id = link.split("-")[-1]
        response = data(id)

        college_id = response["data"]["listingId"]
        abbrevation = response["data"]["abbrevation"]
        name = response["data"]["listingName"]
        about = response["data"]["aboutCollege"]

        arr.append(link)

        ########################################################## sqlite
        conn = sqlite3.connect('college_data.db')
        cursor = conn.cursor()
        query = "INSERT INTO engineering_colleges(id, abbrevation, name, about, link) VALUES (?, ?, ?, ?, ?);"
        try:
            data_tuple = (id, abbrevation, name, about, link)
            cursor.execute(query, data_tuple)
            conn.commit()
            conn.close()
        except:
            pass
        ########################################################## sqlite

        print("{}) {}".format(ctr, name))
        ctr += 1

    if i != 70:
        next_btn = '//*[@id="ChpDesktop"]/section/div[2]/div[1]/section[2]/div/div[2]/div/div[4]/div/a[2]'
        btn = driver.find_element(By.XPATH, next_btn).click()
    time.sleep(2)

driver.close()

ctr = 1
for i in arr:

    print("{}) {}".format(ctr, i))
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome("driver\chromedriver.exe", options=options)
    driver.get(i)

    link = i.split("-")
    id = link[-1]

    time.sleep(2)

    content = driver.page_source
    soup = BeautifulSoup(content, features = "html.parser")

    try:
        loc = soup.find_all(class_="ilp-loc")
        for i in loc:
            location = i.find('span').text.strip()
    except:
        print("!!!!!!!!!!!!!!! ERROR {}".format(id))
        continue

    try:
        image = driver.find_element(By.XPATH, '//*[@id="iulp"]/section/div/div[1]/div/div[2]/div[2]/div/div[1]/img').get_attribute("src")
    except:
        print("!!!!!!!!!!!!!!! ERROR {}".format(id))
        continue

    try:
        rating = soup.find(class_="rating-block rvw-lyr").text
    except:
        print("!!!!!!!!!!!!!!! ERROR {}".format(id))
        continue

    ######################################################### sqlite
    conn = sqlite3.connect('college_data.db')
    cursor = conn.cursor()
    query = "UPDATE engineering_colleges SET location = ?, rating = ?, image = ? WHERE id = ?"
    data_tuple = (location, rating, image, id)
    cursor.execute(query, data_tuple)
    conn.commit()
    conn.close()
    ######################################################### sqlite

    driver.close()
    ctr += 1