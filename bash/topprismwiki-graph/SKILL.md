---
name: topprismwiki-graph
description: Inspect formal REL edges and an explicitly separate candidate relationship overlay. Internal child module of $topprismwiki.
---

# Graph

Formal `REL` edges are the primary graph and must be supported by typed direct
evidence. Candidate edges are a separate Workspace projection with
`state: candidate`; they never affect formal graph metrics and never trigger
automatic cross-links.

```bash
python3 scripts/topprismwiki.py graph "entity" --include-candidates --project /path/to/wiki
```

## Execution contract

The built-in parser recognizes the documented Markdown form
`- [[target]] · relation` and returns `source`, `target`, `relation` and
`state: formal`. Candidate edges are read from the private
`workspace/state/candidates.json` projection only when
`--include-candidates` is supplied.

Candidate edges never affect formal graph metrics, trigger automatic cross-links
or become RELs without direct typed evidence and governance review. The current
Runner does not prove reverse-edge consistency or namespace correctness; mark
those checks as external validation. If an entity is absent, report no formal
edge rather than creating one from co-occurrence. See the
[capability matrix](../../references/capability-matrix.md).
