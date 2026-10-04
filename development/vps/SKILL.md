---
name: vps
description: Manage the ZAO Telegram bot fleet (ZOE, ZAO Devz, ZAOstock, team bots) on VPS 1 via SSH, or send messages to ZOE via Telegram. systemd user units, one dispatcher.
---

# VPS — ZAO Bot Fleet Remote Management

Two modes of interaction:
- **SSH direct** → Run commands on the VPS via `ssh zaal@31.97.148.88 "command"` (system changes, config, debugging, status, deploys)
- **Telegram** → Generate copy-paste messages for ZOE (task instructions, context updates, questions)

You HAVE direct SSH access as `zaal@31.97.148.88`. Use the Bash tool to run commands remotely.

> **Architecture note (2026-05-04 cutover).** The old openclaw Docker container + 7-agent squad (ZOEY/BUILDER/SCOUT/WALLET/FISHBOWLZ/CASTER) was **decommissioned**. Do NOT reference, restart, or `docker exec` into `openclaw-openclaw-gateway-1` — it is gone. The fleet now runs as **systemd user units** under the `zaal` account, each a `tsx`-run Node process from a ZAOOS clone. No Docker, no openclaw CLI, no `/home/node/openclaw-workspace/`. See `CLAUDE.md` → "Primary Surfaces" and `research/agents/601-agent-stack-cleanup-decision/`.

## VPS Environment

```
VPS: Hostinger KVM 2, Ubuntu 24.04, 31.97.148.88, user `zaal`
Runtime: systemd USER units (systemctl --user ...), processes run as zaal via tsx
Repo (main ZAOOS clone): /home/zaal/zao-os   (per bot/src/zoe/posts/README.md)
ZAOstock bots clone:      /home/zaal/zaostock-bot
Node tooling: tsx, npm, git, gh (authenticated as bettercallzaal)
LLM: Minimax (local API; see the `minimax` skill)
```

### Live systemd user units (verified against `bot/systemd/` + bot READMEs)

| Unit | What | Source | Entry |
|------|------|--------|-------|
| `zoe-bot` | **ZOE** — `@zaoclaw_bot`, the single concierge/dispatcher | `bot/src/zoe/` | `bot/src/index.ts` (`npm start` → `tsx src/index.ts`) |
| `zao-devz-stack` | **ZAO Devz** — `@zaodevz_bot`, group dispatch + hourly tip | `bot/src/devz/` | `bot/src/devz/index.ts` |
| `zaostock-bot` | **ZAOstock** — `@ZAOstockTeamBot`, festival team coordination | `bot/` (root) | `npm run start` |

`zao-team-bots` (the brand bots in `bot/src/teams/`) was retired 2026-06-29; brand voices are ZOE persona blocks now (CLAUDE.md, "Decommissioned"). If `systemctl --user list-units` still shows it, that is a leftover to report, not a live bot.

Hermes (`@zoe_hermes_bot`, autonomous fix-PR pipeline) lives in `bot/src/hermes/` — confirm its unit name on the box before acting (`systemctl --user list-units '*hermes*'`); it is not in the committed `bot/systemd/` set.

### ZOE's filesystem (host, NOT a container)

ZOE reads/writes its memory under `~/.zao/zoe/` (`ZOE_HOME`, override via `$ZOE_HOME`). These are plain files on the host, writable by `zaal` — no Docker, no root needed.

```
~/.zao/zoe/persona.md          ZOE identity + VOICE + ANTI-PATTERNS + FORMAT RULES
                               (seeded from PERSONA_DEFAULT in bot/src/zoe/memory.ts;
                                RE-READ EVERY TURN — edits take effect with no restart)
~/.zao/zoe/human.md            human context cache, refreshed daily
~/.zao/zoe/recent/<chat_id>.json   last-N turns per chat (FIFO ring buffer)
~/.zao/zoe/archive/<scope>/<yyyy-mm>.jsonl   rolled-off history
~/.zao/zoe/tasks.json          open task queue (global)
~/.zao/zoe/groups.json         configured groups (managed by /zoe-group-* commands)
~/.zao/zoe/bootloader-template.md   child-bot seed (brand bots, if one is ever brought back)
```

> **persona.md vs code.** A persona/human/tasks edit takes effect on ZOE's **next turn** automatically (these files are re-read per turn) — no restart. A **code** change (anything under `bot/src/`) needs `git pull` + `systemctl --user restart zoe-bot`.

## Routing: SSH or Telegram?

| Intent | Method |
|--------|--------|
| Check health, logs, unit state | SSH direct — run it |
| Deploy code, change config, install packages | SSH direct — run it |
| Edit `persona.md` / `human.md` / `tasks.json` | SSH direct — run it (no restart for persona/human/tasks) |
| Tell ZOE to build something, start a task | Telegram copy-paste |
| Ask ZOE a question, give feedback | Telegram copy-paste |
| Fix a bug in bot code | SSH direct — deploy + restart |

**Rule of thumb:** touches the filesystem, systemd, or repo → SSH direct. A conversation with ZOE → Telegram.

## SSH Patterns

**Single command:**
```bash
ssh zaal@31.97.148.88 "systemctl --user status zoe-bot --no-pager"
```

**Read a ZOE memory file:**
```bash
ssh zaal@31.97.148.88 "cat ~/.zao/zoe/persona.md"
```

**Append to a workspace file (heredoc — no Docker wrapping needed):**
```bash
ssh zaal@31.97.148.88 "cat >> ~/.zao/zoe/persona.md << 'EOF'
<content>
EOF"
```

**Read before overwrite, always.** For structured files (`tasks.json`, `groups.json`) prefer a targeted `jq`/python edit over a blind overwrite.

## Mode: status

**Run these directly via SSH using the Bash tool.** Run them in parallel for speed. All read-only.

```bash
# Unit health for the whole fleet
ssh zaal@31.97.148.88 "systemctl --user status zoe-bot zao-devz-stack zaostock-bot zao-team-bots --no-pager | grep -E 'Loaded|Active|●' "
# ZOE identity (first lines of live persona)
ssh zaal@31.97.148.88 "head -5 ~/.zao/zoe/persona.md"
# ZOE task queue
ssh zaal@31.97.148.88 "cat ~/.zao/zoe/tasks.json 2>/dev/null | head -40"
# Repo state (main clone)
ssh zaal@31.97.148.88 "cd /home/zaal/zao-os && git log --oneline -5 && echo '---' && git status --short | head -10"
# Open PRs / issues
ssh zaal@31.97.148.88 "cd /home/zaal/zao-os && gh pr list --repo bettercallzaal/ZAOOS --limit 5 2>&1"
ssh zaal@31.97.148.88 "cd /home/zaal/zao-os && gh issue list --repo bettercallzaal/ZAOOS --limit 5 2>&1"
# Recent ZOE logs (errors? restarts? clean?)
ssh zaal@31.97.148.88 "journalctl --user -u zoe-bot -n 20 --no-pager"
```

Present results as:

## ZAO Fleet Status

**Units:** [zoe-bot / zao-devz-stack / zaostock-bot / zao-team-bots — active|failed, uptime]
**ZOE identity:** [persona.md first line]
**Task queue:** [tasks.json summary]

### Git State (main clone)
- Last 5 commits + dirty files

### Open PRs / Issues
[list or "none"]

### ZOE Logs (last 20)
[errors? restart loop? healthy?]

### Suggested Actions
[stale tasks, failed units, errors, drift]

## Mode: deploy

**Execute directly via SSH.** Workflow:

1. **Gather local context** — read referenced files, check local git status.
2. **Read current VPS state before writing** (`ssh ... "cat <file>"`).
3. **Deploy:**
   - **Code change** (anything under `bot/src/`):
     ```bash
     ssh zaal@31.97.148.88 "cd /home/zaal/zao-os && git pull && systemctl --user restart zoe-bot && sleep 5 && journalctl --user -u zoe-bot -n 30 --no-pager"
     ```
     (Swap `zoe-bot` for `zao-devz-stack` / `zaostock-bot` / `zao-team-bots` as appropriate.)
   - **persona / human / tasks edit** (no restart):
     ```bash
     ssh zaal@31.97.148.88 "cp ~/.zao/zoe/persona.md ~/.zao/zoe/persona.md.bak && cat >> ~/.zao/zoe/persona.md << 'EOF'
     <block>
     EOF"
     ```
4. **Verify:** `systemctl --user status <unit>` + tail the journal. For persona edits, confirm with `tail` of the file (it applies on ZOE's next turn).

**Rules:**
- ALWAYS read before write; back up `persona.md` before appending.
- Code change → `git pull` + restart. persona/human/tasks → no restart.
- Never write secrets to any file — `bot/.env` holds tokens (`TELEGRAM_BOT_TOKEN`, etc.) and is the systemd `EnvironmentFile`. Use `${VAR}` placeholders in anything you generate. See `.claude/rules/secret-hygiene.md`.
- After a code deploy, watch the journal for a clean boot before declaring done.

## Mode: zoe (update ZOE's memory files)

For giving ZOE new context, tasks, or persona/voice corrections. **Execute directly via SSH.**

1. Decide the target file:
   - identity / voice / format rules / new behavioral instructions → `~/.zao/zoe/persona.md`
   - human context (who/what/preferences) → `~/.zao/zoe/human.md`
   - work queue → `~/.zao/zoe/tasks.json`
2. Read current state (`ssh ... "cat ~/.zao/zoe/<file>"`).
3. Append/edit (back up first; no restart needed — re-read per turn).
4. Verify with `tail`.
5. Optionally generate a Telegram message for ZOE (≤280 chars, ends with "What are your Next 3 Moves?").

> Persona changes should mirror `PERSONA_DEFAULT` in `bot/src/zoe/memory.ts`. If a change is permanent, also land it in `memory.ts` via PR so fresh installs inherit it — otherwise the live file and the seed drift (the exact failure mode that motivated rewriting this skill).

## Mode: tell (direct to ZOE on Telegram)

For instructions / task assignments / feedback to ZOE via Telegram. No VPS code involved.

1. Gather context — what does ZOE need to know?
2. Draft a message: under 500 chars, direct, specific task/question, ends with "What are your Next 3 Moves?" (for task assignments).
3. Output:

```
💬 Send to ZOE on Telegram (@zaoclaw_bot):
```
Then the message in a fenced code block.

## Mode: ask (question for ZOE on Telegram)

Same as `tell` but ends with the question, not "Next 3 Moves".

## Mode: interactive (no args)

Ask: "What do you need? I can:
1. **Check fleet status** (`/vps status`) — runs directly
2. **Deploy changes** (`/vps deploy ...`) — runs directly
3. **Update ZOE's memory files** (`/vps zoe ...`) — runs directly
4. **Tell ZOE to do something** (`/vps tell ...`) — Telegram message
5. **Ask ZOE a question** (`/vps ask ...`) — Telegram message"

## The three tools to reach for first (added 2026-08-08)

These postdate the rest of this skill. Reach for them before hand-rolling an
`ssh` one-liner.

### Deploy: never restart the bot by hand

    ssh vps '~/bin/zoe-autodeploy.sh'

Verifies `origin/main` in a throwaway worktree FIRST, and only restarts the live
clone if that passes - with auto-rollback on a boot error. It exists because
`tsc` passing is not enough: esbuild bundles the real boot graph and can crash a
bot that typechecks cleanly. Do not hot-edit the live clone or restart the
service directly; both are how you get a bot running code nobody verified.

Confirm it landed rather than trusting the output:

    ssh vps 'cd ~/zao-bot-live && echo "HEAD=$(git rev-parse --short HEAD) behind=$(git rev-list --count HEAD..origin/main)"'

### Is a feature actually RUNNING?

    python3 scripts/agents/zoe-liveness.py --remote

Answers built / wired / flagged / live per feature, and compares each flag's
LIVE value against the literal the code accepts. That last part matters: several
flags are gated on `=== '1'`, so setting one to `true` leaves it OFF while
reading as done - the worst kind of wrong, because it looks finished.

And to prove a feature has actually executed since the last boot:

    ssh vps "journalctl --user -u zoe-bot.service --since '1 hour ago' | grep '\[zoe/ran\]'"

One line per feature per boot. **Zero lines is only meaningful if the feature can
log at all** - see `state-claims.md`, "silence is not evidence".

### Check a claim before repeating it

    python3 scripts/agents/zao-verify.py dep|wired|flag|exists|env <arg>

Each answer prints its source. `env` first whenever a tool reports something
surprising: an empty `node_modules` produces hundreds of confident fake errors.

## Where the logs actually are

ZOE runs as a **systemd user unit** (`zoe-bot.service`), so its stdout goes to
**journald, not a tmux pane**. Looking for it in tmux wastes time - the sessions
named after lanes are unrelated. Ancestry check when unsure:

    ssh vps 'cat /proc/$(systemctl --user show -p MainPID --value zoe-bot.service)/cgroup | grep -o "[a-z-]*\.service"'

Note the split: **ZOE runs from `~/zao-bot-live`, but `ZOE_REPO_DIR` points at
`~/zao-os`** - a separate clone used for reading repo state. They are not the
same checkout, and confusing them sends you editing code the bot never loads.

## Known Gotchas (current architecture)

1. **It's systemd `--user`, not system-wide.** Always pass `--user` to `systemctl` / `journalctl`. Without it you'll query the wrong (empty) scope.
2. **persona/human/tasks files are re-read every turn** → no restart for those edits. Only `bot/src/` code changes need a restart.
3. **Two clones on the box.** Main ZAOOS at `/home/zaal/zao-os`; ZAOstock bots run from `/home/zaal/zaostock-bot`. `git pull` the right one for the unit you're deploying.
4. **Tokens live in `bot/.env`** (systemd `EnvironmentFile`). Never echo or commit it. A unit that won't start is often a missing/return-changed env var.
5. **gh CLI** is authenticated as `bettercallzaal`. Workflow order for any bot-driven change: code → commit → push → (PR only if asked).
6. **No Docker.** If a command in an old doc says `docker exec openclaw-...`, it is stale — the container is decommissioned. Translate to a host path / `systemctl --user`.

## Vercel Build Monitoring

```bash
ssh zaal@31.97.148.88 "cd /home/zaal/zao-os && gh pr checks <PR_NUMBER> --repo bettercallzaal/ZAOOS"
```
Common ZAO OS build failures: `@/community.config` → `@/../community.config` (config is at repo root, not `src/`); missing `"use client"` on hook-using components; TS strict-mode errors.

## Prompt Size Rules

- Status output: under 500 words
- Deploy steps: under 2000 words
- Never include API keys or secrets — `${VAR}` placeholders only
- Always use full paths, never `~` inside a heredoc target that another user owns

## Reference Docs

- `bot/src/zoe/README.md` / `USERGUIDE.md` — ZOE deploy + `zoe-bot.service` ops
- `bot/src/zoe/posts/README.md` — the canonical `git pull && systemctl --user restart zoe-bot` deploy line
- `bot/AGENTS.md` — fleet overview, Hermes canonical pattern
- `bot/systemd/` — committed unit files (`zaostock-bot.service`, `zao-team-bots.service`)
- `CLAUDE.md` → Primary Surfaces — the 5 live surfaces + the decommission list
- `research/agents/601-agent-stack-cleanup-decision/` — why openclaw/the squad is gone
