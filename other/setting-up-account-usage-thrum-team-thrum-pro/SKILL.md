---
name: setting-up-account-usage
description: "Use when the user wants to see account usage, quota, usage limits, rate limits or their plan usage, when thrum team shows no Accounts section or the line Usage not enabled on daemon, when account usage says not_installed, version_mismatch or unavailable, or when setting up quota-axi for the daemon and choosing which runtimes it reads."
---

# Setting Up Account Usage (quota-axi)

Account usage is off by default. When on, the daemon runs the pinned `quota-axi` every 15 minutes (and once at start)
and records used/remaining and reset time per account. It never installs, updates or fetches `quota-axi`. Some steps
need the USER at their own terminal: say so before you start.

## 1. Check the state

- `thrum team`: an `--- Accounts ---` section with `used`, `remaining`, `resets`, `last read` is a working reading. A
  line `<daemon-id>: Usage not enabled on daemon (setup: setting-up-account-usage skill)` means that other daemon has no
  reading: do this skill on that daemon. A local daemon with usage off prints nothing.
- Local daemon, usage on, no reading: `<daemon-id>: unavailable (<cause>)`. Look the cause up in the failure table.

## 2. Install the pin (needs Node 22.19 or newer)

- `npm install -g quota-axi@0.1.68`
- `quota-axi --version` must print exactly `0.1.68`. Any other version is reported as `version_mismatch`.
- The binary must be on the PATH the daemon was STARTED with (launchd or systemd PATH, not your shell's). Install into a
  directory already on it, or start the daemon from an environment whose PATH has npm's global bin directory.
  `thrum daemon restart` keeps the daemon's original environment, and a PATH set only in `.thrum/.env` does not
  override an existing one.

## 3. Choose the runtimes (ask the user)

The daemon reads only runtimes that have an agent registered on THIS daemon, and only those in
`daemon.account_usage_runtimes`. Empty or absent means `claude`, `codex`, `cursor`, `copilot`. `muse`, `antigravity` and
`opencode` are never read unless the user lists them.

- Find which of the three exist: `command -v muse`, `command -v agy`, `command -v opencode` show whether the CLI is
  installed (`muse` and `agy` are the launch commands in the runtime presets). The daemon's own test is different: an
  agent registered with that runtime on this daemon. An installed binary with no agent is not read.
- If one is installed, tell the user what reading it involves and let THEM decide. Never add it yourself.

| Runtime | What a reading involves |
|---|---|
| `muse` | Reading its quota also makes Muse's server return an API key; quota-axi discards it unread and rate-bounds the request. |
| `antigravity` | quota-axi launches the `agy` CLI (`agy -p "/quota"`). |
| `opencode` | Reports only the paid OpenCode Go plan. Needs an `opencode-go` key in OpenCode's own store (`opencode.db` or `auth.json`), sends that key to `opencode.ai`, runs `sqlite3 -readonly` (so `sqlite3` must be on the daemon's PATH). No Keychain. A user on free models or another vendor gets no OpenCode reading. |

Names are the runtime names above (`antigravity`, not `agy`). An unknown name is ignored and logged once at daemon
start; a list of only unknown names reads nothing.

## 4. Credentials: on macOS the user takes part (tell them before step 2)

quota-axi never logs in and never refreshes a credential for the daemon (the daemon passes `--no-credential-refresh`,
never `--allow-keychain-prompt`, and the child sees only `HOME` and `PATH`). On macOS, tell the user up front which of
their chosen runtimes will raise a Keychain prompt (table below) and that they approve it themselves in their own
terminal; do not try to do it unattended. Each chosen runtime must already be signed in, with its credential in the
default location under the user's `HOME`; a credential supplied only through an environment variable or a non-default
path is not seen by the daemon.

| Runtime | macOS | Linux (read from files, nothing to approve) |
|---|---|---|
| `claude` | Keychain item. One-time grant by the USER (below). | `~/.claude/.credentials.json` |
| `codex` | File `~/.codex/auth.json`; no Keychain. quota-axi may fall back to a read-only `codex` CLI probe. | `~/.codex/auth.json` |
| `cursor` | Keychain item (Cursor CLI). One-time grant by the USER. | `~/.config/cursor/auth.json` |
| `copilot` | Keychain item (Copilot CLI). One-time grant by the USER; falls back to the `gh` CLI's `hosts.yml` token. | Copilot apps auth file, then `~/.config/gh/hosts.yml` |
| `muse` | `~/.config/muse/auth.json`; when it records Keychain storage, a Keychain item and a USER grant. | `~/.config/muse/auth.json` |
| `antigravity` | No credential files; quota-axi asks the installed `agy` CLI (or running agy processes). | same |
| `opencode` | `opencode-go` key in OpenCode's store; no Keychain. | same |

macOS grant (human step, unconfirmed by any agent run): the USER runs `quota-axi --allow-keychain-prompt` (add
`--provider <name>` to limit it; read `quota-axi --help` first) in their OWN terminal and chooses "Always Allow" for
each Keychain prompt. The grant is stored in quota-axi's cache under `HOME`, which the daemon shares, so it carries
over. Do not run it for the user, do not run it in a shared tmux pane, and never read the Keychain yourself. Without the
grant those runtimes report unavailable with a reason; that is expected, not a failure.

On Linux there is no prompt: after the install and the config change nothing else needs the user, provided the CLIs are
signed in. Not confirmed on a real account: whether every file above exists for a given install.

## 5. Turn it on

Edit `.thrum/config.json` of the repo the daemon serves (from a worktree, the main repo's `.thrum`, named in
`.thrum/redirect`). `thrum config set` refuses these two keys (per-machine settings, not fleet-settable), so edit the
file.

```json
{ "daemon": { "account_usage_quota_axi": true, "account_usage_runtimes": ["claude", "codex"] } }
```

Leave out `account_usage_runtimes` for the default set. Then `thrum daemon restart`; the settings are read at daemon
start. To turn it off set `account_usage_quota_axi` to `false` and restart; the last reading stays.

## 6. Verify by effect

Within a minute of the restart, `thrum team` shows the Accounts section: `used`, `remaining`, `resets`, `last read`. A
`[stale]` mark means the last read failed or is old; the old values are kept and labelled, never shown as fresh. The
daemon log (`thrum daemon logs`) has `account usage (quota-axi): reading` or `unavailable` once per change.

## Failure table

| Shows | Cause | Fix |
|---|---|---|
| `not_installed` | `quota-axi` not on the daemon's PATH | Step 2, then restart from the right environment |
| `version_mismatch` | Installed version is not `0.1.68` | `npm install -g quota-axi@0.1.68` |
| `timeout` | A run took longer than 90 s | Check network and sign-ins; the next run is in 15 min |
| `non_json`, `exit status N` | quota-axi misbehaved | Run `quota-axi --version` as the user; reinstall the pin |
| `auth_required` or `[auth error]` | The provider is signed out | The user signs in to that CLI; quota-axi does not log in |
| unavailable with a Keychain reason (macOS) | No grant yet, or it was denied | The user does the grant in step 4 |
| `[stale]` after a failure | Last read failed | Fix the cause above; it clears on the next good read |
| nothing for a runtime | Not in `account_usage_runtimes`, or no agent of that runtime on this daemon | Step 3 |
