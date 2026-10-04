---
name: people-update
description: Log an interaction or observation about a person into their 02-people/ note (append-only timeline, compiled truth updated sparingly), or create a new person note after confirmation. Use when the user says "people update", "note on <name>", "update <name>'s note", "add person", or describes a meaningful interaction with someone.
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, crm, people]
    related_skills: [braindump, knowledge-stub]
    requires_toolsets: [second_brain]
---

# People update (Hermes edition)

A person note is an interaction journal plus an evolving mental model. History is append-only;
the tools make that physically true — you decide what is worth recording.

1. `sb_brief` once per session (working language, critical stakeholders).
2. `sb_find_person(name)`.
   - `exact` / `likely` → `sb_read(path)` to load Compiled truth + recent timeline, then go to 3.
   - `ambiguous` → show the candidates, ask which one.
   - `none` → **ask before creating**: full name, role, team/company, region (WE | NA | LATAM | APAC | Global),
     relationship (direct-report | peer | manager | stakeholder | external). Then
     `sb_create_note(type="person", name="First Last", fields={role, team, company, region, relationship,
     tags:[<role-tag>, <region-tag>]}, preamble=<English: who, first interaction, context>,
     sections={"Compiled truth": <only what is known and stable>, "Open threads": ..., "Links": ...})`.
3. Log the interaction — one entry, factual, sourced:
   `sb_append_timeline(path, title=<"Weekly 1-1" | "Email exchange" | "Observation" ...>,
   lines=["Source: [[04-meetings/...]] or email/chat/observation", "What: <1-3 factual sentences>",
   "Observation: <interpretation, hypothesis, signal — clearly marked as such>",
   "[ ] Follow-up: <action> — owner: me"  ← checkbox only if it is a real action])`.
   Never write a value judgment about the person; describe behavior and context.
4. Compiled truth: change it **only** for a stable trait confirmed across several interactions.
   Then `sb_append_section(path, "Compiled truth", ["- **<Trait>**: <text> *(updated <date>, confirmed across N interactions)*"])`.
   Never rewrite existing bullets — add a dated one.
5. Ongoing topic → `sb_append_section(path, "Open threads", ["- <topic>"])` if not already listed.
6. `sb_daily_append(section="People touched today", line="- [[02-people/<Name>]] — <interaction type> — topic: <topic>")`.
7. `sb_commit("people-update: <Name>")`.
8. Report: note updated/created, timeline entry added, compiled-truth change (or "unchanged"), any
   pattern you noticed across recent entries (e.g. "second proactive raise this month").
