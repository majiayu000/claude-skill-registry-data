---
name: pricing
description: >-
  Pricing. Sets the price from what they pay today. Takes the money already leaving their account for this
  problem, works out the year, and gives three prices with what each one leaves them, or checks a price you
  already have in mind, with the working shown so it can be argued with. Then puts the chosen price on the
  deal. Use when the user says "what should I charge", "pricing", "how much is this worth", "set the price",
  "founding price", "am I charging too little", or before writing an offer.
argument-hint: "[options <pay per month> | check <price> | set <deal> <price>]"
---

# pricing

Don't price from your costs, and don't price from a competitor's page. Price from what the buyer already pays
to have this problem. It's the only number they can't argue with, because it's theirs.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/price.py" options --pay-month 6400
python3 "${CLAUDE_SKILL_DIR}/price.py" check --pay-month 6400 --price 24000
python3 "${CLAUDE_SKILL_DIR}/price.py" set --deal north-pier --price 24000
```

`--months` changes the term (default 12).

## The three prices

- **Easy yes, 25%** of what they pay now. Quick to say yes to. Good when you need the first customer more than the money.
- **Founding price, about 33%.** The default: a real saving for them, real money for you, and a reason to be early.
- **Full value, 50%.** When you're certain of the problem and they've seen the demo.

## Steps

1. Get the number. Use what they told you, then the board (`spend_month`), then the market research. No number, no price: go back to
   `/market-researcher` or ask them.
2. `price.py options`. Read the three to the user with the working: what they pay, what they'd pay, what they keep.
3. If the user has a price in mind, `price.py check`. It says what share that is, and warns when it's high for something unfinished, or
   so low it reads as a toy.
4. Agree the number with the user. It's their call: the tool shows the working, the user decides.
5. `price.py set`. `/offer-builder` and `/pre-sale link` read it from the deal. A price can't change after they've paid.

## Things to think through

- **What "founding" means.** Say what they get for being first: this price, and a say in what gets built. If the price really won't last,
  name the real date. If it will, don't pretend.
- **Size.** A bigger company paying more for this problem pays a bigger founding price, from the same share of its own number.
- **Annual, up front.** A year up front is the point of a pre-sale. If that's hard for them, a deposit beats a discount (`/pre-sale record --deposit`).
- **Your costs still matter.** Before you commit, check it pays for the build and whatever it costs to run for those 12 months. Stripe also takes its fee.
- **Don't cut the price to win.** Change what they get instead.

## Example from the reel

North Pier pays $6,400 a month, $76,800 a year. Options: $19,000 (25%), $26,000 (34%), $38,000 (49%). The reel's price: `check --price 24000`
says 31% of what they pay today, and they keep $52,800. (Illustrative: North Pier and every figure are fictional.)

## What it never does

- Never sets a price with no number behind it, and never invents what a company pays.
- Never promises the saving. "They keep $52,800" is arithmetic on their current bill, not a guarantee of what they'll save.
- Never changes a price after payment.

## Consent and truth

- Nothing is sent or charged without the user's explicit yes. This skill only does the arithmetic and writes the price on the deal.
- Never invent a number, a result, a client or a deadline. Fill in only what is true and ask when something is missing.
- Pricing here is a starting point, not financial advice.
