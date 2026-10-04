---

name: superpowers-unbundle
description: >
  Scope reduction mode — identify what can be cut from a plan or PR without losing core value.
  The opposite of plan-ceo-review's expansion mode. Use when asked to 'reduce scope', 'unbundle',
  'trim the fat', or 'cut this down'. Runs a 7-step process: identify the ONE thing that must ship,
  inventory all scope items, categorize into Tier 1 through Tier 4, propose cuts one at a time,
  challenge secondary items, validate core still works, and document the cuts. Also for: pre-PR
  scope negotiation, sprint planning with capacity constraints, and identifying v2 deferrals.
  Also for: cutting scope from a running sprint mid-cycle, negotiating with stakeholders on
  what's minimum viable, and identifying deferred features that belong in a v2 backlog.
allowed-tools:
  - Read
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
---


# Unbundle — Scope Reduction Mode

**Purpose:** When scope creep has buried the core deliverable, this skill identifies
what can be cut without losing the point. Ruthless subtraction. Ship the essence.

This is the inverse of scope expansion — we're not adding, we're removing.

---

## Step 0: Identify the Core

Before cutting anything, understand what MUST ship:

Ask via AskUserQuestion:
> "What is the ONE thing this project/plan/PR must deliver? (If everything else gets
> cut and only this survives, the project is a success.)"

Document the core. This is your immovable center.

---

## Step 1: Inventory the Scope

Read the plan/diff/branch. List everything:

```bash
git diff --stat
git log --oneline -10
```

For each item in scope:
1. What does it do?
2. Who asked for it?
3. When was it added?
4. Is it blocking the core?

### Inventory format:
```
ITEM: [name]
Added by: [who/when]
Purpose: [what it does]
Dependencies: [what it needs]
Core?: [yes/no/maybe]
Risk if cut: [what breaks]
Effort to implement: [low/medium/high]
```

---

## Step 2: Categorize for Cutting

### Tier 1 — Cut First (low value, high effort)
- Nice-to-haves added during brainstorming
- "In case we need it later" infrastructure
- Over-engineered abstractions
- Duplicate functionality
- Features targeting <5% of users

### Tier 2 — Negotiate (medium value, medium effort)
- Secondary user flows
- Polish and animation
- Additional integrations
- Edge case handling
- Documentation beyond basics

### Tier 3 — Protect (core value)
- The ONE thing identified in Step 0
- Any feature the core depends on
- Breaking changes that can't be undone

### Tier 4 — Escalate (high value, high effort)
- New features with significant scope
- Architectural changes
- Multi-component additions

---

## Step 3: Propose Cuts

For each Tier 1 item:

AskUserQuestion (one at a time):
> "**[Item name]** was added [when/by whom]. It [does X]. Cutting it saves [effort].
> Risk: [what breaks]. Should we cut it?"

Options:
- **A) Cut** — remove from plan/PR
- **B) Defer** — move to TODOs for v2
- **C) Keep** — too important to lose

After each decision, update the plan/PR with the change.

---

## Step 4: Challenge Tier 2

For Tier 2 items, apply harder scrutiny:

AskUserQuestion:
> "**[Item name]** is nice-to-have but costs [effort]. It handles [X% of users/cases].
> We could ship without it and add it in a patch. Cut it?"

Options:
- **A) Cut now, add later**
- **B) Keep (worth the effort)**
- **C) Reduce scope — implement a simpler version**

---

## Step 5: Validate Core Still Works

After cuts are made, verify:

1. **Core still delivers** — does the ONE thing still work end-to-end?
2. **No broken dependencies** — does cutting X break Y?
3. **No half-measures** — did we cut so much that what remains is broken?

If core is broken by cuts:
- Restore the minimum needed to make core work
- Note which cuts were "too aggressive"

---

## Step 6: Document the Cuts

Update the plan/PR with a cuts section:

```
CUTS MADE
=========
1. [Item] → [Cut/Deferred/Reduced] — rationale
2. [Item] → [Cut/Deferred/Reduced] — rationale

NET EFFECT
==========
Items removed: N
Items deferred: N
Scope reduced by: ~{percentage}%
Core deliverable: INTACT / BROKEN
```

---

## Step 7: Communicate Changes

For each stakeholder who requested a cut item:

If the plan/PR has a body or description, update it to note cuts.

If contributors are affected, briefly note what changed and why.

---

## Review Log

```bash
mkdir -p ~/.claude/.context
echo '{"skill":"unbundle","timestamp":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","status":"STATUS","items_removed":N,"items_deferred":N,"scope_reduction_pct":N,"core_intact":"'"$CORE_INTACT"'"}' >> ~/.claude/.context/reviews.jsonl
```

---

## Completion Status

- **DONE** — All cuts identified, core validated, plan/PR updated
- **DONE_WITH_CONCERNS** — Cuts made but core has minor degradation
- **BLOCKED** — Cannot identify the core (needs clarification)
- **NEEDS_CONTEXT** — No plan/diff/PR available to unbundle
