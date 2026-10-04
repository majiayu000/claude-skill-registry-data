---
name: status
description: Harmonia status - a read-only readout of the active task's stage, markers, and receipts. Use ONLY when explicitly invoked as /harmonia:status.
disable-model-invocation: true
---

This is a read-only readout: it writes nothing - no marker, no receipt, no workspace file.

1. Resolve the active task:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/bin/workspace.sh resolve --repo .
```

   Surface resolve's own message and stop on its non-zero exits (exit 2 ambiguous active tasks; exit 3 no active task).

2. From the resolved workspace dir (`.harmonia/tasks/<id>/`), report:
   - the active task id;
   - its lifecycle stage, derived by reading the artifact contract in `${CLAUDE_PLUGIN_ROOT}/core/lifecycle.yaml` as data and matching which stage-boundary out-artifacts are present - do not hardcode a stage table;
   - which markers and receipts are set: `scope.md`, `design.md`, `boundary.md`, `diff-summary.md`, `verdict.md`, `accepted`, `rejected`, `done`, `abandoned`, and the `receipts/` contents (`check-criteria.json`, `criteria-run.json`).

Report only what is on disk. It composes existing mechanisms into a readout and adds no new script.
