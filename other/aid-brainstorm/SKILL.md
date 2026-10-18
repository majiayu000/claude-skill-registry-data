---
name: aid-brainstorm
description: >
  Diverge on a problem not yet formed into an answerable question, then converge it to a
  DESIGN SEED in `.aid/design/<slug>.md` -- exploration, framings, and the candidate
  directions worth pursuing. Use this skill when a problem space is still open and you want
  to explore it, rather than answer one specific question. Grounded in the Knowledge Base
  (`.aid/knowledge/`) and the project source. It WRITES NO production code and NO KB
  document, and it RESOLVES NOTHING -- you decide what to do with the seed. For an
  already-answerable technical question that wants a curated, verified answer, use
  `/aid-research` instead. Produced by the aid-architect agent and independently verified by
  aid-reviewer. Allocates a work-NNN folder.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit Agent
argument-hint: "<subject> -- a fuzzy problem or theme to explore (not yet a formed question)"
---

# Brainstorm (diverge then converge to a design seed, resolve nothing)

Bind **VERB=`brainstorm`**, **ARTIFACT=`` (none)** -- the `design` *stage* in the
contract's vocabulary -- then follow the shared contract at
`.aid/runtime/templates/design-lifecycle.md`. This skill binds that contract and
restates none of its rules. It serves the case `/aid-research` cannot: a problem not yet
formed into a question. It has no `create` counterpart -- the seed it produces is the
whole deliverable, and the user decides where it goes next.

- **Boundary vs `/aid-research`:** that skill answers an already-formed, answerable
  technical question; this one explores a problem that has not yet become one. Unformed vs
  answerable is the distinction (FR-7).
- **Not a numbered pipeline phase**; does not route to `/aid-execute`.

State machine: **INTAKE -> DESIGN -> VERIFY (loop) -> PRESENT [user decides] -> DONE**, as
`design-lifecycle.md § Skill shape` defines it. Print the `[State: NAME] -- {purpose}`
entry line on each state.

---

## State: INTAKE

1. **Require a subject.** Empty argument -> ask one bootstrapping question ("What problem
   or theme do you want to explore?") and wait. The subject may be fuzzy -- an unformed
   problem is exactly this skill's case, so INTAKE never refuses an argument for not being
   a question.
2. **Confirm the seed slug.** Because `artifact` is empty, feature-002 §4's `<token>` =
   `artifact` rule does not apply: derive a kebab-case `<slug>` from the subject and
   **confirm it with the user**, then the seed is `.aid/design/<slug>.md`.
3. **Allocate** through the Work Initiation Gate exactly as the contract's Allocation rule
   requires (`.agents/skills/aid-design/SKILL.md` INTAKE step 4 is the shape), with
   `initiator: aid-brainstorm`. `phase` is not driven. The `work-NNN` folder is where
   `STATE.md` and the review gate live, even though the seed is the deliverable.
4. **Classify complexity** for the `aid-architect` dispatch (verifier tier >= producer).

**Advance:** DESIGN.

---

## State: DESIGN

Dispatch **`aid-architect`** (clean context, tiered) to write or iterate
`.aid/design/<slug>.md` in the seed shape the contract fixes (`design-seed.md`;
feature-002 §4), grounded in `.aid/knowledge/` and the project source plus any prior seed.
It diverges -- framings, angles, prior art -- then converges to the candidate directions
worth pursuing. The seed's `## Destination` is **optional** here: brainstorm has no fixed
destination until the user promotes the seed. **Never writes `.aid/knowledge/` and never
writes production code** -- the `design` invariant (`design-lifecycle.md`).

**Advance:** VERIFY.

---

## State: VERIFY

**Full verify**, as `design-lifecycle.md` defines it. Not clean -> loop to DESIGN; the
3-cycle circuit breaker there escalates to IMPEDIMENT + `lifecycle: Blocked`.

**Advance:** PRESENT.

---

## State: PRESENT (hard stop -- the user decides)

Set `lifecycle: Paused-Awaiting-Input`. Present the seed clearly. Assert no resolution --
the user iterates (re-invoke this skill), promotes the seed into a `design` lifecycle
entry, or takes it forward however they choose.

**Advance:** DONE.

---

## State: DONE

Set `lifecycle: Completed`, `updated` now, append a `## Lifecycle History` row. The seed
persists at `.aid/design/<slug>.md`; brainstorm has no `create` counterpart to consume it.
