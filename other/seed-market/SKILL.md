---
name: seed-market
description: >-
  Market Sizer. Sizes your market the way investors check it: TAM top-down
  (population x share x spend a year), SAM bottom-up (customers you can
  reach x purchases a year x price) and SOM (the share of SAM you can win in
  N years, with a stated reason). Every input carries a source (a URL, a
  named publication, or an assumption said out loud), vague sources are
  refused, and it refuses any result that breaks SOM <= SAM <= TAM. Records
  sourced facts the deck quotes. Writes seed/market.json for the plan, the
  deck and the pitch coach. Use when the user says "how big is my market",
  "TAM SAM SOM", "size the market", "market size slide", "is this market
  big enough", or after /seed-scout, before /seed-model and /seed-plan.
argument-hint: "[top-down | bottom-up | som | cite | show | check]"
---

# seed-market

The Market Sizer turns "a huge market" into three numbers an investor can
check. The total market (TAM) is everyone who could buy, top-down from
public data. The market you can serve (SAM) is built bottom-up from the
customers you can actually reach, how often they buy and your price. The
share you can win (SOM) is a slice of SAM over a few years, with the reason
written next to it. Every input says where it came from, and the guesses are
labelled as guesses so nobody mistakes them for facts.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/market.py" top-down --population 71M --population-name "US homes with a dog" \
    --population-source "APPA 2026 State of the Industry report (americanpetproducts.org)" \
    --share 10% --share-source "assumption: about 1 in 10 dog homes pays for walks; check with a survey" \
    --spend 2400 --spend-source "assumption: 8 walks a month at the \$25 price" --write
python3 "${CLAUDE_SKILL_DIR}/market.py" bottom-up --customers 400K --customers-source "..." \
    --frequency 96 --frequency-source "..." --price 25 --price-source "..." --unit walk --write
python3 "${CLAUDE_SKILL_DIR}/market.py" som --share 2.5% --years 3 --reason "who switches, and why" --write
python3 "${CLAUDE_SKILL_DIR}/market.py" cite --name "US pet industry spend, 2025" --value 158B --source "APPA ..." --write
python3 "${CLAUDE_SKILL_DIR}/market.py" show
python3 "${CLAUDE_SKILL_DIR}/market.py" check      # exit 1 if anything is out of order or unsourced
```

Other flags: `--level tam|sam` (either method can fill either level),
`--population-name`, `--share-name`, `--spend-name`, `--customers-name`,
`--currency`, `--dir`, `--json`, `--today`.

## What it reads and writes

| file | what |
| --- | --- |
| your sources | public reports, government data, your own pricing; or an assumption with its reason |
| `seed/market.json` | with `--write`: `tam`, `sam`, `som`, `currency`, `method`, the formulas, `inputs` (name, value, unit, source, kind, level), the SOM share, years and reason. `/seed-plan`, `/seed-deck` and `/seed-coach` read it |

## The method and the rules

- **TAM, top-down:** population x share x spend a year. **SAM, bottom-up:**
  customers x purchases a year x price. **SOM:** a share of SAM within N
  years (1 to 10). All yearly, exact (Decimal), rounded half up to the dollar.
- **SOM <= SAM <= TAM.** A write that breaks it is refused (exit 1) and the
  file stays as it was. When SAM changes, SOM is recomputed from its share.
- **A source on every input.** A URL, a named publication, or
  "assumption: <why>". "google", "TBD", "ChatGPT", a single word or an
  assumption without its reason are refused. Assumptions are listed every
  time the numbers print: say so when you quote them.
- **A reason on every SOM**, a real sentence: who switches, why, how you
  reach them. Over 10% of SAM gets a note: be ready to defend it.
- **Facts are not math.** `cite` keeps a sourced number (an industry total)
  that the plan and deck quote, so every number on a slide has a home.
- Estimates from your inputs, not a forecast. Not investment advice.

## Steps

1. Find the real numbers first: a trade association report, census or
   government data, a public filing. Open the page and keep its name or URL.
   Never use a number you could not open.
2. Run `top-down ... --write` for the TAM with those numbers. Where there is
   no public number, write an assumption with its reason, and tell the user.
3. Run `bottom-up ... --write` for the SAM from the customers you can reach
   at launch, how often they buy (match `/seed-model`) and your price.
4. Run `som --share X% --years N --reason "..." --write`. Keep it in line
   with the model's customers in year N.
5. `cite` the headline facts the deck will show. Run `check` (it must exit
   0) and `show`, then read the three numbers and every assumption back.
6. Hand off to `/seed-model` (the 36-month model) and `/seed-plan`, which
   puts the Market section together from `seed/market.json`.

## Example: the reel

Leashly (made up) is a US dog-walking app at $25 a walk. The real numbers
are APPA's: 71 million US homes (53%) have a dog, and Americans spent $158
billion on pets in 2025 (APPA 2026 State of the Industry report). The rest
are Leashly's assumptions, labelled as such:

```
Market size (USD a year), top-down TAM, bottom-up SAM, SOM 2.5% of SAM in 3 years
  TAM  $17.04B    71,000,000 US homes with a dog x 10% x $2,400 = $17,040,000,000
  SAM  $960M      400,000 paying dog homes in the 3 launch cities x 96 walks a year x $25 = $960,000,000
  SOM  $24M       2.5% of SAM $960,000,000 = $24,000,000
  Fact: US pet industry spend, 2025 = $158B (APPA 2026 State of the Industry report (americanpetproducts.org))
  Fact: Share of US homes with a dog = 53% of US homes (APPA 2026 State of the Industry report (americanpetproducts.org))
```

The 10% share, the $2,400 a year (8 walks a month at $25) and the 400,000
launch-city homes are assumptions to replace with real data. The SOM's
reason: owners leaving Rover over fees and Wag! over cancellations switch to
flat $25 walks with a backup walker, 10,000 of the 400,000 homes by year 3.

## What it never does

It never makes up a statistic, never passes off an assumption as a fact,
never inflates a share to make the slide bigger, and never promises that the
market will turn into revenue.
