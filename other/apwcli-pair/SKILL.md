---
name: apwcli-pair
description: Pair apwcli's daemon with Apple Passwords (iCloud Keychain) with nobody at the screen, by reading the macOS 6-digit PIN through Accessibility and submitting it. Use when apwcli says "session is not paired" or "pairing cancelled", after a Mac reboots or logs out, or to pair a fleet Mac over ssh.
---

# apwcli-pair

apwcli's daemon pairs with Apple's password helper once per login session. Pairing shows a
6-digit PIN in a macOS window, "Verification Code", that a person normally reads and types. This
script reads it through Accessibility and submits it, so no one needs to be at the screen.

## Commands

```bash
# on the Mac itself
~/.agents/skills/apwcli-pair/scripts/apwcli-pair

# another fleet Mac, from anywhere
ssh -o BatchMode=yes -o ConnectTimeout=15 <host> 'zsh -lc ~/.agents/skills/apwcli-pair/scripts/apwcli-pair'
```

A paired host prints `already paired` and exits 0, so the command is safe to repeat. Check the
result with `apwcli pw get github.com`, not with `apwcli daemon status`: its `pairing` line reads
"not paired" for a few seconds while a challenge is open even when the session works.

| Exit | Meaning | Do |
|---|---|---|
| 0 | `paired` or `already paired` | carry on |
| 1 | the helper rejected the PIN | run it again; a second failure means a stale window, so `apwcli daemon restart` first |
| 2 | apwcli error (no daemon, no browser) | run `apwcli doctor` on that host |
| 3 | no PIN visible within 15 s | see preconditions; then the fallback |

## Preconditions

- apwcli installed: the `apwcli` role of macbook-provision does it (`uv tool install apwcli`),
  with Google Chrome present for the daemon's headless browser.
- The Mac is logged in and unlocked. A locked screen hides windows from Accessibility.
- The process that runs the script has Accessibility. Over ssh that is
  `/usr/libexec/sshd-keygen-wrapper`; in a terminal it is the terminal app. Check before
  blaming the script (query from `~/.agents/docs/macos-tcc.md`):

  ```bash
  sqlite3 -readonly '/Library/Application Support/com.apple.TCC/TCC.db' \
    "select client, auth_value from access where service='kTCCServiceAccessibility' and client like '%sshd%'"
  ```

  `2` means allowed. Granting it needs a person once; on 2026-10-28 every fleet Mac with apwcli
  already had it (mac-mini-m6, mac-mini-m2, archs-mac-mini, dev-server-frank-lume, macbook-pro-m3).

## Fallback

When exit 3 persists on an unlocked, granted host, read the PIN another way and submit it by
hand: `apwcli daemon pair --pin <digits>` right after the window appears, or ask Frank for the
digits. A screenshot over ssh needs Screen Recording for sshd, which only mac-mini-m2 has.

## Notes

- Pairing lasts for the login session. Rerun after a reboot. The daemon needs no restart.
- The PIN is single-use and is printed only with `--verbose`.
- `scripts/apwcli-pair --selftest` checks the digit parser without touching apwcli.
- Measured on macOS 26: the PIN is the one static text in `group 1` of the window, as "123 456".
  If Apple moves it, dump the window with
  `osascript -e 'tell application "System Events" to tell process "PasswordManagerBrowserExtensionHelper" to get entire contents of window 1'`
  and fix `_PIN_QUERY` in `scripts/pair.py`.
