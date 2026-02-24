# Ansible Architecture, Commands & Python Comparison

## A Comprehensive Reference Guide

**Author:** NetDevOps Team 
**Version:** 1.0 
**Date:** 2025

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Ansible Architecture](#2-ansible-architecture)
3. [How Ansible Works](#3-how-ansible-works)
4. [Ansible vs Python Comparison](#4-ansible-vs-python-comparison)
5. [Installation and Setup](#5-installation-and-setup)
6. [Inventory Management](#6-inventory-management)
7. [Ad-Hoc Commands](#7-ad-hoc-commands)
8. [Playbook Fundamentals](#8-playbook-fundamentals)
9. [Ansible Modules Deep Dive](#9-ansible-modules-deep-dive)
10. [Jinja2 Templating](#10-jinja2-templating)
11. [Roles and Directory Structure](#11-roles-and-directory-structure)
12. [Ansible Vault](#12-ansible-vault)
13. [Common Ansible Commands Cheat Sheet](#13-common-ansible-commands-cheat-sheet)
14. [Error Handling and Debugging](#14-error-handling-and-debugging)
15. [Best Practices](#15-best-practices)
16. [Quick Comparison Reference](#16-quick-comparison-reference)

---

## 1. Introduction

### What is Ansible?

Ansible is an open-source automation tool developed by Red Hat that enables infrastructure as code (IaC), configuration management, application deployment, and orchestration. It uses a simple, human-readable language (YAML) to describe automation jobs, making it accessible to both developers and system administrators.

### Why Ansible Matters for Automation

- **Agentless Architecture** - No software needs to be installed on managed nodes
- **Simple YAML Syntax** - Easy to learn compared to writing full programs
- **Idempotent Operations** - Running the same playbook multiple times produces the same result
- **Extensible** - Thousands of modules for cloud, network, security, and more
- **Push-Based Model** - You control when changes happen from a central node
- **Community and Enterprise Support** - Massive ecosystem with Ansible Galaxy and Red Hat backing

### Why Compare with Python?

Python is the underlying language of Ansible itself and is the most popular language for DevOps and network automation. Understanding how Ansible tasks map to Python code helps engineers:

- Decide when to use Ansible vs custom Python scripts
- Debug Ansible behavior by understanding what happens under the hood
- Extend Ansible with custom modules written in Python
- Transition between the two approaches as project needs evolve

---

## 2. Ansible Architecture

### Architecture Diagram

```
+------------------------------------------------------------------+
|                        CONTROL NODE                               |
|  (Your workstation or CI/CD server running Ansible)               |
|                                                                   |
|  +-------------+  +-------------+  +-----------+  +----------+   |
|  |  Inventory  |  |  Playbooks  |  |  Modules  |  |  Plugins |   |
|  | (hosts.ini) |  | (*.yml)     |  | (builtin) |  | (custom) |   |
|  +------+------+  +------+------+  +-----+-----+  +----+-----+   |
|         |                |               |              |         |
|         +--------+-------+-------+-------+------+-------+         |
|                  |               |              |                 |
|           +------v------+  +-----v-----+  +-----v-----+          |
|           | ansible-    |  | ansible-  |  | ansible-  |          |
|           | playbook    |  | galaxy    |  | vault     |          |
|           +------+------+  +-----------+  +-----------+          |
|                  |                                                |
+------------------+------------------------------------------------+
                   |
                   | SSH / WinRM / NETCONF (No agents required)
                   |
     +-------------+-------------+-------------+
     |             |             |             |
+----v----+  +----v----+  +----v----+  +------v------+
| Managed |  | Managed |  | Managed |  |   Managed   |
| Node 1  |  | Node 2  |  | Node 3  |  |   Node N    |
| (Linux) |  | (Linux) |  |(Windows)|  |  (Network)  |
+---------+  +---------+  +---------+  +-------------+
```

### Core Components

### Control Node

The machine where Ansible is installed and from which automation is run. This is typically your workstation or a dedicated automation server.

- Runs on Linux/macOS (Windows requires WSL)
- Contains all playbooks, inventory, and configuration files
- Initiates connections to managed nodes

### Managed Nodes

The target systems that Ansible manages. These can be servers, network devices, cloud instances, or containers.

- No Ansible agent required
- Only need SSH (Linux), WinRM (Windows), or NETCONF (Network devices)
- Python required on Linux/macOS managed nodes for most modules

### Inventory

A file or script that defines the hosts and groups Ansible manages. Can be static (INI/YAML files) or dynamic (scripts/plugins that query cloud APIs).

```ini
# Static INI inventory example
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[dbservers]
db1 ansible_host=192.168.1.20

[all:vars]
ansible_user=admin
```

### Modules

Discrete units of code that Ansible executes on managed nodes. Each module handles a specific task (e.g., install a package, copy a file, configure a network interface).

- Over 3,000+ built-in modules
- Can be written in any language (most are Python)
- Modules are idempotent by design

### Plugins

Extend Ansible core functionality. Types include:

- **Connection plugins** - How Ansible connects (SSH, WinRM, NETCONF)
- **Callback plugins** - Control output formatting
- **Lookup plugins** - Access external data sources
- **Filter plugins** - Transform data in templates
- **Inventory plugins** - Dynamic inventory sources

### Playbooks

YAML files that define a set of tasks to execute on managed nodes. Playbooks are the core of Ansible automation.

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: true
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
```

### Roles

Reusable, self-contained units of automation that include tasks, variables, files, templates, and handlers organized in a standard directory structure.

### Collections

Distribution format for Ansible content that can include playbooks, roles, modules, and plugins. Collections are distributed through Ansible Galaxy.

### Ansible Galaxy

A public repository for sharing Ansible roles and collections. Similar to PyPI for Python or npm for Node.js.

```bash
# Install a collection from Galaxy
ansible-galaxy collection install cisco.ios
ansible-galaxy collection install junipernetworks.junos
```

---

## 3. How Ansible Works

### Agentless Model

Unlike tools such as Puppet or Chef, Ansible does not require any agent software on managed nodes. It connects using standard protocols:

| Protocol | Target | Port | Use Case |
|----------|--------|------|----------|
| SSH | Linux/macOS/Network | 22 | Most common |
| WinRM | Windows | 5985/5986 | Windows management |
| NETCONF | Network devices | 830 | Juniper, Cisco IOS-XR |
| API/REST | Cloud services | 443 | AWS, Azure, GCP |

### Push-Based Architecture

Ansible uses a push-based model where the control node pushes configurations to managed nodes on demand. This contrasts with pull-based tools where agents periodically check for updates.

```
Push-Based (Ansible):           Pull-Based (Puppet/Chef):

Control Node                    Puppet Server
    |                               |
    +---> Push config               |  <--- Agent polls
    |     to nodes                  |       for changes
    |                               |
    v                               v
Managed Nodes               Managed Nodes (agents)
```

### Execution Flow

1. Ansible reads the playbook and inventory
2. Determines which hosts to target
3. Generates Python scripts from modules
4. Copies scripts to managed nodes via SSH/SCP
5. Executes scripts on remote nodes
6. Captures output (JSON) and returns results
7. Cleans up temporary files

### Idemp
