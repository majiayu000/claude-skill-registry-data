---
name: workflow-design
description: >-
  Designs a multi-agent workflow: which agents (researcher, analyst, drafter, critic, prototyper),
  each one's spawn trigger, how work hands off between them, and which surface each runs on
  (Claude.ai, Claude Code, Cowork). Use when the user or a fellow wants a fleet or team of agents,
  asks how agents should hand off, or wants to orchestrate agents for recurring work like weekly
  research. Not for one agent's role, tools and memory (use agent-design).
type: generator
supersedes: none
---

# Workflow-Design

## What it does

Turns "I'll spin up some agents" into a directed workflow of specialised agents, each
summoned by a rule and dismissed by a rule, run across the three surfaces where the work
actually belongs. The fellow describes the work; the skill first checks whether a fleet is
even warranted, then lays out the multi-step orchestration, assigns the spawn-by-rule fleet
(researcher / analyst / prototyper / drafter / critic — a menu, not a requirement), wires
each agent to an observable spawn trigger and a done condition, and puts every step on the
right surface: Think in Claude.ai, Build in Claude Code, Admin in Cowork. It refuses the two
things fellows reach for: a lone agent doing work that needs a fleet, and a "fleet" that is
really five chat windows with no triggers.

## The Icarus reframe

A workflow is not a chat thread and a fleet is not a tab bar. It is a directed graph of
agents where each agent is spawned by a **rule you could write as an if-condition**, not by
the fellow remembering to open a new window. The unit of design is the spawn trigger — the
observable event that summons an agent and the done signal that dismisses it. The five
archetypes divide labour by **cognitive mode** (gather, structure, make tangible, compose,
falsify), not by topic; you never spawn "the marketing agent", you spawn the critic because
a draft crossed the review threshold. And the critic must be a different agent from the
drafter for the same reason a validator is never the model that wrote the output: nothing
critiques its own work. The three surfaces are three modes, not three logos — diverge in
Claude.ai, build deterministically and repo-grounded in Claude Code, schedule and monitor
the running fleet in Cowork — and putting a step on the wrong surface is the commonest waste
in the whole build.

## When to use / When NOT

Use when: the work has independent sub-tasks that can run in parallel, or a role conflict
that one head cannot hold (drafting and critiquing at once), or depth that overruns a single
context; and the question is now how the agents coordinate and when each one fires.

| Not this skill | Use instead | Why |
|---|---|---|
| "Spec one agent — its role, tools, and memory layer" | `agent-design` | That designs a single agent's guts. This coordinates several. If the honest answer is one agent, route there — a fleet for solo work is theatre. |
| "Design the product's system: input → router → retrieve → reason → validate → output" | `compound-system-architecture` | That is the product's internal request-time pipeline — how a user request is processed. This is the fellow's build/operate fleet — the agents that do the WORK, with a different lifetime and graph. |
| "Write the golden cases and the acceptable failure rate" | `eval-first-spec` | That is the scoreable contract. The critic here runs against those cases; it does not write them. |
| "Make the UI / craft the interface" | `impeccable`, `design/*` | Route the prototyper's craft there. Do not restate a design skill inside the fleet map. |

If the input is a bare one-liner with no work named ("set up some agents for my startup"),
do not invent a fleet. Ask the one question that unblocks it — what work needs doing, and
what artefact does it produce? — or return the smallest honest next step.

## Method

Copy this checklist:

```
Workflow-Design progress:
- [ ] Step 0: Fleet-or-solo gate — does this even need more than one agent?
- [ ] Step 1: State the one-sentence workflow job
- [ ] Step 2: Map the multi-step workflow (each step: owner, artefact, gate)
- [ ] Step 3: Assign the fleet — pick the archetypes actually needed
- [ ] Step 4: Wire every spawn trigger as an observable event + done signal
- [ ] Step 5: Assign each step a surface (Think / Build / Admin) and say why
- [ ] Step 6: Critic-independence check
- [ ] Step 7: Run the kill line before returning
```

**Step 0 — fleet-or-solo gate.** Before designing a fleet, prove one is needed. Score the
three tests; a fleet is warranted only if at least one is a hard yes.

| Test | Question | Yes means |
|---|---|---|
| Parallelism | Are there ≥2 sub-tasks that could run at the same time with no shared state? | fan-out pays |
| Role conflict | Does one agent have to both produce and judge the same artefact? | split drafter/critic |
| Context depth | Does the whole job overrun one agent's usable context or memory? | decompose |

If all three are no, the answer is one agent. Say so, route to `agent-design`, and stop. Do
not build a fleet to look busy.

**Step 1 — the workflow job.** One sentence: what work the whole fleet turns into what
artefact, for whom. Not a list of agents. If it needs "and" three times, it is more than one
workflow.

**Step 2 — the multi-step workflow.** Fill the step table in [template.md](template.md).
Every step names its input, its owner agent, the artefact it emits, and the gate that must
pass before the next step starts. A step with no output artefact is a meeting, not a step.

**Step 3 — assign the fleet.** The five archetypes are a menu. Use the ones the work needs;
mark the rest "n/a — not needed, why". Each is a cognitive mode, not a topic.

| Agent | Cognitive mode | Spawns when | Done when | Hands off to |
|---|---|---|---|---|
| Researcher | Gather + source | a claim is tagged `[Assumption]`/`[Hypothesis]` with no source | claim is sourced or demoted | Analyst |
| Analyst | Structure + quantify | raw facts need a model, a number, or a decision | the number is built with the arithmetic shown | Drafter / Critic |
| Prototyper | Make tangible | a concept needs a concrete thing to react to | a paper/clickable artefact exists | Critic / user |
| Drafter | Compose | a decision or spec must become an artefact | the artefact is complete against its template | Critic |
| Critic | Falsify | a draft/artefact crosses the review threshold | verdict: pass, or a named defect list | Drafter (loop) / human |

**Step 4 — wire the spawn triggers.** This is the core of the skill. Every trigger has three
parts: an observable EVENT, a CONDITION/threshold, and a DONE signal. "When we need research"
is not a trigger — it is a wish. Fill the wiring table and score each trigger on the ladder:
a trigger you can point at an artefact state for is at least 0.5; a vibes trigger is 0.1 and
fails. Every loop (critic → drafter) needs an exit: a max-iteration count or an escalate-to-
human condition, or it spins forever.

**Step 5 — assign surfaces.** Pick the surface by the mode of the step, not by habit.

| Surface | Mode | Belongs here |
|---|---|---|
| Think — Claude.ai | Diverge, explore, no-tools reasoning | researcher's gather, analyst's framing, invention, first concepts |
| Build — Claude Code | Deterministic, repo-grounded, tooled | prototyper's clickable, drafter's spec-against-repo, the eval harness, anything touching files |
| Admin — Cowork | Schedule, fan-out, monitor the running fleet | recurring triggers, parallel dispatch, watching the fleet, hand-back to human |

**Step 6 — critic-independence check.** The critic is a separate agent from the drafter. If
the same agent drafts and critiques, the critic does not exist and quality is self-graded.

**Step 7 — the kill line.** Run the self-check at the foot of [template.md](template.md).

## Evidence standard

Money moved 1.0 → behaviour observed 0.7 → artefact shown 0.5 → verbal commitment 0.3 →
opinion 0.1. Here the ladder scores the **spawn triggers**, because that is where a fleet is
either a machine or a mood board. A trigger tied to opinion ("spawn the researcher when it
feels stuck", 0.1) fails; a trigger tied to an observable artefact state ("the draft holds an
unsourced `[Assumption]`", 0.5) passes; the bar to aim for is behaviour (0.7) — the fleet has
run once and the handoff artefacts actually appeared. The two bars are not in tension: 0.5 is the
design-time pass bar every trigger must clear (a trigger can only be pointed at an artefact state
before the fleet has run), and 0.7 is the post-run read of a fleet that has actually executed — so
do not dock a valid 0.5 design-time trigger for not yet reaching 0.7. The critic's verdict is held to the same
ladder: "looks good" is opinion 0.1 and does not close a review; a verdict must cite the
artefact or eval result it checked. Tag every empirical claim about volume, cadence, or cost
`[Fact]`, `[Assumption]`, or `[Hypothesis]`. A workflow is done when every trigger reads as an
if-condition, not a hope.

## Gotchas

- **The tab-switching fleet.** Five agents with no triggers is five chat windows you switch
  between by hand. If the fellow has to remember to spawn an agent, it is a to-do list, not a
  fleet. The tell: a fleet table with a roster but a blank or vibes trigger column.
- **The self-critiquing drafter.** The same agent that writes the draft also "checks it". That
  is the fleet-level disappearing guardrail — the critic is decoration and quality is self-
  graded. Split them, or admit there is no review.
- **Over-orchestration.** A fleet for work one agent could do in one context is the more common
  failure than under-orchestration, and it is more expensive. If Step 0 shows no parallelism,
  no role conflict, and no depth problem, a fleet is theatre; route to `agent-design`.
- **Wrong surface.** Divergent thinking pushed into Claude Code (slow, over-tooled) or a repo
  build attempted in Claude.ai (no files, no ground truth). Cheap to fix once named, expensive
  to leave. Match surface to mode.
- **Loops with no exit.** A critic → drafter loop with no max-iteration or escalate condition
  runs until someone notices. Every loop names its exit.

## Examples

[examples/sample.md](examples/sample.md) — Barrier Intelligence's discovery-to-v1 build run
as a spawn-by-rule fleet: researcher mines rig field logs and permit data, analyst quantifies
near-miss base rates, prototyper builds a paper alert card, drafter writes the alert-rule spec,
and an independent critic falsifies each rule against known incidents — with every spawn trigger
written as an observable event and the surface split (Think / Build / Admin) called for each step.

## Related skills

- `agent-design` — designs a single agent's role, tools, memory layer, and eval. This skill
  coordinates several such agents; each node in this fleet is one `agent-design` output. When
  Step 0 returns solo, hand the whole thing there.
- `compound-system-architecture` — the product's internal request-time pipeline (input →
  router → retrieve/reason/act → validate → output). That graph runs inside the shipped product
  per user request; this graph is the fellow's build/operate fleet with a different lifetime.
  Do not conflate the two routers.
- `eval-first-spec` — the golden cases the critic runs against. This skill spawns the critic;
  that skill writes what the critic checks.
- `impeccable`, `design/*` — where the prototyper's UI craft is done. Route to them; do not
  restate a design system inside the fleet map.
- Supersedes nothing. It is the multi-agent orchestration gate in the build-craft stage,
  paired with `agent-design` (single agent).
