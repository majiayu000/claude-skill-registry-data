---
name: implement-ticket
description: Implement a JIRA ticket end-to-end, review it with Claude and Codex until clean, and split it into local stacked PR branches. Use when asked to implement or complete a ticket.
argument-hint: <ticket-id>
---

# Implement JIRA Ticket

1. Read the JIRA ticket the user specified, treating any suggested implementation as a hint. Complete the ticket with tests in a worktree from the default branch. Run all later steps there.
2. Split the work into a series of atomic commits. Ensure the commit subject is 50 characters or fewer, uses imperative mood, and follows the conventional commit style with no scope, body, or trailer. Describe the change, not a file list.
3. Cross-check the implementation with both Claude **and** Codex using parallel subagents, running a code review and a security review in each, with appropriate skills if available. The other agent may be found with `command -v $t || find ~/.vscode*/extensions -type f -name $t -perm -u+x 2>/dev/null | sort -V | tail -1`; stop if it is unavailable. Verify each finding and discard false positives. Fix all confirmed high and medium findings. Fix a low finding only if the fix is small and local and doesn't change behavior or design. Fold each fix into the commit it belongs to. Repeat until a pass returns no new high or medium findings.
4. Split the commits into a stack of local PR branches, but do not push. Split only between commits, and keep each branch's diff against its parent under 500 changed lines (additions plus deletions, tests included). Each branch must pass lint and tests on its own.
5. Run `/commit-pr` on each branch diffed against its parent and report the results.
