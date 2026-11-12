---
name: policy-brief
description: "Writes a policy brief: key message, evidence, risks, options and caveats in plain, honest language."
---
<!-- Generated from .claude/skills/policy-brief/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /policy-brief — Policy Brief

**Category:** Documentation · **Primary agent:** `policy-relevance-specialist`

Writes a policy brief: key message, evidence, risks, options and caveats in plain, honest language.

Arguments: whatever the user wrote after the command name.

## Purpose
Write a policy brief that turns model results into a decision-ready message: bottom line first, the evidence, the risks, the options and their trade-offs, with uncertainty and the most important caveats in the main text. Every number traces to a model run. The output is short, honest and readable by a senior decision-maker in minutes.

**Use it when** results must inform a decision or be shared with non-technical audiences.

**Do not use it when** a methodology document is needed (`/technical-note`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Model results
   - Scenario/risk analysis
   - Audience description
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `policy-relevance-specialist` — primary agent; coordinates the work and integrates results
- `policy-brief-writer` — Writes policy briefs and notes
- `stakeholder-liaison-specialist` — Interfaces with stakeholders and counterparts
- `economic-reasoning-specialist` — Frames the economic question and tests whether results make economic sense

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Audience | senior decision-makers, policy analysts, public | Tone and length |
| Length | one page, two to four pages, with annex | Detail |
| Uncertainty | ranges, scenarios, fan charts | Communication |
| Options | single recommendation, menu with trade-offs | Decision support |

## Workflow
1. Ask the audience, decision and length
2. Draft bottom line, evidence, risks, options; keep technical detail in an annex
   - Explain mechanisms in plain language without distorting them
3. Check each number against the model run; include uncertainty ranges
4. Obtain economic-reasoning-specialist and policy-relevance-specialist review; adjust to feedback

## Checkpoints with the user
- After the bottom line: confirm the message
- Before release: confirm caveats and numbers

## Common pitfalls
- Burying the message
- False precision
- Caveats in footnotes
- Mixing model results and judgment without labels

## Output
`docs/briefs/<name>-brief.md`; a Word version or slides on request (`python tools/report.py docx|pptx <file.md> --out <file>`, charts embedded)

The brief has a bottom line, evidence, risks, options, uncertainty and caveats in the main text, and a technical annex; a number-tracing table supports review.

## Gate / verdict
- Uncertainty and top-3 caveats are in the main text
- Every number traces to a model run
- Model results, assumptions and judgment are distinguished

## Suggested next steps
- `/chart-pack`
