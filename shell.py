#!/usr/bin/env python

import subprocess

from craftpy.bcolors import bcolors

class Results(object):
    def __init__(self, cmd, out, err, rc):
        self.cmd = cmd
        self.out = out
        self.err = err
        self.rc = rc

    def __str__(self):
        """
        Human friendly display of results
        """
        out_l = self.out.split('\n')
        err_l = self.err.split('\n')
        if self.rc == 0:
            out = bcolors.WARNING + 'cmd:    ' + bcolors.ENDC + self.cmd
            out += '\n' + bcolors.WARNING + 'stdout: ' + bcolors.ENDC + out_l[0]
            for l in out_l[1:]:
                out += '\n' + bcolors.WARNING + '        ' + bcolors.ENDC + l
            out += '\n' + bcolors.WARNING + 'stderr: ' + bcolors.ENDC + err_l[0]
            for l in err_l[1:]:
                out += '\n' + bcolors.WARNING + '        ' + bcolors.ENDC + l
            out += '\n' + bcolors.WARNING + 'rc:     ' + bcolors.ENDC + str(self.rc)
        else: 
            out = bcolors.FAIL + "ERROR:\n"
            out += '\n' + 'cmd:    ' + self.cmd
            out += '\n' + 'stdout: ' + out_l[0]
            for l in out_l[1:]:
                out += '\n' + '        ' + l 
            out += '\n' + 'stderr: ' + err_l[0]
            for l in err_l[1:]:
                out += '\n' + '        ' + l 
            out += '\n' + 'rc:     ' + str(self.rc)
            out += '\n' + bcolors.ENDC
        return out

    @property
    def succeeded(self):
        return self.rc == 0

    @property 
    def failed(self):
        return self.rc != 0

def run(cmd, stdin=None):
    try:
        # python 3
        subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    except:
        # python 2
        subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = subproc.communicate(input=stdin)
    st = subproc.returncode
    results = Results(cmd, out.strip(), err.strip(), st)
    return results


def remote_run(cmd, host, user='root'):
    cmd = "ssh -oStrictHostKeyChecking=no -oCheckHostIP=no %s@%s '%s'" %(user, host, cmd)
    return run(cmd)


def call(cmd):
    subprocess.call(cmd, shell=True)


def scpto(source_dir='./', source='*', user='root', dest_host='', dest_dir='/tmp/'):
    """
    copy, with scp, one or more files from localhost to a remote host
    """
    # FIXME
    if not dest_host:
        # abort
        return None
    cmd = 'scp %s/%s %s@%s:%s' %(source_dir, source, user, dest_host, dest_dir)
    results = run(cmd)
    return results


def scpfrom(user='root', source_host='', source_dir='/tmp/', source='*', dest_dir='/tmp/'):
    """
    copy, with scp, one or more files from a remote host to localhost
    """
    # FIXME
    if not source_host:
        # abort
        return None
    cmd = 'scp %s@%s:%s/%s %s' %(user, source_host, source_dir, source, dest_dir)
    results = run(cmd)
    return results


def test_ping(hostname):
    """
    code to test if a given host responds to ping 
    """
    cmd = 'ping -c 1 %s' %hostname
    results = run(cmd)
    return results.rc == 0


def test_ssh(hostname):
    """
    code to test if a given host is accessible via ssh
    """
    cmd = 'ssh -o ConnectTimeout=1 root@%s "exit"' %hostname
    results = run(cmd)
    return results.rc == 0

