---
name: daily-briefing
category: exec-function
description: Personal daily briefing assistant. Pulls the last 24 hours of email and calendar from Outlook, summarizes today's schedule, surfaces open action items, and proposes focus blocks. Use when user says "daily briefing", "morning briefing", "daily standup prep", or invokes /daily-briefing.
allowed-tools:
  - mcp__outlook__outlook_get_inbox_emails
  - mcp__outlook__outlook_get_calendar_events
  - mcp__outlook__outlook_get_email_by_id
  - mcp__outlook__outlook_get_unread_emails
  - mcp__outlook__outlook_search_emails
  - mcp__outlook__outlook_get_folder_emails
  - mcp__outlook__outlook_create_meeting_draft
  - mcp__outlook__outlook_check_calendar_conflict
  - mcp__outlook__outlook_get_current_user
  - AskUserQuestion
  - Bash
  - Write
  - Read
  - Glob
  - Skill
related-skills:
  - energy-budget
loop-eligible: true
recurrence-hint: daily

compatibility: claude-code codex opencode
---

# Daily Briefing

Personal daily briefing. Read-only by default for the report; calendar focus-block drafts require user approval before creation.

## Related skills

- **obsidian-markdown** — canonical reference for Obsidian Flavored Markdown (frontmatter, wikilinks, embeds, callouts, properties). The vault writes in this skill use OFM syntax; consult `obsidian-markdown` if you need to extend the templates with new constructs (callouts, block IDs, mermaid options, etc.) rather than reinventing the syntax inline.
- **obsidian-bases** — reference for `.base` file authoring (filters, formulas, views). Used by step 6 when the embedded dashboards are missing from the vault.
- **clarity-council (personal-assistant persona)** — owns the focus-block proposal in step 9 and the executive-summary "next actions" framing. The persona's Decision Lens (reduce mental load, prevent missed commitments, keep the next action obvious) is the load-bearing voice for the whole briefing — its Output Requirements (next action, timing/deadline, dependencies/follow-ups) shape both the open-action-items section and the focus-block table.

## Quick start

1. Find the most recent prior daily note in the vault to determine the briefing window (covers gaps from weekends, alternating Fridays off, holidays, vacations).
2. Pull inbox + calendar from that window-start through now, plus today's calendar.
3. Discover vault link conventions (person notes, tags) — see step 5.
4. Render the daily report (see [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md)) and **save it to the Obsidian vault**.
5. Update the weekly rollup note (see [WEEKLY_TEMPLATE.md](WEEKLY_TEMPLATE.md)).
6. Update the monthly rollup note (see [MONTHLY_TEMPLATE.md](MONTHLY_TEMPLATE.md)).
7. Propose focus blocks; ask the user before creating any drafts.

## Vault path resolution

The skill needs the **Obsidian vault root** to read prior notes and write new ones. It is referenced throughout this document as `{{vault_root}}` — never hardcode a path.

Resolve `{{vault_root}}` once at the start of every run, in this order:

1. **Loaded memory.** Scan the auto-loaded `MEMORY.md` index and any reference memories already in context for a `**Vault root:**` line (or equivalent key like `vault_root:` / `obsidian_vault:`). The canonical entry is `reference_obsidian_vault.md` — its first content line reads `**Vault root:** <absolute path>`. Use that path verbatim.
2. **Memory file lookup.** If the index references a vault memory (e.g. `[Obsidian vault](reference_obsidian_vault.md)`) but the file isn't already loaded, `Read` it and extract the `**Vault root:**` value.
3. **Prompt the user.** If neither of the above yields a path, ask via `AskUserQuestion`:
   *"I need your Obsidian vault root path to save the daily briefing. What's the absolute path? (e.g. `C:\Users\you\Documents\my-vault\`)"*
   Single-select with one option — `Other` lets the user type the path.
4. **Persist the answer.** After receiving a user-provided path, save it to memory so future runs skip the prompt:
   - If `reference_obsidian_vault.md` exists, `Read` it, update the `**Vault root:**` line, and `Write` it back.
   - If it does not exist, create it with frontmatter (`name: obsidian-vault-root`, `type: reference`, short description) and a `**Vault root:**` body line, then add a one-line entry to `MEMORY.md`: `- [Obsidian vault root](reference_obsidian_vault.md) -- vault base path used by daily-briefing`.
5. **Validate.** Verify `{{vault_root}}` exists with a single `Glob("{{vault_root}}/*")`. If empty or errors, surface the failure and re-prompt — do not write to a non-existent path.

After resolution, every path literal below uses `{{vault_root}}` as the prefix.

**Daily note path:** `{{vault_root}}\📅\YYYY\MM\YYYY-MM-DDD.md` — Pittsburgh local date, with a literal `D` prefix on the **day component only** (e.g., `2026\05\2026-05-D05.md` for May 5, 2026).

**Weekly note path:** `{{vault_root}}\📅\YYYY\MM\YYYY-W{NN}.md` — ISO week-year and week number, month folder follows the week's Monday (e.g., `2026\05\2026-W19.md` for the week of May 4, 2026).

**Monthly note path:** `{{vault_root}}\📅\YYYY\YYYY-M{MM}.md` — calendar year and month. Lives in the **year folder**, not in a month subfolder (e.g., `2026\2026-M05.md` for May 2026).

## Workflow

### 1. Determine briefing window

Find the most recent prior daily note so the window covers everything since the last run — gaps from weekends, alternating Fridays off, holidays, and vacations all collapse to a single catch-up briefing.

1. `Glob("{{vault_root}}/📅/**/[0-9][0-9][0-9][0-9]-[0-9][0-9]-D[0-9][0-9].md")` — enumerate all daily notes.
2. Parse the date from each filename (`YYYY-MM-DDD.md` → `YYYY-MM-DD`). Filter to dates **strictly before today** (Pittsburgh local).
3. Pick the maximum (most recent) date — call it `last_run_date`.
4. Compute `window_start`:
   - **Default** — `last_run_date` at 06:00 America/New_York (right before that morning's briefing was generated).
   - **No prior note found**, or the most recent note is older than **14 days** — fall back to 24h before now and tell the user "no recent prior note within 14 days; using 24h fallback window."
   - **Cap at 14 days** even if a prior note exists further back, to avoid blowing context. Warn the user when capping.
5. Compute `gap_days = today - last_run_date`. If `gap_days > 1`, this is a **backfill briefing** — note that in the executive summary and label the email section with the actual date range.

State the chosen window in one short sentence before gathering data, e.g. *"Backfilling since [[2026-05-D07]] (Thu) — 4-day window."*

### 2. Gather data (parallel)

Call these in a single response, using `window_start` from step 1:

- `outlook_get_inbox_emails(since=<window_start ISO>, include_read=true, max_results=50)` — email since last briefing. If `gap_days > 2`, raise `max_results` to 100.
- `outlook_get_calendar_events(start=<window_start>, end=<now>)` — meetings since last briefing.
- `outlook_get_calendar_events(start=<today 00:00>, end=<today 23:59>)` — today's schedule.

If inbox volume is high (>30 emails), also call `outlook_get_unread_emails(max_results=25)` to ensure unread items aren't lost.

`outlook_get_inbox_emails` accepts ISO datetimes for `since` (also `today`, `yesterday`, `7d` shorthands). Prefer the explicit ISO datetime so backfill windows of arbitrary length are exact.

### 3. Triage email

For each email in the briefing window, classify into one bucket:

- **Action required** — direct ask, question, deadline, @mention, or you're the sole recipient
- **FYI** — informational, CC'd with no ask, automated digest
- **Awaiting reply** — emails *you* sent that have no response yet (check Sent Items if needed)

Only fetch full body via `outlook_get_email_by_id` when subject + preview is ambiguous. Keep it cheap.

#### 3a. Action vs. FYI classifier (load-bearing rule)

Default to **FYI**. Promote to **Action required** only when the email passes BOTH a verb test and an addressed-to-user test. Most morning false positives come from over-eager promotion — when in doubt, demote.

**Verb test — does the email ask the user to *do* something?**

The body or subject must contain an actionable verb directed at the user: *reply, review, approve, merge, sign, decide, schedule, draft, fix, investigate, attend, confirm-by-deadline, vote, complete-form, RSVP*. Status verbs (*is, was, has been, will be, completed, deployed, merged, closed*) describe state and do not qualify.

**Addressed-to-user test — is the ask aimed at the user?**

- ✅ User is in `To:` and named in the ask, OR user is the sole recipient, OR user is explicitly @mentioned in body
- ❌ User is on `Cc:` with no name-call ("CC'd for awareness")
- ❌ Email is to a distribution list (`pyrite-team@`, `dev-all@`) with no per-user ask
- ❌ Automated notification (Jira `DoNotReply`, GitLab pipeline, Outlook calendar response) with no human ask layered on top

**Auto-demote to FYI (do NOT render as Action required):**

| Pattern | Why it's FYI |
| :--- | :--- |
| **OOO autoresponder / "I'm out of office, contact X"** | The "contact X" is conditional on the user *needing* something; the email itself contains no ask. Render in FYI as `[[@Person]] is OOO {{dates}}; covered by [[@Backup]]`. |
| **Status broadcast** ("X has been deployed", "Sprint 4 starts Monday", "RHOSP maintenance window confirmed") | State report. No verb directed at the user. |
| **Calendar invite, no body content, you're not the organizer** | The invite itself is the action — accepting/declining is handled in Outlook, not via the briefing. |
| **"FYI" / "For your awareness" / "Heads up" subject lines** | The sender already self-classified. Trust them. |
| **Automated digests** (newsletters, build pipeline summaries, Jira sprint-scope-change pings) | No human ask. |
| **Reply-all chatter on a thread where someone else owns the resolution** | The user is a witness, not an actor. Render as FYI ("12 comments on !2109 — Padmaraju iterating; spot-check optional"). |
| **"Thanks!" / "Got it" / acknowledgment-only replies** | No ask. |
| **Meeting recap / minutes with no per-attendee action items** | The action items live inside; if the user has one named in the body, *that* is the Action — not the recap email itself. |

**When promoting to Action required, the bullet must answer: *what verb, by when, blocking what?*** If you can't answer all three, demote to FYI.

**Record what was demoted.** Track every email that *could* have been promoted but was demoted by this rule (subject + sender + one-word reason). After triage, append a single footer line under the FYI section: `> _Auto-demoted from Action (N items): {{subject}} ({{reason}}); {{subject}} ({{reason}})._` so the user can audit the classifier without re-reading every email.

### 4. Analyze today's schedule

Identify:

- **Conflicts** — overlapping meetings
- **Back-to-back stretches** — 3+ consecutive meetings with no gap
- **Prep gaps** — high-stakes meetings (external attendees, leadership, customer) with no buffer beforehand
- **Free blocks** — contiguous gaps ≥45 min suitable for focus work
- **No-lunch flag** — no free block between 11:30–13:30

### 5. Discover vault link conventions

Before rendering, scan the vault to find existing notes for people mentioned in the briefing data (meeting attendees, email senders). This lets the report use real `[[wikilinks]]` instead of plain names.

**People convention:** each person has their own folder under `🤼 Team/{Category}/{Display Name}/` (e.g., `Dev Teams/Alex R/`, `Dev Teams/Sam/`), and the canonical note inside is `@Firstname Lastname.md` (with literal `@` prefix). Wikilink target uses that filename without extension: `[[@Firstname Lastname]]`.

- `Glob("{{vault_root}}/🤼 Team/**/@*.md")` — enumerate all canonical person notes
- Build a name → wikilink-target map. Match flexibly: full name from email/calendar may need to map to the existing `@First Last` note
- If no match, render the name as plain text — **never invent a wikilink target** (broken links pollute the graph)
- For team/project names (e.g., "Quartz", "Garnet", "Slate" under `Scrum Teams/`), link similarly when a folder/note exists. Verify with `Glob` before linking.

**Team daily notes convention:** each scrum team has its own daily note per work date under `Scrum Teams/{Team}/Scrum 📅/{INC}/{Sprint}/YYYY-MM-DD.md`. The filename is plain ISO date (no `D` prefix — that distinguishes it from your personal daily note `YYYY-MM-DDD.md`). The three parent folders carry the team, increment, and sprint metadata.

- `Glob("{{vault_root}}/Scrum Teams/**/YYYY-MM-DD.md")` — for each date in scope (today for the daily report; each Mon–Fri for the weekly; each week's dates for the monthly), enumerate matching team notes.
- Parse the path: split on `/`, find the segment after `Scrum Teams/` (= **team**), then the segments under `Scrum 📅/` (= **INC**, then **sprint**).
- Wikilink format — use the **full path** with a display alias so Obsidian resolves unambiguously and the link text stays short: `[[Scrum Teams/{Team}/Scrum 📅/{INC}/{Sprint}/YYYY-MM-DD|{Team}]]`. Append the INC/sprint inline as plain text after the link.
- If no team notes exist for a given date, omit the team-notes line entirely (don't render an empty header — the absence is the signal).

### 6. Render the report and save to vault

Use [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md). Lead with the executive summary (3-5 bullets), then the structured sections. Keep the whole report scannable in <60 seconds.

**Executive summary voice — personal-assistant lens.** The summary bullets are not free-form prose; they are written through the **personal-assistant** persona's Decision Lens (reduce mental load, prevent missed commitments, keep the next action obvious). Each bullet must satisfy the persona's Output Requirements: the **next action**, the **timing/deadline** if known, and any **dependency or follow-up**. Avoid bullets that merely describe the day ("4 meetings, 12 unread emails") in favor of bullets that name what the user should do about them ("Reply to [[@Alex R]]'s spec question before the 2pm review — blocks [[@Sam Chen]]'s implementation"). When 3+ bullets compete for the top slot, apply the persona's Eisenhower framing (urgent × important) to rank.

**Carryover rule (Open Action Items):** when populating the `Carrying over (still open)` subsection from the prior daily note (`last_run_date`), `Read` that note's `### ✅ Open Action Items` section and copy **only `- [ ]` lines**. Every `- [x]` line is already done — drop it. This rule applies to both subsections of the prior note (`Carrying over` and `New / from window`); merge the surviving `- [ ]` items into today's `Carrying over (still open)`. If the prior note has zero remaining `- [ ]` items, omit the subsection entirely rather than render an empty header.

**Mandatory: every surviving `- [ ]` item from `last_run_date` MUST be run through the phantom-carryover guard (below) BEFORE being rendered in today's note.** The carryover rule produces a *candidate list*; the phantom guard is the *filter* that decides which candidates survive. Skipping the phantom guard is the #1 cause of stale items re-spawning across weeks. Do not render any `- [ ]` carryover bullet that has not been age-scored and signal-checked.

**Recently-closed dedup rule (applies to `New / from window`):** before adding a `- [ ]` bullet to today's `New / from window` subsection, check whether the same actionable item was completed in any of the last **7 daily notes**. This catches the case where the underlying state (an unanswered email, an open Outlook flag, a stale Jira watcher) still looks "open" to Outlook but the user actually closed the loop offline and marked the vault `[x]` — without this check the briefing keeps re-spawning the same item with louder emojis (see [[feedback_briefing_stale_action_dedup]]).

1. `Glob("{{vault_root}}/📅/**/[0-9][0-9][0-9][0-9]-[0-9][0-9]-D[0-9][0-9].md")`, filter to the **7 most recent dates strictly before today**.
2. For each, `Read` the file and collect every `- [x]` line under `### ✅ Open Action Items` (both subsections).
3. **Match heuristic** — two items are "the same" if their normalized action signatures match. Signature = lowercase + strip emojis/badges (⚠/🚨/🟥/🟧 etc.) + strip overdue/deadline annotations (`OVERDUE`, `N DAYS OVERDUE`, `due Fri YYYY-MM-DD`, `(was due ...)`) + strip the leading verb-and-target keyword pair only (e.g., `reply to @Jordan Chen` + `April shout-outs` survive; the noise around them does not). Wikilinks like `[[@Jordan Chen]]` count as their inner name. Tag suffixes (`#email`, `#mr`) are part of the signature only when they materially change the action.
4. **Apply by recency**:
   - **Match in last 3 days (days T−1, T−2, T−3)** — **suppress silently**. Do not render the new bullet. Add one consolidated line under the `New / from window` subsection footer: `> _Recently closed (suppressed today): {{normalized title}} (closed [[YYYY-MM-DDD]])._` so the user can see what was filtered.
   - **Match 4–7 days back** — render the new bullet, but prefix with `⚠️ Re-surfaced — last closed [[YYYY-MM-DDD]]. Confirm: still open, re-opened, or false re-spawn?` and raise an `AskUserQuestion` before writing the file. Options: `Still open (keep)`, `Already done (suppress like recent)`, `Re-opened — clarify` (free text). Apply the answer to today's file.
   - **No match in 7 days** — render normally; this is a genuinely new item.
5. This dedup runs only for `New / from window`. The `Carrying over` subsection already filters by `[ ]` vs `[x]` and does not need the recency check.

**Suppression memory check (applies to BOTH `Carrying over` and `New / from window`):** at the start of action-item rendering, scan loaded memory for any `feedback_*_resolved.md` entries (the convention is documented in the Phantom-carryover guard below). Each such memory documents a specific item that should **never** be rendered as an action again. For every `- [ ]` candidate, compare its normalized signature against the suppression memory's signature. On match, drop the candidate silently and add a one-line footer under `New / from window`: `> _Suppressed by [[<memory-name>]] ({{reason}})._` Do not prompt — the user has already decided.

**Action-item classifier (applies to BOTH `Carrying over` and `New / from window`):** before rendering ANY `- [ ]` bullet in this section, re-apply the verb test and addressed-to-user test from § 3a. The Open Action Items section is for things the user must *do* — not for state they should *know*. If the bullet is informational (status broadcast, OOO acknowledgment, FYI), move it to the Notes & Follow-ups section as a plain bullet (no checkbox).

Concrete patterns to catch (these have all leaked through before):

- **"Reach out to [[@Person]] backups — OOO through M/DD"** — the user only reaches out *if* they need that person. Pure FYI. Render in Notes & Follow-ups as `[[@Person]] OOO through {{date}}; backups: [[@Backup1]], [[@Backup2]]`.
- **"Read [meeting notes / newsletter / addendum]"** — only an action if a specific decision is pending or a question is directed at the user. Otherwise FYI.
- **"Verify X was sent yesterday"** — borderline. Keep as Action only if the verification is time-critical (e.g., RHOSP shutdown ack with maintenance starting today). Otherwise demote.
- **"Decide: [topic]"** with no external deadline and no one waiting on the answer — this is a personal-grooming item, not a commitment. Move to a separate `### 💭 Open questions (no external deadline)` subsection inside Notes & Follow-ups; do NOT carry as `- [ ]`.

**Phantom-carryover guard (REQUIRED for every `- [ ]` carryover candidate):** an item that has carried as `- [ ]` for more than **5 consecutive daily notes** with no fresh email/Jira/MR/calendar signal in the briefing window is almost certainly stale — and even items at age 3-4 with no fresh signal warrant a prompt. The guard has three explicit phases; **never skip them, even when running non-interactively**. Apply this check BEFORE the age-3 prompt below.

**Phase A — Compute age (explicit scan, not inference).**

The carryover rule reads only `last_run_date`. The age scan reads further back. This is the load-bearing distinction — without the explicit scan, items have "age 1" forever from the briefing's perspective even though they've been carrying for weeks.

1. `Glob("{{vault_root}}/📅/**/[0-9][0-9][0-9][0-9]-[0-9][0-9]-D[0-9][0-9].md")`, filter to the **14 most recent dates strictly before today**, sorted descending.
2. For each candidate item from `last_run_date`, normalize its signature (per the dedup rule's normalizer in § 6 step 3 — lowercase, strip emojis/badges/deadline-annotations, keep verb+target keyword pair).
3. `Read` each of the 14 prior notes' `### ✅ Open Action Items` sections. Count consecutive prior notes (walking backward from `last_run_date`) where the same normalized signature appears as `- [ ]`. Stop counting at the first gap (a note where the signature is absent or `- [x]`).
4. `age = that consecutive count`. If the item appears as `- [ ]` in `last_run_date` only and nowhere prior in the 14-day window, `age = 1`.

**Phase B — Check for fresh signal (explicit checklist, not vibes).**

A "fresh signal" means *new evidence in the current briefing window that the item is genuinely live*. The check is a fixed checklist — do not infer freshness from tangential mentions.

For each item with `age ≥ 3`, scan the current briefing window's data (the emails + calendar from step 2) and mark a fresh signal present **only if at least one of these is true**:

- **Email — direct correspondence.** An email *from* the named person *to* the user (`To:` line, not `Cc:`), OR an email *from* the user *to* the named person, in the briefing window. Mentions of the person in third-party emails (e.g., memos, intern intro thread, recap minutes) do **not** count.
- **Email — explicit subject match.** An email subject in the window contains the Jira ticket key, MR number, or document name from the item's signature. PR labels (`gatekeeper_ready` etc.) on a *different* MR do not count.
- **Calendar — scheduled touchpoint.** A meeting in the briefing window or today's calendar lists the named person as an attendee AND is in a context plausibly related to the item (1:1, project sync, review). Standing all-hands meetings (CCB, knowledge transfer, morning coffee) do **not** count.
- **Jira/MR — direct activity.** A `[JIRA]` or `gitlab` notification email in the window references the exact ticket key or MR number in the item's signature. Activity on adjacent tickets does **not** count.

If none of the above are true, **fresh signal is absent**. Do not stretch — the failure mode is over-eager freshness inference (e.g., "Patel is in the feedback request email therefore the Patel PRJ-23240 question is still live"). Tangential presence is not freshness.

**Phase C — Decide.**

| `age` | Fresh signal? | Action |
| :--- | :--- | :--- |
| 1–2 | (don't check) | Render normally; no prompt. |
| 3–4 | Yes | Continue to the age-3 stale-carryover prompt below. |
| 3–4 | No | Render with `_(phantom check: age N, no fresh signal in window)_` annotation **and** raise the phantom prompt (below). |
| ≥ 5 | Yes | Continue to the age-3 stale-carryover prompt. |
| ≥ 5 | No | Raise the phantom prompt unconditionally. **Do not render the item** until the user responds. |

**Phantom prompt, non-interactive fallback, and the memory write on close:** see [PROMPTS-AND-EDGE-CASES.md](PROMPTS-AND-EDGE-CASES.md#phantom-carry-over-prompt). Never skip the prompt when Phase C calls for it.

**Stale carryover rule (applies to `Carrying over (still open)`):** items that survived the phantom guard use the Phase A `age`. Age 1–2 renders normally; **age ≥ 3 prompts before rendering** — options, how to apply each answer (including flipping every prior `- [ ]`), the two-emoji cap, and the non-interactive fallback are in [PROMPTS-AND-EDGE-CASES.md](PROMPTS-AND-EDGE-CASES.md#stale-carry-over-prompt-age--3).

**Embedded visual surfaces** — the template includes `![[Daily Notes Dashboard.base#...]]` and `![[TODO#By tag]]` embeds that auto-render when the file opens. They depend on these vault files existing:
- `📅/Daily Notes Dashboard.base` (views: `All daily notes`, `This Week`, `Recent (cards)`) — scopes to daily notes (`📅/**/YYYY-MM-DDD.md`)
- `📅/Weekly Rollups.base` (views: `All weeks`, `Recent weeks`) — scopes to weekly notes (`📅/**/YYYY-W{NN}.md`)
- `📅/Scrum Team Activity.base` (views: `Recent activity`, `By team`) — scopes to scrum team daily notes under `Scrum Teams/`
- `TODO.md` (sections: `By tag`) — Dataview-driven; out of scope for auto-creation here

**Detect missing bases on every run:** `Glob` the three `.base` files at `📅/`. If any are missing, follow [PROMPTS-AND-EDGE-CASES.md](PROMPTS-AND-EDGE-CASES.md#missing-dashboard-bases) (ask, then create via `obsidian-bases`). `TODO.md` is user-managed — warn only.

**⛔ Pre-save section checklist (run BEFORE writing the file).** The chart and team-link sections have silently vanished from real runs before (4 consecutive June 2026 notes lost the Mermaid chart; see [[feedback_daily_note_mandatory_sections]]). Before calling `Write`, confirm the assembled report body contains ALL of these — if any is missing, add it (render a minimal/placeholder version rather than skipping):

1. `#### Day at a glance` with a ` ```mermaid ` `gantt` block.
2. `#### Email triage at a glance` with a ` ```mermaid ` `pie` block.
3. `### 👥 Team Daily Notes` with a `[[Scrum Teams/.../YYYY-MM-DD|...]]` wikilink — **unless** the step-5 `Glob` returned zero team notes for the date (genuine absence).
4. `### 📊 Cross-day context` with both `![[Daily Notes Dashboard.base#Recent (cards)]]` and `![[TODO#By tag]]` embeds.

A plain-bullet schedule table does NOT satisfy #1 — the gantt is required in addition to (not instead of) any table.

**Save to vault:**

1. Compute Pittsburgh date: `YYYY`, `MM`, `YYYY-MM-DD`.
2. Create folders if missing — single command: `mkdir -p "{{vault_root}}/📅/YYYY/MM"` (forward slashes work in bash on Windows; the 📅 emoji is preserved).
3. Target file: `{{vault_root}}/📅/YYYY/MM/YYYY-MM-DDD.md` — the `D` prefix goes on the **day component only**, not the year/month and not the folder names. Example for May 5, 2026: `2026/05/2026-05-D05.md`.
4. **Do not overwrite an existing file silently.** If it exists, `Read` it first and ask the user via `AskUserQuestion` whether to overwrite, append a new section (e.g., `## Afternoon update — HH:MM`), or skip the save.
5. Use `Write` with the full report content (frontmatter + body per template).
6. Print the saved path back to the user as a clickable markdown link.

After saving, also display the executive summary inline in chat so the user gets the briefing without opening the file.

### 7. Update the weekly rollup note

After the daily note is saved, regenerate the weekly rollup. Full template, ISO-week math, and preservation rules in [WEEKLY_TEMPLATE.md](WEEKLY_TEMPLATE.md).

**Workflow:**

1. Compute ISO week-year, ISO week number, and the Monday→Friday dates for this week (Pittsburgh time).
2. Compute the weekly file path: `📅/YYYY/MM/YYYY-W{NN}.md` where `MM` = month of the Monday.
3. Ensure the month folder exists (`mkdir -p`).
4. For each Mon–Fri date, check if `📅/YYYY/MM/YYYY-MM-D{DD}.md` exists; if so, `Read` it and extract every `- [ ]` line (unchecked only). Also `Glob("Scrum Teams/**/YYYY-MM-DD.md")` for the same date to collect team daily notes (parse team/INC/sprint from the path per step 5).
5. If a weekly file already exists at the target path, `Read` it and capture everything after the `<!-- end:auto-managed -->` marker — that user content must be preserved in the new write. If markers are missing, ask via `AskUserQuestion` before overwriting.
6. Render the new weekly content per [WEEKLY_TEMPLATE.md](WEEKLY_TEMPLATE.md): navigation links, week-at-a-glance (2-4 bullets pulled from today's executive summary + cross-day themes), and the per-day TODO rollup.
7. `Write` the file: auto-managed region + preserved user content (or default `## Notes` placeholder if none).
8. Print the saved weekly path back to the user as a clickable markdown link.

**Bidirectional links:** the daily note's frontmatter or footer should link to the weekly note (`[[YYYY-W{NN}]]`), and each daily entry in the weekly rollup links to the daily note. This makes Obsidian's graph and backlinks work both ways.

### 8. Update the monthly rollup note

After the weekly note is saved, regenerate the monthly rollup. Full template, week-selection logic, and preservation rules in [MONTHLY_TEMPLATE.md](MONTHLY_TEMPLATE.md).

**Workflow:**

1. Compute the current calendar year and month (Pittsburgh time).
2. Compute the monthly file path: `📅/YYYY/YYYY-M{MM}.md` — this lives in the **year folder**, not a month subfolder.
3. Ensure the year folder exists (`mkdir -p`).
4. Determine which weeks to include: all ISO weeks whose **Monday** falls in the current month, plus one trailing week for forward visibility (typically 5 entries; 6 if the month has 5 in-month Mondays).
5. For each selected week, check if `📅/YYYY/MM/YYYY-W{NN}.md` exists (where `MM` follows that week's Monday). If so, `Read` it and extract the bullets under the `#### 🎯 Week at a glance` section. Also `Glob("Scrum Teams/**/YYYY-MM-DD.md")` for each Mon–Fri of the week and aggregate the distinct **{team} {INC} / {sprint}** combinations that appeared at least once during the week.
6. If a monthly file already exists at the target path, `Read` it and capture everything after the `<!-- end:auto-managed -->` marker. If markers are missing (legacy format), prompt via `AskUserQuestion` before overwriting.
7. Render the new monthly content per [MONTHLY_TEMPLATE.md](MONTHLY_TEMPLATE.md): navigation with `<button class="date_button_today">This Month</button>`, month-at-a-glance (2-4 synthesized themes), and the per-week rollup with date ranges.
8. `Write` the file: auto-managed region + preserved user content.
9. Print the saved monthly path back to the user as a clickable markdown link.

**Note on cascading updates:** the monthly rollup reads from weekly notes, which read from daily notes. Always update in order — daily → weekly → monthly — so each layer reflects the latest data.

### 9. Propose focus blocks

**Delegate to `clarity-council` in single mode (personal-assistant persona).** This step does not author the block list inline — invoke the skill via `Skill`:

**Invocation**:
```
Skill: clarity-council (mode: single)

As a personal-assistant, propose focus blocks for today that pull the highest-leverage 
open actions into the free time available.

Open actions:
[carry-over items from prior days]
[new action items from today]

Today's prep needs:
[high-stakes meetings without buffer time]

Free blocks (≥45 min):
[list of available time slots]

Constraints:
[no-lunch flag if set, other scheduling rules]

Output:
- Prioritized focus blocks with start/end times
- For each block: which action item(s) it covers, why this priority order
- Confidence level for each recommendation
```
- **desired_outcome:** *"A ranked focus-block proposal table — `Time | Block | Purpose` — where each row obeys the persona's Output Requirements: names a concrete next action, ties to a deadline or commitment, and surfaces any dependency (e.g. blocked-by-person, awaiting-input). Apply the Eisenhower Matrix to rank urgent × important. Protect attention: do not propose more than 3 blocks before lunch, and do not break a long contiguous free block into fragments unless the underlying actions genuinely call for it."*
- **constraints:** `[only propose blocks that fit into existing free time (no overlapping meetings), preserve at least one 45-minute uninterrupted window if the day allows it, do not auto-fill every gap]`
- **depth:** `brief`

The persona's Failure Modes (overcommitting, fragmenting attention, turning a small ask into a process) and Blind Spots (over-organizing at the expense of judgment) are the guardrails — if the council output trips them, re-prompt before showing the user.

Present the returned proposal table to the user, then ask via `AskUserQuestion` which blocks (if any) to add to the calendar. For each approved block, call `outlook_check_calendar_conflict` first, then `outlook_create_meeting_draft` with no attendees and `busy_status="busy"`. Never create blocks without explicit approval.

## Rules

- **Read-only for Outlook.** Never mark emails read, flag, move, or delete during briefing.
- **Vault writes are scoped.** Only write to `{{vault_root}}\📅\` — never modify other vault folders.
- **Never overwrite an existing daily note silently.** Always confirm with the user first.
- **Weekly and monthly notes: auto-managed region only.** Regenerate the content between the `<!-- begin:auto-managed by daily-briefing skill -->` and `<!-- end:auto-managed -->` markers. Preserve everything outside those markers verbatim. If markers are missing on an existing weekly or monthly note (legacy hand-edited format), prompt before overwriting — there may be user-authored content to migrate.
- **Checkboxes for action items.** All open action items use `- [ ]` so the global `TODO.md` Dataview query (which scans `📅/`) picks them up automatically.
- **Wikilinks only when targets exist.** Verify the note exists before writing `[[Name]]` — broken links pollute the graph.
- **Drafts only for calendar blocks.** Use `outlook_create_meeting_draft` (opens for review); never auto-send or auto-create finalized appointments.
- **Confirm before drafting.** Always ask which proposed blocks to create — don't batch all.
- **Respect privacy.** If an email subject contains "confidential", "personal", "HR", or "legal", surface only "private email from <sender>" without subject details.
- **Time math.** All times reported in **local time** (America/New_York — EST/EDT, observes DST). Outlook returns local; if any value comes back in UTC or another zone, convert before display. When computing "24 hours ago", anchor on current Pittsburgh wall-clock time.
- **Unavailable MCP.** If `mcp__outlook__*` tools fail, tell the user the Outlook MCP isn't responsive and stop — don't fabricate a briefing.

## Edge cases

Empty inbox/calendar, all-day and cancelled events, no prior note, a gap over 14 days, a same-day re-run, and backfill briefings: see [PROMPTS-AND-EDGE-CASES.md](PROMPTS-AND-EDGE-CASES.md#edge-cases).

## Optional deep-dive

If the user asks for more detail on a specific thread, use `outlook_get_conversation(message_id=...)` to pull the full thread.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/daily-briefing.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
