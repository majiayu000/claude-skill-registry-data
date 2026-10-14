---
name: ship
description: Run the full verification pyramid, confirm /review has no blocking pending findings, and open a pull request. Use as the final step of the pipeline, never to bypass /review.
user-invocable: true
---

1. Run `scripts/verify.sh` (full pyramid, no flags). It must exit 0. If it doesn't, stop —
   do not open a PR against a red suite.
2. Confirm `/review` has run for the current diff and has no unresolved CONFIRMED
   high-severity or critical/serious a11y finding. If `/review` hasn't run yet, run it first.
3. Open a pull request (via `gh pr create` or the host's equivalent) summarizing the feature,
   linking `specs/<feature>/spec.md`.
4. Stop (GATE humano) — merging is a human decision, this skill never merges on its own.
