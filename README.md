# MyBamaChecker

These scripts can be used to automate various tasks on the University of Alabama's 
student/employee portal, MyBama (which uses Banner software). The MyBamaChecker class
is where all the interesting code is; other files just call methods in that.

## System Requirements

* Python3
* the selenium Python module
* Firefox (ideally ESR but the latest release may work) OR a Selenium Server instance

## Usage

If you intend to use HTMLUNITWITHJS instead of Firefox as your browser (good for headless machines),
download the selenium server standalone jar and run it with `$ java -jar selenium-server-standalone....jar`
and leave that running while you run the script. Otherwise just ensure you have Firefox installed.
Of course edit the line that intsantiates the MyBamaChecker object if you want to configure that.


To print the number of spots available in a section for example:
```
$ python3 GetSectionAvail.py username password "Fall 2014" "CS-Computer Science" 200 001
```

To register for some classes for example:
```
$ python3 RegisterForClasses.py username password "Fall 2016" 45970 44405 44663 48386 50232 48001
```


These commands should work on Windows but have only been tested on Linux.


