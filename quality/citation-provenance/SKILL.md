---
description: >
  Literature retrieval and provenance protocol for the problem-investigator.
  Defines the citation-graph rounds, elite-pool filtering, the degradation
  ladder for restricted networks, and bibliography.jsonl discipline.
user-invocable: false
---

# Citation provenance

**Prime rule: a paper you did not retrieve and read does not exist.** Every
citation key in this pipeline traces to a `bibliography.jsonl` entry with
provenance and a `literature/<key>.md` note. No exceptions.

## Retrieval ladder (degrade gracefully)

1. **WebSearch** — scholarly queries ("<topic> site:arxiv.org", venue names,
   author names from seeds). Provenance: `websearch`.
2. **WebFetch** — fetch abstract/HTML pages for candidates found in (1).
   Provenance: `webfetch`. If a fetch fails (403/timeout), keep the search
   snippet as `read_status: abstract-only` ONLY if the snippet contained the
   actual abstract; otherwise drop the paper.
3. **Seeds** — files in `workspace/seeds/`. Provenance: `seed`.
4. **User-provided notes** — material the user pasted or described.
   Provenance: `user-provided`.

In `--offline` mode, skip 1–2 entirely.

## Investigation rounds

- **Round 1 — graph expansion**: from the task topic + seeds, gather candidate
  papers (titles, venues, years, why-relevant). Record the growing graph in
  `investigation/citation-graph.json`: `{nodes: [{key?, title, year, source}],
  edges: [[from, to, "cites|extends|compares"]]}`.
- **Round 2 — elite pool**: score candidates on relevance to the task
  (core / adjacent / background) and quality signals; keep 10–50 in
  `investigation/elite-pool.json`. **Relevance gate**: fewer than 5
  core+adjacent sources ⇒ append `{"event":"stage_investigate","detail":"ABORTED: relevance gate"}`
  to the ledger, reply `ok: false`, and stop — do not force a weak brief.
- **Round 3 — deep read**: for each elite paper, write `literature/<key>.md`
  (provenance frontmatter, factual summary, findings relevant to the task)
  and append its entry to `bibliography.jsonl`. Run
  `python3 .claude/scripts/bib_validate.py <run>` and fix any errors.
- Write `investigation/round{1,2,3}.md` documenting decisions per round.

## The brief

`brief.md` sections: Problem · State of the Art · Gap · Constraints (from
task.md) · Candidate Directions · Related Work. Every prior-work statement
carries `[EV:cite:<key>]`. The brief is the Ideator's ONLY literature input —
make the Gap and Candidate Directions concrete enough to generate from.
