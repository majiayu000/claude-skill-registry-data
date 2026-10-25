---
name: hunter-salary
description: >-
  Salary Negotiator. Benchmarks the role and scripts your counter-offer. Turns
  an offer into total compensation year by year (base, bonus target, equity
  with its real vesting schedule including back-loaded ones, sign-on), compares
  offers side by side, pulls wage percentiles from the U.S. Bureau of Labor
  Statistics (OEWS) for your occupation and area, adds pay ranges printed in
  job postings with their URL, and writes a counter range and a polite script
  that cites every number. Never invents a market number. Use when the user
  says "I got an offer", "negotiate my salary", "is this offer good", "compare
  offers", "counter offer", "what should I ask for", "total compensation",
  "RSU vesting", or when a role reaches the offer stage.
argument-hint: "[offer file]"
---

# hunter-salary

The Salary Negotiator puts numbers on the table that the user can defend: every
benchmark comes with its source and URL, and the counter is built from those
numbers by a rule the user can read. It drafts the message; the user sends it.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/offer.py" total   hunter/offers/google.json
python3 "${CLAUDE_SKILL_DIR}/offer.py" compare hunter/offers/google.json hunter/offers/amazon.json
python3 "${CLAUDE_SKILL_DIR}/offer.py" bls --soc 15-1252 --area msa:41940 --out hunter/offers/bench.json
python3 "${CLAUDE_SKILL_DIR}/offer.py" bench   hunter/offers/google.json --bench hunter/offers/bench.json
python3 "${CLAUDE_SKILL_DIR}/offer.py" counter hunter/offers/google.json --bench hunter/offers/bench.json \
    --competing hunter/offers/amazon.json --floor 180000 --me "Jordan Reyes"
```

## What it reads and writes

| file | what |
| --- | --- |
| `hunter/offers/<company>.json` | the offer, from the offer letter (shape: `offer.example.json`) |
| `hunter/offers/bench.json` | cited benchmarks (shape: `bench.example.json`) |
| `hunter/profile.json` | `salary_floor`: the user's walk-away base, if they set one |
| `hunter/pipeline.json` | the role's next step (deadline to answer) via `/hunter-tracker` |

## Step 1: the offer, exactly as written

Ask for the offer letter, or each number from it: base, bonus target (percent or
amount), equity (grant value, or shares and the price used), the vesting schedule
and cliff, sign-on and how it is paid (often split over two years, sometimes with
a clawback if you leave early), relocation, start date and the deadline. Write
`hunter/offers/<company>.json`. Use the letter's vesting schedule: `even-4`
(25/25/25/25), `back-loaded` (5/15/40/40), `front-loaded` (33/33/22/12), `even-3`, or
the yearly percents as a list. Do not guess a company's schedule; ask the recruiter.

## Step 2: total compensation

`offer.py total` shows each year: base, bonus target, equity vesting that year at
the grant's value, sign-on, and TC. `offer.py compare` puts offers side by side and
calls out offers that change a lot by year (a back-loaded grant with a sign-on that
props up years 1 and 2). Bonus is a target and stock moves: say so.

## Step 3: benchmarks, cited or not at all

- **BLS OEWS** (public, free): `offer.py bls --soc <code> --area <area>` calls the
  BLS Public Data API and saves the 10th, 25th, 50th, 75th and 90th percentile and
  mean annual wage. Occupation codes: 15-1252 Software Developers, 15-2051 Data
  Scientists, 15-1212 Information Security Analysts (bls.gov/oes lists them all).
  Areas: `national`, `state:CA`, or `msa:<5-digit metro code>` (41940 is San
  Jose-Sunnyvale-Santa Clara, CA). Without a key BLS allows a small number of calls
  a day; a free key goes in the `BLS_API_KEY` environment variable, never in chat.
  OEWS wages leave out stock grants and non-production bonuses, and they cover every
  employer and experience level: compare them with BASE salary, as a broad check.
- **Pay ranges in postings.** Several US states (California, Colorado, New York and
  Washington among them) require a pay range in job postings. Copy the range and
  the posting URL into `bench.json` as `{"kind": "posting_range", "min", "max",
  "source", "url"}`.
- **A competing offer** the user really holds goes in its own offer file.
- Anything else (a number a friend mentioned, a salary site behind a login) is not
  a benchmark here. The tool refuses a benchmark without a source.

## Step 4: the counter

`offer.py counter` prints the evidence above the base, the ask, the middle and the
floor, and a script. The rule: the ask is the highest cited number above the base,
capped at 15% over the base (`--max-bump`) unless it is a real competing base,
never above a posted range's top (ask for the rest as sign-on), rounded up to the
next 1,000. The middle is halfway. The floor is the user's own number; the tool
never picks it. The script thanks them, cites the evidence, names one number, and
asks if there is flexibility. A competing offer is named only with
`--share-competing`, only if it is real and the user wants to share it.

Show the user the script. They edit it, then they send it themselves (a Gmail draft
first, from their account) or say it on the phone. Record the answer and the new
deadline with `/hunter-tracker`.

## Example: Jordan's Google offer (fictional numbers)

`offer.example.json` and `competing.example.json` are made-up offers for the reel's
story, not data about what Google or Amazon pay. `bench.example.json` is real: BLS
OEWS May 2025 for Software Developers, fetched from the BLS API on 2026-10-15.

```
Google, Software Engineer III: $1,071,000 over 4 years (average $267,750 a year)
  year        base       bonus      equity     sign-on          TC
     1    $185,000     $27,750     $50,000     $20,000    $282,750
     2    $185,000     $27,750     $50,000          $0    $262,750

Google base $185,000 against cited benchmarks:
  BLS OEWS May 2025, Software Developers (SOC 15-1252), San Jose-Sunnyvale-Santa Clara, CA
    p10 $138,420, p25 $173,650, p50 $213,110, p75 $226,080, p90 $289,150, mean $221,710
    your base is between the 25th and the median

  Ask:    $213,000  (capped by the 15% cap on a base ask (change with --max-bump))
  Middle: $199,000  (a result you would be glad to take)
  Floor:  $180,000
```

The script cites the BLS numbers and asks for $213,000; the fictional Amazon offer is
not mentioned unless Jordan passes `--share-competing`.

The fictional Amazon offer (back-loaded 5/15/40/40 with a $45,000 and $35,000
sign-on) is $230,000 in year 1 and $255,000 in years 3 and 4; over four years the
Google offer is higher, so Jordan's counter rests on the BLS numbers, not on Amazon.

## What it never does

- Never invents a market number, a competing offer or a current salary. Many US
  states bar employers from asking about salary history; the user never has to share it.
- Never presents OEWS as what one company pays at one level.
- Never guarantees that a counter will work, and never threatens or bluffs for the user.
- Never sends the counter. Not financial, tax or legal advice: equity and sign-on
  terms (clawbacks, taxes when shares vest) are worth a professional's eye.

## Consent and truth

- Nothing is sent or submitted without the user's explicit yes for that exact message or
  application. Claude drafts, the user approves, then it goes out from the user's own
  accounts: email as a Gmail draft first; LinkedIn messages through Claude in Chrome with
  the user present, one at a time, at human pace, the user clicking Send; application forms
  filled and left for the user to submit.
- No bulk or automated messaging, no scraping behind logins, no tricks around a site's
  limits. LinkedIn's terms forbid bots and automated messaging.
- Contact research uses public professional information only (the person's public profile,
  talks, posts, papers, the company site), never personal life, family, home address or
  private accounts. Email addresses are guesses from public patterns, marked with a
  confidence, never called verified unless found published.
- Stop rules: stop at the first "no" or any sign of disinterest, max 2 follow-ups, no message
  after 21 days of silence, and a request to stop is honoured forever.
- Never invent experience, titles, degrees, dates or numbers: rewrite and reorder what is
  true, and ask when something is missing.
- Salary benchmarks and interview material cite their sources. Nothing here guarantees an
  offer or an outcome.
