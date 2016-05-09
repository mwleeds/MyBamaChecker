import sys
import time
import ctypes
from subprocess import Popen
from MyBamaChecker import MyBamaChecker


USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

def main():
    crawler = MyBamaChecker(True)
    crawler.login(USERNAME, PASSWORD)
    crawler.click_student()
    crawler.view_grades()
    crawler.select_term_registration("Spring 2016")
    if crawler.new_grades_posted():
        print("A grade has been posted!")
    sys.exit(0)

if __name__ == "__main__":
    main()
