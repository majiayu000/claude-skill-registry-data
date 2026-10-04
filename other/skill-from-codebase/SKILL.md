---
name: skill-from-codebase
description: This skill should be used every time you generate, refresh, or validate codebase-derived SKILL.md documentation for this repository.
compatibility: opencode
---

# Skill-From-Codebase Generation Rules

## Purpose

Define a consistent standard for generating and maintaining `SKILL.md` as an instruction corpus for coding agents.

`SKILL.md` must help agents decide what to edit, how to use public entities, and how to avoid repo-specific mistakes.

## Core Principles

1. **Single documentation artifact** - Maintain one canonical `SKILL.md` at repo root.
2. **Instruction-first** - Prefer actionable guidance over catalog-style descriptions.
3. **Verified facts only** - Never include unverified paths, APIs, counts, or commands.
4. **Adaptive structure** - Infer repository domains and public entity types from current codebase.
5. **Incremental by default when possible** - Use commit baseline diffing to update only impacted sections.
6. **Committed-history only** - Generation and refresh decisions must use committed git history, never uncommitted working-tree changes.
7. **Scope-sync compliant** - Maintain explicit root-folder include/exclude classification and exclude docs-only paths from domain generation.

## Required Files

1. **`SKILL.md` at repository root** - Canonical corpus file.
2. **`.nexus/ai_harness/skills/<project-name>/skills-state.json`** - Generation state for incremental refresh.

State file schema:

```json
{
  "skill_path": ".nexus/ai_harness/skills/<project-name>/SKILL.md",
  "last_generated_commit": "<sha>",
  "generated_at": "<ISO-8601>"
}
```

## Generation Modes

## Commit Baseline Requirement

Generation is commit-based:

- Run only on a clean working tree.
- If `git status --porcelain` is not empty, abort generation.
- Never derive impact analysis from unstaged, staged-but-uncommitted, or untracked files.
- Incremental diff source is strictly `last_generated_commit..HEAD`.

## Scope-Sync Compliance

- Classify every root folder as included or excluded before domain inference.
- Exclude documentation-only roots and paths (for example `docs/`, `**/*.md`) from domain generation.
- Keep excluded paths available for link/source validation only.

### Full Mode

Use full mode when:
- `SKILL.md` does not exist
- `.nexus/ai_harness/skills/<project-name>/skills-state.json` does not exist
- `last_generated_commit` is missing/invalid
- structural changes make partial refresh unsafe

### Incremental Mode

Use incremental mode when both `SKILL.md` and valid state exist:
- diff from `last_generated_commit..HEAD`
- map changed files to impacted sections/cards
- regenerate only impacted sections/cards
- preserve untouched sections verbatim

Escalate incremental -> full when changes are broad or affect global structure (workspace topology, core manifests, large docs reshuffle).

## Orchestration Workflow

The main command agent is the orchestrator. It must not delegate orchestration itself.

1. **Scan/Impact Analysis**
   - Full mode: scan full repository and infer domains.
   - Incremental mode: compute changed files and impacted domains.
2. **Domain Subagents**
   - Spawn subagents per domain/impacted domain.
   - Subagents return draft content, links, rules, pitfalls, and usage-card material.
3. **Assembly Subagent**
   - Spawn one assembly subagent to merge drafts into proposed `SKILL.md`.
   - Full mode: build full document.
   - Incremental mode: patch only impacted sections/cards.
4. **Validator Subagent**
   - Spawn one validator subagent to check all quality gates.
   - On failure, loop assembly + validation until pass.
5. **Finalize**
   - Write `SKILL.md` only after validator pass.
   - Update `.nexus/ai_harness/skills/<project-name>/skills-state.json` with current `HEAD`.

## Required `SKILL.md` Sections

Use this order:

1. `# <Project Name>`
2. Summary paragraph (operational, concise)
3. `## Agent Operating Rules`
4. `## Environment and Version Constraints`
5. `## Quick Task Playbooks`
6. `## Getting Started`
7. `## Workspace Overview`
8. Inferred domain sections
9. `## Usage Cards`
10. `## API Reference`
11. `## Common Pitfalls`
12. `## Optional`

## Usage Card Standard

Do not assume component libraries. Infer dominant entity type (components, modules, endpoints, commands, services, models, etc).

Each usage card must include:
1. `Use when`
2. `Enable/Install` (if applicable)
3. `Import/Invoke`
4. `Minimal flow` (2-4 steps)
5. `Key APIs`
6. `Pitfalls` (1-2 concrete mistakes)
7. `Source` (verified internal repo path only; keep brief, non-catalog)

Usage card constraints:

- `Source` must point to existing internal files or directories in this repository.
- For web usage cards, `Key APIs` must use exact full route identifiers only (for example `/api/v1/users/{id}`), never shorthand names.

## Quality Gates (Mandatory)

1. Exactly one H1 at top.
2. No broken internal links.
3. No duplicate entries.
4. No nonexistent files/directories.
5. No stale/incorrect counts.
6. No unverifiable claims.
7. No generic filler text.
8. Usage cards include executable guidance.
9. API names in usage cards are verified against real symbols in current codebase.
10. Incremental mode changed only impacted sections unless explicit escalation to full mode.
11. Version strings copy manifest semantics exactly (operators and pins), e.g. React `^19.2.4`.

## Anti-Patterns

1. Writing `llms-full.txt` as part of this workflow.
2. Rebuilding entire file on every run when incremental refresh is safe.
3. Inventing APIs from intuition instead of symbol verification.
4. Leaving stale counts/paths after code moves.
5. Rewriting untouched sections during incremental updates.
