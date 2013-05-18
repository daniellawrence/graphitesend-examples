#!/usr/bin/env python
# -------------------------------------------------------------------------
# KSM a memory-saving de-duplication feature, enabled by CONFIG_KSM=y,
# added to the Linux kernel in 2.6.32.  See mm/ksm.c for its implementation,
# and http://lwn.net/Articles/306704/ and http://lwn.net/Articles/330589/

import graphitesend
import os
# Graphitesend
prefix="kernel.ksm."
dryrun=True
g = graphitesend.init(prefix=prefix, dryrun=dryrun)
# KSM
KSM_DIR='/sys/kernel/mm/ksm'
KSM_DATA={}

for ksm_file in os.listdir(KSM_DIR):
    ksm_data = open("%(KSM_DIR)s/%(ksm_file)s" % locals()).read()
    ksm_data = int(ksm_data)
    KSM_DATA[ksm_file] = ksm_data
 
results = g.send_dict(KSM_DATA)

# If we are running this as dryrun, then output the results
if dryrun:
    print results
