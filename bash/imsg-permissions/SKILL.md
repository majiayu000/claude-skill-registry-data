---
name: imsg-permissions
description: Grant the imsg CLI its macOS privacy permissions (Full Disk Access, Automation → Messages, Contacts) and prove each one from every parent that runs imsg; on a SIP-off Mac, also deploy its IMCore bridge. Use when setting up imsg on a Mac, after `brew upgrade imsg` or a node upgrade, when imsg fails with "unable to open database file", "Not authorized to send Apple events" or "(Contacts unavailable)", or when typing indicators, read receipts or `imsg status` need the IMCore bridge.
---

# imsg-permissions

imsg (openclaw/imsg, Homebrew) needs three macOS privacy grants; upstream lists them in
[docs/permissions.md](https://github.com/openclaw/imsg/blob/main/docs/permissions.md). How TCC
grants work, and the backup-first steps for a `TCC.db` edit, are in
[macos-tcc.md](~/.agents/docs/macos-tcc.md). Read it before step 3.

The work centres on the **grant table**: one row per parent that runs imsg, one column per gate.
A cell is ✅ only when a real command from that real parent passed.

| Parent | Full Disk Access | Automation → Messages | Contacts |
|---|---|---|---|
| SSH | | | |
| Terminal.app, Ghostty, iTerm2 (each one installed) | | | |
| paseo daemon (charged to its LaunchAgent's first program, `/bin/zsh`, or node on hosts in macbook-provision's `paseo_node_launch_hosts` (mac-mini-m6); with SIP on, node under a zsh job is denied, personal-agent Q265–Q266) | | | |
| imsg as its own process (LaunchAgent) | | | |
| openroutine daemon (charged to `~/.cargo/bin/openroutine`, its LaunchAgent's program; `cargo install` leaves it ad-hoc signed, so each rebuild drops the grant until coding-agent's `devops/openroutine/resign.sh` re-signs it with a self-made certificate, coding-agent Q710; its `tcc-probe` task checks daily) | | | |

## Scripts

- `probe.sh <own-address> [--keep-ssh]` tests all three gates from the parent that runs it, and
  sends nothing. `--keep-ssh` only in the SSH row.
- `as-imsg.sh [--tty] <imsg args…>` runs imsg once as its own process (a one-shot gui
  LaunchAgent) and prints its output and exit code. `--tty` puts a tty on stdin.

## Steps

1. **Fill the rows.** Keep the terminal apps installed on this host. Find paseo's launch line with
   `plutil -extract ProgramArguments json -o - ~/Library/LaunchAgents/sh.paseo.daemon.plist`;
   macOS charges the first program, even after `exec` (personal-agent Q264). Done when each
   row names a real parent.
2. **Test every cell** with `probe.sh` (`<own-address>` is the user's iMessage address) from its
   parent:
   - SSH: run it in this shell with `--keep-ssh`.
   - Terminal: a `.command` file that runs it, via `open -a Terminal <file>`.
   - Ghostty: `open -na Ghostty --args -e <file>`.
   - paseo: `launchctl submit -l <label> -o <log> --` plus paseo's exact launch line, with
     `exec paseo daemon run` swapped for `exec <probe.sh> <own-address>`; then `launchctl remove <label>`.
   - imsg itself: `as-imsg.sh chats --limit 1 --json` and `as-imsg.sh nickname --local --address
     <own-address> --json`. Its Automation cell waits for step 5.

   Write output to files and read them back. Done when every cell holds pass or fail with output.
3. **Grant each failing cell.**
   - Full Disk Access: System Settings **+**, adding the parent app, or for imsg itself the real
     binary `/opt/homebrew/Cellar/imsg/<ver>/libexec/imsg` (`bin/imsg` is a bash wrapper).
   - Automation: rerun the parent's probe. When "<parent> wants access to control Messages.app"
     shows, click **Allow** with System Events, as macos-tcc.md shows.
   - Contacts: imsg asks only with a TTY on stdin and no `SSH_CONNECTION`/`SSH_CLIENT`;
     `chats` and `history` never ask. For imsg itself, run `as-imsg.sh --tty nickname --local
     --address <own-address> --json`. A terminal app asks only when its own code asks.

   When no prompt shows, read tccd's log (macos-tcc.md). Done when each cell passes, or tccd names
   why it cannot.
4. **Take each blocked cell to the user**, with tccd's reason and the options: leave it, change the
   host, or a direct `TCC.db` edit. Do the edit only on the user's yes, by macos-tcc.md's steps.
5. **Test imsg's own Automation only on the user's yes.** It needs a real send: ask for the
   recipient, then `as-imsg.sh send --to <address> --text "imsg permission test (ignore)"` once,
   and click **Allow** on the prompt. On `may_have_completed … retry is not safe`, find the
   message before any retry (gotchas).
6. **Re-test the whole table.** Remove test files, and quit apps you started. Done when every cell
   is ✅, or marked with its blocker and the user's choice.
7. **Report the table**, and log each grant and each `TCC.db` edit with `log-decisions` in the
   repo you work from.

## IMCore bridge (SIP-off hosts)

Typing indicators, read receipts, polls and the other private sends of upstream
[docs/advanced-imcore.md](https://github.com/openclaw/imsg/blob/main/docs/advanced-imcore.md) need
imsg's helper dylib injected into Messages.app. These are not privacy grants: finish the grant
table first. mac-mini-m2 runs the bridge (Q86).

1. **Check the gates.** `csrutil status` says disabled. `/opt/homebrew/opt/imsg/libexec/imsg-bridge-helper.dylib`
   exists (Homebrew ships it). `defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser`
   names the Messages user, because the bridge agent starts only after login. mac-mini-m2 also has
   `amfi_get_out_of_my_way=1` in `nvram boot-args`, against macOS 26+ library validation. A gate
   that fails goes to the user: SIP and boot-args need Recovery and a reboot.
2. **Inject.** `IMSG_LAUNCH_READY_TIMEOUT=60 imsg launch --json` restarts Messages with the helper.
3. **Keep it across reboots.** `/opt/homebrew/opt/imsg/libexec/imsg launch --install-agent --json`
   writes `~/Library/LaunchAgents/org.openclaw.imsg.bridge.plist`, which re-injects every 300 s
   when the helper is missing or stale. Install it through the `opt` path: the agent saves the path
   of the binary that ran, and `bin/imsg` is a wrapper that runs the versioned Cellar binary, which
   `brew cleanup` deletes.

Done when `imsg status --json` has `advanced_features`, `typing_indicators` and `read_receipts`
true and `helper_version` equal to `version`, and `launchctl print gui/$(id -u)/org.openclaw.imsg.bridge`
shows `last exit code = 0`. Before you use a bridge command, check its `selectors` entry in that
JSON: on macOS 27 some are false (`editMessage`, `deleteChat`, `leaveChat`).

## Gotchas

- **SSH needs no Contacts grant.** Over SSH, imsg reads the AddressBook SQLite files through
  sshd's Full Disk Access. Judge Contacts by `contacts_unavailable`; `source` says
  `local-addressbook` either way.
- **`open` from SSH leaks `SSH_*`** into the app, and imsg then takes the SSH path. `probe.sh`
  unsets them.
- **Terminal.app never asks for Contacts.** Its `Info.plist` has no `NSContactsUsageDescription`.
  Its Contacts cell needs a `TCC.db` row (macos-tcc.md).
- **"Policy disallows prompt."** On mac-mini-m2 (SIP off) tccd refused every Contacts prompt, for
  every parent. All four Contacts cells there came from `TCC.db` rows (personal-agent Q254, Q255).
  On every host, `node` gets the same refusal: its hardened runtime lacks the Contacts
  entitlement, so the node row's Contacts cell needs a `TCC.db` row (m6 test, 2026-10-27). That
  row is possible only with SIP off. With SIP on, when paseo's program has Full Disk Access, a
  `~/.local/bin/imsg` wrapper ahead of `/opt/homebrew/bin` on paseo's PATH that sets
  `SSH_CLIENT` (when unset) makes imsg read names from the AddressBook files. On m6 it gives
  node's imsg calls names; mark that cell ✅ (fallback) (personal-agent Q262).
- **A self-send can land in the phone-number thread.** A send to the user's email address was
  filed under their phone number, so imsg exited 1 with `may_have_completed … retry is not safe`,
  though the message went out. Find it with `imsg chats --limit 5` (newest `last_message_at`)
  and `imsg history --chat-id <id>`; send again only if it is missing (personal-agent Q256).
- **Upgrades drop path grants.** Grants on `libexec/imsg` and on mise's `node` match by path, so
  `brew upgrade imsg` or a new node version needs this skill again. The bridge agent handles its
  own upgrade: a helper whose version differs from the CLI's is replaced at the next check.
