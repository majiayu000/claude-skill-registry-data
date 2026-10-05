---
name: pr-comments
description: "Use when the user says 'PR comments', 'review the comments', or asks to check the current pull request's review feedback. Fetches the current PR's comments, independently assesses whether each is valid, analyzes in depth to anticipate follow-up comments, fixes the valid ones, commits, pushes, replies to each outstanding comment, and summarizes why the comments were missed."
---

# PR Comments Review

## Purpose

Review the current PR's comments, fix the valid ones, commit, push, and
reply to every outstanding comment. Do not treat every comment as
correct: assess each against the real code first. Then explain why we
missed them so the "Ready for review" process improves.

Invoking this skill is the explicit request to commit and push for this
run. It does not carry over to any other work in the session.

## Process

1. **Find the PR.** Run `gh pr view --json number,url,comments,reviews`.
   If it fails (no PR, `gh` not authenticated), stop and say what is
   missing instead of guessing.

2. **Fetch every comment**, including inline diff comments:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{number}/comments
   gh pr view {number} --comments
   ```
   Keep only outstanding comments: not resolved, not already replied
   to by us.

3. **Read the diff and surrounding code.**
   ```bash
   gh pr diff {number}
   ```
   Never judge a comment from its text alone. Open the files and
   cross-reference the lines it points at.

4. **Classify each comment** as exactly one of:
   - **Valid:** the code should change.
   - **Not valid:** the comment does not hold. Cite the code, the
     ticket, or the requirement that shows why.

5. **In-depth analysis before any edit.** For each valid comment, do
   more than the literal ask:
   1. Find the root pattern behind it (same mistake elsewhere in the
      diff, other callers, sibling files, missing tests, docs, types,
      edge cases).
   2. List the follow-up comments a reviewer would likely leave next
      after seeing this fix.
   3. Plan one fix that resolves the comment and those follow-ups.
   Do not widen scope beyond the PR's ticket. If a follow-up is out of
   scope, leave it out and mention it in the summary.

6. **Fix** the valid comments per the plan. Run the relevant tests,
   lint, and type checks and confirm they pass before committing.

7. **Commit and push** to the PR branch. One commit for the round is
   fine unless the changes are clearly separable. Never force-push
   unless the user says so.

8. **Reply to every outstanding comment** on GitHub, after the push so
   the hash exists (use `gh api .../pulls/comments/{id}/replies` for
   inline threads).

   Fixed comments, format:
   `Fixed, commit <short-hash>. <1 sentence on what changed.>`
   - Use "Updated" instead of "Fixed" when it fits better.
   - One sentence is the norm. Use a second only when it must explain
     something like the change going against the ticket.
   - Example: `Fixed, commit a1b2c3d. Removed the blank guard and
     refactored the parser so it now trims, validates, and normalizes
     in one pass.`

   Not-valid comments (pushback):
   - Tell the user which comments we are pushing back on and why.
   - Reply on the thread with the reason. No more than 2 sentences,
     polite and specific.

   For top-level review comments (no native threading), start the
   reply with the original text as a `> ` blockquote. Inline threads
   do not need the quote.

9. **Do not resolve threads.** Leave that to the reviewer.

## Output

Report to the user:

1. **Comments handled:** each comment, valid or pushback, and the
   commit hash or pushback reason.
2. **Follow-ups pre-empted:** extra fixes made beyond the literal
   comments.
3. **Why we missed these:** a bulleted summary, one bullet per
   comment or pattern, naming what check before requesting review
   would have caught it (for example "no test for the empty-list
   case", "did not check the other callers"). This feeds the "Ready
   for review" process.
4. **Replies posted:** confirmation of what was posted where.
