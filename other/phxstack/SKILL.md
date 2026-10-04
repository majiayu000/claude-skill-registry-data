---
name: phxstack
description: Route an Elixir web task to one phxstack workflow. Use for /phxstack, "which phxstack skill", or a task that mentions phxstack without naming a workflow. Invoked bare, lists the workflows.
---

# phxstack

Read the request and repository. Choose one workflow, run it, and stop.

| Situation | Workflow |
|---|---|
| A product idea needs pressure testing | `phxstack-roast` |
| The project lacks product context | `phxstack-interview` |
| A task, plan, or design has unresolved decisions | `phxstack-nail` |
| The task is clear but unplanned | `phxstack-plan` |
| An approved local spec needs implementing | `phxstack-build` |
| Code or a spec feels overbuilt | `phxstack-simplify` |
| A consequential decision needs independent opinions | `phxstack-counselors` |
| An implementation needs checking | `phxstack-check` |
| Docs are missing or stale | `phxstack-document` |
| A lesson should survive this session | `phxstack-learn` |
| Checked work is ready to commit and push | `phxstack-push` |
| A throwaway logic or UI prototype is explicitly requested | `prototype` |
| Primary-source research is explicitly requested | `research` |
| Test-first work is explicitly requested | `tdd` |
| A merge or rebase has conflicts | `resolving-merge-conflicts` |
| A human-only operations procedure is needed | `wizard` |

For browser UI, use the installed `impeccable` skill directly.

For long-running staged work, generated artifacts, or pipeline metadata, load
`phxstack-forward-implementation-first` alongside the active workflow. It is a
companion discipline, not a routing destination, and preserves phxstack's
approved-spec, focused-check, and push-approval checkpoints.

If no task was given, list this table. If routing remains materially unclear
after inspecting the repository, use `phxstack-nail`.
