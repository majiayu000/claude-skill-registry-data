---
name: c3-alter
description: |
  This skill should be used when the user asks to "add a component", "change architecture",
  "refactor X", "implement feature", "fix bug", "create new service", "update diagram", or "remove component".
  Requires .c3/ to exist. All changes flow through ADR process. For questions, route to c3-query instead.
---

# C3 Alter - Change Through ADR

**Every change flows through an ADR.** No exceptions.

## REQUIRED: Load References First

1. `../../references/skill-harness.md` - Routing and red flags
2. `../../references/layer-navigation.md` - How to traverse C3 docs

## Core Loop (All Stages)

```
ANALYZE → ASK (until confident) → SYNTHESIZE → REVIEW
              │                        │
              └── until no open ───────┘
                  questions

On conflict: ASCEND → fix earlier stage → re-descend
```

**Confident = No open questions.** Don't proceed with "TODO" or unclear fields.

---

## Stage 1: Intent

| Step | Action |
|------|--------|
| Analyze | Add/modify/remove/fix? What problem? Scope hint? |
| Ask | Use AskUserQuestion: feature vs fix? problem? urgency? |
| Synthesize | `Intent: [action] Goal: [outcome] Type: [feature/fix/refactor]` |
| Review | User confirms or corrects |

---

## Stage 2: Current State

| Step | Action |
|------|--------|
| Analyze | Read affected C3 docs via layer navigation |
| Ask | Are docs accurate? Recent code changes not documented? |
| Synthesize | List affected components, their current behavior, dependencies |
| Review | User confirms or corrects |

---

## Stage 3: Scope Impact

| Step | Action |
|------|--------|
| Analyze | Which layers change? Dependencies? Linkages? Diagrams? |
| Ask | External systems involved? Breaking changes? Keep or replace? |
| Synthesize | List all affected c3 IDs, note breaking changes |
| Review | User confirms or expands |

---

## Stage 4: Create ADR

Generate at `.c3/adr/adr-YYYYMMDD-{slug}.md`. Use `../../references/adr-template.md`.

**Key sections:** Problem, Decision, Rationale, Affected Layers, References Affected, Verification

| On Accept | Update status to `accepted`, proceed to Plan |
|-----------|---------------------------------------------|
| On Reject | Return to Stage 1/3 based on what changed |

---

## Stage 5: Create Plan

Generate at `.c3/adr/adr-YYYYMMDD-{slug}.plan.md`.

**Include:**
- Pre-execution checklist (update `## References` in affected components)
- Ordered steps: docs first, then code, then diagrams
- Verification commands

---

## Stage 6: Execute

Follow plan order:
1. Make change (doc or code)
2. Check for conflicts
3. Update `## References` if code moved/added/removed

**On conflict - Tiered response:**

| Impact | Action |
|--------|--------|
| High: scope expansion, breaking change, new layer | Ask user, update ADR if needed |
| Low: wording fix, diagram update, ID fix | Auto-fix, note in log |

---

## Stage 7: Verify

Run `/c3 audit`. Check diagrams, IDs, linkages, code-doc match.

| On Pass | Update ADR status to `implemented` |
|---------|-----------------------------------|
| On Fail | Fix issue, re-audit, loop until pass |

---

## Response Format

```
**Stage N: {Name}**
{findings}
**Open Questions:** {list or "None - confident"}
**Next:** {what happens next}
```
