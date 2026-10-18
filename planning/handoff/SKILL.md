---
name: handoff
description: Compact the current conversation into a durable handoff document for another agent or future session to pick up. Use when the user says "handoff", "handoff to /prototype", "summarize for next session", "another agent should continue", or when switching skills/sessions after substantial context has accumulated.
argument-hint: "What will the next session be used for?"
---

# Handoff

Write a concise handoff document so a fresh agent can continue from the current state without rereading the whole conversation.

## When to use

- User asks for `/handoff`, "handoff this", "handoff to /prototype", "handoff back", "summarize for next session", or "another agent should continue".
- A long planning, prototype, diagnosis, or implementation thread is about to switch focus or end.
- A side quest should run in another session and return with a compact verdict.

## Process

1. Identify the handoff target. If the user passed arguments, treat them as the next session's focus, such as `/prototype`, `/tdd`, or "back to grilling session".
2. Create `.scratch/handoffs/` if needed.
3. Save the handoff as `.scratch/handoffs/YYYY-MM-DD-<short-slug>.md`. Use the current local date and a slug for the target or topic. If a file already exists, append a short numeric suffix rather than overwriting.
4. Before writing, read any existing file at that path so you do not clobber prior notes.
5. Write only the context the next agent actually needs.

## Content

Include:

- Goal: what the next session should do.
- Current state: what has already been decided or done.
- Key unresolved questions.
- Relevant artifacts: PRDs, issues, ADRs, design docs, prototype paths, commits, diffs, URLs.
- Suggested next skill or command.
- Return instructions: what result should come back to this thread or parent skill.

Do not duplicate content already captured in PRDs, plans, ADRs, issues, commits, diffs, or prototype notes. Reference them by path or URL.

## Patterns

- "handoff to /prototype" -> explain the question the prototype must answer, the relevant app/module context, and that prototype output is disposable.
- "handoff back" -> summarize what the side quest learned, where the artifact lives, and what decision can now be made.
- "handoff to implementation" -> point at the approved PRD/issues/design artifacts and note remaining risks.

## Anti-patterns

- Do not turn the handoff into a full project history.
- Do not write vague instructions like "continue the work"; name the next concrete move.
- Do not put durable project decisions only in the handoff. If a decision belongs in `CONTEXT.md`, an ADR, an issue, or a PRD, put it there and link to it.

## Next

Start the next session with the skill you named as the handoff target (for example `roblox-to-issues`, `roblox-debugging-bugfix`, or `roblox-game-development-lifecycle`). When a side quest returns, hand its verdict back with `handoff` again.
