#!/usr/bin/env python
'''
Usage: $0 host
(e.g. ./find_pmtu.py example.com)

I wrote this script only as an exercise; you should use the "socket" library
in a production environment.
'''

import argparse
import subprocess

INITIAL_PACKET_SIZE = 1600 # Just for testing; 
                           # should start at 1500 for external hosts

def handle_args():
    parser = argparse.ArgumentParser(
            description='discovers the path maximum transmission unit to the host specified in the first (and only) argument')
    parser.add_argument(
            'host', type=str,
            help='a string representing the ip address or hostname of the host of interest')
    args=parser.parse_args()
    return args.host

def check_ping(size, host):
    # The following shell command was tested on this platform:  macOS Sierra (10.12.6) 
    code = subprocess.call( "ping -D -s " + str(size) + " -c 1 " + host + " >& /dev/null", shell=True)
    return code

# Rather than decermenting the mtu by 1 and testing repeatedly,
# here I'm borrowing from the comparison sort algorithm:
# https://en.wikipedia.org/wiki/Comparison_sort
def find_mtu(host):
    upper_bound = INITIAL_PACKET_SIZE
    packet_size = INITIAL_PACKET_SIZE
    lower_bound = 1
    count = 0
    diff = upper_bound - lower_bound
    while (diff <> 1):
        exit_code = check_ping(packet_size, host)

        if (exit_code <> 0) and (exit_code <> 2): # 0 => received at least one reply; 2 => transmission was successful but no reply
            print "ping exit code: {}".format(exit_code)
            print "An error occurred.  These values are defined in <sysexits.h>."
            print "Is your host resolvable?"
            exit()

        if (count == 0):
            print "IP MTU\t\tPing exit code"
            print "======\t\t=============="

        print str(packet_size) + "\t\t" +  str(exit_code)
        if (exit_code <> 0):
            upper_bound = packet_size
        else:
            if (count == 0):
                print "pmtu is at least {}, try increasing INITIAL_PACKET_SIZE from {} to {}" \
                    .format(str(INITIAL_PACKET_SIZE), str(INITIAL_PACKET_SIZE), str(INITIAL_PACKET_SIZE + 100))
                exit()

            lower_bound = packet_size

        packet_size = (upper_bound + lower_bound) / 2
        diff = upper_bound - lower_bound
        count += 1
    
    return packet_size, count

def print_results(host, mtu, count):
    print
    print "IP MTU to {}: {}".format(host, mtu)
    print "Discovered mtu in {} attempted packets".format(str(count))

def main():
    host = handle_args()
    mtu, count = find_mtu(host)
    print_results(host, mtu, count)

main()
