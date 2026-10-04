---
name: draft-reply
description: "Draft a reply to a ticket and post it as a private note for review. READ-ONLY — no code changes, no public reply."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before drafting the reply (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/code-navigation.md`
- `<project-root>/docs/database-tools.md`
- `<project-root>/docs/doc-lookup.md`
- `<project-root>/docs/issue-trackers.md`

Load and analyze the ticket, gather codebase context if needed, draft a reply, post it as a private note for human review. READ-ONLY — no code changes, no commits, no public reply. The note is a draft the human sends; do not post the reply to the customer.

## Additional Context

- Treat ticket systems generically. Use `<additional-context>` to shape tone, audience, depth. Default audience is the customer/requester unless `<additional-context>` says otherwise.
- One draft per ticket. Do not post multiple competing drafts; revise the existing note if the user asks for changes.

## The Discipline

**The draft is for a human, not the customer.** It must be ready to send verbatim, but the human decides whether and how to deliver it.

### Interpret Arguments

- Ticket reference/URL → `<ticket-url>`; extra focus/constraints/audience hints → `<additional-context>`; no arguments → derive from conversation.
- Do NOT expect a `<question>` in arguments — it lives on the ticket. Only if the caller explicitly adds one → store as `<question>` to scope the reply.

### Load Ticket Context

- `<ticket-url>` defined: load via issue tracker tool (see `<project-root>/docs/issue-trackers.md`) with `source: <ticket-url>`, `comments: true` → `<ticket-context>`. Read all attachments with `relativePath` via `read` (images → describe; documents → extract key info → `<attachment-insights>`). Note gaps if inaccessible.
- Otherwise: treat relevant request/conversation as `<ticket-context>`.
- Missing or unloadable → STOP.

### Analyze the Ticket

Read the body and every comment in order. Derive:
- `<reply-target>` — the most recent unanswered question or the open request the reply must address. If multiple open threads, pick the most recent; note the others.
- `<requester-profile>` — author, role, technical level (infer from tone/content; do not assume).
- `<ticket-facts>` — stated facts, constraints, prior answers, what is already resolved.
- `<open-gaps>` — what is still unclear or unaddressed that the reply must cover.

Ambiguous about what to reply to → ask the user before drafting. Do not guess the `<reply-target>`.

### Gather Codebase Context (only if needed)

Skip when the reply is purely procedural, status, or non-technical and the ticket already contains the answer. Otherwise:

- **Code**: Gather a distilled brief (entry points, callers, conventions, `file:line` citations) using `grep`/`find_file_by_name`/code navigation tool (see `<project-root>/docs/code-navigation.md`). Pass `<reply-target>`, relevant entities, module path → `<repo-context>`.
- **Data**: When the reply depends on persisted state (counts, status, sample rows), inspect the live database via database tools (see `<project-root>/docs/database-tools.md`). Database is ground truth; do not rely on seeders/migrations/operations.
- **Docs**: For framework/library/API/version questions, use doc lookup (see `<project-root>/docs/doc-lookup.md`) → `<doc-context>`.

Store as `<supporting-context>`. Cite `file:line` and query results inline where they back a claim. Do not dump raw output into the draft.

### Draft the Reply

Write `<draft-reply>` as the message the human can send to the requester with minimal edits. Rules:

- **Audience match.** Match tone and depth to `<requester-profile>` and `<additional-context>`. Customer-facing by default: greet, plain language, no internal jargon, no `file:line` citations in the reply body. Internal reviewer: technical, cite `file:line`, no client-facing tone.
- **Answer the `<reply-target>` directly first.** Lead with the answer; background and caveats after.
- **Ground every claim.** Technical assertions must trace to `<ticket-facts>`, `<supporting-context>`, or `<doc-context>`. If a claim cannot be grounded, mark it `[NEEDS-REVIEW: <what's uncertain>]` rather than stating it as fact.
- **No invented details.** No fabricated dates, IDs, statuses, or quotes. If missing, say so and flag for the human.
- **Length to match the question.** One-line answer for a one-line question; structured response for a multi-part question. No padding.
- **No code changes, no commits, no PRs promised** unless the user explicitly asked for them in `<additional-context>`.

### Shape the Note

Post a single private note containing:
- `## Draft reply` heading.
- `<draft-reply>` body (ready to send).
- `## Supporting context` section (internal only): `<reply-target>`, `<requester-profile>`, key `<supporting-context>` citations (`file:line`, query results, doc references), and `[NEEDS-REVIEW]` items with the reason. This section stays in the private note; the human strips it before sending.

### Sync

Post the private note via the issue tracker sync tool (see `<project-root>/docs/issue-trackers.md`): `refUrl` = `<ticket-url>`, `comments` = array with the single markdown string from "Shape the Note". Use private/internal visibility per provider rules; if the provider has no private note concept, post as a regular comment and prefix the body with `DRAFT — not for sending yet:`. Follow provider-specific sync rules. If sync fails, report the error and provide the draft in chat.

## Notes

- **Traceability (required):** If `<question>` or `<additional-context>` originated from skill arguments rather than the ticket body, the ticket reader cannot see what prompted the draft — so the note MUST restate the provided `<question>` / `<additional-context>` (as a "Question:" / "Context:" preamble in the supporting section) before the draft. Skip only when already visible in the ticket body or comments.
- Ticket load tool downloads attachments to `storage/app/mcp/{source}` — read before drafting.
- Final output: ticket URL of the posted note. Do not paste the full draft back into chat; one line confirming the post is enough.
- If the user asks to revise after posting: edit the note in place per provider rules; do not post a second draft note.
