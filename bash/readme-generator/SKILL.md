---
name: readme-generator
category: developer-experience
description: >
  Write, overhaul, or review a project README that is accurate to the repository and
  readable by a human. Use when the user says "write a README", "improve my README", "my
  README is out of date", "review my README", or a project needs its front page.
codex-short-description: "Write, overhaul, or review a README that is accurate to the repo and readable by humans"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
related-skills:
  - writing-humanize
loop-eligible: false
compatibility: claude-code codex opencode
---

# README Generator

You are a Developer Experience advocate writing the front page of a repository. A README has
one job: turn a stranger into someone running the project. Two rules govern every decision.

**Repo truth.** Every command, flag, env var, path, and version comes from a file you read or
a command you ran. When the repository cannot answer something, write
`<!-- TODO: confirm … -->` and surface it to the user. Inventing a plausible install step is
the one failure this skill exists to prevent.

**The 30-second test.** A stranger on the first screen learns *what* it is, *why* they'd want
it, and *how* to run it. Everything else lives below that.

## Workflow

### 1. Scan the repository

Read before writing: manifests and lockfiles, entry points, `scripts`/task definitions, tests,
CI workflows, config schemas and `.env.example`, the license file, and any existing README or
`docs/`. Run `--help` on CLI entry points and capture the real output. Reach for the web only
to confirm framework conventions the repo genuinely cannot settle.

**Done when** you can state without guessing: what the project does, its prerequisites *with
versions*, the exact install command, the exact run command, and every required config key.
Whatever is still unknown becomes a TODO you carry forward.

### 2. Fix the shape

Name the project type — library, CLI, application/service, or internal repo — and the primary
reader. Ask the user only when the repo is genuinely ambiguous. Read
[STRUCTURE.md](STRUCTURE.md) for the section ladder and how it bends per type.

### 3. Draft

Work down the ladder. Lead with the one-liner and the why; put a copy-pasteable quick start
above the fold; render configuration as a table; keep prose blocks short. Every code block
carries a language tag and contains a command you verified in step 1.

**Done when** every Required and Recommended section is present or has a stated reason for
being dropped.

### 4. Review

Score the draft against [REVIEW.md](REVIEW.md) and fix every failure. Gate 1 (Truth) failures
block delivery outright. When the user asked for a *review* of an existing README rather than
a rewrite, this rubric and its reporting format are the whole deliverable.

### 5. Humanize

Run the draft through the `writing-humanize` skill before it ships. A README is the first
thing a human reads, and a scanning draft carries AI cadence the rubric alone will not catch —
uniform sentence rhythm, triads, hedged claims, section openers that restate the heading.
Preserve every command, flag, version, and code block verbatim through this pass; the prose
around them is what changes.

**Done when** the draft reads as though a maintainer wrote it, and step 1's verified facts
survived intact.

### 6. Deliver

Write `README.md`, then tell the user: the sections you produced, every `TODO` marker and what
it needs, and any claim you deliberately left out for lack of evidence. Stage, commit, or push
only on an explicit instruction.

## Quality Loop

1. Draft per step 3.
2. Self-evaluate against the four gates in [REVIEW.md](REVIEW.md).
3. If any gate fails, fix and re-score.
4. Exit when all gates pass, or after two iterations — then report the remaining failures
   rather than hiding them.

## Delegation Map

| User need | Delegate via |
| :--- | :--- |
| Standard pre-ship prose pass | Invoke `writing-humanize` on the draft — step 5, always |

**Loop eligibility:** false — a README is written when the project changes, not on a schedule.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/readme-generator.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
