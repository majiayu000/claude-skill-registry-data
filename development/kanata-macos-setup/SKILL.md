---
name: kanata-macos-setup
description: Use when the user asks to "set up kanata", "replace karabiner",
  "remap caps lock", "key remapper macOS", "kanata connect_failed", "keyboard
  not working after brew upgrade", or needs to configure kanata as a
  Karabiner-Elements replacement on macOS.
---

## Context

On macOS, kanata uses the Karabiner DriverKit VirtualHIDDevice for output.
**Karabiner-Elements (the full app, via `brew install --cask karabiner-elements`) must stay installed** — it is what provides and launches the `Karabiner-VirtualHIDDevice-Daemon`. There is no supported standalone-driver-only install; the daemon's LaunchDaemon plist lives inside the KE app bundle, not in `/Library/LaunchDaemons`. Only KE's *own remapping engine* (`Karabiner-Core-Service` and its GUI agents) gets disabled — the app itself is not removed.

Kanata must run as root via LaunchDaemon (not LaunchAgent).

**Critical**: kanata requires TWO components at boot:
1. `org.pqrs.Karabiner-DriverKit-VirtualHIDDevice` — the kernel dext (auto-started by the system extension framework)
2. `Karabiner-VirtualHIDDevice-Daemon` — the bridge daemon, launched via the plist bundled inside `/Library/Application Support/org.pqrs/Karabiner-Elements/Karabiner-Elements Privileged Daemons v2.app/Contents/Library/LaunchDaemons/org.pqrs.service.daemon.Karabiner-VirtualHIDDevice-Daemon.plist`

If the daemon is missing or can't connect, kanata loops with `connect_failed asio.system:NN` at boot, which monopolizes the internal keyboard HID and blocks all input after login. **Two different root causes produce this same symptom** — see the two troubleshooting entries below; don't assume it's always the HID-conflict one.

## File layout in dotfiles

| Path | Purpose |
|---|---|
| `kanata/kanata.kbd` | Config (XDG, stowed to `~/.config/kanata/`) |
| `kanata-daemon/com.lucatrifilio.kanata.plist` | LaunchDaemon template used only by the manual/README bootstrap flow (`sed __HOME__` + `sudo tee`) — the ansible role uses its own separate jinja template below, not this file |
| `kanata-daemon/karabiner-core-service-watchdog.sh` | Watchdog script, boots out KE Core-Service/agents every 15s (see troubleshooting below) |
| `ansible/roles/macos/templates/kanata.plist.j2` | Real jinja template ansible installs to `/Library/LaunchDaemons/com.lucatrifilio.kanata.plist` |
| `ansible/roles/macos/templates/karabiner-watchdog.plist.j2` | Jinja template ansible installs to `/Library/LaunchDaemons/com.lucatrifilio.karabiner-watchdog.plist` |

Add `--ignore=^kanata-daemon$` to `.stowrc`.

The actual install path is `ansible/roles/macos/tasks/main.yml` (`enable_kanata` var) — it templates `kanata.plist.j2` to `/Library/LaunchDaemons/com.lucatrifilio.kanata.plist`, bootstraps it, disables the KE Core-Service daemon + GUI agents listed below, and installs/bootstraps the watchdog LaunchDaemon (see below). It does **not** install any separate VirtualHIDDevice-Daemon plist — KE's own bundled one is used as-is.

## kanata.kbd template

```
(defcfg
  macos-dev-names-include (
    "Apple Internal Keyboard / Trackpad"
  )
  process-unmapped-keys yes
)

(defsrc
  caps f1   f2   f7   f8 f9   f10  f11  f12
)

(deflayer base
  @cap brdn brup prev pp next mute vold volu
)

(defalias
  cap (tap-hold 200 200 esc lctl)
)
```

`macos-dev-names-include` is a whitelist — only listed devices are intercepted.
All others (external keyboards, Glove80, etc.) are ignored automatically.

**Media keys**: when kanata grabs the device in exclusive mode, the Apple keyboard sends media keys as F-keys (F1, F2, F7-F12) rather than consumer HID events. They must be explicitly mapped back to consumer outputs (`brdn`, `brup`, `mute`, `vold`, `volu`, `pp`, `prev`, `next`) — transparent `_` is not enough. Do NOT use `process-unmapped-keys no` to fix this; it breaks caps lock remapping.

## Kanata LaunchDaemon

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lucatrifilio.kanata</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/kanata</string>
        <string>--cfg</string>
        <string>__HOME__/.config/kanata/kanata.kbd</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/kanata.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/kanata.log</string>
</dict>
</plist>
```

Use `__HOME__` as placeholder — the install step substitutes it with `$HOME`.

## Troubleshooting: kanata stopped working after dotfiles change

**Symptom**: kanata smette di funzionare dopo una modifica al plist template in dotfiles (es. refactor, nuovo path, nuovi argomenti).

**Cause**: il plist in `/Library/LaunchDaemons/` non si aggiorna automaticamente quando cambia il template nel repo — sono due file separati. Il playbook ansible va rieseguito manualmente per propagare il cambiamento.

**Fix**: reinstalla il plist dal template aggiornato:
```bash
cd ~/Progetti/dotfiles
sed "s|__HOME__|$HOME|g" kanata-daemon/com.lucatrifilio.kanata.plist > /tmp/kanata.plist
sudo cp /tmp/kanata.plist /Library/LaunchDaemons/com.lucatrifilio.kanata.plist
sudo launchctl bootout system/com.lucatrifilio.kanata 2>/dev/null || true
sudo launchctl bootstrap system /Library/LaunchDaemons/com.lucatrifilio.kanata.plist
sudo launchctl list | grep kanata  # deve mostrare PID numerico
```

---

## Troubleshooting: kanata not running after reboot (plist present but not bootstrapped)

**Symptom**: kanata not working after reboot; plist exists in `/Library/LaunchDaemons/` but `sudo launchctl list | grep kanata` returns nothing. Process can only be started manually with `sudo kanata ...`.

**Cause**: the plist was copied to `/Library/LaunchDaemons/` but never bootstrapped into launchd (e.g. setup ran `cp` but not `bootstrap`, or the service was `bootout`ed).

**Diagnose**:
```bash
sudo launchctl print system/com.lucatrifilio.kanata
# "Could not find service" = not bootstrapped
```

**Fix**:
```bash
sudo kill $(pgrep -x kanata) 2>/dev/null || true
sudo launchctl bootstrap system /Library/LaunchDaemons/com.lucatrifilio.kanata.plist
sudo launchctl print system/com.lucatrifilio.kanata  # should show state = running
```

---

## Troubleshooting: keyboard blocked after boot (HID device conflict)

**Symptom**: internal keyboard works at login screen but stops after login. `cat /tmp/kanata.log` shows `connect_failed asio.system:61` in a loop.

**Cause**: kanata starts before `Karabiner-VirtualHIDDevice-Daemon` is ready, monopolizing the HID device. This is a *timing* problem — the daemon exists and is compatible, it just hasn't bound its socket yet.

**Diagnose**:
```bash
sudo launchctl list | grep -i "pqrs\|karabiner\|virtual"
# Should show Karabiner-VirtualHIDDevice-Daemon running.
ps aux | grep -E "kanata|VirtualHIDDevice-Daemon"
```

**Fix**:
```bash
sudo launchctl bootout system/com.lucatrifilio.kanata
sudo launchctl bootout system/org.pqrs.service.daemon.Karabiner-VirtualHIDDevice-Daemon 2>/dev/null || true
sudo launchctl bootstrap system "/Library/Application Support/org.pqrs/Karabiner-Elements/Karabiner-Elements Privileged Daemons v2.app/Contents/Library/LaunchDaemons/org.pqrs.service.daemon.Karabiner-VirtualHIDDevice-Daemon.plist"
sudo launchctl bootstrap system /Library/LaunchDaemons/com.lucatrifilio.kanata.plist
```

**Note on `com.apple.provenance`**: files created via `sudo tee` get this xattr and become immutable even with sudo. Workaround: write to `/tmp/` first, then `sudo cp` to the destination.

---

## Troubleshooting: kanata connect_failed despite daemon running — driver/kanata version mismatch (CRITICAL, easy to misdiagnose as the HID-conflict above)

**Symptom**: `connect_failed asio.system:2` loops forever in `/tmp/kanata.log`, even after confirming both `com.lucatrifilio.kanata` and `Karabiner-VirtualHIDDevice-Daemon` are freshly running, even after a full reboot, even after fully removing and reinstalling Karabiner-Elements. `/var/log/karabiner/virtual_hid_device_service.log` shows the daemon logging `bound` successfully but never logs `peer_connected` for kanata's attempts.

**Cause**: `brew install --cask karabiner-elements` always pulls the *latest* driver (`Karabiner-DriverKit-VirtualHIDDevice`). Kanata's macOS client is version-pinned to an older driver protocol — as of kanata v1.12.0 (latest, 2026-07-05) the documented supported driver is **v6.2.0**. Driver v7.0.0+ introduced breaking protocol changes (removed `get_status`, bumped protocol version), so any driver ≥ v7 silently breaks kanata's connection with no clear error — `asio.system:2` (ENOENT) rather than a version-mismatch message. Kanata's maintainer has no macOS hardware and doesn't validate this path, so this drift is not caught upstream.

**Diagnose**:
```bash
# Confirm daemon never logs peer_connected for the new client despite it running:
sudo tail -20 /var/log/karabiner/virtual_hid_device_service.log

# Trace what path kanata is actually trying to reach (look for "vhidd_server" vs whatever
# the daemon actually created — "vhidd_client"/"vhidd_response" dirs are a mismatch):
sudo fs_usage -w -f filesys 2>/dev/null | grep -i kanata

# Compare installed driver version against kanata's supported ceiling:
pkgutil --pkg-info org.pqrs.Karabiner-DriverKit-VirtualHIDDevice   # look at "version:"
gh release view --repo jtroo/kanata --json body -q .body | grep -i "driver version"
```

If the installed driver version is higher than what kanata's release notes document as supported, this is the cause.

**Fix**: downgrade just the driver package (not the whole KE app) to the version kanata supports, via the pqrs-org standalone installer:
```bash
gh release download v6.2.0 --repo pqrs-org/Karabiner-DriverKit-VirtualHIDDevice --pattern "*.pkg" --clobber
sudo installer -pkg Karabiner-DriverKit-VirtualHIDDevice-6.2.0.pkg -target /
pkgutil --pkg-info org.pqrs.Karabiner-DriverKit-VirtualHIDDevice   # confirm version: 6.2.0

# Restart daemon + kanata (no reboot or dext re-approval needed — same team ID/bundle ID):
sudo launchctl bootout system/org.pqrs.service.daemon.Karabiner-VirtualHIDDevice-Daemon 2>/dev/null || true
sudo launchctl bootstrap system "/Library/Application Support/org.pqrs/Karabiner-Elements/Karabiner-Elements Privileged Daemons v2.app/Contents/Library/LaunchDaemons/org.pqrs.service.daemon.Karabiner-VirtualHIDDevice-Daemon.plist"
sudo launchctl bootout system/com.lucatrifilio.kanata
sudo launchctl bootstrap system /Library/LaunchDaemons/com.lucatrifilio.kanata.plist
tail -f /tmp/kanata.log   # should show "driver connected: true", no more connect_failed
```

**Prevention**: `brew upgrade`/`brew reinstall --cask karabiner-elements` will silently re-pull the latest (incompatible) driver. Either `brew pin karabiner-elements`, or re-check `pkgutil --pkg-info org.pqrs.Karabiner-DriverKit-VirtualHIDDevice` after any KE-related brew upgrade and re-apply the downgrade above if it moved past the version kanata's current release documents as supported.

**Do NOT** respond to this symptom by deleting `/Applications/Karabiner-Elements.app` or inventing a standalone `VirtualHIDDevice-Daemon` LaunchDaemon outside the KE app bundle — neither is how the real working setup is structured (see Context above), and both make the actual version-mismatch cause harder to find.

---

## Troubleshooting: Input Monitoring / Accessibility permission lost after every kanata upgrade

**Symptom**: after `brew upgrade kanata` (or after removing/re-adding the entry), kanata crash-loops: first `failed to open keyboard device(s): kanata needs macOS Input Monitoring permission`, then — after re-granting that — `kanata needs macOS Accessibility permission`. **Both** permissions are required, not just Input Monitoring.

**Cause**: kanata ships ad-hoc signed (`codesign -dv` shows `flags=0x20002(adhoc,linker-signed)`, `TeamIdentifier=not set`, identifier like `kanata-<hash>`). The identifier changes on every build/version, so TCC (which ties the grant to resolved path + code requirement) loses the permission on every upgrade — not just when the versioned Cellar path changes, but even at the same path if the binary is rebuilt. Confirmed by the kanata community (github.com/jtroo/kanata/discussions/1537): there is no workaround on the Input Monitoring side, it must be re-granted manually after every upgrade.

**Diagnose**:
```bash
tail -10 /tmp/kanata.log
# "needs macOS Input Monitoring permission" or "needs macOS Accessibility permission"
sudo sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" \
  "SELECT client,auth_value FROM access WHERE service='kTCCServiceListenEvent' AND client LIKE '%kanata%';"
```

**Fix** (repeat on every upgrade, unless/until `brew pin kanata` or a fixed re-sign identifier is adopted):
```bash
readlink /opt/homebrew/bin/kanata   # resolve the real versioned path, e.g. ../Cellar/kanata/1.12.0/bin/kanata
```
1. System Settings → Privacy & Security → **Input Monitoring** → `+` → `Cmd+Shift+G` → paste the resolved real path above (the Finder picker does **not** follow symlinks, it needs the versioned Cellar path, not `/opt/homebrew/bin/kanata`) → select → enable the toggle
2. Repeat the same for **Accessibility** (same path)
3. Restart the service:
```bash
sudo launchctl bootout system/com.lucatrifilio.kanata 2>/dev/null || true
sudo launchctl bootstrap system /Library/LaunchDaemons/com.lucatrifilio.kanata.plist
tail -f /tmp/kanata.log   # expect "driver connected: true", "virtual_hid_keyboard_ready true"
```

**Prevention (not yet applied)**: two options considered, neither implemented:
- `brew pin kanata` — avoids automatic upgrades, permission stays valid until you unpin/upgrade yourself
- Copy the binary to a fixed path and re-sign it with `codesign --sign - --identifier <fixed-id>` instead of the default hash-based identifier — survives upgrades but requires re-running the copy+sign step after every `brew upgrade kanata`

---

## Troubleshooting: KE agents revive and break caps lock remapping (recurring)

**Symptom**: caps lock remapping stops working; kanata log loops `driver connected: false / driver connected: true`. Media keys may also break.

**Cause**: KE user agents (especially `Karabiner-Core-Service-rev2`) restart after a macOS update, KE reinstall, or KE app launch (even a headless `open -g`), grabbing the HID device before kanata. Always check **both** system daemon and user agents.

**Diagnose**:
```bash
sudo launchctl list | grep karabiner   # system daemon
launchctl list | grep karabiner        # user agents — Core-Service-rev2 is the main offender
tail -20 /tmp/kanata.log               # loop = device conflict
```

**Fix**:
```bash
sudo launchctl disable system/org.pqrs.service.daemon.Karabiner-Core-Service
sudo launchctl bootout system/org.pqrs.service.daemon.Karabiner-Core-Service
for agent in \
  org.pqrs.service.agent.Karabiner-Core-Service \
  org.pqrs.service.agent.Karabiner-Core-Service-rev2 \
  org.pqrs.service.agent.karabiner_console_user_server \
  org.pqrs.service.agent.karabiner_session_monitor \
  org.pqrs.service.agent.Karabiner-NotificationWindow; do
  launchctl disable gui/$(id -u)/$agent 2>/dev/null || true
  launchctl bootout gui/$(id -u)/$agent 2>/dev/null || true
done
sudo launchctl bootout system/com.lucatrifilio.kanata
sudo launchctl bootstrap system /Library/LaunchDaemons/com.lucatrifilio.kanata.plist
```

---

## Troubleshooting: "Waiting for a connection from Karabiner-Core-Service to Karabiner-VirtualHIDDevice-Daemon" popup in KE Settings.app

**Symptom**: opening Karabiner-Elements.app (esp. clicking into Simple/Complex Modifications tabs) shows an infinite spinner dialog. kanata itself keeps working fine (`tail /tmp/kanata.log` still shows `virtual_hid_keyboard_ready true`) — this is cosmetic, not a functional break.

**Cause**: `launchctl disable` on Core-Service/its agents (see entry above) only sets the persistent disabled bit — it does not stop KE Settings.app from force-starting those processes directly when you open it or navigate its tabs (confirmed: `/var/db/com.apple.xpc.launchd/disabled*.plist` mtime does not change when the popup appears, so the app is not going through the normal `launchctl enable`/`bootstrap` path). Once Core-Service starts, it can never actually connect — kanata already holds the VirtualHIDDevice-Daemon connection exclusively — so the dialog spins forever until Core-Service is killed again.

Because the disabled bit never flips, a `WatchPaths`-based launchd trigger on the disabled-state file **won't** catch this — there's nothing to watch. The only reliable fix is a polling watchdog.

**Fix**: `com.lucatrifilio.karabiner-watchdog` — a root LaunchDaemon (`ansible/roles/macos/templates/karabiner-watchdog.plist.j2` → `/Library/LaunchDaemons/`) that runs `kanata-daemon/karabiner-core-service-watchdog.sh` every 15s (`StartInterval`), boot-outing Core-Service + its GUI agents (same list as the entry above) if found. Installed automatically via the ansible `macos` role when `enable_kanata`. Manual bootstrap:
```bash
sudo launchctl bootout system/com.lucatrifilio.karabiner-watchdog 2>/dev/null || true
sudo launchctl bootstrap system /Library/LaunchDaemons/com.lucatrifilio.karabiner-watchdog.plist
sudo launchctl print system/com.lucatrifilio.karabiner-watchdog   # state = running
cat /tmp/karabiner-watchdog.log   # empty unless it actually had to boot something out
```

**Note**: an already-open, already-stuck Settings window won't refresh itself just because the watchdog kills the backend process — quit (Cmd+Q) and reopen it. Whether reopening + navigating tabs still briefly flashes the dialog before the watchdog clears it (worst case ~15s) was not confirmed by direct reproduction, only inferred from the mechanism.

---

## Troubleshooting: media keys (volume, brightness, play/pause) not working

**Symptom**: pressing F1/F2/F7-F12 triggers standard F-key actions instead of media actions.

**Cause**: when kanata grabs the device in exclusive mode (`process-unmapped-keys yes`), the Apple keyboard delivers media keys as F1/F2/F7-F12 (keyboard HID page). kanata re-emits them as plain F-keys through VirtualHID, which macOS doesn't translate to media actions.

**Fix**: map F-keys explicitly to consumer outputs in `defsrc`/`deflayer` (see template above). Do NOT switch to `process-unmapped-keys no` — it restores media keys but breaks caps lock remapping.

## Brewfile

```
brew "kanata"
cask "karabiner-elements"   # REQUIRED — provides the VirtualHIDDevice-Daemon kanata depends on.
                            # Do not remove after install; only its Core-Service engine is disabled.
```

## Manual steps (new machine)

1. Add the resolved kanata binary (`readlink /opt/homebrew/bin/kanata` for the real Cellar path) to **both** System Settings → Privacy & Security → **Input Monitoring** and **Accessibility** — see the permission-loss troubleshooting entry above, both are required
2. Remove leftover KE entries from Input Monitoring if present
3. After first install (or any `karabiner-elements` cask upgrade), check the driver version per the version-mismatch entry above — the cask does not pin a kanata-compatible version

## KE services reference

| Service | Keep? | Reason |
|---|---|---|
| Karabiner-Elements.app (full bundle) | YES | hosts the VirtualHIDDevice-Daemon's LaunchDaemon plist |
| `Karabiner-VirtualHIDDevice-Daemon` | YES | kanata output driver bridge |
| `Karabiner-DriverKit-VirtualHIDDevice` (dext) | YES, but version-pinned | must not exceed kanata's supported driver version (v6.2.0 as of kanata v1.12.0) |
| `Karabiner-Core-Service` (daemon) | NO | karabiner_grabber, conflicts with kanata for the HID device |
| `Karabiner-Core-Service` (agent) | NO | KE UI agent |
| `karabiner_console_user_server` | NO | keyboard type dialog |
| `karabiner_session_monitor` | NO | session handling |
| `Karabiner-NotificationWindow` | NO | annoying dialog |
