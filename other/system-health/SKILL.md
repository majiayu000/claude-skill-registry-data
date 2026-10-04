---
name: system-health
description: Preventive hygiene audit of your own Claude Code configuration — memory files, project context (CLAUDE.md), rules, permissions, skills — a deterministic scan of sizes / broken links / stale entries / excessive permissions / junk + interpretation + targeted fixes by agreement. Keeps the setup from rotting before it breaks. Triggers — "check the system", "system health", "workflow hygiene", "what to clean up", "audit memory", "optimize the system".
---

# /system-health — Claude Code config hygiene

Keeps the setup "in an optimization flow": a cheap regular measurement catches degradation (bloated memory/context files, broken links, stale entries, excessive permissions, junk) BEFORE it breaks. Like a server health check, but for your Claude Code configuration rather than servers.

## When to use
- On command or the trigger phrases above.
- Once a week (can be scheduled).
- After a large session with heavy writes to memory.
- When a built-in hook warns "memory index over limit" (that's the signal it's time).

## Process

### Step 1 — deterministic measurement (0 LLM tokens)
A read-only shell pass that changes nothing and emits metrics with `✓OK` / `⚠️WARN` flags. Measure:
- Size of the memory index and each topic file vs the model's read limit.
- Broken `[[wiki-links]]` / pointers in the active index (a link to a non-existent file is a distractor).
- Stale "next-session" / TODO carryovers that are actually finished.
- Orphan files (referenced by no index — invisible to recall, dead weight).
- Project context file size vs target.
- Excessive permission entries (specific grants subsumed by a wildcard).
- `.bak`/junk files lying around.

### Step 2 — interpretation (LLM)
Read the report. Focus on `⚠️WARN` lines. Translate each into a concrete diagnosis: what grew/went stale and why it hurts (recall / tokens / security).

### Step 3 — targeted fixes BY AGREEMENT
Propose minimal surgical fixes per WARN. **Don't act silently** (except pure junk). ROI order:
- **broken links in the active index (CRITICAL)** → fix/remove immediately (distractors hurt recall).
- **index over target** → compress reactively: longest lines first; then move on-demand references out of the "active" section into an on-demand index; finished/dormant → an archive file. Don't cut live facts for a metric.
- **stale "next-session" carryovers** → read status, move finished/dormant to archive.
- **orphan files** (no pointer in any index) → either wire a pointer into the right index, or archive/delete (user decides). A file with no pointer is invisible to recall.
- **consolidation candidates** (a topic spread across many files) → read the group, distinguish DUPLICATES (one fact in N files → merge into one, the rest a link) from FACETS (different triggers → leave alone). Only merge real duplicates, by agreement.
- **project context file over target** → move dated patch-history into topic memory, keep state + ⚠️ invariants + pointers.
- **excessive permissions** → remove specific grants subsumed by a wildcard, keeping MCP/Skill/deny entries.
- **`.bak` junk** → move to a backups dir (pure junk — fine without asking).

## Discipline (the "change accounting" rule)
Back up BEFORE any mutation (snapshot memory + rules to a backups dir) → surgical edit → verify by checking (size + a diff of preserved entries/invariants against the backup, not on faith) → record in one place.

## Anti-actions
- ❌ **Don't squeeze to a target blindly, losing facts** — the read limit matters more than a cosmetic target; if the index loads fully, further squeezing is optional.
- ❌ **Don't mass-merge topic files** — "many files on a topic" ≠ duplicates; they're facets with different triggers, merging loses recall.
- ❌ **Don't delete skills/files without agreement** — they're the user's data/tools; show the finding, the user decides.
- ❌ **Don't touch passwords/credentials in memory** silently — move to a secrets store only on command.
- ❌ **Don't measure size in bytes** — the built-in memory hook measures in Unicode CHARACTERS (non-Latin scripts can be 2 bytes/char).

## Principle
Hygiene is preventive and cheap. A weekly deterministic scan is a few seconds; the LLM only interprets the WARN lines and proposes surgical, reversible fixes by agreement.
