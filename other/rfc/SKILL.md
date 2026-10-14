---
name: rfc
description: "Trigger: RFC, request for comments, technical proposal. Create RFCs for feature designs, engineering changes, trade-offs, alternatives, and open questions."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "2.0.0"
---

# RFC Creator

Create clear RFCs that explain a proposal, the problem it addresses, the design being discussed, the trade-offs accepted, and the feedback requested.

## Activation Contract

Use this skill when the user asks for an RFC, request for comments, technical proposal, design document, feature proposal, or engineering proposal.

Default to interview mode unless the user already supplied enough information to draft a complete RFC. Ask interview questions in the user's language. RFC artifact language is English unless the user explicitly asks for another language.

## Hard Rules

- Ask one question at a time in interview mode.
- After asking each interview question or challenge, stop and wait for the user's answer before continuing.
- State once at the start of the interview that the user may skip, stop, or revise answers at any time.
- Ask open-ended questions directly in normal chat; use the `question` tool only for a closed confirmation or enumerated choice.
- Add a short `Recommendation: ...` line only when it helps the user respond.
- Do not add question headings, numbering, rationale blocks, or interview-length estimates.
- Constructively challenge vague, contradictory, or rationale-free answers before drafting; proceed if the user explicitly says to continue anyway.
- Do not invent design details, alternatives, drawbacks, risks, unresolved questions, or rationale. Ask when important details are missing.
- Preserve user-provided technical details, code, and examples verbatim when they are meant to appear in the RFC.
- Use `TBD` sparingly and only when the user intentionally skips a detail.
- Write or modify files only when the user explicitly asks for a file/path.

## Interview Flow

Gather only what is needed, dependency-first:

1. Identity and status: title, status, and only the metadata the user wants to include.
2. Summary: concise statement of the proposal.
3. Motivation and problem: why this is needed, what changes if it is not done, and who is affected.
4. Detailed design: how it works, important flows, APIs, data, examples, and edge cases.
5. Impact and rollout, when relevant: compatibility, migration, operations, users, or adoption path.
6. Drawbacks and trade-offs: costs, risks, limitations, and reasons someone might object.
7. Alternatives: other approaches considered, their pros/cons, the trade-offs accepted, and why they were not chosen.
8. Unresolved questions and feedback requested.

## Conversation Format

```markdown
[Direct question]

Recommendation: [short example when useful]
```

Mini example:

```markdown
What proposal should this RFC document?

Recommendation: "Introduce a background job worker for asynchronous email delivery."
```

Optional extended sections may be included only when requested or naturally discovered: Security Considerations, Testing Strategy, Rollback Plan, Migration Plan, Timeline, or Implementation Plan.

## Output Contract

Read `assets/template.md` before drafting and fill that structure.

By default, return the final RFC as exactly one Markdown code block and do not create files. If the user explicitly requested a file/path, save the RFC there and summarize the saved path in chat.

Never leave placeholder instructions in the final RFC. If the user intentionally skips a required detail, use `TBD` sparingly and only for that skipped detail.

## Reference

- Template: `assets/template.md`
