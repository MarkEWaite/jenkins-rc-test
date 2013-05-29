#! /usr/bin/python

import urllib2
import sys

def bootstrap(args):
    download_url = "http://mirrors.jenkins-ci.org/war-stable-rc/latest/jenkins.war"
    if args:
        download_url = args[0]
    print "Download URL is", download_url
    pass

if __name__ == "__main__":
    bootstrap(sys.argv[1:])
