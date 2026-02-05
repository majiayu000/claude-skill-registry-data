---
name: Codex Prompt Optimization
description: This skill should be used when the user asks to "create a codex prompt", "write a CTM", "format task for codex", "optimize prompt for codex", "submit to codex", or needs to generate a Codex Task Manifest (CTM) for delegation to OpenAI's Codex agent.
version: 0.1.0
---

# Codex Prompt Optimization

Guide for creating effective prompts for OpenAI's Codex coding agent using the Codex Task Manifest (CTM) format.

## Overview

Codex is OpenAI's coding agent that operates in a sandboxed Linux environment. It excels at clearly bounded tasks but struggles without explicit guardrails. The CTM format provides structure that plays to Codex's strengths while preventing common failure modes.

## What Codex Does Well

- Executing a clearly bounded plan
- Navigating code when "neighborhoods" are named explicitly
- Writing clean Go when constraints are explicit
- Producing structured summaries when formats are enforced
- Multi-file changes with clear scope
- QA tasks (lint, tests, reviews) with defined success criteria

## What Codex Does Poorly (Without Guardrails)

- Over-refactoring beyond task scope
- "Helpful" speculative improvements
- Declaring success without proof
- Forgetting friction once code works
- Architectural decisions requiring judgment
- Tasks needing conversation or iteration

## CTM Structure

The Codex Task Manifest counters Codex's weaknesses by:

1. **Forcing restated understanding** before edits
2. **Hard-coding non-goals** to prevent scope creep
3. **Making verification mandatory** as deliverable
4. **Requiring friction reports** for continuous improvement

### Essential CTM Sections

| Section | Purpose |
|---------|---------|
| `task` | Identity: issue, branch, deliverable |
| `role` | Posture: conservative, craftsmanship |
| `context` | Success definition, non-goals |
| `inputs` | Relevant paths, test hints |
| `constraints` | Design rules, Go rules |
| `plan` | Required steps before editing |
| `verification` | Proof of work requirements |
| `friction_report` | Learning loop for future |
| `pr` | PR template with checklist |

## Generating a CTM

### From a GitHub Issue

To generate a CTM from a GitHub issue:

1. Fetch issue details (title, body, labels)
2. Extract requirements from issue body
3. Identify relevant code paths from issue context
4. Populate CTM template with issue data
5. Set branch name: `codex/issue-[n]-[slug]`

### From an Orca Task Nug

To generate a CTM from a task nugget:

1. Read nugget rationale for task description
2. Extract file references if present
3. Map nugget tags to relevant paths
4. Generate CTM with nugget context

### From a Description

To generate a CTM from a plain description:

1. Parse description for actionable requirements
2. Infer relevant code areas from keywords
3. Define clear success criteria
4. Generate conservative CTM with explicit non-goals

## CTM Best Practices

### Task Identity

```yaml
task:
  id: "[gh-issue-number]"
  title: "[short imperative summary]"
  repo: "github.com/OWNER/REPO"  # From .claude/codex.local.md
  branch: "codex/issue-[n]-[slug]"
  deliverable: "Open a PR that closes #[n]"
```

- Use imperative voice for title ("Add X", "Fix Y")
- Branch naming: `codex/issue-{number}-{slug}`
- Deliverable must be concrete ("Open a PR", not "Implement")

### Role and Posture

```yaml
role:
  primary: "Senior Go engineer working in this repo"
  posture:
    - "Conservative changes"
    - "Craftsmanship over cleverness"
    - "Assume long-term maintainership"
```

Codex mirrors the posture given. Explicit conservatism reduces overreach.

### Non-Goals (Critical)

```yaml
non_goals:
  - "No architectural redesign"
  - "No renames or formatting-only changes"
  - "No new dependencies unless explicitly required"
```

Non-goals act as brakes. Without them, Codex often "improves" unrelated code.

### Required Plan

```yaml
plan:
  required_steps:
    - "Restate the issue requirements in your own words"
    - "Identify current behavior and exact code locations"
    - "Propose a minimal implementation approach"
    - "Define test strategy"
    - "List risks or ambiguities"
```

Codex is far more accurate after explicitly reasoning in writing.

### Verification Requirements

```yaml
verification:
  must_provide:
    - "List of commands run and their outcomes"
    - "Summary of key code changes (what + why)"
    - "Risk assessment and rollback notes"
    - "Anything intentionally left out"
```

Forces Codex to prove work rather than declaring success early.

### Friction Report

```yaml
friction_report:
  minimum_items: 3
  categories:
    - "Repo navigation"
    - "Build/test workflow"
    - "Code ergonomics / API design"
```

Turns PRs into a learning loop. Mine friction reports into Orca nugs (traps, rules) for future improvement.

## Quick CTM Template

For simple tasks, use a minimal CTM:

```yaml
task:
  title: "[imperative summary]"
  repo: "github.com/OWNER/REPO"  # From .claude/codex.local.md
  branch: "codex/[slug]"
  deliverable: "Open a PR"

context:
  success_definition:
    - "[specific criterion]"
  non_goals:
    - "No unrelated changes"

inputs:
  relevant_paths_hint:
    - "[path/to/relevant/code]"

testing:
  commands:
    - "mage qa"
    - "go test ./..."
```

## Additional Resources

### Reference Files

- **`references/ctm-template.yml`** - Full CTM template with all sections
- **`references/ctm-examples.md`** - Real CTM examples for different task types

### Quick Reference

| Task Type | Key CTM Focus |
|-----------|---------------|
| Bug fix | Clear repro steps, test strategy |
| QA/lint | File list, specific rules to enforce |
| Feature | Bounded scope, explicit non-goals |
| Review | Output format, criteria checklist |
