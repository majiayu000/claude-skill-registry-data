---
name: backups-restore
description: "Use when backing up or restoring agent or server state. What to include (config, env files, state, keyring file, signer keys, skills), explicit-include archives, 3-2-1 copies, provider snapshots, encryption and a tested restore drill."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, backup, restore, server, security]
    related_skills: [hermes-gateway-server, server-agent-service, cron-timers, acp-troubleshooting, consent]
---

# Backups and restore — a backup counts only after a restore worked

## When to use
- Before an upgrade, a migration, a rebuild, or any change the owner cannot undo.
- On a schedule for every server that runs an agent.
- When state was lost and must come back.

`tar`, `rsync`, `sqlite3`, `sha256sum`, `gpg` and `age` are system or third-party tools: their man pages are the truth.

## Prerequisites
- A `<backup-dir>` with mode 700 owned by the service user, and a second place off the host (`ssh-access` alias, object storage).
- Writing archives needs `fileWriting`; a restore overwrites state: ask through the consent door (`~/.iclone-os/bin/acp consent request fileWriting --reason "…"`), name what will be replaced, and wait for the owner's yes. A scheduled backup also needs `scheduledTasks` (`cron-timers`).

## Quick reference — what to include
| Item | Typical place | Note |
|---|---|---|
| Hermes home | `~/.hermes` | `hermes backup` zips it |
| Env files | `/etc/<agent>/*.env`, `.env` | secrets: encrypt before it leaves the host |
| State DBs | `<state-dir>/*.db` | copy with `sqlite3 .backup`, not `cp` of a live file |
| acp CLI config + keyring file | the `ACP_CONFIG_DIR` in use, `~/.config/keyring` | needed to stay logged in |
| Signer keys | `~/.local/share/acp-cli/signer-keys.json` | same machine only (acp-troubleshooting E3) |
| Units, timers, crontabs | `/etc/systemd/system/<agent>*`, `crontab -l` | rebuild the box in minutes |
| Custom skills, code not in git | `<agent-dir>` | — |

Leave out what can be rebuilt (venvs, `node_modules`, caches) by listing what you include, never by excluding whole trees: excluding `~/.local` as "cache" once lost the signer keys.

## Procedure
1. Hermes home (any machine):
```sh
f=<backup-dir>/hermes-$(date +%F).zip && hermes backup -o "$f" && chmod 600 "$f"  # example
```
2. Live SQLite databases:
```sh
sqlite3 <state-dir>/<name>.db ".backup '<backup-dir>/<name>.db'"  # example
```
3. Everything else from an explicit list (`<include-list>` holds one path per line, relative to `/`). `tar` writes to stdout and your shell creates the file, so the archive is yours and step 4's `chmod` works:
```sh
sudo tar -czf - -C / --files-from=<include-list> > <backup-dir>/<agent>-$(date +%F).tgz  # example
```
4. Checksum and encrypt anything that holds secrets, then lock the files:
```sh
cd <backup-dir> && sha256sum <archive> > <archive>.sha256 && chmod 600 <archive> <archive>.sha256  # example
gpg --symmetric --cipher-algo AES256 <archive>  # example
```
On macOS use `shasum -a 256` where this skill says `sha256sum` (same file format, same `-c`). Hermes zips hold the `.env` too: encrypt them the same way. The owner types the passphrase and keeps it in their password manager, never next to the archive. Only the `.gpg` files leave the host.
5. Copy off the host (3-2-1: three copies, two kinds of storage, one elsewhere). A provider snapshot is one copy, not the whole plan: it lives in the same account.
```sh
chmod 700 <backup-dir> && chmod 600 <backup-dir>/*.gpg <backup-dir>/*.sha256  # example
rsync -a --chmod=go-rwx --include='*.gpg' --include='*.sha256' --exclude='*' <backup-dir>/ <alias>:<remote-backup-dir>/  # example
```
   The local `chmod` is what keeps the copy private: `rsync -a` carries the 600 files and the 700 `<backup-dir>` (the trailing `/`) to the remote dir, on GNU rsync and on macOS openrsync alike. Do not rely on `--chmod` alone (openrsync accepts it but may not apply it; it rejects `F600,D700`).
6. Restore drill, at least once per setup and after every change to the list. Test the copy that survives a lost host: fetch the off-host `.gpg` into a scratch dir (never over live state), decrypt it (the owner types the passphrase), check it, extract it:
```sh
umask 077 && mkdir -p <scratch-dir> && cd <scratch-dir>  # example
rsync -a <alias>:<remote-backup-dir>/<archive>.gpg <alias>:<remote-backup-dir>/<archive>.sha256 ./  # example
gpg -d -o <archive> <archive>.gpg  # example
sha256sum -c <archive>.sha256 && tar -xzf <archive> -C <scratch-dir>  # example
```
   A Hermes zip is checked the same way, then listed with `unzip -l <archive>`.
7. Real restore (owner's yes): stop the service → move the current state aside (never delete it) → extract → fix owners and modes (env files 0600) → start → verify. Hermes homes come back with `hermes import <zip>`.

## Pitfalls
- A backup never restored is a hope. Record the date of the last successful drill.
- Restoring tokens or a signer onto a second machine while the first still runs breaks both (acp-troubleshooting E14, E17).
- `tar` of a database that is being written gives a corrupt copy; use step 2 or stop the service.
- Backups readable by everyone leak every secret in them.

## Never
- Never send unencrypted secrets off the host.
- Never restore over live state without moving it aside first, and never delete the only copy.
- Never use `hermes import --force` or overwrite files without the owner's yes.

## Verification
Run in `<scratch-dir>` right after the drill (step 6):
```sh
sha256sum -c <archive>.sha256 && tar -tzf <archive> | wc -l && wc -l < <include-list>  # example
ssh <alias> "ls -la <remote-backup-dir>"  # example
```
Pass = `<archive>: OK`, a file count of at least the include-list lines (a listed directory adds its contents), one listed file read back from `<scratch-dir>` with the expected content, and the remote listing shows only `.gpg`/`.sha256` files, `-rw-------`, in a `drwx------` dir.
Delete `<scratch-dir>` only after this check: it holds decrypted secrets.
