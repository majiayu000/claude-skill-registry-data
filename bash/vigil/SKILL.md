---
name: vigil
description: >
  macOS-native self-supervising watchdog that monitors a project autonomously in the background.
  Launch it once and it keeps watching after you close the terminal, sleep, or restart — a launchd
  agent periodically runs read-only health probes (tests, build, dependency audit, a localhost
  health URL, git drift, disk space) and fires native macOS notifications plus an optional spoken
  summary when something changes or breaks. Read-only by default with code-enforced safety rails;
  no LLM runs in the watch loop. Use when the user wants to "watch", "monitor", or "keep an eye on"
  their project, asks to "notify me when" tests break or the build fails, wants a "self-watching"
  or "macOS background" monitor or an overnight/unattended health guardian, or wants to install,
  check on, triage, or stop a background watcher. Has a second mode — "task completion": give a
  plain-language task and Vigil periodically uses a read-only AI judge to check whether it's done,
  then notifies you and uninstalls itself (one-shot). Use task mode when the user says "tell me when
  this task is done", "check if X is finished", "watch until the feature is complete", or "let me
  know when the work is done". Configured via vigil.config.json in the project root.
user-invocable: true
argument-hint: "[install | status | triage | stop | probe <name> | task \"<description>\"]"
---

# Vigil

You set up and operate a **macOS-native self-supervising watchdog**. The operator launches it once;
it then watches their project on its own — surviving terminal close, sleep, and restart — and
notifies them natively when something changes or breaks. **launchd owns the loop**, not the Claude
session: a per-user LaunchAgent runs `cli.mjs tick` every N minutes, and each tick is **pure,
deterministic Node — no LLM in the loop**, so it costs nothing and works offline while watching.

You are involved only at the **edges**: at **setup** (detect the project, design good probes,
install the agent) and on **on-demand triage** (the operator later asks "what broke?"). You are
**read-only by default** with code-enforced safety rails — you never commit, deploy, or run
destructive commands.

## Prerequisites

Verify in order:

1. **macOS**: Run `uname -s` — must be `Darwin`. Vigil relies on `launchd`, `osascript`/`say`,
   and `caffeinate`. If not macOS, stop and tell the operator Vigil is macOS-only.
2. **Node.js**: Run `node --version`. The persistence CLI needs Node 18+.
3. **Config (optional at first)**: There may be no `vigil.config.json` yet — that is expected;
   you build one in Step 2. Read `references/config-schema.md` for the full schema and
   `references/macos-gotchas.md` for the launchd/notification/sudo caveats.

## Two Tools

### 1. Claude's built-in tools — detect, design, triage

Use Read, Glob, Grep, and read-only Bash to detect the project type, propose sensible probe
commands, and later triage a failing probe by reading the offending code.

### 2. Persistence + launchd CLI

```bash
node <skill-directory>/scripts/cli.mjs <command> [args...]
```

All commands output JSON to stdout. The launchd loop calls `tick` directly — no model involved.

## CLI Command Reference

| Command | Description | Input |
|---------|-------------|-------|
| `config` | Resolved config (merges `vigil.config.json` + defaults), emits `_configFound` | — |
| `init` | Write a starter `vigil.config.json` (refuses overwrite without `--force`) | stdin: probes JSON |
| `task` | **Task mode**: one command — write a one-shot AI-judge config for a plain-language task and install it | `"<description>"`, `--interval`, `--model`, `--speak`, `--force` |
| `install` | Generate + load the launchd agent so it watches across restarts (`--dry-run` previews) | — |
| `status` | Is it watching? launchd loaded, last/next run, heartbeat staleness, failing probes | — |
| `tick` / `run-once` | One watch cycle: run probes → compare to last snapshot → record → notify on change. launchd calls this | `--no-notify`, `--probe <name>` |
| `probe <name>` | Run one probe ad hoc with stdout/stderr tail; no snapshot, no notify (triage) | `<name>` |
| `history` | Recent tick events for trend/check-in | `--limit N` |
| `notify` | Fire a TEST notification (+ optional `--speak`) to verify macOS permission | `--message`, `--speak` |
| `halt` / `resume` | Pause/unpause ticks without uninstalling (touches `.vigil/HALT`) | — |
| `stop` / `uninstall` | Unload + remove the launchd agent | `--keep-plist` |

When invoked from launchd, every command receives `--project <abs>` so it never relies on `cwd`.

## Execution Protocol

### Step 0: Load configuration

```bash
node <skill-directory>/scripts/cli.mjs config
```

If `_configFound` is `false`, there is no config yet — go to Step 1 to build one. If `true`, an
existing watcher is configured; branch on what the operator asked (the argument-hint verb):
`status`/`triage` → Step 5/6, `stop` → Step 7, otherwise re-`install` from Step 3.

### Step 1: Verify macOS + prerequisites

```bash
uname -s            # must be Darwin
node --version
sw_vers -productVersion
```

If `uname -s` is not `Darwin`, stop here — Vigil only runs on macOS.

### Step 2: Detect the project & design probes

Inspect the project to propose probes tailored to its stack. Read in parallel:

```bash
ls -a
cat package.json 2>/dev/null
```

Use Glob/Grep to confirm which test/build scripts actually exist and whether there's a dev-server
health endpoint. Propose probes by stack:

- **Node/JS** → `npm test`, `npm run build`, `npm audit --omit=dev` (only scripts that exist in `package.json`).
- **Python** → `pytest -q`, `pip-audit`.
- **Go/Rust** → `go test ./...` / `go build ./...`, or `cargo test` / `cargo build`.
- **Health URL** → if a dev server / port is configured, add an `http` probe to `http://localhost:<port>/health` (or `/`).
- Always add a `git-drift` probe and a `disk` probe.

Present the proposed probe list, interval, and notification settings, and **ask the operator to
confirm or edit**. Make clear that every `shell` command you propose will be added to
`safety.commandAllowlist` — and nothing outside that allowlist can ever run. Only after they
confirm, write the config:

```bash
echo '{"schedule":{"intervalMinutes":30},"notifications":{"enabled":true,"minSeverity":"medium","speak":false},"probes":[{"name":"tests","type":"shell","command":"npm test","severity":"high","timeout":120000},{"name":"git-drift","type":"git","severity":"low"},{"name":"disk","type":"disk","threshold":"10GB","severity":"medium"}]}' \
  | node <skill-directory>/scripts/cli.mjs init
```

Expected:
```json
{ "command": "init", "status": "ok", "path": "/abs/vigil.config.json", "created": true, "probeCount": 3 }
```

Then validate the config with one full pass — **no notifications, no snapshot pollution**:

```bash
node <skill-directory>/scripts/cli.mjs tick --no-notify
```

Review `results[]`. If a probe is `skipped` (e.g. a command not on the allowlist) or fails due to
mis-detection (wrong command, wrong port), fix the config — re-run `init --force` with corrected
probes — and re-run. A probe legitimately failing (e.g. tests currently red) is fine; a
`skipped`/`error` from bad config is not. Do not install a config that errors on setup.

### Step 3: Install the launchd agent

```bash
node <skill-directory>/scripts/cli.mjs install
```

Expected:
```json
{ "command": "install", "status": "ok", "label": "com.vigil.<slug>",
  "plistPath": "/Users/me/Library/LaunchAgents/com.vigil.<slug>.plist",
  "intervalMinutes": 30, "wakeForRun": false, "loaded": true, "kicked": true,
  "notes": ["Notification permission may need approval on first fire — run `notify --test` and click Allow.",
            "wakeForRun=false: probes run on the next interval after the Mac wakes ..."] }
```

To show exactly what gets installed first, run `install --dry-run` (returns the plist XML and the
`launchctl` commands without loading). **Relay the `notes[]` honestly** — especially that with
`wakeForRun:false`, Vigil watches whenever the Mac is awake but does not wake a sleeping Mac. If
the operator wants guaranteed overnight runs, surface the exact `sudo pmset repeat wake ...`
command from `references/macos-gotchas.md` for them to run (Vigil never runs sudo itself).

### Step 4: Verify it's watching + test the notification

```bash
node <skill-directory>/scripts/cli.mjs status
node <skill-directory>/scripts/cli.mjs notify --test
```

`status` should show `"watching": true, "launchdLoaded": true`. Ask the operator whether the macOS
banner from `notify` appeared. If not, relay the `note`: macOS notification permission must be
granted to the terminal app (or Script Editor / terminal-notifier) under System Settings →
Notifications, and Focus/Do-Not-Disturb suppresses banners. Vigil keeps watching either way — the
event log is the source of truth.

### Step 5: How the operator checks in later

Tell them they can return any time — even with no terminal open — and run:

```bash
node <skill-directory>/scripts/cli.mjs status          # is it still watching? what's failing now?
node <skill-directory>/scripts/cli.mjs history --limit 10
```

A notification fires **only when a probe's state changes** (newly broke / recovered / git drift
changed), never every interval — so silence means steady state.

### Step 6: On-demand triage ("what broke?")

When the operator later asks you to investigate a failing probe:

```bash
node <skill-directory>/scripts/cli.mjs status            # find the failing probe name(s)
node <skill-directory>/scripts/cli.mjs probe <name>      # re-run it, get stdout/stderr tail
```

Then diagnose with built-in tools: read the error from `result.stderrTail`, Grep/Read the offending
files, and explain the root cause and a proposed fix. **Do not auto-apply fixes or commit** — Vigil
is read-only; propose the change and let the operator decide. After they fix it, the next `tick`
(or a manual `probe`) confirms recovery and the next change-triggered notification announces it.

### Step 7: Stop / uninstall

```bash
node <skill-directory>/scripts/cli.mjs stop
node <skill-directory>/scripts/cli.mjs status            # confirm "watching": false
```

This unloads the LaunchAgent and removes its plist. `vigil.config.json` and `.vigil/` remain so the
operator can re-`install` later; to discard collected history, they can `rm -rf .vigil` (don't run
destructive deletes yourself unless they explicitly confirm). To pause without uninstalling, use
`halt` / `resume`.

## Mode B — Task completion (AI judge, one-shot)

Use this when the operator wants *"tell me when this task is done"* rather than *"tell me when
something breaks"*. Instead of health probes, Vigil watches a single **plain-language task** and,
each tick, asks a **read-only AI judge** whether it's complete. When it is, Vigil notifies and
**uninstalls itself** (one-shot).

### One command

```bash
node <skill-directory>/scripts/cli.mjs task "create a file named DONE.md in the repo root" --interval 15
```

This writes a one-shot `vigil.config.json` (a single `task` probe + `schedule.oneShot: true`) and
installs the launchd agent — equivalent to running Mode A's `init` + `install`. Flags: `--interval
<min>` (default 15), `--model <alias>` (default `haiku`), `--speak`, `--force` (replace an existing
config). Phrase the task as a concrete, verifiable outcome ("all components in `src/forms/` have
TypeScript types", "the `/health` endpoint returns 200", "tests in `auth.test.ts` pass").

### How the judge works

Each tick spawns `claude -p` headless with a strict read-only prompt and a JSON schema, and parses
the verdict `{ done, confidence, reasoning }`:

```bash
echo "<judge prompt>" | claude -p --output-format json --json-schema '{...}' \
  --permission-mode dontAsk --allowedTools "Read,Grep,Glob" --model haiku --add-dir <project>
```

`done && confidence ≥ threshold` ⇒ probe `ok` (task complete); otherwise `fail` (not yet). The judge
gets only Read/Grep/Glob — it inspects, never edits. Vigil only **judges** completion; it does not
perform the task (you, or a separate coding session, do the work).

### Lifecycle & check-in

- Setup: run the `task` command, then verify with `status` + `notify --test` (Steps 3–4 of Mode A).
- While not done: silent (the not-done baseline doesn't notify).
- When judged done: a **"✅ Task done"** notification fires (message = the judge's reasoning), a
  `completed` event is logged, and the launchd agent self-uninstalls (`status` → `watching:false`).
- Operator can check progress any time with `status` / `history`, or stop early with `stop`.

### Honest caveats (relay these)

- **There IS an LLM in this loop** (unlike Mode A). Each tick is a full headless Claude run that
  **costs tokens** (~$0.05–0.15 with `haiku`). Pick the interval consciously.
- Needs `claude` on PATH and working auth under launchd (the plist sets `HOME` + adds
  `~/.local/bin`; uses the existing subscription, no API key on a normal Mac). Fallbacks in
  `references/macos-gotchas.md` if auth fails.
- The judge can be wrong — the notification carries its reasoning so the operator can verify; the
  `.vigil/` state is kept after the one-shot stop for review.

## Important Notes

### Read-only by default — code-enforced, not prompt-enforced
- Probes are health checks, never mutations. Shell probes spawn with `{ shell: false }` and an argv
  array — no shell, no metacharacter evaluation.
- **Only allowlisted shell commands run.** A `shell` probe whose command is not an exact match in
  `safety.commandAllowlist` is skipped (`status: "skipped"`). You add a command to the allowlist
  only with the operator's explicit confirmation in Step 2.
- **No commits, deploys, or destructive ops.** With `blockDestructive` (default on), even an
  allowlisted command is rejected if it matches the denylist (`rm`, `git push`, `git commit`,
  `sudo`, `npm publish`, `deploy`, `kill`, output redirection `>`, mutating HTTP verbs, …).
- `http` probes are GET-only and localhost-only unless `safety.allowRemoteHttp` is explicitly set.
- Vigil only ever writes inside `.vigil/` and the single launchd plist.

### No LLM in the loop
- launchd invokes `tick` directly; it is deterministic — run probes, compare, record, notify. No
  model is in the overnight loop, so watching is free and offline. Claude is only involved at setup
  (Step 2) and on-demand triage (Step 6), both operator-initiated.

### Sleep / wake honesty (sudo)
- By default Vigil does not wake a sleeping Mac (`wakeForRun:false`); probes due during sleep run on
  the next interval after wake (launchd coalesces missed runs into one). This needs no permissions.
- Guaranteed overnight wakes require `sudo pmset repeat wake ...` (and AC power for a closed lid).
  **Vigil never runs sudo** — surface the exact command for the operator to run.

### Anti-spam notifications
- A notification fires only on a state **transition** above `notifications.minSeverity`. A probe
  that stays broken does not re-notify each interval.

### Full uninstall
- `stop` unloads + removes the LaunchAgent plist. `.vigil/` and `vigil.config.json` stay; delete
  `.vigil/` to discard history. Re-run `install` any time to resume.
