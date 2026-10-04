---
name: case-study
description: Turns an existing internal script or tool into a buyer-facing case study and outreach message grounded in repository evidence. Use when someone says "/case-study", wants to turn internal work into portfolio proof, document an automation, extract a case study from a repository, or pitch an existing tool to prospective clients.
---

# Case Study

Turn one internal tool that already works into credible client-facing proof. Do not write or modify product code.

## Quick start

Run `/case-study [optional script, tool, or subdirectory]` from the project containing the work. The skill inspects the project, asks one compact batch of questions for facts it cannot recover, then writes a case study and outreach message.

## Evidence rules

- Label every claim as **observed**, **implemented**, **documented**, or **user-supplied** in the evidence notes. A README claim is documented; source code is implemented; neither is an observed outcome.
- Treat estimates as estimates and preserve ranges instead of manufacturing precision.
- Exclude secrets, personal data, private client identifiers, and proprietary details unless the user explicitly approves them.
- Write for the buyer, not a code reviewer: outcomes and avoided costs before implementation details.
- Do not overwrite an unrelated existing case-study file.

## Workflow

Inspect first and complete the workflow automatically. Ask only for facts that available files and user context cannot establish, grouped into one compact question set.

### 1. Name the problem, not the tool

Inspect the README, entry points, tests, examples, documentation, and relevant git history. Identify the real user, single input, useful output or decision, and manual or fragile process the tool replaced.

Write one sentence in the affected person's language. A non-programmer with the same problem should recognize their bad day.

If several tools are present, select the one with the strongest evidence of real use. Ask the user to choose only when candidates are genuinely tied.

### 2. Quantify before and after

Collect comparable measures of time, error rate, volume, cost, or risk using this provenance order:
1. **Observed:** behavior or measurements exercised during this run, or captured in an existing benchmark or output.
2. **Implemented:** behavior directly supported by source code or tests but not exercised during this run.
3. **Documented:** claims in READMEs, logs, tickets, or git history.
4. **User-supplied:** confirmed values or explicitly labeled estimates.

Do not run untrusted code merely to create proof. If no honest comparison exists, use a concrete qualitative outcome instead of fake precision.

### 3. Extract the judgment calls

Find two or three decisions a naive implementation would get wrong: validation, matching, deduplication, exception handling, safety limits, fallbacks, or refusal paths.

For each, explain what the tool does, why the obvious approach fails, and what user cost or failure the decision prevents. If none exists, explain that the tool is a receipt rather than a strong case study and offer to inspect another tool.

### 4. Generalize the archetype

Strip away company and domain-specific nouns. Name the broader problem pattern and buyer role that repeatedly encounters it.

Use only prospects the user names or evidence supports. If none are available, leave a visible prompt for three real prospects rather than fabricating them.

### 5. Produce the deliverable

Write `CASE-STUDY.md`. If that path contains unrelated work, write `CASE-STUDY-[tool-slug].md` instead and report the chosen path.

Use this structure:

```markdown
# [Outcome-focused title]

## The problem
[The buyer's bad day.]

## Before and after
[Comparable evidence, with estimates labeled.]

## What I built
[One plain-language sentence.]

## Judgment calls
- **[Decision]:** [Why it mattered and what it prevented.]

## Who else has this problem
[Problem archetype, buyer role, and user-confirmed prospects.]

## Outreach message
> I built a tool that took [before] down to [after] for [problem], and designed it to [judgment call] so [costly failure] does not happen. You're dealing with [archetype]. Worth 15 minutes?

## Evidence notes
- **[Observed | Implemented | Documented | User-supplied]:** [claim] — [source]
```

Keep provenance labels in the evidence notes. In the buyer-facing sections, use only natural qualifiers required for honesty, such as “estimated”; do not make the outreach message read like an audit report.

Keep the client-facing sections near 200 words, excluding evidence notes. Replace placeholders with supported facts; leave missing facts visibly bracketed.

Finish by reporting the output path, showing the outreach message, and naming the one unresolved fact that would most strengthen it. Do not send or publish anything without an explicit request.
