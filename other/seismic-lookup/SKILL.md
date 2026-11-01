---
name: seismic-lookup
description: "Records the seismic design parameters a project needs before structural design starts, one at a time, with the source of each: mapped accelerations, site coefficients, design accelerations, the design category, and the long-period transition. Trigger on \"seismic design category\", \"what is the SDC for this site\", \"seismic parameters\", \"site class\", \"design spectral accelerations\", \"seismic-lookup\", or a pasted site location with a seismic question. Works in any jurisdiction. The parameters come from the user's own hazard tool, code maps, or geotechnical report, and the site class comes from the geotechnical engineer. The skill never supplies a seismic value from memory or from web search, and reports every parameter it could not source as a gap. Writes a CSV and a summary."
license: MIT
metadata:
  title: "Seismic Lookup"
  summary: "Record a site's seismic design parameters and where each came from"
  discipline: "code-life-safety"
  tags: "Compliance, Pre-Design"
---

# Seismic Lookup

Seismic design starts from a short list of parameters and a record of where each
one came from. Which parameters you need is knowable. What they are for your
site is not, so they come from you.

## Scope and limits — read first

**What this does.** Works through the parameters, asks for each, records its
source, writes a CSV plus a summary, and prints a gap list. It says what each
parameter feeds, so a parameter that turns out to be unnecessary gets dropped
rather than guessed.

**What this does not do.**

- **It does not look up seismic values.** No maps, no coefficient tables, no
  risk category listing, no site class definitions. Every value comes from you.
  That is the design, not a gap.
- **It does not determine the site class.** That is the geotechnical engineer's
  determination from measured or inferred subsurface data. Ask for it and record
  who provided it.
- It does not compute base shear, a response spectrum, or detailing
  requirements. It records the inputs those need.
- It does not geocode an address.
- It does not do site-specific ground motion analysis, which some site classes
  and some sites require. Where your code calls for one, this records that it
  is required and stops.
- It does not replace the Engineer of Record or the authority.

**What you need before starting.** The governing loading standard and edition,
the site location, the risk or importance category with what set it, the site
class with who determined it, and access to whatever your jurisdiction publishes
the mapped values in.

## Workflow

### Step 1. Bootstrap if needed

```bash
python scripts/init_workspace.py
```

### Step 2. Establish the standard and the inputs

Ask, in one message:

> 1. Which loading standard governs, and which edition? Seismic maps and site
>    coefficients are redrawn between editions, so the cycle matters here more
>    than almost anywhere.
> 2. Site location, as precisely as the authority requires.
> 3. Risk or importance category, and what set it. Name the occupancy and the
>    clause you read it from.
> 4. Site class, and who determined it. If no geotechnical determination exists,
>    say so; do not assume a default.
> 5. Where will the mapped values come from: an official hazard tool, the code's
>    own maps, or a report you have? Name it; it prints as the source on every
>    line it supplies.

### Step 3. Collect one value per parameter

For each parameter, say what it feeds before asking, then accept a typed value
with its source, a pasted tool output or table to read it out of, or a file to
read.

| Parameter | Feeds |
|-----------|-------|
| Mapped short-period acceleration | Site-modified accelerations |
| Mapped one-second acceleration | Site-modified accelerations |
| Site coefficients, short and one-second | Site-modified accelerations |
| Site-modified accelerations | Design accelerations |
| Design accelerations, short and one-second | Base shear and the design category |
| Seismic design category | Detailing, system limits, height limits |
| Long-period transition period | Long-period base shear |
| Peak ground acceleration, geometric mean | Liquefaction and geotechnical checks |

If none arrives for a parameter, it goes on the gap list. Do not offer a value,
do not search for one, and do not derive a mapped value by interpolating between
two nearby sites.

**For a United States site**, `scripts/fetch_sdc.py` calls the USGS Seismic
Design Maps web service and writes the response with the endpoint recorded as
the source. It is one way to answer Step 3, not a required step, and it does not
apply outside its coverage. It exits rather than falling back to an estimate
when the service is unreachable, which is the behaviour to preserve if anyone
adds an equivalent for another jurisdiction.

```bash
python scripts/fetch_sdc.py --lat <lat> --lon <lon> \
  --risk-category <as supplied> --site-class <as supplied> \
  --project <slug> --out <cache>.json --out-csv <file>.csv
```

### Step 4. Write the record

Head the CSV and the summary with the standard, the edition, the location, the
risk category, the site class and who determined it, and the source of the
mapped values. Foot both with the gap count.

Use `assets/seismic-csv-template.csv` for the columns.

Where the site class or the site conditions call for a site-specific ground
motion analysis under your code, record that as a required next step rather than
producing parameters as if it were not needed.

### Step 5. Update the index

```bash
python scripts/append_to_index.py \
  --project <slug> --lat <lat> --lon <lon> \
  --risk-category <as supplied> --site-class <as supplied> \
  --sdc <as supplied> --sds <as supplied> --sd1 <as supplied> \
  --csv <file>.csv --summary <file>.md
```

Do not edit `docs/seismic/index.md` by hand; the table alignment breaks.

### Step 6. Report

The parameters recorded, the gap list with what each needs, and:

> Every parameter here came from the source named beside it. I supplied none.
> The site class is the geotechnical engineer's determination, not mine.

## Rules

- **Never supply a seismic value.** Not from memory, not from a search, not from
  a figure in this file. There are none in this file.
- **Never assume a site class.** An assumed one is the single most consequential
  guess available here, because it moves every downstream number at once.
- **Record the edition and the source on every line.** Maps get redrawn; a value
  carried forward without its edition is the failure mode.
- **Never interpolate** between contours, between nearby sites, or between
  editions.
- **Never derive a parameter you were not given** just because the arithmetic is
  simple. If a coefficient is missing, the derived value is a gap, not a number.
- Where the code requires a site-specific analysis, say so and stop rather than
  producing parameters anyway.

## Anti-patterns

- Naming a design category for a city because the answer feels familiar.
- Defaulting the site class when no geotechnical report exists. There is no safe
  default; there is only a recorded assumption someone must own.
- Searching the web for a site's mapped accelerations.
- Producing parameters for a site the code says needs a site-specific study.
- Reporting only the parameters that could be sourced, with no gap count.
- Bundling a risk category table or a site class table into this skill later. It
  had both, transcribed from one jurisdiction's code, and they were removed.

## Resources

- `scripts/init_workspace.py` — bootstrap `docs/seismic/`.
- `scripts/fetch_sdc.py` — United States sites only; calls the USGS Seismic
  Design Maps service and records the endpoint as the source.
- `scripts/append_to_index.py` — append a row to the index.
- `assets/seismic-csv-template.csv`, `assets/seismic-index-template.md`.

No reference files. The parameters come from your standard and your
geotechnical engineer.
