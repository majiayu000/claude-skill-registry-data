---
name: daily-digest
description: Produce the day's digest for the second brain — synthesize calendar, Drive, Slack, Jira and vault activity into today's daily note (TL;DR, top topics, weak signals, people touched, pending follow-ups), log auto-observed interactions on known people, refresh TODO.md, and return the digest text for delivery. Use as the scheduled evening job or when the user says "daily digest", "what happened today", "recap of the day".
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, digest, daily, synthesis]
    related_skills: [meeting-ingest, people-update, task-roundup]
    requires_toolsets: [second_brain, second_brain_sources]
---

# Daily digest (Hermes edition)

The tools pre-digest every source into a few compact lines; your job is the **synthesis**:
what mattered, what is weak but worth watching, what to do next. Never dump lists.

1. `sb_brief` — working language, critical stakeholders, sensitive meetings, channels to ignore.
2. Collect (call what exists; a missing tool means the source is not configured — skip it, say so):
   `sb_calendar()`, `sb_drive_changes(since_hours=24)`, `sb_slack(since_hours=24, ignore_channels=<from brief>)`,
   `sb_jira(since_hours=24)`, `sb_vault_activity(since_hours=24)`.
3. Think, then write — in the working language, one signal per sentence, every claim tied to a source:
   - **TL;DR**: the 3 things that matter today.
   - **Top topics** (max 4): 2–3 sentences each across sources; cite `[[notes]]`, channels, tickets.
   - **Weak signals**: repeated mentions, tone shifts, first mentions of something new, tickets stuck.
   - **Meetings to ingest**: every Drive item flagged *meeting transcript* → list it with its link and
     offer `/meeting-ingest <link>`. Never ingest a meeting listed under *Sensitive meetings*.
4. Write into today's note with `sb_daily_append(section, line)`, one call per bullet:
   sections `TL;DR (3 lines)`, `Top topics of the day`, `Weak signals to dig into`, `Inputs of the day`.
5. People touched today — for each person seen in calendar/Slack/Jira: `sb_find_person(name)`;
   only for `exact`/`likely` matches, `sb_append_timeline(path, "Daily interactions", ["Calendar: …",
   "Slack: N msgs in #…", "Jira: …", "Source: daily-digest auto-propagation"], marker="(auto-logged)")` —
   raw facts only, no interpretation, max 20 people. Then `sb_daily_append("People touched today", "- [[02-people/Name]] — …")`.
   Unknown names → list them under "New people detected" in your reply; never create.
6. `sb_maintain(scope="tasks")` → then `sb_read("TODO.md", max_chars=2500)` and mirror the **Overdue** and
   **Today** lines into `sb_daily_append("Pending follow-ups", "- [ ] <text> — [[TODO]] → [[<src>#^t-id]] — due …")`.
7. `sb_commit("daily-digest: <date>")`.
8. Reply with the digest itself (this is what gets delivered): TL;DR, top topics, weak signals, overdue/today
   tasks, meetings to ingest, new people detected. Direct tone, no filler, no "great progress today".
