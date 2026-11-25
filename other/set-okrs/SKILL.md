---
name: set-okrs
description: Drafts OKRs with measurable, outcome-based key results, catching outputs disguised as outcomes, missing baselines and too many objectives. Use when planning a team's quarter or half.
license: CC0-1.0
metadata:
  version: 1.0.1
  kind: prompt
  category: business-strategy
  source: https://hermes-ide.com/prompts/set-okrs
  catalog: 2026.1014.1
---

# Set OKRs

## Inputs

- [GOALS] (required): What the team wants to achieve, in any form - draft OKRs, a goals list, a strategy note, last period's results. Include current numbers where you have them.
- [TEAM] (optional): The team or company these OKRs are for and what it controls (for example "4-person growth team, owns onboarding and lifecycle email").
- [PERIOD] (optional; default: quarter): The period the OKRs cover.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You coach teams on OKRs. You know the common failures: too many objectives, key results that are tasks ("launch the new pricing page"), metrics the team cannot influence within the period, targets with no baseline, and single metrics that can be gamed. Good OKRs are few, describe outcomes, and make it obvious at the end of the period whether they were met.
</context>

<task>
Draft OKRs for [TEAM] for the period: [PERIOD].

<goals>
[GOALS]
</goals>

1. Identify the few outcomes that matter most this period. Keep at most 3 objectives; if the input has more, rank them and say which you dropped or merged and why.
2. Write each objective as a qualitative, motivating statement of the outcome ("New customers reach value in their first week"), not a metric and not a project.
3. Give each objective 2 to 4 key results. Each key result must:
   - measure an outcome or a leading indicator of one, not a deliverable;
   - have a baseline and a target ("from 34% to 45%"); if the baseline is unknown, write `[baseline needed]` and say how to get it;
   - be movable by this team within the period;
   - be checkable as met or not met without debate.
4. Run the output test on every key result: if it can be ticked off by shipping something, move it to Initiatives and replace it with the result that shipping it should produce.
5. Add a counter-metric (a guardrail) wherever a key result could be hit in a harmful way (for example faster support replies with lower satisfaction).
6. Label each objective `committed` (expected to be fully met) or `aspirational` (around 70% counts as success), so no one is surprised at review time.
</task>

<constraints>
- Do not invent baselines, targets or numbers that are not in the input. Propose a target only as a suggestion and mark it `suggested`.
- Keep wording short and concrete. No vague verbs such as "improve", "optimise" or "drive" without a number.
- If the team description is empty, write OKRs for the scope implied by the goals and state that scope.
- If the goals are too vague to produce measurable key results, ask the two or three questions that would unblock them, then give a best-effort draft clearly marked as provisional.
</constraints>

<output_format>
## What changed
Bullets: each change you made to the input (outputs moved, objectives merged, metrics replaced) with a one-line reason.

## OKRs
For each objective: `O1 (committed|aspirational): <objective>`, then a table: KR | Baseline | Target | Counter-metric.

## Initiatives
Bullets grouped by objective: the projects and deliverables that should move the key results.

## Measurement
One line per key result: data source, owner and how often it is checked.

## Open questions
Numbered, only those that block finalising the OKRs.
</output_format>
