---
name: build-sfc
description: "Builds a stock-flow consistent model with balance-sheet and transaction matrices and scenario runs."
---
<!-- Generated from .claude/skills/build-sfc/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /build-sfc — Build SFC

**Category:** Build · **Primary agent:** `sfc-modeler`

Builds a stock-flow consistent model with balance-sheet and transaction matrices and scenario runs.

Arguments: whatever the user wrote after the command name.

## Purpose
Build a stock-flow consistent model: a sectoral model in which every flow comes from somewhere and goes somewhere, every stock changes only through flows and revaluations, and balance sheets of households, firms, banks, government and the rest of the world are tracked explicitly. The output is a model consistent by construction, used for scenarios about debt, credit, financial balances and policy.

**Use it when** sectoral balances, balance sheets, credit and debt dynamics are central, and accounting consistency across sectors is the main discipline needed.

**Do not use it when** optimizing behavior and expectations are central (`/build-dsge`), or agent heterogeneity is the focus (`/build-abm`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Flow-of-funds and national accounts data
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `sfc-modeler` — primary agent; coordinates the work and integrates results
- `financial-stability-stress-testing-specialist` — Builds systemic risk and stress-testing frameworks

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Sectors | households, firms, banks, government, monetary authority, rest of world | Coverage of balance sheets |
| Assets | money, deposits, loans, bonds, equities, foreign assets | Portfolio choices and valuation |
| Behavior | consumption from income and wealth, portfolio rules, investment rules | Dynamics |
| Prices | fixed, markup, valuation of assets | Revaluation effects |
| Calibration | to flow-of-funds data, stylized | Empirical relevance |

## Workflow
1. Define the transaction-flow and balance-sheet matrices
   - Rows and columns sum to zero; every entry has a counterpart
2. Derive equations and verify stock-flow consistency by construction
   - Identify the redundant equation and check it holds in simulation
3. Calibrate to data and run baseline
   - Use flow-of-funds and sectoral accounts (`/data-requirements`)
4. Run debt, credit and policy shock scenarios
5. Compare dynamics with a DSGE or semi-structural benchmark
6. Register the model as a lego set (`/lego-map`): a baseplate plus bricks with declared studs (variables, units, timing) and stubs, so components can later be attached, detached or swapped

## Checkpoints with the user
- After the matrices: confirm sectors and assets
- After behavioral equations: confirm their sources
- After the baseline: confirm sectoral balances are plausible

## Common pitfalls
- Dropping the redundant equation without checking it holds
- Revaluation effects ignored
- Behavioral parameters without empirical grounding
- Reading accounting consistency as validity of behavior

## Output
`models/sfc/<name>/ (+ model.lego.json)`

The folder holds the transaction-flow and balance-sheet matrices, model code, calibration files, scenario scripts, the benchmark comparison and the lego manifest. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Matrices balance
- No redundant-identity violations
- Lego manifest passes `python tools/lego.py check`
- The redundant identity is verified in every simulation
- Behavioral equations are sourced or labeled as assumptions

## Suggested next steps
- `/validate-model`
- `/scenario-analysis`
- `/lego-map`
