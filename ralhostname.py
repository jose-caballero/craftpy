#!/usr/bin/env python

import re
import sys
import socket

from craftpy.shell import run


# ============================================================================== 
#  Lists of Grid Services hostnames 
# ============================================================================== 

ce = ['arc-ce01.gridpp.rl.ac.uk',
      'arc-ce02.gridpp.rl.ac.uk',
      'arc-ce03.gridpp.rl.ac.uk',
      'arc-ce04.gridpp.rl.ac.uk',
      'arc-ce05.gridpp.rl.ac.uk']
central_manager = ['htcondor-cm01.gridpp.rl.ac.uk',
                   'htcondor-cm02.gridpp.rl.ac.uk']
squid = ['squid01.gridpp.rl.ac.uk',
         'squid02.gridpp.rl.ac.uk',
         'squid03.gridpp.rl.ac.uk',
         'squid04.gridpp.rl.ac.uk',
         'squid05.gridpp.rl.ac.uk',
         'squid06.gridpp.rl.ac.uk']
ui = ['lcgui05.gridpp.rl.ac.uk',
      'lcgui05.gridpp.rl.ac.uk']
fts = ['lcgfts01.gridpp.rl.ac.uk',
       'lcgfts02.gridpp.rl.ac.uk',
       'lcgfts05.gridpp.rl.ac.uk',
       'lcgfts06.gridpp.rl.ac.uk',
       'lcgfts07.gridpp.rl.ac.uk',
       'lcgfts08.gridpp.rl.ac.uk',
       'lcgfts09.gridpp.rl.ac.uk',
       'lcgfts10.gridpp.rl.ac.uk']
fts_egi = ['ftsegi01.scd.rl.ac.uk',
           'ftsegi02.scd.rl.ac.uk',
           'ftsegi03.scd.rl.ac.uk']
cvmfs_stratum1 = ['stratum01.gridpp.rl.ac.uk',
                  'stratum02.gridpp.rl.ac.uk' ]
cvmfs_stratum0 = ['cvmfs-release01.gridpp.rl.ac.uk',
                   'cvmfs-uploader02.gridpp.rl.ac.uk',
                   'cvmfs-uploader-iris.gridpp.rl.ac.uk']
site_argus = ['lcgargus01.gridpp.rl.ac.uk',
              'lcgargus02.gridpp.rl.ac.uk']
ngi_argus = ['ngi-argus01.gridpp.rl.ac.uk',
             'ngi-argus02.gridpp.rl.ac.uk']
top_bdii = ['lcgbdii01.gridpp.rl.ac.uk',
            'lcgbdii02.gridpp.rl.ac.uk',
            'lcgbdii03.gridpp.rl.ac.uk']
site_bdii = ['lcgsbdii01.gridpp.rl.ac.uk',
             'lcgsbdii02.gridpp.rl.ac.uk',
             'lcgsbdii03.gridpp.rl.ac.uk']
vo_box = ['lcgvo-alice-1.gridpp.rl.ac.uk',
          'lcgvo-lhcb-1.gridpp.rl.ac.uk']

ce_test = ['arc-ce-test01.gridpp.rl.ac.uk',
           'arc-ce-test02.gridpp.rl.ac.uk', ]
central_manager_test = ['condor01.gridpp.rl.ac.uk',
                        'condor02.gridpp.rl.ac.uk']
fts_test = ['fts-test01.gridpp.rl.ac.uk',
            'fts-test02.gridpp.rl.ac.uk',
            'fts-test03.gridpp.rl.ac.uk',
            'fts-test04.gridpp.rl.ac.uk',
            'fts-test05.gridpp.rl.ac.uk',
            'fts-test06.gridpp.rl.ac.uk',
            'fts-test07.gridpp.rl.ac.uk',
            'fts-test08.gridpp.rl.ac.uk']

batch_farm = ce + central_manager
cvmfs = cvmfs_stratum0 + cvmfs_stratum1
bdii = top_bdii + site_bdii
argus = site_argus + ngi_argus
fts = fts + fts_egi
grid_services = batch_farm + squid + cvmfs + bdii + argus + fts + ui + vo_box
batch_farm_test = ce_test + central_manager_test

# ============================================================================== 
#   Code to convert short strings into real hostnames
# ============================================================================== 

class Hostname(object):
    def __init__(self, hostname):
        self.hostname = hostname

    def complete(self):
        if self._matches_domain():
            return  
        if self._match_mapping():
            return
        if self._matches_four_digits():
            return
        if self._matches_ip():
            return 
        if self._matches_open_stack_format():
            return
        if self._matches_no_dots():
            return

    def _matches_domain(self):
        return self.hostname.endswith(".ac.uk")

    def _match_mapping(self):
        mapping = {'ui05': 'lcgui05.gridpp.rl.ac.uk',
                   'ui06': 'lcgui06.gridpp.rl.ac.uk',
                   'ce01': 'arc-ce01.gridpp.rl.ac.uk',
                   'ce02': 'arc-ce02.gridpp.rl.ac.uk',
                   'ce03': 'arc-ce03.gridpp.rl.ac.uk',
                   'ce04': 'arc-ce04.gridpp.rl.ac.uk',
                   'ce05': 'arc-ce05.gridpp.rl.ac.uk',
                   'ce-test01': 'arc-ce-test01.gridpp.rl.ac.uk',
                   'ce-test02': 'arc-ce-test02.gridpp.rl.ac.uk',
                   'cm01': 'htcondor-cm01.gridpp.rl.ac.uk',
                   'cm02': 'htcondor-cm02.gridpp.rl.ac.uk',
                   'acc-1': 'accounting-1.gridpp.rl.ac.uk',
                   'sq01': 'squid01.gridpp.rl.ac.uk',
                   'sq02': 'squid02.gridpp.rl.ac.uk',
                   'sq03': 'squid03.gridpp.rl.ac.uk',
                   'sq04': 'squid04.gridpp.rl.ac.uk',
                   'sq05': 'squid05.gridpp.rl.ac.uk',
                   'sq06': 'squid06.gridpp.rl.ac.uk',
                   'uploader': 'cvmfs-uploader02.gridpp.rl.ac.uk',
                   'uplaoder': 'cvmfs-uploader02.gridpp.rl.ac.uk',
                   'uploader-iris': 'cvmfs-uploader-iris.gridpp.rl.ac.uk',
                   'release': 'cvmfs-release01.gridpp.rl.ac.uk',
                   'st01': 'stratum01.gridpp.rl.ac.uk',
                   'st02': 'stratum02.gridpp.rl.ac.uk',
                   'st1-01': 'cvmfs-stratum1-01.gridpp.rl.ac.uk',
                   'st1-02': 'cvmfs-stratum1-02.gridpp.rl.ac.uk',
                   'logstash01': 'logstash-ingestor01.gridpp.rl.ac.uk',
                   'logstash02': 'logstash-ingestor02.gridpp.rl.ac.uk', 
                   'vobox-alice': 'lcgvo-alice-1.gridpp.rl.ac.uk',
                   'vobox-lhcb': 'lcgvo-lhcb-1.gridpp.rl.ac.uk',
                   'vobox-lsst': 'lcgvo-lsst-1.gridpp.rl.ac.uk',
                   'wn': 'lcg2400.gridpp.rl.ac.uk',
                   'influx06': 'influxdb06.gridpp.rl.ac.uk',
                   'bdii01': 'lcgbdii01.gridpp.rl.ac.uk',
                   'bdii02': 'lcgbdii02.gridpp.rl.ac.uk',
                   'bdii03': 'lcgbdii03.gridpp.rl.ac.uk',
                   'sbdii01': 'lcgsbdii01.gridpp.rl.ac.uk',
                   'sbdii02': 'lcgsbdii02.gridpp.rl.ac.uk',
                   'sbdii03': 'lcgsbdii03.gridpp.rl.ac.uk',
                  }
        candidate = mapping.get(self.hostname, None)
        if candidate:
            self.hostname = candidate
            return True
        else:
            return False
    
    def _matches_four_digits(self):
        """
        check if hostname is like "1234"
        """
        p = re.compile("^\d{4}$")
        if p.match(self.hostname):
            self.hostname = 'lcg%s.gridpp.rl.ac.uk' %self.hostname
            return True
        else:
            return False
    
    def _matches_ip(self):
        """
        check if hostname is like "123.123.123.123"
        """
        p = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        if p.match(self.hostname):
            self.hostname = socket.getfqdn(self.hostname)
            if self.hostname.endswith('gridpp.rl.ac.uk') or\
               self.hostname.endswith('nubes.stfc.ac.uk'):
                pass
            else:
                self.hostname = ""  
            return True
        else:
            return False
    
    def _matches_open_stack_format(self):
        """
        check if hostname is like "host-123-123-123-123"
        """
        p = re.compile("^host-\d{1,3}\-\d{1,3}\-\d{1,3}\-\d{1,3}$")
        if p.match(self.hostname):
            self.hostname = '%s.nubes.stfc.ac.uk' %self.hostname
            return True
        else:
            return False
    
    def _matches_no_dots(self):
        if self.hostname.find(".") == -1:
            domain_names = [
                'gridpp.rl.ac.uk',
                'scd.rl.ac.uk',
                'fds.rl.ac.uk',
                'nubes.rl.ac.uk',
            ]
            for domain in domain_names:
                _hostname = '%s.%s' %(self.hostname, domain)
                if self._check_nslookup(_hostname):
                    self.hostname = _hostname
                    return True
            else:
                return False
        else:
            return False

    def _check_nslookup(self, hostname):
        cmd = 'nslookup %s' %hostname
        r = run(cmd)
        return r.rc == 0


class HostnameList(object):
    def __init__(self):
        self.hostname_l = []

    def add(self, hostname):
        if isinstance(hostname, list):
            self.hostname_l += hostname
        else:
            self.hostname_l.append(hostname)

    def load(self, filename):
        """
        get the list of hostnames from a file
        """
        f = open(filename)
        for line in f.readlines():
            line = line.strip()
            if line == '':
                continue
            if line.startswith('#'):
                continue
            self.hostname_l.append(line)

    def complete(self):
        out = []
        for i in self.hostname_l:
            out.append( completehostname(i) )
        return out


def completehostname(hostname):
    host = Hostname(hostname)
    host.complete()
    return host.hostname


def completehostname_l(hostname_l):
    out = []
    for hostname in hostname_l:
        hostname = completehostname(hostname)
        out.append(hostname)
    return out

