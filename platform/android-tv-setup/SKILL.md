---
name: android-tv-setup
description: Set up an Android TV or Google TV over network ADB - back up, debloat with the owner's choices, switch off screen recognition (ACR) and take the microphone and camera away from vendor apps, tune performance, set picture and sound like a calibrator, replace the home screen with a clean Apple TV style launcher, and set up a YouTube DPI bypass (ByeByeDPI) where the ISP throttles YouTube, verifying every step with screenshots from the TV. Use when the user wants to debloat, clean up, speed up, configure, calibrate or replace the launcher on an Android TV / Google TV set or box (Xiaomi, TCL, Hisense, Sony, Philips, CHiQ/Changhong, Haier, Nvidia Shield and others). Not for Samsung Tizen, LG webOS or Fire TV launchers.
---

# Android TV setup

Work on the real device, step by step. Every change is reversible and verified with a screenshot or a
command that proves it. Ask the owner before anything that depends on taste or on how they use the TV.
The question bank is `references/questions.md`; ask each question at its phase, in the owner's language,
with checklist/option UI when available.

## Layout

- `scripts/` - helpers, run from the TV's work directory. Python 3, no packages needed.
- `launcher/` - the launcher source (Java, AndroidX RecyclerView). Copied into each TV's work directory.
- `references/` - one file per phase, read it when you reach that phase.
- Work directory per TV: `tvs/<brand-model>/` next to the skill's repo (or the current project).
  It holds `.tv` (one line `IP:5555`), `backup/`, `shots/`, `debloat/`, `launcher/` and the TV's `README.md`.
  `backup/` and `shots/` contain device identifiers: never publish them.

Run scripts as `python <skill>/scripts/<name>.py` with the work directory as the current directory.

| Script | Purpose |
|---|---|
| `scan.py` | find TVs on the LAN (ADB and Cast ports) |
| `tv.py` | shell command, key presses, screenshots |
| `backup.py` | save the original state, print a device summary |
| `disable.py` | disable a package list, refuses core/factory/Wi-Fi-owner packages, logs for restore |
| `setting.py` | change settings, records original values for restore |
| `snapshot.py` | find which settings key a TV menu item writes (save, change one item, diff) |
| `appops.py` | restrict background running for apps, logs for restore |
| `privacy.py` | list ACR/ad packages and apps holding the mic or camera; block mic and camera; blocking DNS with a proof check; logs for restore |
| `restore.py` | undo everything: packages, settings, app ops, Home |
| `build-install.sh` | build the launcher, install, set as Home, print who really holds Home |
| `adb-closed.py` | prove network ADB is closed at the end |

## Phases

1. **Connect** - `references/connect.md`. Find the TV, connect ADB, tell the owner when the
   "Allow debugging?" prompt appears and to tick "Always allow". Ask the connection questions (Q-C*).
2. **Back up** - `scripts/backup.py` before any change. Read the summary aloud: brand, Android version,
   RAM, Google TV or not, who owns the saved Wi-Fi network.
3. **Debloat** - `references/debloat.md`. Sort packages, ask Q-D*, disable in small batches,
   screenshot after each batch.
4. **Privacy** - `references/privacy.md`. Mandatory on every TV, never skipped. Scan with `scripts/privacy.py`,
   have the owner switch off ACR / viewing information / ad ID in the menu (screenshots), disable proven ACR
   packages, block the mic and camera for vendor apps, turn on blocking DNS (`privacy.py dns on`). Ask Q-R*.
5. **Performance** - `references/performance.md`. Measure memory first, ask Q-P*, apply, measure again.
6. **Launcher** - `references/launcher.md`. Ask Q-L*, build, install, take over Home. On Google TV this
   involves the setup wizard and the Wi-Fi owner: follow the file exactly. Verify the cold-start skeletons per
   `launcher.md` section 5a. For owners in Russia (timezone/locale)
   or with slow YouTube, ask Q-B* and set up ByeByeDPI per `references/dpi-bypass.md` before building, so the
   launcher can start it only while YouTube is open.
7. **Picture** - `references/picture.md`. Ask Q-V*, discover the vendor's keys, apply a calibrated profile,
   verify in the TV's own menu.
8. **Sound** - `references/sound.md`. Ask Q-S*, apply, verify.
9. **Reboot check** - reboot once. Confirm Home, network, the disabled list, the settings and the mic/camera app ops survived.
10. **Finish** - `references/finish.md`. Write the TV's README (with a Privacy section), close network ADB, prove it is closed.

Remote buttons (app keys, gear/dashboard key, remapping, Bluetooth remotes) are a separate module that is
not part of this version. Record which buttons stopped working (`getevent -lt` + logcat) and tell the owner.

## Hard rules

- Back up first. Never uninstall system packages: `pm disable-user --user 0` only, one `pm` call per shell call.
- Never disable Android core packages (see `references/debloat.md`) or anything the TV needs to show a picture,
  switch inputs, pair the remote, type, or install apps. When a vendor package name is unclear, read
  `dumpsys package <pkg>` (activities, services, receivers, permissions); ask the owner if still unclear.
- Never launch, even read-only, a package whose name says factory/fac/AT/production. Some boards flip a
  factory flag when one starts and lose the Input key, CEC and Play services on the next boot.
- Before disabling a package, check `dumpsys wifi | grep -o 'cname=[^ ]*'`. Android deletes the saved
  network of a disabled owner and the TV drops off Wi-Fi and ADB. `disable.py` refuses; the owner must
  forget and re-join the network in Settings first. The TV may get a new IP afterwards.
- Disable in small batches and screenshot between them. After the last batch, reboot and compare
  `pm list packages -d` with `backup/disabled-by-us.txt`.
- If `pm disable-user` is refused for every package, stop debloating and say so. Offer DNS blocking and the
  TV's own privacy toggles instead.
- `set-home-activity` can print `Success` and change nothing. Only `dumpsys activity activities | grep mFocusedApp`
  after pressing Home proves the takeover. If Home goes black, re-enable the stock launcher at once.
- Settings writes must be verified: read the value back and look at the TV's menu (screenshot). A vendor key
  that changes in `settings` but not on screen was not applied.
- Live TV, HDMI and DRM apps give 0-byte screenshots. That is the TV, not a fault: check
  `dumpsys activity activities | grep topResumedActivity` instead.
- The privacy phase is not optional. If the owner declines a step, record it in the TV's README as declined.
  Menu toggles are not proof: verify with `privacy.py scan` and `pm list packages -d`.
- Keep it light: TVs have 1-3 GB of RAM. The launcher has no blur, no video, no network polling.
- Finish by closing network ADB: port 5555 is plaintext and gives a shell to authorised keys on the LAN.

## Reporting

After each phase tell the owner, briefly: what changed, how it was verified, how to undo it.
Write per-TV knowledge (package meanings, vendor settings keys, quirks) into `references/devices/<board>.md`
so the next TV of the same family goes faster.
