---
name: setup
description: Initialize or refresh the durable context for this second-brain repository.
---

# Setup

Use this skill for a first-time install or when the user wants to refresh the core profile.

Read `SYSTEM.md` first. Then inspect `workspace/identity.md`, `workspace/objectives.md`, `workspace/style.md`, and `workspace/sources.md`.

## Interview

Ask only for missing or stale information. Ask one prompt at a time. Cover these six areas:

1. **Role and scope** — Who is this for, what work do they do, and who do they serve?
2. **Near-term outcomes** — What 2–4 results matter over roughly the next 8–12 weeks?
3. **Authoritative systems** — Where do current files, communications, meetings, tasks, customer data, and financial or operational truth live?
4. **Repeated work** — Which recurring tasks, reports, decisions, or handoffs consume meaningful time?
5. **Collaboration preferences** — How concise, proactive, formal, or structured should the assistant be? Real writing examples are optional.
6. **Boundaries** — What information should not be stored, and what actions require explicit approval?

Do not invent answers. Reuse facts already present in the repository.

## Write phase

After the interview, update only the relevant files:

- `workspace/identity.md`
- `workspace/objectives.md`
- `workspace/style.md`
- `workspace/sources.md`

Preserve unrelated content.

If the user identified an important recurring pain point, mention that `improve` can turn it into a small workflow later. Do not build extra workflows during setup unless explicitly asked.

## Finish

Return:
- which files were updated,
- the user's current 2–4 outcomes,
- any source routes that are documented but not yet verified,
- one useful first question the user can ask the system based on the saved context.
