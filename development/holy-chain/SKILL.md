---
name: holy-chain
description: >-
  Emperor Time's thumb chain — restoration. Router for four aspects: triage
  (stop digging, snapshot, bracket the breakage), reproduce-and-bisect (make
  it fail on demand, isolate the cause one hypothesis at a time),
  heal-and-verify (minimal fix, root-cause proof, postmortem line), and
  process healing (recovering a derailed loop, skipped gates, bad merges from
  enlisted agents, delivered breaches). Engage when something breaks — a
  regression, a red build, corrupted state, or the process itself. Load one
  aspect file at a time per the Invocation Ritual.
metadata:
  version: 0.2.0
  part-of: emperor-time
  kind: router
---

# Holy Chain — router

> *Enhancement poured into restoration. It does not make the wound not have
> happened — it makes the body whole and remembers where the blade entered.*

Prime directive: **stop digging.** The moment breakage is detected, the
current activity pauses. Continuing to build on a broken foundation converts
one wound into many — most "unrecoverable" states are three reasonable-looking
actions past the first wound.

## Selection table — read exactly one

| Your situation | Aspect file |
|---|---|
| Breakage just detected — secure the scene before anything else | `triage.md` (mechanical: `scripts/emperor triage`) |
| Scene secured — make it fail on demand and isolate the cause | `reproduce-and-bisect.md` (mechanical: `scripts/emperor reproduce`) |
| Cause isolated — fix minimally and prove the cure | `heal-and-verify.md` (mechanical: `scripts/emperor heal-verify`) |
| The *process* broke: skipped gate, bad agent-merge, delivered falsehood, derailed loop | `process-healing.md` (mechanical: `scripts/emperor process-heal`) |

Code wounds run the sequence: `triage.md` → `reproduce-and-bisect.md` →
`heal-and-verify.md`. Before proposing fixes, the heal entry MUST run the four-phase checklist
(`skills/emperor-heal/debug-four-phases.md` / `scripts/emperor heal`) —
Chain Jail leaf; Superpowers systematic-debugging whole skill stays out. Process wounds go straight to `process-healing.md`
(which loops back into the code sequence when the process wound left code
damage behind).

## Chain-wide laws (apply in every aspect)

1. **Reversibility before action** — from triage onward, every step must be
   undoable; healing that can't be reverted is a second gamble, not a cure.
2. **Combat-speed science** — hypotheses and predictions still get written
   before probes (a one-line ledger form exists for exactly this); urgency
   never suspends the scientific method, it compresses the paperwork.
3. **Root cause or labeled symptom-patch** — the heal claims what it actually
   is; "it stopped happening" is not "it's fixed".
4. **Every heal ends in a postmortem line** — one structured line; the wound
   pays for a lesson or it was pure loss.
