---
name: doc-ingest
description: Ingest a produced document — strategy doc, analysis, report, deck, spec, research or external article — into a source note in 06-knowledge/_sources/, linked to its projects and domain hub. Use when the user shares a document or a link and says "ingest this", "process this report", "analyze this doc". Do NOT use for meeting transcripts (meeting-ingest).
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, ingestion, knowledge]
    related_skills: [meeting-ingest, knowledge-stub]
    requires_toolsets: [second_brain]
---

# Doc ingest (Hermes edition)

A source note is not a summary. It exists so that in six months someone can tell what this document
claimed, on what evidence, and whether it turned out to be right.

1. `sb_brief`.
2. Get the text: a Google Docs link → `sb_drive_doc(file_or_url)`; pasted text → use it as-is.
   If `transcript_source` comes back as anything but `full-document`, this is a meeting, not a
   document: stop and run `/meeting-ingest` instead.
3. Classify: **doc-type** (strategy | analysis | report | deck | spec | research | external-article),
   **domain** (from the profile's knowledge domains), **doc-date** — from the document itself, never
   inferred; `unknown` if it is not stated.
4. Extract, keeping the author's meaning and your own opinions out:
   - **Thesis** — the one claim the document exists to make.
   - **Key claims** — each with its evidence, and `confidence: stated | high | medium | speculation`.
   - **Data points** — figures verbatim, each dated `(as of YYYY-MM)`.
   - **Recommendations** — what it asks the reader to do.
   - **Open questions / gaps** — what it asserts without support. This section is where the value is.
5. Entities: `sb_find_person` for each person named (ask before creating), `sb_search` for projects
   and concepts. Every one becomes a wikilink.
6. Action items for the user → `sb_new_action(text, owner="me", due=<only if stated>, source_tag="doc")`.
7. `sb_create_note(type="doc", fields={domain, "doc-type", source=<URL or "pasted by the user">,
   "doc-date", "related-people", confidence}, preamble=<2-3 English sentences: what this document is,
   why it was ingested, when>, sections={...}, slug=<3-5 words>)`. `source` is verbatim: a URL, or a
   plain description. Never paraphrase a citation.
8. `sb_curate(path)` to list it under its domain hub.
9. Link it into the projects it concerns: `sb_append_section("03-projects/<project>.md", "Links",
   ["- [[<doc path>]] — <one line>"])`.
10. `sb_daily_append(section="Docs ingested today", line="- [[<path>]] — <thesis in a half-line>")`.
11. `sb_commit("doc-ingest: <slug>")`.
12. Report: path, thesis, number of claims, action items created, and the gaps you found — those are
    what the user should react to.
