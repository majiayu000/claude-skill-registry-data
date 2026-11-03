---
name: slack-credentials
description: Diagnose or add the browser-session credentials that claude/bin/slack.py uses for a Slack workspace. slack.py refreshes them from Chrome by itself; use this when it still reports not_authed, invalid_auth or token_revoked, when adding a workspace, or when Pablo asks about refreshing Slack tokens. Not for Slack's own OAuth apps or bot tokens.
---

# Slack session credentials

`claude/bin/slack.py` authenticates as Pablo with his browser login: the
`xoxc-…` token and Slack's `d` cookie (`xoxd-…`). Slack invalidates that login
whenever the browser session ends (sign-out, email change, forced re-login).

## Normal case: nothing to do

When Slack rejects the stored pair, slack.py calls `claude/bin/slack_chrome.py`,
which reads the current `d` cookie from Chrome's cookie database (every
profile; decrypted with the Chrome Safe Storage key), derives the
token from the workspace's `/ssb/redirect` page, verifies it with `auth.test`
and caches the pair in `~/.cache/slack-chrome/<domain>.json` (0600). It then
retries the request. No agent, browser tool or Pablo is involved. Never ask
Pablo to copy a token or cookie by hand while this works: a recurring manual
refresh is a defect (`claude/context/secrets.md`).

## When it still fails

slack.py prints `could not read credentials from Chrome: …`. The reasons, and
what to do:

- **No Chrome profile is signed in to the workspace**: Slack logged Pablo out
  of the browser. Ask him to open the workspace in Chrome and sign in; then
  rerun the command. That is his only possible job.
- **Keychain access to Chrome Safe Storage was refused**: macOS asked and was
  denied. Ask Pablo to run the command once himself (`! python3
  claude/bin/slack.py -w WORKSPACE channels`) and click **Always Allow**.
- **Unsupported Chrome cookie encryption** or **integrity check failed**:
  Chrome changed its format. Fix `slack_chrome.py`; meanwhile use the manual
  fallback below.

## Adding a workspace

Add an entry to `WORKSPACES` in `slack.py` with its `domain`
(`<subdomain>.slack.com`) and a 1Password fallback source (see
`claude/context/secrets.md`). With Pablo signed in to it in Chrome, the first
rejection, or `slack_chrome.refresh(DOMAIN)`, fills the cache. Verify with
`python3 claude/bin/slack.py -w WORKSPACE channels | head -3`.

## Manual fallback (only if slack_chrome.py is broken)

1. Token, agent alone: in that workspace's Slack tab (Claude in Chrome, per the
   `chrome-use` skill), run a top-level page script that finds the team in
   `JSON.parse(localStorage.localConfig_v2).teams` by `domain`, calls `await
   navigator.clipboard.writeText(t.token)` and returns only the length and
   whether it starts with `xoxc-`; never the token. Then run `op-clipboard-store
   --vault Automation --account my.1password.com --title ITEM --field token
   --prefix xoxc- --token --force` at once.
2. Cookie, Pablo: DevTools → Application → Cookies → https://app.slack.com →
   row `d` → double-click Value → ⌘A ⌘C; store it with `--field cookie
   --prefix xoxd-`. Ask for one job per message; never have him paste a
   command into Emacs while a credential is on the clipboard.
