---
name: security-review
description: Perform a structured security review of proposed or staged HomeLab changes before merge or deployment.
---
# Security review
Review: secret/key/state leakage into the public repository; new ports, their bind address and the overlay guard; firewall scope; SSH/WireGuard/TLS/auth; container privilege, mounts and the Docker socket (CI runner); secrets on command lines or in Ansible output; Vault and ansible-vault handling; database binding and auth; image pinning; destructive commands; backup and recovery impact. Use the security-reviewer agent where useful. Output severity, evidence, impact, minimal remediation, residual risk, and pass / pass-with-notes / block.
