#!/bin/bash
set -euo pipefail

echo "========================================="
echo " Ansible Installer for Ubuntu 24.04 (WSL)"
echo "========================================="
echo

# Ensure running on Ubuntu 24.04
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [ "$ID" != "ubuntu" ] || [[ "$VERSION_ID" != "24.04"* ]]; then
        echo "WARNING: This script is intended for Ubuntu 24.04. Detected: $PRETTY_NAME"
        read -rp "Continue anyway? (y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo "Aborted."
            exit 1
        fi
    fi
else
    echo "WARNING: Could not detect OS version."
fi

echo "[1/4] Updating package index..."
sudo apt update -y

echo
echo "[2/4] Installing prerequisites..."
sudo apt install -y software-properties-common

echo
echo "[3/4] Adding official Ansible PPA..."
sudo add-apt-repository --yes --update ppa:ansible/ansible

echo
echo "[4/4] Installing Ansible..."
sudo apt install -y ansible

echo
echo "========================================="
echo " Installation complete!"
echo "========================================="
echo
ansible --version
echo
echo "Run 'ansible --version' to verify at any time."
