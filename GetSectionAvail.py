#!/usr/bin/python2.7

###################################################################
# File: GetSectionAvail.py
# Last Edit: 7.24.14
# Author: Matthew Leeds
# Parameter(6): username password term subject course section
# Purpose: Return the number of spots open for a specified course
# and section using Alabama's registration system.
###################################################################

from MyBamaChecker import MyBamaChecker
import sys

# constants
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
TERM = sys.argv[3] # "Fall 2014" for example
SUBJECT = sys.argv[4] # "CS-Computer Science" for example
COURSE = sys.argv[5] # "102" for example
SECTION = sys.argv[6] # "005" for example

def main():
    spider = MyBamaChecker(USERNAME, PASSWORD)
    spider.select_term(TERM)
    spider.select_subject(SUBJECT)
    spider.select_course(COURSE)
    print spider.get_section_avail(SECTION)
    return

if __name__=="__main__":
    main()
