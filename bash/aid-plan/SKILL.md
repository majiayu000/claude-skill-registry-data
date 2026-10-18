---
name: aid-plan
description: >
  Sequence feature SPECs into deliverables -- each one a functional MVP that builds on the
  previous. Strategy, not tactics. Use when feature SPECs are complete and you need a
  delivery roadmap.
allowed-tools: Read Glob Grep Write Edit Bash Shell Terminal
argument-hint: "work-001 (required if multiple works)  [--reset] clear PLAN.md and restart"
---

# Delivery Roadmap

Sequence features into deliverables where each is a functional MVP that works on its own.

## Core Principle

Plan answers ONE question: **"In what order do we deliver, and does each delivery
stand on its own?"**

What Plan does NOT do (already covered by Specify):
- Module mapping, test scenarios, per-feature risks, technical details — all in SPEC.

## The Loop

Each deliverable follows the same cycle:

```
1. PROPOSE  → agent proposes deliverable grouping and sequence
2. DISCUSS  → the user and the agent negotiate (move, reorder, split, merge, defer)
3. WRITE    → save agreed deliverable to PLAN.md
4. REVIEW   → grade against SPECs/KB — pass? next deliverable. fail? back to 1.
```

**Re-run = enter at step 4 with existing PLAN.md.**

## Workspace

```
.aid/
  knowledge/                <- shared KB (read)
    STATE.md                <- minimum grade
  work-NNN-{name}/
    STATE.yml                <- frontmatter-zone keys (authored); Plan/Deliveries is DERIVED (never written here)
    REQUIREMENTS.md         <- read; § 11 holds the `### Feature NNN` sections
                            #  (check Features State in work STATE.yml)
    PLAN.md                 <- OUTPUT: delivery stanzas (each one the delivery
                            #  definition: objective, scope, gate criteria) + execution graph
    deliveries/
      delivery-NNN/           <- CREATED by aid-plan per delivery approved in PLAN.md
        STATE.yml              <- OUTPUT: delivery lifecycle (initial delivery_state: Pending-Spec) + gate key + qa key
```

> Note: `deliveries/delivery-NNN/` must exist before `aid-detail` nests `tasks/task-NNN/` under it.
> The work `STATE.yml`'s Plan/Deliveries view is a DERIVED read-only view assembled
> at read time from `deliveries/delivery-NNN/STATE.yml` files. `aid-plan` does NOT write delivery
> rows into the work `STATE.yml`.

## Arguments

| Argument | Effect |
|----------|--------|
| `work-NNN` | Plan a specific work. Required if multiple works exist. |
| *(no arg)* | Auto-selects if only one work exists. |
| `--reset` | Delete PLAN.md and start fresh. |

## ⚠️ Pre-flight Checks

### Check 1: Locate Work

1. If arg provided → use that work directory
2. If no arg → enumerate works **cross-worktree**: run
   `bash .aid/runtime/scripts/works/enumerate-works.sh` (main tree + every git
   worktree; never the local `.aid/works/` glob, which is empty on `master`), taking
   each record's field-1 `work_id`
3. Single record → auto-select it
4. Multiple records → list them, ask user to choose
5. Zero records on any worktree → **STOP.** "No works found. Run `/aid-describe` first."

### Locate + Enter the Work's Worktree

**As soon as Check 1 resolves the work id** and **before** Check 2 reads
`.aid/works/{work}/REQUIREMENTS.md § 11`, follow
`.aid/runtime/templates/downstream-worktree-entry.md` to normalize `<work-id>` to its bare
`work-NNN` branch name, `locate` the worktree (which **always exits 0** and returns
`<path>\t<status>`), and enter the returned path. Keep the defensive empty-path/non-zero backstop
that stops rather than operate blindly — it should not fire against the real helper. Never create
a new worktree — creation belongs to the work-starting skills only.

### Check 2: Verify Features

1. Read the `### Feature NNN` subsections of `.aid/works/{work}/REQUIREMENTS.md § 11`
2. Check work STATE.yml's Features State (derived view) — each feature should be `Ready`
3. No features → **STOP.** "Run `/aid-describe` then `/aid-specify`."
4. Some not Ready → warn, offer to plan with completed only or wait

### Check 3: Verify Not in Plan Mode

- ✅ `Default` or `Auto-accept edits` → Proceed.
- ❌ `Plan mode` → **STOP.**

## State Detection

State detection reads the files on disk, every run. Nothing remembered from an
earlier run or from this conversation counts as state, because the files may
have changed since.

- No PLAN.md → **FIRST-RUN**
- PLAN.md exists, grade below minimum or not yet graded → **REVIEW**
- PLAN.md exists, graded >= minimum, `deliveries/delivery-NNN/STATE.yml` written for all deliverables -> **DONE**

Print the state-entry line and "you are here" map:

**FIRST-RUN:**
```
[State: FIRST-RUN] — No PLAN.md found; begin dependency mapping and deliverable sequencing.
aid-plan  ▸ you are here
  [● FIRST-RUN ] → [ REVIEW ] → [ DONE ]
```

**REVIEW:**
```
[State: REVIEW] — PLAN.md exists; re-review deliverables against current SPECs and KB.
aid-plan  ▸ you are here
  [✓ FIRST-RUN ] → [● REVIEW ] → [ DONE ]
```

**DONE:**
```
[State: DONE] — Plan is complete and meets minimum grade.
aid-plan  ▸ you are here
  [✓ FIRST-RUN ] → [✓ REVIEW ] → [● DONE ]
```

## Inputs

- **All feature SPECs** — requirements, tech spec, priority, acceptance criteria
- **REQUIREMENTS.md** — scope boundaries, overall priority
- **KB via INDEX.md** — Read `.aid/knowledge/INDEX.md`, use summaries to pull
  relevant docs (typically architecture, module-map, tech-debt — but let the INDEX guide you)
- **Known Issues** — `.aid/works/{work}/known-issues.md` (if exists). Issues registered
  by Specify that block or affect features. Plan may create a fix-first deliverable
  or sequence features to address issues before dependent work.

---

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| FIRST-RUN | `references/first-run-loop.md` | `aid-architect` | → REVIEW |
| REVIEW | `references/review-deliverables.md` | `aid-reviewer` | → DONE |
| DONE | _(inline — plan complete; print summary and exit)_ | `inline` | → halt |

On state entry, print `[State: NAME]` + the "you are here" map from State Detection above.
When a state completes, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** / **PAUSE-FOR-USER-DECISION** → print the pause reason + resume command and exit.
- **HALT** → print the closing summary and exit.

**DONE (inline):** When DONE is detected, print:

```
[State: DONE] — Plan is complete and meets minimum grade.
aid-plan  ▸ you are here
  [✓ FIRST-RUN ] → [✓ REVIEW ] → [● DONE ]

Plan is approved and up to date. Run /aid-plan again with --reset to restart.
```

---

## Feedback Loops

- **→ Discovery:** KB insufficient → Q&A to `.aid/knowledge/STATE.md` `## Q&A (Pending)`
- **→ Specify:** SPEC ambiguous → append to the `qa` sequence in the relevant delivery's `STATE.yml`
- **→ Interview:** Priority unclear → append to the `qa` sequence in the relevant delivery's `STATE.yml`

## Output

`aid-plan` produces two artifact types when a delivery is approved:

### 1. `.aid/works/{work}/PLAN.md` (deliveries + execution graph)

Each `### delivery-NNN` stanza IS the delivery definition -- objective, scope, and
gate criteria live in the stanza, not in a sibling file. A delivery's task listing
and its dependency edges are DERIVED (from each task's `**Source:**` field and from
the `**Depends on:**` field below), so neither is restated here.

```markdown
# Plan -- {Work Name}

## Deliverables

### delivery-001: {Name}
- **What it delivers:** {user-facing value}
- **Features:** feature-001-{name}, feature-003-{name}
- **Depends on:** --
- **Priority:** Must

**Objective:** {one paragraph: what this delivery achieves and why it is scoped as a distinct unit}

**Scope:** {bounded list of what is IN scope, citing features or `AC-N` ids}
**Out of scope:** {anything explicitly excluded, to avoid scope creep}

**Gate Criteria** -- the ordered rubric the delivery gate evaluates; each concrete and
independently testable, each naming an observable (see
`.aid/runtime/templates/requirements/requirements-template.md § Verifiable Acceptance Criteria`):

- [ ] {Criterion 1 -- concrete and testable}
- [ ] {Criterion 2 -- concrete and testable}
- [ ] All section-6 quality gates pass

**Notes:** {constraints or references not captured by the gate criteria; keep brief --
detailed design belongs in the task DETAIL.md files. Omit when there are none.}

### delivery-002: {Name}
- **What it delivers:** {user-facing value}
- **Features:** feature-002-{name}
- **Depends on:** delivery-001
- **Priority:** Must

**Objective:** {...}

**Scope:** {...}
**Out of scope:** {...}

**Gate Criteria**

- [ ] {Criterion 1}
- [ ] All section-6 quality gates pass

## Cross-Cutting Risks

| # | Risk | Impact | Mitigation |
|---|------|--------|------------|
| 1 | {description} | {H/M/L} | {mitigation} |

*(Omit if no cross-cutting risks.)*

## Deferred

| Feature | Reason | Revisit When |
|---------|--------|--------------|
| feature-006-{name} | Could-have | After delivery-003 feedback |

*(Omit if all features included.)*
```

A delivery with zero tasks (e.g. a SPIKE) still carries a full stanza: the objective
and gate criteria are what make it a delivery, and neither depends on tasks existing.

### 2. `.aid/works/{work}/deliveries/delivery-NNN/STATE.yml` (delivery lifecycle)

Seeded from `.aid/runtime/templates/delivery-state-template.yml` with:
- `delivery_state: Pending-Spec`  (SD-8: delivery's own independent lifecycle; NOT derived from tasks)
- `delivery_lifecycle.updated:` set to the current UTC timestamp
- `Branch:` set to `aid/work-NNN-delivery-NNN` (inferred from the folder/worktree, not authored)
- `delivery_gate` and `qa` keys left at their template defaults (filled by `aid-execute`)

A delivery created with ZERO tasks still renders correctly at `Pending-Spec`. The
DERIVED task rollup for this delivery (assembled at read time from
`tasks/task-NNN/STATE.yml` files, which do not exist yet) is simply empty -- that is
correct and expected until `aid-specify` (-> Specified) and `aid-detail` (-> tasks
created) run.

The work `STATE.yml`'s Plan/Deliveries view is DERIVED (read-only at read time);
`aid-plan` does NOT write delivery rows there.

## Quality Checklist

- [ ] Every Ready feature assigned to a deliverable or explicitly deferred
- [ ] Each deliverable is standalone-functional
- [ ] Dependencies between deliverables flow one direction (no cycles)
- [ ] Deliverables follow Must -> Should -> Could priority
- [ ] Cross-cutting risks only if real
- [ ] User approved the sequence
- [ ] Each deliverable was reviewed after writing (step 4)
- [ ] Every delivery stanza carries an objective, scope, and gate criteria (including zero-task SPIKE deliveries)
- [ ] deliveries/delivery-NNN/STATE.yml written for every delivery with delivery_state: Pending-Spec
- [ ] No delivery rows written into the work STATE.yml (Plan/Deliveries is DERIVED)
