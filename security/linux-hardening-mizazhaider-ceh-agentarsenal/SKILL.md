---
name: linux-hardening
description: Use when hardening a Linux server for production, when locking down SSH with key-only authentication, when writing a default-deny firewall with ufw or nftables, when disabling unneeded services, when enabling automatic security updates, when adding auditd rules for sensitive files, and when running a CIS-style checklist adapted for small teams.
version: 1.0.0
domain: linux
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [privesc-linux]
tools:
  - name: openssh
    version: "9.6"
  - name: ufw
    version: "0.36"
  - name: nftables
    version: "1.0"
---

This skill covers practical Linux server hardening for small teams: SSH lockdown, default-deny firewalling, service minimization, automatic security updates, and basic auditing, finished with a CIS-style checklist you can run on every new box. The scope is a single general-purpose server (Debian/Ubuntu and RHEL families). It is hardening, not incident response: if you suspect the box is already compromised, isolate and investigate first instead of hardening around an attacker. It pairs with privesc-linux, which shows what an attacker does with the misconfigurations this skill removes.

## Quick Workflow

1. Inventory the box: OS version, listening ports, enabled services, user accounts.
2. Harden SSH: key-only authentication, no root login, strong algorithms, limited users. Verify with `sshd -T`.
3. Firewall: default deny inbound, allow only the ports the box actually serves.
4. Minimize: disable and mask unneeded services and sockets.
5. Updates: enable automatic security updates with a planned reboot strategy.
6. Audit: add auditd watches on sensitive files, keep logs persistent and shipped off-box.
7. Verify: re-run the inventory, walk the checklist, and sign off.

## Phase 1: Inventory

You cannot harden what you have not listed. Run this on every box before changing anything, and keep the output as your baseline.

```bash
cat /etc/os-release | head -3
ss -tlnp                                   # listening TCP ports and owning processes
systemctl list-unit-files --state=enabled  # what starts at boot
awk -F: '$3==0{print $1}' /etc/passwd      # accounts with UID 0 (should be only root)
lastlog -b 30                              # accounts with recent logins
sudo -l                                    # who can run what as root
```

Any listening port you cannot explain is a finding. Any UID 0 account besides root is a finding. Any enabled service you do not recognize gets investigated before it gets disabled.

## Phase 2: SSH hardening

SSH is the front door. Lock it down in a drop-in config file so package updates never clobber your settings.

```bash
cat > /etc/ssh/sshd_config.d/99-hardening.conf <<'EOF'
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
MaxAuthTries 3
LoginGraceTime 30
MaxSessions 3
AllowUsers deploy
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512
EOF
sshd -t && systemctl reload sshd
sshd -T | grep -Ei 'permitrootlogin|passwordauthentication|kbdinteractive|allowusers'
```

Rules: key-only authentication (password auth off entirely), root login disabled, `AllowUsers` limited to the accounts that need shell access, weak algorithms removed. Always test from a second SSH session before closing your first one. If the box must expose SSH to the internet, add rate limiting (a firewall rule or fail2ban-style limiter) on top.

```bash
ssh -v deploy@host 2>&1 | grep -i "authenticat"   # confirm key auth is offered and used
```

## Phase 3: Firewall, default deny

Default deny inbound, explicit allow for what the box serves. Two common toolsets; pick the one your distro uses.

ufw (Debian/Ubuntu):

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 443/tcp
ufw enable
ufw status verbose
```

nftables (direct ruleset, works everywhere):

```bash
nft add table inet filter
nft add chain inet filter input '{ type filter hook input priority 0; policy drop; }'
nft add rule inet filter input ct state established,related accept
nft add rule inet filter input iif lo accept
nft add rule inet filter input tcp dport 22 accept
nft add rule inet filter input tcp dport 443 accept
nft list ruleset
```

Verify from outside the box, not just from the box itself:

```bash
ss -tlnp | grep -v "127.0.0.1"     # what is reachable from the network
```

Rules: no management ports exposed to the world except through a VPN or bastion. Database ports listen on localhost or a private network only. Document every allowed port and why it exists; an undocumented allow rule is a future incident.

## Phase 4: Service minimization

Every running service is attack surface. Disable what the box does not need, and mask sockets that could be socket-activated back to life.

```bash
systemctl list-unit-files --state=enabled | grep -Ei "avahi|cups|bluetooth|telnet|rpcbind|nfs"
systemctl disable --now avahi-daemon cups bluetooth
systemctl mask telnet.socket
systemctl list-sockets --all | head -20
```

Keep a short list of what stays and why (ssh, your app, logging, updates). Revisit the list after every major change to the box's role. On containers and minimal images this phase is short; on full server installs it is where most of the wins are.

## Phase 5: Security updates

Unpatched services are the most common initial access vector. Automate security updates; plan reboots for kernel updates.

Debian/Ubuntu:

```bash
apt install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
grep -r "Unattended-Upgrade" /etc/apt/apt.conf.d/50unattended-upgrades | head -5
```

RHEL family:

```bash
dnf install -y dnf-automatic
systemctl enable --now dnf-automatic.timer
grep apply_updates /etc/dnf/automatic.conf
```

Rules: automatic security updates on, with alerts on failure. Decide the reboot policy up front (automatic in a maintenance window, or manual with a calendar reminder); an unrebooted kernel update is not an applied update. Check monthly that the automation actually ran: `grep -i unattended /var/log/unattended-upgrades/*.log` or the dnf-automatic equivalent.

## Phase 6: Auditing and logging

Watch the files attackers touch first, keep logs persistent across reboots, and ship them off the box so a compromise cannot erase its own trail.

```bash
apt install -y auditd || dnf install -y audit
cat > /etc/audit/rules.d/hardening.rules <<'EOF'
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/sudoers -p wa -k sudoers
-w /etc/sudoers.d/ -p wa -k sudoers
-w /etc/ssh/sshd_config -p wa -k sshd
-w /etc/shadow -p wa -k identity
EOF
augenrules --load
auditctl -l | head -20
aureport --summary | head -20
```

Also: make journald persistent (`Storage=persistent` in journald.conf), forward logs to a central server or at least a separate append-only location, and set log rotation so auditd cannot fill the disk (`max_log_file` in auditd.conf plus monitoring on disk space).

Suspicious-change checks to run on a schedule:

```bash
find / -xdev -type f -perm -0002 2>/dev/null | head      # world-writable files
find / -xdev -type f -perm -4000 2>/dev/null            # SUID binaries: know each one
awk -F: '($2=="") {print $1}' /etc/shadow 2>/dev/null   # accounts with empty password
```

## Phase 7: CIS-style checklist for small teams

CIS Benchmarks are the industry reference; this is the subset a small team can actually run per box. Check each line, record the result, fix failures.

| # | Control | Check command | Expected |
|---|---|---|---|
| 1 | Only root has UID 0 | `awk -F: '$3==0{print $1}' /etc/passwd` | `root` only |
| 2 | No empty passwords | `awk -F: '($2==""){print $1}' /etc/shadow` | no output |
| 3 | SSH root login off | `sshd -T \| grep -i permitrootlogin` | `no` |
| 4 | SSH password auth off | `sshd -T \| grep -i passwordauthentication` | `no` |
| 5 | Firewall default deny in | `ufw status verbose` or `nft list ruleset` | deny/drop default |
| 6 | No unexpected listeners | `ss -tlnp` | every port documented |
| 7 | Unneeded services off | `systemctl list-unit-files --state=enabled` | only required ones |
| 8 | Security updates automatic | service status of unattended-upgrades / dnf-automatic.timer | active |
| 9 | auditd running with rules | `auditctl -l` | watches from Phase 6 |
| 10 | No world-writable files | `find / -xdev -type f -perm -0002` | none outside /tmp |
| 11 | SUID binaries known | `find / -xdev -type f -perm -4000` | each one justified |
| 12 | Logs persistent and shipped | journald.conf, forwarder status | persistent, off-box copy |

Run the checklist on every new box before it serves traffic, and re-run it quarterly. Drift happens; the checklist catches it.

## Edge cases

- Locking yourself out of SSH: always verify from a second session before closing the first. Keep provider console or serial access credentials somewhere you can reach without SSH.
- Firewall blocking monitoring, backups, or config management: allowlist those source IPs explicitly and document why each exception exists.
- auditd filling the disk: set `max_log_file`, enable rotation, and alert on disk usage. A full disk is its own outage.
- Disabling IPv6 carelessly: some services bind v6 by default. Test before committing, or firewall v6 identically instead of disabling it.
- `AllowUsers` typos: one wrong username locks out a legitimate admin. Verify with `sshd -T | grep allowusers` and a test login.
- Hardened algorithms breaking old clients: check which clients connect before removing legacy key exchange. Prefer upgrading the client over keeping weak algorithms.

## Escalation

- Locked out of SSH: use the provider console, serial console, or rescue boot to fix `sshd_config`, then `sshd -t` before reloading.
- Legitimate traffic blocked by the firewall: add a temporary logging rule, identify the exact port and source, then add a targeted allow. Do not open broad ranges "to make it work".
- A service breaks after minimization: check `journalctl -u <service>` and re-enable only what the role needs. The checklist documents what stays for a reason.
- You find signs of compromise (unknown UID 0 accounts, unexpected listeners, altered binaries): stop hardening. Isolate the box, preserve logs and disk image, and switch to incident response. Hardening around an active attacker just warns them.

## Detection and defender view

For engineering skills this section covers detecting hardening misuse and configuration drift.

- Misconfiguration signals: `PasswordAuthentication yes`, `PermitRootLogin yes`, empty firewall ruleset, auditd not running, security updates disabled or failing silently.
- Detect drift automatically: a nightly script that diffs `sshd -T`, `nft list ruleset` (or `ufw status`), and the enabled-services list against the signed-off baseline. Any diff pages someone.
- Detect attacker-relevant changes: alerts on new UID 0 accounts, new SUID binaries, new listening ports, and auditd rule tampering. These are the exact primitives privesc-linux teaches; watching them is defense.
- Misuse: shared root passwords instead of personal keys, keys generated once and never rotated, `NOPASSWD` sudo for broad groups, exceptions to the firewall that nobody remembers approving. Review exceptions quarterly and expire them.

## Key references

- sshd_config man page and OpenSSH security notes (openssh.com, man sshd_config)
- nftables wiki: ruleset basics and examples (wiki.nftables.org)
- ufw manual (man ufw, Ubuntu Server Guide firewall section)
- CIS Benchmarks for Linux distributions, concept and control structure (cisecurity.org)
- auditd documentation: auditctl, audit.rules, aureport (man pages, distro docs)

## See also

- `linux-hardening-baseline`: Use it instead when hardening must become a repeatable fleet baseline, with benchmark selection, verification, and monitoring.
- `linux-container-hardening`: Use it instead when the target is a container runtime, not a host server.
