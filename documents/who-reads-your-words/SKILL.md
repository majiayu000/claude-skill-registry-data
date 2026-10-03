---
name: who-reads-your-words
description: Shape text intended for people outside the current work process around its actual audience, channel, and genre, preventing task instructions, revision chatter, and agent actions from leaking into the artifact. Use for documentation, PRs, issues, commits, reports, email, announcements, support replies, proposals, UI copy, and other outward-facing writing.
license: MIT
---

# Who Reads Your Words

Write for the people who will receive the words, not for the process that produced them.

## Establish the audience contract

Infer these fields before drafting. Ask only when an unresolved field would materially change the result:

- intended reader or readers
- channel and artifact type
- reader goal and desired action
- context the reader can reasonably possess
- temporal view: current state, change, decision, or direct conversation
- authoritative sources and disclosure boundary

Keep this contract internal. Read [references/audience-contracts.md](references/audience-contracts.md) only when the mode or treatment of history is unclear.

## Separate control from content

Treat task instructions, corrections, rejected proposals, tool activity, and editing history as control information. They select and shape the output but are not automatically content.

Materialize an audience view from verified subject facts and the selected genre. Superseded ideas are tombstoned for composition unless the reader needs them to understand a change, migration, decision, accountability record, or direct reply.

## Choose the writing mode

- **State:** The reader needs the current thing. Typical artifacts are README files, user guides, API docs, reference pages, architecture overviews, landing pages, and UI copy.
- **Change:** The reader needs to understand a project change. Typical artifacts are PR and commit text, changelogs, release notes, and migration guides.
- **Decision:** The reader needs context, alternatives, rationale, or accountability. Typical artifacts are ADRs, proposals, postmortems, and review responses.
- **Direct:** A known recipient is part of the conversation. Typical artifacts are email, support replies, stakeholder updates, announcements, and the task completion response.

The mode controls whether process or history is relevant; it does not grant permission to expose unrelated internal information.

## Compose the audience view

Every sentence must help the intended reader perform their goal, understand the subject, make a decision, or take an appropriate action. Use references such as “you,” “we,” “this change,” and “previously” only when their meaning is available inside the artifact or shared recipient context.

For state writing, describe the verified current state as though the reader never saw the task conversation and the subject had always been in that state. Preserve actionable negative facts—limitations, incompatibilities, security boundaries, and explicit non-goals—when they affect a reader decision.

For change and decision writing, describe subject history and evidence rather than narrating how the assistant was instructed or corrected. For direct writing, mention the work process only to the extent that it serves the recipient.

## Keep artifacts distinct

Do not blend content for different audiences without an explicit structure. In particular, keep a public artifact separate from the completion response that reports edits, checks, uncertainty, and next steps to the requester.

Before delivery, apply two tests:

1. **Orphan-reader test:** Can the intended reader understand and use this text without access to hidden task context?
2. **Counterfactual test for state writing:** If the subject had always been in its current state, would every sentence still belong?

Rewrite from the audience view when either test fails; do not merely delete a suspicious phrase.

## Audit after drafting

For Markdown or plain text, run the deterministic audience-leakage audit when Python is available:

```text
python <skill-directory>/scripts/audit_external_text.py <artifact> --profile state
```

Choose `state`, `change`, `decision`, or `direct` to match the writing mode. Errors indicate strong audience-boundary failures. Warnings require a reader-value decision and are not automatic deletions. Fix relevant findings and rerun the audit before delivery.
