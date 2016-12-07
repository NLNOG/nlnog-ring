These steps are required to add a machine to the ring

# Check that the host has working ipv4 and ipv6 connectivity

check if cpu is 64 bit - if not please report to the owner of the machine that we do not support 32 bit machines in the ring
lscpu

# Add machine to the database

on `master01.infra.ring.nlnog.net`:

```
ring-admin add machine $username $hostname $asnumber $countrycode $geo "$datacenter" $v4address $v6address [$statecode]
```

# Update DNS

Ensure $org.ring.nlnog.net is a CNAME towards the fqdn of the node, on `ns01.infra.ring.nlnog.net`:

```
ring-pdns add node <node>
```

# Create ansible configuration

on `dbmaster01` (note: requires ssh-agent forwarding):

```
ring-admin ansible deploy
```

# Provision the host

From the `ring-ansible` repository:

```
ansible-playbook --vault-password-file=open-the-vault.sh -i nodes -l $machine -u $initial_user -k -K provision.yml
```

**note**: `-k -K` is required to specify the logon and sudo password

# Add the hostkey of the new node to the databae

on `dbmaster01`:

```
cat <file with hostkey> | ring-admin add hostkey <node>
```

# Set the node to active

ring-admin activate machine <node>
ring-pdns activate node <node>
