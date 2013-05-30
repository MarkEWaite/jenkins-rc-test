#! /usr/bin/python

# Boostrap Jenkins acceptance test execution

import os
import socket
import stat
import subprocess
import sys
import tempfile
import time
import urllib2

if os.environ.has_key("JENKINS_HOME"):
    jenkins_master_home = os.environ["JENKINS_HOME"]
else:
    jenkins_master_home = None

if os.environ.has_key("NODE_NAME"):
    jenkins_node_name = os.environ["NODE_NAME"]
else:
    jenkins_node_name = None

print "Node name is ", jenkins_node_name

def cache_jenkins_war(url, destination_directory=None):
    "Cache jenkins.war in the master node userContent directory"
    if not destination_directory:
        if jenkins_master_home:
            destination_directory = os.path.join(jenkins_master_home, "userContent", "jenkins-rc")
            print "Destination directory in JENKINS_HOME", destination_directory
            if not os.path.isdir(destination_directory):
                os.makedirs(destination_directory)
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
    return os.path.abspath(local_file)

def start_jenkins(war_file):
    "Start Jenkins server, return Jenkins process, port number, and JENKINS_HOME directory"
    jenkins_home = tempfile.mkdtemp()
    jenkins_env = { "JENKINS_HOME" : jenkins_home }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    jenkins_port = s.getsockname()[1]
    s.close()
    print "Port:", jenkins_port
    jenkins_cmd = ["java", "-jar", war_file, "--httpPort=" + str(jenkins_port)]
    p = subprocess.Popen(jenkins_cmd, env=jenkins_env)
    return p, jenkins_port, jenkins_home # Process, port number, JENKINS_HOME of started Jenkins server

def confirm_jenkins_started(p, port, timeout=None):
    "Return True if Jenkins has been started"
    return False

def rmrf(file_name):
    try:
        mode = os.lstat(file_name)[stat.ST_MODE]
        if not stat.S_ISLNK(mode) and not (mode & stat.S_IWUSR):
            os.chmod(file_name, stat.S_IWUSR)
        if stat.S_ISDIR(mode):
            for f in os.listdir(file_name):
                rmrf(os.path.join(file_name, f))
            os.rmdir(file_name)
        else:
            os.remove(file_name)
    except OSError:
        pass

def test_rmrf():
    tmp_dir = tempfile.mkdtemp()
    assert os.path.isdir(tmp_dir), tmp_dir + " not a directory"
    rmrf(tmp_dir)
    assert not os.path.isdir(tmp_dir), tmp_dir + " is a directory after rmrf"

def stop_jenkins(p, port, jenkins_home):
    "Stop Jenkins server started previously as process p on port with jenkins_home directory"
    time.sleep(15)
    assert os.path.isdir(jenkins_home), "JENKINS_HOME " + jenkins_home + " missing at entry to stop"
    p.terminate()
    rmrf(jenkins_home)
    assert not confirm_jenkins_started(p, port), "Failed to stop Jenkins"
    assert not os.path.isdir(jenkins_home), "JENKINS_HOME " + jenkins_home + " still exists at exit from stop"

def bootstrap(args):
    download_url = "http://mirrors.jenkins-ci.org/war-stable-rc/latest/jenkins.war"
    if args:
        download_url = args[0]
    war_file = cache_jenkins_war(download_url)
    p, port, jenkins_home = start_jenkins(war_file)
    print "HOME:", jenkins_home
    print "Port:", port
    print "Process:", p
    result = confirm_jenkins_started(p, port, timeout=120)
    stop_jenkins(p, port, jenkins_home)
    assert not result, "Jenkins started without an implementation"
    # assert result, "Jenkins did not start"

if __name__ == "__main__":
    test_rmrf()
    bootstrap(sys.argv[1:])
