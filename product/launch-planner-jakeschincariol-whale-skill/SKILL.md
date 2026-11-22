---
name: launch-planner
description: >-
  Launch Planner. Plans the launch once it is paid for. Works backwards from the earliest date you promised
  a paying customer: requirements confirmed, feature complete, customers testing, fixes, first ship, then the
  rest. The public launch comes last, behind a gate that stays closed until someone has the product, nobody is
  late, and everything they paid for is built. Use when the user says "launch plan", "when do we launch",
  "are we on track", "what's next", "plan the launch", "can we launch yet", "launch checklist", or once
  customers have paid.
argument-hint: "[plan | status | gate]"
---

# launch-planner

The usual order is build, launch, then hope. Here it's the other way round: paid, built, delivered, and only then
launched. By launch day you have customers, a real story and no reason to spend money on ads. This skill plans the
weeks in between, around the only dates that matter: the ones you promised.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/launch.py" plan --today 2026-11-05
python3 "${CLAUDE_SKILL_DIR}/launch.py" status --today 2026-11-20
python3 "${CLAUDE_SKILL_DIR}/launch.py" gate --today 2026-12-20
```

## The plan

Counted back from the first date you promised:

- **25 days before:** every paying customer confirms the requirements (`/requirements confirm`).
- **10 days before:** feature complete, everything on the build list.
- **7 days before:** each customer tests it on their own data, with you watching.
- **2 days before:** fix what they found. If anything will slip, tell them now (`/pre-sale notice`).
- **The day:** ship to the first customer, then each of the others by their own date.
- **14 days after the last one:** the public launch, if the gate is open.

`plan` writes `whale/launch-plan.md`. A step whose date has already passed is marked to do first. If the dates don't fit what's on the build
list, say so today: talk to the customers, not the calendar.

## Steps, every Monday

1. `launch.py status`. Features built, what's next, and days left for each customer.
2. `/pre-sale due`. Anything SOON or LATE is this week's top job.
3. When a customer has it, `/pre-sale deliver`, and check in after a week. Once they've seen a result, `/case-study`.
4. Before anything public, `launch.py gate`.

## The gate

`gate` stays CLOSED until all of this is true, and says what's in the way:

- At least one customer has the product.
- Nobody is late. Deliver, agree a new date, or refund them first.
- Everything paying customers asked for is built.

Why so strict: the customers who paid first took the risk. A public launch while one of them is waiting is how you lose them, and they're your best proof.

## Launching, when it opens

- **Tell the first customers first,** and thank them. Ask if you can name them (`/case-study`).
- **Lead with the case study,** not with features.
- **Go where your buyers are:** the trade group, the forum, the newsletter you found in `/market-researcher`.
- **Pitch the next whales.** You can now say something you couldn't before: a real company uses this, and here's what changed.
- **Keep the pre-sale honest.** New customers get the real product at the real price. The founding price was for the risk they didn't take.

Posting, emailing and spending on a launch are all the user's calls, one at a time.

## Example from the reel's board

Three paying customers on Nov 5, $54,000.00 in. First promise Dec 3. Plan: requirements confirmed by Nov 8, feature complete Nov 23, customers testing Nov 26, fixes
Dec 1, ship Dec 3, Dec 4 and Dec 5, public launch Dec 19. `gate` today: CLOSED, no customer has the product yet. (Illustrative: every company and date is fictional.)

## What it never does

- Never plans a launch before anyone has paid. The plan starts when the money does.
- Never opens the gate over a late or unfinished customer.
- Never posts, sends or spends anything by itself.

## Consent and truth

- Nothing is sent, published or charged without the user's explicit yes for that exact message or post. One yes per message. Never "yes to all".
- A date you promised is a promise. If it will slip, the customer hears it from you first, with their money back on offer.
- Never invent a number, a result, a client or a deadline. Launch claims must be things you can back up.
