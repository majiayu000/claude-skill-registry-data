---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

For one ticket, work in the current checkout only when it is owned by this session. For a dependency-aware multi-ticket build, the parent computes the ready frontier and dispatches each independent ticket to a fresh `ticket-worker` with `worktree: true`. Never run two writers in one checkout.

Load and follow the `tdd` skill where possible, at pre-agreed seams. Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, load and follow the `code-review` skill. Standards and Spec reviewers must be separate fresh contexts. Inside a ticket-worker, they must use `worktree: false` and inherit the worker cwd so they review the actual implementation, not a clean checkout.

The owning worker commits its ticket and returns the supported pi-subagents handoff metadata. The parent integrates worker commits sequentially, resolves conflicts by intent, and owns tracker state and combined verification.
