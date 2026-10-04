---
name: tree-ring-memory
description: Use when an AI agent needs local-first project memory recall, evidence-linked lessons, privacy-safe capture, audit, redaction, or intentional forgetting.
---

# Tree Ring Memory

## Overview

Use this skill to operate Tree Ring Memory as a lifecycle-aware memory layer for
AI agent work. Tree Ring Memory is for durable decisions, lessons, warnings,
project conventions, user preferences, and future seeds. It is not a transcript
dump or a background scraper.

The core idea is that agent memory should age deliberately:

- fresh work can stay detailed while it is still active
- older lessons should compress into stable summaries
- important failures and warnings should remain visible
- durable preferences and project truths should become high-confidence memory
- speculative follow-ups should stay separate from confirmed facts
- sensitive data should be blocked, redacted, or forgotten

## When to Use

Use this skill when:

- The user asks the agent to remember, recall, consolidate, redact, or forget.
- A task depends on previous project decisions, preferences, or warnings.
- The agent is starting or resuming work in a repository with Tree Ring Memory
  or a project-local `.tree-ring` directory.
- A test, incident, PR, benchmark, or review produces a lesson that should help
  future work.
- A source document such as `AGENTS.md`, DOX, or Revolve contains durable
  guidance that should be summarized into memory.
- The agent needs to audit stored memory before a risky change.

## Do not use

Do not use this skill as the primary guide for:

- Short-lived scratch notes that should disappear after the task.
- Raw chain of thought or hidden reasoning.
- Secrets, credentials, tokens, private keys, payment details, or other
  sensitive values.
- Saving entire conversations instead of concise lessons or decisions.
- Treating unverified claims as durable project truth.
- Replacing source documents, tests, issues, PRs, or release records.

## Instructions

Follow the workflow below whenever Tree Ring Memory could improve continuity.
For small tasks, recall narrowly and only write memory when the lesson is
clearly durable. For higher-risk work, include source checks, evidence-linked
capture, and a closeout review.

## Workflow

1. Recall before acting when prior context could affect the task.
2. Prefer narrow project-scoped queries over broad global recall.
3. Read source documents directly when they exist; memory does not replace
   `AGENTS.md`, project docs, tests, issues, PRs, or release records.
4. Store only concise lessons, decisions, warnings, and preferences that will
   materially improve future work.
5. Use evidence-linked capture when a lesson comes from a reviewed run,
   evaluation, checkpoint, incident, branch, PR, issue, or test artifact.
6. Redact, supersede, or delete stale or sensitive memory instead of preserving
   known-wrong context.

## Command Reference

Start with local help so commands match the installed version:

```bash
tree-ring --help
tree-ring evidence --help
tree-ring dox sync --help
tree-ring revolve sync --help
```

If the project has a local Tree Ring setup, read `.tree-ring/SKILL.md` and
`.tree-ring/CLI.md` before assuming a global configuration. If a command needs
the project store explicitly, include the local root:

```bash
tree-ring --root .tree-ring recall --query "release decisions"
tree-ring --root .tree-ring evidence --help
```

Run source adapters in dry-run mode before writing imported summaries:

```bash
tree-ring dox sync --source-root . --dry-run
tree-ring revolve sync --source-root revolve --dry-run
tree-ring integrations scan --source-root .
```

Only write summaries that are concise, useful, source-linked, and privacy-safe.

## Ring Model

Use the ring metaphor to decide retention strength:

- `cambium`: active task context
- `outer`: recent decisions and lessons
- `inner`: older compressed project knowledge
- `heartwood`: durable high-confidence truths and preferences
- `scar`: important failures, regressions, rejected approaches, and warnings
- `seed`: unresolved ideas, hypotheses, and follow-ups

Do not promote weak evidence into `heartwood`. Use `outer` or `seed` until the
user confirms durability or the evidence is strong.

## Privacy Guardrails

Never store:

- secrets, credentials, tokens, private keys, or payment details
- raw chain of thought
- temporary scratchpad notes
- unverified claims as durable truth
- sensitive health, financial, legal, or personal identifier details without
  explicit user instruction
- copyrighted source text beyond short allowed excerpts

When useful memory contains sensitive material, keep only a redacted operational
summary with enough context to avoid repeating the same mistake.

## Closeout Checklist

Before ending meaningful work, ask:

- What did we decide?
- What did we learn?
- What should future agents avoid repeating?
- Did the user state a durable preference?
- Is there a future seed worth revisiting?
- Is any memory wrong, stale, private, or better left unstored?

Only remember answers that are durable, useful, source-grounded, and safe.
