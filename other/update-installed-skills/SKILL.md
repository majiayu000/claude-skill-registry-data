---
name: update-installed-skills
description: Use when syncing or updating previously installed skills to their latest version. Always dry-run updates before applying, and check for breaking changes.
category: workflow
version: 4.1.0
---

# Update Installed Skills

## Goal

Keep installed skills current without breaking the agent's workflow or silently overwriting local customizations.

## Guardrails

- Always use `--dry-run` before running a real update.
- Check what is currently installed before updating: `npx ai-agent-skills list --installed`.
- Never update all skills at once in production without reviewing the dry-run output.
- Use `--format json` to capture structured update results for logging.

## Workflow

1. List currently installed skills.

```bash
npx ai-agent-skills list --installed --format json --fields name
```

2. Check for available updates.

```bash
npx ai-agent-skills check
```

3. Dry-run the update.

```bash
npx ai-agent-skills sync <skill-name> --dry-run
```

4. Apply the update after reviewing.

```bash
npx ai-agent-skills sync <skill-name>
```

5. For bulk updates, review each skill's dry-run output.

```bash
npx ai-agent-skills sync --all --dry-run
```

## Gotchas

- Skills installed from GitHub will attempt a fresh clone during sync. If the upstream repo is gone, the update will fail gracefully.
- Manually edited SKILL.md files will be overwritten by sync. Back up customizations before syncing.
- The `check` command makes network requests to verify upstream sources. It may be slow or fail if sources are unreachable.
