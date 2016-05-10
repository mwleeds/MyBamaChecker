#!/usr/bin/python3

# This script prints the number of open seats in a course specified in config.ini.
# See the README for more information.

__author__='mwleeds'

from configparser import ConfigParser
from MyBamaChecker import MyBamaChecker

def main():
    config = ConfigParser()
    config.read('config.ini')
    USERNAME = config.get('GET_SECTION_AVAIL', 'USERNAME')
    PASSWORD = config.get('GET_SECTION_AVAIL', 'PASSWORD')
    SEMESTER = config.get('GET_SECTION_AVAIL', 'SEMESTER')
    HEADLESS = config.getboolean('GET_SECTION_AVAIL', 'HEADLESS')
    SUBJECT = config.get('GET_SECTION_AVAIL', 'SUBJECT')
    COURSE_NUMBER = config.get('GET_SECTION_AVAIL', 'COURSE_NUMBER')
    COURSE_SECTION = config.get('GET_SECTION_AVAIL', 'COURSE_SECTION')
    crawler = MyBamaChecker(HEADLESS)
    crawler.login(USERNAME, PASSWORD)
    crawler.click_look_up_classes()
    crawler.select_term_search(SEMESTER)
    crawler.select_subject(SUBJECT)
    crawler.select_course(COURSE_NUMBER)
    print(crawler.get_section_avail(SECTION_NUMBER))

if __name__=="__main__":
    main()
