---
name: aid-design-ui
description: >
  Develop a UI design as a DESIGN SEED in `.aid/design/ui.md` -- the screen/flow structure,
  the interaction model, and accessibility notes. Use this skill when a screen's layout and
  behaviour are still being worked out and you want a design you intend to keep. Grounded in
  the Knowledge Base (`.aid/knowledge/`) and the project source. It WRITES NO production
  code and NO KB document -- realize the seed into the built component/page with
  `/aid-create-ui` once it is ready. For a THROWAWAY low-fidelity mock that merely validates
  a UX direction rather than a kept design, use `/aid-prototype-ui` instead. Produced by the
  aid-architect agent and independently verified by aid-reviewer (full verify). Allocates a
  work-NNN folder.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit Agent
argument-hint: "<subject> -- the UI screen(s)/flow to design (structure, interaction, accessibility)"
---

# Design UI (develop a design seed, resolve nothing)

Bind **VERB=`design`**, **ARTIFACT=`ui`** -- the `design` *stage* in the contract's
vocabulary -- then follow the shared contract at
`.aid/runtime/templates/design-lifecycle.md`. This skill binds that contract and
restates none of its rules. The seed it writes is `.aid/design/ui.md`; realizing it into
the built component/page is `/aid-create-ui`'s job, not this one's.

- **Boundary vs `/aid-create-ui`:** that skill *builds* the UI from a ready seed; this one
  only *develops* the seed. Neither resolves anything on its own -- the user decides when a
  seed is ready to realize.
- **Boundary vs `/aid-prototype-ui`:** that skill builds a **throwaway** low-fidelity mock
  to *validate* a direction; this one develops a **kept** design meant to *inform the
  build*. Kept vs throwaway is the distinction.
- **Not a numbered pipeline phase**; does not route to `/aid-execute`.

State machine: **INTAKE -> DESIGN -> VERIFY (loop) -> PRESENT [user decides] -> DONE**, as
`design-lifecycle.md § Skill shape` defines it. Print the `[State: NAME] -- {purpose}`
entry line on each state.

---

## State: INTAKE

1. **Require a subject.** Empty argument -> ask one bootstrapping question ("What UI
   screen(s) or flow do you want to design, and what must it support?") and wait.
2. **Allocate** through the Work Initiation Gate exactly as the contract's Allocation rule
   requires (`.agents/skills/aid-design/SKILL.md` INTAKE step 4 is the shape), with
   `initiator: aid-design-ui`. `phase` is not driven.
3. **Acquire `.aid/design/`** per the contract, then read `.aid/design/ui.md` if a prior
   seed exists -- re-invocation iterates it rather than starting over.
4. **Classify complexity** for the `aid-architect` dispatch (verifier tier >= producer).

**Advance:** DESIGN.

---

## State: DESIGN

Dispatch **`aid-architect`** (clean context, tiered) to write or iterate
`.aid/design/ui.md` in the seed shape the contract fixes (`design-seed.md`;
feature-002 §4), grounded in `.aid/knowledge/` and the project source plus any seed read
in INTAKE. What this artifact's seed must settle: **the screen and flow structure, the
interaction model, and accessibility notes**; its `## Destination` names where the built
component/page lands. **Never writes `.aid/knowledge/` and never writes production code**
-- the `design` invariant (`design-lifecycle.md`).

**Advance:** VERIFY.

---

## State: VERIFY

**Full verify**, as `design-lifecycle.md` defines it. Not clean -> loop to DESIGN; the
3-cycle circuit breaker there escalates to IMPEDIMENT + `lifecycle: Blocked`.

**Advance:** PRESENT.

---

## State: PRESENT (hard stop -- the user decides)

Set `lifecycle: Paused-Awaiting-Input`. Present the seed clearly. Assert no resolution --
the user iterates (re-invoke this skill) or realizes it now (`/aid-create-ui`).

**Advance:** DONE.

---

## State: DONE

Set `lifecycle: Completed`, `updated` now, append a `## Lifecycle History` row. The seed
persists at `.aid/design/ui.md`; consumption happens at `/aid-create-ui`.
