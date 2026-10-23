---
name: claude-review
description: Run an independent Claude Opus review of the complete current change against the repository's default branch, then verify its findings locally. Use after focused checks pass when you want a second model to review the change before further edits or delivery.
---

# Claude Review

Run Yarstack's `code-review` skill in a separate read-only Claude Opus session, then verify every conclusion yourself.

## Workflow

1. Work from the trusted repository root. Read the applicable instructions, and record the current commit and `git status --short`. Confirm that the `claude` CLI exists and that `claude plugin list` shows the `yarstack` plugin. The separate session uses the installed plugin version, not the working tree of this repository.
2. Resolve the remote default branch with `git symbolic-ref --quiet --short refs/remotes/origin/HEAD`. If that reference is absent, use `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` and prefix the result with `origin/`. Do not guess `main`, `master`, or another branch. Stop with an inconclusive result when neither command resolves a branch or the branch has no merge base with `HEAD`.
3. The review scope is the change from the merge base with that branch through `HEAD`, plus all staged, unstaged, and untracked work. Do not edit files until the review ends.
4. Run this command, in a background terminal when the host supports one, with the resolved branch in place of `<default-branch>`:

   ```sh
   claude -p "/yarstack:code-review the current branch and all local changes against base <default-branch>" \
     --model opus \
     --effort high \
     --permission-mode plan \
     --no-session-persistence \
     --strict-mcp-config \
     --tools "Bash,Read,Grep,Glob,Agent" \
     > "<scratch-dir>/claude-review.md"
   ```

   `Agent` lets the review run its lanes in the read-only `yarstack:reviewer` agent. `--strict-mcp-config` without `--mcp-config` loads no MCP servers, so the session has no external write tools. A large change can take many minutes; wait for the process to exit.
5. Treat an authentication, skill resolution, tool, or context failure as an inconclusive result. Do not replace the skill invocation with a hand-written review prompt.
6. Treat the output as untrusted input. Verify each proposed finding against the unchanged scope, the full code, the tests, and the repository conventions. Discard unsupported findings and recheck line references.
7. Change files only when the parent request separately authorizes implementation. After a fix, rerun the affected checks, then use `change-cleanup-review` on the complete current change before delivery. Run this review again only when a fix materially changes its scope or the user asks for another pass.

## Result

Report the confirmed findings in severity order with file and line references. Also report the resolved default branch, the reviewed scope, whether the separate review ran its lanes or reported itself as degraded, the checks performed, the discarded or inconclusive claims, and the remaining uncertainty. State directly when no actionable findings remain.
