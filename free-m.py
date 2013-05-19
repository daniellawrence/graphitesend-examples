#!/usr/bin/env python
import graphitesend
import os

def main():
    free_raw_data = []
    free_data = {}
    for line in os.popen('free -m').readlines():
        line = line.strip()
        bits = line.split()

        if bits[0] == 'total':
            continue

        free_raw_data.append(bits[1:])

    # Parse the first line
    free_data['mem.total'] = free_raw_data[0][0]
    free_data['mem.used'] = free_raw_data[0][1]
    free_data['mem.free'] = free_raw_data[0][2]
    free_data['mem.share'] = free_raw_data[0][3]
    free_data['mem.buffers'] = free_raw_data[0][4]
    free_data['mem.cached'] = free_raw_data[0][5]
        
    # Parse the 2nd line
    free_data['mem.used_minus_buffers'] = free_raw_data[1][1]
    free_data['mem.free_minus_buffers'] = free_raw_data[1][2]

    # Parse the 3rd line
    free_data['swap.total'] = free_raw_data[2][0]
    free_data['swap.used'] = free_raw_data[2][1]
    free_data['swap.free'] = free_raw_data[2][2]

    # Print the results
    g = graphitesend.init(dryrun=True, prefix="free")
    print g.send_dict(free_data)

if __name__ == '__main__':
    main()
