#!/usr/bin/python3

# This script checks if final grades have been posted since the last run of this script.
# See the README for more information.

__author__='mwleeds'

from configparser import ConfigParser
from MyBamaChecker import MyBamaChecker

def main():
    config = ConfigParser()
    config.read('config.ini')
    USERNAME = config.get('CHECK_GRADES', 'USERNAME')
    PASSWORD = config.get('CHECK_GRADES', 'PASSWORD')
    SEMESTER = config.get('CHECK_GRADES', 'SEMESTER')
    HEADLESS = config.getboolean('CHECK_GRADES', 'HEADLESS')
    crawler = MyBamaChecker(HEADLESS)
    crawler.login(USERNAME, PASSWORD)
    crawler.click_student()
    crawler.view_grades()
    crawler.select_term_registration(SEMESTER)
    if crawler.new_grades_posted():
        print("A grade has been posted!")
    else:
        print("No new grades found.")

if __name__=="__main__":
    main()
