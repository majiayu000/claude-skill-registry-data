---
name: zoning-summary
description: "This skill should be used when the user provides a site address, parcel info, or zoning lookup text and needs a structured zoning summary for early design. Trigger on 'zoning summary', 'zoning lookup', 'site zoning for [address]', or pasted zoning portal output. Targets North American projects (US + Canada). Generates a worksheet markdown in `docs/zoning/` and updates the project zoning index."
license: MIT
metadata:
  title: "Zoning Summary"
  summary: "Turn a parcel lookup into a zoning summary for early design"
  discipline: "code-life-safety"
  tags: "Compliance"
---


# Zoning Summary


## Overview


Produce a one-page, designer-actionable zoning worksheet for a site at the early massing stage. The skill loads the North American zoning reference and outputs a fill-in worksheet to `docs/zoning/<site-slug>.md` that names every constraint a designer must look up before sketching mass. If the user pastes raw zoning portal text, the skill extracts and structures it; otherwise it leaves prompts the designer can complete from their own GIS / municipal lookup.


## Scope and limits — read first


**What this does.** Builds a one-page worksheet for a named site and use, naming
every constraint that shapes early massing and, next to each one, what it does
to the design. Values you paste from a portal carry over verbatim; values not
looked up yet stay as `<lookup needed>` with a pointer to where they live.

**What this does not do.**

- **It does not know your district's numbers.** FAR, height, setbacks, coverage,
  and parking ratios are municipal and they change. Not one of them is supplied
  from memory. An empty field is the correct output here; a wrong one is not.
- **It does not look the site up.** It reads what you paste from the city's
  portal, GIS, or by-law text, and prompts for the rest. It also does not
  confirm which district the parcel sits in, which comes from the zoning map.
- It does not run the building code. Egress, fire resistance, and accessibility
  are `code-compliance-review`; this stops at the zoning envelope.
- It does not test a variance, special permit, or bonus. It records what the
  by-law requires as written.
- It does not cover New York City properly. `nyc-zoning-lookup` reads the Zoning
  Resolution itself and cites section and page; this worksheet is the generic
  North American one.

**What you need before starting.** The site by address or parcel, the
jurisdiction, and the intended use, since many constraints are use-dependent.
Then whatever the municipal portal or by-law gives you, pasted rather than
paraphrased.

## When to use


Trigger on:

- A site address or parcel description paired with intended use (program).
- Pasted output from a zoning portal (US municipal zoning lookup, Canadian zoning by-law text, GIS HTML/text).
- Explicit asks: 'zoning summary', 'site zoning for <address>', 'zoning for <parcel>'.
- Early massing / feasibility phase questions tied to a real site.

Do NOT trigger for:

- Detailed code analysis after DD — that is `code-compliance-review` territory.
- Building-code (IBC, NBC) line-item checks unrelated to zoning envelope.
- Pure precedent or program studies with no site — use `precedent-finder`.

## Workflow


### Step 1 — Bootstrap if needed


Check `docs/zoning/index.md` exists. If not:


```bash
python scripts/init_zoning_workspace.py
```


### Step 2 — Identify jurisdiction


Capture the city / county / state-or-province for the site (e.g. "Portland, OR", "Toronto, ON"). Zoning is municipal everywhere in North America, so the city + ordinance/by-law citation is what matters. If no locator is given, ask once.


### Step 3 — Load the reference

- Read `references/na_zoning.md` for the canonical zoning concepts and lookup checklist.
- Always also read `references/design_implications.md` — it bridges constraint to design move.

### Step 4 — Gather inputs


From the user's message (and `docs/project.md` if present), extract:

- **Site identifier** — address, parcel/lot number, or short site name.
- **Intended use** — program (residential / cultural / commercial / mixed-use / etc.).
- **Lot info if known** — area, frontage, road width, slope.
- **Pasted lookup text** — if any, capture verbatim for Step 5 extraction.

If the user pasted zoning portal text, parse out values for as many template fields as possible. Otherwise leave the prompts blank with `<lookup needed>` markers.


### Step 5 — Fill the template


Read `assets/zoning-template.md`. Fill placeholders. Where a value cannot be derived, write `<lookup needed: ...>` with a hint about _where_ to look (e.g. `<lookup needed: city zoning map + ordinance §X>`, `<lookup needed: Toronto zoning by-law 569-2013>`). For each filled or prompted constraint, add a one-line **design implication** drawn from `references/design_implications.md`.


### Step 6 — Write the file


Use the Write tool. Filename:


`docs/zoning/<site-slug>.md`


Slug rule: lowercase, `[^a-z0-9-]` removed, max 40 chars, derived from the site identifier (`123-main-st-portland`, `45-front-st-toronto`). If duplicate, suffix `-<n>`.


### Step 7 — Update the zoning index


```bash
python scripts/append_to_index.py \
  --date 2026-05-06 \
  --site-slug 123-main-st-portland \
  --jurisdiction "Portland, OR" \
  --zone "R-5" \
  --use "multi-family residential"
```


Do NOT edit `index.md` manually with the Edit tool — table alignment breaks easily.


### Step 8 — Report


Tell the user:

- Path to the worksheet file.
- Top 2-3 constraints that will most shape massing (e.g. FAR, setbacks, height, parking, daylight plane) with one-line design implication each.
- The list of `<lookup needed>` items the designer must resolve before next step.

## Rules

- Never write fictional ordinance / by-law numbers, FAR caps, or specific setback values per district. They vary by city — leave them as `<lookup needed>` with a pointer.
- The worksheet is a thinking tool. Empty fields are fine; wrong fields are not.
- Always include a **design implication** line per constraint, not just the number.
- If the user pasted lookup text, quote source values verbatim — do not paraphrase numbers.
- If intended use is missing, ask once before producing the worksheet — many constraints are use-dependent.
- Cite the city + district code together (e.g. "Portland R-5", "Toronto CR 2.5"). District labels are not portable between cities.

## Anti-patterns

- Filling specific zone limits from memory instead of marking them `<lookup needed>`. Zoning ordinances change and vary by city.
- Producing a generic checklist with no site context. The worksheet must name the actual site and use.
- Using a district label without the city ("R-5" alone is meaningless).
- Editing `index.md` manually instead of using `append_to_index.py`.
- Including detailed code analysis (egress, fire ratings, accessibility). That is post-zoning code work.

## Resources

- `scripts/init_zoning_workspace.py` — bootstrap `docs/zoning/` and the zoning index
- `scripts/append_to_index.py` — append a row to `docs/zoning/index.md`
- `references/na_zoning.md` — North American zoning fundamentals (use groups, FAR/coverage/setback, overlays, IBC/NBC cross-ref)
- `references/design_implications.md` — constraint-to-design-move mapping
- `assets/zoning-template.md` — zoning worksheet template
