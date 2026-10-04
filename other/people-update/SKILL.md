---
name: people-update
description: Updates or creates a person note in 02-people/ after an interaction. Append-only on the timeline, never overwriting existing observations. Handles fuzzy matching to avoid duplicates. Use when the user says "people update", "note on [name]", "update [name]'s note", "add person", or as propagation from braindump/meeting-ingest for a significant interaction.
---

# Skill: People Update

## When to activate

- The user explicitly says: "people update", "[Name]'s note", "note on [Name]", "update [Name]".
- The user shares significant info about a person (role change, new behavioral observation, important feedback).
- As propagation from `meeting-ingest` (interaction logged automatically).
- As propagation from `braindump` (if a significant interaction is detected).
- The user asks to create a new person note.

**Do NOT use people-update when:**
- A passing mention with no new info → skip.
- The last interaction was < 24h ago AND the new info isn't substantial → skip (avoid over-writing).

## People-CRM philosophy

This is the **strategic core** of the second brain for anyone who manages
relationships. A person note is NOT a résumé:
- It's an **interaction journal** (append-only timeline).
- It's an **evolving mental model** (compiled truth + recency markers).
- It's a **relationship-strategy tool** (motivations, levers, observed constraints).

**The decisive test**: if in a year the user must re-onboard with this person after
6 months of no contact, does the note let them pick up smoothly? If yes = useful
note. If no = vault rot.

## Preflight

1. **Read `_CLAUDE.md`** (rules, the person type schema) and `00-inbox/MY-PROFILE.md`
   (working language, critical stakeholders, per-skill preferences).
2. **Get the real timestamp.**
3. **Get context**: the new interaction, source (meeting / email / chat / observation), nature.
4. **Determine the invocation mode**:
   - **Manual**: explicit invocation → enrich fully (compiled truth, observations, follow-ups).
   - **Auto**: invoked by daily-brief orchestration → minimal update only (see "Auto mode").
   - **Propagation from meeting-ingest**: intermediate — log the interaction with a factual observation, without touching compiled truth.

## Auto mode (invoked by daily-brief)

When invoked by `daily-brief` orchestration, specific behavior:

### Allowed in auto mode
✅ Update frontmatter:
- `last-interaction: YYYY-MM-DD` (today)
- `updated: YYYY-MM-DD` (today)
- **Clear `staleness-flag`** if present

✅ Append ONE aggregated timeline entry for the day:
```markdown
### YYYY-MM-DD — Daily interactions (auto-logged)
- Calendar: [N events, short detail "1-1 30min 'topic'"]
- Email: [N threads, main topic if detectable]
- Chat: [N DMs or mentions]
- Source: daily-brief auto-propagation
```

### FORBIDDEN in auto mode
❌ NEVER modify "Compiled truth" (manual mode only).
❌ NEVER modify "Open threads" (manual mode only).
❌ NEVER create a new person note (flag in the brief for the user to validate).
❌ NEVER add an interpretive observation to the timeline.
❌ NEVER modify the tags (role, region).

### Recognizable format
The `(auto-logged)` suffix in the timeline entry header is mandatory and
**non-modifiable**. It lets `challenge-decision` and other skills distinguish
human signal from automatic signal.

### Daily duplicate handling
If an `(auto-logged)` entry already exists for the day (daily-brief run twice or by debug):
- Update the existing entry instead of creating a new one.
- Preserve already-logged sources, add only new ones.
- NEVER duplicate.

### Weighting for challenge-decision
`(auto-logged)` entries carry less signal than manual observations.
`challenge-decision` should use them mainly for:
- ✅ Frequency quantification (how many interactions over X months).
- ✅ Temporal pattern detection (an interaction that fades gradually).
- ❌ NOT as evidence of a behavioral pattern or strategic positioning.

## Staleness-flag: automatic management

The `staleness-flag` field is fully managed automatically:
- **Set** by the `Stale People Check` scheduled task if `last-interaction > 30 days`.
- **Cleared** by `daily-brief` auto mode as soon as a new interaction is detected.
- **Cleared** by a manual `people-update` invocation (any update clears the flag).

Flag format:
```yaml
staleness-flag: "stale-30d-since-2026-05-22"
# or for critically stale:
staleness-flag: "stale-60d-since-2026-04-22"
```

The user NEVER touches this flag manually. The system self-heals.

## Process

### Step 1 — Identify the person

#### 1.1 Fuzzy match
Search `02-people/*.md`:
- Exact full-name match.
- First + last name with typo tolerance.
- First name only (ambiguous, ask for confirmation).
- Description ("the PM in Spain", "my manager") → cross-reference frontmatter.

#### 1.2 Cases
- **Single match found** → proceed with update.
- **Multiple matches** → present the list, ask for confirmation.
- **No match** → offer to create (Step 2).
- **Match with typo** → confirm before acting: "Do you mean [[Alex Rivera]]?"

### Step 2 — Creation (if new person)

⚠️ **ALWAYS ask for confirmation** before creating a new person note. An orphan
note is less harmful than a duplicate.

Ask the user if not obvious:
- Correct full name?
- Role / function?
- Team / company?
- Region?
- Relationship to you (direct-report, peer, manager, stakeholder, external)?

Create the note at `02-people/First Last.md` with this template:

```markdown
---
date: YYYY-MM-DD              # date of the first logged interaction
updated: YYYY-MM-DD
type: person
tags: [person, <role-tag>, <region-tag>]
role: "[exact role]"
company: ""                   # company / org name
team: "[team]"
region: WE|NA|LATAM|APAC|Global
relationship: direct-report|peer|manager|stakeholder|external
languages: ["en"]
last-interaction: YYYY-MM-DD
staleness-flag: ""
ai-first: true
---

## For future Claude

Person note for [Name], [role] at [company/team]. First interaction logged on [date].
[1-2 sentence summary of relationship and context.]

## Compiled truth

[What's stable and known about this person, updated episodically. NOT the timeline. Rather:]
- **Professional background**: [trajectory, context]
- **Working style**: [stable observations]
- **Apparent motivations**: [what seems to drive them]
- **Sensitive topics / red buttons**: [what to avoid]
- **Levers / good practices**: [what works to collaborate]
- **Internal network**: [who they work closely with]

## Timeline

[APPEND-ONLY. Each entry = 1 interaction or observation, dated, sourced.]

### YYYY-MM-DD — [Interaction type]
- Source: [[04-meetings/...]] / email / chat / observation
- What: [1-3 factual sentences about what happened]
- Observation: [interpretation, hypothesis, detected signal]
- [ ] Follow-up: [action if applicable — checkbox form so task-roundup picks it up;
  plain `- Follow-up:` (no checkbox) for FYI-only notes]

## Open threads

[Ongoing topics with this person, to track. Editable section, not append-only.]

## Links

- Shared projects: [[03-projects/...]]
- Manager: [[02-people/...]]
- Reports: [[02-people/...]]
- Recent meetings: [[04-meetings/...]]
```

### Step 3 — Update (existing note)

#### 3.1 Append timeline
Add ONE entry to the "Timeline" section:

```markdown
### 2026-05-20 — Weekly 1-1
- Source: [[04-meetings/2026-05-20-1to1-alex]]
- What: Alex raised friction on the qualification script V2, especially edge cases.
  Looking for a sponsor to push a training redesign.
- Observation: 2nd time this month they've raised this proactively. Signal they want
  to make it a project.
- [ ] Follow-up: decide whether to put it in their Q3 development plan — owner: me
```

⚠️ **Append-only**: NEVER delete an existing timeline entry. If old info is
contradicted, add a new entry that mentions the contradiction; don't edit in place.

#### 3.2 Update compiled truth (if applicable)
"Compiled truth" is editable but sparingly. Modify only if:
- You have a new **stable** observation (not a one-off signal).
- It's **confirmed across multiple interactions** (visible recency markers).

When you modify "Compiled truth", **include the update date**:
```markdown
- **Working style**: very field-oriented, little patience for abstract process *(updated 2026-05-20, confirmed across 3 interactions)*
```

#### 3.3 Update frontmatter
- `updated:` → today.
- `last-interaction:` → today.
- If role/team/region changed → update those fields (and log the change in the timeline).

#### 3.4 Update "Open threads" and "Links"
- Add the ongoing topic to "Open threads" if not already there.
- Add the meeting/project to Links if new.

### Step 4 — Propagation

#### 4.1 People index (optional)
If `02-people/_index.md` exists, update the relevant line (name, role, last interaction, status).

#### 4.2 Daily note
Append to `01-daily/YYYY-MM-DD.md` under `## People touched today`:
```
- [[02-people/Alex Rivera]] — [interaction type] — topic: [topic]
```

#### 4.3 Related projects
If the interaction concerns a project, verify the project is linked under "Links" and `related-people`.

### Step 5 — Report

```
✓ Note updated: 02-people/Alex Rivera.md
✓ Timeline: 1 entry added (weekly 1-1)
✓ Compiled truth: "Working style" updated (3rd-iteration confirmation)
✓ Daily note 2026-05-20 updated
✓ Open threads: "Qualification script training redesign" added

→ Pattern detected: 2nd proactive raise on this topic this month
→ Suggestion: create project [[03-projects/Qualification Script Training Refresh]]?
```

## Suggested tags for people

### Role (1 required tag)
- `agent` | `team-lead` | `manager` | `head` | `vp` | `c-level`
- `specialist` | `coach` | `trainer`
- `pm` | `eng` | `design` | `data` | `ops`
- `external-vendor` | `external-client`

### Region (1 required tag if internal)
- `region-we` | `region-na` | `region-latam` | `region-apac` | `region-global`

### Optional tags
- `direct-report` | `peer` | `manager-of-mine` | `sponsor` | `blocker` | `champion`
- `high-trust` | `building-trust` | `caution`

## Anti-patterns to avoid

❌ **Overwriting the timeline** — append-only, never retroactive edits.
❌ **Compiled truth without recency** — if you update, date the change.
❌ **Duplicate** — fuzzy-match before create, always.
❌ **Orphan note** — make sure at least today's daily note links to it.
❌ **Unsourced judgment** — every observation must point to a source (dated meeting/email/observation).
❌ **Inventing info** — if you don't know, write "unknown" or ask the user.
❌ **Descriptive note with no use** — no flat résumé. Always ask: "useful in 6 months?"

## Special cases

### External person (client, vendor, partner)
- `company:` = external name.
- `relationship:` = external.
- More tolerance for incompleteness (less info available).
- Explicitly log the nature of the contact (commercial, customer success, partnership, etc.).

### Person who left the org / leaver
- Keep the note, never delete.
- Update frontmatter: `status: alumni`, `relationship: external-alumni`.
- Note in timeline: "YYYY-MM-DD — Left for [destination]".
- Useful for your future network.

### A key direct report
Special case: the person the user interacts with most. The note can get long. Manage it:
- Timeline grouped by month (sub-headers `## YYYY-MM`).
- Editable "Development plan" section.
- Editable "Quarterly objectives" section.
- Special tags: `direct-report` + `high-trust`.

### Cross-region stakeholder
For multi-region stakeholders:
- Tag `region-global`.
- Explicit note of sub-teams / zones of influence.
- Timeline tagged by regional context if relevant.

### First negative observation
If you log a first potentially negative observation (frustration, friction,
disagreement), do it factually, never as a value judgment. The goal is to track
signals, not to label people.

✅ Good: "Alex expressed frustration about a lack of product-PM support during the
standup. Tense tone, visible disagreement."

❌ Bad: "Alex is negative and hard to manage."

## Final note

This is probably the most valuable skill long-term. A well-kept people CRM =
cumulative relationship capital. Poorly kept = a vault that pollutes searches.

Discipline > volume. 20 excellent notes beat 200 mediocre ones.
