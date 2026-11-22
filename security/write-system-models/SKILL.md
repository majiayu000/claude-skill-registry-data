---
name: write-system-models
description: Use when drafting, revising, or auditing an engineering-paper System Model and Problem Formulation, especially when the operational flow is unclear, symbols precede definitions, timing or state transitions are incomplete, constraints lack physical meaning, the formulation does not close the preceding model, or a rewrite unnecessarily redesigns an established architecture.
---

# Write System Models and Problem Formulations

## Purpose

Write the model in the order the system operates and formulate a problem that closes, rather than recreates, that model. Preserve an established architecture when supplied; introduce only the modules required by the new setting; and make every state, decision, equation, constraint, and objective traceable.

## Required resources and routing

1. Always read [the core contract and quality gates](references/core/contract-and-quality-gates.md) in full.
2. Always read [the reader and terminology contract](references/core/reader-and-terminology-contract.md).
3. Read [the house-style card](references/styles/house-style-card.md) unless the user names another venue or team style. It governs author voice, sentence rhythm, connectives, subsection titles, paragraph openers, captions, and equation lead-ins, and it overrides the generic example sentences of this skill where they differ. When drafting or revising, also read Sections 8, 9, and 13 (titles, model openers, captions and equation lead-ins) of [the full team house style](references/styles/team-house-style.md); read its other sections only when the card's last table names them.
4. Read [the Chinese manuscript adapter](references/languages/zh.md) when the manuscript is written in Chinese.
5. Read [the MEC domain pack](references/domains/mec.md) only for mobile edge computing, UAV-MEC, HAP-UAV, vehicular edge computing, dispersed edge computing, or directly adjacent MEC systems. It also holds the reference-scale table.
6. If no domain pack matches, infer the operational workflow and physical checks from the target architecture and authoritative sources. Do not reuse MEC equations or module order by analogy alone.
7. Run [the fingerprint script](scripts/style_fingerprint.py) on the draft before delivery when Python is available, with the ranges of the scale statement as `--scale` and the term ledger as `--terms`. `--spine --section model` prints the paragraph-opening sentences for the center-sentence audit.

## Highest-priority rule: inherit before extending

When a reference architecture or existing model is supplied, first create:

| Model element | Inherited | Adapted | New | Removed | Reason and evidence |
|---|---:|---:|---:|---:|---|

Cover entities, topology, timing, workflow, physical or service relations, decisions, states, objectives, and constraints. Preserve valid notation and ordering unless a demonstrated dependency or correctness issue requires change. Never present inherited relations as new contributions.

## Workflow

### 1. Recover the system contract

Identify:

- actors, sets, and controller or decision owner;
- physical or logical topology;
- static, mission, event, cycle, or slot timing;
- exogenous parameters and observations;
- state measured at a named instant;
- decisions and their selection instant;
- event order within one decision interval;
- derived performance measures;
- feasibility constraints;
- initial, boundary, terminal, success, and failure behavior.

Mark any missing item as an unresolved requirement.

### 2. Build the dependency graph

For every equation, record its inputs and output, then topologically order the modules. Prefer operational dependency over a topic taxonomy. A scenario-specific module belongs where its inputs have already been defined; an explicit forward reference is required when that order cannot be followed.

### 3. Write the overview as a model map

Open with a compact paragraph that defines the actors and control boundary, time convention, operational cycle, decision vector at a high level, objective family, and subsection map. Do not front-load all symbols. Follow the section-opening rules in the core contract: one overview paragraph and then the first module, no standalone overview subsection, generic subsection titles, at most one forward pointer, and the initial state declared before any recursion.

### 4. Draft each module locally

Use:

`operational transition -> assumptions and primitives -> derived relation -> physical interpretation -> local constraint`

Define every symbol at first use, state domains and units, explain one paper-relevant coupling after each equation block, and place each constraint beside the relation it governs. Keep one dependency chain together.

For dynamic models, specify observation, action, realization, update, and terminal order. Simulate one interval by hand and ensure all branches are mutually exclusive, exhaustive, and feasible.

### 5. Close the formulation

The final problem display may collect previously introduced content, but it may not create new physics. It must state the decision variables, objective direction and aggregation, all active constraints, variable domains, uncertainty semantics, and horizon or policy semantics.

Create a decision traceability matrix:

| Decision | Relation affected | Constraint or domain | Objective path | Decision instant |
|---|---|---|---|---|

Fail the formulation if a claimed decision has no downstream effect, an objective relies on an uncontrolled quantity, or an online decision depends on unavailable future information.

### 6. Preserve the model-method boundary

The model defines physical state, observations, decisions, objectives, feasibility, and causal policy restrictions. Encoding, repair, action masking, network design, search operators, loss functions, training schedules, and algorithm-loop complexity belong in the method section.

### 7. Run the audit

Apply the core inheritance, symbol, causality, timing, dimensional, constraint, traceability, and formulation gates, followed by the selected domain gates. Check headings, first sentences, first symbol occurrences, dependency order, units, one complete interval, decision-to-objective paths, and exact closure between local constraints and the final display.

## Reader gates (check before delivering)

1. Every coined term is defined by function at first use (T); no variable-like names for decisions or objectives.
2. Every definite expression has an antecedent (A); every action has a purpose or a cost (Q).
3. Each proposition has one home (D); each universal or negative claim is tagged and supported (C).
4. Length is inside the declared scale range, or the deviation is recorded (S).
5. Sentence rhythm and connectives are inside the house-style band, or each remaining flag and its reason are listed in the delivery note, not in the manuscript (R).
6. Ledgers and notes stay out of the manuscript (H).

## Output constraints

- Match the manuscript's notation, language, and section architecture.
- Keep ledgers, term tables, and audit notes out of the manuscript text and appendices unless the user asks for them.
- In an audit, distinguish architecture, causal or state, equation or notation, and formulation failures.
- Make the smallest change that resolves a demonstrated dependency or correctness problem.
- Do not redesign a valid model merely because another organization is possible.

