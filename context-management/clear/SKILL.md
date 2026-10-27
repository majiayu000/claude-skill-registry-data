---
description: Safely flush context and resume fresh - distills session state before clearing
argument-hint: ""
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash(date:*)
---

Persist session state then seamlessly resume work. The user should not notice this happening.

**Emergency mode** (compacting/prompt-too-long): Skip reads, distill from in-context memory only, go to Step 3.

---

## Steps

### Step 0: Reset gate + get date

```bash
date +"%m%d%y %H:%M" && rm -f ".claude/logs/.quality-gate-active" ".claude/logs/.session-blocks-$(date +"%m%d-%H")" ".claude/logs/.tool-call-count" ".claude/logs/.compaction-occurred"
```

### Step 1: Read state (parallel, skip in emergency)

Read simultaneously: `.claude/memory.md` + `Daily Notes/MMDDYY.md`

### Step 2: Distill session (from in-context memory)

Extract and compress using **restorable compression** — preserve retrieval paths so the resumed session can restore full context from compressed form:

1. **Task** — one sentence
2. **Done/remaining** — 2-4 bullets, conclusions not process
3. **Decisions** — one line each, WHAT+WHY not HOW
4. **Learnings** — rules/facts for knowledge-nominations
5. **Files touched** — full paths of every file read or modified (not just modified — include key files *read* that informed decisions). These are retrieval anchors for the resumed session.
6. **Active references** — URLs, API endpoints, external resources consulted. Drop content, keep the pointer.
7. **Next action** — precise, actionable instruction including which file(s) to read first

### Step 3: Write handoff to daily note

Append (or create new daily note if none exists):

```markdown
## Session Handoff — HH:MM

**Task:** [one sentence]
**Done:** [bullets]
**Remaining:** [bullets]
**Decisions:** [bullets]
**Files:** [full paths — both modified and key reads]
**Refs:** [URLs, external resources — pointers only, no content]
**Next:** [precise action + which file(s) to read first]
```

### Step 4: Update memory.md (only if changed)

New priorities, threads, decisions → edit. Nothing changed → skip.

### Step 5: Promote and nominate learnings (only if discovered)

**Two-tier promotion:**

**Tier 1: Immediate promotion to `knowledge-base.md`** (high-confidence rules):
- User overrides (explicitly corrected something)
- Empirical facts (verified through testing or data)

Write directly with `[Source: User directive MMDDYY]` or `[Source: Empirical MMDDYY]`.

**Tier 2: Nominate to `knowledge-nominations.md`** (lower-confidence):
- Agent inferences (patterns observed but not confirmed)
- Hypotheses (things that seem true but need more evidence)

Append: `- [MMDDYY] /clear: [learning] | Evidence: [source]`

**Rule: When in doubt, promote. A rule in knowledge-base.md that gets corrected later is better than a rule in nominations that never gets seen.**

### Step 6: Auto-resume (restorable decompression)

Do NOT output a resumption prompt. Do NOT ask the user anything. Instead:

1. Re-read `.claude/memory.md` and `.claude/knowledge-base.md` (compressed context reload)
2. Re-read the daily note handoff you just wrote (for the Next action)
3. **Restore from retrieval anchors** — re-read the file(s) specified in the **Next** field and any critical files from the **Files** list that the next action depends on. This is the decompression step: the handoff told you *what* happened; re-reading the files restores *how* to continue.
4. **Immediately execute the Next action** — pick up exactly where you left off

The user should experience a brief pause, then work continuing seamlessly. No visible "clearing" or "resuming" messages. Just keep working.

Target: 5-7 tool calls, <30 seconds. Emergency: 2-3 calls, <15 seconds.
