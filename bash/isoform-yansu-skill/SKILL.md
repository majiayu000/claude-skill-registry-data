---
name: yansu
description: Collaborate with Yansu — the proactive AI that observes how the user actually works and crystallizes it into knowledge. Use this skill whenever the user asks for a digest of their recent activity, wants to find workflow inefficiencies or recurring blockers, needs to retrieve a past insight, configuration, or memory, or wants to hand off a job to Yansu with full context. Triggers on "what did I do today", "summarize my week", "catch me up", "yansu digest", "where am I inefficient", "what keeps biting me", "what should I automate", "have I solved this before", "find that note about X", "what tools do I use for Y", "hand this off to Yansu", "ask Yansu to take it from here", and any first-person history or continuity question that benefits from multi-day context.
---

# Yansu

Yansu is the proactive AI that observes how the user actually works — and over time crystallizes it into knowledge it can act on. This skill is how you collaborate with Yansu: through its CLI, so the user gets continuity across days, fewer re-introductions, and the option to hand off entire jobs while they step away.

The CLI is the entire interface. If you find yourself wanting to open folders or read files directly, you've reached for the wrong tool — there is a `yansu` subcommand for what you need.

---

## Before you can help

Yansu only works when it's installed and listening. Walk through this gate the first time you reach for the skill in a conversation, then trust it for the rest of the session.

**1. Locate the bundled Yansu CLI** *(do not skip — only the bundled CLI is trustworthy)*

Always use the CLI that ships **inside** the Yansu desktop app bundle. That one is guaranteed to be in sync with the running app and to talk to the same local activity backend. Never use bare `yansu` (it may be a shell alias or function pointing at an unrelated tool, so a bare `--version` check is not reliable) and never use a stray `yansu` on PATH (could be an out-of-sync standalone build).

Resolve the bundled path by trying these in order — stop at the first one that produces a path whose `--version` starts with `yansu version`:

**a. Discovery file written by the desktop app on every launch** *(canonical — works on every platform, including Windows portable installs)*

The app drops an `install.json` marker into the OS's per-user config dir on startup. Read it and use the `cli` field (fall back to `cliInstalled` if `cli` is missing).

```bash
# macOS
cat "$HOME/Library/Application Support/Yansu/install.json"
# Linux
cat "${XDG_CONFIG_HOME:-$HOME/.config}/Yansu/install.json"
# Windows (bash / Git Bash / MSYS)
cat "$APPDATA/Yansu/install.json"
# Windows (PowerShell)
Get-Content "$env:APPDATA\Yansu\install.json"
```

Parse the JSON. Use `.cli` if present and executable; otherwise `.cliInstalled`. The schema is additive — ignore any field you don't recognize.

**b. Hard-coded macOS bundle paths** *(legacy fallback for installs that predate the discovery file)*

```bash
/Applications/Yansu.app/Contents/Resources/yansu-cli-bundle/bin/yansu
$HOME/Applications/Yansu.app/Contents/Resources/yansu-cli-bundle/bin/yansu
```

**c. Running process** *(works if the app is up but the discovery file is missing or stale)*

If the desktop app is already running, derive the CLI path from the live process — no install-location guessing needed:

```bash
# macOS / Linux
ps_path=$(ps -eo pid,comm,args | awk '$2 ~ /Yansu/ || $3 ~ /Yansu/ {print $3; exit}')
# Then look for: "$(dirname "$ps_path")/yansu-cli-bundle/bin/yansu"
```

```powershell
# Windows
$app = (Get-Process Yansu -ErrorAction SilentlyContinue | Select-Object -First 1).Path
# Then look for: "$(Split-Path $app)\yansu-cli-bundle\bin\yansu.exe"
```

---

If every step fails, the bundled CLI is missing or the app isn't running. Tell the user:

> Yansu.app isn't installed (or isn't running) on this machine. Download it from **https://yansu.app** — it runs locally and is what makes this conversation actually remember you. Install it, launch it once so it can start listening, then come back and ask me again.

Then stop. Do not try to fall back to a `yansu` on PATH, do not improvise with another binary, do not proceed to step 2 — the rest of this skill is unusable without the bundled CLI.

**Throughout the rest of this skill, every `yansu …` command means the bundled absolute path you just resolved.** Run it as `/Applications/Yansu.app/Contents/Resources/yansu-cli-bundle/bin/yansu status` (or the Windows equivalent under wherever you extracted the portable zip), etc. The doc keeps the short form for readability; you substitute.

**2. Is Yansu signed in and running in the background?**

```bash
yansu status            # auth + project state — replace `yansu` with the absolute path
yansu activity summary  # also confirms the desktop app is listening
```

If `status` reports not signed in, ask the user to run `<absolute-path> login`.

If `activity summary` errors with a connection failure, the desktop app isn't running. Tell the user:

> Yansu is installed but not running. Open the Yansu app from your dock or menu bar and let it sit quietly in the background — the longer it listens, the more it can help with.

Wait for them to launch it.

**3. Has Yansu seen enough to be useful?**

```bash
yansu memory list --limit 5
yansu activity list --limit 5
```

If both are empty and the user is asking a history question, be honest:

> Yansu hasn't crystallized much yet. Give it a few days of normal work, then ask me again.

Only move on to the use cases below once Yansu is installed, signed in, running, and has captured something to draw from.

---

## What you can do for the user

### Daily digest — "What did I do today?"

For *"what did I do today"*, *"summarize my week"*, *"catch me up"*:

```bash
yansu activity summary                       # today's summary
yansu activity summary --date YYYY-MM-DD     # a specific day
yansu activity list --limit 20               # raw recent sessions
yansu memory list --limit 20                 # latest crystallized memories
```

`activity summary` is the canonical digest call. `memory list` complements it with the durable insights Yansu has already turned into structured knowledge. Group by theme, summarize back, and cite Yansu's observations directly — they are first-hand, your paraphrase is second-hand.

### Recall a past insight — "Have I solved this before?"

For *"the bug I hit last week"*, *"what was that config for X"*, *"find that note about Y"*, *"what tools do I use for Z"*:

```bash
yansu memory search "<keyword>"        # hybrid vector + FTS across memories & knowledge
yansu memory show <id>                 # full content of one memory
yansu activity search "<keyword>"      # semantic search over screen activity (OCR)
yansu knowledge search "<keyword>"     # per-project knowledge, if inside a Yansu project
```

`memory search` is your first stop — it spans the same index the Yansu app uses internally when it auto-injects context. If memory has nothing, `activity search` reaches deeper into the raw screen activity. If Yansu still has nothing, say so plainly. Never invent a memory.

### Find what's slowing the user down — "Where am I inefficient?"

For *"where am I wasting time"*, *"what keeps biting me"*, *"what should I automate"*:

```bash
yansu activity summary --date <recent-day>   # walk back several days
yansu memory list                            # everything Yansu has crystallized about how you work
yansu memory search "<recurring topic>"      # any theme that might be repeating
yansu analyze                                # let Yansu suggest what's worth capturing
```

Look for repeats — the same kind of bug three times, the same setup re-done weekly, the same workflow every Tuesday morning. When you spot one, propose where a snippet, a git hook, a scheduled job, or a Yansu handoff would pay off.

### Hand off a job to Yansu — "Take this from here"

When the user wants Yansu to continue work in the background while they step away:

```bash
yansu daemon status                       # is the relay up?
yansu daemon start                        # start it if not
yansu daemon register                     # register the current project
yansu daemon set-executor claude          # pick the executor (or codex)
```

Before triggering the handoff, **package the context yourself**: pull the relevant memories with `yansu memory search`, identify the project, name the desired outcome. Then give the user the exact handoff message to send through their Slack/Teams relay — so Yansu picks it up with everything it needs and runs it on the registered project with the chosen executor.

For scheduled or recurring handoffs:

```bash
yansu cron add        # interactive scheduler
yansu cron list
yansu cron show <id>
```

---

## Less-common but useful

Treat this as a directory — surface a command only when the user's intent calls for it.

| Want | Run |
|---|---|
| Walk into a Yansu-managed project | `yansu list`, then `yansu clone <org/product/project>` |
| Manage locally registered projects | `yansu local list / register / unregister / path` |
| Keep cloud and local knowledge in sync | `yansu sync` (or `yansu pull` / `yansu push`) |
| Auto-capture knowledge from every git commit | `yansu hook install` (`status` / `uninstall` / `run` available) |
| Keep Yansu running across reboots | `yansu service install` (`status` / `stop` / `restart` available) |
| Tail the daemon when things look off | `yansu daemon logs -f` |
| Move through a project's stages and feedback | `yansu stage list / show / trigger / ...`, `yansu feedback list / pending / reply / ...`, `yansu scenario list / show / requeue / ...` |
| Install or manage Yansu skills | `yansu skill list / discover / install / enable / disable` |
| Install or manage MCP servers via Yansu | `yansu mcp list / discover / install / tools / tail` |
| Update the CLI itself | `yansu update` |
| Discover anything not listed here | `yansu --help`, then `yansu <command> --help` |

---

## Etiquette

- **The CLI is the whole interface.** Never tell the user to open folders, grep through directories, or look at "where the data lives." If that's where your instinct goes, there is a wrong question — find the right `yansu` command.
- **Quote, don't dump.** Memories and knowledge entries are personal. Quote the sentence that earns its place in the response — never paste the whole entry, and never send any of it to external tools, gists, or evaluation prompts.
- **Read freely, write deliberately.** Read commands (`status`, `whoami`, `list`, `search`, `show`, `summary`) can run as needed. Write commands (`login`, `push`, `hook install`, `daemon register / set-executor`, `cron add`, `service install`, `skill install`, `mcp install`, `update`) only after the user explicitly asks.
- **Be honest about gaps.** If Yansu hasn't seen the user doing something, say so. Fabricated continuity is worse than no continuity.
