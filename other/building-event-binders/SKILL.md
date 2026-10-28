---
name: building-event-binders
description: Turn conference roster CSVs into a client-facing HTML binder — a searchable, sortable, filterable prospect site with a hero photo of the host city, stat tiles and downloadable CSVs. Use when someone wants to hand a client a deliverable instead of a spreadsheet, or asks for a binder, a prospect site, or something presentable.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Building Event Binders

## Goal
Turn the CSVs into something you can send a client as a link.

## Why bother

A CSV is a file you attach. A binder is a link you send. It opens on a phone, it looks like you spent money on it, and — this is the part that matters — it gets **forwarded to the person who actually signs**.

Same data. Completely different reception. A spreadsheet says "here's some research." A binder says "here's what I do."

It is also the cheapest upsell in the business: the work is already done, and this is twenty minutes on top.

## Process

### Step 1 — get your CSVs
From `scraping-conference-rosters` and optionally `enriching-conference-companies`. Any CSV in `CONTACT_FIELDS` shape works.

### Step 2 — write a config
```json
{
  "title": "Example Conference 2026",
  "subtitle": "Conference Prospect Binder",
  "owner": "Client Name · Their Company",
  "event_dates": "September 22–24, 2026",
  "venue": "Some Convention Center",
  "city": "Nashville, TN",
  "hero_image": "assets/hero.jpg",
  "hero_credit": "Photo — Someone, CC BY 4.0",
  "intro": "One or two lines on what this is and why it matters.",
  "sections": [
    {
      "id": "speakers",
      "label": "2026 Speakers",
      "icon": "🎤",
      "csv": "data/example-speakers.csv",
      "blurb": "Everyone on stage, with title and company.",
      "columns": ["person_name", "title", "organization", "linkedin_url", "confidence"]
    }
  ]
}
```

### Step 3 — the hero image
A photo of the host city is what makes it feel bespoke rather than generated. **Use a free, properly licensed one** — Wikimedia Commons has good skylines for most cities:

```bash
python -X utf8 -c "
import json,urllib.request,urllib.parse
q='Nashville Tennessee skyline'
u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({
 'action':'query','format':'json','generator':'search',
 'gsrsearch':f'filetype:bitmap {q}','gsrlimit':6,'gsrnamespace':6,
 'prop':'imageinfo','iiprop':'url|extmetadata','iiurlwidth':2000})
r=urllib.request.Request(u,headers={'User-Agent':'binder/1.0 (research)'})
for _,p in json.load(urllib.request.urlopen(r))['query']['pages'].items():
    ii=p['imageinfo'][0]
    print(ii['extmetadata'].get('LicenseShortName',{}).get('value'), ii['thumburl'])
"
```

Download the **exact** `thumburl` the API returns — Wikimedia rejects arbitrary sizes with a 400. Then resize to ~2000px and credit the photographer in `hero_credit`. It is their work and the licence requires it.

Never pay to generate an image for this. A real photo of the real city is better anyway.

### Step 4 — build
```bash
python -X utf8 -m scripts.build_event_binder \
    --config data/example-binder.json \
    --outdir dist/example
```

Output is plain HTML with the data inlined — no build step, no server, no dependencies.

### Step 5 — ship it
Open `dist/example/index.html` locally, or deploy for a link you can send:

```bash
npx --yes wrangler@latest pages deploy dist/example     --project-name my-binder --branch main --commit-dirty=true
```

**To put it behind a key**, add a `_worker.js` at the root of the deploy folder
and set a `DASHBOARD_KEY` environment variable on the Pages project. Access is
then granted by `?k=<key>` in the URL (and a cookie for return visits).

> Use `_worker.js`, **not** a `functions/_middleware.js`. Wrangler 4 silently
> stops compiling the Pages `functions/` directory — it uploads your files, says
> "Deployment complete", and serves the site with no gate at all. The only
> visible difference is that a working deploy prints **"Compiled Worker
> successfully"**. If you do not see that line, your site is public.

Leave the key in the URL rather than stripping it, so one link works on every
device the client opens it on.

## What you get

- **index.html** — hero with the city photo, stat tiles, one card per list
- **one page per CSV** — live search, sortable columns, filter chips for "has LinkedIn" / "has email" / "confirmed only", and a CSV download button
- Confidence rendered as coloured pills so nobody treats a `weak` row as verified

## Choosing columns

Fewer is better. `person_name`, `title`, `organization`, `linkedin_url`, `confidence` covers most cases. For a sponsor list drop `person_name` (there are no people) and show `organization`, `website`, `role_type`.

Leave `columns` out entirely and it picks the non-empty ones for you.

## Edge cases

- **Section skipped** — the CSV path was wrong or the file was empty. It says which.
- **A stat tile reads 0** — that layer has not been run. Either run it or drop that section; a zero on the front page undersells the work.
- **Hero looks washed out** — the veil sits at 34% opacity over the photo. Darker photos read better; night skylines work well.
- **Wikimedia 400** — you changed the thumbnail width. Use the URL the API gave you verbatim.
- **Sticky header overlapping rows** — already handled; the header offset is measured from the real search-bar height at load and on resize, rather than hardcoded.

## Cost
Nothing. It is a static file.
