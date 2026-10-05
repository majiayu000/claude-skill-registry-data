---
name: pattern-library-manager
description: 'Add or tighten reusable approved patterns and anti-patterns in common/** with source-backed examples, approvals, graph links, evals, and validation. Keep project-specific patterns in local-only project/**.'
id: 'agents.skills.pattern-library-manager.skill'
title: 'Pattern Library Manager'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'pattern-library-manager'
tags:
    - 'agents/skill-package'
    - 'agents/patterns'
    - 'agents/authoring'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/pattern-library-manager/references/pattern-entry-template|Pattern Entry Template]]'
    - '[[skills/pattern-library-manager/references/example-sourcing-policy|Example Sourcing Policy]]'
    - '[[common/approved-patterns|Approved Patterns]]'
    - '[[common/anti-patterns|Common Anti-Patterns]]'
    - '[[common/documentation-maintenance|Documentation Maintenance]]'
    - '[[skills/agent-rules-skill-author/SKILL|Agent Rules And Skill Author]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Pattern Library Manager

## Purpose

Add, tighten, or document reusable approved patterns and anti-patterns in this bundle without leaking host-project facts into publishable rules.

This skill owns small reusable pattern-library changes: descriptions, bad/good examples, graph links, trigger/output evals, and validation alignment.

## When To Use

Use this skill when the user asks to:

- add a reusable approved pattern;
- add a reusable anti-pattern;
- tighten an existing common pattern or anti-pattern;
- add code examples to a pattern or anti-pattern;
- add pattern examples sourced from official documentation or user-provided snippets;
- add eval coverage for a pattern-routing regression;
- update `common/approved-patterns.md`, `common/anti-patterns.md`, or `common/anti-patterns/**` for reusable behavior.

## When Not To Use

Do not use this skill for:

- project-specific patterns or anti-patterns; use local-only `project/**` overlays instead;
- general skill creation unrelated to patterns; use `agent-rules-skill-author`;
- implementation, bugfix, refactor, visual QA, or review work;
- adding examples copied from private project code into reusable docs;
- adding long third-party code excerpts.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/documentation-maintenance.md`.
3. Read `common/approved-patterns.md` or `common/anti-patterns.md` depending on the requested change.
4. Read the existing target pattern or anti-pattern file when modifying one.
5. Read `references/pattern-entry-template.md` before creating a new entry.
6. Read `references/example-sourcing-policy.md` before adding code examples.
7. Read `evals/trigger-evals.json` or `evals/output-evals.json` when routing or output behavior changes.

## Tool Contract

- Use the `project_files` capability for repository file reads and writes.
- May use official documentation or trusted maintainer sources to understand a pattern when examples are not supplied by the user.
- Activate `openai_platform_docs` only when a reusable pattern depends on current OpenAI or Codex behavior.
- Must propose sourced examples to the user before committing them when they come from external material or host-project-specific context.
- Must write original, short examples instead of copying long third-party code.
- Must not install packages, change runtime code, create tests, or modify host-project documentation.
- Must not use Figma MCP.

## Workflow

1. Classify the requested change as approved pattern, anti-pattern, example-only update, tightening, or eval coverage.
2. Decide whether the change is reusable bundle policy or host-project local guidance.
3. If the pattern is project-specific, stop and route to a local-only `project/**` overlay plan.
4. For reusable changes, inspect the current common rule or anti-pattern index.
5. Define the rule, allowed exceptions, bad example, good example, apply-when guidance, and validation impact.
6. Ask the user for examples when the requested pattern depends on a concrete code shape not already provided.
7. If examples are not supplied, use official or trusted sources only to understand the pattern, then write short original examples and propose them for user approval before committing.
8. Add or update the smallest owning file:
   - `common/approved-patterns.md` for positive reusable patterns;
   - `common/anti-patterns.md` for the index and routing summary;
   - `common/anti-patterns/<name>.md` for concrete anti-patterns with examples.
9. Update graph links so new documents have incoming edges.
10. Add trigger or output evals when the change prevents a real routing or behavior regression.
11. Run the relevant skill/bundle validators when available.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Report:

```text
Pattern change:
Reusable or local-only decision:
Files changed:
Examples added or proposed:
Source or user example basis:
Eval changes:
Validation:
Risks:
```

## Validation Gates

- Reusable pattern docs must not contain host-project facts.
- Bad/good examples must be short, original, and scoped to the rule.
- External examples must be source-backed and user-approved before committing when they shape the final code example.
- New anti-pattern files must be linked from `common/anti-patterns.md` or `common/anti-patterns/README.md`.
- Pattern changes must not create tests, packages, runtime code, or host documentation edits.
- Every changed reusable Markdown file must keep graph frontmatter and English rule text.

## Trigger Evals

Should trigger:

- "Add an anti-pattern for parallel status booleans with bad and good TypeScript examples."
- "Tighten the useCallback anti-pattern and add eval coverage."
- "Add a reusable pattern for discriminated request statuses."
- "Add examples to this anti-pattern, ask me before using project-specific snippets."

Should not trigger:

- "Create a new feature workflow skill."
- "Implement this React component."
- "Add a project-specific pattern from this app into .agents/project."
- "Review this PR for quality."

## Reference Map

- `references/pattern-entry-template.md`
- `references/example-sourcing-policy.md`
- `common/approved-patterns.md`
- `common/anti-patterns.md`
- `common/documentation-maintenance.md`
- `skills/agent-rules-skill-author/SKILL.md`
