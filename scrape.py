from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import functools
import re
import os
import time
import pathlib
import numpy as np
import json

class Recipe:
    """
    Class of recipe from website Gladkokken.no

    Attributes:
        name(str): name of recipe
        url(str): link to recipe
        imageUrl(str): link to image of recipe
    """
    def __init__(self, name, url, imageUrl):
        self.name = name
        self.url = url
        self.imageUrl = imageUrl
    def __str__(self):
        return self.name


url ="https://gladkokken.no/oppskrifter/middag/"
options = Options()
options.headless = True
#Get current directory
driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\Alan\Downloads\geckodriver-v0.29.1-win64\geckodriver.exe')
driver.get(url)

recipes = []
#Go through all pages until next-button does not work
while True:
    try:
        parser = BeautifulSoup(driver.page_source, "lxml")
        #get list of all recipe items (as li elements)
        recipe_list = parser.find("ul", {"class": "-recipes"}).find_all("li")
        for recipe_item in recipe_list:
            #find desired information
            recipe_url = recipe_item.find('a', href=True)['href']
            recipe_name = recipe_item.find('h2').text.strip()
            recipe_image_url = recipe_item.find('img')["data-src"]
            #create new class and add to class
            newRecipe = Recipe(recipe_name, recipe_url, recipe_image_url)
            recipes.append(newRecipe)
        #find next button and continue to next page
        nextButton = driver.find_element_by_class_name("-next")
        time.sleep(2)
        nextButton.click()
    except Exception as e:
        print(e)
        break
#Create json file
json_dict = {"recipes": []}
for r in recipes:
    jsonStr = json.dumps(r.__dict__)
    json_dict["recipes"].append(json.loads(jsonStr))
#Set to current directory and save json file
currentDir = pathlib.Path(__file__).parent.absolute()
os.chdir(currentDir)
with open("oppskrifter.json", "w") as write_file:
    json.dump(json_dict, write_file)
driver.quit()







