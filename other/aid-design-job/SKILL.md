---
name: aid-design-job
description: >
  Develop a scheduled or background job design as a DESIGN SEED in `.aid/design/job.md` --
  the trigger, the work it performs, and its idempotency and failure handling. Use this
  skill when a job's schedule, its work, and its retry behaviour are still being decided.
  Grounded in the Knowledge Base (`.aid/knowledge/`) and the project source. It WRITES NO
  production code and NO KB document -- realize the seed into the built job with
  `/aid-create-job` once it is ready. Produced by the aid-architect agent and independently
  verified by aid-reviewer (full verify). Allocates a work-NNN folder.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit Agent
argument-hint: "<subject> -- the job to design (trigger, work, idempotency/failure)"
---

# Design Job (develop a design seed, resolve nothing)

Bind **VERB=`design`**, **ARTIFACT=`job`** -- the `design` *stage* in the contract's
vocabulary -- then follow the shared contract at
`.aid/runtime/templates/design-lifecycle.md`. This skill binds that contract and
restates none of its rules. The seed it writes is `.aid/design/job.md`; realizing it into
the built job is `/aid-create-job`'s job, not this one's.

- **Boundary vs `/aid-create-job`:** that skill *builds* the job from a ready seed; this
  one only *develops* the seed. Neither resolves anything on its own -- the user decides
  when a seed is ready to realize.
- **Not a numbered pipeline phase**; does not route to `/aid-execute`.

State machine: **INTAKE -> DESIGN -> VERIFY (loop) -> PRESENT [user decides] -> DONE**, as
`design-lifecycle.md § Skill shape` defines it. Print the `[State: NAME] -- {purpose}`
entry line on each state.

---

## State: INTAKE

1. **Require a subject.** Empty argument -> ask one bootstrapping question ("What job do
   you want to design -- its trigger, the work it performs, and its failure handling?") and
   wait.
2. **Allocate** through the Work Initiation Gate exactly as the contract's Allocation rule
   requires (`.agents/skills/aid-design/SKILL.md` INTAKE step 4 is the shape), with
   `initiator: aid-design-job`. `phase` is not driven.
3. **Acquire `.aid/design/`** per the contract, then read `.aid/design/job.md` if a prior
   seed exists -- re-invocation iterates it rather than starting over.
4. **Classify complexity** for the `aid-architect` dispatch (verifier tier >= producer).

**Advance:** DESIGN.

---

## State: DESIGN

Dispatch **`aid-architect`** (clean context, tiered) to write or iterate
`.aid/design/job.md` in the seed shape the contract fixes (`design-seed.md`;
feature-002 §4), grounded in `.aid/knowledge/` and the project source plus any seed read
in INTAKE. What this artifact's seed must settle: **the trigger, the work it performs, and
its idempotency and failure handling**; its `## Destination` names where the built job
lands. **Never writes `.aid/knowledge/` and never writes production code** -- the `design`
invariant (`design-lifecycle.md`).

**Advance:** VERIFY.

---

## State: VERIFY

**Full verify**, as `design-lifecycle.md` defines it. Not clean -> loop to DESIGN; the
3-cycle circuit breaker there escalates to IMPEDIMENT + `lifecycle: Blocked`.

**Advance:** PRESENT.

---

## State: PRESENT (hard stop -- the user decides)

Set `lifecycle: Paused-Awaiting-Input`. Present the seed clearly. Assert no resolution --
the user iterates (re-invoke this skill) or realizes it now (`/aid-create-job`).

**Advance:** DONE.

---

## State: DONE

Set `lifecycle: Completed`, `updated` now, append a `## Lifecycle History` row. The seed
persists at `.aid/design/job.md`; consumption happens at `/aid-create-job`.
