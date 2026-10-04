---
name: icaire-ingest-meeting
description: Convert ICAIRE meeting transcripts and notes into durable ICAIRE memory. Use when the user asks to ingest, save, summarize, or update memory from a meeting, call, visit, workshop, or conversation.
---

# ICAIRE Ingest: Meeting

Convert meeting records into durable ICAIRE memory that preserves decisions,
actions, people updates, initiative updates, and unresolved questions.

## Contract

- Start from the transcript, notes, recording transcript, Granola entry, or
  meeting summary the user provided or named.
- Use BigBrain or the ICAIRE MCP connector for existing ICAIRE people,
  organizations, initiatives, prior meetings, and page conventions when the
  user has not supplied enough context.
- Prefer the remote ICAIRE MCP connector for remote-brain writes when it is
  available; the remote brain is already rooted at `cortex/`, so use paths like
  `meetings/...`, `people/...`, and `initiatives/...`.
- Before choosing paths, call ICAIRE MCP `filing_rules` and follow the compiled
  `FILING.md` guidance it returns. If that tool is unavailable, list and read
  the relevant `FILING.md` files directly; do not expect a page named
  `filing_rules` to exist.
- Produce durable meeting memory, not just a conversational recap.
- Preserve source uncertainty: distinguish confirmed decisions from implied
  next steps, candidate actions, and open questions.
- Verify persistence after writing by reading or listing the created or updated
  pages before claiming completion.

## Workflow

1. Identify the source and target.
   - Determine meeting title, date, participants, source system, intended brain
     target, and whether the user wants local files or remote ICAIRE MCP writes.
   - If the user only asks to ingest a named meeting, find the source through
     the relevant connector or local context instead of asking for pasted notes
     immediately.
2. Gather existing context.
   - Call ICAIRE MCP `filing_rules` before choosing the meeting page path,
     related page updates, or raw transcript path.
   - Search BigBrain or ICAIRE MCP for matching meetings, people,
     organizations, initiatives, and open actions.
   - Check for an existing meeting page before creating a duplicate.
3. Extract meeting memory.
   - Capture purpose, attendees, summary, key discussion points, decisions,
     action items, owners, deadlines, risks, blockers, initiative updates,
     people updates, organization updates, and open questions.
   - Keep sensitive or uncertain material labeled appropriately.
4. Choose page updates.
   - Create or update one `meetings/*.md` page for the meeting.
   - Update related `people`, `organizations` or `companies`, `initiatives`,
     `projects`, `concepts`, or `inbox` pages only when the source materially
     changes durable knowledge.
   - Add timeline entries for meaningful dated changes.
5. Write in the ICAIRE brain shape.
   - Use frontmatter with `type`, `title`, and `created` when creating new
     pages unless the existing page convention requires more.
   - Keep the body current-state oriented, then separate timeline history under
     `## Timeline`.
6. Verify the write.
   - Read the new or changed meeting page directly.
   - Use list or search only as a secondary check because indexing can lag.
   - Report any pages that still need human review or additional source
     material.

## Output

Return a concise ingestion report with:

- `Created Or Updated`: meeting page and any related pages changed.
- `Meeting Summary`: short durable summary.
- `Decisions`: confirmed decisions only.
- `Action Items`: owner, action, deadline, and confidence where known.
- `People Updates`: durable relationship or role changes.
- `Initiative Updates`: status, milestone, risk, blocker, or dependency changes.
- `Open Questions`: missing facts or unresolved follow-ups.
- `Verification`: pages read back or checks performed.

## Guardrails

- Do not invent attendees, decisions, owners, deadlines, or initiative status.
- Do not treat a transcript summary as authoritative when the underlying source
  contradicts it.
- Do not create duplicate meeting pages when an existing page should be updated.
- Do not use `cortex/meetings/...` for remote ICAIRE MCP paths when the server
  is already rooted at `cortex/`.
- Do not claim that broad search proves a fresh page exists; read or list it
  directly after creation.
- Do not expose sensitive internal notes in an external-facing summary unless
  the user explicitly asks for that artifact.
- Do not bypass the MCP `filing_rules` tool by guessing from stale local
  conventions or by reading a nonexistent `filing_rules` page.
