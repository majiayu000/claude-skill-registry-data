---
name: context-sync
description: Propose writes back to the persistent background context layer — the non-issue-specific things learned in this workspace. Use at the end of a session, when closing the workspace, or when the user says "remember that".
---

# context-sync

The write path to the background context store. Read `memory/README.md` first; the canonical
schema is the [Portable Context Contract](https://github.com/danielrosehill/Claude-Personal-Context-Plugin/blob/main/docs/context-contract.md).

**If the `personal-context` plugin is installed**, hand off: run `/personal-context:remember`
with the candidates below and let it handle schema, ids and indexing. Everything after this line
is the fallback for when it isn't.

## What belongs in the store

The test: *would this still be true and useful in a workspace about something else?*

| Goes to the store | Stays in this workspace |
| --- | --- |
| Who someone is, and how that relationship works | What they did on 14 August |
| A pattern that isn't specific to this issue | A thread within this issue |
| How they want to be spoken to | This session's mood |
| Dated events belonging to their life history | The incident under discussion |
| What has helped before, generally | Whether the timeline helped last week |
| Care history: who they've seen, what was tried | This appointment's brief |

When unsure, it stays here. The store gets read by every future workspace; a cluttered store is
worse than a thin one.

## Procedure

1. **Check the write mode** in `memory/config.yaml`. `mode: off` means propose nothing — say what
   you would have written and stop.

2. **Collect candidates** from this session. Usually one to three. Ten candidates means you are
   exporting the session, not extracting from it.

3. **Show each one as it would be written**, in full, before writing anything:

   ```yaml
   ---
   id: person-m
   type: person          # person | period | event | pattern | care | preference | fact
   title: M — line manager, 2023–present
   scopes: [career]      # which workspaces may load this
   sensitivity: normal   # low | normal | high
   source: inferred      # interview | ingested | inferred | user-written
   confidence: stated    # stated | corroborated | inferred
   created: 2026-08-14
   updated: 2026-08-14
   ---

   <two or three sentences, factual, third person, no interpretation>

   ## History
   - 2026-08-14 — created from <workspace> session <id>
   ```

   For each, ask three things: is it right, is the scope right, and is the sensitivity right.
   `high` means it will not load into a workspace unless asked for by name.

4. **Write only what is confirmed.** One file per entry under the type's directory. Append a line
   to `<store>/INDEX.md`. If the backend is `git`, commit; never push to a public remote.

5. **Updating an existing entry:** append to its `## History` with today's date and what changed,
   revise the body, bump `updated`. Never rewrite history lines.

## Rules

- **Nothing is written silently.** Not even something they said explicitly. Show, ask, write.
- **`source: inferred` stays inferred** until they state it themselves in a later session.
- **Never raise sensitivity downward** on your own — `high` doesn't become `normal` because it
  would be convenient for a brief.
- **Never write issue material to the store** to "keep it safe". This repo is where it lives.
- **Never use model-managed memory as a fallback** when the store is unreachable. If the path in
  `config.yaml` doesn't exist, say so and stop; a broken write is recoverable, a silent one isn't.
- If they ask you to forget something already in the store, delete the entry, remove its INDEX
  line, and say what you removed. Don't argue for keeping it.
