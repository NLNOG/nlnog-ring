These steps are required to add a machine to the ring

# Add machine to the database

On `dbmaster.infra.ring.nlnog.net`:

```
ring-admin add machine $username $hostname $asnumber $countrycode $geo "$datacenter" $v6address [$v4address] [$statecode]
```

# Update DNS

On `ns01.infra.ring.nlnog.net`, ensure $org.ring.nlnog.net is a CNAME towards the fqdn of the node:

```
ring-pdns add node <node>
```

# Create ansible configuration

On `dbmaster.infra.ring.nlnog.net` (note: requires ssh-agent forwarding):

```
ring-admin ansible deploy
```

# Provision the host

On any host that has ring admin SSH-keys, from the `ring-ansible` repository:

```
git pull
ansible-playbook -c ssh --vault-password-file=open-the-vault.sh -i nodes -l $machine -u $initial_user -k -K provision.yml
```

**note**: `-k -K` is required to specify the logon and sudo password

The playbook will upgrade and reboot the machine

# Clean up

On the new machine:

```
passwd --delete root
deluser --remove-home <provisioning_user>
```

Check if the machine has additional autoconf IPv6 addresses and remove them (netplan: `accept-ra: false`)

# Set the node to active

On `dbmaster.infra.ring.nlnog.net`:

```
ring-admin activate machine <node>
```

On `ns01.infra.ring.nlnog.net`:

```
ring-pdns activate node <node>
```

