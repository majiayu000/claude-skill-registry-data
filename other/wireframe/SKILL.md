---
name: wireframe
description: Alias for Visual Stack's review tool, which used to be called wireframe. Builds a UI wireframe and opens it in an interactive review workspace, or reviews an app that is already running. Use only when the user invokes /vstack:wireframe or $vstack:wireframe.
---

The wireframe tool is now `/vstack:review`. Nothing else changed — same workspace, same loop,
same on-disk state.

Read `../review/SKILL.md` completely, load the host adapter it requires, and follow that workflow
for the user's request. Treat this as a direct invocation of the review skill. Do not mention the
rename unless the user asks.
