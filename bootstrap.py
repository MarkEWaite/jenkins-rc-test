#! /usr/bin/python

import os
import sys
import time
import urllib2

def download_jenkins_war(url, destination_directory):
    print "Downloading ", url
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    info = response.info()
    url_last_modified = time.strptime(info["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")
    print "Content last modified:", url_last_modified[:6]
    url_file_name = url.split("/")[-1]
    print "URL file name is", url_file_name
    destination_file = os.path.join(destination_directory, url_file_name)
    print "Destination file name is", destination_file
    if os.path.isfile(destination_file):
        file_last_modified = time.ctime(os.path.getmtime(destination_file))
    else:
        file_last_modified = time.ctime(12 * 60 * 60) # Jan 1, 1970
    print "Local file last modified:", file_last_modified
    pass

def bootstrap(args):
    download_url = "http://mirrors.jenkins-ci.org/war-stable-rc/latest/jenkins.war"
    if args:
        download_url = args[0]
    download_jenkins_war(download_url, ".")
    pass

if __name__ == "__main__":
    bootstrap(sys.argv[1:])
