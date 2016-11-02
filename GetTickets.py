#!/usr/bin/python3

# This script logs in to mybama.ua.edu and refreshes the page just before
# the football ticket lottery opens at 1 PM, and enters it.
# Note that the code is naive to concept of timezones.
# See the README for more information.

__author__='mwleeds'

from datetime import datetime
from time import sleep
from configparser import ConfigParser
from MyBamaChecker import MyBamaChecker

def main():
    config = ConfigParser()
    config.read('config.ini')
    USERNAME = config.get('GET_TICKETS', 'USERNAME')
    PASSWORD = config.get('GET_TICKETS', 'PASSWORD')
    HEADLESS = config.getboolean('GET_TICKETS', 'HEADLESS')
    now = datetime.now()
    future = now.replace(hour=12, minute=58, second=0, microsecond=0)
    delta_t = future - now
    print("opening browser in " + str(delta_t.seconds) + " seconds...")
    sleep(delta_t.seconds)
    crawler = MyBamaChecker(HEADLESS)
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
