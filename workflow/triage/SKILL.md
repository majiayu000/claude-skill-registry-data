---
name: triage
description: Apply a formal state machine to issues — assign category (bug/enhancement/question/spike) and state (needs-triage → needs-info → ready-for-agent → ready-for-human → wontfix). Issues marked ready-for-agent become inputs to supergraph:plan. Use when processing a backlog, reviewing new issues, or preparing work for automation.
---

# /supergraph:triage

Classify issues with a formal state machine. `ready-for-agent` is the handoff trigger to the supergraph pipeline.

Announce: "🗂️ /supergraph:triage — classifying issues..."

## State Machine

```
needs-triage
    ├── enough info → [assign category] → ready-for-agent | ready-for-human
    └── missing info → needs-info → [info provided] → ready-for-agent | ready-for-human

ready-for-agent  → supergraph:plan pipeline
ready-for-human  → manual dev / architectural decision needed
wontfix          → closed with reason
```

## Category Roles

| Category | When |
|---|---|
| `bug` | Observed behavior differs from specified behavior |
| `enhancement` | New capability or improvement to existing behavior |
| `question` | Needs clarification before any action |
| `spike` | Research / proof-of-concept, no production code |

## State Roles

| State | Meaning |
|---|---|
| `needs-triage` | Unreviewed — default for new issues |
| `needs-info` | Blocked on missing information from reporter |
| `ready-for-agent` | Fully specified — safe for `/supergraph:plan` to consume |
| `ready-for-human` | Needs human judgment (architecture, business decision, security) |
| `wontfix` | Will not be addressed — reason required |

## Triage Workflow

### For each issue:

**1. Read the issue completely.**

**2. Assign category** — bug / enhancement / question / spike.

**3. Check readiness for agent:**

A `bug` is `ready-for-agent` when:
- [ ] Steps to reproduce are clear
- [ ] Expected vs actual behavior is stated
- [ ] Environment info is present (version, OS, config)
- [ ] No architectural decision required

An `enhancement` is `ready-for-agent` when:
- [ ] Acceptance criteria are defined
- [ ] Scope is bounded (not open-ended)
- [ ] No design decision blocking implementation

If NOT ready → set `needs-info` and list exactly what's missing (one question per response).

**4. Assign state** and apply labels via GitHub CLI:
```bash
gh issue edit <number> --add-label "bug,needs-info"
gh issue edit <number> --add-label "enhancement,ready-for-agent"
gh issue edit <number> --add-label "wontfix"
# Add comment explaining state change:
gh issue comment <number> --body "Triage: [reason for state]"
```

**5. For `ready-for-agent` issues** — summarize for plan intake:
```markdown
Issue #N: [title]
Category: bug | enhancement
Acceptance: [1-3 criteria]
Constraints: [any known]
→ /supergraph:plan
```

## Batch Triage

For a backlog of issues:
```bash
gh issue list --state open --label "needs-triage" --json number,title,body
```
Process each in order. Report counts at end:
```
Triaged: N issues
  ready-for-agent: N  ← entry point for /supergraph:plan
  needs-info: N
  ready-for-human: N
  wontfix: N
```

## Rules

- Never mark `ready-for-agent` unless acceptance criteria are unambiguous
- `ready-for-human` for anything requiring architecture, security, or business decisions
- One question at a time for `needs-info` issues — don't dump all questions at once
- `wontfix` always requires a reason in the comment
