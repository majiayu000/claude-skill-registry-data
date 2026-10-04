---
name: meeting-ingest
description: Turn a meeting transcript (pasted text, or a Google Doc / Drive link) into a structured note in 04-meetings/ — decisions, action items, tensions, dynamics — and propagate to the people, project and daily notes. Transcript-first — the summary tab is only a flagged fallback. Use when the user says "process this meeting", "ingest meeting", pastes a transcript, or shares a Meet transcript link.
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, meetings, capture]
    related_skills: [people-update, knowledge-stub, daily-digest]
    requires_toolsets: [second_brain]
---

# Meeting ingest (Hermes edition)

Keep verbatim what commits someone (decisions, actions, disagreements, numbers); drop pleasantries,
"you're on mute", repetitions. Never invent a deadline or an owner.

1. `sb_brief`. If the meeting matches a *Sensitive meetings* entry, stop and ask before ingesting.
2. Get the text. Drive link or id → `sb_drive_doc(file_or_url)`: it applies the transcript-first rule and
   returns `transcript_source` (`verbatim` | `summary-fallback` | `full-document`) plus a `warning` when only
   a summary exists. Pasted text → use it as `verbatim`. Note the date (transcript, calendar, or ask).
3. Participants → `sb_find_person(name)` each; `exact`/`likely` → `[[02-people/Name]]`; `none`/`ambiguous`
   → list them in your report, link nothing, create nobody. Project → `sb_search(topic, folder="03-projects")`.
4. Extract: **decisions** (what / why verbatim / who / reversibility reversible|hard-to-reverse|one-way),
   **action items** → one `sb_new_action(text, owner=<me or [[02-people/X]]>, due=<only if stated>,
   source_tag="meeting")` each (unknown owner → "owner: unassigned ⚠️"), **strategic themes** (2–4),
   **key quotes**, **tensions**, **unresolved**, and for 1-1 / stakeholder meetings a short **dynamics** read.
5. `sb_create_note(type="meeting", slug=<topic, not "tuesday meeting">, fields={date, participants:[wikilinks],
   project, "meeting-type": 1-1|team-sync|stakeholder|external|townhall, duration, source:<link or "pasted transcript">,
   "transcript-source": <from step 2>, confidence: high (medium if summary-fallback), "needs-review": <true if summary-fallback>,
   tags:[project, topic tags]}, preamble=<English: record of a <type> on <date> with <people>, covered <topic>,
   N decisions, N actions; if summary-fallback add: "Source: summary tab (transcript unavailable) — information loss expected.">,
   sections={"Context", "Participants", "Decisions", "Action items" (the sb_new_action lines), "Strategic themes",
   "Key quotes", "Tensions / Disagreements", "Unresolved", "Dynamics", "Links" (Source, People, Projects, Related wiki)})`.
6. Propagate — the step that keeps the system alive:
   - each linked person: `sb_append_timeline(path, "Meeting: <slug>", ["Source: [[04-meetings/<slug>]]", "What: <one sentence for this person>"])`
   - the project (if any): `sb_append_timeline(project_path, "Meeting: <slug>", ["Source: [[04-meetings/<slug>]]", "What: <main outcome>"])`
   - hard-to-reverse / one-way decisions: **ask** whether to log a `05-decisions/` note (then `sb_create_note type=decision`)
   - concepts in `missing_links` → `/knowledge-stub` for each
   - `sb_daily_append("Meetings ingested today", "- [[04-meetings/<slug>]] — <type> with <people>")`
7. `sb_commit("meeting-ingest: <slug>")`.
8. Report: path, transcript source (and the fallback warning if any), people linked / unmatched, decisions,
   unassigned actions ⚠️, one open tension if detected.
