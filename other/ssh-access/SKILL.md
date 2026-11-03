---
name: ssh-access
description: "Use when creating SSH keys or an ssh alias for a host. Ed25519 keys with a passphrase, installing the public key, a ~/.ssh/config Host block, 700/600 permissions, agent forwarding caution, rotation, and never showing a private key."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, ssh, keys, security, server]
    related_skills: [vps-provision, server-troubleshooting, consent, github]
---

# SSH access — keys and aliases done safely

## When to use
- The owner needs to reach a server (new VPS, a rebuilt host, a second machine) or wants a short alias for it.
- A key must be rotated, or a login fails with `Permission denied (publickey)`.

For GitHub keys use the `github` skill (`references/auth.md`). `ssh`, `ssh-keygen`, `ssh-copy-id` are system tools: their man pages are the truth.

## Prerequisites
- OpenSSH client (built into macOS and Linux).
- Creating keys or editing `~/.ssh` writes files: ask through the consent door (`~/.iclone-os/bin/acp consent request fileWriting --reason "…"`), say which file, and wait for the owner's yes. Commands on a server also need `terminal`.

## Quick reference
| Item | Rule |
|---|---|
| Type | `ed25519` (RSA only for legacy hosts, 4096 bits) |
| Passphrase | yes for personal keys; typed by the owner, never by you |
| Files | `~/.ssh` 700 · private key and `config` 600 · `.pub` 644 |
| One key per purpose | personal login ≠ deploy key ≠ CI key |
| Alias | `Host <alias>` block with `IdentitiesOnly yes` |

## Procedure
1. Look for an existing key before making a new one:
```sh
ls -l ~/.ssh/*.pub  # example
```
2. Create the key. The owner types the passphrase at the prompt; never pass one with `-N` on the command line (it lands in shell history):
```sh
ssh-keygen -t ed25519 -a 100 -C "<label>" -f ~/.ssh/<key-name>  # example
```
On macOS, store the passphrase in the login keychain once:
```sh
ssh-add --apple-use-keychain ~/.ssh/<key-name>  # example
```
3. Put the PUBLIC key on the server — in the provider panel for a new server, or over a login that already works:
```sh
ssh-copy-id -i ~/.ssh/<key-name>.pub <user>@<server-ip>  # example
```
4. Add the alias to `~/.ssh/config` (append; never rewrite the owner's existing blocks):
```
# example — man ssh_config is the truth
Host <alias>
  HostName <server-ip>
  User <user>
  IdentityFile ~/.ssh/<key-name>
  IdentitiesOnly yes
  ServerAliveInterval 30
  ForwardAgent no
```
On macOS add `UseKeychain yes` and `AddKeysToAgent yes` to the block.
5. Fix permissions (ssh refuses keys that others can read):
```sh
chmod 700 ~/.ssh && chmod 600 ~/.ssh/config ~/.ssh/<key-name> && chmod 644 ~/.ssh/<key-name>.pub  # example
```
6. Test without prompts:
```sh
ssh -o BatchMode=yes <alias> true; echo $?  # example
```
7. Rotate: create the new key (step 2) → append its `.pub` to `~/.ssh/authorized_keys` on the server → log in with the new key in a new session → only then remove the old line from `authorized_keys` → update `IdentityFile` → delete the old local key with the owner's yes.

## Pitfalls
- `Too many authentication failures`: the agent offered every key; `IdentitiesOnly yes` fixes it.
- `REMOTE HOST IDENTIFICATION HAS CHANGED`: stop. Ask the owner whether the server was rebuilt. Only then run `ssh-keygen -R <server-ip>` and accept the new fingerprint shown in the provider console.
- `ForwardAgent yes` lets anyone with root on that host use your keys while you are connected; prefer `ProxyJump` for bastions.
- A server that must pull from GitHub gets its own deploy key created ON the server, never a copy of a personal key.

## Never
- Never print, read aloud, upload or copy a private key (any file in `~/.ssh` without `.pub`).
- Never set `StrictHostKeyChecking no` or `UserKnownHostsFile /dev/null`.
- Never delete a key or an `authorized_keys` line before the replacement login works.

## Verification
```sh
ssh -G <alias> | grep -E '^(hostname|user|identityfile|identitiesonly) ' && ssh -o BatchMode=yes <alias> true && echo ok  # example
```
Pass = the resolved values match the block and the last command prints `ok` (exit code 0).
