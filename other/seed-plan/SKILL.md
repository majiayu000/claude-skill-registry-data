---
name: seed-plan
description: >-
  Business Planner. Turns your idea into a business plan investors can read:
  the nine sections (executive summary, problem, solution, market,
  competition, business model, go-to-market, financial plan, use of funds),
  written with you, with the numbers pulled from the other seed skills'
  files: TAM, SAM and SOM from seed/market.json, competitors' weak points
  from seed/competitors.json, revenue, breakeven and runway from
  seed/model.json. Computes the unit economics (take rate, contribution per
  order, CAC payback, LTV:CAC) and flags empty sections and numbers that
  disagree between files. Writes seed/config.json, seed/plan.json and
  seed/plan.md. Use when the user says "turn my idea into a business plan",
  "write my business plan", "I have a startup idea", "help me plan my
  startup", "check my plan", "unit economics", or before /seed-deck.
argument-hint: "[init --name NAME --one-liner TEXT | build | check]"
---

# seed-plan

The Business Planner turns an idea into the document behind a raise. It sets
up the startup's shared config (name, one-liner, the raise, the founder), lays
out the nine sections every investor expects, and, once Claude and the
founder have written them, stitches in the numbers the other skills found:
the market size, the competitors' weak points, the model's revenue, breakeven
and runway. It works out the unit economics itself and checks the whole thing
for holes: an empty section, a raise that is $1.5M in one file and $1.2M in
another, a use of funds that does not add up, a market share bigger than the
market. A plan is a way to think clearly, not a promise of funding: the pack
does the work, investors decide.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/plan.py" init --name "Leashly" --one-liner "A dog-walking app with flat prices and a backup walker on every walk" \
  --raise 1.5M --instrument "post-money SAFE" --founder "Your Name" --email you@leashly.example \
  --tagline "Dog walks without the surprise fees."
python3 "${CLAUDE_SKILL_DIR}/plan.py" build                 # seed/plan.md + the numbers in seed/plan.json
python3 "${CLAUDE_SKILL_DIR}/plan.py" check                 # the checks only: exit 0 clean, 1 something to fix
```

Other flags: `--dir PATH` (default `./seed`), `init --brand/--ink/--accent
#RRGGBB` (the deck's colours), `init --address`, `--sector`, `--geography`,
`--stage`, `init --force` (start again), `build --today YYYY-MM-DD`, `--json`.

## What it reads and writes

| file | what |
| --- | --- |
| `config.example.json` (this folder) | the shape of `seed/config.json`, filled in for Leashly |
| `seed/config.json` | `init` writes it: the startup (name, one-liner, sector, stage, geography, raise, instrument), the founder (name, email, company address), `sec_user_agent` and the outreach limits (daily cap 20, follow-ups after 3 and 7 business days, 3 touches). Every seed skill reads it |
| `seed/plan.json` | `init` writes the skeleton; Claude writes each section's `text`, `pitch` (one line for the slide) and `points` (up to 3), plus `tagline`, `team` and `brand`. `build` adds `numbers`, `flags`, `notes` and the build date |
| `seed/market.json` | from `/seed-market`: TAM, SAM, SOM and their sourced inputs |
| `seed/competitors.json` | from `/seed-scout`: each app's rating, ratings, low reviews and weak point |
| `seed/model.json` | from `/seed-model`: the assumptions, the 36 months and the summary |
| `seed/plan.md` | `build` writes it: the plan with a key-numbers table, the checks and the nine sections with their tables |

## The unit economics

Computed from the model's assumptions, exactly, and shown in the plan:

| number | how |
| --- | --- |
| revenue per order | price x take rate |
| contribution per order | revenue per order minus the costs of one order (card fees, per-order costs) |
| CAC payback | CAC / (contribution per order x orders per customer a month), in months |
| LTV | contribution per customer a month / monthly churn |
| LTV:CAC | LTV / CAC (most seed investors look for 3x or more) |

## The checks

- **Flags (fix before anyone reads it):** an empty section; a missing
  market.json, model.json or competitors.json; a raise that disagrees
  between config.json and model.json; a use of funds that does not add up
  to the raise; a SOM above the SAM or a SAM above the TAM; year 3 GMV above
  the SOM (the model sells more than the market you said you could win); a
  model.json that no longer matches its own assumptions; a contribution at
  or below $0.
- **Notes (worth a look):** a number in a section's text that is in none of
  the files (years and counts of 10 or less are skipped); LTV:CAC under 3x;
  CAC payback over 12 months; cash that runs out inside 36 months; no
  breakeven; no tagline, no team, an empty pitch line.

## Steps

1. Run `plan.py init` with the startup's name, one-liner, the raise and the
   founder's own name and work email. The email is the one outreach goes
   from: never use anyone else's.
2. Run `/seed-scout`, `/seed-market` and `/seed-model` if their files are
   missing. The plan's numbers come from them, not from memory.
3. Write the nine sections into `seed/plan.json` with the founder, one at a
   time. Plain words, short paragraphs. Every number you write should exist
   in one of the files; if the founder gives a new number, add it to the
   right file first (the market inputs, the assumptions).
4. Give each section a `pitch`: one line, a slide's worth (the deck's lint
   allows 35 words a slide). Give the solution and go-to-market up to 3
   `points`. Add the `team` (real people only) and a `tagline`.
5. Run `plan.py build`. Read back the key numbers and every flag and note.
6. Fix the flags (in the file the flag names), then build again until it
   says every check passed. Never change a number to silence a check
   without the founder's yes.
7. Hand off to `/seed-deck` to turn the plan into the 10-slide deck.

## Example: the reel

Leashly (fictional): "A dog-walking app with flat prices and a backup walker
on every walk", raising a $1.5M seed on a post-money SAFE to launch in 3
cities. `plan.py build` reads the reel's competitor numbers (Rover 4.9 stars
and 515,771 ratings, 106 of 341 recent 1 and 2 star reviews mention fees;
Wag! 4.8 stars and 67,447 ratings, 81 of 324 mention cancellations), the
market (71M US homes with a dog, $158B US pet spend in 2025, a top-down
TAM of $8.5B, SAM $228M, SOM $22.8M) and the model:

```
Leashly: business plan, 9 of 9 sections written.
  Per walk     price $25.00, take 15% = $3.75, contribution $2.23
  LTV:CAC      4.24x, CAC payback 3.37 months
Every check passed: no empty sections, and the numbers agree between files.
Wrote seed/plan.md and seed/plan.json.
Next: /seed-deck turns plan.json into the 10-slide deck.
```

The plan's key numbers: revenue $467,400 / $1,586,640 / $2,993,520 in years
1 to 3, breakeven in month 29 (May 2029), peak burn $82,801 a month, and the
cash lasts all 36 months (low point $252,553). Year 3 GMV ($19.96M) sits
under the $22.8M SOM, so that check passes.

## Rules

- Never promise funding, in the plan or in the chat. Raising money depends
  on the business; investors decide.
- Projections come from the founder's own assumptions. Say so wherever the
  plan shows revenue or runway. Not investment advice.
- No invented numbers: every figure traces to a file, and every market input
  carries its source.
- The team slide and section list real people with their real roles.
