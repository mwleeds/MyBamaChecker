#!/usr/bin/python3

###################################################################
# File: GetSectionAvail.py
# Last Edit: 2015-01-03
# Author: Matthew Leeds
# Parameter(6): username password term subject course section
# Purpose: Return the number of spots open for a specified course
# and section using Alabama's registration system.
#
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
    crawler = MyBamaChecker()
    try:
        crawler.login(USERNAME, PASSWORD)
    except Exception as e:
        print(e)
        return
    crawler.click_look_up_classes()
    crawler.select_term_search(TERM)
    crawler.select_subject(SUBJECT)
    crawler.select_course(COURSE)
    print(crawler.get_section_avail(SECTION))
    return

if __name__=="__main__":
    main()
