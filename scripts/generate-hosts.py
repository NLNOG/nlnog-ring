#!/usr/bin/env python3
# Written by Job Snijders <job@snijders-it.nl>

import sys
import dns.resolver

ringdomain = "ring.nlnog.net"
hosts = []
all_hosts = []

for answers in dns.resolver.query(ringdomain, 'TXT',):
    hosts.append(answers.to_text()[1:-1].split(' '))
all_hosts = sum(hosts, [])

# print standard header that every hosts needs regardless

print("""127.0.0.1   localhost

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

78.152.42.69 master01 master01.infra..ring.nlnog.net puppet
2a02:d28:666::69    master01 master01.infra.ring.nlnog.net puppet

""")

for server in all_hosts:
    server_fqdn = server + "." + ringdomain
    for record in 'A', 'AAAA':
        try:
            server_record = dns.resolver.query(server_fqdn, record)
            server_record = str(server_record[0])
            print(server_record + "\t" + server + "\t" + server_fqdn)
        except Exception as e:
            sys.stderr.write("{} record not found for {}: {}\n".format(record,server_fqdn,str(e)))
    print
