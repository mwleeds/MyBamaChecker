# MyBamaChecker

These scripts can be used to automate various tasks on the University of Alabama's 
student/employee portal, MyBama (which uses Banner software). The MyBamaChecker class
is where all the interesting code is; other files just call methods in that.

## System Requirements

* Python3
* the selenium Python module
* Firefox (ideally ESR but the latest release may work)

And if you want to run it on a headless machine (without a GUI):
* the pyvirtualdisplay Python module
* An X11 Virtual Frame Buffer (xvfb package for Ubuntu/Debian or XQuartz for OS X)

## Usage

1. Ensure that your system meets the requirements listed above.
2. Edit the `config.ini` file in this directory with your login credentials.
Also ensure that HEADLESS is set to True if you want to run the scripts without
an actual Firefox window popping up (such as on a server).
3. Run the appropriate script from the command line:

To print the number of spots available in the configured section for example:
```
$ python3 GetSectionAvail.py
```

To register for the classes with the configured CRNs:
```
$ python3 RegisterForClasses.py
```

To enter hours for the week as an employee:
```
$ python3 EnterHours.py
```

To enter the football ticket lottery at 1 PM:
```
$ python3 GetTickets.py
```

To check if any final grades have been updated since the last run of this script:
```
$ python3 CheckGrades.py
```

## Notes

* You can of course use crontab to periodically run these commands without human intervention.

* These commands should work on Windows or OS X but have only been tested on Linux.

* If you run these on a mail server you can use their output to trigger email notifications.

