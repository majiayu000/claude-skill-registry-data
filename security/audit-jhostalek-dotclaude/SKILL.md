---
name: audit
description: Run an explicitly selected code or UX audit, or a full fourteen-dimension sweep.
argument-hint: "[full|dimension...] [path] [review only]"
disable-model-invocation: true
---

Audit `$ARGUMENTS` using [the shared workflow](references/workflow.md). It defines scope, lens selection, evidence, corrections, and completion. Read only the selected lenses; read [integration](references/integration.md) for multiple dimensions.

Examples: `/audit security src/auth`, `/audit correctness contracts src/api review only`, `/audit ux /settings`, `/audit full`.
