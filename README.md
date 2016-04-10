# Code Plagiarism Detection Script
Created for CSE 330 at Washington University in St. Louis. This will pull repositories from a bitbucket account and send files to Moss. 


## Requirements
* Python 2.7

## Initial Setup
Copy repoauth.py.example into repoauth.py and replace the username and password strings. 

Run
```
    python repo-grabber.py
```
to clone all the repositories into the repositories folder. 

## Sending requests to Moss
Run 
```
    python cpds.py [old-files-substring] [new-files-substring]
```
For example, running
```
    python cpds.py module2 spring2016-module2
```
will compare all files in folders with the substring "module2" in their name, with all files in folders with the substring "spring2016-module2" in their name. This will compare all Module 2 folders from the Spring 2016 semester with any Module 2 folder, from the current semester and from previous semesters.

## Author
Brian Lam

Washington University in St. Louis

