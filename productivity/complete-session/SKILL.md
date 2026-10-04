---
name: complete-session
description: Finalize the current enhancement session — write the Sessions/E{n} retro note, tick the row in the master plan, update Timeline, and commit. Use when the user says "we're done with E4", "wrap this up", or after the last task in a session is checked off.
---

# complete-session

Closes a session cleanly so the vault, memory, and git history all reflect the work.

## Steps

1. **Verify the work is actually done**:
   - All TaskCreate items for this session are `completed`
   - `/typecheck` passes
   - The target page loads without errors
   - Any new endpoints return data
2. **Create or update** `Aqarkom_Knowledge/Sessions/E{n} - {Page}.md` using sibling notes (E1, E2, E3) as templates. Required sections:
   - Frontmatter: `tags`, `created`, `session`, `status: done`
   - **Shipped** — checklist of what landed
   - **Key code** — 1-3 short snippets that show the pattern
   - **Lessons** — anything surprising you learned (also save as feedback memory if it's behavioral)
   - **Related** — links to Features notes, ADRs, etc.
3. **Tick the master plan** — edit `Aqarkom_Knowledge/Sessions/Enhancement Plan E1-E20.md`, change ⏳ → ✅ for this row, link the new note.
4. **Update the Home MOC** if this session unlocked a new section (rare).
5. **Update auto-memory** if anything in this session contradicted or refined an existing memory entry.
6. **Run `/commit-and-track`** to commit and update the changelog.
7. **Tell the user** what changed and what the next ⏳ session is.

## Verification

- [ ] Sessions/E{n}.md exists with all required sections
- [ ] Master plan row is ✅
- [ ] Commit landed
- [ ] User informed of next session

## Anti-patterns

- Don't write the retro before verifying typecheck — broken sessions shouldn't be marked done
- Don't copy-paste prose from prior retros — each session has unique lessons
- Don't skip the memory update — that's how feedback compounds
