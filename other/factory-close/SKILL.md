---
name: factory-close
description: Close out a Linear issue — move to Done, add a closing comment, and clean up the local branch/worktree
argument-hint: <issue-id> (optional — auto-detected from branch if omitted)
---

You're finishing a ticket. This command:
1. Drafts a closing comment summarizing what shipped
2. Moves the Linear issue to `Done`
3. Cleans up the local branch and worktree

It does **not** merge a PR or push code — that's expected to have happened already.

**Invocation input:** an optional issue identifier. If omitted, auto-detect it from the current branch name.

## What to do

1. **Read project configuration.** Prefer `.factory-kit/linear.json`; use legacy `.claude/linear.json` only as a migration fallback. If neither exists, stop and direct the user to setup-linear. Pull `teamKey` and `states.done` (default `"Done"`).

2. **Resolve the issue ID** the same way `/submit` does:
   - Argument provided → normalize (prepend `<teamKey>-` if numeric).
   - Otherwise → parse current branch (`git rev-parse --abbrev-ref HEAD`) for `<teamKey>-<num>` (case-insensitive).
   - If nothing matches, ask the user.

3. **Pre-flight checks.** Run these in parallel, surface what they show, and **gate on user confirmation before mutating anything**:
   - `git status` — any uncommitted changes? If yes, warn and ask before proceeding.
   - `git log <main-or-default>..HEAD --oneline` — commits since divergence. Use this for the closing comment.
   - `git diff --stat <main-or-default>...HEAD` — top-level files touched.
   - Linked PR state if discoverable (inspect Linear issue attachments through the connected integration, or run `gh pr list --head <branch>`). If a PR exists and isn't merged, warn — close is normally a post-merge action.

4. **Draft the closing comment** (≤ 150 words) in the `factory-voice.md` shape — bold labels, short sentences, omit empty sections. The closing comment is the densest node in the decision graph for this issue; link liberally.

   ```
   **Outcome:** <one or two lines on what shipped — not a diff dump>
   **Why:** <the underlying constraint or principle the work satisfied>
   **Tradeoff:** <non-obvious tradeoffs worth recording — omit if the diff is self-explanatory>
   **Open:** <deferred work or follow-ups; file each as its own issue if substantial and link the IDs here>
   **Refs:** <PR # / merge commit SHA / related issue IDs / customer feedback URL if this resolved a customer ask>
   ```

   The reader is someone scanning the issue six months from now to understand *why* this exists. Skip the play-by-play; record the load-bearing decisions. If a follow-up was punted, prefer "filed as `<KEY-N>`" over "TBD" — convert open questions into graph nodes.

5. **Show the draft and ask for approval.** The user can edit tone or pull anything sensitive before it lands in Linear.

6. **On approval, in this order:**
   - Post the comment through the Linear integration with the issue ID and body.
   - Move the issue to Done through the Linear integration, using the configured `done` value. Resolve a state UUID by listing team statuses if names aren't accepted.

7. **Clean up local state.** Confirm once more before any branch-deletion step — destructive operations aren't pre-authorized.
   - If the current directory is a worktree (`git rev-parse --show-toplevel` differs from the main repo root), use the host's worktree-exit capability when available; otherwise use safe git worktree commands matching the user's confirmed merge-or-discard choice.
   - Otherwise: `git checkout main` (or the project's default branch) then `git branch -d <branch>`. Use `-D` only if `-d` refuses and the user explicitly approves (work is unmerged, confirm intent).

8. **Confirm completion.** Print: `<KEY-N> closed. Branch deleted. Worktree exited (if applicable).`

## Style

Follow `factory-voice.md`. Three gates: pre-flight review → closing comment approval → branch deletion confirmation. Don't skip any. The closing comment is the historical record — future readers will judge whether to revisit this decision based on what you write. Name principles, not symptoms. If the issue is already `Done`, still offer the cleanup steps (sometimes Linear gets updated before the branch does).
