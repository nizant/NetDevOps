# Juniper Switch Configuration Playbook

An Ansible playbook for configuring Juniper EX/QFX switches via NETCONF.

## What Gets Configured

| Section              | Details                                                      |
|----------------------|--------------------------------------------------------------|
| **System**           | Hostname, domain, DNS, timezone                              |
| **NTP**              | NTP servers with optional prefer flag                        |
| **Syslog**           | Remote syslog servers and local log files                    |
| **Banner**           | MOTD login banner                                            |
| **SNMP**             | Location, contact, communities                               |
| **Users**            | Local accounts with class, password, and SSH key support     |
| **VLANs**            | VLAN creation with optional L3 IRB interfaces                |
| **Access Ports**     | Access-mode interfaces with VLAN assignment                  |
| **Trunk Ports**      | Trunk-mode interfaces with allowed VLANs and native VLAN     |
| **L3 Interfaces**    | IRB interfaces with IPv4 addresses (VLAN gateways)           |
| **Static Routes**    | Default gateway and any additional static routes             |
| **OSPF** (optional)  | OSPF area, interfaces, passive interfaces                    |
| **Security**         | SSH hardening, login retry limits, console auto-logout       |
| **Backup**           | Config backup before any changes                             |
| **Commit Confirm**   | Safe commit with 5-minute auto-rollback                      |

## Prerequisites

1. **NETCONF** must be enabled on the Juniper switch:
   ```
   set system services netconf ssh
   ```
2. **Ansible** with the `junipernetworks.junos` collection:
   ```bash
   ansible-galaxy collection install junipernetworks.junos
   ```
3. **SSH access** to the switch from the control node.

## Directory Structure

```
juniper-switch-playbook/
├── ansible.cfg
├── inventory                  # Switch inventory
├── playbook.yml               # Main playbook
├── group_vars/
│   └── junos_switches.yml     # Shared config for all switches
├── host_vars/
│   └── switch01.yml           # Per-switch overrides
├── templates/
│   └── banner.j2              # Banner template
├── backups/                   # Created automatically
└── README.md
```

## Quick Start

### 1. Edit the inventory

Uncomment and set the IP addresses of your switches:

```ini
[junos_switches]
switch01 ansible_host=192.168.1.10
switch02 ansible_host=192.168.1.11
```

### 2. Customize variables

Edit `group_vars/junos_switches.yml` to match your network:
- VLANs and IP addressing
- Interface assignments
- SNMP communities
- User accounts and passwords
- Static routes or OSPF settings

For per-switch overrides (e.g., different IP addresses), edit files in `host_vars/`.

### 3. Generate password hashes

```bash
openssl passwd -6 'YourPassword'
```

Paste the hash into the `password` field in `group_vars/junos_switches.yml`.

### 4. Run the playbook

```bash
cd juniper-switch-playbook
ansible-playbook playbook.yml --ask-pass
```

Or with an SSH key:
```bash
ansible-playbook playbook.yml
```

### 5. Target a single switch

```bash
ansible-playbook playbook.yml --limit switch01
```

### 6. Dry run (check mode)

```bash
ansible-playbook playbook.yml --check --diff
```

## Safety Features

- **Configuration backup** is taken before any changes are made
- **Commit confirm** with a 5-minute window — if something goes wrong and you lose connectivity, the switch automatically rolls back
- **Check mode** support for dry runs

## Enabling OSPF

OSPF is disabled by default. To enable it, set `enable_ospf: true` in `group_vars/junos_switches.yml` and configure the `ospf_*` variables.

## Notes

- This playbook uses **NETCONF** (port 830) as the connection method, which is the recommended approach for Juniper devices.
- If your switches don't have NETCONF enabled yet, enable it manually first: `set system services netconf ssh` and commit.
- The playbook is designed for **Juniper EX and QFX** series switches but should work with any Junos device.
