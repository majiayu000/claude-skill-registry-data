---
name: agent-design
description: >-
  Fires when a fellow is designing ONE production agent and asks what it should be built from —
  "design an agent for X", "what tools and memory does this agent need", "spec the agent",
  "our agent isn't getting smarter / never remembers corrections — how do we build its memory".
  Returns a four-part agent spec — role (one owned decision) · tools (the commodity shell) ·
  memory layer (CLAUDE.md · skills · lessons.md · trace archive, loaded at birth) · eval — where the
  memory layer is the only part the fellow owns and therefore the only part that compounds. Do NOT
  fire for the agent's voice / persona / signature phrases (use meta/agent-persona-builder), the
  multi-agent fleet or hand-offs (use workflow-design), writing its golden cases / autonomy level /
  cost budget (use eval-first-spec — this skill routes there and carries the number), or the
  post-launch ship-observe-learn-refine loop and autonomy-raise (use refine-flywheel).
type: generator
supersedes: none
---

# Agent Design

## What it does

Turns "we want an agent for this" into a spec built from four parts, in order of how much of it the fellow actually owns: a **role** stated as one decision the agent owns at a chosen autonomy level; the **minimum tool set**, each tool with its blast radius and guardrail; the **memory layer** — CLAUDE.md, skills, an append-only lessons.md, and a trace archive, each with a load trigger and a writer — which is the owned, compounding part and gets most of the design budget; and the **eval** that proves the whole thing works and is getting better, which is `eval-first-spec`'s golden set, routed there, not restated. The artefact is the filled `template.md`. An agent with no memory layer or no eval is not an agent; it is a prompt with tools, and it does not compound.

## The Icarus reframe

A generic agent design is a prompt, a tool list, and a model — and a competitor can rent the same model, wire the same tools, and copy the prompt from one screenshot in an afternoon. The one part that is yours and gets better only for you is the **memory layer**: CLAUDE.md for durable context, skills for tell-able procedure, an append-only lessons.md for the corrections that are the tacit half of the expertise, and a trace archive of every real run — all loaded into context at birth so run N starts smarter than run N−1. So this skill spends its effort on what gets written, by whom, and when it loads, treats role and tools as the cheap swappable shell around it, and makes an eval prove the memory is compounding rather than merely accumulating.

## When to use / When NOT

Use when a fellow has a validated workflow and needs to spec the single agent that runs it: the role, the tools, what it remembers, and how they will know it works. Trigger phrases: "design an agent for…", "what tools and memory should it have", "spec the agent", "our agent repeats the same mistakes — what's wrong with its memory layer".

| Not this skill | Use instead | Why |
|---|---|---|
| "Give it a personality / voice / signature phrases / make it sound like someone" | `meta/agent-persona-builder` | That designs SOUL/AGENTS/MEMORY/BOOTSTRAP — the agent's voice and operating manual. This designs the product spine (role · tools · memory-as-compounding-asset · eval). A voice is not a moat; a lessons.md is. Compose them; do not restate the persona mechanics here. |
| "Design the fleet / how do the agents hand off / who spawns whom" | `workflow-design` (sibling, 09) | That is the multi-agent orchestration. This specs ONE agent. If the answer needs a researcher, an analyst, and a critic passing work, that is a fleet — route it. |
| "Write the golden cases / set the autonomy level / what's the cost-per-outcome" | `eval-first-spec` (07) | That IS the agent's eval. This skill points at it and carries its autonomy level and number as constraints; it does not re-derive them. |
| "What's the post-launch loop / should we raise autonomy / re-run on the new model" | `refine-flywheel` (08) | That runs the ship→observe→learn→refine loop over a live agent. This designs the memory-layer *structure* the loop then turns. Structure here; cadence there. |
| "How do we build this AI system / the component pipeline / the effort split" | `compound-system-architecture` (07) | That is the system the agent may sit inside (router, retrieve, validate). This is one agent's internals. They compose. |

If the input is a bare "build me an agent" with no workflow, do not invent one. Ask the one question that unblocks it — which single decision does it own? — or return the smallest honest next step.

## Method

Copy this checklist:

```
Agent-design progress:
- [ ] Step 1: State the role as ONE owned decision + its autonomy level
- [ ] Step 2: Spec the minimum tool set (each: job, blast radius, guardrail)
- [ ] Step 3: Design the memory layer — four stores, each with a load trigger AND a writer
- [ ] Step 4: Point at the eval and state what it gates
- [ ] Step 5: Run the compounding check + the kill line
```

Fill in `template.md`.

### Step 1 — Role: one owned decision

One sentence: **which single decision** the agent makes or compresses, for **whom**, on **what trigger**, at **which autonomy level** L0–L4. The autonomy level is *carried from* `eval-first-spec`, not chosen here to sound advanced.

Good: "At each permit request on the rig, the agent decides hold-or-proceed on the gas hazard and drafts the reason for the duty safety officer — autonomy L1, the officer commits every one." Not a role: "an AI copilot for safety officers." That is an engine, not a decision. Name the gap and ask for the decision. Do not invent it. The agent's *voice* — how it phrases that draft — is `agent-persona-builder`'s job, not this step.

### Step 2 — Tools: the commodity shell

The fewest tools that deliver the role. Each row of the tool table:

| Field | Rule |
|---|---|
| Job | The one thing this tool does for the role. |
| Blast radius | Read · Write-reversible · Write-irreversible. Drives the guardrail. |
| Guardrail | For any Write, the check before it fires. High blast → route the rule to `guardrail-design`. |
| Exercised by | The eval case(s) that call it. A tool no golden case touches is cut — it is attack surface, not capability. |

Two rules: a tool whose blast radius exceeds the chosen autonomy level does not belong on the agent (at L1, no tool that *commits* an action — that is the human's). And tools are the commodity part; spend the least design effort here and move the budget to Step 3.

### Step 3 — Memory layer: the part you own

This is the section that matters. Four stores. Fill every column for each — a store with no load trigger never enters the agent's head; a store with no writer stays empty; neither compounds.

| Store | Holds | Written by | Load trigger | Compounding role |
|---|---|---|---|---|
| **CLAUDE.md** | Durable operating context: system facts, the org map, standing rules, thresholds | Human, curated | At birth, every run | Stops the agent re-learning context each session |
| **skills** | Tell-able, repeatable procedures the agent invokes | Explicit capture — route to `explicit-vs-tacit-capture` | Registered at birth; invoked on demand | The *explicit* half of the expertise, versioned |
| **lessons.md** | Append-only log of corrections + failures — one entry each, what was changed and why | The agent / operator, the moment a correction happens | At birth, every run | The *tacit* half accretes here — the defensible part |
| **trace archive** | Every run: input, output, human edit, outcome | The system, automatically | Sampled into eval + discovery (not all into context) | YODA moat + eval fuel + the discovery corpus |

Then the ownership test — why the memory layer, and only the memory layer, is where value compounds:

| Part | Who owns it | Copyable by a competitor? |
|---|---|---|
| Base model | Rented from a lab | Yes — they rent the same one; it improves for everyone at once |
| Tools | Commodity APIs / MCP servers | Yes — same servers, an afternoon's wiring |
| Role / prompt | Visible in one screenshot | Yes |
| **Memory layer** | Accrues from YOUR traces and YOUR corrections | **No — path-dependent workflow exhaust, unique to you** |

State the **compounding mechanism** for this agent, concretely: name the run that got better *because of* what a store captured. For example, "the drain-cross-check correction logged in lessons.md in week 2 turns golden case #17 from fail to pass on the week-3 re-run." If you cannot name a mechanism like that, the memory layer is a filing cabinet, not a flywheel — say so.

### Step 4 — Eval: the instrument that reads compounding

The agent's scoreable contract is `eval-first-spec`'s output: the job line, 20 golden cases (drawn from the trace archive), the autonomy level with derived failure rates, and cost-per-outcome to the cent. Do not restate it. Route there and record what the eval **gates** for this agent:

- **Model swap** — a new model ships only if it holds the eval, not on its headline benchmark.
- **Autonomy promotion** — the level rises only on a measured pass rate over N real cycles.
- **Compounding proof** — the eval is the instrument that reads whether the memory layer made run N beat run N−1. No eval, and you cannot tell whether any change — a new lesson, a new tool, a new model — helped or hurt.

An agent with no eval is a demo. This is a kill condition.

### Step 5 — Compounding check + kill line

Run the self-check at the foot of `template.md`.

**Kill line.** An agent spec ships only when: the role is one owned decision (not "assistant for X") with an autonomy level; the memory layer has all four stores, each with a load trigger AND a writer; at least one store (lessons.md or trace archive) accrues from the agent's OWN runs, not just human-authored config; the compounding mechanism is named; and the eval exists (routed to `eval-first-spec`) and gates model-swap, autonomy, and the compounding proof. Any part missing = not an agent spec. Name which, and the smallest next step. A role and a tool list with no compounding memory is a chatbot; do not ship it as an agent.

## Evidence standard

Every Icarus skill weights behaviour and money over opinion:

| Signal | Score |
|---|---|
| Money moved | 1.0 |
| Behaviour observed | 0.7 |
| Artefact shown | 0.5 |
| Verbal commitment | 0.3 |
| Opinion | 0.1 |

Here the ladder scores the **memory layer's compounding claim** — the same discipline `compound-system-architecture` applies to its data layer. "The agent will learn over time" is opinion (0.1) and does not clear the bar. The bar is behaviour (0.7): lessons.md holds real entries from real corrections, the trace archive holds real runs (artefact, 0.5+), and the eval score *rose* after those entries were written. A memory layer whose stores are all empty or hypothetical is scored `[Hypothesis]` and fails — you have designed a filing cabinet, not a compounding asset. Tag every claim about traces, corrections, tools, cost, or accuracy `[Fact]`, `[Assumption]`, or `[Hypothesis]`. If the trace archive is `[Hypothesis]` because the workflow has never been run, the honest output is "run it by hand first to seed real traces, then design the agent" — not a spec resting on data that does not exist.

## Gotchas

Memory as a filing cabinet, not a flywheel. The stores exist on disk but never load at birth, or nobody writes lessons.md, so run 100 is no smarter than run 1. A store with no load trigger and no writer is decoration. The compounding mechanism in Step 3 is the test: name the run that got better because of what memory captured, or the layer is not a memory layer.

Over-designing the tools, under-designing the memory. Fellows spend the whole design budget on the tool list — the commodity part — and hand-wave the memory ("it'll remember things"). Invert it. Tools are the shell; the memory layer is where the moat lives. If the tool section is longer than the memory section, the priorities are backwards.

Confusing the spine with the persona. SOUL.md, voice, and signature phrases are `agent-persona-builder`'s job. Designing a personality here and filing it under "memory" is a category error: a voice is style, not a compounding asset. The two skills compose — persona for how it sounds, this for what it decides, remembers, and is scored on.

lessons.md that logs praise, not corrections. A memory that only records wins teaches nothing — the tacit moat is in what the human changed and why. If every entry reads "worked well," the log is theatre. The entries that compound are the overrides.

Skipping the eval because "we'll know if it's working." Without the eval you cannot swap the model safely, promote autonomy, or prove the memory compounds. "We'll feel it" is opinion (0.1). Route to `eval-first-spec` and carry the number.

## Examples

[examples/sample.md](examples/sample.md) — a worked agent spec for **Barrier Intelligence** (oil & gas safety): a permit-to-work gas-hazard reviewer at autonomy L1, four read/draft tools each tied to an eval case (and no commit tool, by design), a four-store memory layer whose lessons.md logs every safety-officer override, and the named compounding mechanism where one logged override turns an adversarial golden case from fail to pass on the next re-run. The eval is pointed at `eval-first-spec`, not restated.

## Related skills

`eval-first-spec` (07) — the agent's eval. This skill routes there for the job line, golden set, autonomy level, and cost-per-outcome, and carries them back as constraints. Agent without an eval is a demo; eval without an agent has nothing to score.

`compound-system-architecture` (07) — the AI system the agent may sit inside (input → router → retrieve/reason/act → validate → output). That designs the pipeline; this designs one agent's internals. The trace archive here is grounded in that skill's data layer.

`workflow-design` (09, sibling) — the multi-agent fleet and hand-offs. When one agent is not enough, route there. This skill is a single-agent spec; that one orchestrates several.

`meta/agent-persona-builder` — the agent's voice, SOUL.md, and operating manual. Compose it with this skill: persona for how the agent sounds, agent-design for what it owns, remembers, and is scored on. Do not restate its 25-question persona mechanics here.

`explicit-vs-tacit-capture` (03), `trace-to-interview` (08), `dataset-builder` (03) — feed the memory layer: explicit procedures become skills, the trace archive becomes discovery interviews and golden cases. `moat-design-canvas` (06) argues the defensibility that the compounding memory layer creates.

Supersedes: none. New skill; no prior product-agent design exists in the pack to replace.
