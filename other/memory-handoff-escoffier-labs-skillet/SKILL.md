---
name: memory-handoff
version: 0.1.1
license: MIT
description: Use at the end of any session that discovered durable knowledge (architecture decisions, root causes, setup gotchas, workflow changes, security findings, reusable patterns), or when the user says "hand off", "write a handoff", or "save this for the memory system".
---

# memory-handoff

Coding sessions die with their transcripts. A memory handoff is a short structured note that a memory owner (a long-lived agent, a teammate, or future you) can review and file into durable memory. This skill pairs with [brigade](https://github.com/escoffier-labs/brigade), which lints and ingests handoffs, but works standalone.

In a Brigade-wired repo the handoff is the closing gate of the [Brigade process model](../../../docs/brigade-process-model.md). This skill owns the handoff itself: format, quality bar, routing sections, and lint.

## When a handoff is warranted

Durable knowledge only: architecture decisions, non-obvious root causes, environment gotchas, workflow changes, security findings, reusable commands or patterns, user preferences, research findings. Not task chatter, not anything the repo already records (code, git history, existing docs).

## Where to write it

1. If the repo has a brigade inbox (check `.brigade/` config) or an existing handoff dir (`.claude/memory-handoffs/`, `.codex/memory-handoffs/`), write there.
2. Otherwise create `.claude/memory-handoffs/` and write there.

Filename: `YYYY-MM-DD-HHMM-<slug>.md`

## Format

```md
# Memory Handoff

## Type
setup | workflow | bugfix | decision | security | preference | research | project-context

## Title
Short, specific title

## Summary
2 to 4 sentences. What happened and why it matters.

## Durable facts
- Fact 1
- Fact 2

## Evidence
- files changed: ...
- commands run: ...
- error strings: ...

## Recommended memory action
create-card | update-card | no-card

## Target card
descriptive-card-name.md

## Suggested card content
(the exact card to save; MUST start with YAML frontmatter)
```

`brigade handoff lint` requires the routing sections: `Recommended memory action` is mandatory, and for `create-card`/`update-card` the suggested card content must begin with YAML frontmatter. For `no-card`, replace the card sections with `## Target document` and `## Suggested document content` instead. When unsure of the destination system's exact expectations, scaffold with `brigade handoff draft` and fill it in.

## Quality bar

- Durable, not session fluff. If it will not matter in a month, do not write it.
- Specific and verifiable. Exact paths, exact commands, exact error strings.
- Under 400 words. The reviewer should route it without rethinking the session.
- One handoff per distinct piece of knowledge. Two unrelated discoveries are two files.
- Convert relative dates ("yesterday", "last week") to absolute dates.

## Verify

If the brigade CLI is installed, run `brigade handoff lint` on the repo and fix what it flags. If not, re-read the handoff asking: could someone who was not in this session act on this?

## Common mistakes

- Writing a session narrative instead of extracted facts. The reviewer needs the knowledge, not the story.
- Skipping the handoff because the session "was mostly debugging". Root causes are the single most valuable handoff type.
- Editing the memory owner's canonical files directly instead of handing off. The handoff flow exists so a reviewer can veto.
