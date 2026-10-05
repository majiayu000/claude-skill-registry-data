---
name: topprismwiki-context
description: Build a bounded, evidence-traceable task context from formal Topprismwiki facts and relationships. Internal child module of $topprismwiki.
---

# Context

Create a Workspace projection containing only task-relevant facts, decisions,
timeline, formal relationships, conflicts, and evidence gaps. Do not dump raw
documents or expose secrets. Enforce the token budget and state when content
was truncated.

```bash
python3 scripts/topprismwiki.py context "task" --budget 6000 --project /path/to/wiki
```

The current `--budget` is a character limit used by the reference Runner, not a
token counter. The output is a Workspace artifact containing formal page paths
and hashes; it does not copy raw documents or evidence. If the limit is reached,
the artifact must retain its truncation marker and the response must tell the
user to increase the budget.

Do not add Workspace candidates, unverified relationships, secrets or private
raw content to a context package. For a task that needs source verification,
route to the relevant source child module first. See
[capability-matrix.md](../../references/capability-matrix.md).
