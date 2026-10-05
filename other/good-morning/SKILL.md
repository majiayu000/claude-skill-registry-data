---
name: good-morning
category: scrum-sprint
description: >
  Morning kickoff wrapper running sprint-snapshot, daily-standup-prep, and daily-briefing in
  order; idempotent on same-day re-runs. Use when the user says "good morning", "morning
  routine", "kick off my day", "start my day", or invokes /good-morning.
codex-short-description: "Morning kickoff: sprint snapshot, standup prep, and daily briefing in order"
related-skills:
  - sprint-snapshot
  - daily-standup-prep
  - daily-briefing
loop-eligible: false
recurrence-hint: daily
allowed-tools:
  - Skill
  - AskUserQuestion
  - Bash
  - Read
  - Edit
  - Glob
compatibility: claude-code codex opencode
---
# Good Morning

Single-command wrapper that runs the user's three morning skills in order. Owns no business logic of its own — every artifact is produced by the delegated skill. This skill exists so the user types one command instead of three.

## Quick start

```text
/good-morning                 → run all three phases for default team(s)
/good-morning Aurora          → pass team override down to sprint-* skills
/good-morning --skip-snapshot → skip phase 1 (e.g. snapshot already captured today)
```

Any extra args (team names, `--inc`, `--sprint`, `--days`, etc.) are forwarded to the sub-skills that recognise them. The wrapper itself only consumes `--skip-snapshot`, `--skip-calendar`, `--skip-standup`, `--skip-briefing`.

## Workflow

```text
- [ ] Phase 1:   sprint-snapshot --phase daily            (Jira → vault canvas + md + jsonl)
- [ ] Phase 1.5: team-calendar OOO digest                 (Confluence ICS → who's out this window)
- [ ] Phase 2:   daily-standup-prep --include-sprint-pulse (per-team standup report + burndown)
- [ ] Phase 3:   daily-briefing --no-focus-blocks         (Outlook 24h recap + today's schedule)
- [ ] Phase 4:   One-line summary of artifacts written
```

Run phases **sequentially, never in parallel**. Phase 2 depends on Phase 1's JSONL trend row (burndown forecast reads it). Phase 1.5 runs between them so its OOO digest can flow into both Phase 2 (capacity/coverage) and Phase 3 (FYIs). Phase 3 is independent but ordered last by design.

**Auto-continue between phases.** When a phase completes, immediately invoke the next one — do not pause for user acknowledgment, do not summarise mid-flight, do not ask "shall I continue?". The user invoked /good-morning expecting the whole chain to run unattended. The only legitimate stop points are:

1. A hard failure in Phase 1 (abort the wrapper).
2. A sub-skill raising a genuinely blocking `AskUserQuestion` that the wrapper cannot answer on the user's behalf (e.g. missing roster CSV with no source path). In that case, forward the prompt as-is.
3. **`daily-briefing`'s stale-carryover prompt or recently-closed re-surface prompt** — these are intentional user decisions about specific action items (still open vs done vs cancel vs defer; re-spawn vs false re-surface). Forward as-is; never auto-answer "Still open" on the user's behalf, since silently keeping a stale item is exactly the failure mode these prompts exist to prevent. See `daily-briefing/SKILL.md` § "Recently-closed dedup rule" and § "Stale carryover rule".

Overwrite prompts, "continue?" prompts, and any other yes/no the wrapper can answer for the user should be auto-answered with the continue/overwrite option — never paused for input.

### Phase 1 — Sprint snapshot (daily tag)

Invoke via `Skill`: `sprint-snapshot` with `--phase daily` (preserves literal `daily` in filenames per sprint-snapshot's phase rule). Forward any team / inc / sprint args the user supplied.

Tell the sub-skill the overwrite behavior up-front so it doesn't prompt: *"This run is from /good-morning — if `daily.canvas` or `daily.md` already exist for today, overwrite in place. Do not prompt."* The JSONL trend log is append-only — sprint-snapshot already handles that correctly.

If sprint-snapshot fails (Jira down, roster missing), surface the error and **abort the wrapper** — phases 2 and 3 expect the snapshot to exist.

### Phase 1.5 — Team-calendar OOO digest

Fetch the team's Confluence Team Calendar (PTO / OOO / Travel / Holiday) and build a short digest of who's out during the briefing window. This is the canonical out-of-office source — without it, vacations are only caught by chance from an email (e.g. John Doe's 6/23–6/29 PTO was missed by the schedule view and only surfaced via a manual status email). The digest flows into **both** Phase 2 (capacity/coverage) and Phase 3 (FYIs).

**Resolve the ICS URL** from memory: read `reference_team_calendar_ics.md` and take the `**Team Calendar ICS URL:**` line. If the memory is missing, skip this phase with a one-line warning in the Phase 4 summary (`⚠ Phase 1.5 skipped: no team-calendar ICS configured — add reference_team_calendar_ics.md`) — do **not** prompt or abort; the wrapper still produces all artifacts without it.

**Fetch + parse** with a single Bash call (read-only; never write the ICS into the vault). Save the feed to a scratch path under an allowed working dir (`C:/temp/teamcal.ics`), then parse with Python (`PYTHONIOENCODING=utf-8`). Parsing rules — these are load-bearing, get them wrong and the digest lies:

- **Unfold continuations first** — `re.sub(r'\n[ \t]', '', text)` after normalising `\r\n`→`\n`. Confluence wraps long lines.
- **All-day events; `DTEND` is EXCLUSIVE** (RFC5545). Subtract one day from `DTEND` for the human "last day out" — `DTSTART 20260629 / DTEND 20260704` = out **through 7/3**, back 7/4. Getting this wrong reports people back a day early.
- **Window filter:** keep events where `start <= horizon AND end_exclusive > today` (Pittsburgh local). Horizon = the current sprint's `end_date` from `_sprint.md` if available, else `today + 10 days`.
- **Attribute via the `CN=` field, NOT `SUMMARY`.** This is the load-bearing parsing fact: Confluence PTO events almost always have a bare `SUMMARY:PTO` and carry the person's name in the `ORGANIZER`/`ATTENDEE` line as `CN="Last, First"` (e.g. `ORGANIZER;X-CONFLUENCE-USER-KEY=...;CN="Doe, John";...`). Extract `CN="([^"]+)"` and match **last name AND first name** against the team roster CSV (`{{rosters_dir}}/<Team>.csv`). Matching only `SUMMARY` finds nobody — that was the bug that let John Doe's PTO go unsurfaced. Fall back to `SUMMARY` text only for the rare events that *do* name a person there (`Parrott - PTO`). Split into **attributed** (CN or summary matched a roster member) and **unattributed** (no roster match — counted as "N other platform-org entries", never invented into a roster name).
- **Merge adjacent same-person ranges.** One person often has several back-to-back PTO VEVENTs (e.g. 6/22–6/26 + 6/29–7/3). Collapse contiguous/overlapping ranges per person so the digest reads "John Doe PTO 6/22 → 7/3" rather than two fragments — otherwise the "last day out" understates the absence.
- **Category** comes from `CATEGORIES` (`PTO`, `Holiday`, `Travel`, `Conference`, `Appointment`, `Work Schedule`). Holidays apply to everyone; treat separately from individual PTO.

Build an **OOO digest** object: for each roster member out in-window → `{name, type, first_day, last_day_inclusive}` (after merging adjacent ranges per person); plus any team-wide Holiday; plus the unattributed count. Keep it to the roster + holidays — the calendar is the whole platform org (~960 events), so don't dump everything; the digest is just the handful of roster names plus holidays.

**Forward the digest** to the next two phases (pass it in the invocation text, since sub-skills don't read it themselves yet):

- **To Phase 2 (standup):** *"Team-calendar OOO this window: <digest>. Fold into the sprint-pulse capacity read and the scrum-master suggestions — a member who is OOO should not be flagged as 'no activity / confirm blocked', and their in-flight tickets are coverage risks. Reflect reduced effective capacity for OOO days."*
- **To Phase 3 (briefing):** *"Team-calendar OOO this window: <digest>. Render these as FYI bullets (`[[@Person]] OOO {{dates}}`) in the briefing, and factor team-wide Holidays into the schedule. Do not spawn action items from OOO (per daily-briefing § 3a — 'reach out to backups' is conditional, not a task)."*

If the fetch fails (TLS, network, non-200, empty body), **do not abort** — emit `⚠ Phase 1.5 skipped: team calendar unreachable (<reason>)` in the Phase 4 summary and continue. OOO data is high-value but not load-bearing for the other phases.

### Phase 2 — Standup report (with sprint burndown)

Invoke via `Skill`: `daily-standup-prep`. Pass `IncludeSprintPulse=true` explicitly so the clarity-council burndown chart + statistics-expert forecast + scrum-master suggestions run (this is the "sprint burndown" the user wants). Forward team / days args from the wrapper invocation.

Tell the sub-skill: *"Overwrite today's standup file(s) without prompting — /good-morning expects idempotent re-runs."*

If daily-standup-prep partially fails (e.g. GitLab unreachable), let it produce what it can — its degraded-mode output is still useful. Surface any warnings in Phase 4's summary.

### Phase 3 — Daily briefing (report + rollups, no focus blocks)

Invoke via `Skill`: `daily-briefing`. Phase 3 must produce **all three artifacts**:

1. **Daily report** — `{{vault_root}}\📅\YYYY\MM\YYYY-MM-DDD.md` (daily-briefing step 4)
2. **Weekly rollup** — `{{vault_root}}\📅\YYYY\MM\YYYY-W{NN}.md` (daily-briefing step 5)
3. **Monthly rollup** — `{{vault_root}}\📅\YYYY\YYYY-M{MM}.md` (daily-briefing step 6)

**Skip step 9 (focus-block proposal) entirely.** Tell the sub-skill: *"/good-morning is the caller — run steps 1 through 6 (daily report + weekly rollup + monthly rollup). Skip step 9 (focus blocks). Do NOT propose calendar blocks, do NOT create any meeting drafts. Stop after the monthly rollup is written."*

Same overwrite rule: if any of the three notes already exist for today, overwrite in place — no prompts.

### Phase 4 — Summary

Print one block summarising what was produced:

```text
=== Good morning — 2026-05-18 ===
✓ Snapshot:  [daily.canvas]  [daily.md]              (+1 trend row)
✓ OOO:       John Doe (PTO→6/29), Parrott (PTO→6/23)   (2 out, +1 unattributed)
✓ Standup:   [Aurora 2026-05-D18.md]                 (burndown ↘ on-track)
✓ Briefing:  [2026-05-D18.md]  [2026-W20.md]  [2026-M05.md]  (12 unread, 4 meetings today)
```

Use markdown links so the user can click straight into the vault. The `OOO:` line reflects the Phase 1.5 digest — if Phase 1.5 was skipped or the feed was unreachable, replace it with the `⚠ Phase 1.5 skipped: <reason>` line instead.

**Then run the daily-note section-completeness check (belt-and-suspenders).** `daily-briefing`'s § "Pre-save section checklist" should guarantee these, but the chart silently vanished from 4 consecutive June 2026 notes before the checklist existed — so the wrapper re-verifies. `Read` today's daily note (`{{vault_root}}/📅/YYYY/MM/YYYY-MM-DDD.md`) and confirm it contains all four mandatory surfaces (see [[feedback_daily_note_mandatory_sections]]):

1. A `#### Day at a glance` Mermaid `gantt` block.
2. A `#### Email triage at a glance` Mermaid `pie` block.
3. A `### 👥 Team Daily Notes` standup wikilink — unless `Glob("{{vault_root}}/Scrum Teams/**/YYYY-MM-DD.md")` returns zero matches for today.
4. A `### 📊 Cross-day context` block with the `![[Daily Notes Dashboard.base#Recent (cards)]]` + `![[TODO#By tag]]` embeds.

If any is missing, `Edit` it into the note in place (reconstruct the gantt from the schedule section, the pie from the email-triage counts, the standup link from the `Glob` result) and append a one-line note to the Phase 4 summary: `↻ Repaired missing daily-note sections: <list>`. Do NOT prompt — the sections are mandatory, so repair silently. If this check repairs sections on >1 run, that signals `daily-briefing`'s pre-save checklist is being skipped and needs tightening.

> ⛔ **When reconstructing the gantt, never put a colon (`:`) inside a task label.** Mermaid splits each task line on the first colon to find the `:HH-mm, NNmm` metadata, so a label like `Gap 09:00-10:00 :09-00, 60mm` fails with `Invalid date`. Write time ranges in labels with periods (`Gap 09.00-10.00`, `Lunch gap 12.00-15.00`) and keep the only colon in front of the metadata. See `daily-briefing/REPORT_TEMPLATE.md` § "Day at a glance" for the full rule.

**Then run the action-item post-filter pass (belt-and-suspenders).** `daily-briefing` should have applied the verb test and addressed-to-user classifier from its § 3a and the phantom-carryover guard from § 6, but those rules occasionally let an FYI slip through as a `- [ ]` item. Re-read today's daily note and audit the `## ✅ Open Action Items` section:

1. `Read` `{{vault_root}}/📅/YYYY/MM/YYYY-MM-DDD.md` and extract every `- [ ]` line from `### Carrying over (still open)` and `### New / from window`.
2. For each item, re-apply the heuristics from `daily-briefing/SKILL.md` § 3a:
   - **Verb test** — does the bullet name an actionable verb directed at the user (reply / review / approve / merge / sign / decide-with-deadline / schedule / draft / fix / investigate / RSVP)? Status verbs (is, was, has been) fail.
   - **Addressed-to-user test** — is the ask aimed at the user specifically, or is it broadcast / informational / conditional?
   - **OOO / FYI patterns** — "reach out to X backups" (X is OOO, no actual task), "read [meeting notes]" with no decision pending, "verify Y was sent" with no time-criticality, "decide: [topic]" with no external deadline or stakeholder waiting.
   - **Phantom test** — does the bullet contain a person/MR#/Jira ticket that does NOT appear anywhere in today's `📨 Email Triage` section or `🗓️ Today's Schedule`? If so, there's no fresh signal backing it and it's likely stale.
3. If any items fail the audit, `Edit` the daily note:
   - Remove the bullet from `## ✅ Open Action Items`.
   - Insert it as a plain bullet (no checkbox) under `## 📝 Notes & Follow-ups` if the item still has informational value (OOO notice, status awareness).
   - Drop it entirely if it's a phantom with no information content.
4. Append a one-line console note in the Phase 4 summary listing what was reclassified: `↻ Demoted N action items to Notes & Follow-ups: <one-line list with reason per item>`. Do NOT prompt — the heuristics are conservative enough to demote silently per user feedback. If the user wants to keep something demoted, they can manually restore it.

This is a sanity net, not the primary classifier. If this step is consistently demoting >2 items per run, that's a signal that `daily-briefing/SKILL.md` § 3a needs to be tightened further.

**Then run a personal-assistant pass.** Phase 3 (daily-briefing) was invoked with `--no-focus-blocks`, so the user never sees a focus-block proposal during `/good-morning`. To preserve the "what should I actually do next" signal without re-introducing calendar drafts, invoke `clarity-council` via `Skill` in single mode, persona pinned to `personal-assistant`. Pass:

- **user_problem:** *"Given today's standup and briefing artifacts, what are the 3 most important next actions for the user?"*
- **context:** the executive-summary bullets from the daily briefing (read from `{{vault_root}}/📅/YYYY/MM/YYYY-MM-DDD.md`), the burndown verdict from the standup report, and any impediments/blockers surfaced in Phase 2.
- **desired_outcome:** *"A `## Next actions` block — 3 bullets max, each naming a concrete action, timing/deadline, and any dependency or follow-up. No calendar drafts (that's owned by `/daily-briefing` step 9 when invoked standalone)."*
- **depth:** `brief`

Append the persona's `## Next actions` block to the Phase 4 console output. This makes the wrapper output actionable in its own right rather than just an artifact-link manifest.

## Rules

- **Sequential, never parallel.** Phase 2 reads Phase 1's JSONL; Phase 3 is independent but ordered last by design.
- **Auto-continue between handoffs.** When one phase finishes, the next starts immediately. No pause, no acknowledgment prompt, no mid-flight summary. Only stop for a hard Phase-1 failure or a genuinely blocking sub-skill question the wrapper can't auto-answer.
- **Idempotent.** Re-running on the same day overwrites today's artifacts in place. Never prompt — the user has already opted in by invoking /good-morning. The JSONL trend log is the only exception (append-only, by design).
- **Phase 3 = three artifacts.** Daily report + weekly rollup + monthly rollup. All three. Skip only step 9 (focus blocks).
- **No focus blocks, no calendar drafts.** Phase 3 is report-only. Do not propose blocks, do not create meeting drafts.
- **Forward, don't reinterpret.** Team names, `--inc`, `--sprint`, `--days`, etc. are passed through verbatim to whichever sub-skill recognises them. The wrapper doesn't validate them.
- **Abort on Phase 1 failure.** A missing snapshot breaks Phase 2's burndown. Phases 2 and 3 may degrade gracefully; Phase 1 may not.
- **Phase 1.5 is best-effort, never blocking.** The team-calendar fetch/parse can fail (TLS, network, ICS schema drift) without affecting the other phases — skip with a `⚠` summary line, never abort. It reads the ICS read-only and never writes the feed into the vault.
- **DTEND is exclusive.** Whenever the wrapper renders an OOO date range (digest, summary, forwarded text), the "last day out" is `DTEND − 1 day`. Reporting someone back a day early is the failure mode to avoid.
- **No new memory writes.** All config (vault root, default team, Jira project, team-calendar ICS URL, etc.) is *read* from existing memory keys; the wrapper writes no memory files. (The ICS URL lives in `reference_team_calendar_ics.md`, created once out-of-band — the wrapper only reads it.)

## Edge cases

- **`--skip-snapshot`** — skip Phase 1 only if the user explicitly opts out (e.g. they already ran it from `/sprint-snapshot` earlier). Phase 2 will still attempt to read the most recent JSONL row.
- **`--skip-standup` / `--skip-briefing`** — same pattern; document in the Phase 4 summary which phases ran.
- **Sub-skill prompts despite the override instruction** — answer with the overwrite-equivalent option (`Overwrite`) on the user's behalf, since /good-morning already implies consent. Do not re-ask.
- **Today is a weekend or holiday** — still run all three phases; the artifacts are useful for catch-up. daily-briefing's window logic already handles gap days. If Phase 1.5 finds a team-wide `Holiday` event covering today, note it in the digest so the standup/briefing don't read an empty calendar as "everyone idle".
- **Team-calendar ICS missing or unreachable** — skip Phase 1.5 with a `⚠` line in the Phase 4 summary; the other phases run unchanged. Add/repair the URL in `reference_team_calendar_ics.md`.
- **`--skip-calendar`** — skip Phase 1.5 explicitly (e.g. the feed is down and the user doesn't want the warning noise). The wrapper consumes this flag alongside `--skip-snapshot` / `--skip-standup` / `--skip-briefing`.
- **OOO summary looks wrong by one day** — almost always the exclusive-`DTEND` rule; the last day out is `DTEND − 1`.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/good-morning.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
