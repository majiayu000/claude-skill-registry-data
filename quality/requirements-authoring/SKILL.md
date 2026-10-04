---
name: requirements-authoring
description: Applies repository-specific requirements standards to requirement documents. Use this skill when creating, editing, or reorganizing requirements.
---
# Requirements Authoring

## Discover the Requirements System

Before editing, find and read the repository's agent instructions, source-of-truth hierarchy, requirements index, authoring standards, domain registry, identifier rules, templates, lint configuration, and representative nearby requirements.
Treat those sources as authoritative over this skill's general guidance.

Determine the following without assuming fixed names or locations:

- The canonical requirements root and file organization.
- The distinction between requirements, specifications, design notes, and tests.
- Identifier syntax, allocation policy, uniqueness scope, and anchor normalization.
- Required entry structure and permitted normative language.
- Traceability direction, link format, and required targets.
- Validation commands and repository task runner.

Do not invent an identifier, domain, anchor, or traceability target when the allocation rule is unclear.
Ask for direction when repository sources conflict or when the requested change would alter a higher-priority source of truth without authorization.

## Write Clear Requirements

- State what outcome, behavior, or constraint is required.
- Keep implementation choices out of requirements when the repository assigns design details to specifications.
- Make each requirement atomic, testable, unambiguous, and stable.
- Prefer one independently verifiable obligation per requirement entry.
- Identify the actor, conditions, required behavior, and observable outcome when they are not otherwise clear.
- Use the repository's normative vocabulary consistently.
- Avoid vague qualifiers such as "appropriate," "reasonable," or "as needed" unless they are objectively defined.
- Preserve established terminology and link to canonical definitions instead of duplicating them.
- Separate rationale and examples from normative text when local structure permits them.

## Preserve Identity and Traceability

Retain existing identifiers unless the user explicitly authorizes renumbering or the repository mandates it.
Check the complete identifier namespace before allocating a new value.
Generate anchors and link targets using the repository's exact normalization rules.
Link each requirement to the specifications, acceptance tests, risks, or other artifacts required by local policy.
Verify every link and identifier against real repository content.

## Review Changes for Semantic Integrity

Confirm that edits do not weaken obligations, combine independently testable behaviors, lose edge cases, or silently change scope.
When moving or consolidating requirements, preserve all material constraints and update inbound and outbound traceability.
Call out contradictions between requirements, specifications, tests, and implementation instead of resolving them by assumption.

## Validate the Result

Run the repository-provided formatter, documentation linter, identifier validator, link checker, and traceability checks relevant to the changed files.
Prefer project task-runner commands over invoking underlying scripts directly.
Report commands run, failures encountered, and checks that could not be performed.
