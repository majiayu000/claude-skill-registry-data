---
name: build-io-sam
description: "Builds input-output, supply-use and SAM frameworks with multipliers, linkages, multi-regional and environmentally extended extensions."
---
<!-- Generated from .claude/skills/build-io-sam/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /build-io-sam — Build IO SAM

**Category:** Build · **Primary agent:** `input-output-sam-specialist`

Builds input-output, supply-use and SAM frameworks with multipliers, linkages, multi-regional and environmentally extended extensions.

Arguments: whatever the user wrote after the command name.

## Purpose
Build an input-output, supply-use or social accounting framework that is balanced, documented and ready for multiplier and impact analysis, or as the benchmark dataset for a CGE model. The output is a reproducible table with automated balance checks, multipliers and linkages, and a clear statement of the fixed-coefficient limits that apply to any impact result.

**Use it when** the question concerns sectoral linkages, demand-driven multipliers, value-added content of trade, environmental footprints, or when a CGE model needs a benchmark SAM.

**Do not use it when** prices, substitution and supply constraints matter for the answer (`/build-cge`) or when the shock propagates mainly through supply bottlenecks (`/supply-chain-shock`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Supply-use or input-output tables
   - National accounts for the base year
   - Classification concordances
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `input-output-sam-specialist` — primary agent; coordinates the work and integrates results
- `national-accounts-specialist` — Specializes in national accounts and macro statistics
- `production-networks-specialist` — Models production networks and supply chains
- `trade-gvc-specialist` — Models trade and global value chains
- `carbon-pricing-emissions-specialist` — Analyzes carbon pricing and emissions policy

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Framework | national IO, supply-use, SAM, multi-regional IO | Questions answerable; data needs |
| Technology assumption | industry, product | Symmetric table construction |
| Aggregation | number and grouping of sectors | Aggregation bias; readability |
| Balancing method | RAS, GRAS, cross-entropy | Treatment of negatives; adjustment size |
| Extensions | value added in trade, emissions, employment | Satellite outputs |

## Workflow
1. Choose the framework (national IO, supply-use, SAM, multi-regional) and the sector classification; ask the user to approve
   - Document concordances between classifications
2. Construct and balance the tables (RAS/GRAS/cross-entropy where needed); automate balance checks
   - Report the size of each adjustment
3. Compute Leontief/Ghosh inverses, multipliers, linkages and, if relevant, value-added and environmental extensions
   - Distinguish Type I and Type II multipliers; flag Ghosh interpretation limits
4. Run impact analyses and state the fixed-coefficient limitations alongside results
   - Separate direct, indirect and induced effects; domestic and imported content
5. Document concordances, data sources, adjustments and reproduction steps
6. Register the model as a lego set (`/lego-map`; a stand-alone table uses the `core-io-leontief` baseplate): a baseplate plus bricks with declared studs (variables, units, timing) and stubs, so components can later be attached, detached or swapped

## Checkpoints with the user
- After choosing framework and classification: confirm before construction
- After balancing: confirm the adjustment sizes are acceptable
- Before impact runs: confirm the shock definition

## Common pitfalls
- Gross output multipliers reported as value added or welfare
- Summing multipliers across sectors
- Using an outdated table for a changed economy
- Ignoring imports, which overstates domestic effects

## Output
`models/io-sam/<name>/ (+ model.lego.json)`

The folder holds source data, construction and balancing scripts, the balanced table, multiplier and linkage tables, impact-analysis scripts and results, the documentation note and the lego manifest. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Row and column totals balance to tolerance
- Hawkins-Simon condition verified
- Adjustments and concordances documented
- Lego manifest passes `python tools/lego.py check`
- Fixed-coefficient limitations are stated with every impact result
- Impact results separate domestic and imported effects

## Suggested next steps
- `/build-cge`
- `/supply-chain-shock`
- `/validate-model`
- `/lego-map`
