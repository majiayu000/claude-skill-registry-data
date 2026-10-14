---
name: absorb
description: >
  Analyze one or more external projects (git URL or local path) to extract
  AI-harness practices, agent patterns, or instruction logic and contrast them
  against this repository's harness. Not for application code review.
license: MIT
metadata:
  author: abdi
  adapted_by: andresnator
  source: user-provided absorb draft
  version: "1.2.4"
  status: testing
---

# Absorb

## Activation Contract

Use this skill when the user wants to inspect an external repository or local project to learn from its AI-harness setup: agents, skills, prompts, orchestration rules, or instruction patterns.

Do not use it for application code review, bug hunting, architecture review of the product itself, or test-quality audits.

## Required Input

- One or more targets: git URL(s) and/or local path(s).
- Optional focus: skills, agents, prompts, workflows, installer patterns, or comparison themes.

If no valid target is provided, ask for it before continuing.

## Hard Rules

- Analyze harness and agent configuration, not the external project's business code quality.
- Verify practices from source files, activation points, or wiring; do not promote README claims as proven behavior.
- Contrast every candidate practice against this repository before recommending adoption.
- Prefer repo-native context for the contrast step: `AGENTS.md`, `.ai/atl/skill-registry.md`, `domains/*/README.md`, `domains/*/skills/*/SKILL.md`, `skills/*/SKILL.md`, and relevant local artifacts.
- When available, delegate read-heavy discovery to subagents or researcher passes instead of relying on memory.
- Never auto-adopt, auto-commit, or silently edit this repository as a result of the audit.

## Workflow

### 1. Scope and resolve targets

For each target:

- If it is a local path, verify it exists.
- If it is a git URL, clone or update it only with user awareness and to a clearly stated local destination.
- Confirm the resolved target list before deep analysis.

### 2. Map each external harness

For each resolved target, extract:

- AI entrypoints such as `AGENTS.md`, `CLAUDE.md`, command folders, agent folders, skill folders, config files, prompt files, and AI-related plugins.
- A repo counts as a valid harness even without `AGENTS.md`, `agents/`, or `skills/` trees: its AI surface may live primarily in plugins, runtime config handlers, and maintenance scripts.
- How each candidate practice is triggered or wired.
- Which practices are verified versus aspirational.

For every candidate practice, capture:

| Field | What to record |
| --- | --- |
| Practice | Clear name |
| Mechanism | File path and concrete evidence |
| Status | Verified / partial / aspirational |
| Strength | Why it helps |
| Weakness | Limitation or trade-off |

### 3. Contrast with this repository

For each candidate practice:

- Check whether this repository already has an equivalent or better approach.
- Mark `no adoption needed` when the current harness already covers the need well.
- Carry forward only genuinely better or meaningfully missing practices.

Also record at least three **Our Advantages** points to avoid cargo-cult adoption.

### 4. Adversarial filter

Challenge each surviving practice:

- Is it truly verified?
- Is it better, or just different?
- Does it fit this repo's OpenCode-only, compact, contract-focused conventions?
- Is the adoption cost proportional to the benefit?

Keep only `ADOPT` or `CONDITIONAL` items in the shortlist.

### 5. Deliver

Always write the report to:

`.ai/absorb/YYYY-MM-DD-<slug>.md`

where `<slug>` is a short kebab-case name of the analysis focus or target (fallback: `external-practices`). Create `.ai/absorb/` if it does not exist.

The report should include:

1. Sources analyzed.
2. One section per external project.
3. Verified strengths.
4. Our Advantages.
5. Ranked adoption shortlist with target file paths in this repository.
6. Immediate text-only wins vs. larger follow-up work.

Only when the user explicitly asks not to persist, skip the file and return the same structure as a concise chat summary.

## Red Flags

- The provided path does not exist.
- The user asks for general code quality review instead of harness analysis.
- No AI-config surface is found in the external project.
- Candidate practices are documented but not wired anywhere.

Surface these explicitly; do not fabricate findings.

## Verification

- Targets were resolved before deep analysis.
- Each recommended practice has file-level evidence.
- At least one `no adoption needed` or `Our Advantages` item was recorded.
- The shortlist excludes unverified README-only claims.
- The report file exists at the stated path (unless the user explicitly requested chat-only).
- No commit or automatic adoption was performed.

## Output Contract

Return:

- resolved targets;
- key verified practices;
- rejected or conditional practices with reasons;
- our advantages;
- shortlist with proposed target paths in this repository;
- report path (always, unless the user opted out of persistence).

## Attribution

Created by abdi. Adapted for this repository by andresnator.
