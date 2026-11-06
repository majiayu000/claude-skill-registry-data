---
name: check
description: Validate the project's .claude/code-kit.json and show who owns what. Use after changing the config, when a path's owner or layer is unclear, or when the person asks what the kit enforces here.
---

# Check the code-kit config

From the project root:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" check
node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" unowned
```

- If `check` reports problems, fix `.claude/code-kit.json` (the lead only). Until it's valid, every write except the config itself is blocked.
- Files listed by `unowned` can't be written by anyone. Give each one an owner, or confirm with the person that it should stay frozen.
- For a particular path, run `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" who <path>...`. It shows the path's owner and layer.

Report the summary, and any problem or unowned file, in a few lines.
