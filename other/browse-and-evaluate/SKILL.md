---
name: browse-and-evaluate
description: Use when exploring the ai-agent-skills catalog to find, compare, and evaluate skills before installing. Always use --fields to limit output size and --dry-run before committing to an install.
category: workflow
version: 4.1.0
---

# Browse And Evaluate

## Goal

Find the right skill for a task without flooding the context window or installing blindly.

## Guardrails

- Always use `--fields` on list/search/info to keep output small. Default: `--fields name,tier,workArea,description`.
- Always use `--dry-run` before installing anything.
- Never install more than 3 skills at once without explicit user confirmation.
- Prefer `--format json` in non-interactive pipelines. The CLI defaults to JSON when stdout is not a TTY.
- Use `--limit` when browsing large catalogs. Start with `--limit 10`.

## Workflow

1. Search or browse the catalog.

```bash
npx ai-agent-skills search <query> --fields name,tier,workArea,description --limit 10
```

2. Get details on a candidate.

```bash
npx ai-agent-skills info <skill-name> --fields name,description,tags,collections,installCommands
```

3. Preview the skill content.

```bash
npx ai-agent-skills preview <skill-name>
```

4. Dry-run the install.

```bash
npx ai-agent-skills install <skill-name> --dry-run
```

5. Install only after reviewing the dry-run output.

```bash
npx ai-agent-skills install <skill-name>
```

## Gotchas

- The `preview` command sanitizes skill content to strip prompt injection patterns. If content looks truncated, check if suspicious patterns were removed.
- Collection installs pull multiple skills. Always `--list` or `--dry-run` a collection before installing.
- Upstream (non-vendored) skills require a network fetch at install time. Use `--dry-run` to verify the source is reachable.
