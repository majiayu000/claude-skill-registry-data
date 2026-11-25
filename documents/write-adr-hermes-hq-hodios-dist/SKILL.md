---
name: write-adr
description: Writes an architecture decision record that states one decision, the forces behind it, the options weighed and the honest consequences. Use when a significant technical choice is made or proposed.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: architecture
  source: https://hermes-ide.com/prompts/write-adr
  catalog: 2026.1014.1
---

# Write an architecture decision record

## Inputs

- [DECISION] (required): The decision taken or proposed, or the question to decide, in a sentence or two.
- [CONTEXT] (optional): Notes, constraints, discussion excerpts, links or numbers behind the decision.
- [OPTIONS] (optional): Options that were considered. Leave empty to draw them from the context.
- [STATUS] (optional; one of: proposed, accepted, superseded; default: proposed): Status to record in the ADR.
- [TEMPLATE] (optional; one of: madr, nygard; default: madr): Layout to use when the project has no existing ADRs to copy.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
An architecture decision record (ADR) captures one architecturally significant decision so that someone joining the team in two years can see what was decided, why, and what it cost. Its value is honesty about the forces and the consequences. An ADR that lists only upsides, or quotes a benchmark nobody ran, is worse than no ADR, because readers trust it.
</context>

<task>
Write an ADR for this decision: [DECISION]
Only if [CONTEXT] was provided: 
Context and constraints:
[CONTEXT]
Only if [OPTIONS] was provided: 
Options considered:
[OPTIONS]

1. If you can read the repository, look for existing ADRs (for example `docs/adr/`, `doc/adr/`, `docs/decisions/`, `adr/`). If you find any, copy their layout, numbering and tone, and use the next free number. Otherwise use the [TEMPLATE] layout in the output format below.
2. Extract the decision drivers: the requirements, constraints and quality attributes that actually push the choice (for example latency, cost, team skills, deadline, compliance, existing systems). Use only drivers present in the input or the code.
3. List the options. Include "keep the current approach" when it is a real option. For each option, give pros and cons measured against the drivers, not generic ones.
4. State the decision in one active sentence ("We will …") and say why it wins on the drivers.
5. Write the consequences: what becomes easier, what becomes harder, new risks, follow-up work, and the signal that should make the team revisit this decision.
6. Record the status as [STATUS]. If the input does not support a decision yet, record it as proposed and list what is missing under Open questions.
</task>

<constraints>
- One decision per ADR. If the input bundles several, write the main one and list the others under Open questions as candidates for their own ADRs.
- Never invent facts: no made-up benchmarks, prices, dates, names, quotes or product limits. Where a number would matter and none was given, write `TODO: measure …` with what to measure.
- Every option, including the chosen one, gets at least one real downside.
- Keep it readable in five minutes: about 300 to 800 words.
- Plain language. Define any acronym a new team member might not know.
- Separate what you verified from what you inferred. Mark inferences as such.
- When you do not know, say "I don't know" once and state what would settle it.
</constraints>

<output_format>
First line: the suggested file name, `NNNN-short-kebab-title.md`, using the next number when you know it and `NNNN` when you do not.
Then the ADR in Markdown.

madr layout:
# [Short title of the decision]
- Status: [status] · Date: [today if known, else TODO] · Deciders: [names given, else TODO]
## Context and problem statement
## Decision drivers
## Considered options
## Decision outcome
The chosen option and why, then a "Consequences" list of good, bad and neutral bullets.
## Pros and cons of the options
One subsection per option.
## Open questions
Omit when there are none.

nygard layout:
# [N]. [Title]
Date line, then `## Status`, `## Context`, `## Decision`, `## Consequences`, and `## Open questions` only when needed.
</output_format>
