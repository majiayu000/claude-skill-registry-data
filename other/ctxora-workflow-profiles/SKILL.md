---
name: ctxora-workflow-profiles
description: Start from an ECC skill profile in CTXORA, preview its modules and skills, then add or remove modules or individual skills before installation.
---

# CTXORA Workflow Profiles

Skill profiles are independent from MCP client install profiles such as `codex` or `cursor`.

Inspect the available starting profiles:

```bash
npx ctxora skills profiles --workspace .
```

Preview before writing. Start with `developer` for general application work, `security` or `research` for focused work, and `full` only when broad discovery is worth the larger installed surface.

```bash
npx ctxora skills preview --workspace . --profile developer
npx ctxora skills preview --workspace . --profile developer \
  --add-module security --remove-skill security-scan
npx ctxora skills install --workspace . --profile developer \
  --add-module security --remove-skill security-scan
```

The default output is `.agents/skills`; use `--output` for another host-specific skill directory. Existing modified skills cause a conflict unless `--force` is explicit. Use `--prune` to remove previously CTXORA-installed skills that are no longer selected; modified files are preserved as conflicts.

Installing a skill copies guidance and bundled resources only. It does not execute ECC scripts, enable hooks, install external dependencies, or grant permissions.

The active profile becomes the router candidate boundary. `route_skills` selects a small relevant subset per task; choosing a profile does not load every included skill.
