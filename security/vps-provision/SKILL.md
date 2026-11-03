---
name: vps-provision
description: "Use when setting up a new VPS or cloud droplet. Hardened first boot: snapshot, non-root sudo user, SSH keys only, root login off, two firewall layers, fail2ban, unattended upgrades, time sync, swap and a verification list."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
metadata:
  hermes:
    tags: [iclone-os, server, vps, security, ssh, firewall, linux]
    related_skills: [ssh-access, server-agent-service, backups-restore, server-troubleshooting, consent]
---

# VPS provision — a hardened server before anything runs on it

## When to use
- The owner has a new VPS or droplet (Ubuntu or Debian LTS) for an agent, a bot or a gateway.
- An existing server still accepts password or root SSH logins.

Work only on a host the owner named in this conversation. Commands are Debian-family; each tool's `--help` or man page is the truth.

## Prerequisites
- An SSH key on this machine, its public half added in the provider panel at creation (see `ssh-access`).
- The server address and the first login the provider gives.
- Every command on the server is a write: ask through the consent door (`~/.iclone-os/bin/acp consent request terminal --reason "…"`), name the host and the change, then wait for the owner's yes; package installs also need `installSoftware`. You operate, the owner pays (economyos law 1): never buy, resize, rebuild or delete a server.

## Quick reference
| Area | Default |
|---|---|
| Rollback | provider snapshot before and after |
| Login | non-root `<user>` with sudo, keys only |
| sshd | `PermitRootLogin no`, `PasswordAuthentication no`, `KbdInteractiveAuthentication no` |
| Firewall | provider firewall AND ufw: deny incoming, allow 22 + only what a service needs |
| Brute force | fail2ban `sshd` jail |
| Patches | unattended-upgrades |
| Time | UTC, NTP synchronised |
| Memory | 2 GB swap on small plans |

## Procedure
1. Take a provider snapshot. Keep a second SSH session open until step 9 passes: it is your way back.
2. Update and install the base tools:
```sh
sudo apt update && sudo apt -y full-upgrade && sudo apt -y install ufw fail2ban unattended-upgrades  # example
```
3. Create the non-root user with your key (the owner sets the sudo password at the prompt; SSH stays key-only):
```sh
sudo useradd -m -s /bin/bash -G sudo <user> && sudo passwd <user>  # example
sudo install -d -m 700 -o <user> -g <user> /home/<user>/.ssh  # example
sudo install -m 600 -o <user> -g <user> ~/.ssh/authorized_keys /home/<user>/.ssh/authorized_keys  # example
```
4. From this machine, log in as `<user>` in a NEW session and run `sudo -v`. Do not go on until it works.
5. Harden sshd with a drop-in that sorts first (sshd keeps the first value it reads; cloud images ship `50-cloud-init.conf` with passwords on):
```sh
printf 'PermitRootLogin no\nPasswordAuthentication no\nKbdInteractiveAuthentication no\n' | sudo tee /etc/ssh/sshd_config.d/00-hardening.conf  # example
sudo sshd -t && sudo systemctl reload ssh  # example
```
The unit is `ssh` on Debian/Ubuntu, `sshd` on most other distros.
6. Host firewall — allow SSH before you enable it:
```sh
sudo ufw default deny incoming && sudo ufw default allow outgoing && sudo ufw allow OpenSSH && sudo ufw --force enable  # example
```
Mirror it in the provider firewall (inbound 22 plus the service ports). A long-polling bot or the Hermes gateway needs no inbound port.
7. fail2ban and automatic security updates:
```sh
printf '[sshd]\nenabled = true\nmaxretry = 5\nbantime = 1h\n' | sudo tee /etc/fail2ban/jail.d/sshd.local && sudo systemctl enable --now fail2ban  # example
sudo dpkg-reconfigure -f noninteractive unattended-upgrades  # example
```
8. Time and swap:
```sh
sudo timedatectl set-timezone UTC && timedatectl show -p NTPSynchronized  # example
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile  # example
grep -q '^/swapfile ' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab  # example
```
9. Run the verification below, then take a second snapshot ("hardened base").

## Pitfalls
- Closing the spare session before a fresh key login as `<user>` works is how people lock themselves out.
- `ufw enable` before `ufw allow OpenSSH` drops your own connection.
- Two firewall layers: a port must be open in both to work, and closed in either to be safe.
- fail2ban not starting on a journal-only system: add `backend = systemd` to the jail.
- 1 GB RAM without swap: package builds die with OOM (see `server-troubleshooting`).

## Never
- Never turn on password or root SSH, and never grant `NOPASSWD: ALL` sudo.
- Never paste a private key, token or password into chat, a command line or a repo.
- Never touch a host the owner did not name.

## Verification
```sh
sudo sshd -T | grep -Ei '^(permitrootlogin|passwordauthentication) ' && sudo ufw status && sudo fail2ban-client status sshd  # example
```
Pass = `permitrootlogin no` and `passwordauthentication no`, ufw `Status: active` with 22 only, the `sshd` jail listed, and
`ssh -o PreferredAuthentications=password <user>@<server-ip>` from this machine ends in `Permission denied (publickey)`.
