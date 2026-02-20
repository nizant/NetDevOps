# Network Automation Toolkit — Documentation

> **Authors:** Our Network Engineering Team  
> **Platform:** Windows 11 + WSL 2 (Ubuntu 24.04)  
> **Last Updated:** 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture & Workflow](#architecture--workflow)
3. [Phase 1 — Enabling WSL on Windows](#phase-1--enabling-wsl-on-windows)
4. [Phase 2 — Installing Ansible](#phase-2--installing-ansible)
5. [Phase 3 — Dev Environment Setup Playbook](#phase-3--dev-environment-setup-playbook)
6. [Phase 4 — Juniper Switch Configuration Playbook](#phase-4--juniper-switch-configuration-playbook)
7. [Ansible Variable Precedence (How It Works)](#ansible-variable-precedence-how-it-works)
8. [Complete File Reference](#complete-file-reference)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## Overview

This repository contains our end-to-end toolkit for setting up a **network automation development environment** from scratch on a Windows machine. We built everything in a layered approach — starting from enabling WSL, installing Ansible, provisioning our dev tools, and finally deploying production-ready playbooks that configure Juniper network switches.

Our toolkit is composed of **four phases**, each building on the previous one:

| Phase | Component | Purpose |
|-------|-----------|---------|
| 1 | `enable-wsl.ps1` | Enables WSL 2 on Windows 11 |
| 2 | `install-ansible.sh` | Installs Ansible inside WSL Ubuntu 24.04 |
| 3 | `dev-setup-playbook/` | Provisions our full network automation dev environment |
| 4 | `juniper-switch-playbook/` | Configures Juniper EX/QFX switches via NETCONF |

---

## Architecture & Workflow

Here is how our entire workflow fits together, from a fresh Windows machine to managing live Juniper switches:

```
┌─────────────────────────────────────────────────────────────────┐
│                        WINDOWS 11 HOST                         │
│                                                                 │
│   Step 1: Run enable-wsl.ps1 (as Administrator)                │
│           → Enables WSL 2 + Virtual Machine Platform            │
│           → Installs Ubuntu 24.04                               │
│           → Reboot                                              │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                  WSL 2 — UBUNTU 24.04                   │   │
│   │                                                         │   │
│   │   Step 2: Run install-ansible.sh                        │   │
│   │           → Adds Ansible PPA                            │   │
│   │           → Installs Ansible                            │   │
│   │                                                         │   │
│   │   Step 3: Run dev-setup-playbook                        │   │
│   │           → Installs system packages (git, nmap, etc.)  │   │
│   │           → Creates Python venv with networking libs    │   │
│   │           → Installs Ansible Galaxy collections         │   │
│   │           → Configures SSH, Git, project structure      │   │
│   │                                                         │   │
│   │   Step 4: Run juniper-switch-playbook                   │   │
│   │           → Connects to Juniper switches via NETCONF    │   │
│   │           → Pushes full configuration                   │   │
│   │                                                         │   │
│   │           ┌──────────┐  ┌──────────┐  ┌──────────┐     │   │
│   │           │ Switch01 │  │ Switch02 │  │ Switch03 │     │   │
│   │           │ (Junos)  │  │ (Junos)  │  │ (Junos)  │     │   │
│   │           └──────────┘  └──────────┘  └──────────┘     │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Enabling WSL on Windows

### File: `enable-wsl.ps1`

### What We Built

We created a PowerShell script that automates the entire process of enabling Windows Subsystem for Linux (WSL 2) on a Windows 11 machine. Without this script, we would need to manually enable multiple Windows features, update WSL, and install a Linux distribution — all as separate steps.

### How It Works

The script performs five actions in sequence:

1. **Windows version check** — We first verify the machine is running Windows 11 (build 22000+). If it detects an older build, it warns us but allows us to continue if we choose.

2. **Enable WSL feature** — We use `dism.exe` to enable the `Microsoft-Windows-Subsystem-Linux` Windows feature. This is the core kernel component that allows Linux binaries to run on Windows.

3. **Enable Virtual Machine Platform** — We enable the `VirtualMachinePlatform` feature, which is required for WSL 2. Unlike WSL 1 (which used a translation layer), WSL 2 runs a real Linux kernel inside a lightweight virtual machine, giving us full system call compatibility.

4. **Set WSL 2 as default** — We run `wsl --set-default-version 2` so any future distro installations use WSL 2 rather than WSL 1.

5. **Install Ubuntu** — By default, we install the Ubuntu distribution. We can skip this step with the `-SkipDistroInstall` flag, or choose a different distro with `-Distro <name>`.

### How to Run It

```powershell
# Must be run as Administrator
.\enable-wsl.ps1

# Or with options:
.\enable-wsl.ps1 -SkipDistroInstall
.\enable-wsl.ps1 -Distro "Debian"
```

After running, we **must reboot** for the Windows features to take effect. The script offers to restart the computer automatically.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `-SkipDistroInstall` | Switch | `false` | Skips installing a Linux distribution |
| `-Distro` | String | `"Ubuntu"` | Which distribution to install |

---

## Phase 2 — Installing Ansible

### File: `install-ansible.sh`

### What We Built

We created a Bash script that installs Ansible on our WSL Ubuntu 24.04 system using the **official Ansible PPA** (Personal Package Archive). This ensures we get the latest stable version of Ansible, rather than the potentially outdated version in Ubuntu's default repositories.

### How It Works

The script follows a four-step process:

1. **OS verification** — We read `/etc/os-release` to confirm we're running Ubuntu 24.04. If we're on a different OS, the script warns us but lets us proceed if we accept the risk.

2. **Update package index** — We run `sudo apt update` to refresh the list of available packages. This ensures we don't install stale versions.

3. **Install prerequisites & add PPA** — We install `software-properties-common` (which provides the `add-apt-repository` command), then add the official `ppa:ansible/ansible` repository. This PPA is maintained by the Ansible team and always has the latest release.

4. **Install Ansible** — We install Ansible via `apt` and print the installed version to confirm success.

### How to Run It

From inside our WSL Ubuntu terminal:

```bash
# Option A: Copy from Windows and run
cp /mnt/c/Users/Nish/workspace/install-ansible.sh ~/
chmod +x ~/install-ansible.sh
~/install-ansible.sh

# Option B: Run directly from the Windows mount
bash /mnt/c/Users/Nish/workspace/install-ansible.sh
```

### Why We Use the PPA Instead of pip

We chose the PPA method over `pip install ansible` for several reasons:
- It integrates with our system package manager (`apt`), so updates come through `apt upgrade`
- It handles all dependencies automatically
- It's the officially recommended method for Ubuntu systems
- We avoid polluting our system Python with global pip packages

---

## Phase 3 — Dev Environment Setup Playbook

### Directory: `dev-setup-playbook/`

### What We Built

We created an Ansible playbook that transforms our bare WSL Ubuntu installation into a fully-equipped **network automation development environment**. Instead of manually installing dozens of packages and tools, we codified everything into a repeatable, idempotent playbook.

### Directory Structure

```
dev-setup-playbook/
├── inventory           # Defines localhost as our target
├── playbook.yml        # Main playbook with all tasks
├── vars/
│   └── main.yml        # All customizable variables
└── README.md           # Quick reference guide
```

### How It Works — Task by Task

Our playbook runs against `localhost` (our own WSL machine) and performs the following:

#### 1. System Packages

We install a comprehensive set of system tools that we need for network automation work:

| Category | Packages |
|----------|----------|
| **General utilities** | git, vim, curl, wget, tree, jq |
| **SSH & connectivity** | openssh-client, sshpass, telnet |
| **SNMP tools** | snmp, snmp-mibs-downloader, libsnmp-dev |
| **Network diagnostics** | iputils-ping, traceroute, nmap |
| **File transfer** | tftpd-hpa |
| **Python & build tools** | python3, python3-pip, python3-venv, python3-dev, build-essential, libffi-dev, libssl-dev |

We also enable the Ubuntu multiverse repository (required for `snmp-mibs-downloader`) and uncomment the MIB loading line in `/etc/snmp/snmp.conf` so that SNMP tools can translate OIDs to human-readable names.

#### 2. Project Directory Structure

We create an organized project layout at `~/network-automation/`:

```
~/network-automation/
├── playbooks/       # Our Ansible playbooks
├── inventories/     # Device inventory files
├── roles/           # Reusable Ansible roles
├── templates/       # Jinja2 configuration templates
├── group_vars/      # Group-level variables
├── host_vars/       # Per-device variables
├── backups/         # Device configuration backups
├── scripts/         # Custom Python/Bash scripts
└── venv/            # Python virtual environment
```

#### 3. Python Virtual Environment & Libraries

We create an isolated Python virtual environment and install networking libraries into it. This keeps our system Python clean and lets us manage library versions independently.

**Libraries we install:**

| Library | Purpose |
|---------|---------|
| **netmiko** | SSH connections to network devices (multi-vendor) |
| **napalm** | Unified API for network device configuration |
| **nornir** + plugins | Concurrent automation framework for network devices |
| **paramiko** | Low-level SSH protocol library |
| **scrapli** | Fast, modern SSH/NETCONF client for network devices |
| **textfsm** + **ntc-templates** | Structured parsing of CLI output |
| **pysnmp** | SNMP queries from Python |
| **pyats** + **genie** | Cisco's test automation framework (works with other vendors too) |
| **jinja2** | Template engine for generating configs |
| **pyyaml** | YAML parsing for inventory/variable files |
| **xmltodict** | XML parsing (useful for NETCONF responses) |
| **rich** | Beautiful terminal output formatting |

#### 4. Ansible Galaxy Collections

We install the Ansible collections we need for managing network devices from multiple vendors:

| Collection | Vendor/Purpose |
|------------|----------------|
| `cisco.ios` | Cisco IOS devices |
| `cisco.iosxr` | Cisco IOS-XR devices |
| `cisco.nxos` | Cisco Nexus (NX-OS) devices |
| `cisco.asa` | Cisco ASA firewalls |
| `arista.eos` | Arista switches |
| `junipernetworks.junos` | Juniper Junos devices |
| `ansible.netcommon` | Common networking modules (cli, netconf, etc.) |
| `ansible.utils` | Utility filters and plugins |

#### 5. SSH Configuration

We create an `~/.ssh/config` file tailored for network devices. Older network equipment often uses legacy SSH algorithms that modern SSH clients reject by default, so we explicitly enable them for private IP ranges:

- **Legacy key exchange:** `diffie-hellman-group14-sha1`, `diffie-hellman-group1-sha1`
- **Legacy host key algorithms:** `ssh-rsa`
- **Legacy ciphers:** `aes128-cbc`, `aes256-cbc`, `3des-cbc`
- **Host key checking disabled** for private IP ranges (network devices change keys frequently during reprovisioning)

#### 6. Git Configuration

We set up Git with our team's name and email so our playbook changes are properly attributed in version control.

#### 7. Shell Aliases

We add two convenience aliases to `~/.bashrc`:
- `netenv` — activates our Python virtual environment
- `netdir` — navigates to our project directory

#### 8. Starter Files

We generate a starter `ansible.cfg` and a template inventory file inside the project directory, so we can begin writing playbooks immediately.

### How to Run It

```bash
# Copy to WSL
cp -r /mnt/c/Users/Nish/workspace/dev-setup-playbook ~/dev-setup-playbook
cd ~/dev-setup-playbook

# Customize variables (optional but recommended)
vim vars/main.yml    # Set git name/email, adjust packages

# Run the playbook
ansible-playbook -i inventory playbook.yml --ask-become-pass
```

### Key Variables We Can Customize

All variables live in `vars/main.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `venv_path` | `~/network-automation/venv` | Where the Python venv is created |
| `project_base` | `~/network-automation` | Root of our project directory |
| `system_packages` | *(see above)* | List of apt packages to install |
| `python_packages` | *(see above)* | List of pip packages for the venv |
| `ansible_collections` | *(see above)* | List of Galaxy collections to install |
| `git_user_name` | `"Network Admin"` | Git commit author name |
| `git_user_email` | `"admin@example.com"` | Git commit author email |
| `ssh_config_entries` | *(legacy SSH settings)* | SSH client configuration |

### The Inventory File

Our inventory is simple — we target only `localhost` with a local connection:

```ini
[local]
localhost ansible_connection=local
```

This tells Ansible to run all tasks directly on our WSL machine without SSH.

---

## Phase 4 — Juniper Switch Configuration Playbook

### Directory: `juniper-switch-playbook/`

### What We Built

We created a production-ready Ansible playbook that configures Juniper EX and QFX series switches using **NETCONF** (Network Configuration Protocol). This playbook handles everything from basic system settings to VLAN creation, interface configuration, routing, and security hardening.

### Directory Structure

```
juniper-switch-playbook/
├── ansible.cfg                     # Ansible settings for this project
├── inventory                       # Switch hostnames and IPs
├── playbook.yml                    # Main playbook (all tasks)
├── group_vars/
│   └── junos_switches.yml          # Shared configuration for ALL switches
├── host_vars/
│   └── switch01.yml                # Per-switch overrides
├── templates/
│   └── banner.j2                   # Login banner Jinja2 template
├── backups/                        # Auto-created for config backups
└── README.md                       # Quick reference
```

### How It Works — Task by Task

Our playbook connects to each Juniper switch over NETCONF (port 830) and applies configuration in the following order:

#### 1. Configuration Backup

Before we change anything, we back up the running configuration of each switch. The backup files are saved locally in the `backups/` directory with the format `<hostname>_<date>.conf`. This gives us a safety net — if anything goes wrong, we have the original config to restore.

#### 2. System Basics

We configure the foundational settings every switch needs:
- **Hostname** — set from the Ansible inventory hostname
- **Domain name** — e.g., `example.com`
- **DNS servers** — e.g., `8.8.8.8`, `8.8.4.4`
- **Timezone** — e.g., `UTC`

#### 3. NTP (Network Time Protocol)

Accurate time is critical for logging, certificates, and troubleshooting. We configure one or more NTP servers, with the ability to mark one as `prefer` (the primary source).

Example from our variables:
```yaml
ntp_servers:
  - address: 10.0.0.1
    prefer: true
  - address: 10.0.0.2
    prefer: false
```

This generates the Junos commands:
```
set system ntp server 10.0.0.1 prefer
set system ntp server 10.0.0.2
```

#### 4. Syslog

We configure both **remote syslog servers** (for centralized log collection) and **local log files**. This is essential for monitoring and compliance:

- Remote servers receive specific severity levels (e.g., `warning` and above)
- Local files capture different categories (e.g., `interactive-commands` for audit trails)

#### 5. Login Banner

We deploy a MOTD (Message of the Day) banner that displays when users connect to the switch. Our default banner includes a legal notice about authorized access.

#### 6. SNMP

We configure SNMP for network monitoring:
- **Location** and **contact** strings for device identification
- **Community strings** with appropriate authorization levels (read-only / read-write)

#### 7. Local Users

We create local user accounts on each switch with:
- **Username** and **full name**
- **Login class** — `super-user`, `read-only`, etc.
- **Encrypted password** — generated with `openssl passwd -6`
- **SSH public key** (optional) — for passwordless authentication

Our default setup includes three users:
| User | Class | Purpose |
|------|-------|---------|
| `admin` | super-user | Primary admin account |
| `ansible` | super-user | Service account for automation |
| `readonly` | read-only | Monitoring / NOC access |

#### 8. NETCONF & SSH Services

We ensure that both SSH and NETCONF-over-SSH are enabled. NETCONF is our primary connection method, and SSH is needed as its transport.

#### 9. VLANs

We create VLANs with descriptive names. Each VLAN can optionally have an **L3 IRB (Integrated Routing and Bridging) interface** — this is how we assign an IP address to a VLAN on a Juniper switch, making it act as the default gateway for that subnet.

Our default VLANs:

| VLAN | ID | L3 Gateway | Purpose |
|------|----|------------|---------|
| MGMT | 10 | 10.10.10.1/24 | Management |
| USERS | 20 | 10.10.20.1/24 | Workstations |
| SERVERS | 30 | 10.10.30.1/24 | Servers |
| VOICE | 40 | — | VoIP (L2 only) |
| NATIVE | 999 | — | Native/untagged |

For VLANs with `l3_interface: true`, we automatically:
1. Create the VLAN and associate it with an IRB unit: `set vlans MGMT l3-interface irb.10`
2. Configure the IRB interface with an IP: `set interfaces irb unit 10 family inet address 10.10.10.1/24`

#### 10. Access Interfaces

We configure switch ports in **access mode** — each port is assigned to a single VLAN. These are typically used for end-user devices (PCs, phones, servers).

Example:
```yaml
access_interfaces:
  - name: ge-0/0/0
    description: "User PC - Desk 101"
    vlan: USERS
    enabled: true
```

This generates:
```
set interfaces ge-0/0/0 description "User PC - Desk 101"
set interfaces ge-0/0/0 unit 0 family ethernet-switching interface-mode access
set interfaces ge-0/0/0 unit 0 family ethernet-switching vlan members USERS
```

We can also disable unused ports by setting `enabled: false`, which adds `set interfaces ge-0/0/X disable`.

#### 11. Trunk Interfaces

We configure uplink ports in **trunk mode** — these carry multiple VLANs between switches. We specify which VLANs are allowed and which VLAN is the native (untagged) VLAN.

Example:
```yaml
trunk_interfaces:
  - name: ge-0/0/46
    description: "Uplink to Core Switch 1"
    allowed_vlans: [MGMT, USERS, SERVERS, VOICE]
    native_vlan: NATIVE
```

#### 12. Static Routes

We configure static routes, most commonly a default gateway:

```yaml
static_routes:
  - prefix: 0.0.0.0/0
    next_hop: 10.10.10.254
```

#### 13. OSPF (Optional)

For environments that need dynamic routing, we included optional OSPF support. It's disabled by default (`enable_ospf: false`). When enabled, we configure:
- **Router ID** — typically the management IP
- **OSPF area** — usually `0.0.0.0` (backbone)
- **Interfaces** — with the ability to mark some as `passive` (advertise the subnet but don't form adjacencies)

Passive interfaces are used for user/server subnets that don't need to participate in OSPF neighbor relationships.

#### 14. Security Hardening

We apply a baseline security configuration:

| Setting | Value | Rationale |
|---------|-------|-----------|
| SSH root login | **denied** | Prevent direct root access |
| SSH protocol | **v2 only** | SSHv1 is insecure |
| Max SSH sessions | **5** per connection | Prevent resource exhaustion |
| Login retries | **3** before disconnect | Brute-force protection |
| Backoff factor | **6** seconds | Slow down repeated failures |
| Console auto-logout | **enabled** | Secure unattended consoles |
| ICMP redirects | **disabled** | Prevent routing manipulation |

#### 15. Commit & Verification

After all changes are applied, we perform a final commit with a timestamped comment for audit purposes. Then we gather switch facts (hostname, model, serial number, Junos version) and display a summary.

### How to Run It

```bash
# Copy to WSL
cp -r /mnt/c/Users/Nish/workspace/juniper-switch-playbook ~/juniper-switch-playbook
cd ~/juniper-switch-playbook

# Step 1: Add our switch IPs to the inventory
vim inventory

# Step 2: Customize the configuration variables
vim group_vars/junos_switches.yml

# Step 3: (Optional) Add per-switch overrides
vim host_vars/switch01.yml

# Step 4: Run against all switches
ansible-playbook playbook.yml --ask-pass

# Or target a single switch
ansible-playbook playbook.yml --limit switch01 --ask-pass

# Or do a dry run first
ansible-playbook playbook.yml --check --diff --ask-pass
```

### Understanding the File Structure

Here is how each file in the playbook contributes:

| File | Role | What We Edit |
|------|------|--------------|
| `inventory` | **Where** to connect | Switch hostnames, IPs, credentials |
| `group_vars/junos_switches.yml` | **What** to configure (shared) | VLANs, users, NTP, routes — applies to ALL switches |
| `host_vars/switch01.yml` | **What** to configure (per-switch) | Overrides for a specific switch (e.g., different SNMP location) |
| `playbook.yml` | **How** to configure | The task logic — we rarely need to edit this |
| `ansible.cfg` | **Ansible behavior** | Timeouts, verbosity, connection settings |
| `templates/banner.j2` | **Banner content** | Login banner text |

### Connection Method: NETCONF

We chose **NETCONF** over CLI/SSH for communicating with our Juniper switches because:

- **Structured data** — NETCONF uses XML, so we get machine-parseable responses instead of unstructured CLI output
- **Transactional** — Changes are applied atomically (all-or-nothing), reducing the risk of partial configurations
- **Candidate configuration** — We edit a candidate config and commit it, rather than making live changes
- **Native to Junos** — NETCONF is a first-class citizen on Juniper devices

NETCONF runs over SSH on **port 830**. Our inventory specifies this connection method:

```ini
[junos_switches:vars]
ansible_connection=ansible.netcommon.netconf
```

> **Prerequisite:** NETCONF must be enabled on the switch before we can manage it:
> ```
> set system services netconf ssh
> commit
> ```

---

## Ansible Variable Precedence (How It Works)

A common question is: *"Why do we edit both the inventory and group_vars?"*

The answer is that **they contain different variables serving different purposes**. They don't conflict — they complement each other:

```
┌──────────────────────────────────────────────────────┐
│                    INVENTORY                          │
│                                                       │
│  Defines WHERE to connect:                            │
│  • switch01 ansible_host=192.168.1.10                │
│  • ansible_user=ansible                               │
│  • ansible_connection=netconf                         │
│                                                       │
│  These are CONNECTION variables.                      │
└──────────────┬───────────────────────────────────────┘
               │
               │  (Both feed into the playbook)
               │
┌──────────────┴───────────────────────────────────────┐
│                  GROUP_VARS                            │
│                                                       │
│  Defines WHAT to configure:                           │
│  • vlans: [{name: MGMT, vlan_id: 10, ...}]           │
│  • ntp_servers: [{address: 10.0.0.1}]                │
│  • snmp_communities: [{name: public_ro}]             │
│                                                       │
│  These are CONFIGURATION variables.                   │
└──────────────────────────────────────────────────────┘
```

If the **same variable** appeared in both files, the inventory value would indeed take precedence. But in our design, we intentionally separate concerns:

| Precedence (highest → lowest) | Source |
|-------------------------------|--------|
| 1 | Command-line `--extra-vars` |
| 2 | `host_vars/<hostname>.yml` |
| 3 | Inventory host variables |
| 4 | `group_vars/<group>.yml` |
| 5 | Inventory group variables |
| 6 | `vars/main.yml` (vars_files) |
| 7 | Role defaults |

We use `host_vars/` when a specific switch needs different values than the rest of the group — for example, a different SNMP location or different IRB IP addresses.

---

## Complete File Reference

### Root Directory

| File | Type | Description |
|------|------|-------------|
| `enable-wsl.ps1` | PowerShell Script | Enables WSL 2 on Windows 11 and installs Ubuntu |
| `install-ansible.sh` | Bash Script | Installs Ansible via the official PPA on Ubuntu 24.04 |
| `DOCUMENTATION.md` | Documentation | This file — our comprehensive project guide |

### `dev-setup-playbook/`

| File | Description |
|------|-------------|
| `playbook.yml` | Main playbook — installs packages, creates venv, configures SSH/Git |
| `inventory` | Local inventory targeting `localhost` |
| `vars/main.yml` | All customizable variables (packages, paths, Git config) |
| `README.md` | Quick-start guide for the dev setup playbook |

### `juniper-switch-playbook/`

| File | Description |
|------|-------------|
| `playbook.yml` | Main playbook — full Juniper switch configuration |
| `inventory` | Switch hostnames, IPs, and connection settings |
| `ansible.cfg` | Ansible configuration (timeouts, output format) |
| `group_vars/junos_switches.yml` | Shared configuration for all switches |
| `host_vars/switch01.yml` | Per-switch overrides (example template) |
| `templates/banner.j2` | Login banner Jinja2 template |
| `README.md` | Quick-start guide for the Juniper playbook |

---

## Troubleshooting

### WSL Issues

| Problem | Solution |
|---------|----------|
| "WSL 2 requires an update to its kernel component" | Run `wsl --update` from PowerShell |
| Features not taking effect after script | Reboot the machine — a restart is mandatory |
| Can't access Windows files from WSL | They are at `/mnt/c/Users/Nish/workspace/` |

### Ansible Issues

| Problem | Solution |
|---------|----------|
| `ansible: command not found` | Re-run `install-ansible.sh` or check `which ansible` |
| PPA add fails | Ensure `software-properties-common` is installed |
| "Permission denied" running playbook | Use `--ask-become-pass` to provide sudo password |

### Dev Setup Playbook Issues

| Problem | Solution |
|---------|----------|
| pip install fails for pyats/genie | Ensure `build-essential`, `libffi-dev`, `libssl-dev` are installed |
| `snmp-mibs-downloader` not found | The playbook enables the multiverse repo — run it again |
| Virtual environment not activating | Run `source ~/network-automation/venv/bin/activate` or use the `netenv` alias |

### Juniper Playbook Issues

| Problem | Solution |
|---------|----------|
| "Connection refused" on NETCONF | Enable NETCONF on the switch: `set system services netconf ssh` then `commit` |
| "Authentication failed" | Verify `ansible_user` and `ansible_password` in the inventory, or use `--ask-pass` |
| "Commit check failed" | Run with `--check --diff` first to see what changes would be made |
| Timeout during commit | Increase `command_timeout` in `ansible.cfg` (default is 60s) |
| Old switch rejects SSH connection | Our dev-setup playbook configures legacy SSH algorithms — ensure SSH config is applied |

---

## Next Steps

Here are some ways we can expand our toolkit:

1. **Add more vendor playbooks** — We can create similar playbooks for Cisco IOS, Arista EOS, and Palo Alto firewalls using the same pattern.

2. **Create a config backup playbook** — A standalone playbook that backs up configurations from all our network devices on a schedule.

3. **Add compliance checking** — Playbooks that audit our switch configurations against a security baseline and report deviations.

4. **Integrate with Git** — Version-control our device configurations by committing backups to a Git repository after each change.

5. **Build Ansible Roles** — Refactor our playbook tasks into reusable roles (e.g., `role: juniper-base`, `role: juniper-vlans`) for better modularity.

6. **Add CI/CD** — Set up a pipeline that runs `--check --diff` on pull requests so we can review changes before deploying them to production switches.

---

> **Maintained by our Network Engineering Team** — For questions or contributions, update this document and commit your changes.
