#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Enables WSL (Windows Subsystem for Linux) on Windows 11.
.DESCRIPTION
    This script enables the required Windows features for WSL,
    installs WSL 2, and optionally installs a default Linux distribution.
    Must be run as Administrator.
#>

param(
    [switch]$SkipDistroInstall,
    [string]$Distro = "Ubuntu"
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "`n>> $Message" -ForegroundColor Cyan
}

# Check Windows version
$osVersion = [System.Environment]::OSVersion.Version
if ($osVersion.Build -lt 22000) {
    Write-Host "WARNING: This script is intended for Windows 11 (build 22000+). Your build: $($osVersion.Build)" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne 'y') { exit 0 }
}

Write-Step "Enabling Windows Subsystem for Linux feature..."
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

Write-Step "Enabling Virtual Machine Platform feature..."
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

Write-Step "Setting WSL 2 as the default version..."
wsl --set-default-version 2

Write-Step "Updating WSL to the latest version..."
wsl --update

if (-not $SkipDistroInstall) {
    Write-Step "Installing $Distro distribution..."
    wsl --install -d $Distro
} else {
    Write-Host "`nSkipping distro installation. You can install one later with:" -ForegroundColor Yellow
    Write-Host "  wsl --install -d <DistroName>" -ForegroundColor White
    Write-Host "  wsl --list --online   (to see available distros)" -ForegroundColor White
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host " WSL setup complete!" -ForegroundColor Green
Write-Host " A restart may be required for changes to take effect." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

$restart = Read-Host "`nRestart now? (y/n)"
if ($restart -eq 'y') {
    Restart-Computer -Force
}
