---
name: user-persona
description: Build a research-grounded user persona from interview notes, painpoint research, or survey results, then auto-generate the downstream copy artifacts (homepage headline, channel plan, cold outreach draft). Use when the user says "make me a persona for X," "build a user persona from these notes," "turn my research into a persona," or similar.
---

# User Persona

Turn raw user research into a structured persona document plus downstream copy artifacts in one pass.

## When to trigger this skill

The user wants any of:

- "Build a user persona for [target customer] from this research"
- "Turn these interview notes into a persona"
- "Make me a persona doc"
- "Persona for [audience]"

Do NOT trigger this skill when:

- The user has fewer than 5 interviews / data points (the result is just laundered guesses)
- The user wants a proto-persona before research (use `components/02-discovery/proto-persona.md` instead)
- The user wants competitive personas, not user personas

## Inputs you need

**Required:**
- The product or service being built (one line description)
- The raw research material: interview notes, survey results, painpoint quotes, transcripts

**Strongly recommended (ask if missing):**
- Target market / segment if there are multiple
- Brand voice the downstream copy should match
- One or two example real quotes from the research (if absent, this is probably too early for a persona)

## Workflow

### 1. Confirm the inputs

If the user has only given a target description with no research, stop and ask: "Do you have interview notes or painpoint research to ground this in? Personas built without research just launder assumptions."

If they have research, proceed.

### 2. Generate the persona

Read `template/persona.md` for the structure. Fill every section using only material that's grounded in the research. For each section:

- **Use direct quotes** from the research whenever possible.
- **Mark inferences as inferences.** If demographics are inferred from context, say so.
- **Rank painpoints by severity.** Use the frequency of mentions across the research as the proxy.

Save the populated persona to `~/user-personas/<slug>/persona.md`.

### 3. Generate downstream copy

Read `template/derived-copy.md`. Use the persona just generated as input. Fill the three sections:

1. **Homepage headline** — three alternative headlines tied to the persona's top painpoint
2. **Channel plan** — where the persona spends time online and how they'd actually discover this product
3. **Cold outreach draft** — a message the persona would plausibly reply to (not a generic template)

Save to `~/user-personas/<slug>/derived-copy.md`.

### 4. QA check

Before reporting done, verify:

- Every painpoint has either a direct quote or an explicit "inferred" label
- The day-in-life scenario references a specific time and trigger, not generic context
- The homepage headlines name the painpoint, not the feature
- The cold outreach reads as written to a person, not a segment

If any of these fail, regenerate the relevant section before delivering.

### 5. Present

Tell the user where the two files live and ask whether they want a third artifact: a feature priority list scored against the persona (nice-to-have vs must-have).

## Voice rules for the persona itself

- **Use the person's language, not yours.** If the research says "I just want it to stop breaking," the persona says "I just want it to stop breaking," not "I value reliability."
- **Sentence-case headers.**
- **No marketing puffery in the goals/motivations section.** "Wants to ship faster" beats "Strives for excellence in delivery."
- **Name the persona.** Sarah, not "the target user."
