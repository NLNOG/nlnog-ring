#!/usr/bin/env python

import sys
import dns.resolver

ringdomain = "ring.nlnog.net"

def collect_txt_record():
    answers = dns.resolver.query(ringdomain, 'TXT')
    text = str(answers[0])
    if text and len(text) > 50 and ("xlshosting01" in text) and ("intouch01" in text):
        text = text[1:-1]
    else:
        sys.exit("error: we probably didnt receive a full txt record")
    return text
try:
    record = collect_txt_record()
except:
    sys.exit("error: something went wrong, maybe i cannot reach a resolver")

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
    server_fqdn = server + ".ring.nlnog.net"
    server_a = dns.resolver.query(server_fqdn, 'A')
    server_aaaa = dns.resolver.query(server_fqdn, 'AAAA')
    server_a = str(server_a[0])
    server_aaaa = str(server_aaaa[0])
    print server_a + "\t" + server + "\t" + server_fqdn
    print server_aaaa + "\t" + server + "\t" + server_fqdn
    print ""
