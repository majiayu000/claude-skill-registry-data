---
name: shape
description: "Converge with the PM on a problem's shape. Size first if unsized."
description-budget: 190
version: 1.0.0
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# Shape

Converge with the PM on **what the problem actually is** before the EM goes solo on **how to
solve it**. Plans fuse a PM-owned PRD half (the problem, what "solved" means) with an EM-owned
SDD half (architecture, fix-locus, sequencing); the pipeline has rigor for the SDD half and
almost none for the PRD half. `/shape` is that missing front half: a short, collaborative
problem-convergence beat whose only exit is a ratified problem-set that altitude-routes to the
horizon-appropriate downstream ceremony (`coordinator:plan`, `coordinator:roadmap-planning`, or
`coordinator:goal-setting`).

**Strategic ceremony, not tactical clarification.** Operates at the altitude of product intent,
scope boundaries, and success criteria — questions only the PM can resolve. Tactical
uncertainties (naming, file structure, test framework, commit shape, refactor mechanics) are EM
remit and do NOT belong in a `/shape` exchange, however genuinely unsure the EM is — resolving
them is the EM's job (`global CLAUDE.md § PM Altitude`).

**Announce at start:** "Using `/shape` to converge on the problem before we plan a solution."

**Dispatch authorization — invoking this skill IS the request.** The dispatches named below are constitutive steps of this skill, not a separate thing to get cleared: invoking a skill requests the actions that skill performs. A harness line permitting dispatch "unless the user requested it" is therefore **satisfied here, not overridden** — no precedence claim is needed and none is made. Re-asking spends the very context the dispatch exists to protect. The rule attaches to skill entry and dissolves no PM-authored gate: keyword-gated skills gate entry, and every gate a skill names for itself still binds — per-session cross-repo-commit assent, ask-before-external-action, and any other this skill's own body names. Tripwire: `UNATTRIBUTED-HARNESS-LINE-IS-NOT-PM`.

## When NOT to invoke

- **Trivial work** (single-file change, obvious scope) → just do it.
- **PM doesn't know *what* to build / needs approaches explored** → `coordinator:brainstorming`.
  Discriminator: PM *has* a problem and wants confirmation you understood it → `/shape`; PM
  doesn't know what to build at all → brainstorming.
- **Problem already converged** (a prior `/shape`, an existing approved spec, a known next-step
  on a live workstream) → straight to the downstream skill (§ Transition).

`/shape` and `coordinator:brainstorming` are siblings: brainstorming turns vague intent into a
*design spec* (`docs/specs/`); `/shape` converges on the *problem* (`docs/problems/`) and defers
solutioning entirely. Both chain into a downstream planning ceremony.

## Conform intake — an incoming sizing-object (`route: shape`)

`coordinator:sizing` sometimes routes here rather than straight to plan/roadmap-planning: (a)
large size with unclear JTBD, or (b) a well-trodden problem/solution space where the ask wants a
step-change. If the firing condition is known from the sizing exchange, name it; otherwise state
both as possible. A large-but-clear ask skips shape entirely — this is not a universal sizing
route. Shape keeps its own § Transition horizon-routing regardless — sizing routes INTO shape, it
does not perform shape's downstream routing. This is a receive-and-use-if-present detent: `/shape`
runs exactly as today with no sizing-object present, and sizing never gates or refuses a bare
`/shape` invocation.

<HARD-GATE>
Once `/shape` has started, do NOT invoke any implementation skill, write code, scaffold anything,
or dispatch an executor until the problem-set is written and PM-ratified. The only exit is a
ratified problem-set that transitions via § Transition. If the problem was already converged,
skip `/shape` entirely instead. Once started, see it through.
</HARD-GATE>

## Process (lightweight — not brainstorming's full design dialogue)

1. **Restate the problem(s)** as received, in the PM's vocabulary, falsifiably — the actual
   problem, stated so the PM can catch a misread. With a `route: shape` sizing-object present,
   open from its `intent` field verbatim rather than re-deriving the raw ask.
2. **Surface your single biggest uncertainty** per the forced-articulation contract below — the
   load-bearing step.
3. **PM corrects/confirms.** Iterate to a shared mental model; the written problem-set is its
   residue, not its substitute.
4. **If the PM has a proposed solution-shape**, reflect it back and flag pushback — do NOT
   design. Solutioning is `coordinator:plan`'s job.
5. **On convergence**, scaffold the problem-set (below), fill its body, set `estimated_horizon`,
   ratify with the PM, confirm the horizon, and chain into the downstream ceremony (§ Transition).

## Forced-articulation contract

A yes/no "do I have the shape? ✓" is a **banned response shape** — EM confidence is coupled with
helpfulness, so it self-reports green every time. Step 2 must instead produce the thing that
*reveals a misunderstanding*:

- **(a)** The single least-certain item must be the scope boundary whose wrong guess costs the
  most rework — *"name the boundary that, if guessed wrong, invalidates the most of the plan"*,
  not "name something I'm unsure about."
- **(b)** State the probability-weighted consequence: *"If I'm wrong about X, then Y and Z are
  rework."* A low-stakes selection self-evidently fails this.
- **(c)** Must be a PM-altitude question — product intent, scope boundary, success criteria.
  Tactical/EM-decided uncertainties are disqualified as off-altitude regardless of how unsure you
  are (`global CLAUDE.md § PM Altitude`) — resolving them is your job, surfacing them is noise.
- Also flag any intent you inferred that the PM did not state — scope, priority, constraint.

## The problem-set artifact

**Scaffold via** (POSIX-host form; PowerShell hosts: Shape W, `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`):
`coordinator-doc-new --type problem-set --title "<problem title>"`
— emits `docs/problems/YYYY-MM-DD-<slug>.md`, `status: draft`, canonical skeleton. Tiny by
design: a bulleted problem list, not a design doc.

**Fill and ratify:**
1. List problems under `## Problems` (numbered, NOT prioritized — no `P<n>` prefix).
2. List non-goals under `## Out of scope (architectural reasons)` with hard architectural
   reasons, not "later."
3. On PM convergence (the PM's own statement in conversation is the evidence): flip `status: draft → ratified`, fill `ratified_by`, `ratified_date`,
   `estimated_horizon`, stamp `> Ratified by PM <name> <date>`.

A problem-set without ratification is `status: draft` and does NOT count as an oracle. Plans link
it via `problem_set:`.

## Transition

Once ratified, route by horizon — **detect-then-confirm**: surface your horizon read at
ratification, let the PM confirm before chaining. Never pick a rung silently.

| `estimated_horizon` | Work shape | Downstream ceremony |
|---|---|---|
| `session` | One or two sessions | `coordinator:plan` — problem-set becomes the plan's coverage oracle (`plan-coverage-checker`). |
| `week` | ~week, bounded | `coordinator:roadmap-planning` — seeds a roadmap with sprint-sized stubs. |
| `initiative` | Weeks-to-quarters | `coordinator:goal-setting` — seeds an OKR-shaped goal artifact. May fan out 1→N goal-seed stubs when the vision decomposes into multiple goal-slices. |

**Precedence:** a PM axiom/directive naming a specific downstream skill, or a forced-articulation
tier flag that resolves the horizon unambiguously, overrides the router — the router is the
default for ambiguous or undirected convergence.

**Ambiguous horizon:** ask explicitly — *"Does this feel like a session, a week, or an
initiative?"* Never pick silently.
