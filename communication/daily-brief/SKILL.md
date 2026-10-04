---
name: daily-brief
description: Generates a daily (or weekly) brief by synthesizing connected sources (email, calendar, drive, chat) and the vault notes touched during the day. Produces a note in 01-daily/. Also orchestrates auto-ingestion of meetings and auto-update of people notes. Use as a scheduled daily task, or manually when the user says "daily brief", "what happened today", "recap of the day", "weekly review".
---

# Skill: Daily Brief

## When to activate

- **Scheduled daily task** (e.g. end of day) → daily mode.
- **Scheduled weekly task** (e.g. Monday morning) → weekly mode (synthesis of the previous week).
- Manual invocation: "daily brief", "recap of the day", "what happened", "weekly review".

## Preflight

1. **Read `_CLAUDE.md`** (rules, structure, conventions) and `00-inbox/MY-PROFILE.md`.
2. **Get the real timestamp.**
3. **Determine the mode**: daily (default) or weekly (Monday morning or on request).
4. **Define the time window**:
   - daily: today 00:00 → now.
   - weekly: Monday of last week 00:00 → Sunday of last week 23:59.

## Process

### Step 1 — Multi-source collection

Collect from whatever sources are connected (via available tools / MCP servers).
Run in parallel where possible.

> **Primary vs secondary sources.** Read `primary-communication-channels` from
> `00-inbox/MY-PROFILE.md`. Anything listed there (`email`, `slack`, `teams`, `calendar`, …)
> is a **co-primary source**: treat it as a peer of email and calendar in volume of attention,
> in collection breadth, and in the brief structure. If `slack` (or similar) is listed, do
> NOT under-weight it just because it's high-volume — chat is where most of the day's signal
> lives for many users.

#### 1.1 Email
- Emails received in the window.
- Filter out: newsletters, automated notifications, marketing.
- Keep: conversations with colleagues, relevant externals, decision threads.
- Extract: subject, sender, one-line summary, implicit urgency.

#### 1.2 Calendar
- Events in the window (past + ongoing).
- For each: title, participants, duration, notes/description.
- Cross-reference with `04-meetings/`: if already ingested → link, else → flag for potential ingestion.

#### 1.3 Drive / files
- Docs modified or shared in the window.
- Filter out: your own minor edits.
- Keep: new docs received, collaborative docs touched by others, meeting transcripts created.

#### 1.4 Chat (Slack / Teams / etc.) — co-primary when listed in `primary-communication-channels`

Collect broadly when chat is a primary channel; collect narrowly otherwise.

**Always (whatever the channel's status):**
- DMs received in the window.
- DMs **sent** by the user (signal of what the user cared enough to write).
- Mentions of the user in any channel.
- Replies in threads the user has participated in (started or replied to) within the window.

**Additionally when chat is a primary channel:**
- Activity in any channel the user actively follows — defined as: channels where the user
  has posted, replied, or reacted within the last 14 days, even if not in
  `priority-chat-channels`. This catches the long tail of where the user actually works.
- Reactions the user placed on others' messages (signal of interest / agreement).
- Saved / bookmarked messages.
- Huddles or calls in chat (if surfaceable).

**Filter out** (both modes):
- Bot notifications, CI noise, build-status messages.
- Emoji-only reactions on bot messages.
- Off-topic channels explicitly excluded in `MY-PROFILE.md` (`chat-channels-to-ignore`).

**Extract per channel/thread**: topic (one line), participants, message count, the user's
own contribution, any decision/commitment, any unresolved question.

**Volume guardrail.** A busy Slack day can swamp the rest. Aggregate by **topic, not by
message**: cluster messages across channels/threads into themes (e.g. "onboarding script
friction" pulled from #onboarding, #cs-team, and a DM with Alex). One theme = one bullet,
with the threads cited as sources. Cap at ~10 themes; the synthesis in Step 3 will reduce
further.

#### 1.5 Internal vault
- Notes created or modified in the window (all sections except `07-archive`).
- Especially: new decisions, ingested meetings, people updates, unprocessed braindumps.

### Step 2 — Triage and prioritization

Categorize the collected items:

#### 2.1 Decisions / Commitments
- Any action the user committed to ("I'll handle it", "ok I'll do it", an assigned action item).
- Decisions made by others that impact the user's projects.

#### 2.2 Weak signals
- A topic mentioned repeatedly across channels.
- Detectable interpersonal tensions.
- Shifts in tone/priority from stakeholders.
- First mention of something that could grow.

#### 2.3 Awaited follow-ups
- Action items the user owns with an approaching deadline.
- People waiting on a reply from the user.
- Past commitments to verify.

#### 2.4 Learning / inputs
- Articles shared, docs to read.
- New concepts/frameworks mentioned.
- Best practices surfaced by teams.

#### 2.5 People intel
- People interacted with today.
- New information about known stakeholders (role change, etc.).
- New people encountered (candidates for a person note).

### Step 3 — Intelligent synthesis

⚠️ **Major anti-pattern**: do not produce a flat exhaustive list. The brief must
be **actionable and synthetic**.

Synthesis rules:
- **Top 3–5 topics** only as main sections (not 15) — these synthesize *across all sources*.
- **One sentence = one signal** (no vague paraphrase).
- **Always link** to the source (email, meeting, doc, vault note, chat thread).
- **Recency markers** for external claims.
- **`## Themes from Slack` is separate from the top-5** when chat is a primary channel.
  Chat themes do NOT compete with email/meeting topics for top-5 slots; they get their own
  section so high-volume Slack signal isn't drowned out (see Step 4 template).

### Step 4 — Generate the note

**Daily path**: `01-daily/YYYY-MM-DD.md`
**Weekly path**: `01-daily/YYYY-WW-weekly.md` (e.g. `2026-21-weekly.md`)

⚠️ **If the daily note already exists** (because other skills wrote into it during
the day): APPEND, don't replace. Add the brief at the top under `## Daily brief`,
keeping the existing sections (braindumps, ingested meetings).

**Daily format:**

```markdown
---
date: YYYY-MM-DD
type: daily
tags: [daily]
ai-first: true
---

## For future Claude

Daily brief for [date]. Generated automatically at [timestamp] aggregating email,
calendar, drive, chat, and internal vault activity. Top themes: [3-5 keywords].
[Note any unusual signal or urgent follow-up.]

## TL;DR (3 lines)

1. [The most important thing today, one sentence]
2. [The second thing, one sentence]
3. [The third thing, one sentence]

## Decisions & commitments

- [Committed action] — source: [[email/meeting/chat]] — deadline: YYYY-MM-DD
- [Decision by X impacting project Y] — source: [...]

## Decisions reversed — pending postmortem

> Render only if Step 6.7 detected one or more decisions flipped to `status: reversed` this
> window. Otherwise omit the section entirely.

- [[05-decisions/<slug>]] — reversed YYYY-MM-DD.
  - Hypothesis: <one sentence>
  - Distilled lesson: <one sentence>
  - Vault references found: N decisions, N wikis, N lessons (manifest in [[06-knowledge/<slug>-postmortem]])
  - Proposed updates: ready for your review — accept all / cherry-pick / dismiss.

## Top topics of the day

### [Topic 1]
[2-3 sentences synthesizing what happened on this topic, with linked sources]
**Sources**: [[04-meetings/...]], email from [[02-people/...]], chat thread #channel
**Next**: [action or open question]

### [Topic 2]
[...]

## Themes from Slack

> Only emit this section when `slack` (or another chat tool) is listed in
> `primary-communication-channels`. Aggregate by **theme**, not by message; one bullet per
> theme, citing the channels/threads it spans. This section is independent of the top-5 cap.

- **[Theme 1]** — observed in #channel-a, #channel-b, DM with [[02-people/...]] — N messages,
  the user participated in M. Signal: [one sentence].
- **[Theme 2]** — [...]

(If the day was light on chat: a one-liner like "Slack quiet today" is fine.)

## Weak signals to dig into

- [Signal 1] — observed in [sources] — hypothesis: [...]
- [Signal 2] — [...]

## Pending follow-ups

[Fed from the Overdue + Today buckets of [[TODO]]. Each links back to its source note.
These lines are MIRRORS of existing tasks — they carry the source anchor in the wikilink
and never get a new `^t-id` of their own (task-roundup reconciles through the referenced
anchor).]
- [ ] [Action] — [[TODO]] → [[<source-note>#^t-id]] — due YYYY-MM-DD
- [ ] [Action] — [[<source-note>#^t-id]] — due YYYY-MM-DD

## People touched today

- [[02-people/Alex Rivera]] — 1-1 + 2 emails — topic: training
- [[02-people/...]] — [...]

## Inputs of the day

- [Article/doc shared by X] — source: [link or drive path] — relevance: [why]

## Braindumps of the day

[Links to braindumps created via the braindump skill — that skill appends here]

## Meetings ingested today

[Links to ingested meetings — meeting-ingest appends here]

## Docs ingested today

[Links to ingested documents — doc-ingest appends here]
```

> **Weekly mode also runs `knowledge-build` (two phases)**:
> 1. **Lessons sweep** — conservative pass that proposes new/updated `06-knowledge/` lesson
>    notes flagged `needs-review: true`. List them in the review under `## Knowledge updates`.
> 2. **Curator sweep** (Mode C.2 of knowledge-build) — rebuilds auto-maintained hub
>    listings, refreshes `_INDEX.md`, flags orphans / near-duplicates / aging stubs /
>    stale wikis, and proposes new hubs when 3+ notes cluster on an unhubbed domain.
>    Structural changes always preview and ask. Surface the health counters and any pending
>    proposals at the top of the weekly review under `## Knowledge garden`.

**Weekly format** (different — synthesis-focused vs. collection):

```markdown
---
date: YYYY-MM-DD              # first day of the analyzed week
week: YYYY-WW
type: weekly-review
tags: [weekly]
ai-first: true
---

## For future Claude

Weekly review for week [WW] of [YYYY]. Covers [start date] → [end date]. Compiled
from 7 daily briefs + a direct vault scan.

## Knowledge garden

[Weekly mode only — output of the curator sweep: health counters, passes to stabilize,
pending proposals (new hubs, merges, stubs aging out). Omit if the sweep didn't run.]

## Knowledge updates

[Weekly mode only — lessons proposed/updated by the lessons sweep, flagged
`needs-review: true`, for you to confirm.]

## Themes of the week

[3-5 cross-cutting themes that emerged, with backlinks to daily notes / meetings / decisions]

### [Theme 1]
- Appeared: [first signal]
- Evolution: [how it moved]
- Current state: [resolved / open / escalated]
- Linked to: [[03-projects/...]]

## Decisions of the week

[Structured recap of important decisions, with links to 05-decisions/]

## People focus

[Who emerged most this week? Why?]

## Patterns detected

[Cross-day recurrences, confirmed weak signals]

## Anti-patterns / Friction

[What isn't working, what recurs negatively]

## Energy & focus

[Honest synthesis: where did the energy go, is it aligned with declared priorities?]

## Implicit plan for next week

[What the daily notes suggest as priorities for the coming week]

## Stubs to process

[Incomplete notes or notes awaiting clarification]
```

### Step 5 — Meeting auto-orchestration (CRITICAL)

⚠️ **This is what makes the system run without manual intervention.**

For each meeting transcript detected during the window:

#### 5.1 Whitelist check
A transcript is **auto-ingestable** ONLY if ALL conditions hold:
- ✅ Matches a calendar event in the window (by title, participants, or time).
- ✅ Calendar participants ≥ 2 (including the user).
- ✅ Calendar duration ≥ 15 minutes.
- ✅ NOT in the `sensitive-meetings` list of `00-inbox/MY-PROFILE.md`.
- ✅ Not already ingested (cross-check `04-meetings/` by date + slug).

#### 5.2 Auto-ingest (for transcripts that pass the whitelist)
Invoke `meeting-ingest` in auto mode, with these differences vs. manual:
- Frontmatter: `ingestion-mode: auto` and `needs-review: true`.
- "For future Claude" mentions: `*Auto-ingested via daily-brief on YYYY-MM-DD. needs-review flag is true until the user confirms.*`
- People propagation handled in step 6 (don't duplicate here).
- Hard-to-reverse decisions detected → flag `needs-validation: true` rather than creating directly in `05-decisions/`.

Cap at 5 auto-ingested meetings per daily-brief run to avoid saturating context.
If > 5, ingest the 5 longest/most important and list the rest for the next day.

#### 5.3 Flag for human validation
For transcripts that do NOT pass the whitelist:
- Mention explicitly in the brief:
  ```
  ⏸ Awaiting manual validation:
  - 1-1 with [manager] (sensitive, transcript available) → want me to ingest it?
  - Orphan transcript (no calendar match) → ignore or ingest with context?
  ```
- Auto-ingest NOTHING.
- The user validates yes/no the next day when reading the brief.

### Step 6 — People auto-update (CRITICAL)

For each person the user interacted with during the window (detected via calendar/email/chat):

#### 6.1 Interaction detection
For each person:
- Calendar events (participants including the person).
- Email threads (sender OR recipient = this person; exclude generic cc).
- Chat DMs (direct DM or mention in a critical channel).

#### 6.2 Fuzzy-match against 02-people/
- If the note exists → proceed to update (step 6.3).
- If the note does NOT exist → create NOTHING automatically. Append to the
  "New people detected" section of the brief for the user to validate next day.

#### 6.3 Update the note (auto-logged)
For each person whose note exists:

**Frontmatter**:
- Update `last-interaction: YYYY-MM-DD` (today).
- Update `updated: YYYY-MM-DD` (today).
- **Clear `staleness-flag`** if present (self-healing).

**Timeline**:
Append ONE aggregated entry for the day:
```markdown
### YYYY-MM-DD — Daily interactions (auto-logged)
- Calendar: [events with this person, format "1-1 30min 'title'"]
- Email: [N threads, main topic if detectable]
- Chat: [N DMs or mentions, channel if relevant]
- Source: daily-brief auto-propagation
```

⚠️ **No interpretive observation.** Raw facts only. The "Compiled truth" section is
NEVER touched in auto mode.

⚠️ **Deduplication**: if an `(auto-logged)` timeline entry already exists for the
day (rare: daily-brief run twice), update the existing entry instead of creating a
new one.

#### 6.4 Quantity cap
Auto-update up to 20 people notes per run. If > 20 detected (rare: very busy day),
prioritize:
1. Direct reports
2. Manager
3. Recurring peers
4. Critical stakeholders (per `MY-PROFILE.md`)
5. Others

List the non-updated ones in the brief: "12 other people interacted with today not
auto-updated (volume cap). Invoke people-update manually if needed."

### Step 6.5 — Task roundup & reconciliation (CRITICAL)

Run the `task-roundup` procedure (see `.claude/skills/task-roundup/SKILL.md`):

1. Collect the action items **you own** from today's new/updated notes (ingested
   meetings, decisions, follow-ups) plus anything still open across the vault.
2. Assign a `^t-id` block-ID to any new action line that lacks one (additive edit).
3. Reconcile checkboxes both ways with `TODO.md` at the vault root: a box checked in
   `TODO.md` since the last run flips its source line to `[x] ✅ <date>`, and vice versa.
4. Refresh `TODO.md`, bucketed by due date (overdue / today / upcoming / later / no date
   / waiting-on-others / done).

⚠️ Completing a task in `02-people/` or `05-decisions/` is a checkbox toggle + `✅ <date>`
stamp only — never touch Compiled truth in auto mode.

Then surface the result at the top of the brief: feed `## Pending follow-ups` from the
**Overdue** and **Today** buckets (with the `[[TODO]]` backlinks), and flag the overdue count.

### Step 6.7 — Reversed-decision postmortem auto-trigger (since v4.0)

Scan `05-decisions/` for any note whose `status:` changed to `reversed` **since the last
brief** (compare against the previous daily/weekly's `updated:` window). For each detected
flip:

1. Invoke `challenge-decision` in **postmortem mode** for that decision (auto). The skill
   runs Steps P1 and P2 fully — extracts the hypothesis, cross-references the vault — and
   produces the previewed edits for Step P3.
2. Postmortem auto-mode **never applies the cross-vault edits**. It surfaces them as a
   manifest in this brief under a new section `## Decisions reversed — pending postmortem`,
   with the proposed wiki/lesson updates listed inline for human approval.
3. The postmortem analysis note (`06-knowledge/<decision-slug>-postmortem.md` or appended
   to the reversed decision) is created with `needs-review: true`.

If no decision flipped since the last brief, skip this step silently (don't render an
empty section).

Detection rule of thumb (auto-conservative):
- A decision is "flipped this window" if its file's git history shows the `status:` field
  changed to `reversed` between the previous brief's window-end and now, **or** if a
  timeline entry titled `### YYYY-MM-DD — Reversed` was appended within the window.
- Don't re-trigger on decisions already `reversed` *before* the last brief — those were
  already handled (or skipped) previously. The postmortem fires once per flip.

### Step 7 — Propagation

- **Link from the previous daily**: append "→ Next: [[YYYY-MM-DD]]" in the previous day's daily note.
- **For the weekly**: link from the 7 daily notes of the week to the weekly review.

### Step 8 — Report

```
✓ Daily brief generated: 01-daily/2026-05-22.md
✓ Sources analyzed: Email (12), Calendar (4 events), Drive (3 docs), Chat — primary (47 msgs across 9 channels, clustered into 5 themes)

📥 AUTO-INGESTION
✓ 3 meetings auto-ingested (needs-review: true):
  - [[04-meetings/2026-05-22-team-sync]] (15-min morning review recommended)
  - [[04-meetings/2026-05-22-stakeholder-onboarding]]
  - [[04-meetings/2026-05-22-project-sync]]
✓ 8 people notes auto-updated (last-interaction + auto-logged timeline)
✓ 2 staleness-flags cleared (Alex, Jordan)

⏸ AWAITING VALIDATION
- 1-1 with [direct manager] (sensitive, transcript available) → want me to ingest it tomorrow?
- 2 new people detected (never seen in the vault):
  - "Riley Chen" (3 emails today, seems to be a PM) → create a note?
  - "Sam Patel" (1 meeting + 1 email, external context) → create a note?

✅ TASKS
✓ TODO.md refreshed — ⏰ 2 overdue · 📅 3 due today · ⏳ 5 waiting on others
✓ Reconciled 3 check-offs with source notes (2 done here, 1 done in source)

🎯 SYNTHESIS
✓ Top topic: onboarding script friction
✓ Weak signals: 2 (to dig into)
⚠️ 3 follow-up deadlines approaching (D+2, D+3, D+5)

The vault updated itself.
```

## Configuration (from MY-PROFILE.md)

Read these from `00-inbox/MY-PROFILE.md`:

- **`primary-communication-channels`** — sources to treat as co-primary with email/calendar
  (e.g. `[slack]`, `[teams, slack]`). When set, the matching Step 1 collector goes into
  *broad* mode and the brief renders the corresponding dedicated section (`## Themes from Slack`).
- **Priority chat channels** — a narrower whitelist *within* the chat source for must-read
  channels; still useful as a hint, but no longer the gate for whether chat is collected.
- **`chat-channels-to-ignore`** — explicit blocklist for noisy/off-topic channels.
- **Critical stakeholders** — prioritize in the "People touched" section.
- **Active projects** (`status: active` in `03-projects/*`) — weight related signals.
- **Brief time / weekly time** — when the scheduled runs happen.
- **Tone** — direct, no "great progress today!" filler.
- **Top topics cap** — default 5 (does NOT include `## Themes from Slack`).

## Anti-patterns to avoid

❌ **Flat exhaustive list** — synthesize, don't dump.
❌ **Re-paraphrasing what's already in the vault** — link, don't duplicate.
❌ **Inventing themes** — if the day is quiet, the brief is short. That's fine.
❌ **Corporate tone** — direct and concrete.
❌ **Self-congratulation** — no saccharine "great progress!".
❌ **Skipping weak signals** — that's often where the value hides.
❌ **Overwriting an existing daily** — append, never overwrite.

## Special cases

### Quiet day
If the day is quiet (no meetings, few emails, weekend): a minimal 5–10 line brief.
No need to fill space.

### Very busy day
Beyond 5 topics, don't overflow — keep the top 5, mention "+ N minor topics (see vault)".

### Day off
If the user marked OOO in calendar: skip the brief, or generate only a "follow-ups
awaiting your return" section.

### First use (empty vault)
Degraded brief: just the external sources, no vault cross-referencing. Mention that
value grows as the vault fills.
