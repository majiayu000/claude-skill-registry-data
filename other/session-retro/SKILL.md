---
name: session-retro
description: At the end of a Claude session, write a History/Conversations note summarizing what was asked and done, update the Timeline, and refresh memory if needed. Use when the user says "wrap up", "end of session", or before they're about to /clear.
---

# session-retro

End-of-session sync. Mirrors what the offline extraction script does, but for the *current* conversation.

## Steps

1. **Count user prompts in this session** — scan back through the conversation. Group by date if it spans days.
2. **List files modified** — anything you `Write` or `Edit`'d this session.
3. **Identify the headline** — what was the main thing accomplished?
4. **Find the next session number** — list `Aqarkom_Knowledge/History/Conversations/Session*.md` and pick the next NN.
5. **Create** `Aqarkom_Knowledge/History/Conversations/Session NN - YYYY-MM-DD.md` with:
   - Frontmatter (`session_id`, `started`, `ended`, `prompts`)
   - One-line headline
   - Tool usage summary (which tools, roughly how many calls)
   - Files modified (top 30, deduplicated)
   - User prompts in chronological order with timestamps (best-effort if exact ts not available)
   - Lessons / non-obvious takeaways
   - Related links (Sessions/E*, Decisions, Features)
6. **Update** `Aqarkom_Knowledge/History/Timeline.md` — add a row for this session.
7. **Update** `Aqarkom_Knowledge/History/Conversations/Index.md` — add this session to the table.
8. **Refresh memory** — for any guidance the user gave that wasn't already a memory entry, save it now (feedback type).
9. **Commit** the vault changes with `/commit-and-track`.

## Verification

- [ ] New session note exists
- [ ] Timeline + Conversations Index updated
- [ ] At least one new memory saved IF the user gave new guidance
- [ ] Commit lands

## Anti-patterns

- Don't dump every prompt verbatim — summarize when prompts are repetitive ("user iterated 5x on growth badge styling")
- Don't include code blobs — link to commits instead
- Don't write the retro for a session where nothing was actually done
