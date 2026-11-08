---
name: mac-permissions
description: Diagnose and fix macOS privacy permissions (TCC) when a script, agent or CLI is blocked — Full Disk Access, Accessibility, Automation (Apple Events), Screen Recording, Files & Folders. Use when you see "Operation not permitted", "Not authorized to send Apple events", "not allowed assistive access", "-1743", "-25211", a black or wallpaper-only screenshot, an osascript that hangs, or when you ask "what permission does this need", "why does it work in Terminal but not in my launch agent", "reset the permission prompt". Covers which permission each error means, who the grant belongs to, how to read current grants, tccutil, and what can never be granted from a script.
compatibility: >-
  macOS (tested on macOS 26, Apple silicon). Built-in tools only: sqlite3, tccutil, osascript, open, ioreg. No network.
metadata:
  grounded: "2026-11-03 — grants read, Automation prompt hang and locked-screen capture reproduced live on macOS 26.6"
---

# macOS privacy permissions (TCC)

TCC (Transparency, Consent and Control) decides whether a process may touch private data
or control other apps. Three facts explain nearly every confusing failure:

1. **The grant belongs to the "responsible" app, not to your command.** Run from
   Terminal, `osascript` uses Terminal's grants. Run from VS Code's terminal, VS Code's.
   Run from a LaunchAgent, the grant of the binary in the plist (`/bin/zsh`, `python3`).
   That is why "it works in Terminal but not in my scheduled job".
2. **A script can never grant itself anything.** Only a human clicking in System Settings
   (or a consent dialog) grants. There is no `sudo` path on a SIP-protected Mac. Your job
   is to name the exact pane and the exact app, then stop.
3. **A missing grant often fails silently or hangs**, rather than erroring.

## Which permission, from the symptom

| Symptom | Permission | Settings pane (Privacy & Security >) |
|---|---|---|
| `Operation not permitted` reading `~/Library/Messages`, `~/Library/Mail`, Safari history, another app's container, `TCC.db` | Full Disk Access | Full Disk Access |
| `Operation not permitted` on `~/Desktop`, `~/Documents`, `~/Downloads`, iCloud Drive, removable volumes | Files & Folders (or FDA) | Files & Folders |
| `Not authorized to send Apple events to <App>. (-1743)` | Automation | Automation, under the calling app |
| osascript to an app **hangs** with no output | Automation prompt waiting for a click | answer the dialog, or grant in Automation |
| `osascript is not allowed assistive access. (-25211)` / `(-1719)` from System Events UI scripting | Accessibility | Accessibility |
| Screenshot is wallpaper-only or windows are blank | Screen Recording | Screen & System Audio Recording |
| `could not create image from rect` / `from window` and a **black** full-screen capture | Usually the **screen is locked or the display is off**, not a permission | none; see below |
| Keystrokes/clicks posted from code do nothing | Accessibility (and Input Monitoring for reading keys) | Accessibility / Input Monitoring |

## Read the current grants

The per-user database is readable only by a process that already has Full Disk Access,
which is itself a test:

```bash
sqlite3 "$HOME/Library/Application Support/com.apple.TCC/TCC.db" \
  "select service, client, indirect_object_identifier, auth_value from access order by 1"
# system-wide grants (FDA, Accessibility, Screen Recording live here):
sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" \
  "select service, client, auth_value from access where service in
   ('kTCCServiceSystemPolicyAllFiles','kTCCServiceAccessibility','kTCCServiceScreenCapture')"
```

`auth_value` 2 = allowed, 0 = denied. For Automation (`kTCCServiceAppleEvents`) the
`indirect_object_identifier` is the *target* app's bundle id. If the query itself fails
(an authorization or open error), your responsible app lacks FDA. **Never write to TCC.db**;
SIP blocks it and a corrupted db breaks every prompt.

## Find who is responsible

```bash
ps -o comm= -p $PPID                           # your parent
ps -o comm= -p $(ps -o ppid= -p $PPID)         # and its parent
```

Walk up until you reach an `.app` (Terminal, iTerm, VS Code, Claude) or `launchd`.
That is the row to look for in the settings pane.

## The Automation prompt hang (avoid it in unattended runs)

The first `tell application "X"` from a given responsible app opens a consent dialog and
**blocks until a human answers**. Verified: an osascript to an app with no Automation row
hung past a 120 s tool timeout. In anything unattended, check TCC.db for a
`kTCCServiceAppleEvents` row for that target first, and always wrap the call:

```bash
perl -e 'alarm 10; exec @ARGV' osascript -e 'tell application "Reminders" to count lists'
# exit 142 = killed by the alarm (macOS has no `timeout` command)
```

## Screen capture: permission vs locked screen

When the screen is locked or the display has slept, `screencapture` still exits 0 for a
full-screen grab but the image is solid black, and `-R` / `-l` fail with
`could not create image from rect|window`. Verified on a Mac whose terminal app *did*
hold the Screen Recording grant. Check before blaming TCC:

```bash
ioreg -n Root -d1 -a | grep -A1 CGSSessionScreenIsLocked   # <true/> = locked
pmset -g log | grep -E "Display is turned (on|off)" | tail -1
```

## Reset a decision so the prompt comes back

```bash
tccutil reset AppleEvents com.example.app     # one app, one service
tccutil reset ScreenCapture                    # every app for that service (asks again)
```

Service names drop the `kTCCService` prefix: `All`, `SystemPolicyAllFiles`,
`Accessibility`, `AppleEvents`, `ScreenCapture`, `Photos`, `AddressBook`, `Calendar`,
`Reminders`, `Camera`, `Microphone`. Resetting is safe but makes every affected app
prompt again; prefer the single-bundle form.

## Open the right pane for the human

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Automation"
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
```

These anchors are Apple's documented deep links; they open a visible window, so only
run them for a human who is at the Mac. Then tell them: which app to toggle on, and that the app must be **restarted** for a new
FDA, Accessibility or Screen Recording grant to apply.

## What can't be done from a script

- Granting any TCC permission (no CLI, no defaults key, SIP-protected db).
- Clicking a consent dialog (the dialog ignores synthetic clicks by design). Never try.
- Ad-hoc-signed apps you rebuild get a **new identity each build** and lose their grants;
  sign consistently or expect to re-grant. (`mac-menu-bar-app` covers this.)
