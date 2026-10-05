---
name: mac-smb-automount
description: Auto-mount another Mac's SMB shares on macOS at login and keep them mounted (LaunchAgent + NetFS), over Tailscale or LAN, authenticating with the shared Apple ID (Kerberos LKDC) so no password is stored. Use when mounting a Mac's shares automatically; when an SMB connection to a Mac prompts for a password or returns "Authentication error" despite the right password; when a mount agent keeps declaring healthy mounts stale; or when replacing local Dropbox/Google Drive sync clients with mounts of the server's copies.
---

# Auto-mount a Mac's SMB shares

Deploys `scripts/mount-smb-shares.sh` behind a LaunchAgent on the **client** Mac so the **server** Mac's shares sit at `/Volumes/<share>` after login and come back by themselves after sleep, network changes and server hiccups. Triggers: login, every 300 s, `/var/run/resolv.conf` changes, and every power-state change (`com.apple.powermanagement.systempowerstate`, the same event Time Machine's helper wakes on) so a wake from sleep remounts within seconds instead of waiting for the interval — which launchd stretches well past 5 min on battery. The script exits at once when the lid is closed, so dark wakes cost nothing. Both Macs signed into the same Apple ID is the normal case, and then no password exists anywhere in the setup.

## Facts every step rests on

- **Mounts happen at login, not boot.** NetFS needs the Aqua session (and, with FileVault, the unlocked login keychain), so the agent lives in `gui/<uid>`. A LaunchDaemon would mount as root, outside the user's namespace. With auto-login on and FileVault off, login follows boot unattended.
- **One hostname.** Address the server by its Tailscale MagicDNS name only. Tailscale takes the direct LAN path at home, so the same name works away with no switching logic.
- **NetFS, not `mount_smbfs`.** `/Volumes` is not user-writable; `osascript -e 'mount volume "smb://…"'` mounts there through the privileged agent and shows in Finder. It blocks **forever** when the server cannot authenticate the client, so the script caps it with a watchdog.
- **Probe with `smbutil statshares -m <mountpoint>`** (rc 0 live, 64 gone). Reading the directory from a LaunchAgent gets TCC's `Operation not permitted` while an interactive shell reads fine; an `ls` probe turns every healthy pass into an unmount/remount cycle.
- **SSH is the wrong context.** Over SSH, `mount volume` hangs, keychain writes are refused, and credential caches are invisible. Reach the GUI session instead: `sudo launchctl asuser <uid> sudo -u <user> -i <cmd>`.
- **FileProvider shares need a live GUI session on the server.** Dropbox and Google Drive folders under `~/Library/CloudStorage` mount fine but read empty while the server sits at the login window: server auto-login on, FileVault off (the `mac-mini-as-headless-server` skill covers that).

## Steps

### 1. Recon

Server: `sharing -l` (share names and paths); `dscl . -read /Users/<user> AltSecurityIdentities`.
Client: `nc -z -G 3 <host> 445`; `dscl . -read /Users/<user> AltSecurityIdentities`; `stat -f %Su /dev/console`.

Shares that a client sees beyond `sharing -l` are smbd's virtual shares (whole volumes, home folders); the `macos-smb-server` skill covers trimming them.

Done when the share names are known, port 445 answers on the Tailscale name, both accounts carry the same `com.apple.idms.appleid…` under `AltSecurityIdentities`, and the console owner is the user who will mount.

### 2. First silent mount

From the client's GUI session (a Terminal there, or the `asuser` form): `open "smb://<host>/<share>"`.

Done when `mount | grep smbfs` lists the share within seconds with no dialog, and `klist --list-all` in the GUI session shows a `com.apple.idms.appleid…` cache. A dialog, a hang, or `Authentication error` → [AUTH.md](AUTH.md), then return here. `pkill NetAuthAgent` clears a leftover dialog.

### 3. Install

`scripts/install.sh --host <fqdn> --user <server-account> --share <A> --share <B> …`

Done when every share is mounted, the log has one `mounted <share>` line per share, and `launchctl print gui/$(id -u)/<label>` reports `last exit code = 0`.

### 4. Verify

`scripts/verify.sh` (from a Terminal in the client's GUI session, or over SSH with passwordless sudo — it reaches the GUI session itself) — three checks, all must pass: two forced agent runs add 0 log lines (a healthy pass is silent); unmounting one share is repaired on the next run; `kdestroy -A` plus unmounting everything ends with all shares remounted silently and a fresh credential cache. A reboot is optional: it adds only boot-ordering evidence.

### 5. Retire local sync clients (branch)

Only when the shares are the server's Dropbox / Google Drive folders and the client runs its own copies: [RETIRE-SYNC-CLIENTS.md](RETIRE-SYNC-CLIENTS.md).

## Reading the log

`~/Library/Logs/mount-smb-shares.log` is silent while healthy. `host … unreachable; skipping this pass` is the designed skip: existing mounts are left alone through an outage. `FAILED to mount <X>` repeating for one share while the others mount is server-side — Dropbox auto-updating on the server takes its FileProvider down for a while — and clears by itself. Entries like `//com.apple.idms…@<host>/<user> on /Volumes/<user>` come from clicking the server under Finder → Network; `umount -f` them and connect by hostname.
