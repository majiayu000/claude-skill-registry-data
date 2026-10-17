---
name: tmp-snapshot
description: Save content from the current conversation to /tmp/<descriptive-kebab-name>.md, then return the absolute path and an outline (every header with a one-line summary). Use when the user says "save this to /tmp", "snapshot this", "dump the X part", "stash this", "save the discussion about Y", or otherwise asks to drop content from the chat into a quick scratch markdown file.
---

# tmp-snapshot

Save content the user asked for into `/tmp/<name>.md`, then reply with the path and an outline. Nothing more.

## Steps

1. **Pick the content.** Use what the user pointed at:
   - A topic from this conversation ("save the auth part") → extract just that slice.
   - The whole chat ("save everything we just discussed") → summarize the substantive bits.
   - Text they pasted into their message → use it verbatim.

   If the slice is ambiguous, ask **once** before writing.

2. **Pick a kebab-case filename.** 2–4 words, descriptive of the content, no dates unless they matter to the topic. Path is always `/tmp/<name>.md` — never a subfolder unless the user specifies one. Overwrite if it exists; `/tmp` is scratch.

3. **Write the file** as standalone markdown: one `#` H1 title, `##` for sections, `###` for sub-sections. It should read cleanly without the chat as context. No YAML frontmatter unless the user asks.

4. **Reply with the path + outline.** No preamble, no closing summary. Just those two things.

## Outline format

A tree of every header in the saved file, each followed by **one short sentence** summarizing what's in that section. Indent by header depth.

### Example reply

`/tmp/auth-token-rotation.md`

```
# Auth token rotation — Migrate from server sessions to JWT with refresh tokens.
  ## Current state — Sessions in Postgres, 24h expiry.
  ## Target — Short-lived JWT access + HttpOnly refresh cookie.
  ## Migration — Three-phase rollout plan.
    ### Phase 1 — Dual-write to both stores.
    ### Phase 2 — Read new, fall back to old.
    ### Phase 3 — Drop legacy session table.
```

## Notes

- Keep each summary to one line. The outline should be glanceable, not a re-paste of the doc.
- If the user asks for a different directory (e.g. `/tmp/notes/`), honor it — but default is bare `/tmp/`.
- Don't ask "are you sure?" before overwriting — that's what `/tmp` is for.
