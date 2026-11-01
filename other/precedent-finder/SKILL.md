---
name: precedent-finder
description: "This skill should be used when the user describes a project concept, program, atmosphere, or site condition and needs architectural precedents. Trigger on 'find references', 'similar projects', 'precedents for', or natural-language descriptions paired with phrases like 'something with this feeling'. Caches a curated precedent list in `docs/precedents/` (one file per topic) and updates the project precedent index."
license: MIT
metadata:
  title: "Precedent Finder"
  summary: "Find architectural precedents for a concept or condition"
  discipline: "design-building-types"
  tags: "Pre-Design"
---


# Precedent Finder


## Overview


Recommend 5-8 architectural precedents based on a designer's natural-language brief, with each entry annotated for the _strategy_ (not feature) the designer should learn from. Cache the result so future searches on the same topic short-circuit and the team builds a project-specific precedent library.


## Scope and limits — read first


**What this does.** Reads a brief in the words you would use to describe it and
returns five to eight built precedents, each with the design strategy worth
taking from it and the part of your brief it answers. The list is cached in
`docs/precedents/` so the next search on the same topic starts from it.

**What this does not do.**

- **It does not invent a project.** Name, architect, year, and location each
  have to be verifiable to a primary source or the entry is left out.
  `references/canon.md` is the pool it draws from first, and every entry there
  was checked against a published record.
- It does not search the web. What it knows about a project can be out of date,
  which is why every entry carries a source link for you to open before citing
  it.
- It does not analyse a precedent in depth. It names the strategy; the drawings
  and the monograph are still yours to read.
- It does not tell you how to design. It returns examples, not method.
- It does not offer unbuilt competition entries or your own past work unless you
  ask for them.

**What you need before starting.** The program, the atmosphere or site condition
you are after, and a scale if you have one. A brief as thin as "modern museum"
gets one clarifying question before the list is built.

## When to use


Trigger on:

- Concept/atmosphere descriptions ("a museum embedded into a hillside, warm concrete not cold").
- Program + site briefs ("30,000 sf riverside cultural center, mass timber").
- Explicit asks: "precedents for", "references", "similar projects", "comparable buildings".

Do NOT trigger for general design guidance ("how should I approach this site"). This skill returns _examples_, not method.


## Workflow


### Step 1 — Bootstrap if needed


Check `docs/precedents/index.md` exists. If not:


```bash
python scripts/init_precedents_workspace.py
```


### Step 2 — Parse the brief


Decompose into searchable axes:

- **Program** (museum / housing / cultural / mixed-use / etc.)
- **Scale** (rough area, units, budget tier)
- **Site condition** (urban / coastal / mountain / hillside / industrial)
- **Atmosphere keywords** (warm, brutal, ceremonial, domestic)
- **Material / form keywords** (concrete, mass timber, cantilever, courtyard)

Optionally read `docs/project.md` for additional project context.


### Step 3 — Check the precedent canon


Before generating from memory, load `references/canon.md` for a curated list of well-documented precedents organized by program and atmosphere. Use it as the default pool to draw from — augment with additional projects only when none in the canon match.


### Step 4 — Recommend 5-8 precedents


Deliberately span:

- Different eras (don't recommend only contemporary)
- Different geographies (avoid clustering all from one region)
- Different scales (include at least one smaller and one larger than user's project)
- At least one canonical pick AND at least one unexpected pick

Per precedent:

- Architect (firm) / completion year / location / approximate area
- Three core design **strategies** (not features)
- **The match**: which axis of the brief this addresses
- Source link (ArchDaily, Dezeen, architect's official site, monograph)

### Step 5 — Write the precedent file


Read `assets/precedent-template.md`. Fill placeholders. Filename:


`docs/precedents/<topic-slug>.md`


Slug rule: lowercase, `[^a-z0-9-]` removed, max 40 chars, derived from the brief's dominant keywords (`hillside-museum-concrete`, `riverside-cultural-mass-timber`). If duplicate, suffix `-<n>`.


### Step 6 — Update the precedent index


```bash
python scripts/append_to_index.py \
  --date 2026-05-06 \
  --slug hillside-museum-concrete \
  --program museum \
  --keywords "hillside,concrete,warm" \
  --count 6
```


### Step 7 — Report


Tell the user:

- Path to the precedent file
- The 1-2 strongest matches with one-line reason
- Optionally: "Want me to expand on any of these or pull more in a different direction?"

## Rules

- A "strategy" is a design move, not a feature. "Embedded the mass into the hillside so the roof becomes the site" is a strategy. "Has a green roof" is a feature.
- Cite the strongest single match per project — do not list every possible reason.
- If the brief is too vague ("modern museum"), ask one clarifying question (atmosphere or site) before producing the list.
- Default to North American and international canon. Include local references where the brief specifies a region.
- Do not recommend the user's own work or unbuilt competition entries unless asked.

## Anti-patterns

- Padding the list with weak matches to hit a number. 5 strong is better than 10 mixed.
- Summarizing Wikipedia. Provide design-strategy reasoning a designer can use immediately.
- Inventing projects. If unsure of existence, year, or architect, omit the entry.
- Skipping the canon and going straight to memory — the canon is there to anchor.

## Resources

- `scripts/init_precedents_workspace.py` — bootstrap `docs/precedents/` and the index
- `scripts/append_to_index.py` — append a row to `docs/precedents/index.md`
- `references/canon.md` — curated list of well-documented precedents by program/region/era
- `assets/precedent-template.md` — precedent file template
