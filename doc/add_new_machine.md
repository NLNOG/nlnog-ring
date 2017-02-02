These steps are required to add a machine to the ring

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
git pull
ansible-playbook -c ssh --vault-password-file=open-the-vault.sh -i nodes -l $machine -u $initial_user -k -K provision.yml
```

**note**: `-k -K` is required to specify the logon and sudo password

# Reboot and clean up

```
reboot
passwd --delete root
deluser --remove-home <provisioning_user>
```

# Set the node to active

ring-admin activate machine <node>
ring-pdns activate node <node>

