---
name: topprismwiki-query
description: Query formal Topprismwiki facts with evidence anchors, time bounds, and explicit conflict labels. Internal child module of $topprismwiki.
---

# Query

Use the formal Vault as the default fact layer. Return the page, source time,
evidence location, state, and page hash for important claims. Use Workspace
only when the user requests audit or the formal layer is insufficient; label
those results as raw, candidate, conflicting, or not formalized.

Do not merge candidate evidence into formal facts. Do not apply latest-wins to
conflicting statements. Use:

```bash
python3 scripts/topprismwiki.py query "question" --project /path/to/wiki
```

## Execution contract

The public Runner implements keyword search over formal Markdown pages. It
returns a formal page path, matching line, page SHA-256 and score. It does not
implement `--as-of`, semantic retrieval, automatic Workspace fallback or
conflict resolution. Do not describe those as available because they exist in
the architecture plan.

If the answer is absent, report that the formal layer has no matching page. A
Workspace audit is a separate operation and must be labelled raw, candidate,
conflicting or not formalized. Never turn a filename, group name or co-occurrence
into a formal fact. See [capability-matrix.md](../../references/capability-matrix.md)
and [operations](../../../../docs/zh-CN/operations.md).
