#!/usr/bin/python3

# Usage: $ python3 GetTickets.py username password
# Purpose: Login to mybama.ua.edu, refresh until the football ticket lottery
# is open (1 PM), and enter in it. Note that the code is naive to timezones.

__author__='mwleeds'

from MyBamaChecker import MyBamaChecker
from datetime import datetime
from time import sleep
import sys

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

def main():
    now = datetime.now()
    future = now.replace(hour=12, minute=58, second=0, microsecond=0)
    delta_t = future - now
    print("opening browser in " + str(delta_t.seconds) + " seconds...")
    sleep(delta_t.seconds)
    crawler = MyBamaChecker(True)
    crawler.login(USERNAME, PASSWORD)
    crawler.click_my_tickets()
    now = datetime.now()
    future = now.replace(hour=13, minute=0, second=0, microsecond=0)
    delta_t = future - now
    print("refreshing in " + str(delta_t.seconds) + " seconds...")
    sleep(delta_t.seconds)
    crawler.refresh()
    crawler.request_tickets() 

if __name__=="__main__":
    main()
