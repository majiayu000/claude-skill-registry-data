---
name: rust-rebuild
description: "Modify Allbert in an isolated rebuild worktree, run Tier A validation, and produce an operator-reviewed patch."
intents: meta
allowed-tools: process_exec read_file write_file
---

# Rust Rebuild

Use this skill only when the operator explicitly asks Allbert to change its own Rust source.

## Safety Contract

- Never edit the source checkout directly.
- Never edit `skills/rust-rebuild/` in the source checkout.
- Work only inside the active self-improvement worktree.
- Run the Tier A validation chain before proposing a patch.
- Treat failures as `needs-review`, not as permission to bypass review.
- Produce a concise summary plus the patch artifact path; do not inline large diffs in chat.

## Operating Ritual

1. Confirm that `allbert-cli self-improvement config show` resolves a source checkout and reports a pinned Rust toolchain.
2. Use the kernel-created worktree path from the self-improvement workflow.
3. Inspect files with `read_file` and make edits with `write_file` only inside that worktree.
4. Use `process_exec` inside the worktree for validation commands.
5. If validation fails, capture the failing command and the relevant output tail.
6. Hand the operator a patch summary and next-step hint for approval.

The rebuild output is a review artifact, not an install action. The operator must explicitly approve and install any patch in a later step.
