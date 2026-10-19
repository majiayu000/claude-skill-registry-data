---
name: linux-permissions
description: >
  Manage POSIX file permissions, ACLs, umask, special bits (SUID, SGID, Sticky),
  and Linux capabilities following the principle of least privilege. Use when
  resolving permission denied errors, securing sensitive files and keys,
  configuring shared group directories, or auditing system security boundaries.
compatibility: >
  Agent Skills-compatible coding agents operating in a Linux environment
  with standard coreutils and administrative tool access.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "linux, permissions, security, chmod, chown, acl, capabilities"
  topics: "operating-systems, security, devtools"
---

# Linux Permissions and Access Control

Linux security relies on strict file access controls to isolate processes, protect sensitive data, and enforce the principle of least privilege. This skill covers standard POSIX permissions, octal modes, special bits, extended Access Control Lists (ACLs), and Linux capabilities.

## Core Rules

1. **Least Privilege**: Grant only the minimal permissions required for a user or process to fulfill its function.
2. **Never use `chmod 777` as a fix**: Full write-and-execute permissions for everyone creates critical security vulnerabilities and masks underlying ownership or group misconfigurations.
3. **Protect private keys and credentials**: Secret files (e.g., SSH private keys, `.env` files) must be readable only by their owner (`chmod 600` or `400`).
4. **Be cautious with recursive changes**: Never run `chmod -R` or `chown -R` on system root (`/`) or system directories (`/etc`, `/usr`, `/var`).
5. **Special bits carry high risk**: SUID on executables allows execution with the owner's privileges (often root). Never set SUID on scripts or untrusted binaries.

---

## 1. POSIX Permissions and Octal Representation

Every filesystem entry has three access scopes: **Owner (u)**, **Group (g)**, and **Others (o)**.
Each scope can possess three permissions:
- `r` (Read): Value `4`. Read file contents / list directory entries.
- `w` (Write): Value `2`. Modify file contents / create or delete directory entries.
- `x` (Execute): Value `1`. Run executable binary or script / traverse into directory (`cd`).

### Standard Octal Modes

| Octal | Permission String | Common Use Case |
| :--- | :--- | :--- |
| `600` | `-rw-------` | Private files (SSH keys, credentials, database passwords) |
| `644` | `-rw-r--r--` | Standard public/shared files (documentation, source code) |
| `700` | `drwx------` | Private directories (`~/.ssh`, user scratch dirs) |
| `755` | `-rwxr-xr-x` / `drwxr-xr-x` | Executable binaries/scripts; standard traversable directories |
| `775` | `drwxrwxr-x` | Collaborative group directories with write access for group members |

### Practical Commands
```bash
# Set specific file permissions
chmod 600 ~/.ssh/id_ed25519

# Make a script executable for owner and group only
chmod 750 deploy.sh

# Change ownership and group
chown deployer:www-data /var/www/app/config.json

# Apply permissions selectively (files vs directories)
# Ensure directories are 755 and regular files are 644 without breaking directory traversal:
find /var/www/html -type d -exec chmod 755 {} +
find /var/www/html -type f -exec chmod 644 {} +
```

---

## 2. Special Bits: SUID, SGID, and Sticky Bit

Special permission bits modify default execution and inheritance behavior:

### SUID (Set User ID — `4000`)
- Displayed as `rws` or `rwS` in owner position.
- When an executable with SUID runs, it executes with the privileges of the file owner (e.g., `/usr/bin/passwd` runs as root).
- **Rule**: Never set SUID on shell scripts (Linux kernels ignore SUID on interpreted scripts for security).

### SGID (Set Group ID — `2000`)
- On files: runs with group privileges of the file.
- **On directories (`chmod 2775 <dir>` or `chmod g+s <dir>`)**: Every new file or sub-directory created inside inherits the directory's group instead of the creating user's primary group. Crucial for team shared folders!

### Sticky Bit (`1000`)
- Displayed as `rwt` in others position (e.g., `/tmp` has mode `1777`).
- On directories (`chmod +t <dir>`): Users can only delete or rename files that they own, even if the directory has general write permissions.

---

## 3. POSIX Access Control Lists (ACLs)

When standard Owner/Group/Other is too coarse (e.g., giving user `alice` read access and user `bob` write access without changing group ownership), use ACLs:

```bash
# View active ACLs on a file
getfacl config.yaml

# Grant user 'developer' read and write access
setfacl -m u:developer:rw config.yaml

# Grant group 'auditors' read-only access
setfacl -m g:auditors:r config.yaml

# Set default ACL on a directory (inherited by newly created files)
setfacl -d -m g:auditors:r /var/log/audit/

# Remove all extended ACLs
setfacl -b config.yaml
```

---

## 4. Linux Capabilities: Splitting Root Privileges

Instead of granting full root via SUID, Linux capabilities divide root privileges into distinct units:

```bash
# Allow a binary (e.g., custom web server) to bind to low ports (< 1024) without running as root:
sudo setcap 'cap_net_bind_service=+ep' /opt/app/bin/server

# Check capabilities on a binary
getcap /opt/app/bin/server

# Remove capabilities
sudo setcap -r /opt/app/bin/server
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Security Risk | Correct Practice |
| :--- | :--- | :--- |
| `chmod 777 <file>` | Allows any local user or compromised service to modify/inject code | Identify required user/group, set `640` or `750` |
| SSH key with mode `644` | OpenSSH client will refuse to connect (`UNPROTECTED PRIVATE KEY FILE!`) | Set SSH private keys to `chmod 600` |
| `chmod -R 755` on source tree | Makes data files, READMEs, and config files executable | Separate `find ... -type d` from `find ... -type f` |
| Running web applications as root | System compromise on remote code execution | Run as dedicated unprivileged service account (`www-data`, `app`) |

---

## 6. Real-World Troubleshooting Scenarios

### Scenario A: Resolving "Permission Denied" in a Shared Deployment Directory
Users `ci-bot` and `lead-dev` both need to write files into `/opt/releases/`. Currently, files created by `ci-bot` cannot be modified by `lead-dev`.

```bash
# 1. Create or verify common group
sudo groupadd -f release-team
sudo usermod -aG release-team ci-bot
sudo usermod -aG release-team lead-dev

# 2. Assign directory ownership and SGID bit
sudo chown -R ci-bot:release-team /opt/releases
sudo chmod 2775 /opt/releases

# 3. Set default ACL so new files are group-writable automatically
sudo setfacl -d -m g:release-team:rwx /opt/releases
```

### Scenario B: Auditing World-Writable Files
Locate insecure files that any user on the system can tamper with:

```bash
# Find world-writable regular files excluding /proc, /sys
find / -xdev -type f -perm -0002 2>/dev/null
```

---

## 7. Verification Checklist

- [ ] Private credentials have restrictive permissions (`600` or `400`).
- [ ] No regular files have inappropriate execute bits set.
- [ ] No unverified files have world-writable mode (`777` or `o+w`).
- [ ] Group collaboration directories have SGID (`2775`) set.
- [ ] Access controls match the principle of least privilege.
