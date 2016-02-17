#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import re
import subprocess
import sys
import thread
import requests
import time
import concurrent.futures
from pprint import pprint
from lxml import html

# Atomic variable lock for thread pool count
# lock = thread.allocate_lock()

thread_count = 0

## Grab a URL from a moss call
## Regex Source:
##
## http://stackoverflow.com/questions/6883049/
##      regex-to-find-urls-in-string-in-python

def get_url(response):
    urls = \
        re.findall("""http[s]?://(?:[a-zA-Z]|
            [0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F]
            [0-9a-fA-F]))+"""
                   , response)
    if len(urls) > 0:
        return urls[0]
    else:
        return None


## Get all percentages from a moss URL

def get_percentages(url):
    page = requests.get(url)
    content = page.content
    percentages = re.findall('[0-9]+%', content)
    return percentages


## Scrape a moss URL to find the highest percentage match

def get_high_percentages(url, cutoff):
    high_score = False
    percentages = get_percentages(url)
    if len(percentages) > 0:
        for score in percentages:
            score = int(score.strip('%'))
            if score > cutoff:
                high_score = True
    return high_score


## See if two files should be compared. Compare them if they are

def compare_files(_old, _new, output_filename):
    global thread_count
    cutoff = 70
    if get_extension(_new) == get_extension(_old) and _new != _old:
        response = subprocess.check_output(['moss/moss', _new, _old])
        url = get_url(response)
        if url is None:
            exit
        high_score = get_high_percentages(url, cutoff)
        if high_score:
            percentages = get_percentages(url)
            print '****************'
            print '***** ALERT ****'
            print '****************'
            print _new
            print _old
            for _score in percentages:
                print _score
            print url
            with open(output_filename, 'a') as file:
                file.write('******' + '\n')
                file.write(_new + '\n')
                file.write(_old + '\n')
                file.write(url + '\n')
                for _score in percentages:
                    file.write(str(_score) + '\n')
        else:
            print 'Okay: ' + url


## Send moss request

def moss_compare(new_files, old_files):
    global thread_count

    output_filename = sys.argv[1] + '_comp_' + sys.argv[2] + '.txt'
    print 'Writing output to ' + output_filename

    executor = concurrent.futures.ProcessPoolExecutor(max_workers=10)

    for _new in new_files:
        for _old in old_files:
            futures = executor.submit(compare_files, _new, _old,
                output_filename)

      # compare_files(_new, _old, output_filename)

## Grab file extension

def get_extension(file_path):
    extension = os.path.splitext(file_path)[1]
    return extension


## Return files with matched name

def walk(substring='.php'):
    matched_files = []
    _dir = os.getcwd() + '/repositories'
    for (root, dirs, files) in os.walk(_dir):
        for file in files:
            path = os.path.join(root, file)
            if substring in path:
                if not '.git' in path:
                    matched_files.append(path)
    return matched_files


## Usage

def printUsage():
    print 'USAGE:'
    print 'python file-walker.py [new modules] [old modules]'
    print "  Grab files whose full path contains the given substring, such as 'spring2015-module1'"


## MAIN

if __name__ == '__main__':
    if len(sys.argv) > 2:
        old_files = walk(sys.argv[1])
        print 'Grabbed old files'
        new_files = walk(sys.argv[2])
        print 'Grabbed new files'
        moss_compare(new_files, old_files)
    else:
        printUsage()

      