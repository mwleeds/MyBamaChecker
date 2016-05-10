#!/usr/bin/python3

# This script registers for the classes specified in config.ini.
# See the README for more information.

__author__='mwleeds'

import json
from configparser import ConfigParser
from MyBamaChecker import MyBamaChecker

def main():
    config = ConfigParser()
    config.read('config.ini')
    USERNAME = config.get('REGISTER_FOR_CLASSES', 'USERNAME')
    PASSWORD = config.get('REGISTER_FOR_CLASSES', 'PASSWORD')
    SEMESTER = config.get('REGISTER_FOR_CLASSES', 'SEMESTER')
    HEADLESS = config.getboolean('REGISTER_FOR_CLASSES', 'HEADLESS')
    CRNS = json.loads(config.get('REGISTER_FOR_CLASSES', 'CRNS'))
    crawler = MyBamaChecker(HEADLESS)
    crawler.login(USERNAME, PASSWORD)
    crawler.click_add_or_drop_classes()
    crawler.select_term_registration(SEMESTER)
    crawler.register_for_CRNs(CRNS)

if __name__=="__main__":
    main()
