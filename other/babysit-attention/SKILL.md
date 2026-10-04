---
name: babysit-attention
description: Resolve a paused PR supervisor decision with explicit human input.
argument-hint: <pr-number> <reason>
user-invocable: true
disable-model-invocation: true
---

This window was opened by the persistent babysit supervisor because automated progress is
ambiguous, its retry cap was reached, or the PR's branch conflicts with its base. Read the
supervisor state, summarize the exact PR, SHA, failing checks, and attempt count, then ask
the user to choose whether to retry with a fresh budget, leave it paused for manual repair,
or stop babysitting. Use the active client's native input mechanism. Never mutate GitHub,
push, or restart automatically before that choice.

When the reason is a merge conflict (`mergeStateStatus` is `DIRTY`), summarize the PR and
head SHA, then offer only "leave paused" or "stop babysitting" — a fresh retry budget does
not apply to a conflict, and resolving it needs a manual rebase, so point the user at
`/cenci:sync`. The supervisor keeps polling on its own and clears this hold automatically
once a rebase is pushed; no separate re-arm step is needed.
