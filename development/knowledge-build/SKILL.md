---
name: knowledge-build
description: Builds and maintains 06-knowledge/ as a structured graph — wiki pages (encyclopedic, grown from first mention), lessons (distilled patterns), source documents (in _sources/), and domain index hubs that route navigation. Includes a curator that updates hubs incrementally on every capture and runs a weekly sweep (orphans, duplicates, clusters needing hubs). Use when the user says "build/update knowledge", "wiki on X", "fais une fiche sur X", "what have we learned about X", "consolidate learnings", "curate the knowledge base", "knowledge garden", "bootstrap knowledge".
---

# Skill: Knowledge Build

This skill makes `06-knowledge/` earn its place. It turns the folder into a real **second
brain** at two altitudes plus an organizing layer:

- **Wiki** (`type: wiki`) — encyclopedic pages on concepts, entities, jargon, tools, teams,
  processes. Created as **stubs on first mention**, grown incrementally. Your personal
  Wikipedia.
- **Lessons** (`type: knowledge`) — distilled syntheses of recurring patterns, frameworks,
  principles, anti-patterns. Gated by recurrence (3+ sources) and decision reversals.
- **Domain hubs** (`type: index`) — Map of Content per knowledge domain. Each hub at
  `06-knowledge/<domain>.md` lists every wiki, lesson, and source doc tagged with the
  matching `domain:` field. The root `06-knowledge/_INDEX.md` lists the hubs.

Source documents (`type: doc`) live in `06-knowledge/_sources/` (not at the root), so they
don't drown the durable knowledge.

All four flavors must cite their sources (rule 3.4) and use `domain:` to route to a hub.
`recall` and `challenge-decision` query through hubs first.

## When to activate

**Wiki mode**
- **Auto (on first mention)** — invoked by `braindump`, `meeting-ingest`, `doc-ingest`
  whenever they extract a wikilink to `06-knowledge/<concept>.md` that doesn't yet exist
  (Wiki stub protocol below).
- **Manual** — "fais une fiche sur X", "wiki on X", "write a knowledge note about Y".
- **On enrichment** — a new source mentions an entity already in the wiki → append new facts
  with inline citations, never silently overwrite.

**Lessons mode**
- **Manual** — "consolidate learnings", "what have we learned about X", "synthesize lessons".
- **Auto (weekly)** — a phase of `daily-brief` weekly mode: conservative sweep, flag for review.
- **Offered** after a significant `doc-ingest` or a `reversed` decision.

**Curator mode** (the organizing layer)
- **Auto incremental** — every time a wiki / lesson is created or enriched, or a doc is
  ingested, the matching hub is updated and `_INDEX.md` counters refresh. Silent for
  listing changes inside `auto-maintained: true` hubs.
- **Auto sweep (weekly)** — a phase of `daily-brief` weekly mode after the lessons pass.
  Rebuilds hub listings from scratch, detects orphans, proposes new hubs / merges, flags
  stubs awaiting enrichment.
- **Manual** — "curate", "knowledge garden", "tidy 06-knowledge", "rebuild indexes".
- **Bootstrap** (one-shot) — "bootstrap knowledge" or `knowledge-build curator --bootstrap`
  on first install / after a major version upgrade. Migrates an existing 06-knowledge/ into
  the structured layout (see Bootstrap below).

**Do NOT use when:**
- The user wants an answer, not a synthesis → use `recall`.
- The user wants to ingest a document → use `doc-ingest` (which then triggers this skill
  for stubs / lessons / hub updates).

## Preflight

1. **Read `_CLAUDE.md`** (schemas for `type: wiki`, `type: knowledge`, `type: doc`, `type: index`)
   and `00-inbox/MY-PROFILE.md` (`## Knowledge domains`, working language).
2. **Get the real timestamp.**
3. **Route the invocation:**
   - Triggered by another skill with a target slug → **Wiki stub protocol** (one stub).
   - User named one topic → **Topic mode** (wiki page or lesson, by intent).
   - "Curate / knowledge garden / rebuild indexes" → **Curator sweep**.
   - "Bootstrap knowledge" → **Curator bootstrap**.
   - Sweep mode (auto/weekly, no topic) → **Lessons sweep** then **Curator sweep**.
4. **Wiki vs lessons routing for a named topic:**
   - "Wiki / fiche / encyclopedic / what is X / who is team Y" → Wiki page.
   - "Lesson / pattern / what we learned / what works for X / anti-pattern" → Lesson.
   - Ambiguous → wiki page first (lower bar); offer a lesson on top if evidence supports.

## Mode A — Wiki (encyclopedic pages)

### A.1 Path & naming
`06-knowledge/<slug>.md` (evergreen, kebab-case, **undated**). Same folder as lessons and
hubs — distinguished by `type: wiki` in frontmatter.

The slug is the canonical name of the thing: `pricing-tiers.md`, `agentforce.md`,
`onboarding-team.md`, `chargebee.md`, `weekly-business-review.md`, `mqp.md`.

### A.2 Wiki stub protocol (called by other skills)

When `braindump`, `meeting-ingest`, or `doc-ingest` detect a new concept/entity wikilink
`[[06-knowledge/<slug>]]` that doesn't exist yet:

1. Create the file with the stub template (A.3), populated with:
   - Frontmatter `type: wiki`, `needs-review: true`, `confidence: speculation`,
     `created-from: "[[<trigger-note-path>]]"`, `domain: <inferred>` (see A.3).
   - One line in `## Summary` if the trigger gave a definition; else the explicit stub:
     `*Stub — first mentioned in [[…]] on YYYY-MM-DD. Awaiting more sources.*`
   - The trigger note in `## Sources` with date + a ≤ 1-line verbatim snippet.
2. Backlink from the trigger note's `## Links → Related wiki`.
3. **Call the curator incremental update**: add the new wiki page's listing to the matching
   `06-knowledge/<domain>.md` hub (silent if `auto-maintained: true`). If the domain has no
   hub yet, add the page to `_INDEX.md` `## Unsorted` instead.
4. Don't block the user — the stub is created silently in propagation; user reviews
   `needs-review: true` stubs via daily-brief or `vault-tend knowledge garden`.

### A.3 Wiki page template

```markdown
---
date: YYYY-MM-DD              # stub creation
updated: YYYY-MM-DD
type: wiki
tags: [wiki, <topic-tags>]
domain: <domain-slug>         # routes to 06-knowledge/<domain>.md hub
aliases: ["<other names>", "<acronym>"]
confidence: stated | high | medium | speculation
needs-review: true | false
created-from: "[[<trigger-note-path>]]"
ai-first: true
---

## For future Claude

Wiki page on [topic]. [One sentence stating what it is, in plain words.] Built incrementally
from the sources listed at the bottom — every fact in this note traces to one of them.

## Summary

[1–3 sentences. The thing in plain language: what it is, why it matters here.]

## What we know

- <Fact 1> — [[<source>]] (as of 2026-04)
- <Fact 2> — [[<source>]] (confidence: medium)
- <Fact 3 from external source> — https://… (as of 2026-03)

## Open questions / unknowns

- [What the vault doesn't yet say about this thing.]

## Related

- Domain hub: [[06-knowledge/<domain>]]
- People: [[02-people/...]]
- Projects: [[03-projects/...]]
- Related wiki: [[06-knowledge/...]]
- Lessons: [[06-knowledge/...]]

## Sources

> Cumulative provenance. Every time this page is touched, add the source here with the date.
> Never remove an entry — this is the audit trail.

- [[<trigger-note-path>]] — YYYY-MM-DD (stub created, "<verbatim 1-line snippet>")
- [[<source-2>]] — YYYY-MM-DD (added: <what was added>)
- <external URL> — YYYY-MM-DD (added: <what was added>)
```

**Domain inference for a new stub:**
1. If the trigger note has a `domain:`, use it.
2. Else: scan the trigger context (project, tags, surrounding wikilinks) and match against
   `## Knowledge domains` in `MY-PROFILE.md`.
3. Else: use `domain: unsorted` (the curator surfaces it in `_INDEX.md`).

### A.4 Enrichment (subsequent encounters)

- **Append, don't overwrite**. New facts → `## What we know` with citation. Contradictions
  → add with date and a `*supersedes the 2026-03 statement — see [[…]]*` note; never delete.
- **Always add an entry to `## Sources`** with date + one-line "what was added".
- Update `updated:`; bump `confidence:` only when warranted; clear `needs-review:` if appropriate.
- **Call curator incremental** to refresh the hub's "Recent activity" line.

### A.5 Wiki anti-patterns
❌ Writing a fact without a citation — every line traces.
❌ Silently overwriting — append with dates.
❌ Inventing facts — say `unknown` in `## Open questions`.
❌ Thick first version — start as stub, grow with evidence.
❌ Forgetting `domain:` — leave `unsorted` rather than skip.

## Mode B — Lessons (distilled patterns)

### B.1 Detect lesson candidates
A candidate is **recurring or load-bearing**, not a one-off:
- A topic across **3+** meetings/daily notes/docs.
- A repeated **anti-pattern** or friction in weekly reviews.
- A **principle revealed by a decision** — especially a `reversed` one.
- A **framework or concept** introduced by an ingested doc.
- A **stable fact about how things work** consolidated across many wiki pages.

Weight evidence: human/manual full weight; `needs-review: true` ~70%; `(Backfilled)` ~30%.

### B.2 Match against existing lessons
- **Exists** → update (B.4): add evidence, date the change.
- **Doesn't exist** → draft new (B.3).
- **Overlaps two** → propose a merge.

### B.3 Write a lesson
**Path**: `06-knowledge/<concept-slug>.md` (evergreen, kebab-case, undated).

```markdown
---
date: YYYY-MM-DD
updated: YYYY-MM-DD
type: knowledge
tags: [knowledge, <topic-tags>]
domain: <domain-slug>
confidence: high | medium | speculation
needs-review: false
ai-first: true
---

## For future Claude

Durable lesson on [topic]: [one-line statement]. Distilled from N vault sources.

## What we know

[The framework / lesson / principle / stable fact, stated plainly.]

## Evidence

- [[05-decisions/2025-09-03-...]] (reversed) — <lesson> (as of 2025-09)
- [[04-meetings/2026-02-...]] — <supporting observation> (as of 2026-02)
- [[06-knowledge/<wiki-page>]] — <wiki fact this lesson rests on>

## Anti-patterns / caveats

- [What not to do, or where this stops being reliable.]

## Links

- Domain hub: [[06-knowledge/<domain>]]
- Projects: [[03-projects/...]]
- Related wiki: [[06-knowledge/...]]
- Related lessons: [[06-knowledge/...]]
```

### B.4 Update an existing lesson
Same template, append-only on `## Evidence` and `## What we know`. If a wiki page the lesson
rests on now contradicts, mark `needs-review: true` and add `## Open questions`.

### B.5 Auto mode (weekly) specifics
- **Conservative**: at most a few lessons per run; prefer updating evidence to inventing.
- Mark auto-created/updated `needs-review: true`; list in the weekly review.
- Never touch human-curated notes (no `needs-review`, recently `updated`) beyond appending evidence.

## Mode C — Curator (the organizing layer)

The curator is what makes `06-knowledge/` navigable instead of a junk drawer. It owns
`type: index` notes (domain hubs + root `_INDEX.md`) and routes every wiki/lesson/doc into
its hub via `domain:`.

### C.1 Incremental update (called on every capture)

Trigger: a wiki / lesson is created or enriched, or a doc is ingested.

1. Read the captured note's `domain:`.
2. If `06-knowledge/<domain>.md` exists with `auto-maintained: true`:
   - Add the note to the right listing section (Wiki pages / Lessons / Source documents),
     sorted alphabetically. Skip if already listed.
   - Prepend a line to `## Recent activity`: `- YYYY-MM-DD: <action> [[<note>]]`.
   - Update `updated:` on the hub.
3. If `06-knowledge/<domain>.md` does NOT exist:
   - Add the note to `06-knowledge/_INDEX.md` `## Unsorted by domain` section with the
     domain slug noted.
   - If 3+ notes now share this unhubbed domain, **propose a new hub** in the next sweep
     (preview-first); don't auto-create silently.
4. If `domain: unsorted` (no domain inferred):
   - Add to `_INDEX.md` `## Unsorted (no domain)` for human review.
5. Refresh root `_INDEX.md` counts and `## Recent activity`.

**Silent vs preview**: listing refreshes inside an `auto-maintained: true` hub are silent.
Creating a hub, moving a note between hubs, merging notes — always preview and ask.

### C.2 Sweep (weekly via daily-brief, or `knowledge-build curator`)

Full pass over `06-knowledge/`:

1. **Inventory.** Group every note by `domain:`. Identify: domains with ≥ 3 notes (need a hub),
   domains with < 3 notes (stay unsorted), notes without `domain:` (flag).
2. **Hub maintenance.** For each existing `auto-maintained: true` hub:
   - Rebuild the listing sections from scratch (catches renames, deletes, splits).
   - Refresh `## Summary` from the constituent notes' summaries (≤ 5 sentences, cited).
   - Append a `## Recent activity` line summarizing the sweep.
3. **Propose new hubs.** For each unhubbed domain with ≥ 3 notes: preview the hub content
   and ask before creating.
4. **Orphans.** A note is orphan if it has no inbound wikilinks from any hub or other note
   (besides its `created-from`). Flag in `_INDEX.md` `## Health → Orphans`.
5. **Near-duplicates.** Slug similarity > 70% OR title/aliases overlap → propose a merge
   (preview the combined note; never auto-merge).
6. **Stubs awaiting enrichment.** `type: wiki` with `needs-review: true` older than 14
   days → flag in `## Health → Stubs to enrich`.
7. **Stale wiki pages.** `updated:` more than 90 days ago AND no inbound activity → flag.
8. **Refresh `_INDEX.md`** end-to-end (hubs list with counts, recent activity, health stats,
   unsorted lists).
9. **Self-verification loop** (since v4.0) — the sweep must reach a stable state before exit:
   1. Snapshot the state of each `auto-maintained: true` hub + `_INDEX.md` after step 8.
   2. Re-run steps 2 and 8 once (a "verification pass").
   3. **Compare**: if the verification pass produces *zero* changes to any hub or
      `_INDEX.md`, the sweep is stable → exit and report.
   4. If the verification pass *did* produce changes, the previous pass was incomplete. Run
      another full pass (steps 2–8) on the hubs that changed, then re-verify.
   5. **Budget**: max 3 passes total (1 initial + up to 2 re-iterations). If still not
      stable, stop and flag the unstable hubs in the report under `## Health → Curator
      unstable` with the diff between the last two passes — that's a bug signal, not a
      reason to keep looping.
10. **Report** what was rebuilt, proposed, flagged — and how many passes it took to stabilize.


### C.3 Bootstrap (one-shot)

Triggered by "bootstrap knowledge" or `knowledge-build curator --bootstrap`. Used on first
install or after upgrading from a version that didn't have the curator.

Run interactively, in batches, with confirmations:

1. **Create `06-knowledge/_sources/`** if missing.
2. **Move existing `type: doc` notes** (anything currently at the root of `06-knowledge/`
   with `type: doc` in frontmatter) into `_sources/`. Update all inbound wikilinks. **Preview
   the list, confirm before moving.**
3. **Read `## Knowledge domains`** from `MY-PROFILE.md`. If empty, **propose a starting
   taxonomy** inferred from the notes' existing tags (cluster the top 5–8 tag groups). User
   confirms / edits.
4. **Tag domains.** For each wiki/lesson/doc without `domain:`:
   - Infer from tags / linked projects / slug. Show top 3 candidates per note in batches of
     20. User confirms / corrects.
   - Ambiguous → `domain: unsorted`.
5. **Create domain hubs.** For each domain in `MY-PROFILE.md` (and proposed ones from step 3),
   write `06-knowledge/<domain>.md` with `auto-maintained: true` and the constituent notes
   listed.
6. **Move vault-meta artifacts**: any note in `06-knowledge/` whose slug matches
   `kickstart-backfill-*`, `vault-health-*`, or any one-shot operational marker → propose
   moving to `07-archive/`. Confirm.
7. **Replace `06-knowledge/README.md`** with `06-knowledge/_INDEX.md` (write the new file,
   archive the old README content if non-trivial).
8. **Final report**: hubs created, notes moved, notes archived, domains established, orphans
   detected.

Bootstrap is **idempotent**: running it again on an already-bootstrapped vault is a no-op
beyond `_INDEX.md` refresh.

## Domain hub template (`type: index`)

```markdown
---
date: YYYY-MM-DD
updated: YYYY-MM-DD
type: index
tags: [index, <domain>]
domain: <domain-slug>
auto-maintained: true
ai-first: true
---

## For future Claude

Map of Content for the **<Domain>** domain. Auto-maintained by knowledge-build (curator).
Lists every wiki, lesson, and source doc tagged `domain: <domain-slug>`. Entry point for
any `<domain>`-related query — start here before drilling into individual notes.

## Summary

[1–3 sentences synthesizing the state of this domain, refreshed by curator sweep. Cite the
2–3 most load-bearing notes.]

## Wiki pages

- [[06-knowledge/<wiki-slug>]] — <one-line description from the wiki's ## Summary>

## Lessons

- [[06-knowledge/<lesson-slug>]] — <one-line takeaway from the lesson's ## What we know>

## Source documents

- [[06-knowledge/_sources/YYYY-MM-DD-<slug>]] — <doc-type, 1-line topic>

## Recent activity

- 2026-05-28: enriched [[06-knowledge/<wiki>]] (+1 source)
- 2026-05-27: stub created [[06-knowledge/<wiki>]]

## Open questions

[Surface the `## Open questions` from constituent wiki pages, deduplicated.]
```

## Root `_INDEX.md` template

```markdown
---
date: YYYY-MM-DD
updated: YYYY-MM-DD
type: index
tags: [index, root]
auto-maintained: true
ai-first: true
---

## For future Claude

Root index of `06-knowledge/`. Auto-maintained by knowledge-build curator. Use this as the
entry point: navigate to a domain hub, then to individual notes. `recall` queries this first
to scope the search.

## Domain hubs

- [[06-knowledge/<domain-1>]] (N wikis · N lessons · N source docs · updated YYYY-MM-DD)
- [[06-knowledge/<domain-2>]] (...)

## Sources (most recent 10)

- [[06-knowledge/_sources/YYYY-MM-DD-<slug>]] — <domain>, <doc-type>

## Unsorted by domain

[Notes whose `domain:` slug has no hub yet (< 3 notes). The curator proposes a hub when a
cluster grows.]

- [[06-knowledge/<slug>]] — `domain: <slug>`

## Unsorted (no domain)

[Notes without a `domain:` field — to be tagged by the user.]

- [[06-knowledge/<slug>]]

## Health

- N wiki pages · N lessons · N source docs · N hubs.
- N orphans (no inbound links).
- N stubs awaiting enrichment (>14 days `needs-review: true`).
- N stale wiki pages (>90 days no update, no activity).
- N near-duplicates flagged for review.

[When a category is non-empty, list the offending notes in a matching subsection right
below: `### Orphans`, `### Stubs to enrich`, `### Stale wikis`, `### Near-duplicates`,
`### Curator unstable` (sweep step 9). Omit empty subsections.]
```

## Connect (across all modes)
- Backlink each new wiki/lesson from the projects, decisions, and people it informs.
- Cross-link related notes: wiki pages link to lessons that draw on them; lessons link back
  to wiki pages they reference; both link to their domain hub.

## Report

```
WIKI / LESSONS
✓ New wiki stub: 06-knowledge/qualification-script.md (domain: cs-ops, from [[04-meetings/...]])
✓ Enriched: 06-knowledge/onboarding-team.md (+1 source, confidence high)
✓ New lesson: 06-knowledge/change-rollout-lessons.md (needs-review: true)

CURATOR (incremental)
✓ Hub updated: 06-knowledge/cs-ops.md (+1 wiki listed)
✓ _INDEX.md refreshed (counts: 12 wikis · 3 lessons · 11 docs · 5 hubs)

CURATOR (sweep, if applicable)
✓ Hub rebuilt: 06-knowledge/salesforce.md (6 wikis, 1 lesson, 4 docs)
✓ Proposed new hub: 06-knowledge/vendor-stack.md (4 notes cluster: boost, zowie, amazon-connect, chargebee) — confirm?
✓ 2 orphans flagged in _INDEX.md (no inbound links)
✓ 1 near-duplicate flagged: 06-knowledge/qualif-script vs 06-knowledge/qualification-script — merge?
→ 1 lesson candidate ("tooling-before-training") with only 2 sources — left for next time
```

## General anti-patterns
❌ **Fabricating** — only crystallize what the vault supports; cite or don't claim.
❌ **Overwriting human-curated notes** — append dated evidence.
❌ **Uncited assertions** — every line traces.
❌ **Auto-finalizing interpretation** — auto-created notes flag `needs-review: true`.
❌ **Auto-creating hubs silently** — sweep proposes, never creates without confirmation.
❌ **Hand-editing listing sections of an auto-maintained hub** — the curator rewrites them.
   Edit the hub's intro/summary, or set `auto-maintained: false` and own it.
❌ **Writing a `type: doc` at the root of `06-knowledge/`** — they go in `_sources/`.

## Special cases

### Reversed decisions
Richest lesson source. When a `05-decisions/` note is `status: reversed`, mine the lesson
and the conditions that triggered the reversal.

### Topic mode
"What have we learned about X" → produce/refresh one focused note on X. Routes to wiki or
lesson per A vs B routing.

### Manually-owned hub
Set `auto-maintained: false` in a hub's frontmatter to take ownership. The curator stops
rewriting its listings but still updates `## Recent activity` and counts.

### Working language
Bodies in the vault's working language (`MY-PROFILE.md`); preamble always English.
