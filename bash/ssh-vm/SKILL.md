---
name: ssh-vm
description: >-
  v1.0.13 — Use when a task requires SSH access to a VM to deploy software or test it there. Skip local-only tests and SSH discussion without a remote VM action.
---

# SSH VM

Use this skill only when the task calls for an actual SSH deployment or test on
a VM. Ask for the VM IP or hostname if missing. Use `ubuntu` for an Ubuntu
Desktop live USB unless the user gives another username. Whenever you provide
VM-console bootstrap commands, always include a `sudo passwd <username>` step
for the SSH account (default `ubuntu`; use the VM's `whoami` value if different).
The user chooses the password at the VM's local `passwd` prompt; do not ask
them to send it in chat. For password-based SSH login, use an interactive
SSH prompt and let the user enter it there. Never print, log, save, or put
passwords in a shell command.

## First contact with a VM

When the user starts a VM task by providing an IP address or hostname and has
not confirmed that SSH setup is complete, assume the VM is unprepared. Do not
connect, probe the port, or run any network reachability check. Give the user
the VM-console setup commands below and wait for them to confirm they ran the
commands. An IP address alone does not mean SSH is ready. If the user confirms
SSH is already configured, proceed to **Connect after setup is confirmed**.

If the operating system is unknown, ask the user to identify it from the VM
console before giving operating-system-specific commands; still do not probe
the VM over the network.

## Fresh Ubuntu VM setup

For a fresh Ubuntu Desktop VM, ask the user to open Terminal on the VM itself
(and finish the welcome screen first if this is a live USB), then run:

```bash
sudo apt update
sudo apt install -y -o Dpkg::Options::="--force-confold" openssh-server
sudo systemctl enable --now ssh
sudo passwd "$(id -un)"
sudo sshd -T | grep -i '^passwordauthentication'
sudo ss -lntp | grep ':22'
hostname -I
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

`sudo passwd "$(id -un)"` sets the password for the current account; if the SSH
username is different, use `sudo passwd <ssh_username>` for that account. The
user enters the new password at the VM's local `passwd` prompt. The apt option
keeps existing package configuration files if dpkg asks which version to use.
Ask them to report whether `passwordauthentication` is `yes` and whether SSH
is listening, but not to share the password. A live USB loses this setup on
reboot.

## Connect after setup is confirmed

Only after the user confirms the console commands ran, or confirms SSH was
already configured, make a connection attempt. Use their IP/hostname, username,
port, and key when provided. For key-based access, a short probe is:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 ubuntu@VM_IP 'id -un; hostname'
```

For password-only access, skip the `BatchMode` probe and open an interactive
SSH session so the user can enter the password at the SSH prompt:

```bash
ssh -tt -o ConnectTimeout=5 ubuntu@VM_IP
```

Use the actual username and add `-p PORT` when the user provides a non-default
port. Never ask the user to send the password in chat or put it in a command.

A new live session may generate a new host key. If SSH warns that the key
changed, compare its fingerprint with the VM console's `ssh-keygen` output
before replacing the old `known_hosts` entry. Never disable host-key checks.
If authentication fails, check the username and ask the user to reset the
password locally with `sudo passwd <ssh_username>` if needed. For a timeout,
check the current IP, port 22 with `sudo ss -lntp`, and `sudo ufw status` on the
VM.

## Deploy and verify

After login, confirm `id -un`, `hostname`, and the relevant VM environment.
Inspect the destination before copying. Transfer the needed files with `scp`
or `rsync` without a delete option, run the project's installer or activation
on the VM, then check its behavior, status, and logs **on the VM**. Respect the
project's desktop and service rules.

For every relevant local change to a project the user asked to run on the VM,
update that project's VM copy, apply the change there, and verify it there.
Local tests alone do not prove a VM deployment. If SSH is unavailable, report
the exact failure and the VM-console step needed to resume.

When a test depends on visible desktop behavior, capture and inspect a VM
screenshot if a safe, supported capture method is available. SSH access alone
does not guarantee access to the guest display; do not assume GUI screenshot
tools will work from a remote shell. If visual confirmation would help but no
capture method is available, ask the user to provide a screenshot. Use the
image to guide any needed fix, then deploy and verify that fix on the VM. Keep
captures outside the project source unless the user asks to retain them.
