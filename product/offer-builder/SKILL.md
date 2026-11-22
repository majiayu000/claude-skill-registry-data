---
name: offer-builder
description: >-
  Offer Builder. Writes the offer they can say yes to. One page: the problem in their own numbers, what
  they get, the price, the date it ships, and the way out, with the plain statement that it isn't finished
  yet. A lint refuses an offer that leaves any of that out or that leans on fake urgency, made-up proof and
  promises nobody can keep. Every offer waits for your yes. Use when the user says "write the offer", "make
  them an offer", "offer page", "proposal", "one-pager", "what do I send them", "they asked for details",
  or "founding customer offer".
argument-hint: "[draft <deal> | lint <file> | record <deal>]"
---

# offer-builder

A good offer takes one page and leaves no question open. The buyer should be able to forward it to their
boss with no explanation. This skill writes that page, and won't let it say anything you can't back up.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/offer.py" draft --deal north-pier --get "Every late invoice chased automatically" \
    --get "Built to your requirements, which we go through together after you pay"
python3 "${CLAUDE_SKILL_DIR}/offer.py" lint --offer whale/offers/north-pier.md
python3 "${CLAUDE_SKILL_DIR}/offer.py" record --deal north-pier --text-file whale/offers/north-pier.md \
    --subject "Your Product: the offer" --approval "yes" --at 2026-11-02T10:15
```

## What is on the page

1. **Today:** what they pay now for this, from the board. "$6,400 a month ($76,800 a year)."
2. **What it does,** in one line.
3. **What you get:** only what they told you they want (`--get`, repeat it). Never a padded feature list.
4. **The price:** from `/pricing`. One number, paid up front.
5. **When:** the ship date, from `/pre-sale terms`.
6. **What you should know:** it isn't finished, and how they get their money back.
7. **The next step:** say yes and you send the Stripe link.

## Steps

1. Check that `/pre-sale terms` is set and the deal has a price from `/pricing`. `draft` refuses without them.
2. `offer.py draft`. Read their words from the demo call and use them. Fill every `[fill: ...]`.
3. `offer.py lint`. Fix everything it finds. If a line isn't provable, it doesn't go in.
4. **Ask.** Show the page. "Send this to Renee Alvarez at North Pier Logistics? Reply yes or no." One offer per question, every time.
5. **Send.** On a yes, as a Gmail draft from the user's account, which the user sends (or through the Gmail connector right after that yes).
6. **Log.** Only after it went out: `offer.py record --approval "<their yes, word for word>"`. The deal moves to `offer-sent`, and `/follow-up`
   keeps it alive. When they say yes, `/pre-sale link`. When they push back, `/objection-handler`.

## What lint refuses

- No price, no ship date, nothing saying it isn't finished, or no way to get their money back.
- Fake urgency: "act now", "limited time", "only 3 spots left", "last chance". If the price really does end, say the real date and why.
- Claims nobody can check: "guaranteed", "risk-free", "#1", "best in the industry", "trusted by", "thousands of customers".
- Anything still marked `[fill: ...]`.

## Example from the reel

For North Pier Logistics: "Today you pay about $6,400 a month for invoice collections service ($76,800 a year)." Founding customer · 12 months,
$24,000.00, paid up front. Ships within 30 days of payment, built to your requirements. It isn't finished, and they get every dollar back if it
doesn't ship. (Illustrative: North Pier and every figure are fictional.)

## What it never does

- Never sends, and never records an offer that did not go out.
- Never hides that the product isn't finished.
- Never invents a customer, a result, a discount or a deadline to make it feel urgent.

## Consent and truth

- Nothing is sent or charged without the user's explicit yes for that exact offer. Claude drafts, the user says "yes", then it goes out from
  the user's own accounts. One yes per message. Never "yes to all".
- Stop at the first "no" or any sign of disinterest. A request to stop is honoured forever, across every skill.
- Never invent a number, a result, a client or a deadline. An offer is a template, not legal advice: have a lawyer read your standard terms once.
