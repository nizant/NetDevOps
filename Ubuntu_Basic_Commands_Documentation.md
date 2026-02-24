# Ubuntu Basic Commands Documentation

## A Comprehensive Reference Guide

---

**Author:** NetDevOps Team  
**Date:** 2025  
**Version:** 1.0

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Information Commands](#2-system-information-commands)
3. [File & Directory Management](#3-file--directory-management)
4. [File Viewing & Editing](#4-file-viewing--editing)
5. [File Permissions & Ownership](#5-file-permissions--ownership)
6. [User Management](#6-user-management)
7. [Package Management (APT)](#7-package-management-apt)
8. [Process Management](#8-process-management)
9. [Networking Commands](#9-networking-commands)
10. [Disk & Storage Management](#10-disk--storage-management)
11. [Search & Find Commands](#11-search--find-commands)
12. [Compression & Archiving](#12-compression--archiving)
13. [SSH & Remote Access](#13-ssh--remote-access)
14. [System Services (systemctl)](#14-system-services-systemctl)
15. [Useful Shortcuts & Tips](#15-useful-shortcuts--tips)
16. [Quick Reference Cheat Sheet](#16-quick-reference-cheat-sheet)

---

## 1. Introduction

Ubuntu is a popular Debian-based Linux distribution widely used for servers, desktops, and cloud infrastructure. This guide covers essential terminal commands every Ubuntu user and system administrator should know.

**Opening the Terminal:**
- Press `Ctrl + Alt + T` to open the terminal
- Or search for "Terminal" in the application menu

**Command Syntax Convention:**
```
command [OPTIONS] [ARGUMENTS]
```
- `[ ]` indicates optional parameters
- `< >` indicates required parameters
- `|` indicates "or" (choose one)

---

## 2. System Information Commands

### Display System Information

```bash
# Display Linux kernel version
uname -r

# Display all system information
uname -a

# Display Ubuntu version
lsb_release -a

# Display hostname
hostname

# Display current date and time
date

# Display system uptime
uptime

# Display logged-in users
who

# Display current user
whoami
```

### Hardware Information

```bash
# Display CPU information
lscpu

# Display memory usage
free -h

# Display detailed hardware info
lshw -short

# Display PCI devices
lspci

# Display USB devices
lsusb

# Display block devices (disks)
lsblk
```

---

## 3. File & Directory Management

### Navigating Directories

```bash
# Print current working directory
pwd

# Change directory
cd /path/to/directory

# Go to home directory
cd ~
cd

# Go up one directory level
cd ..

# Go to the previous directory
cd -

# Go to root directory
cd /
```

### Listing Files

```bash
# List files and directories
ls

# List with detailed information (permissions, size, date)
ls -l

# List all files including hidden files
ls -a

# List with detailed info + hidden files
ls -la

# List with human-readable file sizes
ls -lh

# List files sorted by modification time (newest first)
ls -lt

# List files recursively
ls -R
```

### Creating Files & Directories

```bash
# Create an empty file
touch filename.txt

# Create a new directory
mkdir my_directory

# Create nested directories (parent + child)
mkdir -p parent/child/grandchild

# Create a file with content
echo "Hello World" > filename.txt
```

### Copying, Moving & Renaming

```bash
# Copy a file
cp source.txt destination.txt

# Copy a file to another directory
cp source.txt /path/to/destination/

# Copy a directory recursively
cp -r source_dir/ destination_dir/

# Move a file (also used for renaming)
mv oldname.txt newname.txt

# Move a file to another directory
mv file.txt /path/to/destination/

# Move a directory
mv source_dir/ /path/to/destination/
```

### Deleting Files & Directories

```bash
# Remove a file
rm filename.txt

# Remove a file (prompt before deletion)
rm -i filename.txt

# Remove a directory and its contents recursively
rm -r directory_name/

# Force remove without prompting
rm -rf directory_name/

# Remove an empty directory
rmdir empty_directory/
```

### Symbolic & Hard Links

```bash
# Create a symbolic (soft) link
ln -s /path/to/original /path/to/link

# Create a hard link
ln /path/to/original /path/to/link

# View where a symbolic link points
readlink symlink_name
```

---

## 4. File Viewing & Editing

### Viewing File Contents

```bash
# Display entire file content
cat filename.txt

# Display with line numbers
cat -n filename.txt

# View file page-by-page (scroll with Space, quit with q)
less filename.txt

# View file page-by-page (forward only)
more filename.txt

# Display the first 10 lines
head filename.txt

# Display the first N lines
head -n 20 filename.txt

# Display the last 10 lines
tail filename.txt

# Display the last N lines
tail -n 20 filename.txt

# Follow a file in real-time (great for logs)
tail -f /var/log/syslog
```

### Text Editors

```bash
# Nano editor (beginner-friendly)
nano filename.txt
# Save: Ctrl + O | Exit: Ctrl + X

# Vim editor (advanced)
vim filename.txt
# Insert mode: i | Save & Exit: Esc, :wq | Exit without saving: Esc, :q!

# Vi editor
vi filename.txt
```

### Text Manipulation

```bash
# Sort lines in a file
sort filename.txt

# Remove duplicate consecutive lines
uniq filename.txt

# Sort and remove all duplicates
sort filename.txt | uniq

# Count lines, words, and characters
wc filename.txt

# Count only lines
wc -l filename.txt

# Display specific columns (e.g., column 1)
cut -d ',' -f 1 filename.csv

# Replace text in a file
sed 's/old_text/new_text/g' filename.txt

# Print lines matching a pattern
awk '/pattern/ {print}' filename.txt
```

---

## 5. File Permissions & Ownership

### Understanding Permissions

```
Permission Format: -rwxrwxrwx
                    |  |  |  |
                    |  |  |  +-- Others (o)
                    |  |  +----- Group (g)
                    |  +-------- User/Owner (u)
                    +----------- File type (- = file, d = directory)

r = read (4)    w = write (2)    x = execute (1)
```

### Changing Permissions

```bash
# Give owner full permissions (read, write, execute)
chmod 700 filename.txt

# Give owner full, group read+execute, others read
chmod 754 filename.txt

# Common permission sets
chmod 644 filename.txt   # Owner: rw, Group: r, Others: r
chmod 755 script.sh      # Owner: rwx, Group: rx, Others: rx
chmod 600 private.key    # Owner: rw, Group: none, Others: none

# Add execute permission for owner
chmod u+x script.sh

# Remove write permission for group
chmod g-w filename.txt

# Add read permission for all
chmod a+r filename.txt

# Apply permissions recursively
chmod -R 755 directory/
```

### Changing Ownership

```bash
# Change owner of a file
sudo chown newowner filename.txt

# Change owner and group
sudo chown newowner:newgroup filename.txt

# Change ownership recursively
sudo chown -R newowner:newgroup directory/

# Change group only
sudo chgrp newgroup filename.txt
```

---

## 6. User Management

### User Operations

```bash
# Add a new user
sudo adduser username

# Add a new user (low-level command)
sudo useradd -m username

# Delete a user
sudo deluser username

# Delete a user and their home directory
sudo deluser --remove-home username

# Modify a user
sudo usermod -aG groupname username    # Add user to a group

# Set or change a user's password
sudo passwd username

# Switch to another user
su - username

# Switch to root user
sudo su -

# Execute a command as root
sudo command_here

# Display user ID and group info
id username

# List all users
cat /etc/passwd

# List all groups
cat /etc/group
```

### Group Operations

```bash
# Create a new group
sudo groupadd groupname

# Delete a group
sudo groupdel groupname

# Add a user to a group
sudo usermod -aG groupname username

# List groups a user belongs to
groups username
```

---

## 7. Package Management (APT)

### Updating & Upgrading

```bash
# Update package lists (fetch latest info from repositories)
sudo apt update

# Upgrade all installed packages
sudo apt upgrade

# Update + upgrade in one line
sudo apt update && sudo apt upgrade -y

# Full upgrade (handles dependencies more aggressively)
sudo apt full-upgrade

# Upgrade the entire distribution
sudo apt dist-upgrade
```

### Installing & Removing Packages

```bash
# Install a package
sudo apt install package_name

# Install multiple packages
sudo apt install package1 package2 package3

# Install without prompting (auto yes)
sudo apt install -y package_name

# Remove a package (keep config files)
sudo apt remove package_name

# Remove a package and its config files
sudo apt purge package_name

# Remove unused dependencies
sudo apt autoremove

# Clean package cache
sudo apt clean
sudo apt autoclean
```

### Searching & Package Information

```bash
# Search for a package
apt search keyword

# Show package details
apt show package_name

# List installed packages
apt list --installed

# List upgradable packages
apt list --upgradable

# Check if a package is installed
dpkg -l | grep package_name
```

### Installing .deb Files

```bash
# Install a .deb file
sudo dpkg -i package_file.deb

# Fix broken dependencies after dpkg install
sudo apt install -f
```

---

## 8. Process Management

### Viewing Processes

```bash
# List running processes (snapshot)
ps aux

# List processes in tree format
ps auxf

# List processes for current user
ps -u $USER

# Real-time process monitor
top

# Improved process monitor (if installed)
htop

# Display process by name
pgrep -a process_name
```

### Managing Processes

```bash
# Run a command in the background
command &

# List background jobs
jobs

# Bring a background job to the foreground
fg %1

# Send a job to the background
bg %1

# Kill a process by PID
kill PID

# Force kill a process
kill -9 PID

# Kill a process by name
killall process_name

# Kill processes matching a pattern
pkill pattern
```

---

## 9. Networking Commands

### Network Information

```bash
# Display network interface information
ip addr show

# Display IP address (short form)
ip a

# Display routing table
ip route show

# Display DNS information
cat /etc/resolv.conf

# Display hostname and IP
hostname -I
```

### Connectivity Testing

```bash
# Ping a host
ping google.com

# Ping with a limited count
ping -c 4 google.com

# Trace the route to a host
traceroute google.com

# Trace route (modern alternative)
tracepath google.com

# DNS lookup
nslookup google.com

# Detailed DNS lookup
dig google.com

# Check if a port is open
nc -zv hostname port

# Test connectivity to a port
telnet hostname port
```

### Network Utilities

```bash
# Display listening ports and connections
ss -tuln

# Display all connections
ss -a

# Display network statistics
netstat -s

# Download a file from the web
wget https://example.com/file.tar.gz

# Download a file with curl
curl -O https://example.com/file.tar.gz

# Make an HTTP GET request
curl https://api.example.com/data

# Display network interface statistics
ifstat
```

### Firewall (UFW)

```bash
# Check firewall status
sudo ufw status

# Enable firewall
sudo ufw enable

# Disable firewall
sudo ufw disable

# Allow a port
sudo ufw allow 22

# Allow a specific service
sudo ufw allow ssh

# Deny a port
sudo ufw deny 8080

# Delete a rule
sudo ufw delete allow 22

# Allow from a specific IP
sudo ufw allow from 192.168.1.100
```

---

## 10. Disk & Storage Management

### Disk Usage

```bash
# Display disk space usage
df -h

# Display disk usage of current directory
du -sh .

# Display disk usage of each subdirectory
du -sh */

# Display disk usage sorted by size
du -sh * | sort -rh

# Display inode usage
df -i
```

### Disk Partitions & Mounting

```bash
# List block devices
lsblk

# List partitions with details
sudo fdisk -l

# Mount a device
sudo mount /dev/sdb1 /mnt/usb

# Unmount a device
sudo umount /mnt/usb

# Display mounted filesystems
mount | column -t

# Check filesystem for errors
sudo fsck /dev/sdb1
```

---

## 11. Search & Find Commands

### Finding Files

```bash
# Find files by name
find /path -name "filename.txt"

# Find files by name (case-insensitive)
find /path -iname "filename.txt"

# Find files by type (f=file, d=directory)
find /path -type f -name "*.log"

# Find files modified in the last 7 days
find /path -mtime -7

# Find files larger than 100MB
find /path -size +100M

# Find and delete files
find /path -name "*.tmp" -delete

# Find files and execute a command on each
find /path -name "*.log" -exec rm {} \;
```

### Searching Inside Files

```bash
# Search for a pattern in a file
grep "pattern" filename.txt

# Search recursively in all files
grep -r "pattern" /path/to/directory/

# Case-insensitive search
grep -i "pattern" filename.txt

# Show line numbers with results
grep -n "pattern" filename.txt

# Count matching lines
grep -c "pattern" filename.txt

# Show lines that do NOT match
grep -v "pattern" filename.txt

# Search with extended regex
grep -E "pattern1|pattern2" filename.txt

# Search using locate (fast, uses database)
locate filename.txt

# Update locate database
sudo updatedb

# Find command location
which command_name
whereis command_name
```

---

## 12. Compression & Archiving

### tar (Tape Archive)

```bash
# Create a tar archive
tar -cvf archive.tar directory/

# Create a compressed archive (gzip)
tar -czvf archive.tar.gz directory/

# Create a compressed archive (bzip2)
tar -cjvf archive.tar.bz2 directory/

# Extract a tar archive
tar -xvf archive.tar

# Extract a gzip archive
tar -xzvf archive.tar.gz

# Extract a bzip2 archive
tar -xjvf archive.tar.bz2

# Extract to a specific directory
tar -xzvf archive.tar.gz -C /path/to/destination/

# List contents of an archive
tar -tzvf archive.tar.gz
```

### zip & gzip

```bash
# Create a zip archive
zip archive.zip file1 file2

# Create a zip archive of a directory
zip -r archive.zip directory/

# Extract a zip archive
unzip archive.zip

# Compress a file with gzip
gzip filename.txt

# Decompress a gzip file
gunzip filename.txt.gz

# Compress with bzip2
bzip2 filename.txt

# Decompress bzip2
bunzip2 filename.txt.bz2
```

---

## 13. SSH & Remote Access

### SSH Commands

```bash
# Connect to a remote server
ssh username@remote_host

# Connect on a specific port
ssh -p 2222 username@remote_host

# Connect using a private key
ssh -i ~/.ssh/private_key username@remote_host

# Generate an SSH key pair
ssh-keygen -t rsa -b 4096

# Generate an Ed25519 key (recommended)
ssh-keygen -t ed25519

# Copy SSH public key to a remote server
ssh-copy-id username@remote_host

# Run a remote command without interactive shell
ssh username@remote_host "ls -la /var/log"
```

### SCP (Secure Copy)

```bash
# Copy a file to a remote server
scp file.txt username@remote_host:/path/to/destination/

# Copy a file from a remote server
scp username@remote_host:/path/to/file.txt /local/path/

# Copy a directory recursively
scp -r directory/ username@remote_host:/path/to/destination/

# Copy using a specific port
scp -P 2222 file.txt username@remote_host:/path/
```

---

## 14. System Services (systemctl)

### Managing Services

```bash
# Start a service
sudo systemctl start service_name

# Stop a service
sudo systemctl stop service_name

# Restart a service
sudo systemctl restart service_name

# Reload service configuration
sudo systemctl reload service_name

# Check service status
sudo systemctl status service_name

# Enable service to start on boot
sudo systemctl enable service_name

# Disable service from starting on boot
sudo systemctl disable service_name

# List all running services
systemctl list-units --type=service --state=running

# List all services
systemctl list-units --type=service --all
```

### System Control

```bash
# Reboot the system
sudo reboot

# Shutdown the system
sudo shutdown -h now

# Shutdown at a specific time
sudo shutdown -h 22:00

# Cancel a scheduled shutdown
sudo shutdown -c

# Log out of the current session
logout
exit
```

---

## 15. Useful Shortcuts & Tips

### Terminal Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + C` | Cancel the current command |
| `Ctrl + Z` | Suspend the current process |
| `Ctrl + D` | Log out / close terminal |
| `Ctrl + L` | Clear the terminal screen |
| `Ctrl + A` | Move cursor to beginning of line |
| `Ctrl + E` | Move cursor to end of line |
| `Ctrl + U` | Delete from cursor to beginning |
| `Ctrl + K` | Delete from cursor to end |
| `Ctrl + W` | Delete the word before cursor |
| `Ctrl + R` | Reverse search command history |
| `Tab` | Auto-complete commands/filenames |
| `Tab Tab` | Show all possible completions |
| `↑ / ↓` | Navigate command history |

### Piping & Redirection

```bash
# Pipe output of one command to another
command1 | command2

# Redirect output to a file (overwrite)
command > output.txt

# Redirect output to a file (append)
command >> output.txt

# Redirect errors to a file
command 2> errors.txt

# Redirect both output and errors
command > output.txt 2>&1

# Redirect both (modern syntax)
command &> output.txt

# Use output of a command as input
command < input.txt
```

### Command Chaining

```bash
# Run commands sequentially
command1 ; command2

# Run command2 only if command1 succeeds
command1 && command2

# Run command2 only if command1 fails
command1 || command2
```

### Aliases & History

```bash
# Create a temporary alias
alias ll='ls -la'

# View all aliases
alias

# Remove an alias
unalias ll

# View command history
history

# Run the last command again
!!

# Run command #42 from history
!42

# Clear command history
history -c
```

---

## 16. Quick Reference Cheat Sheet

| Category | Command | Description |
|---|---|---|
| **Navigation** | `pwd` | Print working directory |
| | `cd /path` | Change directory |
| | `ls -la` | List all files with details |
| **Files** | `cp src dst` | Copy file |
| | `mv src dst` | Move/rename file |
| | `rm file` | Delete file |
| | `touch file` | Create empty file |
| | `mkdir dir` | Create directory |
| **Viewing** | `cat file` | View file contents |
| | `less file` | View file (paginated) |
| | `head -n 10 file` | First 10 lines |
| | `tail -f file` | Follow file updates |
| **Search** | `grep "text" file` | Search in file |
| | `find / -name "file"` | Find file by name |
| **Permissions** | `chmod 755 file` | Change permissions |
| | `chown user:group file` | Change ownership |
| **Packages** | `sudo apt update` | Update package lists |
| | `sudo apt install pkg` | Install a package |
| **Network** | `ip addr show` | Show IP addresses |
| | `ping host` | Test connectivity |
| | `ss -tuln` | Show listening ports |
| **Process** | `ps aux` | List processes |
| | `kill PID` | Kill a process |
| | `top` | Real-time process viewer |
| **System** | `sudo reboot` | Reboot |
| | `df -h` | Disk space usage |
| | `free -h` | Memory usage |
| **Services** | `systemctl status svc` | Service status |
| | `systemctl start svc` | Start a service |

---

## Additional Resources

- **Ubuntu Official Documentation:** [https://help.ubuntu.com](https://help.ubuntu.com)
- **Ubuntu Community Wiki:** [https://wiki.ubuntu.com](https://wiki.ubuntu.com)
- **Man Pages:** Type `man command_name` in the terminal for detailed help
- **Built-in Help:** Type `command_name --help` for quick usage info

---

*This document was created as part of the NetDevOps project documentation.*  
*For questions or contributions, refer to the project repository.*
