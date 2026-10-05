---
name: review
description: Code-review workflow for verified issues in specific files, functions, diffs, or code sections. Use whenever a review is requested, whether by the user or by another agent. Report findings; the requester decides what to do with them.
metadata:
  website: "https://photostructure.com/coding/claude-code-review/"
---

# Code Review

Read and follow [`references/single-pass.md`](./references/single-pass.md), then
review the scope you were given.

## Scratch files

Any copy this workflow makes — of the repo, of a build-output directory, of a
file you replay edits onto — belongs in the operating system's temporary
directory, in a fresh directory named for the project and the purpose. Never
inside the checkout, and never under a home directory.

Delete it before you finish. A repo or build-output copy runs to gigabytes,
nothing reaps a home directory, and the out-of-disk failure that eventually
follows surfaces somewhere unrelated — a test suite that hangs, a build that
dies mid-link — costing far more to diagnose than the copy ever saved.

## Adapting for your project

- **Name your standards explicitly** in
  [`references/single-pass.md`](./references/single-pass.md) — `AGENTS.md`,
  optional `CLAUDE.md`, `docs/DESIGN-PRINCIPLES.md` — in place of the generic
  "relevant design documents".
- **Add project-specific "what to look for" items** to the same file, e.g. "new
  public APIs have rate limiting", "DB queries use parameterized inputs", "error
  messages don't leak internal paths".
- **Tune the exclusion list** there if your team *does* want style or refactor
  feedback. The default is strict because noise is the bigger problem.
