---
name: chrome-cdp-setup
description: Set up Google Chrome on macOS to always launch with the Chrome DevTools Protocol enabled (127.0.0.1:9222) via a Dock launcher app, so local AI agents (Playwright, Puppeteer, browser-use, OpenClaw) can drive the real logged-in browser with no per-connection approval prompt. Use when the user wants to enable a CDP/remote-debugging port for Chrome, pick between the flag, chrome://inspect, and extension routes, connect an agent to Chrome, test a CDP connection, diagnose a 404 from /json/version or an "Allow remote debugging?" dialog, or troubleshoot/revert an existing Chrome-CDP Dock setup.
---

# Chrome CDP Setup (macOS Dock launcher)

Makes the Dock's Chrome icon launch Chrome with `--remote-debugging-port` so any local
agent can connect over CDP. Chrome 136+ ignores that flag on the default profile
directory, and the Chrome 144+ `chrome://inspect` toggle that does work there makes a
human approve every connection — so the launcher points Chrome at a one-time APFS clone
of the real profile. All logins, bookmarks, and extensions carry over at near-zero disk
cost, the flags take precedence over the toggle, and nothing ever prompts.

Scripts live in this skill's `scripts/` dir; run them with absolute paths
(`~/.claude/skills/chrome-cdp-setup/scripts/...`).

## Which route

| Need | Route |
|---|---|
| Unattended agent loop, headless, CI, several tools sharing one browser | **This skill**: flags + a separate `--user-data-dir`, launched from the Dock wrapper. No prompts. |
| Real default profile, human at the keyboard, occasional | `chrome://inspect/#remote-debugging` toggle, then `PLAYWRIGHT_MCP_CDP_TIMEOUT=0 playwright-cli attach --cdp=chrome`; the human clicks Allow once per connection. See REFERENCE.md "Approval mode". |
| Real default profile, one tab, no Chrome prompt | `playwright-cli attach --extension=chrome` (Playwright extension). Per-tab access; its own approval popup takes a shared token via `PLAYWRIGHT_MCP_EXTENSION_TOKEN`. |
| Real default profile, whole browser, no prompt | Not possible in Chrome 136+. The profile clone is the closest thing. |

## Quick start

```bash
scripts/setup_chrome_cdp.sh              # full setup (default port 9222)
scripts/set_default_browser.sh           # optional: make it the default browser — one macOS dialog to click (--revert undoes it)
scripts/verify_cdp.sh                    # signals + one-line verdict naming the state and the fix
uv run --with playwright python scripts/cdp_agent_test.py   # external-agent smoke test
```

The Dock tile stays named "Google Chrome CDP" while Chrome runs, because the launcher
`exec`s Chrome and keeps the app identity. One consequence: macOS attributes Chrome's
own writes to the wrapper, so grant it App Management (System Settings ▸ Privacy &
Security) or Chrome's auto-update stays blocked. See REFERENCE.md "Which app is running".

## Setup workflow

1. Preflight: confirm `/Applications/Google Chrome.app` exists, `/Applications` is
   writable and Command Line Tools are installed (`xcode-select -p`); note profile size
   with `du -sh ~/Library/Application\ Support/Google/Chrome`.
2. Run `scripts/setup_chrome_cdp.sh [port]`. It is idempotent and:
   - quits Chrome cleanly and stops if anything still holds the port — flag mode binds
     it with no fallback. Open tabs come back on relaunch only if the profile restores
     the last session; otherwise they are one ⌘⇧T away (REFERENCE.md)
   - clones `~/Library/Application Support/Google/Chrome` → `Chrome-CDP` (`cp -Rc`;
     skipped if the clone already exists)
   - builds `/Applications/Google Chrome CDP.app`: a compiled stub that `exec`s Chrome
     with the flags, Chrome's icon, ad-hoc signed. Compiled because SIP refuses a script
     executable; `exec` because that keeps the Dock tile named Google Chrome CDP
     (REFERENCE.md "Wrapper app anatomy")
   - pins `--profile-directory` to the clone's last-used profile, so a multi-profile
     clone opens that profile instead of the picker — the picker leaves CDP with no
     default browser context and Playwright's `connect_over_cdp` fails at attach
   - swaps the Dock's Chrome tile for the wrapper (Dock prefs backed up first) and
     restarts the Dock
   - launches the wrapper, waits for `http://127.0.0.1:<port>/json/version`, and on
     Apple Silicon checks that Chrome came up native rather than under Rosetta
3. Confirm with `scripts/verify_cdp.sh [port]` — the last line must read `OK`. Any other
   verdict (`APPROVAL MODE`, `PORT STOLEN`, `PORT TAKEN`, `NOT LISTENING`, `DOWN`,
   `UNHEALTHY`) names the fix, and the exit status is 1.
4. Prove end-to-end with `cdp_agent_test.py` — it connects from an independent process,
   lists the real tabs, opens its own tab, rewrites the DOM, screenshots, and
   disconnects leaving Chrome running.

## Connecting agents

- Playwright: `chromium.connect_over_cdp("http://127.0.0.1:9222")`
- Puppeteer: `puppeteer.connect({ browserURL: "http://127.0.0.1:9222" })`
- playwright-cli: `playwright-cli attach --cdp=http://127.0.0.1:9222`. Not `--cdp=chrome`:
  that reads the *default* profile's `DevToolsActivePort` and cannot reach the wrapper.
- Raw WS: re-fetch `webSocketDebuggerUrl` from `/json/version` each launch (it rotates).
- Python agents need only `pip install playwright` or `uv run --with playwright` — no
  `playwright install` browser download, since they attach to the running Chrome.
- `Browser context management is not supported.` at attach means Chrome is sitting on
  the profile picker — see REFERENCE.md "Profile picker".
- A first attach to a browser that has been up for hours with dozens of tabs can exceed
  Playwright's 30 s connect timeout: it attaches to every target, and idle renderers
  answer slowly. Raise the timeout (`PLAYWRIGHT_MCP_CDP_TIMEOUT` for playwright-cli) or
  retry once; the retry is fast.

## Rules that prevent breakage

- Always start Chrome from the Dock icon. Spotlight, or a link click while Chrome is
  closed, launches the non-CDP default-profile instance — quit it and relaunch from the
  Dock. With the `chrome://inspect` toggle on, that instance also grabs port 9222 in
  approval mode: `/json/version` answers 404 and every connection prompts.
  `verify_cdp.sh` names this state. `set_default_browser.sh` takes the link click off
  that list by making the wrapper the default browser (one macOS consent dialog).
- Chrome's own "Relaunch to update" keeps the flags, so CDP stays up, but the process
  comes back as `Google Chrome.app`: a second Dock tile until the next quit, and the
  Dock tile then no longer names the wrapper. Quit and relaunch from the Dock when
  convenient (REFERENCE.md "Which app is running").
- Never run both instances at once (session divergence, duplicate extension connections).
- The CDP server takes a few seconds after launch: poll with
  `curl --retry 30 --retry-delay 1 --retry-all-errors`.
- The active profile may be `Profile N`, not `Default` — read `profile.last_used` from
  the clone's `Local State` before asserting the clone is broken.
- Loopback only: never add `--remote-debugging-address`. Any local process can drive
  the browser and read that profile's cookies — the machine is the trust boundary.
- On Apple Silicon, confirm the running Chrome shows `Arch=ARM64`
  (`lsappinfo info -app com.google.Chrome | grep -io 'Arch=[a-z0-9_]*'`; older macOS
  prints it lowercase). A stale LaunchServices record for the wrapper can silently run
  the whole browser under Rosetta at several times the CPU cost — see "Rosetta trap"
  in REFERENCE.md.

## Details

Gotchas, approval mode, the Rosetta trap, raw-CDP notes, and revert steps: see
[REFERENCE.md](REFERENCE.md).
