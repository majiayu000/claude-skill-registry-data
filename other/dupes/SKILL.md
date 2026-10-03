---
name: dupes
description: Semantic near-duplicate articles, capabilities, or functionalities via embedding cosine similarity. Surface candidates, then offer merge/keep/delete inline.
allowed-tools:
  - "mcp__bigweld__find_dupes"
  - "mcp__bigweld__delete_node"
---

# /dupes [label]

Call `find_dupes(label)` for the requested label (default "Article" if unspecified; ask Alex if he wants Capability or Functionality dupes too). Present pairs ranked by similarity score. For each pair Alex flags as a real dupe, propose `delete_node()` for the loser with `confirmed=False` first to show the diff, then `confirmed=True` after his nod. Skip pairs he wants to keep.
