---
name: authoring-a-playbook
description: Use when adding a new case playbook to process/playbooks/, editing an existing one, or reviewing a change to one — covers the required frontmatter, the fixed body sections, the hard rules, and the matrix/frontmatter agreement that reviews have historically missed. Required before creating any file under process/playbooks/, because playbook-schema.md is machine-checkable in principle but checked by humans in practice.
version: 0.1.0
---

# Authoring a Playbook

## Overview

A **case** is a class of work with its own trigger, entry criteria, and agent subset —
`greenfield`, `defect`, `incident`, `deprecation`. A **playbook** is the recipe for one case:
which agents and skills it uses, in what order, with which gates and loop-backs.

The division of labour is fixed and worth internalising before you write anything:

| Document | Defines |
|---|---|
| `process/agent-roster.md` | **who** the agents are |
| `process/agent-handoff-protocol.md` | **how** work moves between them |
| `process/playbooks/<case>.md` | **which** of them run, in **what order**, for this case |

A playbook therefore *references*; it never *redefines*. If you find yourself restating an
agent's scope or a gate's semantics, you are duplicating a source of truth that will drift.

**Adding a case is a drop-in:** one file conforming to `playbook-schema.md`, plus one column in
the matrix. The roster and the protocol never change to add a case.

## When to Use

- Adding a case.
- Editing an existing playbook — adding or removing an agent, changing gates or ordering.
- Reviewing a change under `process/playbooks/`.

**Do NOT use for:** adding an *agent* (use `authoring-an-agent`; the roster gets the agent
first, as its own change, and only then does a playbook reference it).

---

## Step 1 — Establish that it is a distinct case

A case earns its own playbook when it has a **distinct trigger and distinct entry criteria**,
not merely a different feel. Test it against the existing cases and the picker in
`process/playbooks/README.md`. Two useful discriminators:

- **What starts it?** A packet, a defect report, a page, a removal decision, a question.
- **What is its relationship to the canonical baseline?** `produces`, `consumes`, or `none`.

If a candidate case differs from an existing one only in scope size, it is a variant — document
it inside that playbook rather than forking a near-duplicate. `greenfield`'s increment variant
lived that way legitimately until its divergence justified promotion.

## Step 2 — Write the frontmatter

Every field is required. `playbook-schema.md` §1 is authoritative; this is its working form:

```yaml
---
case: <slug>                    # unique; equals the filename stem AND the matrix column
name: <Human Title>
trigger: <the artifact or event that starts a run of this case>
entry_criteria:                 # what the Orchestrator verifies before issuing handoff 0001
  - <precondition>
agents: [01,02,...]             # roster IDs, INCLUDING conditional ones
skills: [<skill-name>]          # [] if none
gates: [scope, design, release] # ordered slugs; [] if the case has none
baseline: produces              # produces | consumes | none
closure: >                      # one line: what makes a run of this case done
  <traceable to handoff-protocol §6.1 or a documented variant>
---
```

Field rules that carry real weight:

- **`agents`** — every ID must exist in the roster overview table. **Conditional agents belong
  in this list.** A matrix cell marked `~` and an ID absent from `agents:` is the exact
  contradiction this repository has shipped before.
- **`baseline`** — `produces` means the case promotes requirements/glossary/architecture into
  canonical `docs/` at its terminal gate; `consumes` means it diffs against them; `none` means
  it touches neither.
- **`closure`** — cite the protocol section it derives from. A closure condition nobody can
  check is not one.

## Step 3 — Write the body in the fixed section order

Seven sections, all required, in this order (`playbook-schema.md` §2). "none yet" is a valid
value; omitting a section is not.

```markdown
## When to use / when NOT     entry test, with explicit pointers to the right case when this is wrong
## Entry criteria             expanded preconditions the Orchestrator verifies before 0001
## Run at a glance            ASCII phase/agent flow with [H] gate and ↺ loop-back markers
## Phase-by-phase             per agent: what it receives and produces IN THIS CASE
## Loop-backs used            the subset of the protocol's escalation table this case exercises
## Closure criteria           matches the frontmatter `closure`
## Worked example             link to ../examples/<case>-<project>.md, or "none yet"
```

Conventions the existing playbooks share, which yours should too:

- Open with a **Purpose** paragraph and the `[H]` / `↺` **Legend** before the first section.
- Name agents as `NN-agent-slug` in the flow block and as `` `NN` `` in prose.
- Mark conditional steps `(~)` in the flow and **Conditional** in the phase-by-phase entry,
  and always say *what* makes them fire.
- Number the phase-by-phase entries continuously across phases. Inserting a step means
  renumbering the ones after it.
- State a **KEY INVARIANT** where the case has one. `defect` has "reproduce with a failing test
  first"; `brownfield-onboard` has "reconstruct only what exists"; `deprecation` has "no silent
  deletion". A case without an invariant is usually a case that has not been thought through.
- **Document deliberate non-use.** Where a case pointedly does *not* use an agent another case
  would, say so and why — `brownfield-onboard` does this for `09` and `23`. Silence reads as an
  oversight; an explicit "not used" reads as a decision.

## Step 4 — Add the matrix column and reconcile it

In `process/playbooks/README.md`:

1. Add the case to the picker and the column-abbreviation legend.
2. Add a column to the case × agent matrix — one cell for every one of the 29 agents.
   `x` = used · `–` = not used · `~` = conditional (opt-in per run).
3. Add a sentence to the "Reading the columns" paragraph explaining the column's shape.

The matrix header claims *"Every column is authoritative — each is taken from the agent set its
playbook actually runs."* Make that true in both directions:

- Cell is `x` or `~` → the ID **is** in that playbook's `agents:` list **and** appears in the
  body.
- Cell is `–` → the ID is **not** in the `agents:` list.

## Step 5 — Verify

```bash
# frontmatter present and ordered
head -20 process/playbooks/<case>.md
# all seven sections, in order
grep -n '^## ' process/playbooks/<case>.md
# every agents: ID exists in the roster
grep '^agents:' process/playbooks/<case>.md
```

Reconcile the matrix against every playbook mechanically. The check lives in the test suite,
not in this skill, so it cannot silently go stale when the matrix grows a column:

```bash
uv run pytest tests/test_matrix.py tests/test_playbooks.py   # or: just test
```

`test_matrix.py` derives the columns from the matrix header and the case list from the
playbook files, fails if it parses zero rows, and fails on any cell where `x`/`~` disagrees
with that playbook's `agents:` list. CI runs it on every pull request; run it locally before
you push.

Finally, bump the case count in `README.md` (e.g. "10 cases" → "11 cases") and add the case to the
list in the "What's covered" section.

---

## Hard rules (`playbook-schema.md` §3)

- **Project-agnostic.** A playbook describes the case, never a specific project. Project
  specifics live in `process/examples/` (narrative) and `runs/` (real artifacts).
- **References, never redefinitions.** Name roster agents by ID; link protocol sections. Never
  restate an agent's scope or a gate's semantics.
- **No time estimates.** Ordering reflects dependency only, never duration.
- **Drop-in, not rewire.** If a case needs an agent the roster lacks, the roster gets the agent
  first, as its own change.

## Conformance checklist

- [ ] `case` equals the filename stem and the matrix column header
- [ ] All nine frontmatter fields present
- [ ] Every `agents:` ID exists in the roster; conditional agents included
- [ ] All seven body sections, in the fixed order
- [ ] Purpose paragraph and `[H]` / `↺` legend before the first section
- [ ] Phase-by-phase numbering continuous; every conditional step says what fires it
- [ ] Deliberate non-use of an agent is stated, not left silent
- [ ] Matrix column added and reconciled in both directions
- [ ] Case counts updated in `process/playbooks/README.md` and `README.md`
- [ ] `closure` traceable to handoff-protocol §6.1 or a documented variant

## Reference

- `process/playbooks/playbook-schema.md` — authoritative; this skill is its working form
- `process/playbooks/README.md` — the picker and the case × agent matrix
- `process/agent-roster.md` — the agent registry
- `process/agent-handoff-protocol.md` — §3 gates, §4 loop-backs, §6 closure
