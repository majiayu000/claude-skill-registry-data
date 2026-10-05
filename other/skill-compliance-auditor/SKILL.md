---
name: skill-compliance-auditor
description: Audit reusable plugin skills, project-local .codex skills, AGENTS.md, nested instructions, context cost, stale guidance, duplicated rules, routing gaps, and daily-vs-library placement. Use when maintaining this harness, validating generated local skills, or checking whether agents can actually follow the available instructions.
---

# Skill Compliance Auditor

## Purpose

Find whether agent instructions and skills are usable, discoverable, current, and placed at the right scope instead of bloating daily context.

## Inspect First

- plugin `skills/`, project `.codex/skills`, root and nested `AGENTS.md`
- README, docs indexes, validation scripts, generated local skills, and recent skill changes
- any existing skill compliance report

## Procedure

1. Inventory instruction surfaces.
   - Separate plugin skills, project-local skills, root instructions, nested instructions, and docs.
   - Treat plugin skills as reusable authoring workflows and project-local skills as thin repo-specific operating workflows.

2. Check compliance and signal.
   - Run `scripts/check_skill_compliance.py <repo-or-plugin> --json` when available.
   - Flag missing frontmatter, missing required sections, oversized local skills, stale file links, duplicated hard rules, weak routing links, and instruction content that belongs in docs.
   - Classify local skills as `daily`, `on_demand`, or `library` based on frequency and evidence.

3. Produce a report when requested.
   - Use `assets/templates/skill-compliance-report.md.tmpl`.
   - Prioritize fixes that reduce daily context, remove contradiction, or make a skill trigger more reliably.

4. Route fixes.
   - Use `$project-local-skill-generator` for repo-local skill generation.
   - Use `$agents-md-author` or `$nested-agents-md-author` for instruction map cleanup.
   - Use `$harness-diagnostics` when compliance issues are part of a broader maturity audit.

## Validation

- Run `scripts/check_skill_compliance.py <repo-or-plugin>`.
- Confirm every finding names a concrete file, skill, or missing route.
- Confirm recommendations preserve the plugin/project-local split.

## Completion Criteria

- Skill and instruction issues are grouped by severity and scope.
- Daily instructions are lean, local skills are backed by repo artifacts, and reusable harness logic remains in plugin skills.
