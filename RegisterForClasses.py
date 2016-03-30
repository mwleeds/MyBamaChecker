#!/usr/bin/python3

# Usage: $ python3 RegisterForClasses.py username password "term" crn1 crn2 ...
# Purpose: Register for all the classes specified by the Course
# Registration Numbers passed on the command line.

__author__='mwleeds'

from MyBamaChecker import MyBamaChecker
import sys

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
TERM = sys.argv[3] # "Fall 2014" for example
CRNS = sys.argv[4:] # ['45970', '45124', '44405', '44225'] for example

def main():
    crawler = MyBamaChecker(True)
    try:
        crawler.login(USERNAME, PASSWORD)
    except Exception as e:
        print(e)
        return
    crawler.click_add_or_drop_classes()
    crawler.select_term_registration(TERM)
    crawler.register_for_CRNs(CRNS)

if __name__=="__main__":
    main()
