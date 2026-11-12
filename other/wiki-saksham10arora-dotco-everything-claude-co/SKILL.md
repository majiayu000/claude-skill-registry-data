---
name: wiki
description: Use when the user says "wiki", "compile inbox", "update wiki", "knowledge base", "process inbox", or "add to wiki"
---

# /wiki: compile the inbox into a linked knowledge base (Karpathy's LLM-wiki pattern)

1. List `inbox/`. If empty, say so and stop.
2. Read `wiki/_index.md` for existing articles.
3. For each inbox file: read it, decide its topic, then update the matching `wiki/<slug>.md` or create one:

```
# <Topic>
## Summary
2-3 dense sentences, tied to the user's goals in hot.md.
## Key concepts
- **Concept**: one line each
## How it connects to my work
## Related
[[slug]] | [[slug]]
## Sources
---
*Last updated: YYYY-MM-DD*
```

4. Add a backlink to the new article from every existing article that should reference it.
5. Rewrite `wiki/_index.md`: `- [[slug]]: one-line description`, alphabetical, with a "Last compiled" date.
6. Move processed files to `archive/raw/YYYY-MM-DD-<name>`.
7. Report: files processed, articles created or updated, backlinks added, anything surprising.
