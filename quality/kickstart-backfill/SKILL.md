---
name: kickstart-backfill
description: One-shot skill to invoke once, on Day 1, to pre-fill the vault from 1 to 6 months of historical data (email, calendar, drive, chat). Creates retroactive people, project, decision, and meeting notes. Use when the user says "kickstart", "backfill", "initialize the vault", "pre-fill with the last 3 months".
---

# Skill: Kickstart Backfill

## ⚠️ Special skill — single use

This skill is meant to be invoked **once**, on Day 1 of the system. It takes time
(30–60 min depending on the window) and consumes context. It's the initial
investment to start with an already-living vault instead of from zero.

**NEVER invoke it as a scheduled task.**

## When to activate

- The user explicitly says: "kickstart", "backfill", "initialize the vault", "pre-fill with [period]".
- The user mentions wanting to start the second brain with an existing state of the world.

## Preflight

1. **Read `_CLAUDE.md`** and `00-inbox/MY-PROFILE.md`.
2. **Ask the user for 3 inputs**:
   - **Time window**: 1 month? 3 months? 6 months? (recommendation: start with 3 months).
   - **Sources to scan**: email only? + calendar? + drive? + chat? (recommendation: calendar + email first).
   - **Detail level**: exhaustive (all interactions) or strategic (top stakeholders + active projects only)? (recommendation: strategic for the first pass).

3. **Confirm the scope** before starting — show an estimate ("I'll scan ~N calendar events, ~N email threads, and create about N notes. ETA: ~X min. Go?").

## General strategy

⚠️ **Not a raw dump**. The goal is NOT to create 500 low-level notes. It's to
capture the user's **existing mental model**:
- Who are their N regular stakeholders?
- What are their N active projects?
- What are the N major decisions made recently?
- What are the N significant meetings?

Aim for **30–60 notes total**, not 500. Quality > volume.

## Process in 5 phases

### Phase 1 — Stakeholder mapping (15 min)

#### 1.1 Extraction from calendar
- Scan all events in the window.
- Count frequency per participant (excluding the user).
- Top 20 by frequency = candidates for person notes.

#### 1.2 Extraction from email
- Scan the threads in the window.
- Count threads per sender (filter out noreply / newsletters).
- Cross-reference with the calendar list.

#### 1.3 Presentation and validation
Show the user a **proposed shortlist**:

```
I identified 23 recurring people over the last 3 months.
Here are the top 15, ranked by interaction frequency:

1. Alex Rivera — 32 calendar events + 47 email threads — probably [direct-report]
2. [Name] — 18 events + 25 threads — probably [peer or manager]
3. ...

For each, I'll create a note in 02-people/ with:
- Filled frontmatter (inferred role, region, relationship)
- Timeline pre-filled with major meetings and threads
- Compiled truth ENRICHED only with what's observable (no speculation)

Do you want to:
A) Proceed on the 15?
B) Adjust the list (add/remove)?
C) More restrictive mode (top 10 strategic only)?
```

⚠️ **Ask for validation before creating.** This phase is critical: it's the base
of the strategic CRM.

#### 1.4 Create the person notes

For each validated person:

**Frontmatter**: fill with what's inferable
- `role`: from email signatures or calendar descriptions.
- `team`, `region`: best guess + flag if uncertain.
- `relationship`: ask the user if ambiguous.
- `last-interaction`: date of the last event/thread.
- `date` (first logged interaction): the oldest in the window.

**Compiled truth**: **stay minimal**. Include ONLY:
- Observable professional background (role, team, trajectory if visible in signatures/profiles).
- Explicit marker: *"Compiled truth to be enriched through future interactions"*.

**Do NOT include**:
- Psychological inferences.
- Working style (not enough reliable historical signal).
- Motivations (same).

**Timeline**: create entries **grouped by month** for the backfilled window:

```markdown
## Timeline

### 2026-03 (Backfilled — aggregated)
- **Meetings** (8): 5 team standups, 2 1-1s, 1 stakeholder review
  - Recurring topics: qualification script V2, training
  - See: [[04-meetings/2026-03-15-1to1-alex]], [[04-meetings/2026-03-22-...]]
- **Email threads** (12): mostly about [topic]
- **Observation**: *(backfilled, based on calendar/email only, to be enriched)*

### 2026-04 (Backfilled — aggregated)
...
```

⚠️ **Explicit `(Backfilled)` marker** on each entry so future-Claude knows these
are not real-time observations but a post-hoc reconstruction.

### Phase 2 — Project mapping (10 min)

#### 2.1 Detect candidate projects
Scan:
- Recurring topics in email threads (3+ threads on the same topic = candidate project).
- Recurring calendar events (e.g. weekly project sync).
- Drive folders with recent activity.
- Active chat channels (if connected).

#### 2.2 Validate with the user
```
Candidate projects detected:
1. "Qualification Script V2" — 12 events, 23 emails, active drive folder → STRONG
2. "Direct Report Coaching" — weekly recurrence with Alex → STRONG
3. "Process Unification" — 8 emails, 3 drive docs → MODERATE
4. "Tooling Migration" — a few mentions → WEAK

Which do you validate? Want to add any not detected automatically?
```

#### 2.3 Create the project notes

For each validated project, create `03-projects/<slug>.md` with:
- Frontmatter: `status: active` (default), ask the user for priority.
- Goal: ask the user (one sentence).
- Stakeholders: auto-detected from calendar/email.
- Timeline: key events detected in the window, grouped by month.
- Explicit `(Backfilled)` marker on retroactive timeline entries.

⚠️ **Ask the user for each project: "Goal in one sentence?"** — that's what turns a
descriptive note into a strategic one.

### Phase 3 — Historical decisions (10 min, optional)

#### 3.1 Detection
Scan emails and drive docs for keywords signaling decisions:
- "we've decided", "approved", "let's go with", "final decision".
- "reversal", "we're changing course", "stopping".
- Threads with "decision" in the subject.

#### 3.2 Validation
List candidate decisions to the user:
```
I detected 7 potential decisions in the last 3 months:

1. (2026-03-08) Centralize tier-1 in one hub — source: email thread [...] → major decision?
2. (2026-04-12) Onboarding training redesign — source: meeting [...]
...

Which should I log in 05-decisions/?
```

#### 3.3 Creation
For validated decisions, create `05-decisions/YYYY-MM-DD-<slug>.md` with:
- Frontmatter `status: implemented` (default, since retroactive).
- Decision, Context, Rationale sections (from email/meeting sources).
- `(Backfilled)` marker.
- **Important note**: *"Logged retroactively on YYYY-MM-DD via kickstart-backfill. Source materials reviewed but full rationale may be incomplete."*

### Phase 4 — Major meetings (10 min, optional)

For the meetings the user identifies as strategically important (max 10):
- Create notes in `04-meetings/`.
- If a transcript is available → ingest via the standard meeting-ingest process.
- Otherwise → minimal note with participants, topic, known outcome, marker `(Backfilled, no transcript)`.

**Anti-pattern**: don't create 50 meeting notes for the window. Only the key
meetings (stakeholder reviews, manager 1-1s, major decisions).

### Phase 5 — Knowledge baseline (5 min, optional)

If the user allows, create 1–3 `06-knowledge/` notes to crystallize emerging patterns:
- Observed anti-patterns.
- An applied framework.
- Major lessons learned detected.

⚠️ **Ask for validation** for each knowledge note. This is interpretive content and
must be validated by the user.

## Generate the backfill report

At the end, create a meta note: `06-knowledge/kickstart-backfill-YYYY-MM-DD.md`

```markdown
---
date: YYYY-MM-DD
type: backfill-report
tags: [meta, backfill]
ai-first: true
---

## For future Claude

Report of the kickstart backfill executed on [date]. Window covered: [start-date] →
[end-date]. This documents what was reconstructed retroactively vs. what was captured
in real-time afterward.

## Method

- Time window: [...]
- Sources scanned: [email | calendar | drive | chat]
- Mode: strategic | exhaustive

## Stats

- People created: N
- Projects created: N
- Decisions logged: N
- Meetings created: N
- Knowledge notes seeded: N

## Important caveats for future-Claude

All notes created in this operation are marked `(Backfilled)` in their timeline.
Behavioral observations and compiled truths are DELIBERATELY minimal — based only
on the observable (role, interaction frequency), not the interpretive.

**When using challenge-decision with this vault in the first weeks**: weight
backfilled notes lower than real-time notes. A backfilled note = ~30% of the weight
of a real-time note.

As the user works the system in real time, the notes enrich with real observations.
After ~6–8 weeks, the "backfill" effect is diluted.

## Links to created notes

[Auto-generated list of notes]
```

## Final report to the user

```
✓ Kickstart backfill complete
✓ Window: 2026-02-20 → 2026-05-20 (3 months)

Created:
- 14 people notes (02-people/) — top stakeholders identified
- 4 project notes (03-projects/) — all status: active
- 3 historical decisions (05-decisions/)
- 6 key meetings (04-meetings/)
- 1 knowledge note (observed anti-patterns — to validate)
- 1 meta report (06-knowledge/kickstart-backfill-2026-05-20.md)

⚠️ To do within the next 7 days to finalize:
1. Re-read the 14 people notes, complete the "Compiled truth" with your real mental model
2. Validate the "Goals" of the 4 projects (I put best-guesses to confirm)
3. Check that no people note is a duplicate (fuzzy match is limited in this mode)

The vault is now seeded. Day 1 operational.
Your first daily-brief will have material to cross-reference.
```

## Anti-patterns to avoid

❌ **Over-inferring** — no psychology, no invented motivations. Stick to observable.
❌ **Too many notes** — 30–60 max total. Not 500.
❌ **Forgetting the `(Backfilled)` marker** — critical so future-Claude weights correctly.
❌ **Skipping user validation** — each phase has its validation gate.
❌ **Trying to resolve everything in one pass** — it's OK to leave stubs to enrich.
❌ **Including speculative decisions** — if a decision isn't explicitly documented, don't log it.

## Alternative modes

### "Light" mode (15 min)
For a faster start:
- Skip phases 3 and 4.
- Limit phase 1 to top 10 people.
- Limit phase 2 to top 3 projects.

### "Heavy" mode (60–90 min)
For a very rich start (vault at 100+ notes):
- Extend the window to 6 months.
- Include all stakeholder meetings.
- Create knowledge notes per project (retroactive mini-PRD).

### "Topic-focused" mode
To start focused on one specific project:
- Skip generic people.
- Deep-dive one project: all meetings, all decisions, all involved stakeholders.
- Output: an ultra-documented project from Day 1.

Ask the user for their mode at preflight.

## Once the skill is done

This skill is **archivable**. Once used:
- You can disable the skill (move it out of `.claude/skills/` for clarity).
- Or keep it for reference (in case the user wants to re-backfill an older period later).

Typical invocation: once on Day 1, sometimes a second time after 6 months to ingest
a missed period (if there was a gap or the user wants to extend retroactively).
