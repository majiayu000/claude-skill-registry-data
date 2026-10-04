---
name: project-next-action
description: Use when a Research Pilot project needs a read-only recommendation for the next workflow action.
argument-hint: "<project>"
---

# Project Next Action

Status: **transition**. Keep as a read-only advanced router. Do not expand this
as the core product surface; project understanding should be observed through
dashboard read models and discussed in chat.

Recommend next workflow:

```bash
python3 "$PLUGIN_ROOT/tools/project_next_action_cli.py" suggest --repo "$WORKSPACE_PATH" --project "$PROJECT_ID" --json
```

This router may recommend human gate review, gap inspection, paper search, warrant cleanup, translation cleanup, or experiment proposal.

It must not run search, deep read, delta apply, Zotero writes, or experiments.
