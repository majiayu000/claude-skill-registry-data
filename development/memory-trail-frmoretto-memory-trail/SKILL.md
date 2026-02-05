---
name: memory-trail
description: Decision memory and session logging for AI-assisted development. Use when tracking architectural decisions, maintaining context across sessions, implementing confidence protocols, or coordinating between agents. Triggers on "memory trail", "decision memory", "track decisions", "session logging", "why did we decide", "check past decisions".
---

# Memory Trail v1.0

**Purpose:** Lightweight persistence layer for AI-assisted development that tracks WHY decisions are made, not just WHAT changed.

**Core insight:** Checkpoints track WHAT changed; Memory Trail tracks WHY.

---

## Quick Start

To implement Memory Trail in a project:

1. Create `docs/DECISION_MEMORY.md` using template in `assets/DECISION_MEMORY_TEMPLATE.md`
2. Create agent rules file (`.roo/rules-code/rules.md` or equivalent) using `assets/AGENT_RULES_TEMPLATE.md`
3. Create `docs/sessions/` directory for session logs
4. **Customize:** Add project-specific critical decisions to the Quick Reference section

---

## The 4 Components

### 1. Decision Memory

File: `docs/DECISION_MEMORY.md`

Architectural decisions as constraints. Agents read before implementing.

**Format:**
```markdown
### [DEC-001] Decision Title
**Category:** ARCHITECTURE | TECHNOLOGY | PATTERN | POLICY
**Date:** YYYY-MM-DD
**Status:** ACTIVE

**Context:** What prompted this
**Decision:** What you decided
**Rationale:** Why this choice
**Consequences:** What this constrains
```

**Agent protocol:**
- Read before significant changes
- Cite as `[per DEC-XXX]` when following
- STOP if action conflicts
- Propose new decisions for architectural choices

### 2. Confidence Protocol

Signal uncertainty at START of every response:

| Level | When | Behavior |
|-------|------|----------|
| 🟢 CERTAIN (95%+) | Routine, reversible | Proceed, log action |
| 🔵 CONFIDENT (80-94%) | Standard, some complexity | Show intent, proceed |
| 🟡 PROBABLE (60-79%) | Multiple approaches | Explain, request approval |
| 🟠 UNCERTAIN (40-59%) | Significant tradeoffs | Present options |
| 🔴 UNCLEAR (<40%) | Missing info | Ask first |

**Risk adjustments:**
- DESTRUCTIVE: -15%
- IRREVERSIBLE: -25%
- SECURITY: -20%
- TESTED: +15%
- REVERSIBLE: +10%

### 3. STOP Triggers

Hard stops requiring human decision:

| Category | Examples |
|----------|----------|
| **Security** | API keys, auth logic, encryption |
| **Destructive** | DELETE, DROP, bulk removal |
| **Irreversible** | Schema migrations, renaming |
| **Financial** | Payment code, pricing logic |

**When triggered:** Signal 🔴 UNCLEAR, explain risk, present 2-3 options, wait.

### 4. Session Logs

Per-task action tracing. One file per task.

**Pattern:** `docs/sessions/SES-YYYY-MM-DD-NNN.md`

**Format:**
```markdown
# Session Log: SES-YYYY-MM-DD-NNN

**Date:** YYYY-MM-DD
**Agent:** [Agent Name]

## Actions

| Action | Confidence | Decisions | Files |
|--------|------------|-----------|-------|
| Added feature X | 🟢 | [DEC-001] | file.py |
```

**Rules:**
- One file per task (never append)
- Sequential numbering: 001, 002, 003...
- Merge to `*-recap.md` daily
- For history: read only recap files

---

## Pre-flight Protocol

Before any significant action:

```
☐ DECISION_MEMORY.md read this session?
  - NO → Read it now
  - YES → Proceed
☐ Relevant [DEC-XXX] constraints?
  - YES → Cite: "Implementing per [DEC-XXX]"
  - CONFLICTS → STOP, flag to human
☐ STOP trigger category?
  - Security / Destructive / Irreversible / Financial → 🔴 → Options → Wait
☐ Confidence signaled?
```

---

## Multi-Agent Coordination

Agents share context via files:

| File | Who Writes | Who Reads |
|------|------------|-----------|
| `docs/DECISION_MEMORY.md` | Human + Agents | All agents |
| `docs/sessions/SES-*.md` | Each agent | All (recaps only) |
| `CLAUDE.md` / rules file | Human | All agents |

---

## When to Create a Decision

Create a decision when:
- Choice affects multiple files/features
- Choice will recur in future sessions
- Choice has alternatives with different tradeoffs
- Confidence < 80% on architectural choice
- Same question asked 2+ times

**Decision proposal format:**
```
PROPOSED DECISION:
Category: [ARCHITECTURE | TECHNOLOGY | PATTERN | POLICY]
Title: [Short imperative phrase]
Context: [What prompted this]
Decision: [What you're proposing]
Rationale: [Why this choice]
Consequences: [What this constrains]
```

---

## Decision Categories

| Category | When to Use |
|----------|-------------|
| ARCHITECTURE | System structure, component boundaries |
| TECHNOLOGY | Tool/library/service choices |
| PATTERN | Recurring implementation approaches |
| POLICY | Business rules, compliance requirements |

---

## Session Log Lifecycle

```
Task starts → Create SES-YYYY-MM-DD-NNN.md
During task → Log actions to table
Task ends → Add Handoff section

End of day → Merge sessions to SES-YYYY-MM-DD-recap.md
End of month → Merge recaps to SES-YYYY-MM-rollup.md
```

**Retention:**
- Session files: Keep 7 days
- Daily recaps: Keep 30 days  
- Monthly rollups: Keep indefinitely

---

## Resources

- **Templates:** See `assets/` for ready-to-use templates
  - `DECISION_MEMORY_TEMPLATE.md`
  - `AGENT_RULES_TEMPLATE.md`
  - `SESSION_LOG_TEMPLATE.md`
  - `SESSION_RECAP_TEMPLATE.md`

---

## Validation Checklist

After implementing, verify:

- [ ] Agent reads DECISION_MEMORY.md before changes
- [ ] Agent cites decisions as [DEC-XXX]
- [ ] Agent signals confidence at response start
- [ ] STOP triggers halt dangerous operations
- [ ] Session logs created per task (not appended)

---

## Anti-Patterns

| ❌ Don't | ✅ Do Instead | Why |
|----------|---------------|-----|
| Skip reading Decision Memory | Always read at session start | Constraints get violated |
| Append to existing session file | Create new file per task | Loses task boundaries |
| Signal confidence after action | Signal at START of response | Too late to adjust |
| Make decisions without [DEC-XXX] | Propose for Decision Memory | Next session forgets |
| Include timestamps in logs | Use sequential numbering | LLMs unreliable at time |

---

## Related

- **Stream Coding Stack** — Integrated methodology
- **Stream Coding** — Documentation-first development
- **Clarity Gate** — Epistemic verification

---

**Version:** 1.0
**Author:** Francesco Marinoni Moretto
**License:** CC BY 4.0
