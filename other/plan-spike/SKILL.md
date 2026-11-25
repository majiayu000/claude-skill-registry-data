---
name: plan-spike
description: Turns a technical unknown into a time-boxed spike with a sharp question, exit criteria, cheapest-first experiments and a clear deliverable. Use when an unknown blocks a decision or an estimate.
license: CC0-1.0
metadata:
  version: 1.0.1
  kind: prompt
  category: planning
  source: https://hermes-ide.com/prompts/plan-spike
  catalog: 2026.1014.1
---

# Plan a spike

## Inputs

- [QUESTION] (required): The unknown that blocks progress, in your own words.
- [TIMEBOX] (optional; default: 2 days): Maximum time the spike may take.
- [CONTEXT] (optional): The decision or work this unblocks, what is already known, and any constraints.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
A spike is a short, time-boxed investigation that buys information, not features. Spikes go wrong when the question is vague ("look into Kafka"), when nobody defines what "done" means, or when the prototype quietly becomes production code. A good spike plan fixes all three before the clock starts.
</context>

<task>
Plan a spike for: [QUESTION]
Only if [CONTEXT] was provided: 
Context:
[CONTEXT]
Time box: [TIMEBOX].

1. Rewrite the unknown as one or two answerable questions, each with a yes or no, a number, or a choice between named options as its answer.
2. Name the decision or estimate the answer unblocks, and who makes it.
3. Define exit criteria: the evidence that answers each question, and what result would mean "go", "no go" or "need more data".
4. List the experiments, cheapest and most informative first (reading docs and code, asking someone, a throwaway prototype, a measurement). Give each a share of the time box and what it should show.
5. Add a checkpoint at about half the time box to decide whether to continue, narrow the question or stop.
6. Define the deliverable: a short findings note with the answer, the evidence, the recommendation and what remains unknown.
</task>

<constraints>
- Fit the whole plan inside [TIMEBOX]. If it cannot be answered in that time, say so and narrow the question instead of stretching the box.
- Prototype code is throwaway by default. Say so in the plan, and list anything that must be rebuilt properly if the answer is "go".
- Do not pre-decide the answer or bias the experiments toward one outcome.
- Do not state facts about tools or products you are unsure of; turn them into things the spike checks.
</constraints>

<output_format>
## Question
The sharpened questions, numbered.
## Decision it unblocks
One or two lines.
## Exit criteria
Bullets: go, no go, need more data.
## Plan
Numbered experiments with time share and expected evidence, plus the checkpoint.
## Deliverable
What the findings note contains.
## Out of scope
Bullets.
</output_format>
