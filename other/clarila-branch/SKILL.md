---
name: clarila-branch
description: "Find, prepare or inspect the Git branch/worktree associated with one issue. Use for issue workspace ownership and placement, not automatic cleanup or a competing checkout."
---

# Resolve one owned workspace

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Verify the full repository/issue identity, Git common directory, branch, existing worktrees and any active session. Discover prior work by identity rather than title or branch spelling.
2. Reuse a matching registered or harness-provided worktree. Never nest worktrees or relocate an active checkout.
3. For a requested new workspace, fetch the intended remote base and create a real Git worktree beneath /Users/dimmasyusuf/Developer/.worktrees/<project>/<workspace>. Inspect repository-specific base policy before choosing the ref.
4. Register actual path, branch, common repository and source head. Use existing work helpers for mechanical operations while preserving their authority and safety checks.
5. Clean up only when explicitly requested and after checking dirty/unpushed work, linked sessions and ownership. Never reset or discard unrelated changes.

## Verify the checkout association

Prefer the host's native worktree capability when preparing new isolation. Inspect existing linked-worktree and superproject/submodule identity before choosing a location. Compare the verified remote repository, issue metadata and common Git directory when titles or branch names disagree.

After any authorized creation or reuse, read back the actual path, branch, full HEAD and base used. Retain preexisting dirty/unpushed state and the observed owner in the handoff. If ownership is unknown, continue repository/base inspection and name the exact association that must be resolved before another writer can start.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record.

## Deliverable

Return verified repository/worktree/branch/head and ownership, or the exact conflicting workspace.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.

Read the [operation-specific reference](references/worktrees.md) when performing this responsibility.

For mechanical issue setup, list, sync and requested cleanup, read the [local issue workflow](../clarila/local-workflow/guide.md) and use its scripts with the central worktree-root override. Preserve legacy/native worktrees in place.
