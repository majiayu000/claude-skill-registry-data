---
name: mathodology-agent-pipeline
description: Use when planning a modeling solution, selecting the next useful step or briefing a specialist.
---

# Mathodology Modeling Prompts

Use the following questions in whatever order the task needs. They are prompts
for reasoning, not mandatory stages or files.

## Understand the problem

What decision is the reader trying to make? What is given, unknown or required?
Which mechanisms must the solution represent? Check the actual contest rules
when applicable, including deadline, page limits and AI-use requirements.

## Formulate a model

Start with a useful baseline. Define variables, units, assumptions, constraints
and the objective. Compare plausible alternatives when there is a real choice;
do not invent extra models to meet a quota. Explain why the added complexity
changes the answer. Check identifiability, data requirements and limiting cases.

## Challenge the result

Which observation could disprove the model? Can a simpler baseline perform as
well? Test influential assumptions and plausible adverse scenarios. Separate
parameter uncertainty, observation noise and structural uncertainty. Match the
paper's claims to the implemented mathematics and the data actually used.

## Communicate the answer

Answer the problem's questions with interpretable quantities and limitations.
Choose figures from [figure presets](../mathodology-figure-presets/SKILL.md),
including the once-per-task image2 question. Build the explanation around the
results, not the history of experiments. Review with
[review questions](../mathodology-award-gates/SKILL.md).

## Focused collaboration

When delegation is useful and available, give a specialist a bounded question,
relevant data, current assumptions and a concrete output. Agree file ownership
for concurrent editing. Ask for ordinary prose: finding, reasoning, artifact
paths and unresolved uncertainty. The lead integrates the answer and resolves
conflicting evidence; it does not collect points or gate every intermediate step.

For a fresh task, a compact prompt is:

> Solve the supplied modeling problem. State assumptions, build and test a
> useful baseline, add justified complexity, and connect each recommendation to
> evidence. Adapt the workflow to the available time. Select purposeful figures
> using mathodology-figure-presets and ask once about image2 availability.
> Keep calculations reproducible and explain what could change the conclusion.
