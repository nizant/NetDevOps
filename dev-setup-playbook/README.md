# Network Automation Dev Setup Playbook

An Ansible playbook that sets up a complete network device configuration development environment on Ubuntu 24.04 (WSL).

## What Gets Installed

### System Packages
Git, Vim, curl, SSH tools, SNMP utilities, nmap, telnet, TFTP, Python 3, and build tools.

### Python Libraries (in a virtual environment)
netmiko, napalm, nornir, paramiko, scrapli, textfsm, pysnmp, pyats/genie, and more.

### Ansible Collections
- `cisco.ios`, `cisco.iosxe`, `cisco.iosxr`, `cisco.nxos`, `cisco.asa`
- `arista.eos`
- `junipernetworks.junos`
- `ansible.netcommon`, `ansible.utils`

### Project Structure
```
~/network-automation/
├── ansible.cfg
├── playbooks/
├── inventories/
│   └── hosts          # starter inventory
├── roles/
├── templates/
├── group_vars/
├── host_vars/
├── backups/
├── scripts/
└── venv/              # Python virtual environment
```

## Usage

### 1. Customize variables (optional)
Edit `vars/main.yml` to change:
- Git username/email
- Python packages to install
- Ansible collections to install
- Project directory path

### 2. Run the playbook
```bash
cd dev-setup-playbook
ansible-playbook -i inventory playbook.yml --ask-become-pass
```

### 3. Start using the environment
```bash
# Activate the Python virtual environment
netenv

# Navigate to the project directory
netdir

# Verify tools
ansible --version
python -c "import netmiko; print(netmiko.__version__)"
```

## Shell Aliases
The playbook adds these aliases to your `.bashrc`:
- `netenv` — activates the Python virtual environment
- `netdir` — navigates to `~/network-automation/`
