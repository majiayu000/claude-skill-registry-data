---
name: chrome-use
description: "Rules for driving Pablo's Chrome. Use before the first browser step of any task: Claude in Chrome (mcp__claude-in-chrome__* tools), the Codex Playwright MCP browser_* tools or desktop control-chrome, or any work on a logged-in site; also before activating, raising or opening a Chrome window or profile. Not for web search or plain HTTP fetches."
user-invocable: false
---

# Chrome use

These rules apply to every agent that drives Pablo's Chrome: Claude in Chrome
(`mcp__claude-in-chrome__*`), the Codex CLI's Playwright MCP `browser_*` tools,
and the Codex desktop app's Chrome plugin (`control-chrome`). Where the vendor
skills (`claude-in-chrome`, `chrome-browser`, `control-chrome`,
`chrome-troubleshooting`) differ from them, these rules take precedence.

## When to use the browser

For background web research, use the web search/browsing tool and the mapped
service clients or direct public downloads (`claude/context/service-access.md`).
Do not switch to Pablo's live Chrome because an HTTP request fails or a site
presents a challenge, unless a skill's documented browser step calls for it
(such as `download-paper`'s `needs-browser` job).

When a task needs Pablo's logged-in accounts or a site with no other agent
path, use the browser without asking: Pablo has authorized this standing use
and does not want to repeat it. Each agent uses its own browser control:

- Claude: Claude in Chrome.
- Codex CLI: the `playwright` MCP server's `browser_*` tools, which drive
  Pablo's Chrome through the Playwright MCP Bridge extension. If they are
  missing, say so.
- Codex desktop app: the Chrome plugin through its `control-chrome` skill and
  browser client. Verify the connection with a read-only tab listing before
  navigating. A failed generic Playwright or guessed CDP connection does not
  show that this plugin is unavailable.

To fill in a form for Pablo, take his name, date of birth, contact details
and address from `/Users/pablostafforini/My Drive/dotfiles/claude/context/personal-details.md`
instead of asking him. Card numbers, passport numbers and passwords are not
there and stay out of agent-typed fields; Pablo's permission does not change
this, so do not ask for it. When a form needs one of them, say so at the start,
fill in everything else, leave it unsubmitted, and tell Pablo which tab and
Chrome profile window to finish it in.

## Never steal focus

Pablo is working at the same machine. Never bring Chrome or one of its windows
to the front.

- Get your own tab through the browser tool's own calls (Claude in Chrome:
  `tabs_context_mcp` with `createIfEmpty`, `tabs_create_mcp`). That is the
  normal start, needs no permission, and is allowed even when the extension
  puts its tab group in a new window. Never open windows any other way, and
  never ask to: a window does not fix a page stall.
- Work only in your own tabs. Claude in Chrome cannot use tabs Pablo opened
  himself, so never offer to. When a site needs a sign-in in your tab (1Password
  web signs in per tab), navigate your tab there and ask Pablo to sign in in
  that tab, naming it and its Chrome profile window.
- Do not click links or buttons that open a new tab or window (Chrome
  activates them). Read the link's `href` and navigate your own tab to it.
- Never raise, activate or reorder Chrome windows: no AppleScript or
  `osascript`, System Events, `open -a`, or `chrome-profile-open`.
- Never fall back to screenshots of the desktop or coordinate clicking outside
  the browser tools.
- If a tab sits in a background window and input to it fails, or Pablo must act
  there (sign-in, 2FA, a permission prompt), tell him which Chrome profile
  window holds it, by its alias in `claude/chrome-extension-profiles.json`
  (for example `tlon`), and let him switch to it.

`chrome-profile-open <alias> URL` is only a launcher for a page Pablo asks to
have opened manually; it activates Chrome. Configure its aliases with
`chrome-profile-open --setup <alias>`. Project wrappers may call it when manual
opening is the requested action. The only automated caller is the Claude hook
`chrome-bridge-recover.py`, which uses `--background`.

## Classify a failure before recovering

A communication failure means setup, browser selection or the tab listing
(`tabs_context_mcp`, `browser.tabs.list()`, `browser_tabs`) fails.

- Claude: the `chrome-bridge-recover` hook reopens this account's Chrome
  profile in the background and says whether to retry. Retry while it says to;
  report a connection problem only once it says the profile has been open 60 s
  and the extension still does not answer. This replaces the vendor skills'
  "stop after two or three attempts".
- Codex: run the plugin's or server's documented connection checks, except
  any step that opens a window (such as `open-chrome-window.js`); skip that
  step. If communication still fails, fail closed and report which check
  failed.

Once a browser is selected and a tab exists, a navigation timeout ("Timed out
waiting for tab … to navigate"), a hung page read, or `js execution timed out;
kernel reset` is a page or REPL failure. Connection checks pass and prove
nothing about it. Recover without asking: read the tab again; after a kernel
reset, rerun the bootstrap and rebind the browser; then open a fresh tab from
that browser and retry the navigation once. If it fails again, report it.

Challenge-protected hosts (DDoS-Guard, Cloudflare; for example Anna's Archive)
can outlast the navigation's load wait while their interstitial runs, so a
timeout there is expected: read the tab until its title changes before calling
the page unavailable. Treat it as a communication failure only if a fresh tab
listing also fails.
