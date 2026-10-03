---
name: vps-hardening
description: Baseline-harden a Debian or Ubuntu VPS in roughly thirty minutes. Covers SSH key-only authentication, UFW firewall, fail2ban with web-app jails, unattended security upgrades, kernel sysctls, journalctl retention, and sudo policy. Invoke when provisioning a new VPS, inheriting one without documented hardening, or before exposing a service to the public internet.
---

# VPS Hardening

A pragmatic baseline for a single Debian/Ubuntu VPS hosting a few services. Not a CIS benchmark — those are excellent but too long for a vibe-coded side project to follow on day one. This is the 30-minute version that gets you 90% of the way.

Assumptions: you have root SSH access (typically via the provider's initial password). You will be the first and probably only operator.

## When to invoke

- New VPS provisioned, no hardening yet
- Inherited a VPS with no documentation
- Service is about to face public internet traffic
- Periodic re-audit (quarterly is reasonable)

## Step 0 — Get a backup before changing anything

```bash
# From your laptop, snapshot the VPS via your provider's panel/API first.
# All steps below are reversible, but a snapshot turns a mistake from a crisis into an inconvenience.
```

## Step 1 — Update everything, then create a non-root user

```bash
# As root, on the VPS
apt update && apt upgrade -y
apt install -y sudo ufw fail2ban unattended-upgrades curl ca-certificates gnupg

# Create a personal user with sudo
adduser deploy                # set a strong passphrase (you will rarely use it)
usermod -aG sudo deploy
```

From now on, prefer to SSH as `deploy` and use `sudo` for privileged actions. `root` will be locked from SSH in step 3.

## Step 2 — Authorize your SSH key for the new user

From your **laptop**:

```bash
ssh-copy-id deploy@<vps-ip>
# Verify you can log in as deploy and run sudo
ssh deploy@<vps-ip> 'sudo -v && echo OK'
```

If you do not have an SSH key yet:

```bash
# On the laptop
ssh-keygen -t ed25519 -C "deploy@<your-laptop-name>"
```

Ed25519 is the modern default; RSA-2048 also fine but slower.

## Step 3 — Lock SSH down

Edit `/etc/ssh/sshd_config` (on the VPS, as root or sudo):

```sshd
# Auth
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no

# Hygiene
LoginGraceTime 30
MaxAuthTries 3
MaxSessions 4
ClientAliveInterval 300
ClientAliveCountMax 2

# Reduce surface
AllowAgentForwarding no
AllowTcpForwarding no       # set yes if you actually need SSH tunneling
X11Forwarding no
PrintMotd no
UseDNS no

# Restrict who can log in at all
AllowUsers deploy
```

The "change port from 22" debate is largely security theater for shared-host targeted attacks but does cut log noise — your call. If you change it, update UFW (next step).

Apply, but keep your current session open and **open a second SSH session** to verify before exiting the first:

```bash
sudo sshd -t                  # syntax check
sudo systemctl reload ssh     # or 'sshd' on some distros
```

If the new session works, you are safe to drop the first.

## Step 4 — Firewall (UFW)

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp         # or your custom SSH port
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

For services bound to specific source IPs (admin endpoints, monitoring), use scoped rules:

```bash
sudo ufw allow from 203.0.113.5 to any port 9000 proto tcp comment 'admin from office'
```

## Step 5 — fail2ban

Default install bans on SSH brute-force. Add web jails for the apps you actually run.

```bash
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

In `/etc/fail2ban/jail.local`, ensure `[sshd]` is enabled. For nginx-fronted auth endpoints:

```ini
[nginx-http-auth]
enabled  = true
port     = http,https
logpath  = /var/log/nginx/error.log
maxretry = 5
bantime  = 1h

[wp-login]
enabled  = true
port     = http,https
filter   = wp-login          # create /etc/fail2ban/filter.d/wp-login.conf
logpath  = /var/log/nginx/access.log
maxretry = 5
findtime = 10m
bantime  = 2h
```

```bash
sudo systemctl enable --now fail2ban
sudo fail2ban-client status
```

A common `wp-login.conf` filter:

```ini
[Definition]
failregex = ^<HOST> .* "POST /wp-login.php
ignoreregex =
```

## Step 6 — Unattended security upgrades

```bash
sudo dpkg-reconfigure -plow unattended-upgrades   # Yes
```

Edit `/etc/apt/apt.conf.d/50unattended-upgrades`:

```
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    // "${distro_id}:${distro_codename}-updates";  // optional
};
Unattended-Upgrade::Mail "you@example.com";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "04:00";
```

Test:

```bash
sudo unattended-upgrade --dry-run --debug 2>&1 | head -30
```

If you cannot tolerate auto-reboots (stateful daemons without graceful restart), set `Automatic-Reboot "false"` and create a calendar reminder to reboot weekly.

## Step 7 — Kernel sysctls

`/etc/sysctl.d/99-hardening.conf`:

```
# Network
net.ipv4.tcp_syncookies = 1
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv4.conf.all.log_martians = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Filesystem / kernel
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
kernel.dmesg_restrict = 1
kernel.kptr_restrict = 2
kernel.unprivileged_bpf_disabled = 1
```

Apply:

```bash
sudo sysctl --system
```

## Step 8 — sudo policy

By default, `sudo` requires a password and times out quickly. Keep it that way. Common bad patterns to avoid:

- `deploy ALL=(ALL) NOPASSWD: ALL` — never, except for ephemeral CI users with no SSH access
- Putting service accounts in `sudo` group — they shouldn't need it; use `systemd` units with the right `User=`/`Group=` instead

If a service truly needs to run a single command with sudo (e.g. `systemctl restart myapp`), allow exactly that:

```
deploy ALL=(root) NOPASSWD: /bin/systemctl restart myapp
```

Validate with `visudo` so you cannot save a broken file.

## Step 9 — journalctl retention and log shipping

```bash
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
sudo systemctl restart systemd-journald
```

In `/etc/systemd/journald.conf`:

```
Storage=persistent
SystemMaxUse=2G
SystemKeepFree=2G
SystemMaxFileSize=200M
```

For multi-host setups, ship to a central log store (Loki, ELK, hosted) — but for a single-VPS side project, local retention is fine.

## Step 10 — Backups (yes, this is security)

A VPS is hardened against attackers; backups are hardened against you. Set up:

- **Snapshots at the provider** weekly, retain 4
- **App data export** (DB dumps, uploads) to off-site storage (S3/R2) daily, retain 30 days
- **Test restore once** before you need it — most backups are corrupted in some way and only restore-tested ones are real

## Step 11 — Quick audit script

Run this every month or after onboarding a new VPS:

```bash
#!/usr/bin/env bash
set -u
echo "== Distro / kernel =="; lsb_release -d 2>/dev/null; uname -r
echo "== Unattended-upgrades =="; systemctl is-active unattended-upgrades || true
echo "== UFW =="; sudo ufw status
echo "== fail2ban =="; sudo fail2ban-client status
echo "== Listening ports =="; sudo ss -tlnp
echo "== Recent root logins =="; sudo last -F root 2>/dev/null | head -10
echo "== Failed SSH (last 200) =="; sudo grep 'Failed password' /var/log/auth.log* 2>/dev/null | tail -20
echo "== Users with shell =="; awk -F: '$7 !~ /nologin|false/ {print $1, $7}' /etc/passwd
echo "== sudoers files =="; sudo ls -la /etc/sudoers.d/
echo "== Cron jobs =="; for u in $(cut -d: -f1 /etc/passwd); do sudo crontab -u "$u" -l 2>/dev/null | sed "s|^|[$u] |"; done
echo "== Pending updates =="; sudo apt list --upgradable 2>/dev/null | head -20
```

## Common follow-ups

- **Docker on the same VPS** → see [`docker-container-security`](../docker-container-security/SKILL.md) (planned). Note: Docker bypasses UFW by default; you need ufw-docker rules.
- **WordPress on this VPS** → see [`wordpress-hardening`](../wordpress-hardening/SKILL.md)
- **Behind Cloudflare** → see [`cloudflare-hardening`](../cloudflare-hardening/SKILL.md), and restrict ingress to Cloudflare's IPs in UFW

## What this skill will not do

- Replace a full CIS benchmark for regulated environments
- Help harden a server you do not own or operate
- Endorse `PermitRootLogin yes` or `PasswordAuthentication yes` on internet-facing SSH
