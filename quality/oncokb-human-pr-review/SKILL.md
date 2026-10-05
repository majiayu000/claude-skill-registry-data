---
name: oncokb-human-pr-review
description: Guide an interactive human PR review by summarizing changes and linked issues, checking reviewer understanding with a quiz, and posting reviewer-approved PR comments.
---

## Scope

- Use when a user wants guided, interactive support while they review a pull request.
- This skill coaches reviewer understanding first; it is not a replacement for direct code changes.
- Post PR comments only when the user explicitly asks you to post them.
- Every PR comment created by this workflow must start with `[AI-assisted]`.

## Core interaction rules

- Ask for the PR link first.
- Use `gh` for GitHub PR and issue inspection.
- Keep interaction conversational and checkpointed: summarize, quiz, confirm understanding, then proceed.
- If this is not the reviewer's first pass on the PR, check unresolved prior review comments and report what is still open.
- If this is not the reviewer's first pass on the PR, highlight what changed since that reviewer's last review activity.
- If the reviewer is confused, propose specific comment text and ask for approval before posting.
- Never post comments preemptively.

## Workflow

1. Collect the PR link.
   - Ask the user for the PR URL they are reviewing.
   - If missing, stop and request it before doing anything else.
   - Completion criterion: PR URL is provided and valid.

2. Summarize the PR and linked issues.
   - Inspect PR title, description, changed files, and commit summary.
   - Identify linked issues in the PR body (for example `Fixes #...`, `Closes #...`, `Refs #...`, or issue URLs).
   - For each relevant linked issue, summarize problem, expected outcome, and why this PR addresses it.
   - Provide a reviewer-focused summary:
     - what changed
     - where data flow changed
     - why the implementation is structured this way
     - notable risks or assumptions
   - Completion criterion: reviewer gets a concise PR + issue context summary that can stand alone.

3. If this is a follow-up review, inspect prior review state.
   - Determine whether this is the logged-in reviewer's first review pass on the PR.
   - If not first pass, inspect prior review comments and threads.
   - Identify unresolved comments and clearly point them out to the reviewer.
   - Summarize code changes made since the logged-in reviewer's last review (new commits, updated files, and affected behavior/data flow).
   - Completion criterion: reviewer sees both unresolved prior feedback and a clear delta since their last review.

4. Quiz reviewer understanding.
   - Ask targeted questions that check understanding of:
     - data flow before vs after this change
     - key control points and failure paths
     - rationale for the chosen approach vs alternatives
   - Use at least 3 concrete questions tied to this PR.
   - Evaluate responses for confidence and correctness.
   - Completion criterion: either reviewer demonstrates understanding, or specific confusion areas are identified.

5. Handle confusion with optional PR comments.
   - If confusion is identified, explain the confusing area in plain language first.
   - Ask whether the user wants to post clarification comments on the PR.
   - You may recommend comment text, but always ask before posting.
   - If approved, post comments that begin with `[AI-assisted]` and clearly request the missing explanation.
   - Completion criterion: either understanding is restored, or approved `[AI-assisted]` clarification comments are posted.

6. Run and explore locally.
   - Ask the reviewer to run the code locally.
   - Provide a checklist of concrete interactions to validate behavior and data flow.
   - Tailor checklist items to changed files and issue intent.
   - Completion criterion: reviewer has a local validation checklist aligned to PR risk.

7. Invite follow-up questions and optional comment requests.
   - Tell the user to ask questions about any code path they do not understand.
   - If they remain unsure about part of the code, ask if they want you to add a PR comment.
   - Recommend a comment when useful, but wait for explicit approval before posting.
   - Any posted comment must start with `[AI-assisted]`.
   - Completion criterion: unresolved confusion is either clarified directly or turned into approved PR comments.

## Comment style for this skill

- Start every posted PR comment with `[AI-assisted]`.
- Keep comments specific and actionable.
- Focus on missing context, unclear data flow, hidden assumptions, or unclear rationale.
- Prefer one concrete request per comment.

## Output requirements

- Report back to the user with:
  - PR URL reviewed
  - key change summary
  - linked issues summary and relevance
  - unresolved prior review comments (for non-first-pass reviews)
  - changes since the logged-in reviewer's last review activity (for non-first-pass reviews)
  - quiz questions asked and understanding gaps found
  - any proposed comments and whether they were posted
  - local run checklist provided

## Quality bar

- Do not skip the quiz step.
- Do not skip unresolved-comment and since-last-review checks for non-first-pass reviews.
- Do not post any PR comment without explicit user approval.
- Do not post comments without the `[AI-assisted]` prefix.
- Keep recommendations grounded in PR diff and linked issue context.
