---
name: cf-handoff
version: 1.0.0
author: Ashay Kubal @ Qball Inc.
description: Generate a session handoff document. Use when ending a session, reaching token thresholds, or previewing handoff contents.
user-invocable: true
argument-hint: [--preview]
allowed-tools:
  - Bash
  - Read
  - Edit
---

> **CLI Usage:** When unsure about a CLI's interface or flags, run it with `--help` first. Do NOT attempt to discover functionality by reading plugin source code — doing so leads to incorrect execution from assumptions made without context of the holistic flow.

# Session Handoff

Generate or preview the session handoff document for the current CLEAR session. Captures metrics, decisions, progress, and priorities for the next session.

## Plugin Root Resolution

CLI commands in this skill reference `$CLEAR_PLUGIN_ROOT` — a `.claude/settings.json` env var the shell expands. The SessionStart hook persists it, but settings env vars load at session **launch**, so on a brand-new consumer's **first session** (before its next restart) the variable is empty and `node "$CLEAR_PLUGIN_ROOT/build/..."` fails with `MODULE_NOT_FOUND`.

**First-session bootstrap** — if `$CLEAR_PLUGIN_ROOT` is empty, set it inline in the *same* Bash call as the CLI (each Bash call is a fresh shell, so a separate `export` would not carry over):

```bash
export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"
```

Prepend it to the CLI in one shell line: `export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"; <node "$CLEAR_PLUGIN_ROOT/build/..." command>`. `${CLAUDE_PLUGIN_ROOT}` resolves in this SKILL.md body to the actually-loaded plugin path; once the consumer restarts, `$CLEAR_PLUGIN_ROOT` is populated and the assignment is a harmless no-op.

---

## When to Use This Skill

| Trigger Pattern | Example User Request |
|-----------------|---------------------|
| Session ending or wrapping up | "Create a session handoff" |
| Token budget checkpoint reached | "Generate handoff, I'm at 75%" |
| Preview handoff contents | "What would be in the handoff?" |

**DO NOT use for:**
- Initializing a new session (use `/cf-init` instead)
- Viewing session status without generating a handoff (use `/cf-status` instead)

---

## Usage

- `/cf-handoff` -- Generate the handoff document
- `/cf-handoff --preview` -- Preview contents without creating a file

---

## Instructions

### Step 0: Pre-flight Check

```bash
if [ -f ".clear/state/session.json" ]; then echo "SESSION_ACTIVE"; else echo "NO_SESSION"; fi
```

If `NO_SESSION`: display "No active CLEAR session. Run `/cf-init` to initialize CLEAR." and stop.

### Branch: --preview

If `$ARGUMENTS` contains `--preview`, read session state and display a preview:

```bash
SESSION_STATE=$(cat .clear/state/session.json)
SESSION_NUM=$(echo "$SESSION_STATE" | jq -r '.clearSessionNumber')
TOKEN_PCT=$(echo "$SESSION_STATE" | jq -r '(.tokenUsage.estimate * 100) | floor')
CONVERSATION_TURNS=$(echo "$SESSION_STATE" | jq -r '.tokenUsage.promptCount')
echo "Handoff Preview for Session ${SESSION_NUM}"
echo "========================================"
echo "Token Usage: ${TOKEN_PCT}% | Conversation Turns: ${CONVERSATION_TURNS}"
echo ""
echo "The handoff document will include:"
echo "- YAML frontmatter with all metrics (to be updated)"
echo "- Summary, Completed/In Progress items, Technical decisions"
echo "- Patterns Established, Learnings, Patterns Observed"
echo "- Changes this session (knowledge, plan, workpackage)"
echo "- Code changes table, Test results, Next session priorities"
echo ""
echo "Run /cf-handoff without --preview to generate the document."
```

Stop after displaying preview.

### Branch: Generate (no --preview)

**Step 1 -- Generate:** Invoke session-handoff.sh. The `$CLEAR_PLUGIN_ROOT` bootstrap
is prepended in the *same* shell line (per Plugin Root Resolution above) so this works
on a brand-new consumer's first session, before the settings env var has loaded:

```bash
export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"; \
  echo '{"session_id": "manual", "cwd": "'"$(pwd)"'", "manual": true}' | \
  "$CLEAR_PLUGIN_ROOT/scripts/session/session-handoff.sh"
```

**Step 2 -- Display result.** The script returns JSON with the document path. Show:

```
Handoff document generated at: .clear/sessions/session_N_YYYYMMDD.md

Next steps:
1. Update YAML frontmatter metrics (prod/test files, lines, test results, complexity, hours)
2. Fill in markdown sections (Summary, Completed Items, Technical Decisions, Patterns Established, Learnings, Patterns Observed, Code Changes, Next Priorities)
3. Change status from PARTIAL to COMPLETE when done
```

**Step 3 -- Open for editing.** Read the generated file so Claude can help fill it in:

```bash
HANDOFF_PATH=$(cat .clear/state/session.json | jq -r '.handoff.documentPath')
cat "$HANDOFF_PATH"
```

### YAML Frontmatter Reference

The handoff uses a single YAML frontmatter block. Key fields:

| Group | Fields |
|-------|--------|
| Identity | `session`, `date`, `workpackage`, `branch`, `status` (PARTIAL/COMPLETE/BLOCKED) |
| Tokens | `tokens_pct`, `tokens_count`, `conversation_turns` |
| Code Files | `prod_files_created`, `prod_files_modified`, `test_files_created`, `test_files_modified` |
| Lines | `lines_prod`, `lines_test`, `lines_docs` |
| Docs | `docs_created`, `docs_modified` |
| Tests | `tests_passed`, `tests_failed`, `tests_total` |
| Metadata | `complexity` (simple/medium/complex), `decisions_count`, `actual_hours` |

### Retrospective Sections

The handoff scaffolds four retrospective sections: `## Technical Decisions`,
`## Patterns Established`, `## Learnings`, `## Patterns Observed`.

If you captured a technical decision, pattern, or learning via `/cf-knowledge` during the
session, include its knowledge ID (e.g., `TD-N`, `PAT-N`, `LES-N`) in the handoff entry.
Items without IDs document content in the handoff but are not registered as knowledge
entries. `## Patterns Observed` is for in-session observations that aren't yet established
patterns (no associated knowledge ID).

Bullet format inside each section is open — fill conversationally. Leave a section's
bullets empty if nothing applies.

### Auto-trigger Note

The underlying script (`scripts/session/session-handoff.sh`) is invoked automatically by `session-monitor.sh` at the critical threshold (75% by default — configurable via `.clear/config/session-management.yaml`). This skill is the manual invocation surface for the same script — both paths produce the same handoff document. Auto-generated documents will have placeholder values that should be updated before finalizing.

### After Handoff

1. Finalize the handoff document — edit `.clear/sessions/session_N_<date>.md` directly via Edit (the path-allowlist carve-out permits this). Update placeholder zeros and `status: PARTIAL` → `status: COMPLETE` once the session is closed out.
2. Commit the handoff document to version control.
3. The next session can resume using the documented priorities.

Metrics capture runs automatically at the start of the next session (`session-init.sh` scans `.clear/sessions/` for finalized handoffs and appends to `.clear/metrics/metrics.csv`). Only handoffs whose `status:` value contains `complete` (any case — `COMPLETE`, `Complete`, `completed`, etc.) are captured; partial/abandoned handoffs are ignored. One-session lag is intentional; no manual invocation required.

---

## Completion Checklist

- [ ] Session state verified as active
- [ ] Handoff document generated (or preview displayed)
- [ ] Handoff file opened for review and editing
