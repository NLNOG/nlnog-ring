# Overview of RING hardware 

## Container07 (xs4all)

Hosted at Xs4all

### Hardware

16 cores / 48GB RAM / 173GB disk

## Network

virbr0 is bridged to eth0 (uplink)
  IPv4 address: 82.94.249.164/29
  IPv4 gateway: 82.94.249.161
  IPv6 address: 2001:888:2000:3e::1339/64
  IPv6 gateway: 2001:888:2000:3e::1
virbr1 is virtual switch on the box with this IP space:
  IPv4 prefix: 82.94.230.128/28
  IPv6 prefix: 2001:888:2001::/48

### Functions

* Xs4all01 ring node
* Lookingglass
* Staging01 ring node

## Container02

Hosted at Leaseweb

### Hardware

8 cores / 16GB RAM / 120GB disk

### Network

eth0 (uplink)
  IPv4 address: 85.17.27.45/27
  IPv4 gateway: 85.17.27.62
  IPv6 address: 2001:1AF8:4010::2/126
  IPv6 gateway: 2001:1AF8:4010::1
virbr1 is virtual switch on the box with this IP space:
  IPv4 prefix: 95.211.149.16/28
  IPv6 prefix: 2001:1AF8:4013::/48

### Functions

* Key management service
* Database
* IPv6 proxy
* Mail relay
* Wordpress website
* SQA collector

## Container06

Hosted at PCextreme

### Hardware

1 core / 32GB RAM / 223GB disk

### Network

eth0 (uplink)
  IPv4 address: 109.72.82.182/24
  IPv4 gateway: 109.72.82.3
  IPv6 address: 2a00:0f10:0103:010f::1/56
  IPv6 gateway: 2a00:0f10:0103:0100::3
virbr1 is virtual switch on the box with this IP space:
  IPv4 prefix: 109.72.93.32/28
  IPv6 prefix: 2a00:f10:122::/64

### Functions

* Backups
