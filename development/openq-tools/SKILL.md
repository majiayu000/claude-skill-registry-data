---
name: openq-tools
description: "Open questions register. Use for: QID generation, OQ-SIG-001 format IDs, append questions, open_questions.md. Generate sequential QIDs, append questions with context. Use in clarifier when registering open questions instead of guessing. Invoke via bash .claude/scripts/demoswarm.sh openq next-id|append."
allowed-tools: Bash, Read, Write
---

# Open Questions Tools Skill

Helpers for the open questions register (`open_questions.md`). Generates sequential QIDs and appends entries.

## Invocation

**Always invoke via the shim:**

```bash
bash .claude/scripts/demoswarm.sh openq <command> [options]
```

**Do not set PATH or call helpers directly.** The shim handles resolution.

---

## Operating Invariants

### Repo root only
- Assume working directory is repo root.
- All paths are repo-root-relative.

### QID format
- Pattern: `OQ-<FLOW>-<NNN>` (e.g., `OQ-SIG-001`, `OQ-PLAN-002`, `OQ-BUILD-003`)
- Flow codes: `SIG` (signal), `PLAN` (plan), `BUILD` (build), `GATE` (gate), `DEPLOY` (deploy), `WISDOM` (wisdom)
- Sequential within flow (auto-incremented from existing entries)

### Append-only
- Never modifies existing entries
- Only appends new questions at the end

---

## Allowed Users

Primary:
- `clarifier`
- Flow orchestrators (when questions arise mid-flow)

Secondary:
- Any agent that needs to register an open question rather than guessing

---

## Command Reference

| Command | Purpose |
|---------|---------|
| `openq next-id` | Generate next QID for a flow |
| `openq append` | Append question entry to file |

---

## Quick Examples

### Generate next QID

```bash
# Get next available QID for signal flow
bash .claude/scripts/demoswarm.sh openq next-id \
  --file ".runs/feat-auth/signal/open_questions.md" \
  --prefix "SIG"
# stdout: OQ-SIG-003 (next available)

# For plan flow
bash .claude/scripts/demoswarm.sh openq next-id \
  --file ".runs/feat-auth/plan/open_questions.md" \
  --prefix "PLAN"
# stdout: OQ-PLAN-001 (if empty)
```

### Append a question

```bash
# Append new open question (auto-generates QID)
bash .claude/scripts/demoswarm.sh openq append \
  --file ".runs/feat-auth/signal/open_questions.md" \
  --prefix "SIG" \
  --question "Should authentication use JWT or session cookies?" \
  --default "Use JWT for stateless authentication" \
  --impact "Session cookies require server-side state management"
# stdout: OQ-SIG-003 (the assigned QID)
```

---

## Contract Rules

1. **stdout**: QID string for both `next-id` and `append` (append returns the assigned QID)
2. **exit code**: `0` on success, non-zero on failure
3. **File missing**: `next-id` returns first ID (e.g., `OQ-SIG-001`); `append` creates file with header if needed
4. **Auto-increment**: `append` automatically generates the next QID (no need to call `next-id` first)

---

## Entry Format

Appended entries follow this format:

```markdown
- QID: OQ-SIG-003
  - Q: Should authentication use JWT or session cookies? [OPEN]
  - Suggested default: Use JWT for stateless authentication
  - Impact if different: Session cookies require server-side state management
  - Added: 2025-12-12T10:30:00Z
```

---

## For Agent Authors

In clarifier or when questions arise:

1. **Just call `append`** — it auto-generates and returns the QID
2. **Never hand-roll QID counters** — let the tool handle sequencing
3. **Use `next-id` only** if you need to preview the ID before appending

Example pattern:

```bash
# Simple: append directly (auto-generates QID, returns it)
QID=$(bash .claude/scripts/demoswarm.sh openq append \
  --file ".runs/${RUN_ID}/signal/open_questions.md" \
  --prefix "SIG" \
  --question "What is the expected session timeout?" \
  --default "30 minutes of inactivity" \
  --impact "Shorter timeout improves security but reduces UX")

echo "Registered question: $QID"
```

---

## Flow Codes Reference

| Flow | Code | Example QID |
|------|------|-------------|
| signal | SIG | OQ-SIG-001 |
| plan | PLAN | OQ-PLAN-001 |
| build | BUILD | OQ-BUILD-001 |
| gate | GATE | OQ-GATE-001 |
| deploy | DEPLOY | OQ-DEPLOY-001 |
| wisdom | WISDOM | OQ-WISDOM-001 |

---

## Installation

The Rust implementation is preferred. Install to repo-local directory:

```bash
cargo install --path tools/demoswarm-runs-tools --root .demoswarm
```

The shim will automatically resolve in order:
1. `.demoswarm/bin/demoswarm` (repo-local install, preferred)
2. `demoswarm` on PATH (global install)
3. `cargo run` fallback (dev environments)
4. Python fallback (legacy)
