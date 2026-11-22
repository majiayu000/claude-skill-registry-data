---
name: pre-sale
description: >-
  Pre-Sale. Gets customers to pay up front, and uses what they ask for to build the exact product. Sets
  honest terms (it isn't finished, the date it ships, how they get their money back), checks them, prepares
  a Stripe Payment Link in your own account for one buyer, logs real payments, and tells you when enough
  companies have paid to call it validated. Then it holds you to the date: it flags every promise coming due
  and writes the delay notice with the refund offer. Use when the user says "pre-sell", "pre-sale", "get them
  to pay up front", "take a deposit", "charge before I build", "send a payment link", "validate with money",
  "who has paid", "am I validated", or "they said yes".
argument-hint: "[terms | link <deal> | record <deal> | validated | due]"
---

# pre-sale

This is the one that changes the game. Anyone will say "that sounds great". Very few will pay. A company
that pays before the product exists has told you the only thing that matters, and then it tells you exactly
what to build. But you are holding someone's money for something that doesn't exist yet, so this skill is
strict about being open and about giving it back.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/presale.py" terms --item "Founding customer · 12 months" --ships-in 30
python3 "${CLAUDE_SKILL_DIR}/presale.py" check
python3 "${CLAUDE_SKILL_DIR}/presale.py" link --deal north-pier
python3 "${CLAUDE_SKILL_DIR}/presale.py" record --deal north-pier --amount 24000 --ref pi_3Qa1b2 --on 2026-11-03 --live
python3 "${CLAUDE_SKILL_DIR}/presale.py" validated --marketing-spent 0
python3 "${CLAUDE_SKILL_DIR}/presale.py" due --today 2026-11-05
python3 "${CLAUDE_SKILL_DIR}/presale.py" notice --deal copperline --new-date 2026-12-19 --reason "The QuickBooks sync needs two more weeks."
python3 "${CLAUDE_SKILL_DIR}/presale.py" new-date --deal copperline --date 2026-12-19 --said "Yes that works." --at 2026-11-30
python3 "${CLAUDE_SKILL_DIR}/presale.py" refund --deal copperline --ref re_3Qa1b2 --on 2026-12-20
python3 "${CLAUDE_SKILL_DIR}/presale.py" deliver --deal north-pier --on 2026-12-01
```

## The three things the buyer always sees

`check` refuses a checkout without them, and `link` puts them right above the pay button:

1. **It isn't finished.** "This product is not finished yet. You are paying now for the version we build to your requirements."
2. **The date.** "Ships within 30 days of payment." `check` refuses anything over 90 days: for longer, take a deposit.
3. **The way out.** "If it has not shipped by the promised date, or we can't build what you asked for, you get every dollar back."

## Steps

1. **Terms first.** `presale.py terms`. Promise a date you would bet on. Then `presale.py check`.
2. **Only after a real conversation.** `link` refuses a deal that hasn't replied. Nobody pays from a cold email.
3. **Price it.** `/pricing` sets the amount, from what they pay today. `/offer-builder` writes the one page they say yes to.
4. **Try it in test mode.** In Stripe's test mode, open the link and pay with Stripe's test card, 4242 4242 4242 4242. Test
   payments never go on the board.
5. **Create the real link.** `presale.py link` prints exactly what to create: one buyer, one payment, the terms above the button.
   Ask: "Create this Stripe link for $24,000.00 for North Pier Logistics? Reply yes or no." On a yes, create it in the user's
   own account, through the Stripe connector or the Dashboard, in live mode only if they said live.
6. **Send it.** Show the email with the link. "Send this to Renee Alvarez? Reply yes or no." Then it goes out from their account.
7. **Log only what Stripe shows.** The user (or the connector) confirms the payment is marked paid and live. Then
   `presale.py record --live` with the reference. That starts the clock: `ships_by` is the date you promised.
8. **Ask what they need.** The same day, hand over to `/requirements`. "You paid for the version built to your requirements. What
   are they?" That is the list you build.
9. **Check the score.** `presale.py validated` says VALIDATED only at your target (default 3 paying companies), and a refund takes it back.

## Holding the money

Stripe's pre-order guidance doesn't rule out charging up front, and it is worth reading before you do. Payment Links charge at once.
Stripe also describes saving the card to charge later, or authorizing now and capturing later, but an authorization typically lasts
only about 7 days, so it won't span a 30-day build. Stripe says pre-orders carry real risk and recommends partial deposits, limiting
the number of orders, realistic delivery dates, and keeping enough cash on hand for refunds and disputes. So:

- **Don't spend it until it ships.** Keep enough to refund everyone. A customer can also dispute a card charge, and Stripe can hold funds.
- **A deposit is a real yes.** `record --deposit` logs a part payment, and the deal keeps its first date.
- **Stop selling at what you can build.** Three customers you delight beat twenty you refund.
- **Tell Stripe what you do** if they ask, and check your account's terms for your country.

## When the date slips

`due` flags every promise. Tell them *before* the date, never after. `notice` writes the email: the new date, and their money back if
that doesn't work or you don't hear from them. Only their yes moves the date (`new-date`). Refund quickly, 7 working days at most,
and `refund` logs it. In the US, the FTC's Mail, Internet, or Telephone Order Merchandise Rule covers most goods ordered online: ship
when you said (within 30 days if you said nothing), and if you can't, get their consent to the delay or refund them. Whether it covers
your product is a question for a lawyer. This skill works that way regardless.

## Example from the reel

Your Product, Founding customer · 12 months, $24,000.00, ships in 30 days. North Pier Logistics pays on Nov 3, Saltmarsh Freight
$18,000.00 on Nov 4, Copperline Haul $12,000.00 on Nov 5. `validated`: VALIDATED, 3 of 3 paying customers, $54,000.00 in, marketing spent
$0.00. Then `/requirements` turns what they asked for into the build list. (Illustrative: every company and payment is fictional, and
the card in the reel is Stripe's published test number.)

## What it never does

- Never sees, asks for or types a card number. The buyer pays on Stripe's own page.
- Never sends a link or creates a live one without a yes. Never charges anyone, and never moves money itself.
- Never hides that it isn't finished, and never takes money for something the user doesn't intend to build.
- Never counts a test payment, a promise or a "yes, send me the invoice" as a paying customer.

## Consent and truth

- Nothing is sent, created or charged without the user's explicit yes for that exact message or link. Claude drafts, the user says
  "yes", then it goes out from the user's own accounts. One yes per message. Never "yes to all".
- Stop at the first "no" or any sign of disinterest. A request to stop is honoured forever, across every skill.
- Never invent a number, a result, a client or a deadline. Taking money before delivery has legal and tax consequences that vary by
  place: this is not legal, tax or financial advice, so have a professional read your terms once.
