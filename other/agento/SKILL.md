---
name: agento
description: "Harness-probe router skill. When invoked as /agento with arguments, echo (report) the exact arguments received so the harness's skill argument resolution can be observed, including through a symlink."
argument-hint: "Arguments to echo back"
user-invocable: true
disable-model-invocation: false
---

# agento (harness-probe)

You are a probe skill for the Agento harness-probe delivery. When you are invoked
as `/agento <arguments>`, report exactly what you received:

1. On one line: `agento skill arguments=<the exact arguments passed after /agento>`.
2. On one line: how you were invoked (the slash-command text, if visible to you).
3. On one line: the location this skill loaded from, if visible to you (for
   example a path ending in `skills/agento`).
