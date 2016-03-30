# MyBamaChecker

These scripts can be used to automate various tasks on the University of Alabama's 
student/employee portal, MyBama (which uses Banner software). The MyBamaChecker class
is where all the interesting code is; other files just call methods in that.

## System Requirements

* Python3
* the selenium Python module
* the pyvirtualdisplay Python module (if you want to run it without a GUI)
* Firefox (ideally ESR but the latest release may work)

## Usage

Ensure that your system meets the requirements listed above. If you don't have a graphical display,
edit the line that intsantiates the MyBamaChecker object and change the headless parameter to True.

To print the number of spots available in a section for example:
```
$ python3 GetSectionAvail.py username password "Fall 2014" "CS-Computer Science" 200 001
```

To register for some classes for example:
```
$ python3 RegisterForClasses.py username password "Fall 2016" 45970 44405 44663 48386 50232 48001
```

To enter hours for the week as an employee:
```
$ python3 EnterHours.py username password
```

To enter the football ticket lottery at 1 PM:
```
$ python3 GetTickets.py username password
```

## Notes

* You can of course use crontab to periodically run these commands without human intervention.

* These commands should work on Windows but have only been tested on Linux.

* If you pass your password on the command line (rather than editing the scripts), it may be saved by your shell (in the ~/.bash_history file for Bash) which is obviously a security risk.

