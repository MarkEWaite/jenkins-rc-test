#! /usr/bin/python

# Boostrap Jenkins acceptance test execution

import os
import sys
import time
import urllib2

def download_jenkins_war(url, destination_directory=None):
    if not destination_directory:
        if os.environ.has_key("JENKINS_HOME"):
            jenkins_home = os.environ["JENKINS_HOME"]
            destination_directory = os.path.join(jenkins_home, "userContent")
            print "Destination directory in JENKINS_HOME", destination_directory
            if not os.path.isdir(destination_directory):
                print "Directory", destination_directory, "not found"
        else:
            print "Using default destination directory '.'"
            destination_directory = "."
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    info = response.info()
    url_last_modified = time.strptime(info["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")
    print "Content last modified:", url_last_modified[:6]
    url_file_name = os.path.join(url.split("/")[-2], url.split("/")[-1])
    local_file = os.path.join(destination_directory, url_file_name)
    print "Destination file name is", local_file
    if os.path.isfile(local_file):
        file_last_modified = time.ctime(os.path.getmtime(local_file))
    else:
        file_last_modified = time.ctime(12 * 60 * 60) # Jan 1, 1970
    print "Local file last modified:", file_last_modified
    if file_last_modified < url_last_modified:
        print "Downloading ", url, "to", local_file
        local_dir, file_name = os.path.split(local_file)
        print "Destination dir", local_dir, "File name", file_name
        if not os.path.isdir(local_dir):
            os.makedirs(local_dir)
            open(local_file, "wb").write(response.read())

def bootstrap(args):
    download_url = "http://mirrors.jenkins-ci.org/war-stable-rc/latest/jenkins.war"
    if args:
        download_url = args[0]
    download_jenkins_war(download_url)

if __name__ == "__main__":
    bootstrap(sys.argv[1:])
