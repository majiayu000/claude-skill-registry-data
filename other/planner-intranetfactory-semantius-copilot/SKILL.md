---
name: planner
description: Plan leisure trips on the planet Hoth. Use this skill whenever the user asks about visiting, skiing, spa bathing, or booking activities on Hoth, or mentions Hoth resorts, operators, or regions. It knows the sites in each region and how to fetch live opening times from the Hoth Tourism API.
---

# Hoth trip planner

You are planning a leisure trip on the planet Hoth. Everything you need is in
this skill — do NOT invent sites, operators, or opening times from memory.

## Step 1 — find candidate sites

Hoth has two tourist regions. Read the reference file for the region the user
is interested in (read both if unsure):

- `references/echo-basin.md` — the Echo Basin region
- `references/north-ridge.md` — the North Ridge region

Each reference lists the sites in that region with their operator and what
they offer. Pick the sites that match what the user wants to do.

## Step 2 — fetch opening times

Opening times MUST come from the Hoth Tourism API via the bundled script —
never guess them. Run it with the exact site names from the reference file
(comma-separated), plus the date range, using exactly this command shape:

```
node .agents/skills/planner/scripts/opening-times.js --sites="Echo Base Thermal Springs,Wampa Ridge Spa" --from=2026-08-01 --to=2026-08-03 2>&1
```

Always keep the `2>&1` at the end so errors are visible. The script prints a
JSON array with one entry per site: `site_name`, `site_id`, and
`opening_times` (one `{date, open, close}` per day in the range).

## Step 3 — answer

Present a short plan: which sites to visit, run by which operator, with their
opening times per day. Mention the region the sites are in.
