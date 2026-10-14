---
name: matt-implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

> Originally written by Matt Pocock and redistributed under the MIT License.
> See [UPSTREAM.md](UPSTREAM.md) for provenance and local modifications.

Implement the work described by the user in the spec or tickets.

Where possible, at pre-agreed seams, load and follow the `tdd` skill using the current harness's native skill mechanism.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, load and follow the `code-review` skill using the current harness's native skill mechanism to review the work.

Commit your work to the current branch.
