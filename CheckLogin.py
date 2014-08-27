#!/usr/bin/python2.7

#####################################################################
# File: CheckLogin.py
# Last Edit: 8.15.14
# Author: Matthew Leeds
# Parameter(6): username password
# Purpose: Checks login credentials by testing them on mybama.ua.edu.
#####################################################################

from MyBamaChecker import MyBamaChecker
import sys

# constants
USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

def main():
    spider = MyBamaChecker()
    try:
        spider.login(USERNAME, PASSWORD)
    except Exception as e:
        print "0"
    else:
        print "1"
    return

if __name__=="__main__":
    main()
