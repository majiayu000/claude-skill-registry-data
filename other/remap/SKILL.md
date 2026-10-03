---
description: Rebuild the architecture index after files were added, removed, renamed, or restructured. Cheap to run; run it whenever the shape of the repo changed rather than waiting to be asked.
---

# Refresh the index

```
chamnan-map
```

Run this after any change to the repo's *shape* — new module, deleted file, renamed directory, a
function moved somewhere else. Not after every edit; the index describes structure, and editing the
body of a function does not change structure.

A stale index is worse than none. It is confidently wrong, and the next session will believe it and
open the file that no longer holds what it says.

If the described-coverage percentage fell, new files arrived without an opening comment. Say which
ones. **Read `agents` from `.chamnan/config.json` (default `true`) first** — with `false`,
name the files and leave them to the user. Otherwise offer the `chamnan:commenter` agent (the
plugin-scoped name, so a second installed plugin that also ships a `commenter` cannot be
picked instead), wait for the go-ahead, and tell it which language to write in from
`language` (default `en`) — the agent writes English unless named, so bootstrap passes it
explicitly and this path must too.

`chamnan-map --undocumented` is where the full list comes from — one path per line, all of them.
The rebuild's own output names at most eight, as examples; a session that treats those eight as the
list will fix eight and report the gap as closed.
