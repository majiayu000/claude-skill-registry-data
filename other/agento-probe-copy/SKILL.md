---
name: agento-probe-copy
description: "Harness-probe copy skill. When invoked as /agento-probe-copy with arguments, echo (report) the exact arguments received so the harness's non-symlinked skill resolution can be compared against the symlinked agento skill."
argument-hint: "Arguments to echo back"
user-invocable: true
disable-model-invocation: false
---

# agento-probe-copy (harness-probe)

You are a probe skill for the Agento harness-probe delivery. When you are invoked
as `/agento-probe-copy <arguments>`, report exactly what you received:

1. On one line: `agento-probe-copy skill arguments=<the exact arguments passed after /agento-probe-copy>`.
2. On one line: how you were invoked (the slash-command text, if visible to you).
