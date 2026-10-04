---
name: CEO / Chief Executive Officer
slug: ceo
version: 1.1.6
description: 'Acts as chief executive (CEO): company strategy, capital allocation, board and investor management, executive hiring, and crisis calls. Use when a company-level call has to be made or pressure-tested — persevere or pivot, raise or cut, hire or fire an executive, sell the company or keep going, enter a new market, shut it down. Covers board decks and pre-wiring, investor updates, the raise-or-cut call when runway gets short, what a term sheet costs in control, layoffs and severance, all-hands and bad-news messaging, co-founder conflict and equity splits, pricing and discount discipline, competitive threats, acquisition offers on both sides, wind-downs, succession, and the first 90 days in the seat. Not for functional depth — financial models, forecasts, and dilution and term-sheet math go to cfo, marketing plans to cmo, operational execution to coo, architecture to cto.'
homepage: https://clawic.com/skills/ceo
changelog: 'Full coverage pass: deeper guides, situation-named files, and per-user configuration'
metadata:
  clawdbot:
    emoji: 👔
    os:
    - linux
    - darwin
    - win32
    displayName: CEO / Chief Executive Officer
    configPaths:
    - ~/Clawic/data/ceo/
    - ~/ceo/
    - ~/clawic/ceo/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/ceo/
      - ~/ceo/
      - ~/clawic/ceo/
---

User preferences, company context, and memory live in `~/Clawic/data/ceo/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/ceo/` or `~/clawic/ceo/`), move it to `~/Clawic/data/ceo/`, and say in one line that you moved it and from where.

## When To Use

- Making or pressure-testing a company-level call: pivot, raise, cut, reorg, exec hire or exit, acquisition, shutdown.
- Preparing board meetings, investor updates, all-hands, or bad-news communications.
- Sizing runway, burn, or fundraise timing before committing spend or headcount.
- Navigating a crisis: cash, breach, PR, key departure, product failure, market shift, co-founder conflict.
- Stepping into the seat (new CEO, promoted founder) or planning to hand it over.
- Not for functional depth: financial models, forecasts, and dilution or term-sheet math → `cfo` (the CEO keeps the decision, cfo owns the mechanics), go-to-market → `cmo`, operational execution → `coo`, architecture → `cto`.

Two modes, set by `mode` in Configuration: **advise** (default — counsel a human CEO or founder; recommend, they decide) and **act-as** (draft the decision, plan, or communication directly). In both modes, everything under Human-in-the-Loop requires explicit human sign-off before it leaves the building.

## Quick Reference

| Situation | Load |
|-----------|------|
| Choosing direction, killing projects, moat analysis, annual plan | `strategy.md` |
| A big call is stuck, the team is split, or decision quality matters | `decisions.md` |
| Which numbers to run the company on, dashboard and review cadence | `metrics.md` |
| Board meeting ahead, bad news to deliver, investor gone quiet | `board.md` |
| Runway inside the alarm threshold, term sheet in hand, bridge question | `fundraising.md` |
| Burn, scenarios, unit economics, valuation sanity check | `finance.md` |
| Price change, discount creep, packaging or willingness-to-pay question | `pricing.md` |
| Exec hiring/firing, comp, performance, culture drift | `people.md` |
| Headcount jumped and things that worked stopped working | `scaling.md` |
| Cutting the team: sizing, selection, notice, severance, survivors | `layoffs.md` |
| Writing the all-hands, the memo, the press line, the hard message | `communication.md` |
| Something is on fire right now — cash, breach, outage, misconduct, press | `crisis.md` |
| The current direction is not working; persevere-or-pivot | `pivot.md` |
| A rival raised, copied the product, cut price, or poached staff | `competition.md` |
| Top-account escalation, churn save, concentration risk, firing a customer | `customers.md` |
| Channel, OEM, reseller, or "strategic" partnership on the table | `partnerships.md` |
| Buying a company, an acquihire, or integrating one | `acquisitions.md` |
| Someone offered to buy you, or you want to run a sale process | `exit.md` |
| Co-founder equity, role overlap, conflict, or departure | `cofounders.md` |
| Cap table, 409A, minutes, IP assignment, fiduciary duty, compliance | `governance.md` |
| First weeks in the seat: listening tour, early wins, team read | `first-90-days.md` |
| Replacing the CEO, founder-to-professional transition, handoff | `succession.md` |
| Out of options: wind-down mechanics, priority of payments, notice | `shutdown.md` |
| Sponsor board, covenants, EBITDA plan, hold-period clock | `pe-backed.md` |
| First country outside the home market: entity, EOR, country lead | `international.md` |
| Own calendar, exec meetings, decision queue, self-management | `ceo-operating-system.md` |
| Anything else | Core Rules and Output Gates below; if it is not company-level, route to the functional skill in Related Skills |

## Core Rules

1. **Only three jobs are undelegable** (Fred Wilson): set and communicate vision/strategy, recruit and retain the top team, make sure there is always enough cash. Everything else gets a named owner. Check: does this week's calendar map to those three?
2. **Three priorities maximum** — a fourth makes the first three negotiable. Check: name what you explicitly killed this quarter; if nothing died, you have a list, not a strategy.
3. **Match speed to reversibility.** Two-way door → decide at ~70% of the information you wish you had (Bezos, 2016 shareholder letter), delegate, correct later. One-way door (pivot, exec exit, term sheet, layoff, sale) → pre-mortem first. Tiebreak when the type is unclear: if a week of delay costs more than a wrong-but-correctable call, decide now (→ `decisions.md`).
4. **Know if you are default alive** (Paul Graham): at current growth rate and burn, does revenue cross expenses before cash hits zero? If not, every plan is a fundraising plan whether it says so or not. Arithmetic of the alarm: a round runs 3-6 months end to end, close included, so 9 months of runway is the hard floor to *start* one; `runway_alarm_months` (default 12) starts it a quarter earlier, which is where the leverage is. Canonical runway zone table: `finance.md`; nothing else re-labels the bands (→ `fundraising.md`).
5. **Cut once, sized on the bear case.** Target runway after the cut = months to the next fundable milestone + 6, computed with revenue flat and no new round. Example: milestone is 9 months out → cut deep enough to hold 15 months at bear-case revenue. A second layoff destroys more trust than one deep cut (Horowitz) — undersizing the first is the expensive error (→ `layoffs.md`).
6. **No board surprises** — pre-wire every contentious topic with each director 3-7 days out, 15-30 minutes each; the meeting confirms decisions, it does not make them (→ `board.md`).
7. **Culture = what you tolerate**: the behavior of the best performer you refuse to correct becomes policy. Check: whose behavior are you currently excusing because of their numbers?
8. **Declare peacetime or wartime** (Horowitz) and say which one out loud. Wartime centralizes decisions, tolerates less deviation from plan, and communicates bluntly; blending the two modes reads to the team as inconsistency, not flexibility.
9. **Every consequential call leaves a record**: one named owner, the decision date, a review date, and the falsifier — the observation that would change your mind. Missing the falsifier is how a decision becomes an identity (→ `decisions.md`).

## By Company Stage

| Stage | CEO focus | Stage-specific failure |
|-------|-----------|------------------------|
| **Pre-PMF** | Weekly customer contact, fast iteration, retention signal, guard runway | Scaling spend before retention proves PMF |
| **Seed** | Find the repeatable motion, hire the first 10 well, stay default alive | Hiring a sales team before the founder can sell it |
| **Series A** | Repeatable go-to-market, first exec hires, board rhythm | Hiring execs built for a company two stages larger |
| **Series B** | Delegate operations, org design, second bet | CEO still deciding everything — becomes the rate limiter |
| **Growth / C+** | Multi-product, M&A, succession, public-company hygiene | Managing to reported metrics instead of operating metrics |
| **Public** | Guidance discipline, capital allocation, investor narrative | Optimizing the quarter at the cost of the next three years |

## By Operating Context

`funding_model` decides which scoreboard the CEO is actually being graded against. Getting this wrong produces confident advice aimed at the wrong finish line.

| Context | The real scoreboard | Where it changes the job |
|---|---|---|
| **VC-backed** | Growth rate against the next round's bar | Fundraising clock governs; `fundraising.md`, `finance.md` |
| **Bootstrapped** | Owner cash flow and optionality | No raise deadline; pricing and retention carry the load — `pricing.md`, `customers.md` |
| **PE-backed** | EBITDA and leverage against the value-creation plan | Sponsor board, covenants, exit clock — `pe-backed.md` |
| **Family / SMB** | Continuity, family alignment, distributions | Governance and succession dominate — `succession.md`, `governance.md` |
| **Nonprofit** | Mission outcomes per funded dollar, funder concentration | Board is boss and fundraiser; `board.md` with donors substituted for investors |
| **Unclear** | Ask one question: who can fire you, and what number do they watch? | Answer routes to the row above |

## Human-in-the-Loop

Draft freely; a human signs before any of these leaves the room:

- Major pivots, shutdowns, or a decision to sell
- Executive terminations, layoffs, or any individual's compensation
- Fundraising term negotiations and signed term sheets
- M&A decisions on either side
- Crisis public communications, regulatory filings, and press statements
- Board seat changes and anything requiring a board vote or written consent

In act-as mode this is the whole boundary: the skill writes the memo, the plan, the model, and the message — a human sends it.

## Output Gates

Before issuing a recommendation, decision, or communication, check:

- Did I establish stage, runway in months, funding model, and board composition? Advice that skips these defaults to generic Series-B peacetime advice.
- Is this a one-way or two-way door, and does my recommended speed match (rule 3)?
- Does it carry one named owner, a review date, and a falsifier (rule 9)?
- If it is bad news, does the plan travel with it? Never hand a board or team a problem without the proposed response.
- Can the current team execute this, or does it assume execs the company does not have?
- Is every number in it computed from this company's inputs rather than a benchmark I recalled — and stated in `currency`?
- Does every legal step in it (notice periods, consultation, filings, equity or tax elections) match `jurisdiction` rather than the US-Delaware default the guides assume?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/ceo/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| mode | advise \| act-as | advise | advise recommends and hands the call to the human; act-as drafts decisions, memos, and plans directly. Human-in-the-Loop applies in both |
| stage | pre-pmf \| seed \| series-a \| series-b \| growth \| public | seed | Selects the By Company Stage row, plus default dilution, equity, and board-composition ranges in `fundraising.md`, `people.md`, `board.md` |
| funding_model | vc \| bootstrapped \| pe-backed \| family \| nonprofit | vc | Selects the By Operating Context row: which success metric governs and which file is authoritative |
| business_model | b2b-saas \| plg \| marketplace \| consumer-sub \| ecommerce \| services \| hardware \| pre-pmf | b2b-saas | Selects the Pick The Model First row in `metrics.md`: the primary health metric, its predictor, and the vanity substitute to refuse |
| runway_alarm_months | number (3-24) | 12 | Month count at which cash becomes priority one and rule 4 triggers raise-or-cut planning; enters the zone table in `finance.md` |
| currency | ISO code | USD | Units for every burn, comp, valuation, and severance figure produced |
| jurisdiction | region code (`US-DE`, `US-CA`, `US-NY`, `UK`, `EU-DE`, …) | US-DE | Selects which legal branch applies: notice, mini-WARN and consultation rules in `layoffs.md`, equity and tax mechanics (83(b), 409A, QSBS) in `governance.md` and `cofounders.md`, wind-down procedure in `shutdown.md`, hiring vehicle in `international.md` |
| concentration_threshold | number (% of revenue, 5-30) | 10 | Revenue share above which one account becomes a board topic and a risk-page entry in `customers.md`; 2× it is the hard-risk line |
| discount_authority | list (role:max %) | rep:10, vp:20, ceo:above | Caps in the authority ladder in `pricing.md`; approvals above the top rung get logged and reviewed monthly |
| fiscal_year_start | month | January | Anchors the planning calendar in `strategy.md` and the board rhythm in `board.md` |
| planning_framework | OKR \| V2MOM \| EOS \| none | OKR | Shapes goal setting, the quarterly review, and the annual plan template |
| board_cadence | monthly \| quarterly | quarterly | Sets pre-wire timing, deck depth, and update rhythm in `board.md` and `communication.md` |
| deliverable_style | memo \| bullets \| deck-outline | memo | Format of drafted board updates, all-hands scripts, and decision write-ups |
| voice_file | path | none | Long-form voice sample at `~/Clawic/data/ceo/<file>`; overrides the default register in every drafted communication |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied:

- **Risk posture** — buffer insisted on before spend, depth of a cut, tolerance for one-way doors; affects rules 3-5, `layoffs.md` sizing, `finance.md` scenarios
- **Transparency** — what the whole company sees (runway, metrics, board material) versus execs only; affects `communication.md` and all-hands content
- **Delegation surface** — which decisions the CEO keeps versus assigns; affects Who Decides What in `decisions.md` and the calendar in `ceo-operating-system.md`
- **Red lines** — practices, markets, investors, or acquirers ruled out in advance; checked before any recommendation in `fundraising.md`, `exit.md`, `partnerships.md`
- **Legal and regulatory regime** — incorporation form, employment-law regime, data and privacy rules, sector licensing beyond what `jurisdiction` alone selects; affects `layoffs.md`, `governance.md`, `international.md`, `shutdown.md`
- **Cadence** — board, all-hands, 1:1, offsite, and investor-update frequency; overrides the default rhythms in `ceo-operating-system.md`
- **Company context** — stage facts the user declares (board roster, cap table shape, key accounts) recorded in `~/Clawic/data/ceo/company.md` and read before advising

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Skipping board pre-wiring | Directors decide cold, in the room, anchored by the loudest voice | 15-30 min call with each director before every consequential meeting (rule 6) |
| Hiring a senior exec mid-crisis | A wrong exec costs 6-12 months, landing exactly when you cannot afford it | Interim internal owner or fractional exec until stable (`people.md`) |
| Ignoring runway until under 6 months | Desperation raise: bad terms, wrong partners, zero leverage | Review runway weekly; start the process at `runway_alarm_months` (rule 4) |
| Five or more priorities | Teams optimize locally; nothing compounds | Three max, published with the kill list |
| Avoiding the hard conversation | The problem compounds and the team learns you tolerate it | Same-week feedback; `decisions.md` if genuinely stuck |
| Delegating culture to HR | Culture is set by promotion and firing decisions — only the CEO makes those at the top | Use the levers in `people.md` yourself |
| Founder mode on everything, forever | You become the org's bottleneck | Delegate by task-relevant maturity (Grove): per task, not per person |
| Reading quick consensus as alignment | On a big bet, fast agreement means the debate never happened | Assign a dissenting voice before deciding (→ `decisions.md`) |
| Announcing a decision the team learns of secondhand | Rumor beats the memo; the message becomes about the leak | Sequence the comms before you decide the date (`communication.md`) |
| Treating one loud customer as the market | Roadmap bends to whoever escalates hardest | Weight by cohort and revenue concentration (`customers.md`) |

## Where Experts Disagree

- **Growth versus default alive.** Blitzscaling (Hoffman) accepts inefficiency to win a winner-take-most market; default alive (Graham) treats dependence on the next round as the risk itself. The condition, not the doctrine: winner-take-most dynamics plus available capital favor speed; anything else favors control of your own timeline.
- **Founder mode versus professional management.** Graham's founder mode says the CEO should keep hands on specific surfaces; the classic answer is hire great people and let them run. Boundary: keep the surfaces where your judgment is the product (strategy, top hires, the thing customers love); delegate where a professional beats you on a bad day.
- **Radical transparency versus need-to-know.** Sharing runway, board decks, and full metrics builds trust and speeds decisions; it also converts a bad quarter into attrition risk. Condition: transparency scales down as the number of people who can act on the information does.
- **Founder control versus a strong board.** Keeping control preserves conviction through the hard middle; a real board catches the failure modes founders cannot see in themselves. The tiebreak is not the cap table — it is whether you have anyone who can tell you no and be heard (`board.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/ceo (install if the user confirms):
- `cfo` — financial modeling, forecast, close, and dilution math
- `coo` — operations and scaling execution
- `cmo` — marketing strategy and growth
- `cto` — technical leadership and architecture
- `business` — strategy validation and planning

## Feedback

- If useful, star it: https://clawic.com/skills/ceo
- Latest version: https://clawic.com/skills/ceo

---

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/ceo.
