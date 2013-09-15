#!/usr/bin/env python
# example:
#./ping_times.py www.google.com
#systems.lintendo.ping_times.www_google_com.max_ms 6.235000 1379207320
#systems.lintendo.ping_times.www_google_com.avg_ms 6.235000 1379207320
#systems.lintendo.ping_times.www_google_com.mdev_ms 0.000000 1379207320
#systems.lintendo.ping_times.www_google_com.min_ms 6.235000 1379207320

import graphitesend
import os
import sys

stats = os.popen('ping -c 1 %s' % sys.argv[1]).readlines()[-1]

safe_hostname = sys.argv[1].replace('.','_')
(ping_min, ping_avg, ping_max, ping_mdev) = stats.split('=')[-1].strip().strip(' ms').split('/')

g = graphitesend.init(group='ping_times.%s.' % safe_hostname, suffix='_ms', dryrun=True)
print g.send_dict({
    'min': ping_min,
    'max': ping_max,
    'avg': ping_avg,
    'mdev': ping_mdev
})


