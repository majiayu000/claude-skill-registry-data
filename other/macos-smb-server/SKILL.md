---
name: macos-smb-server
description: Configure macOS's built-in SMB server (com.apple.smb.server) — settings apply only when committed via SCPreferences, never via defaults write. Use when a Mac's "Macintosh HD" or a home folder is visible to other machines on the LAN (virtual shares), when disabling guest access on file shares, when a com.apple.smb.server change doesn't take effect, or when proving server-side which shares a Mac offers.
---

# macOS SMB server (com.apple.smb.server)

Validated on macOS 26 (Darwin 25.6), Mac mini M2, 2026-08. Two facts drive everything here:

- **Virtual shares**: beyond the explicit sharepoints, smbd automatically offers every mounted
  volume to admin users ("Macintosh HD", external drives) and each authenticating user's own home
  folder. They never appear in System Settings or `sharing -l`, so they can't be removed there.
- **Commit, don't write**: smbd never reads
  `/Library/Preferences/SystemConfiguration/com.apple.smb.server.plist` off disk. A `defaults
  write` there is invisible until reboot. Changes apply only when committed through the
  SCPreferences API, whose commit fires the `com.apple.smb.preferences` launchd event that runs
  `/usr/libexec/smb-sync-preferences`.

## 1 — Classify what clients see

`sharing -l` lists the explicit sharepoints and their per-share guest flags. Anything a client
sees beyond that list is a virtual share. Done when every share visible from a client is
classified as sharepoint or virtual — the two are fixed by different mechanisms.

## 2 — Change settings

Sharepoints use the `sharing` tool directly, effective immediately: `sudo sharing -r <name>`
removes one, `sudo sharing -e <name> -g 000` turns off its guest access, `-a <path>` adds one.

Server-level keys go through an SCPreferences commit, then a restart:

    sudo swift scripts/smb-prefs.swift VirtualAdminShares=false VirtualHomeShares=false AllowGuestAccess=false
    sudo launchctl kickstart -k system/com.apple.smbd

| Key | Effect |
|---|---|
| `VirtualAdminShares` | every mounted volume offered to admin users |
| `VirtualHomeShares` | each user's home folder offered to that user |
| `AllowGuestAccess` | global guest switch (per-share guest flags still apply) |
| `NetBIOSName`, `ServerDescription` | identity shown to the network |

Values: `Key=true|false|delete|<string>`. Revert is the same commit with `true`. Without Swift
(no CLT), `sudo defaults write` on the plist plus a reboot also applies — the sync helper is
RunAtLoad. For keys beyond this table, ground truth is `strings /usr/sbin/smbd` and
`strings /usr/libexec/smb-sync-preferences`.

## 3 — Verify server-side, then client-side

The kickstart drops live sessions; clients auto-reconnect within seconds and re-request the trees
they had mounted, so the server's own log is the proof:

    log show --last 2m --predicate 'process == "smbd"' --info

`connect_to_named_tree status: 0xc00000cc` (STATUS_BAD_NETWORK_NAME) means the requested share is
no longer offered. Done server-side when each removed share is refused or absent from the log.

Clients lie: Finder resumes stale sessions and cached listings across smbd restarts. Have the
client eject its mounts (or Disconnect), reconnect, and confirm the fresh listing shows only the
intended sharepoints — that confirmation completes the task.
