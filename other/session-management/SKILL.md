---
name: session-management
version: 1.1.0
author: Ashay Kubal @ Qball Inc.
description: "Use when PERFORMING session actions: checking token usage, preparing handoffs, or ending sessions early. Do NOT load for questions about past sessions or reading historical handoff documents."
tags: session, lifecycle, handoff, token-management
user-invocable: false
allowed-tools: Read, Write, Bash, Glob
---

> **CLI Usage:** When unsure about a CLI's interface or flags, run it with `--help` first. Do NOT attempt to discover functionality by reading plugin source code — doing so leads to incorrect execution from assumptions made without context of the holistic flow.

# Session Management Skill

## Purpose

This skill provides guidance for Claude on managing session lifecycle in the CLEAR framework. It explains token thresholds, handoff procedures, and how to manually invoke session operations.

## Plugin Root Resolution

CLI commands in this skill reference `$CLEAR_PLUGIN_ROOT` — a `.claude/settings.json` env var the shell expands. The SessionStart hook persists it, but settings env vars load at session **launch**, so on a brand-new consumer's **first session** (before its next restart) the variable is empty and `node "$CLEAR_PLUGIN_ROOT/build/..."` fails with `MODULE_NOT_FOUND`.

**First-session bootstrap** — if `$CLEAR_PLUGIN_ROOT` is empty, set it inline in the *same* Bash call as the CLI (each Bash call is a fresh shell, so a separate `export` would not carry over):

```bash
export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"
```

Prepend it to the CLI in one shell line: `export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"; <node "$CLEAR_PLUGIN_ROOT/build/..." command>`. `${CLAUDE_PLUGIN_ROOT}` resolves in this SKILL.md body to the actually-loaded plugin path; once the consumer restarts, `$CLEAR_PLUGIN_ROOT` is populated and the assignment is a harmless no-op. Reference files are left unchanged.

## When to Take Action vs. Just Answer

### TAKE ACTION (run scripts) when user says:
- "check my token usage" / "how much context have I used"
- "prepare session handoff" / "prepare for handoff"
- "end session early" / "wrap up this session"
- "initialize session tracking"

### JUST READ FILES (no scripts) when user asks:
- "have we completed the handoff?" → Check `.clear/state/session.json`
- "what was in the last handoff?" → Read `.clear/sessions/*.md`
- "how many sessions have we had?" → Read `.clear/state/session-history.json`
- "what happened in session 14?" → Read the specific session file

## Command Reference

Session management is implemented as bash scripts in `${CLEAR_PLUGIN_ROOT}/scripts/session/` rather than TypeScript CLIs. The architectural inversion is intentional: session events come directly from Claude Code hook bindings, so the bash layer IS the implementation, not an envelope translator. Scripts read JSON via stdin from the hook dispatcher and emit JSON to stdout (which CC interprets as either `additionalContext` injection or `decision:block` semantics, depending on hook event).

| Action | Invocation | Triggered Automatically By |
|--------|------------|----------------------------|
| Initialize session state | `scripts/session/session-init.sh` (stdin JSON) | SessionStart hook (via `dispatchers/session-start.sh`) |
| Check token/context usage | `scripts/session/session-monitor.sh` (stdin JSON) | UserPromptSubmit hook (via `dispatchers/user-prompt.sh`) |
| Generate session handoff | `scripts/session/session-handoff.sh` (stdin JSON) | `session-monitor.sh` at critical threshold; `/cf-handoff` manual |
| Finalize session state | `scripts/session/session-finalize.sh` (stdin JSON) | SessionEnd hook (via `dispatchers/session-end.sh`) |
| Log compaction event | `scripts/session/session-precompact.sh` (stdin JSON) | PreCompact hook (direct binding) |
| Stop-turn knowledge assessment | `dispatchers/session-stop.sh` (stdin JSON) | Stop hook (every Claude response turn) |
| Diagnose session-domain state | `node build/infrastructure/sync/cli/debug-cli.js session` | Manual; routed via `/cf-debug session` |
| Sync-state operations | `node build/infrastructure/sync/cli/sync-bridge-cli.js --op=<...>` | Hook-internal (see Dispatcher Orchestration) + `/cf-reload` |

All script invocations expect JSON via stdin (`session_id`, `cwd`, plus event-specific fields). Manual snippets are documented in **Manual Invocation** below.

## Manual Invocation

When the user requests a session action, run the appropriate script.

**Script Location**: `scripts/session/` in the CLEAR plugin directory

### Check Token/Context Usage

**User says**: "check my token usage", "how much context am I using"

**Action**: Run the session monitor script
```bash
echo '{"session_id":"manual","cwd":"'$(pwd)'","hook_event_name":"Manual"}' | "$CLEAR_PLUGIN_ROOT/scripts/session/session-monitor.sh"
```

**Present to user**: The estimated token usage percentage and prompt count.

### Prepare Session Handoff

**User says**: "prepare session handoff", "prepare for handoff", "end session early"

**Action**: Run the session handoff script
```bash
echo '{"session_id":"manual","cwd":"'$(pwd)'","manual":true}' | "$CLEAR_PLUGIN_ROOT/scripts/session/session-handoff.sh"
```

**Present to user**:
- Path to the generated handoff document
- Resume command for next session
- Prompt user to review and enhance the handoff content

### Initialize Session (if needed)

**User says**: "initialize session tracking", "start session tracking"

**Action**: Run the session init script
```bash
echo '{"session_id":"manual-'$(date +%s)'","cwd":"'$(pwd)'","hook_event_name":"Manual"}' | "$CLEAR_PLUGIN_ROOT/scripts/session/session-init.sh"
```

**Present to user**: Confirmation of session initialization with session number.

## SessionStart Dispatcher Orchestration

The SessionStart hook does NOT call `session-init.sh` directly. Instead, it routes through `scripts/dispatchers/session-start.sh`, which fans out to multiple domain scripts and aggregates their JSON output into the `additionalContext` injection.

**Source-aware reload behavior**: the dispatcher reads a `source` field from stdin JSON and adjusts behavior accordingly:

| Source | Trigger | Reload Behavior |
|--------|---------|-----------------|
| `startup` | Normal session start | Always reload all domains; clear accumulator |
| `resume` | `/resume` command | Skip reload if same session active; clear accumulator (Ctrl+C recovery) |
| `clear` | `/cf-reload` skill invocation | Wipe context, must reload; clear accumulator |
| `compact` | After compaction | Context compressed, must reload; PRESERVE accumulator (mid-session, accumulator is current) |

**Fan-out (in order)**:

1. `session-init.sh` — Creates/resumes session state, initializes thresholds from config
2. `scripts/plan/plan-load.sh` — Loads master-plan + active phase context
3. `scripts/workpackage/workpackage-load.sh` — Loads active WP detail + dependencies
4. `scripts/knowledge/knowledge-load.sh` — Loads recent knowledge entries + pending captures
5. `sync-bridge-cli --op=load` — Loads sync-state aggregator (cross-domain summary)
6. **Pending-Reviews Carry-over** — see subsection below
7. **Prior-session handoff load** — reads most recent `.clear/sessions/session_*.md` as resume context

When `/cf-reload` is invoked, it triggers this same dispatcher with `source: clear`, refreshing the entire context stack without reinitializing the project.

## Pending-Reviews Carry-over

Closes a SessionEnd-invisibility gap: SessionEnd stdout is invisible to Claude (a Claude Code platform limitation), so the carry-over surface had to move to SessionStart where stdout IS visible.

**Flow**:

1. During a Claude turn, the PostToolUse hook (via `dispatchers/post-tool.sh`) detects edits to CLEAR-managed files. On Level A/B surfaces, it appends knowledge entry IDs needing review to `.clear/state/pending-reviews.json`.
2. If those reviews aren't actioned before session end, the file persists across the session boundary.
3. On the next SessionStart, `dispatchers/session-start.sh` reads `pending-reviews.json` and invokes `pending-reviews-cli` to render unactioned flags into the `additionalContext` injection.
4. Claude sees a "PENDING REVIEW" banner at session start and can act on it.

This is a **load-bearing Claude-facing surface** — session start may include text that requires acknowledgement before normal work resumes.

## Stop Hook 3-Tier Knowledge Assessment

The Stop hook fires after every Claude response turn (not just at session close). It is bound to `scripts/dispatchers/session-stop.sh`, which implements a three-tier assessment of whether knowledge capture should be prompted.

**Important separation from finalization**: `session-finalize.sh` runs on SessionEnd, NOT Stop — Stop fires every turn. The Stop hook is exclusively for **knowledge capture**, NOT session lifecycle finalization.

| Level | Condition | Action |
|-------|-----------|--------|
| **A — Deterministic** | Changed files match `.clear/knowledge/**` or `plans/**/workpackages/**` | Reverse-index lookup for linked entries; emit `decision:block` with surface text + linked entry IDs |
| **B — Heuristic** | Changed files match patterns in `change-patterns.yaml` (via `change-patterns-cli`) | Pattern-specific message + linked entries; emit `decision:block` with evaluate prompt |
| **C — Threshold** | No A/B match, but accumulator has ≥ N changed files (default 3) | Emit `decision:block` with generic capture prompt; clear accumulator checkpoint |

**Mechanism**: `decision:block` is a JSON return value from the dispatcher's stdout (`{"decision": "block", "reason": "..."}`). Claude Code's hook runtime parses the JSON; when `decision` is `block`, the `reason` text is injected into the conversation. The `emit_blocking_decision()` helper in `scripts/lib/common.sh` emits these payloads and logs to `hooks.log` for observability.

**Recursion guard**: when Claude responds to an injected `decision:block` reason, the next Stop fire receives `stop_hook_active: true` in the stdin JSON. The dispatcher checks this guard first and exits silently to prevent infinite assessment loops.

**Accumulator semantics**: `.clear/state/accumulator/changed-files.json` (or similar — see `dispatchers/post-tool.sh`) accumulates changed files across turns. Level C uses this accumulation. A/B fires checkpoint the accumulator (clear-and-record). C below threshold preserves it for the next turn.

**Exclusion filter**: `.clear/state/**`, `.clear/audit/**`, `logs/**`, `tmp/**`, `sessions/**`, `node_modules/**`, `.claude/**`, `.git/**`, `build/**` are excluded BEFORE assessment runs. Project-root files matching excluded dir names (e.g., `build.sh`) are NOT excluded.

## Diagnostics Cross-References

For session-state issues, prefer purpose-built tools over manual file reads:

- **`/cf-debug session`** — Routes to `debug-cli session` which validates session state integrity (e.g., dual-ID consistency, schema version, stale-active detection). Supports `--repair` for auto-fixable issues.
- **`/cf-status`** — Read-only formatted session summary (number, tokens, thresholds, active WP, context health). No mutations.
- **`sync-bridge-cli`** operations (`--op=`) — Cross-domain sync state ops: `load`, `persist`, `update-workpackage`, `update-knowledge`, `link-knowledge`, `reconcile`, `reconcile-plan`. Most invocations are hook-internal (see Dispatcher Orchestration); manual invocation is rare.

## How Automatic Session Automation Works

All session scripts above are wired to Claude Code hooks via `hooks/hooks.json` and the dispatcher layer in `scripts/dispatchers/`. See the **Command Reference** table for the full script ↔ hook mapping, and the sections below for behavioral detail on SessionStart fan-out, Pending-Reviews carry-over, and the Stop hook 3-tier assessment. Manual invocation (above) is for on-demand user requests; the automation runs without explicit user intent.

## Token Thresholds

The scripts monitor token consumption against these thresholds:

| Threshold | Default | Action |
|-----------|---------|--------|
| Warning | 60% | Prepare for handoff, complete current task |
| Critical | 75% | Handoff document generated automatically |
| Emergency | 85% | Stop new work immediately |

## Understanding Session State

The scripts maintain state in `.clear/state/session.json`:

```json
{
  "sessionId": "uuid-from-claude-code",
  "clearSessionNumber": 15,
  "tokenUsage": { "estimate": 0.45, "promptCount": 12 },
  "status": "active",
  "handoff": { "prepared": false }
}
```

## Session Files Reference

| File | Purpose |
|------|---------|
| `.clear/state/session.json` | Current session state (sessionId, clearSessionNumber, status, tokenUsage, thresholds, handoff prep flag) |
| `.clear/state/session-history.json` | Rollup of prior sessions (endTime, prompts, tokenUsage, handoffPrepared) — written by `session-finalize.sh` |
| `.clear/state/pending-reviews.json` | Unactioned PostToolUse Level A/B knowledge review flags; surfaced at next SessionStart (see [Pending-Reviews Carry-over](#pending-reviews-carry-over-k27-p5)) |
| `.clear/state/accumulator/changed-files.json` | Changed-file accumulator for Stop hook Level C threshold (see [Stop Hook 3-Tier](#stop-hook-3-tier-knowledge-assessment)) |
| `.clear/state/sync-state.json` | Cross-domain sync aggregator written by `sync-bridge-cli` |
| `.clear/sessions/session_[N]_[DATE].md` | Handoff documents — scaffolded by `scripts/session/session-handoff.sh`. Includes Summary, Completed Items, Technical Decisions, Patterns Established, Learnings, Patterns Observed, Code Changes, and Next Session Priorities. |
| `.clear/config/session-management.yaml` | Configuration overrides (token thresholds) |

## Configuration

The scripts read configuration from `.clear/config/session-management.yaml` if it exists:

```yaml
session_management:
  token_thresholds:
    warning: 0.60
    critical: 0.75
    emergency: 0.85
```

