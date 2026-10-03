---
name: no-comments
description: "Review Roblox Luau comments and suppressions, deleting narration while preserving non-obvious invariants, platform constraints, and authored contracts."
---

# Comment review

Review only the requested files or current diff.

1. Classify each comment as narration, stale explanation, workaround, invariant, platform constraint, security boundary, data migration note, authored-asset contract, or public API documentation.
2. Delete narration that repeats the code. Improve names, types, data shapes, or module boundaries when a comment exists only because the code is hard to follow.
3. Keep a concise comment when it explains a non-obvious reason the code cannot express, including Roblox engine behavior, ordering, replication, persistence, security, or authoring constraints.
4. Verify claims against source, repository guidance, and current Roblox behavior when the claim may have changed. Use `$how` or `$why` for uncertain constraints.
5. Treat analyzer suppressions and casts as evidence. Remove them only after the root cause is fixed and the relevant check passes.
6. Report deleted, rewritten, and retained comments with the reason for every retained exception.

Never trade a useful invariant for silence. The target is less reader work, not zero comments.
