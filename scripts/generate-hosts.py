#!/usr/bin/env python
# Written by Job Snijders <job@snijders-it.nl>

import sys
import dns.resolver

ringdomain = "ring.nlnog.net"

def collect_txt_record():
    answers = dns.resolver.query(ringdomain, 'TXT')
    text = str(answers[0])
    if text and len(text) > 50 and ("xlshosting01" in text) and ("intouch01" in text):
        text = text[1:-1]
    else:
        sys.exit("error: we probably didn't receive a full txt record")
    return text

record = collect_txt_record()

# print standard header that every hosts needs regardless

print """127.0.0.1   localhost

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

212.19.220.59   master01 master01.ring.nlnog.net puppet
2001:6e0:100:4001::3    master01 master01.ring.nlnog.net puppet
"""

servers = record.split(" ")

for server in servers:
    server_fqdn = server + "." + ringdomain
    for record in 'A', 'AAAA':
        server_record = dns.resolver.query(server_fqdn, record)
        server_record = str(server_record[0])
        print server_record + "\t" + server + "\t" + server_fqdn
    print
