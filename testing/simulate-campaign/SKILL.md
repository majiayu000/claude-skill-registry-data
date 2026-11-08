---
name: simulate-campaign
description: Run ad copy, landing pages or a finished deliverable past a panel of synthetic reader personas before spending money or sending it — five small-business owner personas (restaurant, Italian, bar & grill, Mediterranean, cafe) scoring scroll-stop, click, trust and buy, plus two reader-QA gates (a PE roll-up acquirer and a commercial real estate broker) that return SHIP or REFRAME. Use to catch copy defects, wrong-audience framing and machine-smelling numbers before launch; not to predict response rates.
---

# Simulate campaign (synthetic reader panel)

Show each creative to each persona, have the persona react in first person with scores and
objections, then rank and fix. The personas live in `personas/`; each is a self-contained prompt
("You ARE ...").

## What a persona panel is good for, and what it isn't

**Good at:** catching copy defects. A headline nobody would stop for, a pitch that smells like a
sales funnel, a number that reads as machine-guessed, a deliverable written to the wrong reader
(owner advice in a broker brief), an objection the page never answers.

**Bad at:** predicting who will reply or buy. In a backtest of persona panels against real
outreach outcomes, panel scores ranked actual replies at about chance (AUC ~0.5). Treat scores as a
defect detector, never a forecast, and never report "personas say 70% will click".

Synthetic personas also drift toward agreement. Counter it: the persona file says what makes them
bounce; ask for objections before scores; and run each persona as a **separate** call or subagent
that sees only its persona file and the creative, never your reasoning or the other personas'
answers. (For a fuller anti-sycophancy protocol on a live product, see `role-litmus`.)

## The panel

| File | Who | Use for |
|---|---|---|
| `maria.md` | struggling full-service owner, cash-tight, scrolls late at night | ads, landing pages |
| `tony.md` | established Italian owner, skeptical of tech | ads, landing pages |
| `dave.md` | overwhelmed bar & grill owner, no bandwidth | ads, landing pages |
| `yara.md` | cost-squeezed Mediterranean owner, needs proof | ads, landing pages |
| `jake.md` | data-literate cafe owner, needs depth | "is this too basic?" |
| `acquirer.md` | PE / roll-up buyer (home services) | reader-QA on a deal feed or target list |
| `broker.md` | commercial real estate broker | reader-QA on a prospecting dossier or brief |

Write your own from the same shape: who they are, their numbers, their psychology (pain, pride,
skepticism, when and where they read, what stops the scroll, what makes them click, bounce and
buy), then the scoring protocol. Adjust prices in the files to your offer.

## Run it

1. **Collect the creatives.** For ads: headline, primary text, image description, CTA, and the
   landing page text (fetch the live page so the persona reads what ships). For a deliverable:
   the draft itself.
2. **Match personas to creatives.** Each sector's ad goes to its sector persona; run a cross-test
   (every persona x every ad) when the targeting is broad.
3. **One isolated call per (persona, creative)**: the persona file as the system prompt, the
   creative as the message, and an instruction to answer in this JSON:
   ```json
   {"scroll": 0, "click": 0, "trust": 0, "buy": 0,
    "monologue": "...", "objections": ["..."], "one_change": "...", "verdict": "SHIP|REFRAME|null"}
   ```
4. **Rank** variations by mean score; list the objections that recur across personas.

## Reading the scores

| Score | Meaning |
|---|---|
| 8-10 | strong |
| 6-7 | workable with the persona's one change |
| 4-5 | weak: read the objections, rewrite |
| 0-3 | dead for this audience |

- **Scroll is the gatekeeper.** Under 5 and nothing else matters: fix the headline first.
- **High scroll + low buy** = the ad hooks and the landing page doesn't close.
- **Reader-QA personas** end on SHIP or REFRAME. An audience-test failure (owner-facing advice
  in a broker or buyer document) is REFRAME regardless of other scores.
- Objections that two or more personas raise are the real fixes; a single persona's objection is
  a curiosity.

## Iterate

Fix the recurring objections, re-run, compare. When the top variants clear 7 across their target
personas, the copy is free of the defects a panel can see. Then measure the real thing with real
traffic.
