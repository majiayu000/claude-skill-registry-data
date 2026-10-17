---
name: stackadapt-bidding-and-budgets
description: Choose and configure the bid strategy, budget, and pacing for a StackAdapt ad group. Use for StackAdapt bidding, StackAdapt bid strategy, automated bidding on StackAdapt, StackAdapt budget, StackAdapt pacing, maximum bids, target CPA or target CPC, maximize delivery, and in-flight budget management, including which bid type matches awareness, traffic, engagement, or conversion goals.
---

# StackAdapt bidding and budgets

Match the bid approach to the objective, size the budget so the bid can learn, and pace it so the
flight delivers in full without front-loading. StackAdapt is a self-serve multi-channel
demand-side platform (native, display, video, connected TV, audio, in-app, and digital
out-of-home). On StackAdapt the ad group is the line item, so bid, budget, and pacing are all set
per ad group.

This skill owns the bid, budget, and pacing decision. For where these sit in the build order, see
the `stackadapt-campaign-setup` skill. For the audience the bid competes for, see the
`stackadapt-targeting-and-audiences` skill. For CPM, CPC, CPA, ROAS, and pacing-index math, see
the `programmatic-foundations` skill. For reading whether the bid is hitting goal, the
`reporting-by-campaign-goal` skill gives the by-objective report recipes.

## When to use this skill

- "Which bid strategy should I use on StackAdapt?" / "Automated or manual bidding?"
- "Set a target CPA / target CPC." / "Should I let it maximize delivery?"
- "What maximum bid should I set?"
- "Set the budget and pacing for this ad group." / "Daily or lifetime budget?"
- "My campaign is under-pacing / spending too fast / blowing through budget."
- "How do I manage budget in flight?"

Boundary with sibling skills. This skill decides the bid, the budget number, and the pacing mode.
It does not decide the audience (`stackadapt-targeting-and-audiences`) or diagnose deep delivery
failures once setup is correct (`stackadapt-optimization-and-troubleshooting`).

## Quick reference

Pick the bid type from the objective and the signal you have:

| Objective | Bid type | Optimizes toward | Use when |
| --- | --- | --- | --- |
| Awareness / reach | CPM | Impressions delivered | Brand, reach, video, CTV, audio, DOOH |
| Traffic | CPC | Clicks to site | Drive site visits, lower-funnel native or display |
| Engagement | CPE | Post-click content engagement | Content, blog, and video where dwell matters |
| Conversions | Target CPA (automated) | Conversions at a cost target | Pixel events are live and accruing |
| Conversions / value | Goal-based automated (CPC or CPA goal) | The KPI you set, bid managed by the model | You want the model to chase a defined KPI |
| Spend the budget | Maximize delivery | Fullest delivery for the budget | Fixed budget, secondary CPA sensitivity |

Two control modes sit on top of the bid type:
- Manual or fixed bid: you set the price, you keep hard control, the model does not move it.
- Automated or smart bidding: the model sets each bid in real time toward the goal and KPI you
  defined. It needs signal (conversions for CPA) and budget room to learn.

A maximum bid caps what any single auction bid can reach. Budget and pacing then govern how that
spend is spread across the flight.

## Core process

1. Read the objective off the campaign. Awareness, traffic, engagement, or conversions was set at
   the campaign level (see `stackadapt-campaign-setup`). The objective is what makes one bid type
   correct and the others wrong, so start there.
2. Pick the bid type from the table. CPM for awareness, CPC for traffic, CPE for engagement,
   target CPA for conversions. The campaign automatically optimizes toward the goal you choose, so
   the bid type is also a statement of what "good" means for this ad group.
3. Choose manual or automated control. Use a fixed or manual bid when you need hard price control,
   when volume is too low for a model to learn, or at launch before there is conversion signal.
   Use automated or smart bidding when the objective is conversions, the pixel is firing enough
   events, and you want the model to set each bid toward the target. Do not put a brand-new
   conversion ad group straight onto target CPA with no events; it has nothing to learn from.
4. Set the target only when automated. For target CPA, set a CPA the economics can bear and that
   recent performance suggests is reachable, not an aspirational number the model cannot hit. An
   unreachable target starves delivery because the model will not bid. If you have no history,
   start on a fixed bid, gather data, then switch.
5. Set a maximum bid. Cap the per-auction bid so a thin-supply moment cannot overpay. Set it high
   enough not to choke delivery but low enough to protect efficiency. Too low a max bid is a
   common cause of under-delivery.
6. Set the budget on the ad group. The ad group is the budget container, so the number lives here,
   not on the campaign. Use a daily budget for always-on, steady delivery; use a lifetime or total
   flight budget when the total is fixed and you want the system to spread it. Give automated
   bidding enough budget to clear the daily auctions it needs to learn; a starved budget keeps a
   smart bid stuck in learning.
7. Set pacing. Even pacing spreads spend across the flight and is the default for always-on and
   brand work. Accelerated pacing spends as fast as auctions allow, for short, time-boxed pushes
   only, and you must watch for early budget exhaustion. Match pacing to whether the goal is steady
   presence or fast volume.
8. Manage in flight. Check the pacing index (delivered vs expected for the flight to date) and
   cost vs goal on a regular cadence. The Suggestions Hub recommends optimizations based on the
   bid type and goal you set, including a concrete suggested bid value when it advises raising or
   lowering a bid, and can flag domains to exclude. Act on under- or over-delivery early, while
   there is still flight left to correct.

## Decision rules and thresholds

- Bid type follows the objective, not preference. Awareness is CPM, traffic is CPC, engagement is
  CPE, conversions is target CPA. If the requested bid type contradicts the objective, fix the
  objective or the bid type before launch.
- Fixed bid at cold launch, automated once signal exists. A conversion ad group with no pixel
  events cannot run a productive target CPA. Start fixed, let events accrue, then move to
  automated. Switching too early traps the model in learning.
- Set a target CPA the data can reach. The model only bids when it can plausibly hit the target,
  so an unreachable CPA reads as under-delivery. Anchor the target to recent actual CPA, then
  tighten gradually.
- A maximum bid that is too low throttles delivery. If an ad group under-delivers, check the max
  bid before blaming targeting or budget; raise it if it is clipping winnable auctions.
- Budget lives on the ad group. Set and control spend per ad group. The campaign is not the budget
  container on StackAdapt.
- Give automated bidding room to learn. Too small a daily budget keeps a smart bid in learning and
  hurts performance. Fund enough daily auctions, or widen the audience, before concluding the bid
  strategy failed.
- Even pacing by default, accelerated only for bursts. Even pacing for always-on, brand, and
  steady delivery. Accelerated for short, time-sensitive pushes, and monitor for early exhaustion.
- One change at a time in flight, then let it settle. Automated bids need a learning window after a
  target or budget change. Stacking several edits at once makes the result unreadable; change one,
  give it time, then reassess.
- Read pacing and cost-to-goal together. On pace but over CPA, or under CPA but under-pacing, are
  different problems with different fixes. Check both before acting.

## Templates and examples

Three ad groups in one campaign, each matched to its objective:

```
Ad group: ACME_CTV_Awareness_2026Q3
  Objective:  Awareness / reach
  Bid type:   CPM, fixed
  Max bid:    set to plan CPM ceiling
  Budget:     $20,000 lifetime over the flight (ad-group level)
  Pacing:     Even
  Why:        Reach goal, so price impressions on a fixed CPM and spread evenly
              across the flight for steady presence.

Ad group: ACME_Native_Traffic_2026Q3
  Objective:  Traffic
  Bid type:   CPC, automated once clicks stabilize
  Max bid:    cap above expected winning CPC, not at it
  Budget:     $300/day (ad-group level)
  Pacing:     Even
  Why:        Goal is site visits; start manual CPC, move to automated CPC goal
              once volume is steady so the model optimizes clicks.

Ad group: ACME_Display_Conversions_2026Q3
  Objective:  Conversions
  Bid type:   Fixed CPC for the first ~1-2 weeks, then Target CPA
  Target CPA: anchored to recent actual CPA, tightened gradually
  Max bid:    set so it does not clip winnable conversion auctions
  Budget:     $500/day, enough to clear daily auctions for learning
  Pacing:     Even
  Why:        Pixel events must accrue before target CPA can learn; launch fixed,
              switch to target CPA once events are flowing, fund learning.
```

In-flight adjustment example:

```
Symptom:  Conversion ad group is at 60% of expected pace mid-flight, CPA on goal.
Read:     Delivery problem, not an efficiency problem (CPA is fine).
Action 1: Raise the maximum bid; a low cap is the usual delivery throttle.
Action 2: If still short, widen audience (see targeting skill) or raise budget so
          the smart bid has more auctions to learn from.
Then:     Change one lever, let the learning window pass, recheck pace and CPA.
```

## Common pitfalls

- Putting a brand-new conversion ad group straight on target CPA with no pixel events, so it has
  nothing to learn from and barely delivers. Launch on a fixed bid first.
- Setting an aspirational target CPA the data cannot reach, then reading the resulting
  under-delivery as a targeting problem. Anchor the target to actual recent CPA.
- A maximum bid set too low, quietly throttling delivery. Check the cap first when an ad group
  under-delivers.
- Starving automated bidding of budget, trapping it in learning, then blaming the strategy. Fund
  enough daily auctions.
- Setting budget or pacing on the campaign and expecting it to control the ad group. Budget and
  pacing live on the ad group on StackAdapt.
- Leaving accelerated pacing on for an always-on flight, then exhausting the budget early. Use even
  pacing unless it is a deliberate short burst.
- Stacking several in-flight changes at once so the learning signal is unreadable. One change, let
  it settle, then reassess. For persistent delivery failures after setup is correct, hand off to
  `stackadapt-optimization-and-troubleshooting`.

## Sources

- [How to Run a Successful Native Advertising Campaign | StackAdapt](https://www.stackadapt.com/resources/blog/how-to-run-a-successful-native-advertising-campaign) (as of June 2026)
- [Optimize Your Campaigns With Suggestions Hub | StackAdapt](https://www.stackadapt.com/resources/blog/suggestions-hub) (as of June 2026)
- [StackAdapt Developer Documentation (REST, GraphQL, Pixel API, Data Taxonomy, MCP Server)](https://docs.stackadapt.com) (as of June 2026)

The exact in-product bid-strategy menu (the precise labels for automated and goal-based bidding),
the maximum-bid field, daily versus lifetime budget controls, and the even versus accelerated
pacing toggle are documented in the StackAdapt help center. Some help center articles require a
logged-in account, so they are not cited here; where a specific in-product control, label, or
default is not publicly documented, the guidance above states the operational best practice
rather than a fabricated citation. For account-level help, see the StackAdapt help center at
support.stackadapt.com.
