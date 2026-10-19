---
name: linux-hardening
description: >
  Apply defense-in-depth system hardening measures across Linux servers and services.
  Use when securing OpenSSH configurations (/etc/ssh/sshd_config), sandboxing systemd
  services with ProtectSystem/NoNewPrivileges, configuring host firewalls with ufw/nftables,
  enforcing auditd logging, or checking system compliance with Lynis.
compatibility: >
  Agent Skills-compatible coding agents administering Linux servers with root/sudo access.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "linux, hardening, security, ssh, systemd-sandboxing, ufw, auditd, selinux"
  topics: "security, operating-systems, devops"
---

# Linux System Hardening & Security Baselines

Linux system hardening applies defense-in-depth controls across operating system layers to reduce the attack surface, prevent privilege escalation, isolate daemon services, and log security events. Follow the CIS (Center for Internet Security) Linux Benchmarks.

## Core Rules

1. **Disable SSH Password Authentication**: Enforce public-key authentication (`ed25519` keys only) and disable root login via SSH (`PermitRootLogin no`).
2. **Default Deny Firewall Policy**: Configure host firewalls (`ufw` or `nftables`) to drop all incoming traffic by default, explicitly opening only required service ports.
3. **Sandbox all custom systemd units**: Use systemd security flags (`ProtectSystem=strict`, `NoNewPrivileges=yes`, `PrivateTmp=yes`) to isolate services from the underlying OS.
4. **Enforce automatic security patching**: Configure `unattended-upgrades` on Debian/Ubuntu or `dnf-automatic` on RHEL/Fedora for automatic kernel and security fixes.
5. **Never disable SELinux or AppArmor**: If access is denied, inspect audit logs (`ausearch -m avc -ts recent`) and generate a targeted policy rule rather than setting permissive mode.

---

## 1. Hardened OpenSSH Configuration (`/etc/ssh/sshd_config.d/99-hardened.conf`)

```ini
# Disallow remote root login
PermitRootLogin no

# Enforce public-key authentication; disable insecure passwords
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes

# Disallow empty passwords
PermitEmptyPasswords no

# Modern, secure cryptographic key exchange & cipher suites
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com

# Disable unused legacy features
X11Forwarding no
AllowTcpForwarding no
AllowAgentForwarding no

# Connection timeout and alive checks
ClientAliveInterval 300
ClientAliveCountMax 2
MaxAuthTries 3
```

Validate and reload SSH:
```bash
# Test sshd syntax before restarting!
sudo sshd -t
sudo systemctl reload sshd
```

---

## 2. Host Firewall Configuration with `ufw`

```bash
# 1. Set default policies: block incoming, allow outgoing
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. Allow SSH (always do this before enabling to avoid lockouts!)
sudo ufw allow 22/tcp comment "SSH administration"

# 3. Allow specific service ports
sudo ufw allow 443/tcp comment "HTTPS Web Traffic"

# 4. Enable firewall
sudo ufw --force enable
sudo ufw status verbose
```

---

## 3. Sandboxing Services in systemd

Evaluate the security posture of any service using `systemd-analyze`:

```bash
# Score security exposure from 0 (very secure) to 10 (unhardened)
systemd-analyze security nginx.service
```

Key hardening directives for `/etc/systemd/system/<service>.service`:
```ini
[Service]
# User and permissions
User=appuser
Group=appuser
NoNewPrivileges=yes

# Filesystem sandboxing
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
PrivateDevices=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true

# Read-write exceptions
ReadWritePaths=/var/log/app /tmp

# Network sandboxing (if service does not need network)
# PrivateNetwork=yes
```

---

## 4. Kernel Hardening via Sysctl (`/etc/sysctl.d/99-security.conf`)

```ini
# Disable IP packet forwarding (unless this is a router)
net.ipv4.ip_forward = 0

# Ignore ICMP broadcast requests (prevent Smurf attacks)
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Enable TCP SYN Cookies to defend against SYN flood attacks
net.ipv4.tcp_syncookies = 1

# Disable ICMP redirect acceptance
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0

# Restrict dmesg access to root only
kernel.dmesg_restrict = 1

# Hide kernel pointers from unprivileged users
kernel.kptr_restrict = 2
```

Apply immediately:
```bash
sudo sysctl --system
```

---

## 5. Security Auditing with Lynis

```bash
# Run comprehensive automated system security audit
sudo lynis audit system --quick
```

---

## 6. Verification Checklist

- [ ] `sshd -t` confirms clean configuration; password authentication disabled.
- [ ] Firewall active with default deny incoming policy (`ufw status`).
- [ ] SELinux in `Enforcing` or AppArmor in `enforce` mode.
- [ ] Custom services run as non-root with `ProtectSystem=strict`.
- [ ] `sysctl` hardening parameters verified active.
