---
name: review-a-skill
description: Use when evaluating whether a skill belongs in a library. Preview content, check frontmatter, validate structure, and decide whether to keep, curate, or remove.
category: workflow
version: 4.1.0
---

# Review A Skill

## Goal

Evaluate a single skill's quality, relevance, and safety before it enters or stays in a library.

## Guardrails

- Always use `--format json` for machine-readable output in automated pipelines.
- Always use `--fields` to limit output size when inspecting catalog entries.
- Always use `--dry-run` before curating or removing a skill.
- Never remove a skill without first checking if other skills depend on it via `info --format json` dependencies.

## Workflow

1. Preview the skill content to check for quality and safety.

```bash
npx ai-agent-skills preview <skill-name>
```

The preview command sanitizes content — if it flags sanitization, investigate before proceeding.

2. Inspect the catalog entry for metadata completeness.

```bash
npx ai-agent-skills info <skill-name> --format json --fields name,description,tags,collections,dependencies
```

3. Validate the skill's SKILL.md structure.

```bash
npx ai-agent-skills validate <skill-name>
```

4. If the skill needs curation (notes, collections, verification):

```bash
npx ai-agent-skills curate <skill-name> --notes "Reviewed: solid patterns" --verify --dry-run
npx ai-agent-skills curate <skill-name> --notes "Reviewed: solid patterns" --verify
```

5. If the skill should be removed:

```bash
npx ai-agent-skills curate <skill-name> --remove --dry-run
npx ai-agent-skills curate <skill-name> --remove --yes
```

## Decision Criteria

- **Keep**: Clear description, valid frontmatter, useful to the library's audience, no injection patterns.
- **Curate**: Needs better whyHere, collection placement, or verification status.
- **Remove**: Duplicate, outdated, broken source, or contains suspicious content.

## Gotchas

- The `preview` command only works for vendored (house) skills. Upstream skills show description and whyHere only.
- The `validate` command checks frontmatter structure but not content quality — that requires human or agent judgment.
- Removing a skill that other skills depend on will break the dependency graph. Always check `dependencies.usedBy` first.
