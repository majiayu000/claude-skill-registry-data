---
name: agent-dx-cli
description: Designs, reviews, and refactors CLIs for AI agents. Use when building Agent DX CLIs or checking existing CLI contracts. Checks predictability, defense in depth, and context efficiency with evidence scores.
metadata:
  language: en
  translation_of: agent-dx-cli-cn
  version: "0.4.2"
---

# Agent DX CLI

Design, review, and refactor CLIs for agents. Preserve the user's scope, stack, and existing authorization.
Human conveniences and agent contracts can coexist; add only mechanisms the task needs.

## Workflow

1. Inspect code, current help/schema, and actual output. Record the CLI artifact and version.
2. Read [principles, reasons, and examples](references/agent-dx-patterns.md). Assess all applicable checks; distinguish missing, unverified, and verified behavior.
3. Implement authorized changes, fixing acceptance blockers first. Reuse established libraries and share validation/execution across CLI, MCP, and batch surfaces.
4. Verify positive and negative cases in an authorized isolated fixture. Report changes, per-check evidence, scores, and unresolved limits.

Proceed when facts and authorization suffice. Clarify only ambiguity that changes the target or consequences. A review request authorizes review only.

## Principles

- **Predictability:** preserve typed intent from input to outcome; expose a queryable contract instead of requiring guesses.
- **Defense in depth:** validate input, enforce current permissions, and reconcile outcomes independently; one safeguard cannot replace another.
- **Context efficiency:** return bounded data and load task-relevant knowledge; every extra field or instruction must earn its cost.

## Execution boundaries

- Default to non-interactive execution. Optional interaction requires explicit selection and a TTY.
- Treat agent input as untrusted. Enforce typed, field-specific constraints in the shared executor before business effects.
- Treat server content as untrusted data even after sanitization; preserve provenance.
- Schema, previews, quality reports, and confirmation flags do not grant permission. Declare actual preview effects and recheck authorization at execution.
- Return `unknown` for unresolved outcomes. Reconcile before safe replay; report completion only after the requested result is verified.

## Optional references

- For API/GWS alignment, use [GWS practice](references/gws.md). Retain its pinned version and verify project differences.
- For companion skill authoring or review, use [SKILL+CLI authoring](references/skill-cli.md). Separate the four disclosure layers and retain useful decision guidance.
  Compare materially changed guidance with a no-skill baseline; stale syntax or misleading rules can make performance worse.

## Scoring and acceptance

The patterns reference defines ten dimensions with two checks each. Score each check 0–5; the total is 100. This is the skill's scoring convention.

| Score | Required evidence |
| --- | --- |
| 0 | Missing or contradicted. |
| 1 | Documented only. |
| 2 | Implemented but unverified. |
| 3 | Positive cases passed. |
| 4 | Relevant negative cases passed. |
| 5 | End-to-end validation passed in the target environment. |

For static criteria: 3 means implementation review; 4 means consumer and negative-case comparison; 5 means reproducible contract or dependency checks.
Attach evidence and the tested artifact/version to every score. Necessary behavior must be verified before acceptance.
Acceptance requires at least 90 overall, with validation and authentication each at least 9.
Credential leaks, authorization bypass, preview business writes, unsafe replay, or false completion block acceptance regardless of score.
Explain every N/A; requested but missing features are not N/A. Report raw points and normalized score: raw points / applicable maximum × 100.
