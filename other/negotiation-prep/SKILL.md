---
name: negotiation-prep
description: Walk into the negotiation with a plan, not a hope. Sets your walk-away and your target, builds the concession ladder (what you trade and what you get for it), maps their likely asks, and drafts the responses that protect price and terms. Built for B2B sales teams, customizable to your CRM and your deal process. Trigger on "prep me for this negotiation", "the prospect wants a discount", "what should I concede", "build my concession ladder", "hold price on a new deal", or any pre-negotiation planning.
---

# Negotiation Prep

## What this does
Turns a looming price conversation into a plan you can run. It fixes your target and your walk-away before the pressure sets in, lays out the order you trade concessions and what you ask for in return each time, predicts what the other side will push on, and gives you the words to hold the line. You leave knowing the floor you will not cross and the moves you will make above it.

## What you'll need
You do not need to connect anything to get value today. Bring the deal and the skill runs now. Connect the tools below and it pulls the context automatically and adds signals you cannot paste by hand.

- Works today with: what you paste about the deal. The price on the table, what they have asked for, the terms in play, who is in the room, and your own cost floor. A few sentences is enough to start.
- More powerful connected to a CRM: it reads the deal size, stage, close date, and history automatically, so the ladder is anchored to the real opportunity.
- Sharper with a meeting or email tool: pulls what the buyer actually said they cared about, so their likely asks are grounded, not guessed.
- Sharper with a pricing or quoting record: anchors the walk-away to your real discount floor, not a round number.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you tell it today and gets more powerful as you connect tools. It never invents a term or a number it cannot see. A gap is a question it asks you, not a guess it makes.

- **Bring your data**: paste the deal and the asks. The skill builds the full plan today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the deal, the history, and the stated priorities automatically. Same plan, less effort, better anchored.
- **Just exploring**: no live deal? Get the framework, the fields it reads, and a worked example on sample numbers, so you can see the shape before you bring a real one.

Every run ends with the one thing that would sharpen the next: a priority to confirm, a floor to set, a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org selling annual contracts. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| DEAL fields | size, stage, close date | Opportunity.Amount, StageName, CloseDate |
| PRICE_FLOOR | the discount you will not cross | 15% off list (set yours) |
| TARGET | the outcome you are steering to | list price, 12-month term |
| TRADE_LEVERS | what you can give that costs you little | term length, start date, case study, logo rights |
| ASK_FOR | what you request in return each time | signature date, multi-year, exec sponsor |
| WALK_AWAY | the point past which you stop | below floor and no term concession |

Your floor and your levers are yours. The skill plans the trades; it does not set your price.

## The method

### Walk-away and target (set both first)
Two positions before anything else. The TARGET is what you are steering to. The WALK_AWAY is the point past which the deal costs more than it earns. Everything in between is where you negotiate. Name both before the conversation so no in-room pressure quietly moves them.

### The concession ladder (trade, never give)
List what you can concede in order of least painful to most. For each rung, name what you ask for in return. Nothing moves for free. A discount buys a signature date. A longer term buys a better rate. If you cannot name what a concession buys you, it is not on the ladder yet.

### Their likely asks (anticipate, then answer)
Map what the other side will push on: price, payment terms, scope, timing, an exit clause. For each, draft the response that holds. The goal is that nothing they ask catches you deciding on the spot.

### Protect price and terms (the holds)
For the two or three things you will not move, write the sentence that holds them without ending the conversation. "I can't move the rate, but here is what I can do on the start date." A hold with an alternative is a hold that survives.

### Sequence and room (who, in what order)
Note who is in the room and who is not. Plan what you open with, what you hold back, and what you never put on the table unless asked. The first number anchors the range, so decide it on purpose.

## Quality gates
- No concession on the ladder without a named thing it buys you.
- Walk-away is set before the plan is built, never adjusted mid-plan to make a deal fit.
- Their likely asks are grounded in what they actually said where that is available, and flagged as assumption where it is not.
- Any number carried from the deal is shown with its source, never invented to look precise.

## Output (example)
```
NEGOTIATION PLAN · Acme Corp · $60K on the table (illustrative)
Target: list price, 12-month term, signature by month-end
Walk-away: below 15% off OR no term commitment

Concession ladder (trade, do not give):
  1. Flexible start date     -> ask: signature this week
  2. 10% off list            -> ask: 24-month term
  3. Add onboarding credit   -> ask: reference logo + case study
  (floor: 15% off, and only with a multi-year term)

They will likely ask:
  "Can you do 20% off?"  -> Hold. Offer the term-for-rate trade instead.
  "Net-60 payment"       -> Give, in exchange for the signature date.
  "Month-to-month"       -> Hold hard. This breaks the model.

Open with: list price, framed on the outcome, not the number.
```

## Where the inputs come from
PRICE_FLOOR, TARGET, and WALK_AWAY are yours to set. The 15% floor and the ladder rungs above are examples, illustrative only, not a recommendation for your business. The method does not change when your numbers do. Set the floor to your real economics and the ladder plans itself around it.

## Example chat
Here is the skill running on a real deal, start to finish.

**You:** Prospect wants 20% off. What's my plan going into this call?

**Claude:** Ladder built, holds drafted, floor set at 15%.
```
Concession ladder (trade, do not give):
  1. Flexible start date  -> ask: signature this week
  2. 10% off list         -> ask: 24-month term

They will likely ask:
  "Can you do 20% off?"  -> Hold. Offer the term-for-rate trade instead.
```
The catch worth naming: the plan holds 20% by offering a different trade, not by just saying no. A flat no invites another ask; a hold-with-an-alternative gives them something to react to instead of push against. That's the difference between protecting the floor and losing the room. One sharpener: connect your CRM so the walk-away is anchored to this deal's real discount floor instead of the 15% default I used.

## Go further
The plan is step one. Here is where an operator takes it once the manual version proves out.

- **Ground the floor in real deal history.** Pull closed-won discount data from Salesforce so the walk-away reflects what actually got approved on similar deals, not a round number.
- **Rehearse the holds before the call.** Run the likely-asks list through a scheduled Claude task that role-plays the buyer's pushback, so the responses are practiced, not improvised live.
- **Log what actually got traded.** After the call, write the real concession ladder used back to the opportunity record, so the next negotiation prep learns from what worked, not just what was planned.

You built the ladder once, now the next deal starts from what actually happened, not a blank page.


## Make it yours
Fork it. Change the levers, the floor, the order of the ladder. The point is not to run someone else's give-and-take. It is to walk in with yours already decided. Built by an operator. Customize it, break it, make it better.
