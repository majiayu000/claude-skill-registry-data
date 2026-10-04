---
name: knowledge-stub
description: Create or enrich a wiki page in 06-knowledge/ for a concept, tool, team, process or piece of jargon, with cited sources, then route it into its domain hub. Use when the user says "wiki on X", "fais une fiche sur X", "what do we know about X (write it down)", or when another skill reports a missing 06-knowledge/ wikilink.
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, knowledge, wiki]
    related_skills: [braindump, people-update]
    requires_toolsets: [second_brain]
---

# Knowledge stub (Hermes edition)

Wiki pages grow from the first mention: start as a stub, enrich with cited facts, never overwrite.
Every fact traces to a source; the `## Sources` section is the audit trail.

1. `sb_brief` once per session — read the **knowledge domains** list.
2. `sb_search(concept, folder="06-knowledge")`. If a page exists (same thing under another name counts):
   - `sb_append_section(path, "What we know", ["- <fact> — [[<source note>]] (as of YYYY-MM)"])`
   - `sb_append_section(path, "Sources", ["- [[<source note>]] — <date> (added: <what>)"])`
   - `sb_curate(path, action="enriched")` → done, go to 5.
3. Otherwise create the stub. Domain: pick from the brief's knowledge domains; if none fits use `unsorted`.
   `sb_create_note(type="wiki", slug="<canonical-name>",
   fields={domain, aliases:[<other names, acronym>], confidence:"speculation", "needs-review": true,
   "created-from": "[[<trigger note>]]", tags:[<topic tags>]},
   preamble=<English: "Wiki page on X. <one plain sentence saying what it is>. Built incrementally from the sources below.">,
   sections={"Summary": "*Stub — first mentioned in [[<trigger note>]] on <date>. Awaiting more sources.*"
   OR a 1-3 sentence definition if the trigger gave one,
   "Sources": "- [[<trigger note>]] — <date> (stub created, \"<verbatim 1-line snippet>\")"})`.
   If the trigger text states a fact, add it under "What we know" with the citation. Do not invent facts.
4. `sb_curate(path, action="stub created")` — lists the page in its hub or in `_INDEX.md` Unsorted.
5. If you were called from another skill, stop here (that skill commits). Otherwise
   `sb_commit("wiki: <slug>")`.
6. Report: page path, domain, hub it landed in, and whether it is a stub awaiting enrichment.
