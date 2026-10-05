---
name: oncokb-verify-comments-are-addressed
description: Verify whether pull request review comments are addressed, then guide the PR author through code fixes or prefixed replies for unresolved comments.
---

## Scope

- Use when the user wants help checking whether PR review comments were addressed.
- Start from a PR URL and review the full comment state (open, outdated, resolved, and unresolved threads).
- Support PR authors only.
- Post PR comments or replies only when the user explicitly asks to post them.
- Every comment or reply posted by this workflow must start with `[AI-assisted]`.

## Core interaction rules

- Ask for the PR link first.
- Confirm the user is the PR author before analysis.
- Use `gh` for GitHub PR and review-thread inspection.
- For each unresolved concern, offer two paths:
  - address the code issue
  - reply for clarification or explain why it cannot be addressed now
- Never post unapproved comments.

## Workflow

1. Collect PR URL.
   - Ask the user for the PR URL.
   - If missing, stop and request it.
   - Completion criterion: valid PR URL is provided.

2. Confirm PR author role.
   - Ask whether the user is the PR author.
   - If the user is not the author, stop and tell them this skill is author-only.
   - Completion criterion: user explicitly confirms they are the PR author.

3. Inspect PR comments and review threads.
   - Read issue comments, review comments, and review-thread status from GitHub.
   - Identify each actionable reviewer concern and classify as:
     - addressed in code
     - addressed by existing reply
     - not yet addressed
     - unclear (needs clarification)
   - For code-addressed comments, verify diff evidence where possible.
   - Completion criterion: each actionable comment has a clear status with supporting evidence.

4. Report unresolved or unclear items.
   - Summarize all comments that are not clearly addressed.
   - For each item, propose next action:
     - code change recommendation, or
     - reply recommendation requesting clarification / explaining constraints
   - Completion criterion: user has an actionable per-comment plan.

5. Execute user-chosen follow-up per unresolved comment.
   - If user chooses code fix, guide or implement the change and re-check whether the original concern is now addressed.
   - If user chooses reply, draft a concise response.
   - If user approves posting, publish the response with `[AI-assisted]` at the start.
   - Completion criterion: each unresolved comment is either addressed by code, answered with an approved prefixed reply, or explicitly deferred with rationale.

6. Final verification pass.
   - Re-scan comment threads after changes/replies.
   - Report remaining unresolved items, if any, with exact next actions.
   - Completion criterion: user has a final addressed/unaddressed ledger and knows what remains.

## Comment format requirements

- Prefix every posted PR comment or reply with `[AI-assisted]`.
- Keep replies specific, respectful, and tied to the original reviewer concern.
- If clarification is requested, ask one concrete question per reply.
- If deferring, include reason and planned follow-up.

## Output requirements

- Report back with:
  - PR URL checked
  - author confirmation
  - total actionable comments reviewed
  - per-comment status (`addressed`, `replied`, `unaddressed`, `needs clarification`, `deferred`)
  - comments/replies drafted and whether they were posted
  - any remaining blockers and next actions

## Quality bar

- Do not claim a comment is addressed without evidence from code or thread replies.
- Do not post comments without explicit user approval.
- Do not post any comment/reply without the `[AI-assisted]` prefix.
- Keep status tracking exhaustive: every actionable comment must be accounted for.
