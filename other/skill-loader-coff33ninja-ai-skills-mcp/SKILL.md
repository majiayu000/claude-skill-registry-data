---
name: skill-loader
description: When a skill is loaded, selectively loads the most relevant direct cross-references with strict caps. Preserves core operating discipline without letting cross-references cascade into context bloat.
---

# Skill Loader

## Problem it solves

Skills are activated individually, but many skills rely on nearby operating discipline. For example, a code-modification skill often needs validation, symbol checks, and existing-pattern checks to prevent repeat corrections. Cross-references keep those guardrails connected after context compaction, but loading every related skill creates context bloat and weakens focus.

## Protocol

### 1. Inspect direct cross-references

Whenever a skill is loaded, inspect only its own `## Cross-references` section. Identify direct skill names listed in bold at the start of each bullet.

Do not recursively inspect cross-references from referenced skills during normal work.

### 2. Classify references by operational value

Load a cross-referenced skill only when it changes behavior for the current task. Prefer references whose bullet explains a concrete action, such as validating edits, verifying symbols, avoiding global installs, preserving backups, or checking sources.

Skip references that are only broadly related, informational, or already covered by a loaded skill.

### 3. Apply strict load caps

Default cap:

```
initial skill + up to 3 direct cross-references
```

Expanded cap for broad audit, release, security, or repo-wide maintenance tasks:

```
initial skill + up to 5 direct cross-references
```

Only exceed these caps when the user explicitly asks for comprehensive coverage or the task cannot be done safely without the additional skills.

### 4. Prefer the core discipline set

When choosing among relevant references, prioritize these recurring guardrails:

- **self-validate** — verify that edits, generated files, and cross-reference changes actually worked.
- **safe-code-modifications** — avoid unsafe removal or broad edits without usage checks.
- **follow-existing-patterns** — align changes with the repository's current conventions.
- **anti-phantom-symbols** — verify APIs, imports, methods, and file paths before relying on them.
- **anti-premature-termination** — do not declare completion before validation and user-visible criteria are met.

Use task-specific skills when they are more relevant than a core discipline skill. Examples: `uv` for Python environment work, `verify-and-cite` for factual claims, `project-backup-status` before risky repo edits, or `playwright` for browser automation.

### 5. Deduplicate and avoid cycles

If multiple loaded skills reference the same target skill, load it once. Never load `skill-loader` merely because another skill lists it; this skill is a policy controller, not a task skill.

### 6. Preserve active discipline through compaction

When summarizing work for context compaction or handoff, include a compact active discipline set:

```
Active skill discipline: self-validate, follow-existing-patterns, anti-phantom-symbols
```

This keeps the important behavioral constraints alive after memory condensing without reloading the whole graph.

### 7. When no cross-references exist

Some skills have no operational cross-references. No additional loading is needed.

### 8. Selection checklist

Before loading a cross-reference, answer:

1. Does it prevent a likely failure mode in this task?
2. Does its bullet state a concrete operational reason?
3. Is it within the cap?
4. Is it not already covered by an active skill?

If any answer is no, skip it and continue.

## Detection triggers

Activate when a skill is loaded and its cross-references may materially affect the task. This is a companion protocol, not a mandate to load every related skill.

## When NOT to use

- The loaded skill has no `## Cross-references` section
- The user explicitly asks you to load only one skill
- Loading more skills would exceed the caps without a concrete safety reason
- The cross-reference is only conceptual or documentary

## Cross-references

- **dont-kill-tokens** — Loading multiple skills consumes context. Use caps and skip tangential references.
- **anti-tool-sprawl** — Each skill load is a tool call. Batch relevant loads and avoid graph traversal.
- **self-validate** — After skill or cross-reference edits, validate that the instruction set is internally consistent.
- **follow-existing-patterns** — Cross-referenced skills may have their own patterns. Follow the most specific one for the current subtask.
- **context-engineering** — Use together. skill-loader handles which skills to load; context engineering handles which project files to load.
