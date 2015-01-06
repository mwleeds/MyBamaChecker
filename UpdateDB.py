#!/usr/bin/python3

##########################################################################
# File: UpdateDB.py
# Last Edit: 2015-01-03
# Author: Matthew Leeds
# Parameters(4): username password term dbfile
# Purpose: Update the database file with the names of every course in
# Alabama's registration system.
##########################################################################

from MyBamaChecker import MyBamaChecker
import sys

# constants
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
TERM = sys.argv[3] # "Fall 2014" for example
DB_FILE = sys.argv[4] # "classes.json" for example

def main():
    spider = MyBamaChecker()
    spider.login(USERNAME, PASSWORD)
    spider.select_term(TERM)
    spider.update_db(USERNAME, PASSWORD, TERM, DB_FILE)
    return

if __name__=="__main__":
    main()
