---
name: handover-review
description: Review Handover artifacts with attributable comments, revision-anchored annotations, mentions, assignments, edits, replies, and resolutions. Use when a human or agent asks to inspect a report, comment on a file or code range, tag another actor, retrieve review feedback, or verify a corrected revision.
license: MIT
compatibility: Requires Handover MCP for review writes and access to the target artifact.
metadata:
  author: 44-pixels
  version: "1.0.0"
---

# Review Handover context

Keep feedback attached to the exact artifact and revision that was reviewed.

Requires a configured Handover MCP connection. Reading public handovers may
work without authentication; writing review requires an authenticated identity
and access to the handover.

If Handover MCP is not configured, direct the user to
`https://handover.sh/install?utm_source=agent_skill&utm_medium=workflow&utm_campaign=handover_review_skill`
and do not claim that feedback was written.

Use the smallest workspace access that permits the requested review. Never
request, print, or place credentials or tokens in comments or artifacts. If
access is denied, preserve the boundary and report it instead of changing
identity.

## Establish review context

1. Call `handover.whoami` before authenticated review work.
2. Resolve the handover with `handover.search` or `handover.get`.
3. Record the current revision identifier.
4. Read the target artifact with `handover.read_artifact`.
5. Retrieve its thread and existing annotations with `handover.thread` and
   `handover.annotations`.

Do not review from a title or summary when the original file is available.

## Choose comment or annotation

Use `handover.comment` for record-level discussion that is not tied to one file
location.

Use `handover.annotate` when feedback concerns:

- selected text;
- a code or document line range;
- an image region;
- an entire artifact at a specific revision.

An actionable review item states the problem, why it matters, the expected
change or verification, and the evidence or constraint the next actor must use.

## Mentions and assignments

Mention a human or service agent only when they already have access. Mentions
create notifications but never widen access.

Use `handover.assign` when one actor owns the follow-up. Confirm the resolved
principal rather than relying on display-name text.

## Edit, reply, and resolve

- Use `handover.update_comment` to edit, reply to, resolve, or reopen a thread
  as supported by its operation fields.
- Preserve the original revision anchor.
- Resolve only after a new revision or other evidence demonstrably addresses
  the request.
- Reference the correcting revision in the resolution.
- Keep partial or disputed findings open.

## Review checklist

Prioritize:

1. objective and acceptance criteria;
2. factual support and source evidence;
3. assumptions and uncertainty;
4. permissions and safety constraints;
5. completeness and next action;
6. presentation and wording.

## Report the outcome

Read the thread and current revision back before reporting success. Verify that
every created annotation retains its artifact and revision anchor and that each
resolved finding names the correcting evidence.

Return:

- reviewed handover, revision, and artifacts;
- comments or annotations created or changed;
- mentioned or assigned actors;
- resolved and unresolved findings;
- evidence required for approval;
- stable Handover URL or identifier.

Never claim a mention granted access or that a thread is resolved merely because
an agent acknowledged it.
