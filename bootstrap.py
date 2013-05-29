#! /usr/bin/python

# Boostrap Jenkins acceptance test execution

import os
import sys
import time
import urllib2

def download_jenkins_war(url, destination_directory):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    info = response.info()
    url_last_modified = time.strptime(info["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")
    # print "Content last modified:", url_last_modified[:6]
    url_file_name = os.path.join(url.split("/")[-2], url.split("/")[-1])
    destination_file = os.path.join(destination_directory, url_file_name)
    # print "Destination file name is", destination_file
    if os.path.isfile(destination_file):
        file_last_modified = time.ctime(os.path.getmtime(destination_file))
    else:
        file_last_modified = time.ctime(12 * 60 * 60) # Jan 1, 1970
    # print "Local file last modified:", file_last_modified
    if file_last_modified < url_last_modified:
        print "Downloading ", url, "to", destination_file
        destination_dir, file_name = os.path.split(destination_file)
        print "Destination dir", destination_dir, "File name", file_name
        if not os.path.isdir(destination_dir):
            os.makedirs(destination_dir)
            open(destination_file, "wb").write(response.read())

def bootstrap(args):
    download_url = "http://mirrors.jenkins-ci.org/war-stable-rc/latest/jenkins.war"
    if args:
        download_url = args[0]
    download_jenkins_war(download_url, ".")

if __name__ == "__main__":
    bootstrap(sys.argv[1:])
