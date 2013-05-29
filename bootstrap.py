#! /usr/bin/python

import sys
import time
import urllib2

def bootstrap(args):
    download_url = "http://mirrors.jenkins-ci.org/war-stable-rc/latest/jenkins.war"
    if args:
        download_url = args[0]
    print "Downloading ", download_url
    req = urllib2.Request(download_url)
    response = urllib2.urlopen(req)
    info = response.info()
    last_modified_str = info["Last-Modified"]
    print last_modified_str
    last_modified = time.strptime(last_modified_str, "%a, %d %b %Y %H:%M:%S %Z")
    print "LTS RC download_url content last modified:", last_modified[:6]
    pass

if __name__ == "__main__":
    bootstrap(sys.argv[1:])
