#!/usr/bin/env python
import graphitesend
import os


cols = ['filesystem', 'size', 'used', 'avail', 'pused', 'mountpoint']

FS_DATA = []

for line in os.popen('df -k').readlines():
    line = line.strip()
    if line.startswith('Filesystem'):
        continue

    bits = line.split()
    single_fs = dict(zip(cols, bits))
    # Generate graphite-friendly names 
    single_fs['gfilesystem'] = single_fs['filesystem'].replace('/', '_')
    single_fs['gmountpoint'] = single_fs['mountpoint'].replace('/', '_')
    # Remove the '%' frpm pused
    single_fs['pused'] = single_fs['pused'].replace('%', '')
    
    FS_DATA.append(single_fs)

graphite_fs = {}
for fs in FS_DATA:
    graphite_fs["%s.size" % fs['gmountpoint']] = fs['size']
    graphite_fs["%s.used" % fs['gmountpoint']] = fs['used']
    graphite_fs["%s.avail" % fs['gmountpoint']] = fs['avail']
    graphite_fs["%s.pused" % fs['gmountpoint']] = fs['pused']
    
g = graphitesend.init(prefix='filesystem', dryrun=True)
print g.send_dict(graphite_fs)
