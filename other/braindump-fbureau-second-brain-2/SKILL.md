---
name: braindump
description: Capture an unstructured thought into the second-brain vault as an AI-first note in 00-inbox/, linking people, projects and concepts. Use when the user says "braindump", "note this", "capture this", "I have an idea", or shares a stream of thoughts. Do NOT use for meeting transcripts (meeting-ingest) or questions (recall).
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, capture, notes]
    related_skills: [people-update, knowledge-stub]
    requires_toolsets: [second_brain]
---

# Braindump (Hermes edition)

The tools enforce the vault contract; you supply the content and the judgment. Keep it light:
a braindump is a capture, not an essay.

1. `sb_brief` once per session — note the working language and the knowledge domains.
2. From the user's text decide: **domain** (personal | professional | project-specific | mixed),
   **energy** (low | medium | high), ≤ 4 topic tags, one-sentence **insight**, the open
   **tension** if any, one concrete **follow-up** if obvious (else none).
3. People mentioned → `sb_find_person(name)` for each. `exact`/`likely` → use the returned
   path as `[[02-people/Name]]`. `ambiguous` or `none` → **ask the user**; never create a person here.
4. Projects and concepts mentioned → `sb_search(query)`. Link existing notes as
   `[[03-projects/...]]` / `[[06-knowledge/...]]`. Unknown concepts still get a wikilink
   `[[06-knowledge/<slug>]]` — you will create the stub in step 7.
5. Follow-up → `sb_new_action(text, owner="me", due=<only if the user said one>, source_tag="braindump")`.
6. `sb_create_note(type="braindump", fields={domain, energy, tags, related-people, related-projects},
   preamble=<2-3 English sentences: what was captured, why, when>, sections={"Raw content": <the user's
   words cleaned for spelling only, NOT rewritten>, "Insight": ..., "Tension / Open question": ...,
   "Links": "- People: ...\n- Projects: ...\n- Concepts: ...", "Suggested follow-up": <the sb_new_action line>},
   slug=<3-5 words>)`. Sections are in the working language; the preamble is always English.
7. For each `missing_links` entry under `06-knowledge/` → run the **knowledge-stub** procedure
   (`/knowledge-stub`). Missing people links: ask, don't create.
8. `sb_daily_append(section="Braindumps of the day", line="- [[<path without .md>]] — <topic>")`.
9. `sb_commit("braindump: <slug>")`. If the hook rejects, read the error, fix, commit again.
10. Report in 3 lines: path created, links resolved / stubs created, suggested follow-up. Offer
    `people-update` if a significant interaction with a known person was described.
