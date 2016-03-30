#!/usr/bin/python3

# Usage: $ python3 EnterHours.py username password
# Purpose: Enter worked hours for the week into the Workforce system.

__author__='mwleeds'

from MyBamaChecker import MyBamaChecker
import sys

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
# HOURS is a list of lists of strings starting with Sunday
HOURS = [["12:00 pm,3:30pm"], ["8:00am,10:30am"], ["12:30pm,3:00pm"], ["1:00pm,5:00pm"], ["12:30pm,4:00pm"], ["1:00pm,5:00pm"], []]
# BLACKLIST is a list of "MM/DD" dates that shouldn't have hours input.
BLACKLIST = ["03/13", "03/14", "03/15", "03/16", "03/17", "03/18", "03/19"]

def main():
    crawler = MyBamaChecker(False) # use True on headless machines
    crawler.login(USERNAME, PASSWORD)
    crawler.click_hours()
    crawler.enter_hours(BLACKLIST, HOURS)
    crawler.save_hours()

if __name__=="__main__":
    main()
