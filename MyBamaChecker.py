#!/usr/bin/python3

# Purpose: Class used to log in to mybama.ua.edu and perform various
# functions such as registering for classes or entering the football
# ticket lottery. See the README for more info.

#TODO add more docstrings
#TODO organize the methods better

__author__='mwleeds'

import sys
import time
import json
import timeit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

class MyBamaChecker(object):

    def __init__(self, headless=False):
        if headless:
            from pyvirtualdisplay import Display
            Display(visible=0, size=(2000, 1600)).start()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(60)
        self.driver.maximize_window()

    def login(self, username, password):
        self.driver.get("https://mybama.ua.edu/cp/home/displaylogin")
        # log in
        self.driver.find_element(By.ID, "username").clear()
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.ID, "button").click()

        # Periodically check if the login was successful;
        # this should give the user time to do 2FA
        for i in range(20):
            time.sleep(1)
            if self.driver.current_url.startswith("https://mybama.ua.edu"):
                return
        raise Exception("ERROR: Invalid login credentials.")

    def click_student(self):
        self.driver.find_element(By.LINK_TEXT, "Student").click()

    def view_grades(self):
        self.driver.find_element(By.LINK_TEXT, "Student Services").click()
        self.driver.find_element(By.LINK_TEXT, "Student Records").click()
        self.driver.find_element(By.LINK_TEXT, "Final Grades").click()
        self.driver.switch_to.frame("content")

    def new_grades_posted(self):
        grades = {}
        try:
            with open('grades.json') as f:
                grades = json.load(f)
        except FileNotFoundError:
            pass
        table = self.driver.find_element(By.CSS_SELECTOR, "table.datadisplaytable:nth-child(4)")
        rows = table.find_elements(By.XPATH, "./tbody/tr")
        new = False
        for i, row in enumerate(rows):
            if i == 0 or i == len(rows) - 1: continue
            crn = row.find_element(By.XPATH, "./td[1]").text
            grade = row.find_element(By.XPATH, "./td[6]").text
            if crn not in grades:
                grades[crn] = grade
            elif grades[crn] != grade:
                new = True
                grades[crn] = grade
        with open('grades.json', 'w') as f:
            json.dump(grades, f)
        return new

    def click_look_up_classes(self):
        # Click on "Look up classes"
        self.driver.find_element(By.LINK_TEXT, "Look up classes").click()
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def click_add_or_drop_classes(self):
        # Click on "Add or drop classes"
        self.driver.find_element(By.LINK_TEXT, "Add or drop classes").click()
        self.driver.switch_to.frame("content")

    def click_hours(self):
        self.driver.get("https://bnrsupport.ua.edu/CASSSO/action/wfsso")
        time.sleep(4)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(1)
        time.sleep(1)
        self.driver.find_element(By.ID, "ext-gen15").click()
        time.sleep(2)
        self.driver.switch_to.frame(1)
        # Close the bottom panel so the screen isn't too cramped
        self.driver.find_element(By.ID, "ext-gen186").click()

    def enter_hours(self, day_blacklist, hours):
        time.sleep(2)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(1)
        for num in [188,189]:
            days_input = 0
            table = self.driver.find_element(By.XPATH, "//table[@id='ext-gen" + str(num) + "']")
            row = table.find_element(By.XPATH, "./tbody[1]/tr[1]")
            # Skip the week if hours have already been put in.
            if "unpopulated" not in row.get_attribute("class"):
                continue
            for i in range(7): # for each day of the week
                dayRow = table.find_element(By.XPATH, "./tbody["+str(i+1)+"]")
                # Skip the day if it's been blacklisted.
                if dayRow.find_element(By.XPATH, "./tr[1]/td[1]").get_attribute("title").split(" ")[1] in day_blacklist:
                    continue
                else:
                    days_input += 1
                ActionChains(self.driver).move_to_element(dayRow).perform()
                dayHours = hours[i]
                for i, shift in enumerate(dayHours):
                    time.sleep(1)
                    if i > 0:
                        # click + button to add a row
                        dayRow.find_element(By.XPATH, "./tr[1]/td[2]/img").click()
                        time.sleep(1)
                    shiftRow = dayRow.find_element(By.XPATH, "./tr["+str(2*i+1)+"]")
                    start = shiftRow.find_element(By.XPATH, "./td["+("5" if i>0 else "6")+"]/div[2]/div[1]/input")
                    self.click_body()
                    ActionChains(self.driver).move_to_element(dayRow).perform()
                    start.clear()
                    start.send_keys(shift.split(",")[0])
                    time.sleep(1)
                    self.click_body()
                    time.sleep(1)
                    end = shiftRow.find_element(By.XPATH, "./td["+("6" if i>0 else "7")+"]/div[2]/div[1]/input")
                    self.click_body()
                    ActionChains(self.driver).move_to_element(end).click().perform()
                    end.clear()
                    end.send_keys(shift.split(",")[1])
                    time.sleep(1)
                    self.click_body()
            if days_input > 0: break # only do the first week if it succeeded

    def save_hours(self):
        saveButton = self.driver.find_element(By.ID, "ext-gen64")
        ActionChains(self.driver).move_to_element(saveButton).click().perform()
        time.sleep(3)

    def click_body(self):
        body = self.driver.find_element(By.XPATH, "/html/body")
        body.click()
        body.send_keys(Keys.ESCAPE)

    def select_term_search(self, term):
        # takes a term (such as "Fall 2014") as input, selects it, and submits the form
        Select(self.driver.find_element(By.ID, "term_input_id")).select_by_visible_text(term)
        self.driver.find_element(By.CSS_SELECTOR, "div.pagebodydiv > form > input[type='submit']").click()

    def select_term_registration(self, term):
        # takes a term (such as "Fall 2014") as input, selects it, and submits the form
        Select(self.driver.find_element(By.ID, "term_id")).select_by_visible_text(term)
        self.driver.find_element(By.CSS_SELECTOR, "div.pagebodydiv > form > input[type='submit']").click()

    def select_subject(self, subject):
        # takes a subject (such as "CS-Computer Science") as input, selects it, and submits the form
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

    def register_for_CRNs(self, CRNs):
        # CRNs should be an iterable containing CRNs as strings.
        # They'll all be put into the Add Classes Worksheet and submitted.
        crn_table = self.driver.find_element(By.XPATH, "//table[@summary=\"Add Classes Data Entry\"]")
        for i, crn in enumerate(CRNs):
            input_box = crn_table.find_element(By.ID, "crn_id" + str(i+1))
            input_box.send_keys(crn)
        self.driver.find_element(By.XPATH, "//input[@value=\"Submit Changes\"]").click()
        time.sleep(2)

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
                    if len(section.strip()) > 0:
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
            self.driver.switch_to_default_content()
            self.driver.switch_to.frame("nav")
            self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr[1]/td/table[2]/tbody/tr[2]/td[11]/a/img").click()
            self.login(username, password)
            self.select_term(term)
            self.driver.switch_to_default_content()
            self.driver.switch_to.frame("content")

    def click_my_tickets(self):
        self.driver.find_element(By.ID, "myticketslink").click() 
        self.driver.switch_to.frame("content")

    def refresh(self):
        self.driver.refresh()
        self.driver.switch_to.frame("content")
    
    def request_tickets(self): 
        requestButton = self.driver.find_element(By.XPATH, "/html/body/div[3]/form/input[6]")
        if requestButton.get_attribute("value") == "Request Ticket":
            requestButton.click()
            self.driver.switch_to_alert().accept()

    def __del__(self):
        self.driver.quit()

