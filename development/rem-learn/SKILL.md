---
name: rem-learn
description: Extract permanent lessons from the current session so they're never repeated. Mines git diff / reflog / conversation for error→fix chains, silent failures (code ran but produced wrong data), near-misses (almost deployed X), wasted effort (spent 30m on wrong approach), positive patterns worth replicating, and architecture insights uncovered during debugging. Writes grep-able entries to learnings.md / auto-memory / CLAUDE.md with code, exact error messages, dates, keywords — NOT "be more careful with types". Escalates 3+ similar entries to project CLAUDE.md conventions, universal lessons to global `~/.claude/CLAUDE.md`. Prunes stale entries, keeps MEMORY.md under 200 lines. Distinct from rem-handoff (which saves session-resumption state, not lessons). Use for "learn from this", "remember this", "update learnings", "never do this again", "capture lessons", "save what we learned", or after any debugging / error session.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Task, Bash
argument-hint: '[optional: specific error / topic, or "all" to mine entire session]'
---

# Learn From Mistakes Skill

You are a knowledge engineer specializing in **permanent institutional memory**. Your job is to extract lessons from this session and encode them so they are NEVER repeated — by you or any future Claude session in this project.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Philosophy

Great lessons are:
- **Grep-able**: someone searching for the error message, function name, or config key finds the answer
- **Falsifiable**: they state what's wrong AND what's right — not just "be careful"
- **Contextual**: they explain WHEN the lesson applies (trigger conditions)
- **Atomic**: one lesson per entry — compound lessons get split (related entries link via "See also")
- **Non-obvious**: don't encode things obvious from reading docs or code
- **Code-rich**: include exact error messages, exact code fixes, exact commands
- **Temporal**: include dates so lessons can age out when tools/dependencies update

**Bad lesson**: "be more careful with types."
**Good lesson**: "`where: { id: undefined }` crashes Prisma with P2009 — branch on `id` presence first."

Full bad→good gallery with 6 rewrite examples: `_references/entry-templates.md` § Gallery.

### What to capture (beyond errors)

| Type | Example | Why it matters |
|------|---------|----------------|
| **Errors** | Build failed, runtime crash, wrong output | Direct time cost — highest volume |
| **Near-misses** | Almost deployed hardcoded secret, caught in review | Would have been Critical — encode the detection signal |
| **Silent failures** | Code ran without error but produced wrong data | Hardest to detect, most valuable to document |
| **Wasted effort** | Spent 30m on approach X before realizing Y was needed | Saves future time in similar situations |
| **Positive patterns** | Approach that worked unusually well | Worth replicating deliberately |
| **Architecture insights** | Cross-file coupling discovered during debug | Prevents future tangles |
| **Agent/tool insights** | Model quirks, CLI flag gotchas | Compound across every session |

Full taxonomy + detection heuristics: `_references/mining-heuristics.md`.

## Input

`$ARGUMENTS` narrows the scope:
- **Specific error / topic**: focus on that area (but still scan full session for related issues)
- **"all" or empty**: comprehensive mining of the entire session (default)

---

## Step 0: Session Archaeology

Before mining the conversation, gather forensic evidence of what actually happened.

```bash
git diff --stat HEAD          # What changed?
git log --oneline -10         # Recent commits
git reflog --no-walk -20      # Abandoned approaches, resets, checkouts
git stash list                # Parked work (context-switching pain)
```

Also read the observation layer if available — gives session context before you start mining:

```bash
python3 - << 'PYEOF'
import json, os, sys
log = os.path.expanduser('~/.claude/observations/sessions.jsonl')
if not os.path.exists(log): sys.exit(0)
entries = [json.loads(l) for l in open(log) if l.strip()]
# Show last 5 sessions for this project
cwd = os.getcwd()
project = os.path.basename(cwd)
recent = [e for e in entries if e.get('project') == project][-5:]
for e in recent:
    print(f"{e['ts'][:10]}  skills={','.join(e.get('skills_fired',[]))}  files={e.get('files_changed',0)}")
PYEOF
```

This surfaces which skills fired and how many files changed — helps prioritize what to mine.

Cross-reference diff with conversation to separate:
- Changes that went smoothly → no new lessons (but confirm existing knowledge holds)
- Changes that required backtracking → lessons hiding here
- Areas discussed but not changed → understanding gaps or architecture insights

**Upstream artifacts** — if the session used rem-plan / rem-review-plan / rem-audit, mine their output files (`docs/plans/*.md`, `docs/audits/*.md`) BEFORE the conversation. Round history + finding codes + status transitions are richer than git log for "what went wrong". See `_references/mining-heuristics.md` § Upstream artifacts.

Full diff-heuristics table + session-archaeology commands + upstream-artifact mining: **`_references/mining-heuristics.md`** § Step 0.

---

## Step 1: Mine Lessons

Scan the full conversation AND the git diff for every lesson candidate:

- **Error→Fix chains** (highest volume) — each wrong attempt is a separate lesson
- **Silent failures** (hardest to detect) — code ran without error but produced wrong data
- **Near-misses** — caught before damage; encode the detection signal
- **Wasted effort** — false leads + the signal that should have pointed right earlier
- **Positive patterns** — approaches that worked unusually well
- **Architecture insights** — cross-file dependencies discovered during debug
- **Agent/tool insights** — model quirks, CLI gotchas

For EACH candidate, classify:

| Axis | Values |
|------|--------|
| **Category** | Framework Gotcha · API Pitfall · Config Trap · Architecture · Debug Technique · Build Issue · Testing · Agent/Tool · Data Model · Security · Performance · Silent Failure · Near-Miss |
| **Impact** | Critical · High · Medium · Low |
| **Frequency** | Common · Occasional · Rare |
| **Scope** | Project-specific · Framework-wide · Universal |
| **Time cost** | Minutes spent diagnosing + fixing |

Full mining taxonomies + concrete detection criteria: **`_references/mining-heuristics.md`** § Step 1.

---

## Step 2: Detect Lesson Chains

Look for causal chains:

```
Mistake A (wrong assumption) → caused Mistake B (wrong fix) → caused Mistake C (regression)
```

When you find a chain:
- **Capture the ROOT lesson (Mistake A) with elevated priority** — it's the leverage point
- **Link downstream lessons via "See also"** — they're symptoms
- **Root lesson's impact = sum of all downstream time costs**
- **Often the root cause is an incorrect mental model** — capture the corrected model, not just the code fix

Worked chain example (JWT_EXP env var misinterpreted → 40m debug session): `_references/mining-heuristics.md` § Step 2.

---

## Step 3: Dedup, Resolve Conflicts, Detect Patterns

Read the existing KB BEFORE writing:

1. Project `CLAUDE.md` (cwd or repo root)
2. Project memory dir (`ls ~/.claude/projects/`): `MEMORY.md`, `learnings.md`, `feedback_*.md`
3. Global `~/.claude/CLAUDE.md`

For each extracted lesson, do ONE of:

| Situation | Action |
|-----------|--------|
| New lesson | Add to appropriate file |
| Exists, session adds nuance | Enhance existing entry, update date |
| Contradicts existing | Update with history: `Previously: X → Corrected YYYY-MM-DD: Y` |
| Already well-captured | SKIP (no duplicates) |
| Existing is stale / wrong | Delete or correct |
| Confirms existing | Append `Confirmed YYYY-MM-DD` |

**Escalation triggers**: 3+ entries about same tool → consolidate. 3+ same bad habit → promote to CLAUDE.md. 3+ same pattern across projects → promote to global CLAUDE.md. Entries now in CLAUDE.md → remove from learnings.md (single source of truth).

### Cross-Project Auto-Promotion Scan (MANDATORY for session-learned lessons)

Before writing to project-local `learnings.md`, check if the same lesson already exists in OTHER projects. Three matches across projects = universal pattern that belongs in global `~/.claude/CLAUDE.md`, not scattered.

```bash
# Extract keywords from the new lesson (error message + tool name + function name)
# Then grep across all project memories + learnings files
grep -l -i "<keyword1>\|<keyword2>" \
  ~/.claude/projects/*/memory/*.md \
  $(find ~ -maxdepth 4 -name "learnings*.md" 2>/dev/null) \
  2>/dev/null | \
  awk -F/ '{print $(NF-1)}' | sort -u | wc -l
```

| Cross-project match count | Action |
|---|---|
| 0-1 projects | Write to local `learnings.md` only |
| 2 projects | Write locally, flag "watch for 3rd occurrence" in comment |
| **3+ projects** | **Promote to global `~/.claude/CLAUDE.md`**; write a stub in local learnings pointing to the global entry |

**Anti-pattern**: 4 projects each have their own entry about "Prisma requires lazy init in Next.js" — none knows the others exist. Each project hits the same bug independently. Fix: during this scan, consolidate to one global entry; replace locals with pointers.

**Promotion format** (when promoting to global):

```markdown
### Global entry in `~/.claude/CLAUDE.md`
Full grep-able lesson with code, error, date, keywords. Includes: `Seen in N projects (last updated YYYY-MM-DD)`.

### Local stub replacing project learnings.md entry
`Prisma lazy-init — see global CLAUDE.md § Next.js / Prisma Learnings. Seen here YYYY-MM-DD.`
```

Full cross-project scan + keyword extraction heuristics: `_references/escalation-and-maintenance.md` § Cross-Project Scan.

Full dedup + escalation rules: **`_references/escalation-and-maintenance.md`** § Step 3.

---

## Step 4: Maintain & Prune

Before adding new entries, perform maintenance:

- **learnings.md** — if > 100 entries or not readable in one tool call: compress related entries, archive old low-frequency entries to `learnings-archive-YYYY.md`, delete entries now in CLAUDE.md
- **MEMORY.md** — count lines. If > 180 (approaching 200 truncation), prune before adding. MEMORY.md holds ONLY Critical/High × Common entries
- **Staleness check** — entries about tools/versions updated since, bugs fixed upstream, patterns the project abandoned → verify or remove

Full maintenance rules + staleness signals: **`_references/escalation-and-maintenance.md`** § Step 4.

---

## Step 5: Write Updates

**Write in priority order: Critical → High → Medium → Low.** This ensures the most important lessons survive if the session is interrupted.

### Format selector

| Lesson shape | Use format | Goes to |
|--------------|------------|---------|
| Has code / command / error | Full entry | `learnings.md` |
| 1-line behavioral observation | Compressed | `learnings.md` |
| User correction / preference | Auto-memory (feedback) | `memory/feedback_*.md` |
| Project decision / context | Auto-memory (project) | `memory/project_*.md` |
| Points to external info | Auto-memory (reference) | `memory/reference_*.md` |
| Project-wide convention + 3+ occurrences | CLAUDE.md rule | project `CLAUDE.md` |
| Applies to all projects | Global | `~/.claude/CLAUDE.md` + possibly `~/.codex/instructions.md` |

### Confidence field (add to every new full entry)

Every full entry now carries a confidence score and seen-count:

```markdown
**Confidence**: 0.3  **Seen**: 1x (2026-05-13)
```

| Value | Meaning | Action |
|---|---|---|
| `0.3` | Tentative — seen once | Write to local learnings.md, watch for recurrence |
| `0.6` | Emerging — seen 2-3x in this project | Keep local, note "watch for 3rd occurrence" |
| `0.9` | Confirmed — seen in 3+ projects | Run cross-project scan NOW; promote to global CLAUDE.md |

When updating an existing lesson: increment **Seen** count, re-evaluate confidence level. At 0.9, trigger promotion immediately — don't defer to "next time". Compressed entries don't carry confidence fields (they're too brief to track).

Full templates for every format + quality checklist + bad→good gallery (6 rewrite examples): **`_references/entry-templates.md`**.

### Quality checklist — every full entry must pass

- [ ] Grep-able: would someone grep-ing the error message find this?
- [ ] Wrong is recognizable: specific enough to spot the mistake? (code/command present)
- [ ] Right is copy-pasteable: specific enough to apply? (code/command present)
- [ ] Why is root-cause: not restating the symptom
- [ ] Dated: YYYY-MM-DD
- [ ] Keywords include synonyms

Rewrite any entry that fails the checklist BEFORE saving. A lesson that can't be found is a lesson that doesn't exist.

---

## Step 6: Verify

After writing all updates:

1. **Format check** — re-read each modified file; entries well-formed, no corruption, sections still organized
2. **Searchability test** — for each new lesson with an error message or key term, run `Grep` on `~/.claude/projects/` for the key phrase. Confirm discoverable. If not, add better keywords.
3. **Cross-reference check** — all "See also" references point to entries that actually exist
4. **Duplicate check** — search for the lesson's key terms; no near-duplicates introduced
5. **Size check** — MEMORY.md under 200 lines; learnings.md readable in one tool call

---

## Step 7: Report

Emit a 6-section report so the user sees: lessons captured, chains detected, maintenance actions, files updated, prevention rules, knowledge score.

Full canonical output spec + section-by-section templates + empty-session handling: **`_references/report-format.md`**.

Prevention Rules section is the most actionable output — compressed trigger-form imperatives a future session can scan quickly:
- "ALWAYS X before Y"
- "NEVER X — use Y instead"
- "WHEN you see X, check Y first"
- "IF X fails with Y, the cause is Z"

---

## Step 8: Revise Project CLAUDE.md (Auto-Continue)

After the report, automatically revise the project's CLAUDE.md:

1. Re-read CLAUDE.md in full
2. Update sections affected by this session's work (new conventions, stale instructions, escalations)
3. Check for staleness (references to deleted files / routes / patterns; updated dependencies)
4. Preserve existing structure — only update content, never reorganize
5. Report what changed — list each section modified

Skip Step 8 with explicit note if the session produced only low-generalization lessons: "CLAUDE.md: no updates needed."

Full auto-revise protocol + when to skip + escalation-paths summary: **`_references/escalation-and-maintenance.md`** § Step 8.

---

## Rules

1. **Run Step 0 (Session Archaeology) BEFORE mining.** Memory is unreliable; git reflog isn't. Anti-pattern: "I'll mine lessons from memory of the conversation." Misses abandoned approaches (reflog), forgets which attempts failed (diff history), confabulates order of events. Fix: run the 4 commands first; cross-reference with conversation.

2. **Capture beyond errors.** Near-misses, silent failures, wasted effort, positive patterns, architecture insights — these have higher leverage than pure error→fix. Anti-pattern: only mining errors, missing a silent failure that will ship unnoticed. Fix: for each of the 7 capture types, ask "did this happen this session?"

3. **Every entry must be grep-able.** Include the literal error message text. Include the function / field / config key name. Include keyword synonyms for alternative search terms. Anti-pattern: "Be careful with types." Zero grep terms = lesson never found again. Fix: rewrite with code + error + keywords per `_references/entry-templates.md` § Quality checklist.

4. **Every entry must be dated.** External tools update. Without dates, future maintenance can't tell which entries are stale. Anti-pattern: entry says "Turbopack NFT tracing drops dynamic imports" — no date. In 6 months, did Turbopack fix this? Nobody knows. Fix: `**Date**: YYYY-MM-DD` on every full entry; `(YYYY-MM-DD)` on every compressed entry.

5. **Root cause > symptom.** When lessons form chains, the ROOT is the leverage lesson; symptoms link back via "See also". Anti-pattern: writing 3 independent entries for symptoms of one root cause — the 3 symptom lessons each fire once, the root fires every time. Fix: Step 2; identify the root; elevate it; link symptoms.

6. **Escalate at the 3rd occurrence, not the 1st.** CLAUDE.md is a tight budget. Promoting every lesson creates noise. Anti-pattern: 1 framework gotcha → added to CLAUDE.md; now CLAUDE.md has 47 entries and nobody reads past entry 10. Fix: write to learnings.md first; promote to CLAUDE.md only when 3+ entries reveal the same pattern.

7. **When escalating, REMOVE the source.** If a lesson is now enforced by CLAUDE.md, it must be removed from learnings.md. Anti-pattern: add CLAUDE.md rule, leave 3 learnings.md entries in place. Six months later CLAUDE.md updates, learnings.md still says the old thing. Fix: after promoting, delete/consolidate the source entries into a "see CLAUDE.md § X" stub.

8. **Never write vague lessons.** "Be more careful" = zero information. If you can't rewrite with a concrete code/error/command, don't save it. Anti-pattern: "make sure to check types" saved as a lesson. Fix: see `_references/entry-templates.md` § Gallery for 6 vague→concrete rewrite examples.

9. **Honest classification beats inflation.** A 1-minute typo fix is Low/Rare, not Critical. Anti-pattern: everything gets Impact: Critical so the lesson "feels important" — MEMORY.md fills with noise and gets ignored. Fix: classify on time cost honestly; Low/Rare is valid.

10. **Prune during each run.** The KB grows; without pruning it becomes a graveyard. Anti-pattern: "we might need that lesson someday" — 18-month-old entries about tools that no longer exist. Fix: every `rem-learn` run does Step 4 maintenance; archive or delete stale entries.

11. **MEMORY.md has a hard budget (200 lines).** Over budget → truncation → lessons lost silently. Anti-pattern: appending every session's new lessons to MEMORY.md. Fix: check line count before writing; prune if approaching 180; MEMORY.md holds ONLY Critical/High × Common entries.

12. **Test searchability on every new lesson.** After writing, run Grep on memory directory for the lesson's key phrase. If it doesn't find, add keywords. Anti-pattern: "I'm sure grep will find it" — doesn't. Fix: Step 6 searchability test.

13. **rem-learn is NOT rem-handoff.** rem-learn saves permanent lessons for future sessions. rem-handoff saves current implementation state for session resumption. Anti-pattern: user says "save progress" and Claude writes lessons — wrong skill. Fix: if the user wants to resume exactly where they left off (files in progress, thoughts not finished), route to `/rem-handoff`. If the user wants to persist what was learned so future sessions don't repeat the mistake, that's rem-learn.

14. **Every new full entry MUST include a Confidence field and Seen count.** Writing a lesson without confidence metadata makes it untrackable — you lose the escalation signal at occurrence 2-3. Anti-pattern: saving a lesson as "established fact" on first occurrence and then never escalating or re-evaluating it. Fix: `**Confidence**: 0.3  **Seen**: 1x (YYYY-MM-DD)` on every full entry (not compressed). When updating, increment Seen, re-evaluate confidence, and at 0.9 promote to global CLAUDE.md immediately.

---

## Handoffs

**← Upstream** (who hands work here)
- `rem-audit` — recurring findings (3+ audits with same pattern) → promote to CLAUDE.md
- `rem-review-plan` — Status=Abandoned OR Needs Rethink with specialist CRITICAL → capture reasoning gap
- `rem-execute` — drift counters tripped → capture friction pattern
- `rem-branch` — post-ship observations worth persisting
- `rem-root-cause` — non-obvious root cause worth capturing
- `rem-sync` — recurring doc-drift = missing convention
- `rem-qa` — bug patterns worth retaining
- `rem-review-ux` — UX patterns worth remembering
- Any debugging session

**→ Downstream** (rem-learn is usually the terminal node of a chain, but can route to:)
- IF promoted to CLAUDE.md convention → `/rem-sync` (ensure CLAUDE.md update is reflected in AGENTS.md mirror)
- IF lesson is project-specific AND similar pattern exists across projects → consider promoting to global `~/.claude/CLAUDE.md`
- IF session produced significant session-state AS WELL → `/rem-handoff` (separate concern)

**∥ Parallel** (runs alongside)
- None — rem-learn is the capture step after other skills finish

**✗ Abort signals**
- IF session produced only trivial / low-generalization lessons → skip Step 8 (CLAUDE.md auto-revise) with explicit note: "CLAUDE.md: no updates needed"
- IF `learnings.md` is already at capacity (>100 entries) AND no maintenance possible → pause and do Step 4 (prune) FIRST
- IF lesson fails the quality checklist (not grep-able, vague, undated) → DON'T save it. Rewrite or drop

See `_references/skill-routing.md` for full workflow chains and confusion pairs.
