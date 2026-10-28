---
name: scraping-conference-rosters
description: Scrape a conference or trade show website for its published speakers, sponsors, exhibitors and partners — names, job titles, companies and logo walls. Use when someone names a specific event and wants the list of who will be in the room, or asks to scrape an event site, get the speaker list, or find the exhibitors at a conference.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Scraping Conference Rosters

## Goal
Turn a conference URL into a list of the people and companies who will be there — before you buy a ticket, and before anyone else in your niche thinks to look.

## When to use
- "Who's speaking at [conference]?"
- "Get me the exhibitor list for [event]"
- "I'm going to [conference] in March, who should I meet?"
- Straight after `discovering-live-events` has named an event worth attending

## Why this is the highest-value step in the whole repo

Every other script here finds *events*. This one tells you *who is in the room*.

A conference publishes its own roster — 100 names with titles and companies, sitting in public HTML. That is a better prospect list than anything you can buy, because every person on it has already paid to be somewhere you will also be. It is the difference between "cold outreach" and "I'll see you there."

## Process

### Step 1 — point it at the roster page
```bash
python -X utf8 -m scripts.scrape_conference_roster \
    --url https://example.com/2026/speakers \
    --event-name "Example Conference 2026" \
    --output data/example-speakers.csv
```

Free, and takes about a minute.

### Step 2 — get the sponsors and exhibitors too
```bash
python -X utf8 -m scripts.scrape_conference_roster \
    --url https://example.com/2026/partners https://example.com/exhibitors \
    --event-name "Example Conference 2026" \
    --output data/example-sponsors.csv
```

Sponsors and exhibitors are usually a **logo wall** — images, not text. The scraper reads company names out of the alt text and the outbound links. This is the specific reason it drives a real browser instead of fetching HTML.

### Step 3 — don't forget last year
```bash
python -X utf8 -m scripts.scrape_conference_roster \
    --url https://example.com/2025/speakers \
    --event-name "Example Conference 2025" \
    --output data/example-2025-speakers.csv
```

Past speakers and past exhibitors are an underrated list. They already valued the event enough to show up once, most will come back, and "I saw you spoke last year" is a warmer opener than anything about this year.

### Step 4 — let it find the pages itself
If you don't know the URLs:
```bash
python -X utf8 -m scripts.scrape_conference_roster \
    --site https://example.com --event-name "Example Conference 2026" \
    --output data/example-roster.csv
```
It reads the site's own navigation looking for speakers / sponsors / exhibitors / attendees pages.

### Step 5 — hand it to enrichment
See the `enriching-conference-companies` skill. Companies become named decision-makers with LinkedIn URLs.

## Reading the output

`CONTACT_FIELDS`, same as everything else in this repo, so it flows straight on.

| Column | Meaning |
|---|---|
| `person_name` | Blank on sponsor rows — those are companies, not people |
| `role_type` | `speaker`, `sponsor`, `exhibitor`, `attendee`, `organizer` |
| `confidence` | `confirmed` = name, title and org all present |
| `source` | The exact page it came from |

## Gated pages are a finding, not a failure

Some roster pages sit behind a form or a login. The scraper detects that and tells you which page and what the gate says, rather than writing an empty CSV that looks like a broken selector.

**When that happens, fill the form in yourself.** You are a genuine prospective attendee, the form is the intended way in, and the list behind it is usually the exhibitor list — the most valuable one. Do not try to automate around it.

Common gates: HubSpot "get instant access" forms, event apps (Grip, Swapcard, Whova) that need a ticket to log in.

## Edge cases

- **Fewer rows than the page claims.** Count the repeating card marker ("VIEW PROFILE", "Read Bio") on the page. That is the true number; marketing copy saying "175+ speakers" often counts last year too.
- **Names with credentials.** "Amber Childs, PhD" is handled — credentials are stripped before any job-title test. If a new suffix breaks it, add it to `_strip_credentials`.
- **A whole page of junk rows.** The site had no repeating card marker, so it fell back to a heuristic. Pass the specific roster URL rather than `--site`.
- **Sponsor logos giving domain names instead of brands.** The logo had no alt text, so it used the link target. Usually still correct, occasionally lowercase.
- **JS-heavy sites.** Already handled — it renders and scrolls. Raise `--scrolls` if the page lazy-loads a lot.

## Cost
Nothing. It is your own browser.
