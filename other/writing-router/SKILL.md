---
name: writing-router
description: Route writing requests to the correct installed workflow. Use when a request could mean natural prose, technical documentation, repository agent instructions, or a post-draft style audit. Do not use when the user already named plain-english, simple-english, style-review, or writing-great-agents-md.
---

# Writing Router

Choose one primary writing workflow. Do not stack rule sets that optimize for different readers.

For repository instructions under Oh My Pi, the native locations are `.omp/AGENTS.md` and `.omp/RULES.md`; `writing-great-agents-md` documents their loading rules.

## Route

| Request | Load and follow |
|---|---|
| README, runbook, procedure, API guide, error message, incident report, release note, localization-ready text | `skill://simple-english` |
| Essay, blog post, email, product explanation, announcement, or other voice-led nonfiction | `skill://plain-english` |
| `AGENTS.md`, `CLAUDE.md`, `.omp/AGENTS.md`, `.omp/RULES.md`, or repository instructions | `skill://writing-great-agents-md` |
| Audit, score, compare, or polish an existing technical Markdown file | `skill://style-review` |

If the document mixes technical instructions with narrative prose, apply each workflow only to its matching section. Never run Plain English and Simplified Technical English over the same passage.

## Documentation Gate

Before drafting technical documentation:

1. Name the intended reader and the task that the document must help them complete.
2. Inspect the source of truth. Do not infer commands, behavior, defaults, metrics, or compatibility from style guidance.
3. Verify commands, paths, examples, links, and factual claims with the available project tools.
4. Draft with Simple English in pragmatic mode unless the user explicitly requests strict STE.
5. Use Style Review only as a final quality pass. A style score does not prove technical correctness.

The goal is clear, trustworthy prose. Do not promise that text can evade an AI detector.

## Loading in Oh My Pi

Relative paths in this skill (`references/…`, `scripts/…`) resolve against the skill's own directory. Read them with `skill://writing-router/<relative-path>`. When a shell command needs a real filesystem path, that directory is `<OMP_HOME>/skills/writing-router/` — `~/.omp/agent/skills/writing-router/` by default. Invoking `/skill:writing-router` also prints the resolved location.
