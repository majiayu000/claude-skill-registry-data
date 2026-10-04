---
name: cdev
description: Use when the user invokes /cdev (with or without arguments) in a repo conditioned for continuous autonomous development, or asks to run the active sprint, "follow the plan", "sigue el plan", or overnight/unattended work — starts the single execution loop, adapted through the role profile the repo resolves to.
---

# CDev — the execution loop

Single entry point, single loop. Invoking it is the **elevated autonomy** mandate: work
proactively assuming what the project needs and stop **only at real blockages** — never to ask
what to do next.

The repo is the memory: `SPRINTS.md` = plan · `AGENT_PROGRESS.md` = handoff · git = state. The
repo's specifics live in its `docs/develop/AGENT_EXECUTION_PROTOCOL.md`; the role's specifics
live in a **role profile**; this skill is the generic operating system and the autonomy
threshold. If the repo's protocol is stricter about *when to stop and ask*, this explicit
invocation elevates it; on safety gates the strictest always wins.

## Resolve the role

Read the repo guide (`AGENTS.md`; hosts with their own filename read it through a pointer,
e.g. `CLAUDE.md`) and `docs/develop/` (RECOGNITION document if present, protocol).
Then load the matching profile from this package's `profiles/` directory: resolve this skill's
base directory to its **real path first** (dereference junctions/symlinks), then go to
`../../profiles/`:

- **Backend** (API/services/own schema, no UI) → `profiles/backend.md`.
- **Frontend** (consumes an external backend) → `profiles/frontend.md`.
- **Fullstack/other** → no profile ships: the repo's own protocol must supply the four things a
  profile would (what "verified" means, what "evidence" means, the hardest gate, the
  self-chosen work order). Same loop, same contract. When in doubt, what the repo declares wins.

A profile supplies **exactly those four things** and can never alter the loop, the stop
conditions, the autonomy threshold or the gate policy.

**Not conditioned** (no `docs/develop/` with SPRINTS/protocol) → do not improvise the loop:
propose the `bootstrap` skill and stop there.

## Start (every invocation/resumption)

Read in order: the repo guide (`AGENTS.md`) → protocol → `SPRINTS.md` → `AGENT_PROGRESS.md` (latest entry) →
`git status` + recent commits. If the repo declares an upstream contract (a consumed producer's
published report), read it **before** starting the sprint: it is the contract — never invent
fields, and record divergence from deployed reality as a blocker/decision, not a guess. Resume
from there; do not re-derive what was already decided.

If git shows real work the plan does not know about (commits/WIP with no batch or progress
entry), **reconcile first**: reflect it in `SPRINTS.md` + `AGENT_PROGRESS.md` before
continuing — repo-as-memory does not function while plan and code disagree.

**No argument** = resume the plan's pending work. **With argument** = same loop scoped to that
focus (e.g. `/cdev sprint 09`).

## Loop (repeat until a real blockage)

1. **Select:** first `READY`/`IN_PROGRESS` batch of the `ACTIVE` sprint, in strict declared
   order. Mark it `IN_PROGRESS`. Working branch per the repo's convention; default when the
   repo declares none: `cdev/sprint-<nn>-batch-<nn>`, numbering matching the plan's own. A
   batch depending on an unmerged predecessor branches from that predecessor's branch (merging
   is a human gate, so stacking is the only way to see its work). Never a shared branch.
2. **Implement only that batch.** Reuse before writing; smallest correct diff; additive by
   default so live contracts do not break.
3. **Verify** with the real sequence — the profile defines what "verified" means for the role,
   the protocol fixes the exact commands. If a declared check turns out not to be a real gate
   (it passes while checking nothing), record it as pass-with-caveat and raise a blocker to
   fix the gate — a gate that lies is worse than none. Steps whose blast radius exceeds the
   working branch are prepared, never executed (§ gates).
4. **On failure, diagnose before fixing:** exact error quoted, find every caller, fix the root
   cause once where they all route through, re-run the failed command and then the full
   sequence. Never silence a check to make a step pass.
5. **Record** in `AGENT_PROGRESS.md`, in the ordering the protocol declares: honest status,
   what was done, files, verification **pass/fail/not-run per check**, blockers each naming
   the minimum human decision, next. Incomplete is never `DONE`.
6. **Commit the whole batch** on its branch, unit in the message; useful-but-unfinished →
   `wip(...)`. Never push.
7. **Close:** `DONE` only when acceptance is met with recorded evidence — evidence as the
   profile defines it. Next batch.

## Auto-advance

- **Batch done** → next batch of the sprint.
- **Batch blocked (non-quota)** → `BLOCKED` with reason + the minimum human decision, then
  *blocked-but-not-idle*: next batch whose dependencies are met; if none, the next independent
  sprint. Blocked work is never quietly closed.
- **Sprint done** → if the repository has downstream consumers, publish the contract delta
  where they look (the repo's report convention) as part of closing; mark `DONE`, promote the
  next `PENDING` to `ACTIVE`, continue.
- **Plan exhausted** → derive the next work yourself in the profile's self-chosen order,
  staying inside DEFINED/PARTIAL areas of the clarity map (`PRODUCT.md`; if the repo has no
  map yet, approximate — defined = existing source doc + contract — and note it in
  `docs/develop/DECISIONS.md`). A next-phase draft is written as `PROPOSAL`, never self-activated; continue
  with the other work meanwhile. Record what was self-chosen and why.

## It only stops when

- No ungated work remains anywhere — say exactly which approvals would unblock what.
- A safety gate requires human action and everything else depends on it.
- Contradictory docs, or an `ABSENT` area without which it cannot continue (open question
  recorded; inventing product is forbidden).
- The repo is in an unsafe state.
- Usage/quota limit: save everything, update `AGENT_PROGRESS.md`, commit what is safe (`wip`
  if needed), exit cleanly. Resumption reads the repo, never conversational memory.

## Safety gates (never elevated)

The shape is core: **blast radius beyond the working branch** (push to shared branches, merge,
PRs, deploy, history rewriting) · **irreversible on shared state** (remote schema apply,
destructive data operations) · **real money and live credentials**. The repo's protocol lists
its own gates; the profile lists the role's typical ones; the union applies and the strictest
wins. Prepare, don't execute: draft + blocker naming the decision. A past authorization
recorded in the repo is never a present one.

## Optional composition (host bindings)

If available in the host, compose: a minimal-diff discipline at every step, test-driven work on
domain logic, systematic debugging on failures, a verification pass before claiming done. The
rules above stand on their own without any of them.
