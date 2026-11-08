---
name: seed-terms
description: >-
  Term Sheet Reader. Reads a SAFE or a term sheet in plain English, does the
  dilution math and flags the clauses to ask a lawyer about. Works out what a
  post-money SAFE owns at its cap and what it converts into at a priced round
  (cap price vs discount price, whichever is lower), builds a priced round's
  cap table with the option-pool shuffle (price per share, new shares, the
  pool top-up, the effective pre-money, everyone's dilution), and scans a
  pasted term sheet for the traps: liquidation preference over 1x,
  participating preferred, full ratchet, redemption, cumulative dividends,
  board control, operating vetoes, pay-to-play, drag-along, long no-shops,
  exploding deadlines, founder vesting resets, super pro rata and MFN, each
  with a severity and a question for the lawyer. Not legal advice. Writes
  seed/terms/ with --write. Use when the user says "read this term sheet",
  "is this a good deal", "what does this SAFE mean", "how much do I own
  after", "how much dilution", "what's the option pool shuffle", "what is a
  post-money cap", "any red flags in this", or when an investor sends terms
  after a /seed-closer call.
argument-hint: "[safe | round | scan FILE]"
---

# seed-terms

The Term Sheet Reader is for the day an investor says yes and sends paper.
It does two jobs. First the arithmetic: what a SAFE really owns, what a
priced round does to the cap table, and how much of "the valuation" is
quietly paid by the founders through a bigger option pool. Then the reading:
it walks through the document and flags the clauses founders most often
regret, in plain words, with the exact question to put to a lawyer.

**Not legal advice, and not investment advice.** It is arithmetic and a
keyword reader. A startup lawyer should read every document before the user
signs anything, and the scanner only flags clauses it knows.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/terms.py" safe --investment 500k --cap 10m                      # 5.00% at the cap
python3 "${CLAUDE_SKILL_DIR}/terms.py" safe --investment 500k --cap 10m --other 1m@10m       # the whole SAFE round
python3 "${CLAUDE_SKILL_DIR}/terms.py" safe --investment 500k --cap 10m --discount 20 --round-pre 24m --round-raise 6m --pool 10
python3 "${CLAUDE_SKILL_DIR}/terms.py" round --pre 6m --raise 1.5m --pool 10 --shares 7000000
python3 "${CLAUDE_SKILL_DIR}/terms.py" round --pre 24m --raise 6m --pool 10 --cap-table seed/terms/cap-table.json
python3 "${CLAUDE_SKILL_DIR}/terms.py" scan term-sheet.txt                                  # exit 3 = a high flag
```

Amounts: `500k`, `1.5m`, `$1,500,000`. Percentages: `20` or `20%`. A SAFE:
`[name=]investment[@cap][:discount]`, like `Northlight=500k@10m` or
`250k@8m:20`. Add `--write` to save `seed/terms/safe.json`,
`seed/terms/round.json` or `seed/terms/scan-<name>.md`; `--json` on scan.

## What it reads and writes

| file | what |
| --- | --- |
| a term sheet or SAFE as text | for `scan`: paste the PDF's text into a .txt file first |
| `--cap-table FILE.json` | optional: `{"holders": [{"name", "shares"}], "pool_unissued", "safes": [{"name", "investment", "cap", "discount"}]}` |
| `seed/terms/safe.json`, `round.json` | with `--write`: every input and every number shown |
| `seed/terms/scan-<name>.md` | with `--write`: the flags, the excerpts and the questions |

## The method

- **Post-money SAFE** (Y Combinator's standard form). Ownership at the cap =
  investment / post-money cap. It converts at the lower of the cap price
  (cap / company capitalization: every share, option, the unissued pool and
  all converting SAFEs, but not the new money or a pool top-up made for the
  round) and the discount price (the round price x (1 - discount)). With
  post-money caps, every extra SAFE dilutes the founders, not the other SAFE
  holders.
- **Priced round.** Price per share = pre-money / fully diluted pre-money
  shares, where that count already includes the converted SAFEs and the new
  pool. The pool target is the unissued pool as a share of the post-money
  count. That is the option-pool shuffle: the pool is carved out before the
  money comes in, so only existing holders pay for it. The tool prints the
  effective pre-money (pre-money minus the pool top-up at the round price).
- The math is exact (fractions), shares are rounded down to whole shares at
  the end. Real documents round the price first; expect a few shares of drift.
- **The scanner** splits the text into clauses and flags, by rules: a
  liquidation preference over 1x, participating preferred (capped or not),
  full-ratchet or narrow-based anti-dilution, redemption rights, cumulative
  dividends, investor control of the board (it counts the seats), protective
  provisions that reach into the budget, hiring or debt, pay-to-play, a
  drag-along the preferred alone can trigger, a no-shop over 30 days (60 or
  more is high), a deadline of 48 hours or less, a founder vesting reset,
  super pro rata, MFN, and a new pool counted in the pre-money. Severity is
  high (push back), medium (understand it, likely negotiate) or low (common,
  know it). The standard versions (1x non-participating, broad-based weighted
  average, no redemption, founder board majority, a 30-day no-shop) are listed
  as standard.

## Steps

1. Ask for the document and the numbers (the raise, the valuation or cap,
   the pool, the current shares). For a PDF, extract the text into a .txt.
2. `terms.py scan FILE`. Read every flag back in plain words: what it means,
   then the question for the lawyer. Never tell the user a clause is fine to
   sign; say what is standard and what is not.
3. Run the math: `safe` for a SAFE (with `--other` for the rest of the round),
   `round` for a priced round. Show the founders' percentage before and after
   and the effective pre-money. Try the counter-offer too (a smaller pool, a
   higher cap) so the user sees what each ask is worth.
4. Write the questions into a short list for the lawyer. Recommend a startup
   lawyer before signing, every time.
5. Hand off: /seed-dataroom for the confirmatory diligence that follows a
   signed term sheet (`share-list --stage after`), and /seed-updates to keep
   the other investors posted.

## Example: the reel

Leashly (fictional) raises its $1.5M seed. As post-money SAFEs at an
illustrative $10M cap, `safe --investment 500k --cap 10m --name Northlight
--other 1m@10m` shows Northlight's $500,000 owning 5.00% at the cap, the whole
$1.5M owning 15.00%, and the founders keeping 85.00% before the next round.

Priced instead, at $6M pre-money with a 10% pool: `round --pre 6m --raise 1.5m
--pool 10 --shares 7000000` gives $0.7500 a share, 2,000,000 new shares for the
investors (20.00%), a 1,000,000-share pool (10.00%), and the founders at
70.00%. The pool's $750,000 comes out of the founders' side: the effective
pre-money is $6,000,000 - $750,000 = $5,250,000.

A tough (synthetic) term sheet with a 2x participating preference, a full
ratchet, investor board control, a 60-day no-shop and a 48-hour deadline comes
back with 11 high flags; the founder-friendly version comes back with standard
terms and two low notes.

## What it never does

- Never says "sign it", never calls a term sheet good or bad overall.
- Never presents its math as the official cap table: the company's lawyer and
  cap-table records are the source of truth.
- Never treats a clause it did not flag as safe. Not legal advice; not
  investment advice.
