#!/usr/bin/env python

import dns.resolver

hostname = "ring.nlnog.net"

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

answers = dns.resolver.query(hostname, 'TXT')
text = str(answers[0])
if text and len(text) > 2:
    text = text[1:-1]
servers = text.split(" ")

for server in servers:
    server_fqdn = server + ".ring.nlnog.net"
    server_a = dns.resolver.query(server_fqdn, 'A')
    server_aaaa = dns.resolver.query(server_fqdn, 'AAAA')
    server_a = str(server_a[0])
    server_aaaa = str(server_aaaa[0])
    print server_a + "\t" + server + "\t" + server_fqdn
    print server_aaaa + "\t" + server + "\t" + server_fqdn
    print ""
