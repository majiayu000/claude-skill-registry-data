---
name: agents-progressive-disclosure
description: Refactor oversized agent instruction files into concise shared rules and task-specific references when instruction cleanup is requested.
---

# Agents Progressive Disclosure

Use this skill to reduce unnecessary instruction context while preserving project-specific constraints. Keep a short, self-contained file when splitting it would add indirection without helping task selection.

## Delivery and scope

Deliver the revised instruction files. Keep review findings and editing boundaries out of their operational rules unless they are themselves an intended rule. Necessary editorial notes go in native comments, otherwise the conversation; routine checklists need not be reported. Preserve useful permission boundaries, while removing repeated defensive checks on trusted internal calls and redundant approval steps. Detailed examples are optional, not required sections.

## Core Model

Treat the root instruction file as a router, not a rule warehouse. Audit the instruction surfaces as a system: nearest `AGENTS.md` files, skill metadata and bodies, tool/action descriptions, and task-local instructions must have clear ownership and precedence.

- The entry file keeps only high-frequency, long-lived, must-always-apply rules.
- Detailed task-specific rules move into `docs/` files.
- When routing to separate documents is useful, state when to read them.
- Load the documents relevant to the current task.

## Workflow

1. Identify the target instruction file.
   - Prefer the current directory's `AGENTS.md` unless the user names another file.
   - Also support `CLAUDE.md`, `GEMINI.md`, or project-specific equivalents.

2. Inspect existing structure.
   - Read the target file fully.
   - Inspect linked docs and the applicable instruction hierarchy.
   - For catalog audits or suspected shadowing, inspect the relevant active skill roots for duplicate names, stale copies, and missing references. A single-file cleanup does not require an inventory of every installed skill.
   - Inspect tool/action descriptions when the instruction depends on how the agent selects or invokes a capability.

3. Classify rules into buckets.
   - Keep in entrypoint: language defaults, safety boundaries, tool priority, conflict priority, and critical must-always-follow rules.
   - Move to docs: command catalogs, search strategies, framework-specific instructions, package-manager rules, environment setup, Git workflow, deployment, testing, document style, domain terminology, long examples.

4. Design the docs map.
   - Use existing `docs/` names when they already fit.
   - Otherwise create focused names such as:
     - `docs/response-style.md`
     - `docs/search-and-evidence.md`
     - `docs/local-environment.md`
     - `docs/project-workflow.md`
     - `docs/domain-context.md`
   - Create `docs/README.md` only when it helps navigate multiple docs.

5. Edit conservatively.
   - Preserve user- and project-specific instructions unless they are demonstrably contradictory, unreachable, unsafe, or stale.
   - Do not turn a discovery index into a second copy of the full skill body; metadata should make the right skill findable, while the body owns the workflow.
   - Keep a recoverable original through version control or a local backup when needed.
   - Rewrite the entrypoint as a compact router with:
     - scope statement;
     - core principles;
     - on-demand docs index;
     - always-on safety/tool rules;
     - precedence rules.
   - Move useful detail into references; remove obsolete, duplicate, or explicitly unwanted restrictions rather than relocating them unchanged.
   - Avoid duplicating the same long rule in multiple places. Give shared content-placement decisions one global owner; skill entrypoints add only domain-specific choices and examples.
   - Separate instructions for doing the work from the artifact's section outline. Inspect linked templates and examples for contradictory output patterns, including captions, speaker notes, tooltips, and collapsed panels.
   - Route subject matter and meaningful limitations to the reader-facing result; route actionable editorial issues to native comments or the handoff; delete routine process residue. Do not weaken scientific, safety, or required disclosure content while removing boilerplate.

6. Validate preservation.
   - Compare line counts before and after.
   - Search for critical keywords from the original file across the new entrypoint and docs.
   - Verify the entrypoint tells future agents when to read each doc.
   - Check that no doc contradicts the entrypoint.
   - Verify edited templates are tracked and actually deployed, not merely changed in ignored local directories. Separate static rule checks from tests of generated agent output; neither guarantees future compliance.

## Suggested Entrypoint Shape

```md
# Agent Instructions

> Scope: This file is the entrypoint. It keeps only always-on rules; task details live in docs/.

## Core Principles

- [language/default behavior]
- [safety boundary]
- [primary tool or evidence policy]
- [this file is a router, not a warehouse]

## Read-On-Demand Index

| Task type | Read first | Trigger |
| --- | --- | --- |
| Search and evidence | `docs/search-and-evidence.md` | Current info, URLs, official docs, high-risk claims |
| Local commands | `docs/local-environment.md` | Shell, paths, environment, tools |

## Always-On Rules

- [short critical rules]

## Repository Convention Priority

Subject to the host's instruction hierarchy:

1. User's current explicit instruction.
2. Nearest project instruction file.
3. This file.
4. Routed docs details.
```

## Validation Commands

Use focused checks appropriate to the changed files, for example:

```zsh
wc -l AGENTS.md docs/*.md
rg --files docs
rg -n 'critical keyword|another keyword' AGENTS.md docs
sed -n '1,180p' AGENTS.md
```

Choose critical keywords from the source file, not from the template.

## Guardrails

- Do not delete rules merely because they are verbose; move them to the right doc.
- Do not bury safety-critical rules only in a routed doc.
- Do not create many tiny docs with overlapping responsibilities.
- Do not add project-specific opinions that were not in the source file unless the user asks.
- Do not claim installation into Codex unless you actually copy or install the skill into the active skills directory and verify it.
