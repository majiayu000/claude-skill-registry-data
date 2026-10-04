---
name: recall
description: Harmonia recall - surface relevant past learnings for the current repo mid-session. Use ONLY when explicitly invoked as /harmonia:recall.
disable-model-invocation: true
---

Run the recall script and surface the summaries it returns:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/bin/memory/recall.sh
```

Forward `--repo <path>` and `--budget-lines <n>` when the developer asks to widen or narrow the pull; otherwise the defaults apply. The script is the single source of truth: it filters the global tier by language-tag overlap with the repo, keeps project-tier and legacy `docs/solutions/` entries unfiltered as always relevant to their own repo, and returns what is left newest-first under a line budget. This wraps the same script the session-start hook and roster agents call directly, so it is a convenience over that mechanism, not a separate one; do not fork its logic.
