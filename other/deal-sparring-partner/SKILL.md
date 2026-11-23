---
name: deal-sparring-partner
description: "Use when the user is about to negotiate a purchase, rent, vendor, contract or service deal (a car, an apartment lease, a contractor quote, a subscription renewal) and wants to prepare, rehearse or practise it, or have the other side played back to them (for example 'help me negotiate this', 'play the landlord', 'let me practise before I call the dealer')."
---

# Deal Sparring Partner

## Overview

Prepares the user, plays the other side realistically, then scores the result by a number, not by feel. A rehearsal is only worth something if the counterpart concedes the way real ones do and the score measures what the user actually kept. A script sets the counterpart's concession ladder and computes the score.

## Setup

Get four things, asking at most one short question for anything missing: which side the user is on, what the deal is, their **walkaway** (the worst deal they would still take, set by their best alternative) and their target. Put every term on one scale of money: a month of free rent, a warranty or a faster delivery gets a dollar value. Say that the other side's numbers in the rehearsal are estimates. For high-stakes legal or employment contracts, say you are not a lawyer.

## Process

1. **Prep sheet.** Estimate the other side's opening, target and reservation (their worst acceptable deal) from comparable prices you found and opened this session, with source and date; anything not sourced is labelled as an assumption. List the other side's interests, three objections they will raise with a reply for each, and what the user can trade that costs them little and is worth something to the other side.
2. **Fix the ladder.** Run `python scripts/deal.py ladder --side buyer|seller --opening N --target N --reservation N` (the script sits next to this file; `--side` is the user's side). Keep the output to yourself.
3. **Play the other side**, one short in-character message per turn, no coaching mid-scene. Rules: start at rung 0; move one rung only when the user concedes something, gives a reason you can accept, or offers a trade; accept any offer at or better than your current rung; never pass `never_cross`; never reveal a ladder number you have not offered or say how firm you are; if the user calls an offer final and then moves, treat later "finals" as weak. Real counterparts ask questions and name their own constraints; do that, and invent no facts the prep sheet does not support. Stay in character until the user says stop, agrees a price or walks.
4. **Score** only an agreed price or a walk. If the scene just stops, ask whether the user walks or keeps going, and play on. Run `python scripts/deal.py score --side ... --walkaway N --reservation N --final N` (or `--no-deal`). Report its `outcome`, the user's share of the zone, and what it means: a deal worse than the walkaway, a missed deal, or no deal possible are different results. Never judge who won by comparing the sizes of the concessions. The reservation was an estimate, so call the share approximate.
5. **Debrief** against the transcript, quoting the user's own messages: did they anchor first, give a reason with each ask, concede in shrinking steps, trade rather than give, ask questions, and say "final" only when they would walk. Give the two changes that would have moved the number most, then offer a second round.

## Common Mistakes

- Conceding in uneven or growing steps; use the ladder.
- Conceding because the user sounds sure, with no reason or trade.
- Hinting at the reservation or coaching during the scene.
- Scoring by concession size or by whether the user "felt" good.
- Prices from memory instead of opened, dated comparables.
- Letting the other side invent facts that make the user's case impossible.
