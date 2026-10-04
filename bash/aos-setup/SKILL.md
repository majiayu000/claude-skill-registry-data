---
name: aos-setup
description: >-
  Bring a machine to a complete, verified AOS installation: the skills pack,
  MCP servers, gate hooks, memB (engine, MCP, ambient hook, WebUI), OpenWiki
  (CLI, auth, harness integrations, refresh daemon) and Synapse. Run once on a
  new computer, and again whenever something in the ecosystem stopped working.
category: bdb-core
risk: low
source: bdb
date_added: "2026-09-13"
---

# AOS Setup — Machine Level

Installing the AOS npm package is the easy half. The half that quietly fails is
everything around it: memB has no venv, the ambient memory hook was never
wired, OpenWiki has a CLI but no provider credentials, Synapse's binary is not
on `PATH`. The result is a machine where most skills work and the memory,
documentation and visualization layers silently do nothing.

This skill closes that gap: **measure first, then fix only what is broken.**

This is also where a **new agent harness** gets wired: adding Codex or
Antigravity to a machine that already runs Claude Code is this skill's job, not
a reinstall.

For per-project wiring — a folder's slug, its wiki, its memB binding — use
`/aos-project-init` after this one.

### What each harness can actually do

Portability is not uniform, and pretending otherwise is how people end up
believing memory works everywhere:

| | Skills | MCP | Hooks |
|---|---|---|---|
| Claude Code | `~/.claude/skills` | `~/.claude.json` | **yes** |
| Antigravity | `~/.gemini/config/skills` | `mcp_config.json` | **yes** (.agents/hooks.json / hooks.json) |
| Codex | `~/.codex/skills` | `config.toml` | **yes** (config.toml) |
| OpenCode | — | `opencode.jsonc` | no |
| Cursor / Roo | `bdb-skills` | `mcp.json` | no |

Claude Code, Google Antigravity, and OpenAI Codex have native hook support, allowing memB to inject ambient memory per prompt across all three harnesses. For hookless harnesses (Cursor, Roo, OpenCode, Windsurf), the same context arrives through the rule files that harness loads at start — see section 5 — which means it is as fresh as the last write, not as fresh as the prompt. Say so plainly rather than letting someone assume parity.

---

## 1. Measure

Run the doctor. It is read-only; it installs and edits nothing.

```bash
node skills/global_config/aos-setup/scripts/aos-doctor.mjs        # from the AOS repo
node ~/.claude/skills/aos-setup/scripts/aos-doctor.mjs            # from an installed copy
```

Flags: `--json` for machine-readable output, `--net` to also compare the
installed AOS version against npm.

It reports up to 29 checks across seven areas, each with the exact fix command.
The exact number varies by machine: the LaunchAgent rows are macOS-only, the
OpenWiki integrations row needs the CLI on `PATH`, the npm-version row needs
`--net`, and the optional-module rows appear only for modules the manifest
claims are installed.

| Area | What is verified |
|---|---|
| `prereq` | Node ≥ 22, `python3`, `git`, `uv`, `gh` |
| `aos` | `~/.agents/.bdb-manifest.json`, skills synced into each harness's skill directory |
| `hooks` | `go-gate.mjs`, `graph-gate.mjs`, `memb-inject.mjs` — present **and** wired in `~/.claude/settings.json` |
| `memB` | module, venv, `~/.MemBDB/memb.db`, WebUI on `:8088`, autostart, `memb-mcp` venv, MCP registration |
| `openwiki` | CLI, `~/.openwiki/.env` credentials, harness integrations, 2-hourly refresh daemon |
| `synapse` | binary on `PATH`, daemon on `:7781` |
| `memory` | identity layer (≥ 10 godmode facts), share of raw file chunks, stale paths |

Exit code is `0` only when every check passes. **Report the failing rows to the
user before changing anything**, then work the sections below in order — each
one covers a block the doctor can flag.

---

## 2. Machine configuration

Two things are machine-specific and ship with **no** value, because AOS is a
public package: one person's `web, media, infra` means nothing on someone
else's disk.

```bash
aos-config propose     # read this machine's layout, suggest nothing more
aos-config show        # what is configured now
```

`propose` looks for a workspace root (`~/dev`, `~/Projects`, `~/src`, `~/code`)
and offers its immediate subdirectories as the domain vocabulary. **Present the
proposal, do not apply it** — the user decides which of those are real domains
and which are just folders. Then ask for the memB `user_id`, which must never
be invented either.

```bash
aos-config set workspaceRoot ~/dev
aos-config set domains bdb-core,web,media,agents,infra
aos-config set userId <the user's memB id>
```

The result lands in `~/.agents/aos-config.json`. `/aos-project-init` reads it
to offer a domain per project and refuses to guess when it is missing.

### The identity layer (godmode facts)

With `workspaceRoot` and `userId` set, section 2 has one more job: the identity
interview, which fills memB's godmode layer — the standing facts about the
person this machine belongs to, injected into every prompt. The doctor's
`memory` rows report whether this layer exists.

Run it as a conversation, one question at a time: who the user is and their
role, company and brands, how the workspace is structured, and their ground
rules. Propose sources instead of asking blind — glob `WORKSPACE.md`,
`AGENTS.md` and `agents.md` directly under the configured workspace root (e.g.
`~/dev/WORKSPACE.md`) and offer each as source material before using it. Never
read the whole tree.

From the answers, draft **20–40 facts**, one sentence each, each ≤ 300 chars.
Show the full numbered list to the user and save only after explicit
confirmation — writes happen only on a literal GO.

Save each fact via the memb-mcp `add_memory` tool, exactly this shape:

```js
add_memory({ text: <fact>, category: "godmode", infer: false })
```

The shape is load-bearing. No `project_id`: omitting it stores the fact
globally, which is what makes it identity rather than project context.
`infer: false`: the text is stored verbatim, never LLM-rewritten. `user_id`
defaults to `bdb_developer`, which the ambient hook accepts as its baseline
user. Never write credentials or high-entropy strings into a fact.

---

## 3. Install or update AOS itself

```bash
npx -y @hybridlabor-api/aos@latest
```

The interactive installer asks which harnesses to target (Claude Code, Gemini /
Antigravity, Codex, OpenCode, Claude Desktop, …), which MCP servers to wire,
and which optional modules to pull. Non-interactive variants:

```bash
npx -y @hybridlabor-api/aos -y --platforms=2      # unattended, one platform
npx -y @hybridlabor-api/aos --dry-run             # show what it would do
```

Two things worth insisting on when the installer asks:

- **Pick every harness the user actually runs.** A harness left unselected gets
  no skills at all, which is the single most common "AOS doesn't work here".
- **Enable the optional modules** — memB, Synapse, OS Remote, Creator
  Extension, Tool Installer. They are what the doctor's memB and Synapse
  sections check for.

The installer writes `~/.agents/.bdb-manifest.json`. If that file is absent,
nothing was ever installed globally, no matter how many skills happen to sit in
a harness directory.

---

## 4. memB — memory that actually retains

memB is three separate pieces, and a machine can have any subset:

| Piece | Lives at | Doctor row |
|---|---|---|
| Engine + WebUI | `~/.agents/memB` (venv, `:8088` daemon) | `module`, `python venv`, `WebUI :8088`, `autostart` |
| MCP server | `~/.gemini/config/mcps/memb-mcp` (venv + `run.py`) | `memb-mcp server`, `memb_mcp registered` |
| Ambient hook | `~/.claude/hooks/memb-inject.mjs` | `memb-inject.mjs`, `memb-inject.mjs wired` |

The engine and the MCP come from the installer. If the venv is missing, repair
it in place rather than reinstalling everything:

```bash
cd ~/.agents/memB
uv venv --seed .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

`uv venv --seed` has been observed to create a venv without `pip`; that is why
`uv pip install --python <venv>` is the command above and not `python -m pip`.

The store lives in `~/.MemBDB/memb.db`. An empty store is normal on a fresh
machine — `/aos-project-init` seeds it per project.

---

## 5. The ambient memory hook

The hook is what makes memB *ambient* rather than something an agent has to
remember to query. On every prompt it reads the SQLite store directly and
injects the relevant memories as context. It fails open: any error exits `0`
and the prompt proceeds untouched.

Since v4.4.0 the installer ships `memb-inject.mjs` into `~/.claude/hooks/` and
wires it as an automated prompt hook across Claude Code (`UserPromptSubmit` in `settings.json`),
Google Antigravity (`PreInvocation` in `hooks.json` / `.agents/hooks.json`), and OpenAI Codex (`UserPromptSubmit` in `config.toml`). **v4.4.0's Quick Update did not** — it
refreshes skills and submodules, and hooks are harness plumbing rather than
skills, so a machine that already had AOS updated to 4.4.0 without ever
receiving the hook. Fixed in v4.4.1; a machine that took that update needs one
more run:

```bash
npx -y @hybridlabor-api/aos@latest
```

The wiring is merged into `~/.claude/settings.json`, Antigravity `hooks.json`, and Codex `config.toml`, never written over them:
user keys and foreign hook entries survive, and a re-run replaces the BDB entry
rather than adding a second copy.

The hook carries an `aos-hook-version:` line on its second line, and the doctor
compares it against what the installed release expects. That is why the row can
read *stale* rather than simply passing: a hook file that exists and is wired
can still be an old copy carrying a bug this version fixed. When you change the
hook in a way machines must pick up, bump that line and the expected value in
`aos-doctor.mjs` in the same commit — the test suite fails if the two disagree.

Unlike the two gate hooks, this one stays `$HOME`-anchored even in a project
harness — the memB store is machine-global, and pointing it at
`$CLAUDE_PROJECT_DIR` would make it fail on every prompt in any project the
harness was never installed into.

**On hookless harnesses** — Cursor, Roo, OpenCode, Windsurf — native hooks are not supported, so the same
context is written into the rule files that harness loads instead:

```bash
python3 ~/.agents/memB/memb_auto_inject.py --global      # RULES.md, CODEX.md, …
python3 ~/.agents/memB/memb_auto_inject.py --dir <repo>  # a project's AGENTS.md
```

It merges into a delimited block and leaves everything outside it alone. The
block carries the time it was written, because this path is only ever as fresh
as its last run.

Standing facts that should reach every prompt — persona, brand rules, house
style — go one per line into `~/.MemBDB/ambient-persona.txt`. Lines starting
with `#` are ignored. This file is deliberately *not* shipped: ask the user
what belongs there rather than inventing it, and never copy another machine's.

Verify by starting a session and checking that the first prompt carries a
`[memB Ambient Memory Context]` block.

---

## 6. OpenWiki

```bash
npm install -g openwiki@latest        # CLI, needs Node >= 22
openwiki auth <provider>              # google | openai | groq | openrouter | ollama | …
openwiki integrations list            # per-harness host integration status
openwiki integrations install claude  # repeat for codex / cursor / opencode
```

Credentials land in `~/.openwiki/.env`. Without them every wiki run fails at
auth — the CLI being on `PATH` proves nothing on its own.

The 2-hourly refresh daemon comes from the AOS installer when an OpenWiki API
key is supplied. To install it separately:

```bash
bash ~/.claude/skills/openwiki-skill/scripts/install_daemon.sh          # macOS / Linux
powershell -ExecutionPolicy Bypass -File install_daemon.ps1             # Windows
```

Wikis themselves are per-repository (`.openwiki/` in each project) — that is
`/aos-project-init`'s job, not this one's.

---

## 7. Synapse

The installer downloads the module, symlinks the binary to
`~/.local/bin/synapse` and registers a daemon on port `7781`. Two failure modes
the doctor separates deliberately:

- **Binary not found** — usually `~/.local/bin` missing from `PATH`. Add it to
  the shell profile; do not copy the binary somewhere else.
- **Port closed** — the daemon is not running. On macOS:
  `launchctl load -w ~/Library/LaunchAgents/com.bdb.synapse.plist`.

If no pre-built binary exists for the platform, build it:
`cd ~/.agents/bdb-synapse && go build -o synapse ./cmd/synapse/`.

---

## 8. The dashboard

`aos-dashboard` serves one page on `http://127.0.0.1:7900` showing every BDB
service live — memB, Synapse, the OpenWiki daemon, AO Orchestrator and RemoteOS
— with its version, port, LaunchAgent state, start/stop/restart, and its log
files inline. It polls every five seconds.

```bash
aos-dashboard                 # opens the browser
aos-dashboard --no-open       # just serve
aos-dashboard --port 7901     # if 7900 is taken
```

It binds to `127.0.0.1` only, and every control action is matched against a
fixed service table — an id or action the table does not contain is refused,
and no value from the request ever reaches a shell or a file path.

It also surfaces causes a port probe cannot see. The AO Orchestrator card
checks the code signature of `~/.local/bin/ao`: a binary rebuilt and copied
into place unsigned is SIGKILLed by AMFI at launch (exit 137), which otherwise
looks like a daemon that is simply down, with nothing in the log. The fix it
names is `codesign -s - -f ~/.local/bin/ao`.

Use it when the user asks what is running, or when a doctor row says a port is
closed and the question is why.

---

## 9. Confirm

Re-run the doctor. Do not report success from the fact that commands ran —
report the doctor's own count:

```bash
node skills/global_config/aos-setup/scripts/aos-doctor.mjs
# 26/26 checks pass. AOS is fully wired.
```

Anything still failing that the user deliberately does not want (no Synapse on
a headless server, no OpenWiki daemon on a laptop) is fine — say so explicitly
instead of leaving it looking broken.

Then hand off: **the machine is ready; per-project setup runs through
`/aos-project-init` in each repository.**

---

## Red flags

- Reporting "AOS installed" on the strength of a successful `npx` run. The
  installer succeeds happily with memB skipped and no hook wired.
- Overwriting `~/.claude/settings.json` instead of merging into its `hooks`
  object — that silently removes the go-gate.
- Treating an empty `~/.MemBDB` as a defect. It is the expected state until
  something is ingested.
- Copying the reference machine's persona file verbatim onto someone else's
  computer. Ask what their standing facts are.
- Saving godmode facts the user never saw — the interview shows the list
  first, always.
