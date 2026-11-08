---
name: seed-scout
description: >-
  Competitor Scout. Finds the weak points of your competitors in their own
  App Store reviews: searches the App Store for the apps people already use
  for your idea, reads up to the 500 most recent reviews of each, sorts the
  one- and two-star ones into themes (fees and pricing, cancellations and
  no-shows, support, bugs, trust and safety, payments and refunds,
  availability), and names each rival's weak point with the evidence ("106
  of 341 recent 1-2 star reviews mention fees"). Writes seed/reviews/ and
  seed/competitors.json for the plan, the deck and the pitch coach. Use when
  the user says "who are my competitors", "find my competitors' weak
  points", "what do people hate about Rover", "read their reviews", "scout
  the competition", "competitor research", "why do customers leave X", or at
  the start of a raise, before /seed-market.
argument-hint: "[\"your idea in a few words\" | APP_ID ...]"
---

# seed-scout

The Competitor Scout finds the gap you can win in. People who already pay a
rival tell the App Store exactly what is wrong with it, in public, every day.
This skill reads those reviews in bulk, counts what the angry ones complain
about, and turns that into one plain sentence per rival that a business plan
and a pitch deck can stand on. It reports what reviewers wrote and how often.
It never makes a complaint up, and it never calls a rival bad in general.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/scout.py" find "dog walking"                   # the apps people find for the idea
python3 "${CLAUDE_SKILL_DIR}/scout.py" reviews 547320928 --write            # 500 most recent -> seed/reviews/
python3 "${CLAUDE_SKILL_DIR}/scout.py" reviews "Wag" --write                # a name works: it says which app it picked
python3 "${CLAUDE_SKILL_DIR}/scout.py" themes 547320928                     # what the 1-2 star reviews say
python3 "${CLAUDE_SKILL_DIR}/scout.py" compare 547320928 940734609 --write  # weak points -> seed/competitors.json
python3 "${CLAUDE_SKILL_DIR}/scout.py" pricing 547320928 --note "keeps 20% of each booking" --source URL --write
python3 "${CLAUDE_SKILL_DIR}/scout.py" show
```

Other flags: `--pages 1..10` (50 reviews a page), `--stars 1` (one-star
only), `--by count` (the most mentioned theme instead of the gap), `--rules
FILE` (your own themes), `--country gb`, `--dir`, `--json`, `--today`,
`--offline DIR` (saved responses, for testing).

## What it reads and writes

| file / feed | what |
| --- | --- |
| iTunes Search API | `find`, and turning a name into an app id. Free, no key, not an official API |
| iTunes Lookup API | each app's rating, rating count and full name |
| customer-reviews RSS | `.../rss/customerreviews/page=N/id=APP_ID/sortby=mostrecent/json`: 50 a page, 10 pages, so the 500 most recent reviews in one country |
| `seed/reviews/<app_id>.json` | with `--write`: the reviews read (date, stars, title, text, version; no reviewer names) |
| `seed/competitors.json` | `compare --write`: one row per app with `themes`, `top_theme`, `weak_point`, `weak_point_line`, `examples`, the rating and the source. `/seed-plan`, `/seed-deck` and `/seed-coach` read it |

## How the themes and the weak point work

- **Low reviews** are the one- and two-star ones (`--stars` changes it). M in
  "N of M" is how many of those were read, N how many mention the theme.
- **Keyword rules**, on the title and the text, case-insensitive. A review can
  hit several themes. The rules are listed at the top of `scout.py`; `--rules
  FILE` adds themes for another industry (`{"key": {"label", "patterns"}}`).
- **The weak point** of each app, when you compare two or more: the theme that
  sets it apart, its share of low reviews minus the pooled share of the other
  apps. Support complaints show up for every app, so they rarely win; a
  complaint one rival gets far more than the others does. A theme needs at
  least 5% of the app's low reviews to count. With one app, or `--by count`,
  it is the most mentioned theme. The output says when the two differ.
- **Rounding.** The rating rounds half up to one decimal (4.88527 is 4.9).
  Shares are one decimal. Counts are exact.
- **Polite.** One request at a time, a one-second pause between pages, a
  20-second timeout, a User-Agent that names this project.

## Steps

1. Ask for the idea in a few words, the way a customer would search for it.
   Run `scout.py find "<words>"` and pick the two to four real rivals (the
   most ratings, the same job). Confirm the list with the user.
2. Run `scout.py reviews APP_ID --write` for each one.
3. Run `scout.py compare APP_ID APP_ID ... --write`. Read every rival's
   weak point, its evidence line and its examples.
4. **Read the examples before you quote a theme.** Keyword rules miss
   sarcasm and catch the odd false hit. If a theme looks wrong, open
   `seed/reviews/<id>.json`, read the matching reviews and say what you saw.
5. **Read each rival's pricing page by hand.** Search for "<rival> fees" or
   "<rival> pricing", open the rival's own help or pricing page, and write
   down what it actually charges with `scout.py pricing APP_ID --note "..."
   --source URL --write`. A fee you cannot link to stays out of the plan.
6. Tell the user, per rival: the rating and rating count, the weak point,
   "N of M recent 1-2 star reviews mention it", and the pricing note with
   its link. Then say the gap in one line: what the new product does about
   it.
7. Hand off to `/seed-market` to size the market, then `/seed-model` and
   `/seed-plan`, which pull `seed/competitors.json` into the Competition
   section. `/seed-coach` turns it into the questions investors will ask.

## Example: the reel

Leashly (a made-up startup: "a dog-walking app with flat prices and a backup
walker on every walk"). On October 25, 2026 the scout read the 500 most
recent US reviews of Rover and of Wag!. `scout.py compare 547320928
940734609 --write`:

```
Competitors: their most recent App Store reviews, 1-2 star only
  app            rating    ratings  low/read   weak point                  evidence
  Rover             4.9    515,771   341/500   fees and pricing            106 of 341 (31.1%)
  Wag!              4.8     67,447   324/500   cancellations and no-shows  81 of 324 (25.0%)
Weak point = the complaint that sets each app apart: its share of low reviews minus the others'.
  Wag!: the most mentioned is customer support (95 of 324), but the other apps get it about as often.
```

Rover's fee share is 31.1% against Wag!'s 24.7%, a 6.4 point gap.
Wag!'s cancellation share is 25.0% against Rover's 12.3%, a 12.7 point gap.
The pricing note comes from Rover's own help center: Rover keeps 20% of
each sitter booking and adds a service fee for owners at checkout. That is
Leashly's story: flat $25 walks with no surprise fees, and a backup walker
on every walk.

## Rules

- Quote counts as "N of M recent 1-2 star reviews mention X", with the
  date read. Never "everyone hates X".
- Reviews are what reviewers wrote, not facts about the company. Pricing
  claims come from the rival's own page, with its URL.
- Never copy a stranger's review into a deck or an email. Titles in the
  plan are fine as evidence; the full texts stay in `seed/reviews/`.
- Never log in to the App Store or anywhere else. These feeds are public.

## What it never does

It never invents a review, a rating or a fee, never posts a review, never
contacts a competitor or a reviewer, and never says a rival is failing. A
weak point is where customers complain most, compared with the others.
