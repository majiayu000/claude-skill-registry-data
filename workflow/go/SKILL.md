---
name: go
description: Compatibility entry for Visual Stack's former /vstack:go command. Runs the wireframe and UI review tool, now called review. Use only when the user invokes /vstack:go.
---

Visual Stack is the wireframe and UI review tool. This legacy entry no longer inspects pipeline state
or routes to other workflow stages.

Read `../../skills/review/SKILL.md` completely, load the host adapter it requires, and follow that workflow
for the user's request. Treat this as a direct invocation of the review skill. If the request does
not yet name a screen or running UI, ask only for the minimum information that the review skill
cannot infer.
