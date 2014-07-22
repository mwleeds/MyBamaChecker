#!/usr/bin/python2.7

###################################################################
# 
# File: myBamaChecker.py
# Last Edit: 7.21.14
# Author: Matthew Leeds
# Purpose: Log in to mybama.ua.edu and check class registration
# information automatically.
# 
###################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import sys, time, re, json

# constants
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
DB_FILE = "classes.db"

class MyBamaChecker():

    def __init__(self):
        # load the p<F4>age
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNITWITHJS)
        self.driver.implicitly_wait(30)
        self.driver.get("https://mybama.ua.edu/cp/home/displaylogin")
        # log in
        self.driver.find_element(By.ID, "user").clear()
        self.driver.find_element(By.ID, "user").send_keys(USERNAME)
        self.driver.find_element(By.NAME, "pass").clear()
        self.driver.find_element(By.NAME, "pass").send_keys(PASSWORD)
        self.driver.find_element(By.LINK_TEXT, "Sign In").click()
        # Click on "Look up classes"
        self.driver.find_element(By.LINK_TEXT, "Look up classes").click()
        self.driver.switch_to.frame("content")
    
    def select_term(self, term):
        # takes a term (such as "Fall 2014") as input, 
        # selects it, and submits the form
        Select(self.driver.find_element(By.ID, "term_input_id")).select_by_visible_text(term)
        self.driver.find_element(By.CSS_SELECTOR, "div.pagebodydiv > form > input[type=\"submit\"]").click()

    def select_subject(self, subject):
        # takes a subject (such as "CS-Computer Science") as input, 
        # selects it, and submits the form
        Select(self.driver.find_element(By.ID, "subj_id")).select_by_visible_text(subject)
        self.driver.find_element(By.NAME, "SUB_BTN").click()

    def select_course(self, course):
        # takes a course number (such as "102") as input, selects it, and submits the form
        courses = self.driver.find_elements(By.CSS_SELECTOR, ".dddefault")
        for courseElem in courses:
            if courseElem.text == course:
                form = courseElem.find_element(By.XPATH, "../td[3]/form")
        form.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    
    def get_section_avail(self, section):
        # takes a section number (such as "005") as input and 
        # returns the number of spots available in that section
        rows = self.driver.find_elements(By.XPATH, "//tr")
        for row in rows:
            if row.find_element(By.XPATH, "./*[1]").get_attribute("class") == "dddefault":
                if row.find_element(By.XPATH, "./*[5]").text == section:
                    return row.find_element(By.XPATH, "./*[13]").text

    def update_db(self):
        # Scrapes course and section data for all subjects in the current term,
        # and outputs that data to a file in json format.
        termDict = {}
        inputBox = self.driver.find_element(By.ID, "subj_id")
        for subject in inputBox.find_elements(By.TAG_NAME, "option"):
            subject.click()
        self.driver.find_element(By.NAME, "SUB_BTN").click()
        tables = self.driver.find_elements(By.CSS_SELECTOR, "div.pagebodydiv > .datadisplaytable")
        for table in tables:
            if table.text != "":
                subject = table.find_element(By.XPATH, "./tbody/tr[2]/th")
                sections = subject.find_elements(By.XPATH, "../../tr[position()>2]")
                listOfSections = []
                for section in sections:
                    listOfSections.append(section.text)
                termDict[subject.text] = listOfSections
        outFile = open(DB_FILE, 'w')
        json.dump(termDict, outFile)
        outFile.close()

    def __del__(self):
        self.driver.quit()

def main():
    spider = MyBamaChecker()
    spider.select_term("Fall 2014")
    spider.update_db()
    '''spider.select_subject("CS-Computer Science")
    spider.select_course("102")
    print spider.get_section_avail("005")'''

if __name__=="__main__":
    main()
