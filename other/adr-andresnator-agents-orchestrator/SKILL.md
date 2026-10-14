---
name: adr
description: "Trigger: ADR, architecture decision record, technical decision. Create ADRs that document context, options, rationale, consequences, and trade-offs."
license: MIT
metadata:
  author: andresnator
  status: done
  version: "2.0.0"
---

# ADR Creator

Create concise Architecture Decision Records that explain a decision, the context that forced it, the options considered, and the consequences accepted.

## Activation Contract

Use this skill when the user asks for an ADR, architecture decision record, technical decision record, or any formal record of why a technical or architectural choice was made.

Default to interview mode unless the user already supplied enough information to draft a complete ADR. Ask interview questions in the user's language. ADR artifact language is English unless the user explicitly asks for another language.

## Hard Rules

- Ask one question at a time in interview mode.
- State once at the start of the interview that the user may skip questions or stop the interview at any time.
- Ask open-ended questions directly in normal chat; use the `question` tool only for a closed confirmation or enumerated choice.
- Add a short `Recommendation: ...` line only when it helps the user respond.
- Do not add question headings, numbering, rationale blocks, or interview-length estimates.
- Constructively challenge vague, contradictory, or rationale-free answers before drafting; proceed if the user explicitly says to continue anyway.
- Do not invent alternatives, pros, cons, or rationale. Ask when alternatives are missing.
- Use `Accepted` when the decision is already made; use `Proposed` for proposals, evaluations, or unclear status.
- Write or modify files only when the user explicitly asks for a file/path.

## Interview Flow

Gather only what is needed, dependency-first:

1. Decision title and status.
2. Context: problem, constraints, forces, and why the decision matters now.
3. Chosen option or proposal.
4. Options considered, with pros and cons for each.
5. Consequences: benefits, drawbacks, risks, and trade-offs.
6. Follow-up only when there are useful open actions or unresolved questions.

## Conversation Format

```markdown
[Direct question]

Recommendation: [short example when useful]
```

Mini example:

```markdown
What decision should this ADR capture?

Recommendation: "Adopt PostgreSQL for billing data."
```

## Output Contract

Read `assets/template-markdown.md` before drafting and fill that structure.

By default, return the final ADR as exactly one Markdown code block and do not create files. If the user explicitly requested a file/path, save the ADR there and summarize the saved path in chat.

Never leave placeholder instructions in the final ADR. If the user intentionally skips a required detail, use `TBD` sparingly and only for that skipped detail.

## Reference

- Template: `assets/template-markdown.md`
