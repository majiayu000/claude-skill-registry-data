---
name: add-pr-comments
description: Use when posting validated code review findings as GitHub PR line-level comments or a GitHub PR review after completing a review.
---

# Add PR Comments

Post validated code review findings from the current review as a GitHub PR review with line-level comments. Use this only after findings have been reviewed, deduplicated, and validated against the current diff.

## Procedure

1. **Resolve the PR.**
   - Run: `gh pr view --json number,headRefOid,url -q '{number: .number, sha: .headRefOid, url: .url}'`
   - Extract PR number, HEAD commit SHA, and PR URL.
   - If this fails because the current branch has no PR, ask the user for the PR number and repo.

2. **Confirm review language.**
   - If the user has not specified a language for the review comments, ask before posting.

3. **Use the final finding list.**
   - Use only findings from the completed review.
   - Each finding should include: title, severity, confidence, evidence (`file:line` or `file:startLine-endLine`), why it matters, and recommended fix.
   - If the user edited findings, use the edited set.

4. **Classify findings.**
   - Line-anchored: findings with evidence in `file:line` or `file:startLine-endLine` format.
   - General: findings without a specific file/line reference.

5. **Filter and deduplicate.**
   - Skip `low` confidence findings unless severity is `high` or `critical`.
   - Merge duplicates that point to the same file/line or same failure mode; keep the higher-severity framing.

6. **Build the GitHub review payload.**
   - Get owner/repo: `gh repo view --json nameWithOwner -q .nameWithOwner`
   - POST to `/repos/{owner}/{repo}/pulls/{pr_number}/reviews`.
   - Payload fields:
     - `commit_id`: HEAD commit SHA from step 1
     - `event`: `APPROVE` for `ready to approve`, otherwise `REQUEST_CHANGES`
     - `body`: a short, plain-language summary of how the PR looks overall — the gist you'd give a teammate, not a formal report
     - `comments`: line-anchored comments, each with:
       - `path`: relative file path from repo root
       - `line`: line number, or range end line
       - `start_line`: range start line, only for multi-line ranges
       - `side`: `RIGHT`
       - `body`: formatted finding comment

7. **Write each comment like a human reviewer, not a linter.**

   Talk to the author like a teammate. Lead with the problem in plain language, use contractions, and ask a question when you're genuinely unsure. Vary your openings — don't start every comment the same way. One or two sentences is usually enough; don't pad, and drop the rigid template and bracketed severity tags.

   - Signal severity with words, not tags: prefix `nit:` or `minor:` for small stuff; for a blocker, just say it's a blocker and why.
   - Point to a fix, but phrase it as a suggestion — "Could we...?", "Maybe pull this into...", "Worth guarding against X here?"
   - This applies in every review language (step 2): write how a person actually talks, not a stiff formal translation.

   Examples:
   - *Blocker:* "SQL injection on `name` here — it's concatenated straight into the query, so a crafted value runs arbitrary SQL. Can we switch to a parameterized query? This one's a blocker."
   - *Medium:* "`lib/date.js` already exports a `formatDate()` that does this — worth importing it instead so we don't keep two copies in sync?"
   - *Nit:* "nit: this `reduce` could just be `.flat()`."

8. **Post the review.**
   - Send the payload with `gh api ... --input <payload-file>`.
   - If there are more than 50 line-anchored comments, split them into batches of 50.

9. **Handle errors.**
   - `422`: move comments that cannot be anchored to the diff into the review body, then retry.
   - `403` or `404`: report that the `gh` token or user may lack write access.
   - If the PR HEAD SHA differs from the reviewed SHA, warn the user and ask before posting.

10. **Report the result.**
    - State the number of line comments posted.
    - State the number of general findings included in the body.
    - Provide the PR link.
    - State the review event used: `APPROVE` or `REQUEST_CHANGES`.
