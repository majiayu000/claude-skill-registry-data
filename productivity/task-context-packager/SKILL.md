---
name: task-context-packager
description: Creates the minimum evidence-backed context package an agent needs to complete one repository task without rereading the entire codebase. Use when preparing a coding-agent handoff, delegating a bounded issue, resuming interrupted work, isolating relevant files and constraints, or reducing a large repository into task-specific goals, evidence, dependencies, acceptance criteria, and verification commands.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: generator
  audience: developers-maintainers-and-coding-agents
  tags:
    - task-context
    - agent-handoff
    - repository-navigation
    - context-engineering
    - delegation
    - acceptance-criteria
  status: draft
  side_effects: none
---

# Task Context Packager

## Purpose

Create a compact, self-contained handoff for one repository task. Give the receiving agent enough verified context to act safely while replacing broad repository summaries with precise file, symbol, command, constraint, and decision references.

The package is a navigation aid, not a substitute for opening the specific files before editing them.

## When to use this skill

Use this skill when:

- A task will be delegated to another agent or developer.
- An interrupted task needs a clean resumption package.
- A large repository makes repeated orientation expensive.
- An issue, plan item, or request needs task-local goals, boundaries, evidence, and checks.
- Several files matter, but reading the whole repository would add noise.

Do not use this skill when:

- The task is still too vague to define a concrete outcome; clarify or write the brief first.
- The user needs a full repository audit, architecture map, or onboarding guide.
- The task requires live debugging state that cannot be captured in a static package.
- The receiving agent already has current, sufficient task context.

## Inputs to inspect

Start with:

- The exact task request, issue, plan item, or acceptance criteria.
- Repository-level instructions such as `AGENTS.md`, `CONTRIBUTING.md`, and scoped instruction files.
- The smallest likely set of target files and their direct tests, types, callers, imports, configuration, and documentation.
- Relevant working-tree changes when they could affect or overlap the task.
- Existing commands for focused validation.
- Prior decisions, failures, or review feedback that materially constrain the task.

Use filenames, imports, symbols, targeted search, and test references to expand outward. Do not begin by reading every file or generating a repository-wide summary.

## Context selection rules

Include an item only when it does at least one of these jobs:

- Defines the requested outcome or a non-goal.
- Constrains how the work may be performed.
- Identifies a likely edit location or affected interface.
- Explains a dependency, caller, invariant, or regression risk.
- Supplies an acceptance criterion or verification method.
- Records an unresolved decision the receiving agent cannot safely invent.

Classify candidate context as:

- **Mandatory:** Needed before the agent can act safely or verify completion.
- **Useful:** Likely to save discovery time but not required to start.
- **Excluded:** Interesting repository context with no task-local consequence.

Prefer paths, symbols, line ranges, and short paraphrases over copied files. Include a snippet only when exact wording, syntax, or shape is important. Never include secrets, credentials, personal data, or unrelated private context.

## Workflow

1. **Normalize the task.** State the desired outcome, deliverable, scope, non-goals, and whether implementation is authorized. Preserve ambiguity as an open question rather than silently resolving it.
2. **Read governing instructions.** Find repository and directory-scoped instructions that apply to likely target files. Record only rules that affect this task.
3. **Locate the task surface.** Search for named features, symbols, routes, components, tests, configuration, and documentation. Identify the smallest plausible edit set.
4. **Trace one dependency ring.** Inspect direct callers, imports, types, tests, fixtures, and configuration around the task surface. Expand farther only when evidence shows a meaningful impact.
5. **Capture current state.** Summarize relevant behavior, existing partial work, failing evidence, and overlapping working-tree changes. Distinguish verified facts from inference.
6. **Define the execution contract.** Record allowed files or areas, protected behavior, dependencies, expected artifacts, acceptance criteria, and focused verification commands.
7. **Prune the package.** For every item, name the action or decision it enables. Remove duplicates, generic architecture prose, transitive details, and background that the agent can discover cheaply.
8. **Check sufficiency.** Confirm that an agent can identify where to start, what not to change, how to recognize completion, and which uncertainties require escalation.
9. **Add freshness metadata.** Record the branch or revision when available, relevant working-tree state, and when the package was assembled. Warn that changed files or stale runtime state must be rechecked.

## Output format

Return:

```md
# Task context: <task name>

## Task contract
- Outcome:
- Deliverable:
- In scope:
- Out of scope:
- Implementation authority:

## Governing instructions
- `<path>` — <task-relevant rule>

## Start here
| Priority | File or symbol | Why it matters | Inspect or change |
|---|---|---|---|

## Current behavior and evidence
- Verified:
- Inferred:
- Existing or overlapping changes:

## Dependencies and invariants
- ...

## Acceptance criteria
- [ ] ...

## Verification
- `<focused command>` — <what it proves>

## Open questions and escalation triggers
- ...

## Freshness
- Assembled:
- Branch/revision:
- Working-tree notes:
```

Omit empty sections only when their absence cannot hide risk. Keep useful context as pointers; attach exact snippets only when the receiver needs them before opening the source.

## Quality bar

The task is complete only when:

- The package covers exactly one bounded task.
- Every included item has a stated task-local purpose.
- Facts, inferences, and unresolved questions are distinguishable.
- Governing instructions and overlapping changes are surfaced.
- The likely edit surface and its direct dependency ring are identified.
- Scope, non-goals, invariants, acceptance criteria, and verification are explicit.
- The receiver can start without a repository-wide reread, but is directed to inspect target files before editing.
- The package contains no secrets or unnecessary private context.

## Edge cases

- If the task spans unrelated subsystems, split it into separate context packages or state why it is indivisible.
- If the edit surface cannot be located, package the discovery task instead of inventing target files.
- If generated, vendored, or build output files appear relevant, identify their source of truth and avoid presenting generated output as the primary edit target.
- If runtime state is essential, include the reproduction steps and observable state, then mark the static package as insufficient by itself.
- If repository instructions conflict, cite both and make the conflict an escalation trigger.
- If no focused test exists, provide the narrowest available validation and identify the coverage gap.
- If the working tree is dirty, separate task-related changes from unrelated user work and do not imply that either is safe to overwrite.

## Related skills

- `implementation-plan-writer`
- `project-brief-builder`
- `requirements-gap-finder`
