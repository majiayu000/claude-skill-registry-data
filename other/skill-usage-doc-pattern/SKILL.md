---
name: skill-usage-doc-pattern
description: |
  Pattern for shipping a human-only USAGE.md alongside a complex Claude Code skill,
  so users learn how to invoke the skill optimally without polluting the model's
  context. Use when: (1) user asks "should I add example prompts to my skill?",
  (2) user asks where to put human-facing docs for a skill, (3) user wants to
  document optimal invocation phrasing for a complex skill they authored,
  (4) you've just refined a skill where invocation phrasing meaningfully shifts
  output quality and want to capture the invocation patterns. Covers the placement
  decision (skill root, NOT SKILL.md, NOT references/), the audience-separation
  rationale (SKILL.md is loaded into model context on every trigger; root files
  like USAGE.md are not auto-loaded), the canonical document shape (TL;DR template
  + scenarios + signals table + anti-patterns + what-not-to-say + pairing matrix),
  and the scoping rule (only do this for complex skills where invocation phrasing
  meaningfully changes output).
author: Claude Code
version: 1.0.0
date: 2026-05-02
---

# Skill USAGE.md pattern

## Problem

Complex Claude Code skills (the kind that orchestrate multi-step pipelines, query
external APIs, or produce structured artefacts) often have a hidden quality
ceiling: the model triggers correctly on the user's prompt, runs the pipeline,
and produces a valid output — but a *better-shaped* prompt would have produced a
markedly better output.

The model only learns trigger phrases from the YAML `description` field. That
field is keyword soup ("demand check for [entity], SERP recon for [keyword]…")
written for semantic matching, not for teaching humans how to invoke the skill
well. Users have no canonical place to learn:

- What optional context to include (entity scope, locale, existing-state hints)
- Anti-patterns that still trigger but produce mediocre output
- What they *don't* need to say (defaults the skill already handles)
- How the skill pairs with other skills

The naive solutions are all wrong:

- **Add it to SKILL.md** — every line is loaded into model context on every trigger. Pure waste.
- **Add it to `references/`** — the model may load files from `references/` if SKILL.md tells it to. Mixing human and model audiences in one folder makes the model accidentally read human-only docs.
- **Skip it** — leaves the invocation-quality ceiling unaddressed.

## Context / Trigger Conditions

Use this skill when:

1. User asks "should I add example prompts to my skill?" or "where do I document
   how to use my skill?"
2. User has just authored or refined a complex Claude Code skill and you notice
   that invocation phrasing meaningfully changes output quality
3. User wants to document invocation patterns for an existing skill so future-them
   (or teammates) invoke it optimally
4. You're advising on the architecture of a multi-skill workflow and need to
   capture how skills should be invoked and chained

**Skip this pattern when:** the skill is small enough that any reasonable trigger
produces equivalent output (e.g. `commit-me`, `semantic-html`). The maintenance
burden of a USAGE.md only earns its place when invocation phrasing has real
output-quality leverage.

## Solution

### 1. Place the file at the skill root, named `USAGE.md`

```
.claude/skills/{skill-name}/
├── SKILL.md              ← model-facing, auto-loaded on trigger
├── USAGE.md              ← HUMAN-ONLY, never auto-loaded
├── references/           ← model-facing if linked from SKILL.md
│   └── ...
└── evals/
    └── evals.json
```

**Why skill root, not `references/`:**
- `references/` is the conventional spot for model-facing supporting docs that
  SKILL.md tells the model to read. Putting human-only docs there muddies the
  audience and risks the model reading them.
- A file at skill root with the name `USAGE.md` (or `HOW-TO-INVOKE.md`) signals
  "human only" by convention. The Claude Code skill loader does not auto-read
  files at the skill root other than `SKILL.md`.

**Why not in `SKILL.md`:**
- SKILL.md is loaded into the model's context every time the skill triggers.
  Every byte of human-only content is wasted tokens on every invocation, forever.

### 2. Use this canonical structure

````markdown
# How to invoke `{skill-name}` for best results

> **Audience:** {user name} (the human). The model does not read this file.

## TL;DR — the canonical prompt shape

```
{trigger phrase} for {primary input}.
{optional: signal 1}
{optional: signal 2}
```

## {3–5} common scenarios

### 1. {Scenario name (most common case)}

```
{concrete prompt example}
```

Use when: {one-line condition}

### 2. {Highest-leverage signal scenario}

```
{concrete prompt example}
```

Use when: {condition}. {One sentence on why this scenario unlocks the most output quality.}

(continue for 3–5 scenarios)

## Signals that improve the output (when relevant)

| Signal | What to add | Why it helps |
|---|---|---|
| {signal 1} | `{phrasing}` | {what it unlocks in the skill} |
| {signal 2} | `{phrasing}` | {what it unlocks} |

## Anti-patterns (these still trigger the skill but produce mediocre output)

| Don't say | Say instead | Why |
|---|---|---|
| `{vague prompt}` | `{better prompt}` | {why the better one wins} |
| `{over-specified prompt}` | `{leaner prompt}` | {what's redundant} |

## What you don't need to say

The skill already does these by default:

- {default behavior 1}
- {default behavior 2}

## Pairing with other skills

| You're doing | Run this first | Then |
|---|---|---|
| {workflow 1} | `{this skill}` | `{next skill}` |

## When to *not* run this skill

- {boundary condition 1}
- {boundary condition 2}
````

### 3. Apply the scoping rule

Only ship `USAGE.md` for skills where invocation phrasing meaningfully shifts
output quality. Symptoms that earn it:

- The skill takes optional context that materially changes the output (locale,
  scope, existing-state, downstream consumer)
- The skill has multiple distinct verdict tiers or output shapes the user can
  influence
- The skill chains with other skills in non-obvious ways
- The skill has anti-patterns that trigger correctly but produce weak output

Symptoms that do **not** earn it:

- The skill does the same thing regardless of how you phrase the trigger
- The skill is a single-shot transform (e.g. "format this code", "extract this
  data")
- The skill is so simple that the description field already covers everything

### 4. Discover the signals empirically

Don't write USAGE.md from imagination. Sit with the skill's SKILL.md and
`evals/evals.json` first, and ask: for each canonical eval prompt, what optional
signal would have produced an even better output? Those signals are the ones
that earn a row in the "Signals that improve the output" table.

## Verification

To verify the USAGE.md doesn't accidentally get loaded into model context:

1. Trigger the skill with a normal prompt
2. Check the model's context — `USAGE.md` should not appear
3. Check that `SKILL.md` does NOT contain `read_file` calls referencing `USAGE.md`
4. Check that the `references/` directory (if any) does NOT contain a copy of
   `USAGE.md`

To verify the USAGE.md actually helps users:

1. Pick the skill's lowest-quality recent invocation
2. Reframe the prompt using the USAGE.md template
3. Compare output quality

## Example

For the R3 `entity-demand-check` skill, the USAGE.md surfaced one
high-leverage signal that was not obvious from SKILL.md: mentioning the
existing R3 URL up front (`we already have /nas-data-recovery but I think
it's slipped`) triggers a specific verdict tier in the skill (page-revival
case) that recommends refreshing the existing URL instead of building a
parallel page. Without that signal, the user might invoke the skill
generically and get a "GO — build a new page" verdict that overlooks the
existing URL entirely.

That is exactly the kind of leverage USAGE.md is for: the skill *can* do the
right thing, but only if the user knows which signal unlocks it.

See `/Users/atilaalacan/CODE/R3/r3comv2/.claude/skills/entity-demand-check/USAGE.md`
for a full worked example.

## Notes

- The pattern intentionally does not use frontmatter on USAGE.md — it's not a
  skill, it's documentation. Keep it as plain markdown.
- If you want a single index across all skills, create a separate
  `docs/skills-cheatsheet.md` at the project root that links to each skill's
  USAGE.md. Don't try to centralise the per-skill content.
- This pattern is orthogonal to evals. `evals/evals.json` captures *correctness*
  of the skill's behaviour; USAGE.md captures *invocation craft* for the human.
- For projects with multiple authors, the audience line at the top can be
  generalised to "the team" rather than naming a specific person.

## References

- Claude Code Skills documentation (skill structure, references/ folder, SKILL.md
  loading behaviour)
- Worked example: `/Users/atilaalacan/CODE/R3/r3comv2/.claude/skills/entity-demand-check/USAGE.md`
