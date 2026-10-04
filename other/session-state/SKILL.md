---
name: session-state
description: Maintain SESSION-STATE.md, the durable within-session memory that survives context compaction. Use when a constraint, settled decision, existing-infrastructure (survey) finding, or open thread must persist across a long session so it is not re-derived or re-litigated. Triggers on /state, "remember this for the session", "record this constraint/decision", or after surveying what already exists. For cross-session/personal memory use .claude/memory/ on Claude or native memories on Codex; for repo-derivable facts, do not record at all.
when_to_use: A fact must survive context compaction WITHIN this session — a hard constraint, a settled decision, a survey result (existing infra to reuse), or an open thread/next step. Not for cross-session memory (.claude/memory/ on Claude, native memories on Codex) and not for anything derivable from the repo.
compatibility: Requires Bash. Works in Claude Code and Codex via install.sh; Claude provides /state, while Codex invokes this skill by name or intent.
---

# Session State

`SESSION-STATE.md` (project root, gitignored; schema in this skill's `assets/SESSION-STATE.template.md`) is the harness's live external memory — NORTH_STAR Lever 3. A model's context compresses over a long session and settled facts drift; this file is the durable copy, re-surfaced by hooks:

- **SessionStart** injects the whole file (Claude and Codex).
- **UserPromptSubmit** injects a compact digest — **Constraints + Decisions + Open threads** — each Claude turn.
- **PreCompact** checkpoints before context is compressed (Claude and Codex).

## How to record (never hand-edit)

Writing via a script — not by editing the file from memory — is the point: it captures the fact even when attention is full. Resolve the writer project-first, then global install fallbacks ([path layout](../findings-ledger/references/install-paths.md)):

```
PROJ="${CLAUDE_PROJECT_DIR:-.}"
# 1. Repo checkout (source of truth)
SS="$PROJ/.claude/skills/session-state/scripts/session-state.sh"
# 2. Project Codex install
[ -f "$SS" ] || SS="$PROJ/.agents/skills/session-state/scripts/session-state.sh"
# 3. Global Claude Code install
[ -f "$SS" ] || SS="$HOME/.claude/skills/session-state/scripts/session-state.sh"
# 4. Global Codex install
[ -f "$SS" ] || SS="$HOME/.agents/skills/session-state/scripts/session-state.sh"
```

| Type | Use for | Re-injected each turn? |
|---|---|---|
| `constraint` | hard rules in force (e.g. "Rust only, no Python") | **yes** |
| `decision` | settled choices, date-stamped (so they're not re-litigated) | **yes** |
| `infra` | survey-before-act findings — what already exists, to reuse (writer emits `[surveyed:name]` from first token) | no |
| `thread` | in-flight items / next steps | **yes** |

### Claude Code — `/state` slash command

In Claude Code, use the `/state` command (`.claude/commands/state.md`), which invokes the writer above:

```
bash "$SS" init
bash "$SS" init-orchestrator   # init + default orchestrator constraints (idempotent)
bash "$SS" show
bash "$SS" constraint "<entry text>"
bash "$SS" decision   "<entry text>"
bash "$SS" infra      "<entry text>"
bash "$SS" thread     "<entry text>"
```

Valid types: `constraint`, `decision`, `infra`, `thread`, `init`, `init-orchestrator`, `show`. If the type is empty or invalid, list the valid types — do not guess. `init`, `init-orchestrator`, and `show` take no text; the four entry types take the text as one quoted argument.

### Codex

Ask Codex to use `session-state`, for example: “Use session-state to record this decision: …”. The skill runs the same writer commands; no Claude slash command is installed. Codex re-injects the full state at session start and after compaction. Use Codex's native memory feature for cross-session personal memory.

**Orchestrator mode:** run `init-orchestrator` at session start so dispatch constraints re-inject every turn.

Keep entries terse. For `infra`, lead with the service name as the first word — e.g. `"rabbitmq broker on :5552 (docker-compose) — reuse"` — the writer stores `[surveyed:rabbitmq] …` so survey guards suppress only when a command names that exact surveyed subject.

## When to reach for it (proactively)

- You just established a hard constraint, or the user gave one → record a `constraint`.
- You made or were given a settled decision → record a `decision`.
- You surveyed and found existing infrastructure (a running service, an existing config) → record `infra`, so a later step reuses it instead of rebuilding.
- You are leaving a thread unfinished → record a `thread`.

## Activation (on by default)

The writer works as soon as the skill is installed. **Supported hooks are registered by `install.sh`**; Codex asks you to review and trust them with `/hooks` before they run. Hook JSON examples and security notes: [references/hook-setup.md](references/hook-setup.md).

## Discipline

Keep entries terse — Constraints, Decisions, and Open threads are re-injected every turn, so bloat re-creates the token tax. Prune stale lines. Do not duplicate `.claude/memory/` (cross-session) or facts derivable from the repo.

## Known limitations

- **Existing-infra is SessionStart-only.** Survey findings (`infra`) are not in the per-turn digest — only Constraints, Decisions, and Open threads are. After mid-session compaction, infra coverage still depends on SessionStart injection (or recording a load-bearing finding as a `constraint`). The survey-before-act guard covers provisioning commands only.
- **Token-cost tradeoff.** Adding Decisions to the digest (#158) improves post-compaction decision coverage at the cost of a slightly larger always-on per-turn injection. Keep decision bullets terse; prune stale ones.
