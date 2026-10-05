---
name: mac-mini-as-headless-server
description: Use when setting up a Mac (especially Mac Mini or Apple Silicon Mac Studio) for unattended 24/7 server operation, headless use, or remote-only access. Covers sleep prevention, screen saver, Wake-on-LAN, auto-restart, App Nap, SSH enablement, and — on Apple Silicon — a caffeinate LaunchDaemon that stops the headless display from parking (physical panel and VNC/screen-share going black even with displaysleep=0). Targets macOS 15 (Sequoia) and later.
---

# Configure macOS for Server Use

## Overview

Configures macOS for unattended 24/7 server operation by disabling sleep, screen saver, and App Nap, while enabling Wake-on-LAN, auto-restart after power failure, and SSH remote login. The screen lock lives in the user keybag and changing it requires the user's account password (root alone can't), so the script verifies it, offers to turn it off when run interactively (you type the user's password once), and prints the exact CLI/GUI fix on unattended runs.

**Requires `sudo`. Targets macOS 15 (Sequoia) and later.** Target hardware: Mac Mini, Mac Studio, or any Mac used as a headless server.

**Apple Silicon caveat:** on an Apple Silicon Mac with no local keyboard/mouse, `pmset displaysleep 0` is *not* enough. WindowServer still *parks* the physical display (DPMS off ~30s after each wake), which turns the panel black **and** makes RealVNC / screen-capture sessions show black, because they capture the physical display. The only reliable fix is to hold a `PreventUserIdleDisplaySleep` assertion continuously — this skill installs a `caffeinate -d` LaunchDaemon (step 7) for that.

## When to Use

- Setting up a Mac as a home server, CI runner, or always-on machine
- Preparing a Mac Mini for headless/remote-only operation
- Troubleshooting a Mac that keeps sleeping, locking, or becoming unreachable
- Fixing a headless Apple Silicon Mac whose physical display or VNC/screen-share session goes black despite `displaysleep 0`

## Quick Reference

| Setting | Command | Effect |
|---------|---------|--------|
| Screen saver off | `defaults -currentHost write com.apple.screensaver idleTime -int 0` | Disables screen saver activation |
| System sleep off | `pmset -c sleep 0` | Never sleep |
| Display sleep off | `pmset -c displaysleep 0` | Never turn off display |
| Disk sleep off | `pmset -c disksleep 0` | Never spin down disks |
| Dim before sleep off | `pmset -c halfdim 0` | No pre-sleep dimming (absent/no-op on some modern Macs — not listed in their `pmset -g custom`) |
| Wake-on-LAN | `pmset -c womp 1` | Wake on network access |
| Auto-restart | `pmset -c autorestart 1` | Restart after power loss |
| App Nap off | `defaults write NSGlobalDomain NSAppSleepDisabled -bool YES` | Prevents app throttling |
| SSH on | `systemsetup -setremotelogin on` | Enables Remote Login — needs Full Disk Access; confirm with `-getremotelogin` |
| Keep display awake (Apple Silicon) | `caffeinate -d` via LaunchDaemon | Holds `PreventUserIdleDisplaySleep` — stops the headless display *park* that `displaysleep 0` does **not** prevent (panel + VNC go black) |
| Screen lock status | `sysadminctl -screenLock status` | Reports lock state — no sudo needed |
| Screen lock off | `sysadminctl -screenLock off -password -` | Needs the **user's** account password (user keybag) — root/sudo alone can't change it. Scriptable form: `-password 'pw'`. Step 8 runs the interactive form for you on TTY runs |

## Implementation

Run the bundled script as root, via `sudo` from the target user's account (it refuses to run from a bare root shell so per-user defaults land in the right account):

```bash
sudo bash scripts/setup.sh
```

What it does, in order:

1. **Screen saver off** — `idleTime 0`, per-user
2. **All sleep off** — `pmset -c sleep/displaysleep/disksleep/halfdim 0`
3. **Wake-on-LAN** — `womp 1`
4. **Auto-restart after power failure** — `autorestart 1`
5. **App Nap off** — per-user global default
6. **SSH on** — `systemsetup -setremotelogin on`; needs Full Disk Access and can fail while exiting 0, so trust the verify output, not this step
7. **Keep-display-awake LaunchDaemon** — writes `/Library/LaunchDaemons/com.local.keepdisplayawake.plist` running `caffeinate -d` (RunAtLoad + KeepAlive, survives reboots), loads it, then fires `caffeinate -u -t 2` to wake an already-parked panel. Follows with a verification dump: `pmset -g`, daemon state (want a PID), display assertion (want caffeinate listed), and `systemsetup -getremotelogin` (want On)
8. **Screen lock** — checks `sysadminctl -screenLock status` (no sudo needed). On an interactive (TTY) run it prompts once for the user's account password and turns the lock off in place; unattended runs get the manual GUI/CLI instructions instead

## Common Mistakes

- **Running without sudo** — `pmset` and `systemsetup` require root; `defaults` commands must run as the real user via `sudo -u`
- **Omitting the power-source flag** — `pmset` defines `-a` (all), `-b` (battery), `-c` (charger), `-u` (UPS); the man page doesn't say which profile a flagless write targets, so be explicit — `-c` (or `-a`) on a desktop
- **Expecting immediate effect** — Screen saver and lock-screen changes may require logout/restart
- **FileVault blocking auto-login** — Auto-login (System Settings > Users & Groups > Login Options) requires FileVault off
- **Trusting `systemsetup -setremotelogin on`** — it requires Full Disk Access (per `man systemsetup`) and historically exits 0 even on failure, so a plain run can silently do nothing. Always confirm with `systemsetup -getremotelogin` (the script prints it in the verify block)
- **Relying on `pmset displaysleep 0` alone on Apple Silicon** — it does *not* stop the headless display park; you need the `caffeinate -d` LaunchDaemon (step 7). Symptom: the physical panel and/or VNC session is black even though `pmset -g` shows `displaysleep 0`.
- **Expecting `caffeinate -d` to wake a black screen** — `-d` only *prevents* sleep; it won't wake an already-parked panel. Fire a one-shot `caffeinate -u -t 2` to wake it (step 7 does this after loading the daemon).
- **Running a bare `caffeinate -d` instead of the LaunchDaemon** — an orphaned/nohup'd caffeinate holds the assertion until the next reboot, then silently dies and the display parks again. Use the LaunchDaemon (step 7) so it comes back at boot.
- **Trying to disable the screen lock with `defaults write com.apple.screensaver askForPassword -int 0`** — ignored since macOS 10.13 High Sierra, though old blog posts still recommend it. The setting lives in the user keybag (MobileKeyBag) and changing it needs the **user's** account password — root/sudo alone can't do it, but it *is* scriptable if you supply the password: `sysadminctl -screenLock off -password 'pw'` (or `-password -` to be prompted). Verify with `sysadminctl -screenLock status` — no sudo needed (step 8). For fleets, an MDM configuration profile with the `com.apple.screensaver` payload is the hands-off alternative.

## Reverting

To restore display sleep later:
```bash
sudo pmset -c displaysleep 10  # 10 minutes
```

To remove the keep-display-awake LaunchDaemon (step 7):
```bash
sudo launchctl bootout system /Library/LaunchDaemons/com.local.keepdisplayawake.plist
sudo rm /Library/LaunchDaemons/com.local.keepdisplayawake.plist
```

To re-enable the screen lock (as the user, no sudo; prompts for the account password):
```bash
sysadminctl -screenLock immediate -password -   # or a delay in seconds
```
