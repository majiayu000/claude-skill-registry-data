---
name: dream
description: Memory consolidation - review, merge, prune, and index memory files. Run periodically to keep memories organized and up-to-date.
user_invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Dream: Memory Consolidation

You are performing a dream - a reflective pass over your memory files. Synthesize what you've learned recently into durable, well-organized memories so that future sessions can orient quickly.

## Phase 1 - Orient

- `ls` the memory directory to see what already exists
- Read `MEMORY.md` to understand the current index
- Skim existing topic files so you improve them rather than creating duplicates
- If `logs/` or `sessions/` subdirectories exist, review recent entries there

## Phase 2 - Gather recent signal

Look for new information worth persisting. Sources in rough priority order:

1. **Daily logs** (`logs/YYYY/MM/YYYY-MM-DD.md`) if present - these are the append-only stream
2. **Existing memories that drifted** - facts that contradict something you see in the codebase now
3. **Transcript search** - if you need specific context, grep transcripts for narrow terms:
   `grep -rn "<narrow term>" .claude/transcripts/ --include="*.jsonl" | tail -50`

Don't exhaustively read transcripts. Look only for things you already suspect matter.

## Phase 3 - Consolidate

For each thing worth remembering, write or update a memory file. Use these type conventions:

| Type | What belongs | Examples |
|------|-------------|----------|
| **user** | User's role, goals, preferences, knowledge | "senior Go dev, new to React" |
| **feedback** | Corrections AND confirmations from user | "don't mock DB in tests", "bundled PR was right call" |
| **project** | Ongoing work context, deadlines, initiatives | "merge freeze 2026-03-05 for mobile release" |
| **reference** | Pointers to external systems | "pipeline bugs in Linear project INGEST" |

Each memory file uses this format:
```markdown
---
name: {{name}}
description: {{one-line description}}
type: {{user, feedback, project, reference}}
---

{{content - for feedback/project: rule, then **Why:** and **How to apply:**}}
```

Focus on:
- Merging new signal into existing topic files rather than creating near-duplicates
- Converting relative dates ("yesterday", "last week") to absolute dates
- Deleting contradicted facts - if today's investigation disproves an old memory, fix it at the source

## Phase 4 - Prune and index

Update `MEMORY.md` so it stays under 200 lines AND under ~25KB. It's an **index**, not a dump:

- Each entry: one line under ~150 chars: `- [Title](file.md) - one-line hook`
- Never write memory content directly into MEMORY.md
- Remove pointers to stale, wrong, or superseded memories
- Shorten verbose entries - move detail to the topic file
- Add pointers to newly important memories
- Resolve contradictions - if two files disagree, fix the wrong one

## What NOT to save

- Code patterns, architecture, file paths - derivable from the project
- Git history - `git log` / `git blame` are authoritative
- Debugging solutions - the fix is in the code
- Anything already in CLAUDE.md
- Ephemeral task details or conversation context

---

Return a brief summary of what you consolidated, updated, or pruned. If nothing changed, say so.
