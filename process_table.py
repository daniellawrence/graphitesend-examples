"Read the process table using the ps command, then throw the data at graphite."
#!/usr/bin/env python
import graphitesend
from collections import defaultdict
import os

def gather_ps_data():
    "Execute ps, capture all the data into a dict()"
    PS_COLS = ['size', 'rss', 'user', 'pcpu', 'pmem', 'command']
    PS_COMMAND = 'ps -eo size,rss,user:20,pcpu,pmem,command'
    PS_DATA = []

    for line in os.popen(PS_COMMAND).readlines():
        # Commands have lots of arguments, throw them away we just want
        # the executable.
        bits = line.split()[:len(PS_COLS)]
    
        # throw away the header
        if bits[0] == 'SIZE':
            continue

        # Throw away kenerl tasks
        if bits[-1].startswith('['):
            continue

        # Throw away the path, just grab the executable
        bits[-1] = bits[-1].split('/')[-1]

        # Covert the list of columns into a dict
        PS_DATA.append(dict(zip(PS_COLS, bits)))

    return PS_DATA


def percent_by(PS_DATA, group_field):
    group_data = defaultdict(lambda: defaultdict(int))
    for proc in PS_DATA:
        # Grab the key info from PS_DATA and make sure its a float.
        pmem = float(proc['pmem'])
        pcpu = float(proc['pcpu'])
        size = float(proc['size'])
        rss  = float(proc['rss'])
        # Append the key info to the running tally for 'group_field'
        group_data[proc[group_field]]['pmem']  += pmem
        group_data[proc[group_field]]['pcpu']  += pcpu
        group_data[proc[group_field]]['size']  += size
        group_data[proc[group_field]]['rss']   += rss
        group_data[proc[group_field]]['count'] += 1

    return graphitfy_group(group_data, group_field)


def graphitfy_group(group_data, group_field):
    graphite_data = {}
    for group_field_name, usage in group_data.items():
        for key, value in usage.items():
            metric = "ps.by_%s.%s.%s" % (group_field, group_field_name, key)
            graphite_data[metric] = value

    return graphite_data


def main():
    PS_DATA = gather_ps_data()
    percent_by_user = percent_by(PS_DATA, "user")
    percent_by_command = percent_by(PS_DATA, "command")
    g = graphitesend.init(dryrun=True)
    print g.send_dict(percent_by_user)

    
if __name__ == '__main__':
    main()
