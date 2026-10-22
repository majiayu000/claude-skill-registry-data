---
name: ssh-doctor
description: >-
  Triages SSH on macOS: Remote Login settings, launchd sshd, connections closed before auth, and stale
  sessions. Use when SSH to a Mac connects then drops, Remote Login looks enabled but is unusable, or
  Mac SSH needs diagnosis.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
platform: macos
license: MIT
---

# SSH Doctor

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

Use when SSH connects then closes before auth, Remote Login seems advertised but unusable, or Mac SSH needs diagnosis.

## Rules

- Do not print secrets, tokens, full env, or broad secret grep output.
- Validate locally first: loopback failure means server-side sshd/launchd/config; loopback success plus remote failure means network/firewall/filter/listen path.
- Report suspicious config lines before changing `/etc/ssh/sshd_config`.
- Prefer non-interactive SSH:

```bash
ssh -o RequestTTY=no -o RemoteCommand=none HOST 'hostname; id -un'
```

## Baseline

```bash
hostname; id -un; sw_vers
ipconfig getifaddr en0
sudo systemsetup -getremotelogin
sudo systemsetup -setremotelogin on
sudo launchctl print system/com.openssh.sshd 2>&1 | head -80
sudo launchctl kickstart -k system/com.openssh.sshd
sudo lsof -nP -iTCP:22 -sTCP:LISTEN
nc -vz 127.0.0.1 22
ssh -4 -F /dev/null -o RequestTTY=no -o RemoteCommand=none USER@127.0.0.1 'hostname; id -un'
```

## Config Audit

```bash
sudo sshd -T 2>&1 | egrep -i '^(allowusers|denyusers|allowgroups|denygroups|listenaddress|maxstartups|logingracetime|usepam|passwordauthentication|pubkeyauthentication|authenticationmethods)'
sudo egrep -n '^[[:space:]]*(AllowUsers|DenyUsers|AllowGroups|DenyGroups|Match|MaxStartups|LoginGraceTime|ListenAddress|AuthenticationMethods|UsePAM|PasswordAuthentication|PubkeyAuthentication)\b' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/* 2>/dev/null || true
```

Suspicious:
- `DenyUsers` matching target user
- Restrictive `AllowUsers` / `AllowGroups`
- `Match` block accidentally applying
- Tiny `MaxStartups` or `LoginGraceTime`
- `ListenAddress` missing target interface

## Logs

```bash
sudo log show --last 30m --predicate 'process == "sshd" OR process == "launchd"' --style compact | tail -160
```

## Stale sshd-session Fix

Inspect first:

```bash
sudo launchctl print system/com.openssh.sshd 2>&1 | egrep 'active count|copy count|state =|last exit code|runs ='
ps -axo pid,ppid,uid,user,state,lstart,etime,comm,args | awk '/sshd-session:/ && !/awk/ {print}'
```

If stale sessions are blocking new SSH:

```bash
ps -axo pid=,args= | awk '/sshd-session: / && !/awk/ {print $1}' | xargs sudo kill -TERM
sleep 2
ps -axo pid=,args= | awk '/sshd-session: / && !/awk/ {print}'
```

## Firewall (remote failure only)

Only after loopback works but remote fails:

```bash
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
sudo lsof -nP -iTCP:22 -sTCP:LISTEN
```

## Closeout

Report:
- Root cause
- Exact commands changed
- Validation output, redacted as needed
- Whether remote should retry
