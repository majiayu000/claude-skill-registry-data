---
name: groom-notes
description: Review, prune, and suggest notes in notes.toml. Cleans stale notes and proposes new ones from recent changes.
disable-model-invocation: false
argument-hint: "[--warnings|--patterns|--all]"
---

# Groom Notes

Review all notes in `docs/notes.toml` — clean up stale ones and suggest new ones from recent work.

## Phase 1: Prune

1. **Parse notes**: Read `docs/notes.toml` and list all notes with their sentiment, text preview, and mentions.

2. **Identify candidates for removal**:
   - Notes that reference removed/renamed files (check with `Glob`)
   - Notes that contradict current code (e.g., "X doesn't work" when X was fixed)
   - Duplicate or near-duplicate notes covering the same topic
   - Notes about temporary issues that have been resolved
   - Notes with stale mentions (files that no longer exist)

3. **Present findings**: Show a summary of candidates grouped by reason:
   - **Stale**: References removed code or fixed issues
   - **Superseded**: Newer note covers the same ground
   - **Duplicate**: Multiple notes saying essentially the same thing
   - **Update mentions**: File paths that moved but lesson is still valid

4. **Get approval**: Present the list of proposed changes. Ask the user to confirm before making changes.

5. **Execute**: Use `cqs notes remove` / `cqs notes update` CLI commands. If the CLI isn't available, edit `docs/notes.toml` directly.

6. **Report**: Show before/after count and what was changed.

## Phase 2: Suggest

After pruning, scan for note-worthy events that aren't already captured:

1. **Check recent git history**: `git log --since="1 week ago" --oneline` (or since last groom)
2. **Look for surprise-worthy patterns**:
   - Bug fixes — what was the non-obvious cause? (sentiment: -0.5 or -1)
   - Refactoring lessons — what pattern worked or didn't? (sentiment: 0.5 or -0.5)
   - New features — any architectural decisions worth remembering? (sentiment: 0)
   - CI/tooling changes — any gotchas? (sentiment: -0.5)
   - Performance discoveries — unexpectedly fast or slow? (sentiment: 0.5 or -0.5)
3. **Cross-check existing notes**: Don't suggest notes that duplicate existing ones
4. **Present suggestions**: Show proposed notes with text, sentiment, and mentions
5. **Get approval**: User confirms which to add
6. **Execute**: Use `cqs notes add` for each approved suggestion

### What makes a good note

Notes capture **surprises** — things that broke predictions or would trip up a future session:
- "X looks like it should work but doesn't because Y" (negative surprise)
- "Doing X this way was unexpectedly effective" (positive surprise)
- "X and Y are coupled in non-obvious ways" (neutral observation)

**Not** good notes: routine changes, things obvious from code, activity logs.

## Staleness checks

Start with the built-in checker — it verifies every mention against the filesystem and index in one call:
```
cqs notes list --check --json
```
For anything it flags, confirm manually (Glob the file, `cqs "<symbol>" --name-only`) before proposing removal.

Cross-reference with git log — if a note mentions an issue number, check if that issue is closed.

## Rules

- Never remove or add notes without user approval
- Preserve the file header comments
- Keep notes that capture general lessons even if the specific code changed
- When in doubt, keep the note — false negatives (missing a useful note) are worse than false positives (keeping a stale one)
- Sentiment is DISCRETE: only -1, -0.5, 0, 0.5, 1
- After grooming, suggest running `cqs index` to update the search index
