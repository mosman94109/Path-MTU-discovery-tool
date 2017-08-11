Usage: $0 host
(e.g. ./find_pmtu.py example.com)
help: $0 --help

I wrote this script only as an exercise; you should use the "socket" library
in a production environment.

Rather than decermenting the mtu by 1 and testing repeatedly,
in this script I borrowed from the comparison sort algorithm:
https://en.wikipedia.org/wiki/Comparison_sort
