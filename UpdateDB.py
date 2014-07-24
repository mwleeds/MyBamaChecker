#!/usr/bin/python2.7

##########################################################################
# File: UpdateDB.py
# Last Edit: 7.24.2014
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
DB_FILE = sys.argv[4] # "classes.db" for example

def main():
    spider = MyBamaChecker(USERNAME, PASSWORD)
    spider.select_term(TERM) 
    spider.update_db(DB_FILE)
    return

if __name__=="__main__":
    main()
