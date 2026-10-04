---
name: ventoy
description: "Configure Ventoy multiboot USB media and plugin settings, and diagnose boot or Secure Boot enrollment issues."
category: cross-platform
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["ventoy", "multiboot-usb", "iso-bootloader", "uefi-secure-boot", "ventoy-json", "mok-enrollment", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Ventoy Multiboot USB Creator AI Skill Guide (Claude)

## Overview & Engine Architecture
Ventoy is an open-source multiboot USB utility that eliminates the need to repeatedly format flash drives. Once Ventoy is installed, users simply copy ISO, WIM, IMG, VHD(x), and EFI files directly onto the data partition. During boot, Ventoy's **in-memory hooking engine** dynamically mounts the target ISO image in RAM and chains execution via GRUB2/Shim. Claude operates as an Operating System Deployment Specialist and Systems Engineer, specializing in **UEFI Secure Boot (MOK - Machine Owner Key) enrollment**, **`ventoy.json` plugin configuration**, **unattended OS automated installations (Windows / Linux kickstarts)**, and **persistent Live Linux storage**.

### Ventoy Disk Partition Structure & Boot Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Ventoy Drive Partition Layout               │
│                                                             │
│  Partition 1: Large Data Partition (exFAT / NTFS / ext4)    │
│  ├── Raw Boot Images (*.iso, *.wim, *.vhd, *.img)           │
│  └── `/ventoy/ventoy.json` (Configuration & Plugin Scripts) │
│                                                             │
│  Partition 2: Hidden Boot Partition (`VTOYEFI` - 32MB FAT)  │
│  ├── UEFI Shim Loader & Enrolled MOK Certificate            │
│  ├── GRUB2 Custom Dynamic Kernel & Hooking Drivers          │
│  └── Legacy x86 MBR / BIOS Bootstrap Code                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **UEFI Secure Boot Remediation**: Guide users through the Machine Owner Key (MOK) enrollment sequence (`Enroll MOK` $\rightarrow$ `Continue` $\rightarrow$ `Enroll Key` $\rightarrow$ `Password: ventoy`) to bypass Secure Boot restrictions without disabling system security.
2. **Declarative `ventoy.json` Authoring**: Author structured plugin configurations to automate Windows 11 hardware bypasses (TPM 2.0 / RAM / CPU checks), auto-inject unattended answers, and configure theme layouts.
3. **Data Persistence Management**: Configure persistent live storage images (`persistence.dat`) for Ubuntu, Kali Linux, and Fedora Live USB environments.
4. **Automated CLI Installation**: Script automated disk preparation on Linux (`Ventoy2Disk.sh -i /dev/sdX`) and Windows (`Ventoy2Disk.exe /I V:`) with safety checks preventing accidental host OS drive overwrites.

---

## Production Configuration Recipe: Master `ventoy.json` Configuration

Save this file as `/ventoy/ventoy.json` on the main Ventoy USB data partition:

```json
{
  "control": [
    { "VTOY_DEFAULT_SEARCH_ROOT": "/ISOs" },
    { "VTOY_MENU_TIMEOUT": "10" },
    { "VTOY_DEFAULT_IMAGE": "/ISOs/Ubuntu-24.04-Desktop.iso" },
    { "VTOY_WIN11_BYPASS_CHECK": "1" },
    { "VTOY_WIN11_BYPASS_NRO": "1" }
  ],
  "theme": {
    "file": "/ventoy/themes/flat/theme.txt",
    "gfxmode": "1920x1080"
  },
  "menu_alias": [
    {
      "image": "/ISOs/Win11_23H2_English_x64.iso",
      "alias": "Windows 11 Enterprise (Unattended Bypass)"
    },
    {
      "image": "/ISOs/Ubuntu-24.04-Desktop.iso",
      "alias": "Ubuntu 24.04 LTS Live (Persistent Storage)"
    },
    {
      "image": "/ISOs/archlinux-x86_64.iso",
      "alias": "Arch Linux Netinstall"
    }
  ],
  "persistence": [
    {
      "image": "/ISOs/Ubuntu-24.04-Desktop.iso",
      "backend": "/ventoy/persistence/ubuntu_persistence.dat"
    }
  ],
  "auto_install": [
    {
      "image": "/ISOs/Win11_23H2_English_x64.iso",
      "template": "/ventoy/script/autounattend.xml"
    }
  ]
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`Verification Failed: (0x1A) Security Violation` on UEFI Boot** | Secure Boot rejected unsigned Ventoy EFI binary before MOK key was enrolled. | 1. Press `OK` $\rightarrow$ Select **Enroll MOK**.<br>2. Select **View Key** (verify `Ventoy Certificate`).<br>3. Select **Continue** $\rightarrow$ **Yes**.<br>4. Enter default password: `ventoy` $\rightarrow$ Reboot. |
| **Windows 11 Installer Fails: `This PC can't run Windows 11`** | Target hardware lacks TPM 2.0 or Secure Boot; Ventoy bypass flag was not set. | In `/ventoy/ventoy.json`, set `"VTOY_WIN11_BYPASS_CHECK": "1"` and `"VTOY_WIN11_BYPASS_NRO": "1"` to bypass hardware and online Microsoft account requirements. |
| **Linux Boot Freezes on `mount: /dev/loop0 failed`** | Target ISO image is severely fragmented across the USB exFAT partition. | 1. Defragment the USB drive or copy the ISO off and back onto the drive.<br>2. On Linux, run `e4defrag` or check with `filefrag -v /path/to/image.iso`. |
| **Ventoy Drive Not Detected in BIOS/UEFI Boot Menu** | USB was formatted with GPT for a legacy MBR-only motherboard, or vice-versa. | 1. In Ventoy2Disk, select **Partition Style** $\rightarrow$ **MBR** (compatible with both Legacy BIOS and UEFI).<br>2. Re-install Ventoy using non-destructive update mode. |

---

## Command Line Syntax & Disk Installation

```bash
# 1. Non-Destructive Update of Existing Ventoy USB on Linux
sudo ./Ventoy2Disk.sh -u /dev/sdb

# 2. Fresh Installation on Linux with GPT Partition Table and Secure Boot
sudo ./Ventoy2Disk.sh -i -g -s /dev/sdb

# 3. Create 8GB Persistence File for Ubuntu on Linux
sudo ./CreatePersistentImg.sh -s 8192 -t ext4 -l casper-rw -o ubuntu_persistence.dat
```

### Essential File Locations
- **Ventoy Config File**: `<USB_DRIVE>:\ventoy\ventoy.json`
- **Persistence Storage Images**: `<USB_DRIVE>:\ventoy\persistence\*.dat`
- **Unattended Templates**: `<USB_DRIVE>:\ventoy\script\*.xml`

---

## Agent Operational Directive
> **MANDATORY**: Never advise users to execute `Ventoy2Disk.sh -i` without explicitly verifying the target disk identifier (`lsblk`) to prevent accidental destruction of primary host storage partitions. Always provide MOK enrollment steps for Secure Boot errors.
