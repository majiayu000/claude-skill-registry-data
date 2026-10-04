---
name: resolving-merge-conflicts
description: Use when resolving an in-progress Git merge, rebase, or cherry-pick conflict.
---

# Resolving Merge Conflicts

1. Inspect the exact Git operation, current status, conflict stages, and surrounding history. Do not assume every conflict has the same source branch or intended result.

2. Recover both intents from the conflicting commits, current code, tests, issue or pull request context, and project rules. Treat commit messages as leads rather than complete specifications.

3. Resolve each hunk at the owning seam. Preserve compatible intent. When the intents conflict, follow the stated goal and record the tradeoff. Do not add unrelated behavior during conflict resolution.

4. Run the smallest checks that exercise the resolved paths, then the project checks required for the operation. Inspect the resulting diff for dropped work and conflict markers.

5. Continue, abort, stage, or commit only when the current request and Git operation authorize that action. Never stage unrelated files. If the right resolution requires a product or architecture choice, stop before finalizing and present that decision with the evidence.

Report the resolved files, checks run, unresolved choices, and the exact Git state. Do not claim the merge or rebase is complete until Git confirms it.
