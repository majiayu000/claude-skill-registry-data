---
name: skill-cleaner
description: Audit or simplify skills while preserving technical knowledge, quality requirements, and clear decision boundaries.
disable-model-invocation: true
---

# Skill Cleaner

Reduce unnecessary instructions without reducing useful knowledge or the quality and maintainability requirements.
Treat lower context cost as a design benefit, not the acceptance criterion.

## Choose the scope

For a content cleanup, inspect the named skills and their relevant references.
For an inventory, duplicate, or prompt-budget audit, use the analyzer below.
A focused content edit does not require a global inventory or session-log scan.

Treat an audit request as read-only.
Apply edits when the user requests cleanup or accepts proposed changes.
Preserve unrelated work and the existing invocation policy.
Commit, disable, uninstall, or delete skill directories only when the user authorizes those actions.

## Content decisions

Compare the current content with its prior version before a substantial reduction.
Inspect reference callers before a move or removal.
Use these criteria for each meaningful section, rather than a target line count:

| Content | Decision |
| --- | --- |
| Repeated reminders, fixed task itineraries, arbitrary agent counts | Remove when they add no necessary constraint |
| Quality requirements and technical invariants | Preserve with their actual conditions |
| Framework pitfalls, compatibility details, and project conventions | Keep in task-specific references |
| Useful code examples, diagnostic commands, and reusable scripts | Preserve or correct where they prevent repeated research |
| Substantial detail that only some tasks need | Move behind a link with a clear activation condition |
| Conflicting or outdated advice | Resolve from the affected contract and authoritative evidence |
| Duplicate material | Consolidate only after confirming equivalent coverage and a reachable retained copy |

Model familiarity is not evidence that technical documentation is redundant.
Do not substitute assumed model knowledge, Git history, or an archive for a maintained reference.
External sources support local guidance but do not replace project-specific reasons, pitfalls, or useful examples.
When value or correctness remains uncertain, retain the material conditionally and state the uncertainty.

## Structure and boundaries

Keep descriptions short and specific enough to select the skill correctly.
Keep shared purpose, essential constraints, and task routes in the root.
Place substantial examples and specialized procedures in existing references when possible.
Link each retained reference from the task that needs it.
A short, single-purpose skill does not require another router.

Separate framework requirements from library conventions, project preferences, and illustrative examples.
State the version or configuration boundary when behavior depends on it.
Preserve the user's chosen architecture and dependency policy unless the task requires a change.

Replace blanket process rules with conditions and completion criteria.
For example, local implementation can continue through relevant corrections and affected checks within the authorized scope.
That scope does not imply permission for publication, certificate trust, account changes, or destructive cleanup.
Keep approval boundaries at the consequential action, not at harmless inspection.

Preserve the required outcome when removing its prescribed method.
For example, remove a universal MVVM mandate while retaining state ownership, lifecycle, and dependency constraints.
Remove a mandatory full test suite for every edit while retaining checks appropriate to the affected contract.
Resolve contradictions in reachable references as well as in the root.

## Evidence and acceptance

Use repository contracts and resolved dependency versions for project-specific claims.
Use current primary documentation for uncertain or version-sensitive behavior.
Correct invalid examples instead of restoring them unchanged.
Label schematic examples and distinguish source review from successful compilation.

For a substantial reduction, account for removed technical topics in the change summary.
Identify which topics remain, which moved, and which were removed with a reason.
A restored topic needs a useful reference, not only a heading or an external link.

Validate changed metadata, local links, and affected scripts.
Use `quick_validate.py` from skill-creator when available.
A metadata or link check does not establish equivalent task performance.

For a broad rewrite, use an independent scenario pass when available and authorized.
Include an ordinary edit and a task that needs the specialized knowledge.
Check reference discovery, retained constraints, and the scope of permitted actions.
Use isolated artifacts for execution tests.
Report untested behavior without a claim of equivalent model performance.

## Inventory analyzer

Use [the bundled analyzer](scripts/skill-cleaner.ts) when inventory evidence affects the cleanup decision.
From this repository root:

```bash
node --experimental-strip-types skills/personal/skill-cleaner/scripts/skill-cleaner.ts --no-logs
```

From another location, resolve the script relative to this skill directory.
The analyzer scans configured default roots. `--root <path>` adds a root rather than restricting the scan.

Use session evidence only when the user places that history in scope.
For an authorized usage audit, omit `--no-logs` and select `--months` and `--max-log-mb`.
The `--deep-logs` flag expands log discovery. It does not create subagents.
Do not expose private transcript contents in reports.

Treat the analyzer report as a set of candidates:

- Skill Budget estimates description-list pressure, not task quality or actual tokens consumed.
- Description candidates need a trigger-clarity check, not merely shorter grammar.
- Duplicate candidates need body, resource, version, customization, and load-path comparison.
- Unused candidates mean no detected use within the sampled logs, not proof that a skill has no value.
- Root summaries describe discovery and configuration evidence, not a guaranteed view of the active harness.

The script defaults to `gpt-5.5`, a 2% budget, and an approximate byte-to-token conversion.
It reads a local model cache and can fall back to 272,000 context tokens.
These are implementation assumptions, not verified current Codex limits.
Use `--model`, `--context-tokens`, and `--budget-percent` when authoritative values are available.
State the source and fallback status with any reported budget.
Do not prefer a built-in copy solely because it is built in.

## Completion

Report the changes, retained knowledge, resolved conflicts, validation limits, usage, and file scope.
For an audit, report recommendations without edits.
For an authorized cleanup, leave a reviewable diff unless the user requests a commit.
