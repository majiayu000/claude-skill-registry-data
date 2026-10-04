---
name: meeting-ingest
description: Ingests a meeting transcript (video-call transcript, raw notes, transcribed audio) and produces a structured note in 04-meetings/ with decisions, action items, dynamics, and participants. Automatically updates impacted people notes and the daily note. Use when the user shares a transcript, says "process this meeting", "ingest meeting", "I have a meeting to process", or uploads a transcript.
---

# Skill: Meeting Ingest

## When to activate

- The user shares a meeting transcript (text or a doc link).
- The user says: "process this meeting", "ingest", "meeting note", "analyze this meeting".
- The user uploads a file named `meet*`, `transcript*`, `recording*`, or a doc of a session.
- You detect the shared content is clearly a multi-speaker transcript.

**Do NOT use meeting-ingest when:**
- The content is < 200 words → use `braindump`.
- The meeting is only upcoming (pre-meeting briefing) → make a manual prep note.
- It's just the user's short notes → use `braindump`.

## Preflight

1. **Read `_CLAUDE.md`** (rules, structure, conventions) and `00-inbox/MY-PROFILE.md`
   (working language, `sensitive-meetings` list, per-skill preferences).
2. **Get the real timestamp** of processing time.
3. **Determine the meeting date** (priority: from the transcript / calendar invite; fallback: ask).
4. **Capture the source link** — if the transcript comes from a Google Doc, a recording, or a
   calendar event, keep its URL **verbatim** for the `source:` field, so you can jump back to
   the original later. If there's no link (pasted text), set `source: "pasted transcript"`.
5. **List existing notes** in `02-people/` and `03-projects/` for reference resolution.
6. **Determine the invocation mode**:
   - **Manual**: the user invokes it explicitly → standard behavior.
   - **Auto**: invoked by daily-brief orchestration → adapted behavior (see "Auto mode").

## Source priority — transcript-first, summary fallback

Google Meet (and most call platforms) produce **two** Drive artifacts after a meeting:

- A **transcript tab/file** — full verbatim of what was said. This is the ground truth.
- A **summary / AI notes tab** — a model-generated digest, default tab in Drive's preview.
  This is lossy: it drops dynamics, side-discussions, contested exchanges, the exact
  wording of decisions, and most action-item nuance.

**Rule:** when ingesting from a Drive doc / Meet artifact, you ALWAYS read the **transcript**
first. The summary is a fallback, not a default.

### Decision tree
1. **Transcript available** (transcript tab populated, or a separate `*-transcript.docx` /
   `*.vtt` next to the recording in Drive) → use the transcript verbatim as the source.
   Record `transcript-source: verbatim` in frontmatter.
2. **Transcript missing but summary available** → fall back to the summary. Mark the meeting
   note with degraded confidence:
   - `confidence: medium` in frontmatter.
   - `transcript-source: summary-fallback` in frontmatter.
   - **"For future Claude" preamble must state explicitly**: `*Source: summary tab (transcript
     unavailable). Information loss expected — dynamics, exact decision wording, and
     side-discussions are not captured.*`
   - `needs-review: true` (the user may want to re-process if the transcript appears later).
3. **Neither available** → do not ingest. Flag in the brief for manual handling.

### Why this matters
Summaries elide ~40-60% of useful signal: the framing of disagreement, the exact phrasing of
commitments, the moments of hesitation that reveal real risk. `challenge-decision` and
`people-update` rely on those nuances. Defaulting to the summary tab is the single biggest
quiet quality leak in the orchestration — don't take it.

## Auto mode (invoked by daily-brief)

When this skill is invoked by `daily-brief` orchestration (not directly by the user):

### Behavioral differences
- **Frontmatter**: `ingestion-mode: auto` and `needs-review: true`.
- **"For future Claude" preamble** explicitly states: `*Auto-ingested via daily-brief on YYYY-MM-DD. needs-review flag is true until the user confirms during morning review.*`
- **Hard-to-reverse decisions**: flag `needs-validation: true` in the meeting note rather than auto-creating a dedicated `05-decisions/` note. The user creates the decision note later if they validate.
- **Newly detected people**: no auto-creation of a stub. List them for the user to validate.
- **Ambiguous participant fuzzy-match**: use the best guess but flag `needs-review` instead of asking interactively.
- **No user interaction**: if critical data is missing, insert an explicit placeholder with `⚠️ to verify on review` rather than a question (the scheduler runs autonomously).

### Auto-ingestion guardrails
Auto-ingest ONLY if ALL of these are true:
- ✅ Matches a calendar event (title / participants / time).
- ✅ Participants ≥ 2 including the user.
- ✅ Calendar duration ≥ 15 minutes.
- ✅ NOT in the `sensitive-meetings` list of `00-inbox/MY-PROFILE.md`.
- ✅ NOT already ingested (cross-check `04-meetings/`).

If any condition fails → do NOT ingest. daily-brief flags it for manual validation.

**Source choice (auto mode)**: the transcript-first rule (see *Source priority*) applies the
same way in auto mode. If only the summary is available, daily-brief still ingests but with
the degraded markers (`confidence: medium`, `transcript-source: summary-fallback`,
`needs-review: true`) and a one-line callout in the brief: *"N meetings ingested from
summary only — transcript missing."*

### "Post-auto validation" mode
When the user later invokes `meeting-ingest` on an already auto-ingested note
(signal: "validate the meeting from Tuesday with [X]"):
- Read the existing note.
- Re-process the original transcript if available.
- Enrich the sections (especially decisions, action items, dynamics) with a more critical eye.
- Update frontmatter: `ingestion-mode: auto-validated` and `needs-review: false`.
- Note in the "For future Claude" preamble: `*Validated by the user on YYYY-MM-DD.*`
- **Append-only**: keep the original auto-ingest sections; add "Validation notes" if needed.

## Process

### Step 1 — Initial parsing

Identify from the transcript:

- **Meeting date and time** (if not in the transcript frontmatter, search the content).
- **Duration** (start/end timestamps if available).
- **Participants**: names, roles if mentioned.
- **Meeting type**: 1-1 | team-sync | stakeholder | external | townhall.
- **Main topic**: one summarizing sentence.

If ambiguous, ask ONE clarification (priority: type + associated project).

### Step 2 — Participant resolution

For each identified participant:

1. **Fuzzy-match** against `02-people/*.md`.
2. Unique match → direct wikilink.
3. Multiple matches → list to the user for a choice.
4. No match → offer to create a stub (with the role inferred from the transcript).
5. **Always confirm** before creating a new person note.

### Step 3 — Noise filtering

Remove from the transcript:
- Off-topic side chats.
- Technical difficulties ("you're on mute", "can you see my screen").
- Opening/closing pleasantries.
- Exact repetitions.

⚠️ **Keep verbatim** the sentences that:
- Contain a decision.
- Commit someone to an action.
- Express a disagreement or tension.
- Give a number / a verifiable fact.

### Step 4 — Structured extraction

For each section below, be exhaustive but factual:

#### 4.1 Decisions
For each decision:
- **What**: the decision itself (one clear sentence).
- **Why**: the stated rationale (verbatim if possible).
- **Who**: decision-maker(s) — wikilinks.
- **Reversibility**: reversible | hard-to-reverse | one-way.
- **Impacted stakeholders**: wikilinks.

#### 4.2 Action items
For each action:
- **What**: concrete action.
- **Owner**: wikilink (else "unassigned" + flag).
- **Deadline**: date if mentioned, else "unspecified".
- **Depends on**: if applicable.

#### 4.3 Strategic themes
2–4 themes max. No fluff — substantive angles.

#### 4.4 Key quotes
The sentences worth keeping verbatim (citations, strong positions, useful phrasings).

#### 4.5 Tensions and disagreements
If present: who vs. whom, on what, status (resolved / open).

#### 4.6 Unresolved
What should have been settled and wasn't. With a proposed next step.

### Step 5 — Dynamics analysis (optional, by meeting type)

For 1-1s and stakeholder meetings, add a dynamics section:
- Participation / notable silences.
- Leadership moments.
- Perceived energy level.
- Weak signal worth digging into.

Skip for townhalls / team-syncs.

### Step 6 — Generate the note

**Path**: `04-meetings/YYYY-MM-DD-<slug>.md`

The `<slug>` reflects the topic, not the format
(`stakeholder-review-onboarding` rather than `tuesday-meeting`).

**Required format:**

```markdown
---
date: YYYY-MM-DD              # meeting date
ingested: YYYY-MM-DD          # ingestion date
type: meeting
tags: [meeting, <project-tags>, <topic-tags>]
participants: ["[[02-people/...]]", ...]
project: "[[03-projects/...]]"      # optional if cross-cutting
meeting-type: 1-1|team-sync|stakeholder|external|townhall
duration: <min>
source: "<verbatim link to the transcript / Google Doc / recording, or 'pasted transcript'>"
transcript-source: verbatim | summary-fallback   # which Drive tab/file was ingested
confidence: high | medium                        # medium when transcript-source: summary-fallback
ai-first: true
---

## For future Claude

This is the ingested record of a [meeting-type] held on [date] with [participants].
It covered [main topic]. Key outcomes: [N decisions, N action items]. [Note any
unresolved item or follow-up.]

## Context

[2-3 sentences: why this meeting, what preceded it, the situation at the time.]

## Participants

- [[02-people/Name 1]] — role in the meeting
- [[02-people/Name 2]] — role in the meeting

## Decisions

### [Short decision title]
- **What**: [decision]
- **Why**: "[verbatim or paraphrased rationale]"
- **Decision-maker(s)**: [[02-people/...]]
- **Reversibility**: reversible|hard-to-reverse|one-way
- **Impact**: [[02-people/...]], [[03-projects/...]]

[Repeat for each decision]

## Action items

<!-- Each line carries owner, due date, #from/meeting tag, and a ^t-id anchor for TODO.md sync -->
- [ ] [Action] — owner: me — due: YYYY-MM-DD — #from/meeting ^t-xxxxxx
- [ ] [Action] — owner: [[02-people/...]] — due: YYYY-MM-DD — #from/meeting ^t-xxxxxx
- [ ] [Action] — owner: unassigned ⚠️ — due: unspecified — #from/meeting ^t-xxxxxx

## Strategic themes

1. **[Theme 1]**: [1-2 sentences]
2. **[Theme 2]**: [1-2 sentences]

## Key quotes

> "[Verbatim quote]" — [[02-people/Name]], about [context]

## Tensions / Disagreements

[Optional section, skip if nothing to report.]

## Unresolved

- [Open question] — proposed next step: [action]

## Dynamics

[Optional section, mainly for 1-1 and stakeholder meetings.]

## Links

- Source: [original transcript / Google Doc / recording link, if any]
- People: [all participant + mentioned wikilinks]
- Projects: [wikilinks to discussed projects]
- Related decisions: [[05-decisions/...]] if a major decision was logged separately
- Previous meetings: [[04-meetings/...]] if part of a series
```

### Step 7 — Propagation (CRITICAL)

This step is what keeps the system alive. Do NOT skip it.

#### 7.1 Update people notes
For each participant existing in `02-people/`:
- Append a Timeline entry: `- YYYY-MM-DD: [[04-meetings/<slug>]] — [one sentence on what happened for this person]`.
- Update `last-interaction` in the frontmatter.
- **Append-only**: never overwrite.

#### 7.2 Update project notes
For each project referenced in `03-projects/`:
- Append to the "Timeline" section: `- YYYY-MM-DD: meeting [[04-meetings/<slug>]] — [main outcome]`.
- If decisions were made, append to the project's "Key decisions".
- Update `updated:` in the frontmatter.

#### 7.3 Important decisions → 05-decisions/
If a decision is **hard-to-reverse or one-way**, also create a dedicated note in
`05-decisions/YYYY-MM-DD-<slug>.md`. These notes are the database for `challenge-decision`.

#### 7.4 Wiki stubs for new concepts / entities (+ curator incremental)
Scan the transcript and the extracted note for **things** the user might want to look up
later — concepts, tools, teams, processes, jargon, vendors. For each that does NOT already
exist as `06-knowledge/<slug>.md`:
- Create a wiki stub per the **Wiki stub protocol** in
  `.claude/skills/knowledge-build/SKILL.md` (Mode A.2). `type: wiki`, `needs-review: true`,
  `domain: <inferred>` (from project / tags / MY-PROFILE knowledge-domains; else `unsorted`),
  `created-from: "[[04-meetings/<this-meeting>]]"`, one verbatim 1-line snippet from the
  transcript in `## Sources`.
- Backlink from the meeting note's `## Links → Related wiki`.
- **Call curator incremental** (Mode C.1 of `knowledge-build`) so the new wiki page lands in
  the right `06-knowledge/<domain>.md` hub and the root `_INDEX.md` refreshes. Silent for
  `auto-maintained: true` hubs.
- If the meeting just enriches an existing wiki page, **append** new facts with citation to
  that page (Mode A.4) and call curator incremental for `## Recent activity`.

In **auto mode** (called by daily-brief), stubs are created silently with `needs-review:
true` — they're surfaced in the brief for the user to confirm/enrich.

#### 7.5 Daily note
Append to `01-daily/YYYY-MM-DD.md` (ingestion date) under `## Meetings ingested today`:
```
- [[04-meetings/<slug>]] — [meeting-type] with [main participants]
```

#### 7.6 Action items
Keep the action items in the meeting note (with `^t-id` anchors). The ones the user
owns are consolidated into the vault-root `TODO.md` by `task-roundup` (and by
`daily-brief`'s roundup phase) — no need to duplicate them anywhere else.

### Step 8 — Report

```
✓ Meeting ingested: 04-meetings/2026-05-20-stakeholder-review-onboarding.md
✓ 3 participants linked: [[Alex Rivera]], [[Jordan Park]], [[Sam Lee]]
✓ 2 people notes updated (timeline + last-interaction)
✓ Project [[03-projects/Onboarding Refresh]] updated
✓ 1 major decision logged: 05-decisions/2026-05-20-centralize-tier1.md
✓ Daily note for 2026-05-20 updated

→ 2 unassigned action items ⚠️: owners need clarifying
→ 1 unresolved tension detected: "ownership of QA training" between Alex and Jordan
→ Suggestion: invoke challenge-decision on the tier-1 centralization (one-way, high impact)
```

## Anti-patterns to avoid

❌ **Keeping everything** — filter the noise (mute, technical issues, side chats).
❌ **Summarizing everything** — preserve decisions and key quotes verbatim.
❌ **Skipping propagation** — step 7 is non-negotiable.
❌ **Default owner** — if no clear owner, flag with ⚠️, never assign arbitrarily.
❌ **Inventing dates** — if no deadline is mentioned, write "unspecified".
❌ **Creating people without confirmation** — for new names, ask the user.

## Special cases

### Multilingual transcript
Teams are often international. If a meeting is in English with a few phrases in
another language, keep the original language in the quotes. The rest of the note
stays in English (consistent with the AI-first preamble).

### Low-quality transcript (raw voice-to-text)
If there are many ASR errors, flag it in the "For future Claude" preamble:
`Note: transcript quality is low (ASR errors). Verbatim quotes may contain transcription errors.`

### Recurring meeting (weekly 1-1, weekly sync)
Detect a series (same participants, same cadence). Link to the previous meeting
in the series under "Links > Previous meetings".

### 1-1 with a direct report
These meetings are often the most frequent and strategic. Be more thorough on
dynamics, objective tracking, and the report's development. Systematically link
to the relevant `[[03-projects/...]]` coaching/development project if one exists.
