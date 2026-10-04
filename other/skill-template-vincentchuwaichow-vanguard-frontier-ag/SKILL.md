---
name: provider-skill-name
description: Use this skill for a specific cloud workflow. Mention provider, trigger phrases, expected inputs, and when not to use it.
---

# Human Skill Name

## Purpose

Describe the workflow and the user problem it solves.

## Inputs

- Required cloud/provider context.
- Files or commands to inspect.
- Safety constraints.

## Workflow

1. Verify scope and credentials without exposing secrets.
2. Read official documentation for claims that may drift.
3. Prefer read-only inspection before mutation.
4. Produce findings with evidence and risk level.

## Output

Return concise findings, remediation steps, and validation commands.

## Security notes

Call out permissions, production risks, and approval gates.
