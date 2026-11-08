---
name: seed-deck
description: >-
  Pitch Deck Designer. Turns the business plan into a 10-slide pitch deck in
  the order investors expect: title, problem, solution, market, competition,
  business model, go-to-market, team, financials, the ask. Writes ONE
  self-contained 16:9 HTML file (inline CSS, no fonts or scripts from the
  web, arrow-key navigation, a print stylesheet that saves to PDF one slide
  a page) in your brand colours, with real charts drawn from your numbers.
  Lints it: 35 words or fewer a slide, one idea a slide, a use of funds that
  adds up to the raise, and every number on a slide traced to your plan,
  model, market or competitor files. Reads seed/plan.json, writes
  seed/deck.html. Use when the user says "make my pitch deck", "turn the
  plan into a deck", "build the slides", "check my deck", "how many words a
  slide", or after /seed-plan.
argument-hint: "[build | outline | lint] [--brand #RRGGBB]"
---

# seed-deck

The Pitch Deck Designer turns the plan into the ten slides a partner flips
through in three minutes. Each slide carries one idea in a line or two, and
the numbers come from the files, not from memory: the competitors' weak
points from their own reviews, the market from sourced inputs, the unit
economics and the three years of revenue from the model, the use of funds
from the raise. The deck is a single HTML file you can open anywhere, present
with the arrow keys and print to PDF. A good deck earns a meeting; it does
not guarantee a check. Investors decide.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/deck.py" outline               # what each slide will say, with its word count
python3 "${CLAUDE_SKILL_DIR}/deck.py" build                 # seed/deck.html, then the lint
python3 "${CLAUDE_SKILL_DIR}/deck.py" build --brand "#2F6FEB" --ink "#0E1B33" --accent "#FFB020"
python3 "${CLAUDE_SKILL_DIR}/deck.py" lint                  # exit 0 clean, 1 something to fix
```

Other flags: `--dir PATH` (default `./seed`), `--plan PATH`, `build --out
PATH`, `--json` on outline and lint.

## What it reads and writes

| file | what |
| --- | --- |
| `seed/plan.json` | from `/seed-plan` (after `plan.py build`): each section's `pitch` and `points`, the `tagline`, `team`, `brand` colours and the `numbers` block |
| `seed/model.json`, `seed/market.json`, `seed/competitors.json`, `seed/config.json` | read by the lint only: every number on a slide must be in one of them or in plan.json, and plan.json must not be older than model.json |
| `seed/deck.html` | `build` writes it: one file, 10 slides, 16:9 (1280 x 720), inline CSS and a few lines of plain JavaScript |

## The ten slides

| # | slide | what is on it |
| --- | --- | --- |
| 1 | Title | the name, the tagline, the raise and the instrument, the founder |
| 2 | The problem | the problem line and the competitors' review evidence ("106 of 341") |
| 3 | The solution | the solution line and up to 3 points |
| 4 | The market | the market line and TAM, SAM, SOM (the circles are not to scale), with sources |
| 5 | Competition | one card per competitor (rating, ratings, weak point) and yours |
| 6 | Business model | price, what you keep, contribution, LTV:CAC, CAC payback |
| 7 | Go to market | the line and up to 3 numbered steps |
| 8 | Team | the people in plan.json, with initials |
| 9 | Financials | revenue for years 1 to 3 as bars, breakeven month, peak burn |
| 10 | The ask | the ask line, the instrument, the use of funds as bars with shares |

Presenting: open the file in a browser. Right arrow, space or Page Down
moves on; left arrow or Page Up goes back; Home and End jump; a click on the
right or left half moves too; `#4` in the address opens slide 4; P prints.
Without JavaScript the slides simply stack. Print > Save as PDF gives one
16:9 slide a page (13.333 x 7.5 in), backgrounds included.

## The lint

- **35 words or fewer** in a slide's body. The title, the footnote and the
  page number do not count.
- **One idea a slide**: a lead of at most 2 sentences and at most 3 points.
- **The ask adds up**: the use of funds equals the raise.
- **Every number traces**: each number shown (rounded is fine: $8.5B for
  8,520,000,000, $2.23 for 2.225) is in plan.json's numbers, model.json,
  market.json, competitors.json or config.json. Years and counts of 10 or
  less are not checked.
- **Nothing missing**: no empty slide, no market, competition, business
  model, financials or ask slide without its data, no team, no stale plan.

## Steps

1. Make sure `/seed-plan` has run `plan.py build` with every check passing.
   The deck refuses a plan.json without numbers.
2. Run `deck.py outline` and read the ten slides back to the founder. Tight
   lines win: if a slide runs long, shorten the section's `pitch` or
   `points` in seed/plan.json and run `plan.py build` again.
3. Ask for the brand colours (or keep the ones in plan.json), then run
   `deck.py build`.
4. Fix everything the lint lists. Numbers are fixed at their source (the
   model, the market file), never by editing the HTML.
5. Open seed/deck.html with the founder. Offer the PDF: Print > Save as PDF.
6. Hand off: `/seed-coach` drills the questions this deck invites,
   `/seed-dataroom` files it under 02 Pitch deck, and `/seed-closer` links it
   in the outreach.

## Example: the reel

Leashly (fictional), from the reel's plan. `deck.py outline` gives:

```
 1. Leashly          12 words  Dog walks without the surprise fees. | Raising a $1.5M seed · post-money SAFE
 2. The problem      29 words  Owners pay fees on top of fees. Walkers cancel last minute. | 106 of 341 | ...
 4. The market       28 words  $158B US pet spend (2025). 71M US homes have a dog. | TAM | $8.5B | ...
 5. Competition      33 words  Rover: fees. Wag!: cancellations. | Rover | 4.9★ · 515,771 ratings | ...
 6. Business model   23 words  15% take rate. No owner fee. | $25 | a walk | $3.75 | we keep (15%) | ...
 9. Financials       27 words  Breakeven in month 29 on the seed alone. | Revenue | Year 1 | $467K | ...
10. The ask          28 words  $1.5M seed to launch in 3 cities. | Post-money SAFE | Product and engineering | ...
```

The problem slide shows Rover's 106 of 341 and Wag!'s 81 of 324; the market
slide TAM $8.5B, SAM $228M, SOM $22.8M; the business model $25 a walk, $3.75
kept, $2.23 contribution, 4.24x LTV:CAC, 3.37 months payback; the financials
$467K, $1.59M and $2.99M of revenue with breakeven in month 29 (May 2029) and
an $82.8K peak monthly burn; the ask $600K (40%) product and engineering,
$450K (30%) city launches, $300K (20%) marketing, $150K (10%) operations and
insurance. The lint is clean: the longest slide has 33 words.

## Rules

- No slide promises funding, returns or a valuation. The financials slide
  says the projections are the founder's own assumptions, not a forecast.
  Not investment advice.
- Every number on a slide comes from a file. Change numbers at their source.
- Real people on the team slide, with their real roles.
- The deck file loads nothing from the internet: it works offline and in
  any inbox preview.
