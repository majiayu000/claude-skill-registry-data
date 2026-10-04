---
name: embedded-linux-login-debug
description: Use when logging into, connecting to, or preparing to debug an embedded Linux device
---

# Embedded Linux Login Debug

## Overview

Use this skill to choose a safe login path for an embedded Linux device before debugging. The agent should identify the available access method, collect only the required connection details, and start with read-only checks after login.

## When To Use

Use this skill when:

- The user wants to log in to an embedded Linux device, development board, router, gateway, camera, or appliance.
- The user mentions SSH, serial console, UART, ADB, Telnet, local console, recovery console, or vendor web debug access.
- The task requires checking runtime state on a target device before changing files, services, partitions, networking, or firmware.

Do not use this skill when:

- The target is a normal cloud server or desktop Linux machine with a known access path.
- The user only needs static source-code analysis and no device access.
- The request is to flash firmware, erase storage, modify bootloader settings, or change partitions without a separate safety plan.

## Login Method Decision

Ask which access methods are available. If the user is unsure, suggest this order:

1. SSH over network, if the device has an IP address and SSH server.
2. Serial UART console, if network access is unavailable or boot logs are needed.
3. ADB, if the target is Android-based or exposes Android Debug Bridge.
4. Telnet, only for trusted lab networks or legacy devices.
5. Local console with display and keyboard, if physically accessible.
6. Vendor web or recovery console, if shell access is not exposed directly.

## Required Inputs By Method

### SSH

Ask for:

- Device IP address or hostname.
- SSH port, defaulting to `22` if unknown.
- Username.
- Authentication method: password, private key, or agent-forwarded key.
- Whether the network is reachable from the current machine.

If a password is required, ask the user to type it into the SSH prompt when possible. Do not ask the user to paste reusable passwords into chat unless there is no alternative.

Command pattern:

```bash
ssh -p <port> <user>@<ip>
```

### Serial UART

Ask for:

- Local serial device path, such as `/dev/ttyUSB0`, `/dev/ttyACM0`, or `/dev/tty.usbserial-*`.
- Baud rate, commonly `115200`.
- Data format if known, commonly `8N1`.
- Whether the user has permission to access the serial device.
- Whether the board needs reset or power cycle to see boot logs.

Command patterns:

```bash
picocom -b 115200 /dev/ttyUSB0
screen /dev/ttyUSB0 115200
minicom -D /dev/ttyUSB0 -b 115200
```

### ADB

Ask for:

- Whether the device is connected by USB or ADB-over-TCP.
- Whether USB debugging or ADB is enabled.
- Device serial or IP and port, if multiple devices exist.
- Whether shell access requires `su`.

Command patterns:

```bash
adb devices
adb shell
adb connect <ip>:5555
adb -s <serial> shell
```

### Telnet

Ask for:

- Device IP address or hostname.
- Telnet port, defaulting to `23` if unknown.
- Username and password, if required.
- Confirmation that this is a trusted lab network.

Warn that Telnet sends credentials in plaintext. Prefer SSH when available.

Command pattern:

```bash
telnet <ip> <port>
```

### Local Console Or Vendor Console

Ask for:

- Physical access method: HDMI, LCD, keyboard, recovery menu, web UI, or vendor debug page.
- Login account, role, or recovery mode requirements.
- Whether the console can run shell commands or only displays status.
- Any device-specific constraints, such as maintenance windows or watchdog resets.

## Workflow

1. Identify the target.
   Ask what device or board is being debugged, what problem is being investigated, and whether the device is already booted.

1. Select the login method.
   Use the decision list above. If multiple methods are available, prefer the least invasive path that gives enough visibility.

1. Collect required inputs.
   Ask only for the fields required by the selected method. Do not request passwords unless the login tool cannot prompt interactively.

1. Check reachability before login.
   For network methods, use safe checks such as `ping`, `nc -vz <ip> <port>`, or `ssh -v` when appropriate. For serial, confirm the device path exists and is not already in use.

1. Log in.
   Provide the exact command with placeholders or user-provided values. Avoid embedding secrets in commands, shell history, scripts, or logs.

1. Run read-only baseline checks.
   After shell access is confirmed, collect:

```bash
whoami
hostname
uname -a
cat /etc/os-release 2>/dev/null || cat /etc/issue 2>/dev/null
ip addr
ip route
mount
df -h
ps
dmesg | tail -n 80
```

1. Summarize the session.
   Record login method, target identifier, current user, kernel version, OS identity, network addresses, and any immediate anomalies.

## Safety Rules

- Do not reboot, power-cycle, reset, flash, erase, remount read-write, change network settings, kill processes, or edit startup scripts without explicit user approval.
- Treat commands under `/dev/mtd*`, `/dev/mmcblk*`, `/dev/sd*`, bootloader shells, and firmware tools as high risk.
- Prefer read-only inspection until the user confirms the intended fix.
- If the connection method is insecure, such as Telnet, state the risk and keep the session limited to trusted lab environments.
- Do not store passwords in files, shell history, command examples, or final summaries.

## Verification

Before claiming the device is ready for debugging:

- Confirm the selected login method and command.
- Confirm shell access by reporting `whoami`, `hostname`, and `uname -a`.
- Confirm whether the filesystem is read-only or read-write from `mount`.
- Confirm network identity from `ip addr` or the login target.
- State any skipped checks and why.

## Common Failures

- Assuming SSH is available when the device only exposes serial console.
- Asking for every possible credential before choosing a login method.
- Pasting passwords into commands that may be saved in shell history.
- Running destructive recovery, flash, or reboot commands as part of initial login.
- Treating Android ADB shells like normal SSH shells without checking user, `su`, and partition state.

## Example

User:

```text
我要登录一台嵌入式 Linux 设备看看服务为什么没起来。
```

Agent:

1. Asks which access methods are available: SSH, serial UART, ADB, Telnet, local console, or web console.
2. If the user chooses SSH, asks for IP, port, username, and authentication method.
3. Provides `ssh -p <port> <user>@<ip>` and lets the terminal prompt for the password.
4. After login, runs read-only baseline checks.
5. Summarizes the device identity and asks before making any changes.
