#!/usr/bin/python3

# This script enters the hours configured in config.ini into the Workforce system.
# See the README for more information.

__author__='mwleeds'

import json
from configparser import ConfigParser
from MyBamaChecker import MyBamaChecker

def main():
    config = ConfigParser()
    config.read('config.ini')
    USERNAME = config.get('ENTER_HOURS', 'USERNAME')
    PASSWORD = config.get('ENTER_HOURS', 'PASSWORD')
    HEADLESS = config.getboolean('ENTER_HOURS', 'HEADLESS')
    HOURS = json.loads(config.get('ENTER_HOURS', 'HOURS'))
    BLACKLIST = json.loads(config.get('ENTER_HOURS', 'BLACKLIST'))
    crawler = MyBamaChecker(HEADLESS)
    crawler.login(USERNAME, PASSWORD)
    crawler.click_hours()
    crawler.enter_hours(BLACKLIST, HOURS)
    crawler.save_hours()

if __name__=="__main__":
    main()
