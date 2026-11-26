---
name: graphify
description: Query the graphify knowledge graph before reading files. Trigger /graphify.
---

[FILE] graphify skill
[OBJ] Knowledge graph exploration.
[TRIGGER] `/graphify`
[RULES]
1. [REQ] If `graphify-out/graph.json` exists, use graphify before raw grep/read.
2. [CMD] `graphify query "<question>"` — get scoped subgraph.
3. [CMD] `graphify path "<A>" "<B>"` — dependency path.
4. [CMD] `graphify explain "<concept>"` — related concepts.
5. [CMD] `graphify update .` after code edits.
