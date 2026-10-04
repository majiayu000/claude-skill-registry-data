---
name: public-skill-launcher
description: Package an AI skill, prompt workflow, or internal operating habit into a public-ready release with a catchy hook, safe redaction, useful examples, demo tasks, README copy, and launch messaging. Use when preparing a skill for GitHub, social sharing, marketplace submission, documentation, or community feedback.
---

# Public Skill Launcher

Turn a useful internal skill into something a stranger can understand, try in 60 seconds, and want to share - without leaking how it really works inside.

The goal is not to publish everything. The goal is to ship the smallest delightful version that proves usefulness, and hold the rest back.

## Public Core Rule

Ship the useful public core. It should be genuinely helpful on its own - a real win the user can feel today. Keep the internal edge out of the public package:

- deep heuristics and the exact decision thresholds,
- tuned parameters, prompt internals, scoring weights,
- proprietary data, private benchmarks, client specifics,
- the parts that took the most work to get right.

Done well, the public skill is good enough that people adopt it and say "this is useful" while the sensitive depth stays private. A public skill can and should be smaller than the internal one. If the useful part cannot survive without private details, build a toy version or do not publish.

## Launch Shape

Produce a package with these pieces:

```text
name:
one_line_hook:
who_it_helps:
pain_it_solves:
what_it_does:
quick_start:
example_prompts:
demo_task:
safety_notes:
what_is_not_included:
launch_post:
```

Keep every piece concrete. A popular skill makes a user think "I can use this today," not "interesting architecture."

## Workflow

### 1. Find the public core

Split the idea into three layers:

- Public: the generic workflow, the user benefit, safe examples. (ship)
- Semi-private: implementation style, internal naming, detailed heuristics. (trim or generalize)
- Private: protected mechanisms, internal data, credentials, client details, unpublished IP. (never)

Ship the public layer. Generalize the semi-private. Drop the private.

### 2. Name it for recall

Prefer names that are short, action-oriented, easy to say, and specific enough to remember.

Good patterns:
- `bug-repro-packager`
- `readme-rescue`
- `demo-script-maker`
- `release-note-polisher`
- `prompt-to-checklist`

Avoid names that depend on private project lore, internal codes, or anything only an insider would recognize.

### 3. Write the hook

```text
For [audience] who struggle with [pain], this skill [action] so they can [visible outcome].
```

- "For indie hackers shipping fast, this skill turns messy change notes into a clean launch post."
- "For AI coding agents, this skill packages a bug report into a reproduction-ready checklist."

One sentence. If it needs two, the scope is too wide - narrow it.

### 4. Make the demo tiny

A public skill needs a 60-second demo that:

- uses fake or harmless inputs,
- produces a visible artifact,
- shows a clear before -> after,
- ends with a copyable result,
- touches no private file.

If the demo needs setup, make a smaller demo.

### 5. Add examples

3 to 5 example prompts, practical not abstract:

```text
Use $skill-name to turn this git log into release notes.
Use $skill-name on this stack trace to make a repro checklist.
Use $skill-name to rewrite this README intro for newcomers.
```

### 6. Scrub for safety

Before publishing, scan the package and remove or replace:

- credentials, API keys, tokens, URLs to private services,
- personal names, client names, internal team references,
- internal/absolute file paths,
- unpublished IP, private metrics, internal datasets, project codes,
- any instruction that reveals a protected method.

Replace each with a toy example or a generic placeholder. Publishing is irreversible - once it is out, it can be cached, forked, and indexed even after deletion. When in doubt, leave it out.

### 7. Write the launch post

```text
I made [skill].

It helps [audience] do [job] without [pain].

Try it when you need to:
- [use case 1]
- [use case 2]
- [use case 3]

Example:
[short input -> short output]

Link:
```

Useful and light. Do not oversell.

## Worked Example

Internal skill: a release-note generator with tuned commit-classification heuristics and team-specific tone rules.

Public version:

```text
name: release-note-polisher
one_line_hook: For makers who ship often, this turns a messy git log into a clean, readable release note.
who_it_helps: Solo devs and small teams who dread writing changelogs.
pain_it_solves: Raw commit logs are noisy; hand-writing notes is slow and easy to skip.
what_it_does: Groups commits into Added / Fixed / Changed, drops noise, writes plain-language bullets.
quick_start: Use $release-note-polisher on your last 20 commits.
example_prompts:
  - Use $release-note-polisher to turn this git log into v1.2 notes.
  - Use $release-note-polisher to summarize this week's merges for a blog post.
demo_task: Paste a 15-line fake git log -> get a 3-section release note.
safety_notes: Uses only the commit text you paste; no repo access, no private data.
what_is_not_included: The internal commit-importance scoring and team tone presets are not part of this public version.
launch_post: |
  I made release-note-polisher.
  It turns a messy git log into a clean release note in seconds.
  Try it when you need to: ship notes fast, summarize a sprint, write a changelog you actually like.
  Example: 15 noisy commits -> Added / Fixed / Changed, in plain English.
```

The `what_is_not_included` line is doing real work: it is honest, sets the public boundary, and signals that private tuning is not part of the release.

## README Copy Template

````markdown
# Skill Name

One sentence hook.

## What It Does

- Benefit 1
- Benefit 2
- Benefit 3

## Quick Start

```text
Use $skill-name to ...
```

## Example

Input:
```text
...
```

Output:
```text
...
```

## Not Included

This public version uses generic examples and intentionally leaves out the deeper tuning, private data, and protected internals.
````

## Taste Rules

- Lead with usefulness, not architecture.
- Show one real-feeling example before any theory.
- Keep the first screen short.
- Prefer verbs over grand names.
- Name what is excluded - honesty about the boundary builds trust, not suspicion.
- Do not publish internal logs as proof; publish sanitized examples.

## Release Decision

```text
GO:   useful with toy examples and no protected detail.
TRIM: useful, but private details still need removing or generalizing.
HOLD: value depends on private depth or on unpublished evidence.
NO:   contains secrets, client data, credentials, or core IP.
```

When uncertain, choose TRIM or HOLD. Publishing cannot be undone.
