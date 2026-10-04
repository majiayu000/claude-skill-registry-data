---
name: capa
description: |
  Corrective and Preventive Action process for fixing broken processes. Use when:
  - A delivered feature doesn't work despite having process skills in place
  - The same failure pattern recurs (you've seen this before)
  - "Done" was claimed but it doesn't actually work
  - A skill or gate failed to fire when it should have
  - Process was followed on paper but missed reality

  Trigger: /capa [what's broken], or when user says "figure out why X isn't working",
  "why did this fail again", "our process didn't catch this", "do a retrospective on X"

  NOT for: simple bugs (use systematic-debugging), first-time implementation (use dev-process),
  or design exploration (use brainstorming). CAPA is for when the PROCESS itself failed.
---

# CAPA: Corrective and Preventive Action

## The Iron Law

```
FIX THE PROCESS FIRST.
THEN USE THE FIXED PROCESS TO FIX THE DEFECT.
```

If you fix the defect before fixing the process, you lose leverage to fix the root cause.
The defect fix is the PROOF the process works — not the primary deliverable.

## Is this a CAPA? — Triage BEFORE opening a record

Not every annoyance is a CAPA. Use this bright line:

| Signal | Route |
|--------|-------|
| A skill/gate/process **failed to fire** when it should have | **CAPA** — open a record |
| Same failure pattern has happened **before** | **CAPA** — open a record |
| "Done" was claimed but **doesn't work** | **CAPA** — open a record |
| Annoyance, one-off bug, slow-loading UI, small paper-cut | **Friction** → capture-mcp or friction-graph |
| Kyle said "that was friction" or "log this for later" | **Friction** → capture-mcp |
| Idea, follow-up, bookmark, todo | **capture-mcp** (not a CAPA) |

If in doubt, ask: *"Did a skill fail to do its job?"* If no, it's friction. Don't inflate friction into CAPA — that's how the `recurring_patterns` view gets useless.

## Database

**Canonical path:** `/mnt/pi-data/capa/capa.db` (host-persistent, nightly-backed-up, no permission prompts)

```bash
CAPA_DB="sqlite3 /mnt/pi-data/capa/capa.db"
$CAPA_DB "YOUR QUERY"
```

Schema is in `references/schema.sql`. The DB is initialized; don't recreate it. If it is ever lost, restore from `gdrive:orangepi-claude-backup/pi-data/capa/` or re-init with:
```bash
cat references/schema.sql | sqlite3 /mnt/pi-data/capa/capa.db
```

Log every phase transition to the `changelog` table. This is append-only — never delete rows.

**DO NOT** use `~/.claude/capa/` — that path triggers permission prompts and is not backed up cleanly. It is the Claude Code config dir, not a data dir.

## The Eight Phases

You MUST complete each phase before proceeding. Create tasks for tracking.

```
Phase 1: DETECT ──> Phase 2: INVESTIGATE ──> Phase 3: RESEARCH ──> Phase 4: DESIGN
                                                                        │
Phase 8: CLOSE <── Phase 7: RE-EXECUTE <── Phase 6: VERIFY <── Phase 5: IMPLEMENT
```

### Phase 1: DETECT — Document the Failure

**Goal:** Create a clear record of what went wrong.

1. **Document the gap:**
   - What was expected to happen?
   - What actually happened?
   - Who noticed, and when?
   - Is there a post-mortem or failure report? (Read it fully.)

2. **Create CAPA record:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "
     INSERT INTO capa_records (title, trigger_description, status, severity)
     VALUES ('[short title]', '[full description]', 'open', '[critical|high|medium|low]');
   "
   ```

3. **Log to changelog:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "
     INSERT INTO changelog (capa_id, phase, action, details)
     VALUES ([id], 'detect', 'CAPA opened', '[summary]');
   "
   ```

**Output:** CAPA record ID. Use this ID for all subsequent phases.

---

### Phase 2: INVESTIGATE — Trace Process Failure

**Goal:** Map every failure to the skill or gate that should have prevented it.

<HARD-GATE>
Do NOT propose fixes yet. Investigation only. If you catch yourself proposing solutions,
STOP and return to tracing the failure chain.
</HARD-GATE>

1. **Trace the failure chain** using the 5 Whys:
   - What broke? → Why? → What should have caught it? → Why didn't it? → What's the root cause in the process?

2. **Map each failure to a skill/gate:**

   | Failure | Skill That Should Have Caught It | Why It Didn't Fire |
   |---------|----------------------------------|--------------------|
   | [what went wrong] | [which skill] | [why it was skipped/unavailable/ineffective] |

3. **Categorize root causes** and log them:
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "
     INSERT INTO root_causes (capa_id, description, skill_that_failed, why_it_failed, category)
     VALUES ([id], '[description]', '[skill name]', '[why]', '[category]');
   "
   ```

   Categories: `spec_written_from_memory`, `wrong_code_path`, `mock_tested_not_real`,
   `tests_never_ran`, `self_reported_verification`, `skill_not_available`,
   `skill_not_enforced`, `no_acceptance_criteria`, `speed_over_correctness`

4. **Check for patterns** — has this root cause appeared before?
   ```bash
   sqlite3 -header -column /mnt/pi-data/capa/capa.db "SELECT * FROM recurring_patterns"
   ```

5. **Update status:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "UPDATE capa_records SET status='investigating', category='[primary category]' WHERE id=[id]"
   ```

**Output:** Root cause map with skill-to-failure mapping. Present to user before proceeding.

---

### Phase 3: RESEARCH — External + Internal Best Practices

**Goal:** Find proven solutions before designing your own.

1. **External research** (Perplexity):
   - Query industry best practices for each root cause category
   - Look for how top engineering orgs (Google SRE, Amazon COE) solve this class of problem
   - Use `perplexity_ask` with `max_tokens_per_page: 256`, `max_results: 3`

2. **Internal research:**
   - **Kyle's memory:** Search `~/.claude/projects/-home-orangepi/memory/` for related past decisions
   - **Kyle's preferences:** Check CLAUDE.md and MEMORY.md for relevant preferences
   - **Previous CAPAs:** Query the DB for similar root cause categories
   - **Existing skills:** Read relevant skill files to understand current gaps
   - **Shared documents:** Check if Kyle has shared articles, templates, or reference docs

3. **Log findings:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "
     INSERT INTO research_findings (capa_id, source_type, finding, citation)
     VALUES ([id], '[perplexity|github|memory|article|previous_capa|skill_review]',
             '[finding]', '[url or reference]');
   "
   ```

4. **Update status:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "UPDATE capa_records SET status='researching' WHERE id=[id]"
   ```

**Output:** Research findings with citations. Synthesize into 3-5 actionable insights.

---

### Phase 4: DESIGN — Design the Process Fix

**Goal:** Design specific changes to skills, gates, or enforcement that address each root cause.

1. **For each root cause, propose a fix:**
   - What skill/gate needs to change?
   - What's the specific change? (new skill, modified skill, new enforcement mechanism)
   - How will it prevent recurrence?

2. **Propose 2-3 approaches** with trade-offs (like brainstorming):
   - Option A: [lightest touch — modify existing skill]
   - Option B: [moderate — new gate or enforcement]
   - Option C: [heaviest — new skill or architectural change]
   - Recommend one with reasoning

3. **Get Kyle's approval:**
   > "Here's the process fix design. [Present options.] I recommend Option [X] because [reason]. Approve to proceed?"

4. **Update status:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "UPDATE capa_records SET status='designing' WHERE id=[id]"
   ```

<HARD-GATE>
Do NOT implement process changes without Kyle's approval on the design.
</HARD-GATE>

**Output:** Approved process fix design.

---

### Phase 5: IMPLEMENT — Build the Process Fix

**Goal:** Build the approved process changes. This is the primary deliverable.

1. **Implement each approved change:**
   - New or modified skill files
   - New gates or enforcement mechanisms
   - Config changes
   - DB schema updates (if needed)

2. **Log each change:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "
     INSERT INTO process_changes (capa_id, change_type, description, files_changed)
     VALUES ([id], '[new_skill|modified_skill|new_gate|new_enforcement|config_change]',
             '[what changed]', '[\"file1.md\", \"file2.md\"]');
   "
   ```

3. **Update status:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "UPDATE capa_records SET status='implementing' WHERE id=[id]"
   ```

**Output:** Working process changes, committed if applicable.

---

### Phase 6: VERIFY — Dry-Run Against Original Failure

**Goal:** Prove the new process would have caught the original failure.

1. **Walk through the original failure scenario** with the new gates in place:
   - At step X, the new gate would have fired because [reason]
   - The failure would have been caught at [phase] instead of reaching production

2. **For each root cause, verify the fix addresses it:**

   | Root Cause | Fix Applied | Would It Have Caught It? | Evidence |
   |-----------|-------------|--------------------------|----------|
   | [cause 1] | [fix 1] | Yes/No | [how you verified] |

3. **Mark changes as verified:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "UPDATE process_changes SET verified=1 WHERE capa_id=[id]"
   ```

4. **Update status:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "
     UPDATE capa_records SET status='verifying', process_fixed=1 WHERE id=[id]
   "
   ```

**Output:** Verification table showing each root cause is addressed.

---

### Phase 7: RE-EXECUTE — Fix Original Defect with New Process

**Goal:** Use the new process to fix what originally broke. This proves the process works.

1. **Invoke the appropriate process skills:**
   - If the failure was a spec error → use `brainstorming` to re-spec correctly
   - If the failure was implementation → use `dev-process` pipeline
   - If the failure was testing → use `test-driven-development`
   - The point: follow the FIXED process, not a shortcut

2. **The new process gates should fire naturally:**
   - If they don't fire, the process fix is incomplete → go back to Phase 5
   - If they fire but don't catch the issue → go back to Phase 4

3. **Update status:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "UPDATE capa_records SET status='re-executing' WHERE id=[id]"
   ```

**Output:** The original defect, fixed correctly using the new process.

---

### Phase 8: CLOSE — Record and Learn

**Goal:** Close the loop. Log outcome, update records, save learnings.

1. **Update CAPA record:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "
     UPDATE capa_records SET
       status='closed',
       closed_at=datetime('now'),
       defect_fixed=1,
       outcome='[summary of what changed and what was learned]'
     WHERE id=[id]
   "
   ```

2. **Final changelog entry:**
   ```bash
   sqlite3 /mnt/pi-data/capa/capa.db "
     INSERT INTO changelog (capa_id, phase, action, details)
     VALUES ([id], 'close', 'CAPA closed', '[lessons learned summary]');
   "
   ```

3. **Save to memory** if the learning is durable:
   - Process changes that affect future work → save to claude-mem or memory file
   - One-off fixes → skip memory, the DB record is enough

4. **Check stats** — how are we trending?
   ```bash
   sqlite3 -header -column /mnt/pi-data/capa/capa.db "SELECT * FROM category_stats"
   sqlite3 -header -column /mnt/pi-data/capa/capa.db "SELECT * FROM recurring_patterns"
   ```

**Output:** Closed CAPA record. Brief summary to Kyle.

---

## Red Flags — STOP and Return to Earlier Phase

| Thought | Reality | Go Back To |
|---------|---------|------------|
| "Let me just fix the defect quickly first" | Process fix is the primary deliverable | Phase 4 |
| "The process fix is overkill for this" | If the process failed, it needs fixing | Phase 2 |
| "I know the fix without researching" | Past knowledge may be outdated or wrong | Phase 3 |
| "This root cause is too small to track" | Small gaps compound. Log everything. | Phase 2 |
| "The same skill exists, it just wasn't used" | Then enforcement is the root cause | Phase 2 |
| "Let me skip verification, the fix is obvious" | Obvious fixes fail silently | Phase 6 |

## Quick Queries

Check open CAPAs:
```bash
sqlite3 -header -column /mnt/pi-data/capa/capa.db "SELECT * FROM capa_summary WHERE status != 'closed'"
```

Check recurring patterns:
```bash
sqlite3 -header -column /mnt/pi-data/capa/capa.db "SELECT * FROM recurring_patterns"
```

Full stats:
```bash
sqlite3 -header -column /mnt/pi-data/capa/capa.db "
  SELECT COUNT(*) as total,
    SUM(CASE WHEN status='closed' THEN 1 ELSE 0 END) as closed,
    SUM(CASE WHEN process_fixed THEN 1 ELSE 0 END) as process_fixed,
    SUM(CASE WHEN defect_fixed THEN 1 ELSE 0 END) as defect_fixed
  FROM capa_records
"
```

Which skills fail most:
```bash
sqlite3 -header -column /mnt/pi-data/capa/capa.db "
  SELECT skill_that_failed, COUNT(*) as fails
  FROM root_causes WHERE skill_that_failed IS NOT NULL
  GROUP BY skill_that_failed ORDER BY fails DESC
"
```
