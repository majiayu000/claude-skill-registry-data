---
name: tradecraft-attack-scenarios
description: >
  Turn a goal + a scope into a concrete, ordered attack scenario across multiple skills — not one
  technique in isolation. Load at the START of an engagement, on "where do I even begin", when a
  target has many surfaces, or to plan an objective-driven path (e.g. "reach domain admin",
  "prove data exfil"). This is how an agent decides what to try, in what order, and why.
domain: tradecraft
type: methodology
stability: locked
modes: [pentest, bugbounty, defense]
mitre: []
tools: []
schema_version: 1
---

# Building an attack scenario

## When it applies
You have an authorized scope and an objective, and the target exposes several possible surfaces.
Before running anything, you need a plan that sequences the right skills toward the objective and
adapts as evidence comes in. This is the layer above individual techniques.

## Why it works
Real engagements are graphs, not checklists: each result changes what's worth trying next. Planning
the scenario explicitly — objective, hypotheses, ordered leads, decision points — is what turns a
pile of 127 techniques into a coherent path, and it's exactly what the `secskills watch` Attack Map
renders (`lead`, `status`, `rationale`).

## Method
1. **State the objective in impact terms**: "read another tenant's data", "code exec on the app
   host", "domain admin". Everything is prioritised by what moves you toward it.
2. **Enumerate surfaces from recon** (`recon-*`): web, API, cloud, AD, network, people. Each surface
   is a branch.
3. **Generate leads per surface** and score each by *impact × likelihood × cost/noise*. A likely
   high-impact, low-noise lead goes first.
4. **Order into a scenario**: recon → highest-value lead → the pivots each success unlocks. Write it
   to `plan.md` as an ordered, checkbox strategy; tag each lead with a slug for the activity log.
5. **Define decision points**: for each lead, note "if confirmed → pivot to X; if blocked → why, and
   the fallback". This is the branching that makes it adaptive (see `tradecraft-pivot-decisions`).
6. **Re-plan on evidence**: every confirmed finding or dead end updates scores and can reorder what's
   next. The plan is living, not a one-shot.

## Gotchas
- Don't breadth-scan everything — depth on the highest-value lead beats shallow coverage.
- Objective drift: if a lead doesn't advance the stated objective, park it, don't chase it.
- Keep it inside scope; an attractive lead outside `scope.txt` is not a lead (load `tradecraft-scope-roe`).

## Verify success
There is a written `plan.md` with an objective, ordered leads carrying rationale, and explicit
"if/then" pivots — and the agent is working the top lead, not wandering.

## References
MITRE ATT&CK (tactic ordering); PTES; the `exploit-chaining` and `tradecraft-pivot-decisions` skills.
