---
name: skill-name
description: Use when an agent needs to perform a specific repeatable task in a specific context
---

# Skill Name

## Overview

State the core purpose in one or two sentences. Explain what this skill helps an agent do, without turning the overview into a long tutorial.

## When To Use

Use this skill when:

- The task matches a repeatable workflow.
- The agent needs domain-specific constraints, tool order, or verification rules.
- The expected output has a recognizable quality bar.

Do not use this skill when:

- The task is a one-off note.
- The behavior is better enforced by code, linting, or a script.
- General documentation already covers the need clearly.

## First Questions

Ask for the minimum inputs the workflow depends on, for example:

- The target library, tool, chip, or protocol version in play.
- The runtime context (bare-metal or RTOS) and relevant config files.
- The exact command, error code, or symptom being investigated.

## Workflow

Name this section for the task shape: `Integration Checklist` for library
integration skills, `Debug Workflow` for debugging skills, or keep `Workflow`
for anything else.

1. Gather the minimum context needed for the task.
2. Follow the domain-specific steps in order.
3. Stop and ask for clarification if required inputs are missing.
4. Verify the result with the checks below.

## Common Failures

- Writing a broad essay instead of operational guidance.
- Making the description summarize the workflow instead of trigger conditions.
- Adding too many examples instead of one strong example.
- Forgetting verification, which makes the skill hard to trust.

## Verification

Before claiming completion:

- Confirm the expected artifact exists.
- Confirm the output matches the user's request.
- Run the relevant command, checklist, or manual inspection step.
- Report any limitation or skipped check.

## Example

User: "Create a release note from these commits."

Agent:

1. Loads the release-note skill because the task is a repeatable writing workflow.
2. Collects commit messages and user-facing changes.
3. Drafts the release note in the required format.
4. Checks that the note avoids internal-only implementation details.
