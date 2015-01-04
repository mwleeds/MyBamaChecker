#!/usr/bin/python3

###################################################################
# 
# File: MyBamaChecker.py
# Last Edit: 2015-01-03
# Author: Matthew Leeds
# Purpose: Class used to log in to mybama.ua.edu and check class 
# registration information automatically. Assumes selenium is 
# installed and a selenium server is running if you want to use 
# an htmlunit instead of FF/Chrome.
# 
###################################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import sys, time, json

class MyBamaChecker(object):

    def __init__(self):
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.HTMLUNITWITHJS)
        self.driver.implicitly_wait(30)

    def login(self, username, password):
        self.driver.get("https://mybama.ua.edu/cp/home/displaylogin")
        # log in
        self.driver.find_element(By.ID, "user").clear()
        self.driver.find_element(By.ID, "user").send_keys(username)
        self.driver.find_element(By.NAME, "pass").clear()
        self.driver.find_element(By.NAME, "pass").send_keys(password)
        self.driver.find_element(By.LINK_TEXT, "Sign In").click()
        if "Failed Login" in self.driver.page_source:
            raise Exception("ERROR: Invalid login credentials.")
            return
        # Click on "Look up classes"
        self.driver.find_element(By.LINK_TEXT, "Look up classes").click()
        self.driver.switch_to.frame("content")
    
    def select_term(self, term):
        # takes a term (such as "Fall 2014") as input, 
        # selects it, and submits the form
        Select(self.driver.find_element(By.ID, "term_input_id")).select_by_value("201440")
        self.driver.find_element(By.CSS_SELECTOR, "div.pagebodydiv > form > input[type='submit']").click()

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

    def update_db(self, username, password, term, filename):
        # Scrapes course and section data for all subjects in the current term,
        # and outputs that data to a file in json format.
        outFile = open(filename, 'w+')
        try:
            loadedDict = json.load(outFile) # in case a previous try failed part way
        except ValueError: # empty file
            loadedDict = {}
        outFile.close()
        stay = True
        while stay: # while there are subjects left to scrape
            inputBox = self.driver.find_element(By.ID, "subj_id")
            foundOne = False
            for subject in inputBox.find_elements(By.TAG_NAME, "option"):
                if subject.text not in loadedDict: # select untouched subjects
                    subject.click()
                    foundOne = True
            stay = foundOne # break from loop when finished
            self.driver.find_element(By.NAME, "SUB_BTN").click()
            self.driver.switch_to_default_content()
            self.driver.switch_to.frame("content")
            #print(self.driver.page_source)
            try:
                thisTable = self.driver.find_element(By.XPATH, "//div[@class='pagebodydiv']/table[@class='datadisplaytable' and position()=2]")
            except NoSuchElementException:
                f = open('dump.html', 'w+')
                f.write(self.driver.page_source)
                f.close()
                raise
            subjectName = thisTable.find_element(By.XPATH, "./tbody/tr[2]/th").text
            print("subject: " + subjectName)
            courses = thisTable.find_elements(By.XPATH, "./tbody/tr[position()>2]")
            numCourses = len(courses)
            coursesDict = {} # to hold courses and sections in a subject
            for j in range(3, numCourses + 3):
                self.driver.switch_to_default_content()
                self.driver.switch_to.frame("content")
                thisSubject = self.driver.find_element(By.XPATH, "//div[@class='pagebodydiv']/table[@class='datadisplaytable' and position()=2]")
                course = thisSubject.find_element(By.XPATH, "./tbody/tr[position()=" + str(j) + "]")
                courseName = course.text
                print(courseName)
                courseSections = []
                course.find_element(By.XPATH, "./td[3]/form/input[@type='submit']").click()
                rows = self.driver.find_elements(By.XPATH, "//div[@class='pagebodydiv']/form/table[@class='datadisplaytable']/tbody/tr[position()>2]")
                for row in rows:
                    # append each section number to the list
                    section = row.find_element(By.XPATH, "./td[5]").text
                    if len(section) > 0:
                        courseSections.append(section)
                print(courseSections)
                coursesDict[courseName] = courseSections
                self.driver.back()
            loadedDict[subjectName] = coursesDict
            outFile = open(filename, 'w')
            json.dump(loadedDict, outFile)
            outFile.write("\n")
            outFile.close()
            # log out and back in to prevent a time-out
            #print("relogging")
            self.driver.switch_to_default_content()
            self.driver.switch_to.frame("nav")
            self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr[1]/td/table[2]/tbody/tr[2]/td[11]/a/img").click()
            self.login(username, password)
            self.select_term(term)
            self.driver.switch_to_default_content()
            self.driver.switch_to.frame("content")

    def __del__(self):
        self.driver.quit()

