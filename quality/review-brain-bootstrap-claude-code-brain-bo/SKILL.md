---
name: review
description: Full 10-point expert code review. Use before any PR or MR. Checks correctness, cross-layer consistency, transaction safety, test coverage, and security. Spawns reviewer subagent for isolation.
---

# Review Skill

Run a full expert code review before merging.

## When to use
- Before opening or merging a PR/MR
- When asked to review code
- After implementing a significant feature

## Protocol

### 1. Gather the diff
```bash
git --no-pager diff main...HEAD | head -500
```
Or specify a branch: `git --no-pager diff <base>...<head> | head -500`

### 2. Read context
- `claude/templates.md` for PR template requirements
- `claude/rules.md` for project-specific rules

### 3. Spawn reviewer subagent (recommended for isolation)
> "Spawn a reviewer subagent to review this PR. Diff: [paste diff]. Focus on the 10-point protocol."

### 4. Or: Self-review with the 10-point protocol

**Point 1 — Ticket re-read:** Does every scenario in the ticket/task get addressed?

**Point 2 — Cross-layer consistency:** Grep every new field name, type, enum across ALL layers:
```bash
grep -rn --color=never '<new_field_name>' . | head -50
```

**Point 3 — Enum completeness:** Are all enum values handled in every switch/if-chain?

**Point 4 — Transaction safety:** Are there external calls (HTTP, queue, email) inside DB transactions? → Move them outside.

**Point 5 — Race conditions:** Is there shared mutable state accessed concurrently without synchronization?

**Point 6 — Test coverage:** Every new branch/case/error path has a dedicated test?

**Point 7 — Pre-existing vs. introduced:** Run lint before and after. Distinguish new warnings from pre-existing ones.

**Point 8 — Cross-branch merge safety:** Will this still apply cleanly after other pending branches merge?

**Point 9 — Security:** New HTTP calls? Data exposed? New permissions? Unsafe defaults?

**Point 10 — Confidence gate:** Overall confidence 0-100. Only proceed to PR description if ≥95.

### 5. Output the review

Report format:
- Verdict: PASS / FAIL / NEEDS WORK
- Confidence: X/100
- Blocking issues (must fix)
- Advisory suggestions (non-blocking)

### 6. If passing: generate PR description
Use `/mr` skill after the review passes.

## Rules
- NEVER generate a PR description before the review passes
- NEVER skip a point to save time — a missed bug costs 100x the review time
- If spawning a subagent, wait for its full report before proceeding
