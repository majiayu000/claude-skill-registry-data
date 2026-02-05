---
name: add-dag-node
description: >
  Scaffold a new DAG node in afi-reactor, wire it into the pipeline, and ensure
  all types and validators are imported from afi-core while obeying AFI
  Orchestrator Doctrine and the AFI Droid Charter.
---

# Skill: add-dag-node (afi-reactor)

## Purpose

Use this skill when you need to add a **new DAG node** to the AFI Reactor
pipeline, wire it into the existing graph, and keep everything aligned with:

- AFI Droid Charter
- AFI Droid Playbook
- afi-reactor/AGENTS.md
- AFI Orchestrator Doctrine (the "10 Commandments")
- Canonical types and validators from `afi-core`

This skill is primarily used by `dag-builder-droid` and any future reactor droids
that work on the DAG.

---

## Preconditions

Before changing anything, you MUST:

1. Read:
   - `afi-reactor/AGENTS.md`
   - AFI Orchestrator Doctrine file referenced there
   - AFI Droid Charter
   - AFI Droid Playbook

2. Confirm:
   - The requested node belongs in **afi-reactor** (orchestration), not in
     `afi-core` (validators / runtime logic) or `afi-config` (governance).
   - The change does **not** require editing smart contracts, Eliza configs, or
     deployment/infra repos.

If any requirement is unclear or appears to violate Doctrine or AGENTS.md,
STOP and ask for human clarification instead of trying to be clever.

---

## Inputs Expected

The caller should provide, in natural language or structured form:

- Node name (e.g. `NewsSentimentEnricher`, `GreeksScorer`)
- Node purpose:
  - What this node does in one or two sentences
- Lifecycle stage:
  - One of: `Raw`, `Enriched`, `Analyzed`, `Scored`
- Inputs:
  - What data it expects, and from which upstream node(s) or stage(s)
- Outputs:
  - What it emits and which downstream nodes or stage(s) should consume it
- Canonical types / validators:
  - Which types / schemas / validators exist in `afi-core` that should be used,
    if known

If any of this information is missing, ask clarifying questions or produce a
minimal, clearly-labeled stub that's safe to evolve later.

---

## Step-by-Step Instructions

When this skill is invoked, follow this sequence:

### 1. Restate the requested change

In your own words, summarize:

- The node's purpose
- Its lifecycle stage
- Its upstream and downstream relationships

This summary should be short and precise, so humans can quickly confirm the
intent.

---

### 2. Locate the DAG structures

Identify the current DAG layout and relevant files, typically including:

- DAG engine and orchestration code (e.g. `src/core/dag-engine.ts` or similar)
- DAG graph or codex (e.g. `config/dag.codex.json` or similar config files)
- Any codex/metadata that describes nodes and stages (e.g. `codex/*.json`)
- Any existing node patterns in `src/dags/` (or equivalent)

Do **not** modify these yet; just understand how the DAG is currently modeled.

---

### 3. Create the node scaffold

Create a new node file under the appropriate folder, for example:

- `src/dags/<stage>/<nodeName>.ts`  
  or
- `src/dags/<nodeName>.ts`

Follow any existing naming and folder conventions in afi-reactor.

In the new file:

1. Import canonical types / schemas / validators from `afi-core` where needed.
   - Never re-define schemas or validators that already exist in `afi-core`.
2. Export a clearly named function such as:
   - `runNode`, `execute`, or the project's established pattern.
3. Keep implementation minimal:
   - If the logic is not well-specified, stub the body with `TODO` comments and
     clearly throw or return a safe placeholder.
   - Do **not** implement complex business logic unless explicitly requested.

All comments should be clear, referencing:

- The node's purpose
- Its lifecycle stage
- Any assumptions or TODOs

---

### 4. Wire the node into the DAG graph

Update the DAG graph / codex / configuration files so this new node is part of
the pipeline:

1. Register the node with:
   - Unique identifier / key
   - Stage (Raw / Enriched / Analyzed / Scored)
   - Input/output relationships (upstream/downstream nodes)
2. Ensure the wiring respects:
   - No forbidden cycles (unless explicitly allowed by the Doctrine)
   - The existing pipeline architecture and naming conventions
3. If there is a central registry for node metadata, add a minimal entry using
   the existing pattern.

If wiring rules are ambiguous or require architectural changes, STOP and mark
this as a human decision point.

---

### 5. Add minimal tests or runners (optional but recommended)

Where patterns already exist (e.g. in `ops/runner/` or `test/`):

- Add a small integration test or runner stub that:
  - Constructs a minimal signal or input
  - Passes it through the new node
  - Asserts basic shape/flow (not business outcomes)
- Do not introduce new test frameworks or heavy dependencies.

If no test patterns exist yet, leave a clearly marked TODO and surface this
in your summary.

---

### 6. Validate and build

Run at least:

- `npm run build` in `afi-reactor`

If relevant quick tests exist and are safe to run:

- `npm test` (or the closest equivalent)

Do not mark the skill as "successful" if the build fails. Instead, stop, gather
error output, and surface it with minimal, clear commentary.

---

## Hard Boundaries

When using this skill, you MUST NOT:

- Create or modify validators or schemas in `afi-reactor`.
  - Those belong in `afi-core` or `afi-config`.
- Duplicate or move canonical logic from `afi-core` into `afi-reactor`.
- Modify any other repos (`afi-token`, `afi-eliza-gateway`, `afi-config`,
  `afi-ops`, `afi-infra`, etc.).
- Introduce new external services, queues, or transports.
- Perform large, sweeping refactors of the DAG architecture without explicit
  human approval.
- Change tokenomics, emissions, or smart contracts.

If a request forces you towards any of the above, STOP and escalate.

---

## Output / Summary Format

At the end of a successful `add-dag-node` operation, produce a short summary
that includes:

- Node name and stage
- Files created
- Files modified (graph/config/metadata)
- Any new tests or runners added
- Any TODOs or open questions that must be resolved by a human

Aim for something a human maintainer can read in under a minute to understand
exactly what changed and why.

---

## Example Usage Patterns

You should use this skill for requests like:

- "Add a new Raw-stage node that normalizes exchange metadata before enrichment."
- "Insert a News Sentiment Enricher node between the Enriched and Analyzed stages."
- "Wire an existing afi-core validator into a Scored-stage node that computes
  a composite score."

You should NOT use this skill for:

- Changing how PoI/PoInsight are defined at the validator/agent level.
- Modifying Eliza agents, character specs, or AFI gateway behavior.
- Editing or deploying smart contracts.

