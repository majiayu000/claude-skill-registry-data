---
name: proposal-builder
description: Build a proposal that closes, not a brochure. It opens with their problem in their words, scopes the solution to that problem, frames the price on the value it returns, states the terms plainly, and ends with one clear next step. Written to send, not to rewrite. Built for B2B sales teams, customizable to your CRM and your deal process. Trigger on "write a proposal", "build the SOW", "draft the quote", "turn this deal into a proposal", "make a proposal I can send", or any proposal or quote request.
---

# Proposal Builder

## What this does
Takes what you know about a deal and produces a proposal that moves it forward. It leads with the buyer's problem stated the way they stated it, scopes only the solution that solves it, frames the price against the value returned rather than a feature list, lays out the terms with no surprises, and closes on a single unambiguous next step. The output is written to send, not to be rebuilt from scratch.

## What you'll need
You do not need to connect anything to get value today. Bring the deal and the skill runs now. Connect the tools below and it pulls the context automatically and adds detail you cannot paste by hand.

- Works today with: what you paste about the deal. The problem they described, what you are proposing, the price, the term, and the next step you want. A short brief is enough to start.
- More powerful connected to a CRM: it reads the account, deal size, stage, and the contacts automatically, so the recap and the pricing match the real opportunity.
- Sharper with a meeting or email tool: pulls the buyer's own words on the problem and the outcome they wanted, so the recap sounds like them, not you.
- Sharper with a pricing or quoting record: pulls the accurate line items and terms, so the numbers are right the first time.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you tell it today and gets more powerful as you connect tools. It never invents a price, a term, or a promise it cannot see. A gap is a question it asks you, not a claim it makes up.

- **Bring your data**: paste the brief. The skill drafts the full proposal today on your real details. No connection required.
- **Connect your tools**: the same skill pulls the account, the quote, and the buyer's own words automatically. Same proposal, less effort, grounded in what was actually said.
- **Just exploring**: no live deal? Get the structure, the fields it reads, and a worked example on sample details, so you can see the shape before you bring a real one.

Every run ends with the one thing that would sharpen the next: a quote to confirm, a buyer quote to add, a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org selling scoped annual contracts. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| DEAL fields | account, size, stage, contacts | Opportunity.Amount, StageName, ContactRole |
| PRICING model | how you package and price | per-seat, per-usage, flat platform fee |
| VALUE metric | the outcome the price maps to | hours saved, pipeline added, cost avoided |
| TERM fields | length, start, payment terms | 12-month, net-30, start on signature |
| NEXT_STEP | the single action you want them to take | sign, book the kickoff, forward to procurement |
| BRAND | tone and format of the send | your template, your voice |

The value metric is yours. The skill frames the price against the outcome you choose, not a generic one.

## The method

### The problem recap (their words, not yours)
Open by restating the problem the buyer described, in language they would recognize as their own. This proves you listened and sets the frame the rest of the proposal answers to. If you cannot state their problem clearly, the proposal is not ready and the skill says so.

### The scoped solution (only what solves it)
Describe the solution as the answer to that problem, nothing more. Cut every feature that does not map to the problem you just recapped. Scope creep in a proposal reads as padding and slows the signature.

### Pricing framed on value (anchor to the outcome)
Present the price against the value it returns, not against a list of features. Tie the number to the VALUE metric the buyer cares about. The price should feel like the smaller number in a comparison the buyer already accepts.

### Terms, stated plainly
Lay out length, start date, payment terms, and anything that affects what they sign. No buried conditions. A term the buyer discovers late is a term that stalls the deal in legal.

### The one next step
End with a single, specific, dated action. Not "let us know your thoughts." One step, one owner, one date. A proposal with two next steps has none.

## Quality gates
- The problem recap uses the buyer's language where it is available, never a generic restatement.
- Every scoped item maps to the recapped problem; anything that does not is cut.
- The price is framed against a named value metric, never presented as a bare feature list.
- Terms are stated in full, with nothing that would surprise the buyer in legal review.
- The proposal ends with exactly one next step, with an owner and a date.
- Any number in the proposal is shown as given or sourced, never invented to look precise.

## Output (example)
```
PROPOSAL · Acme Corp (illustrative)

The problem you described
  Reps rebuild the same account research by hand before every call,
  and it is costing your team roughly a day a week each.

What we propose
  The workflow that pulls that research automatically, in the CRM
  your reps already live in. Nothing they have to learn separately.

Investment
  $60K / year. Against ~1 day/week/rep returned to selling, this
  pays back inside the first quarter (illustrative figure).

Terms
  12-month term, starts on signature, net-30. No usage caps.

Next step
  Sign by the 30th and we run kickoff the first week of next month.
```

## Where the inputs come from
The price, the payback, and the value figures above are examples, illustrative only, not a claim about your numbers. The problem recap and the buyer's words come from what you paste or from a connected meeting or email tool. The pricing and terms come from what you enter or from a connected quoting record. The skill states what it is given and asks for what it is missing; it does not manufacture a number to fill a gap.

## Example chat

**You:** Turn this into a proposal. Acme Corp, they told us reps burn a day a week rebuilding account research by hand. We're proposing the automated research workflow, $60K/year, 12-month, net-30, want signature by the 30th.

**Claude:** Drafted and ready to send.
```
PROPOSAL · Acme Corp (illustrative)

The problem you described
  Reps rebuild the same account research by hand before every call,
  costing the team roughly a day a week each.

Investment
  $60K / year. Against ~1 day/week/rep returned to selling, this
  pays back inside the first quarter (illustrative figure).

Terms
  12-month term, starts on signature, net-30. No usage caps.

Next step
  Sign by the 30th and we run kickoff the first week of next month.
```
Caught one thing: you gave me a price but no payback claim, so I framed the return off the day/week figure you gave me instead of inventing an ROI number. That is the gate this skill holds, price gets tied to a value metric you actually stated, never a bare number.

**You:** Good. Can you tighten the terms section, legal always finds something in there.

**Claude:** Tightened, nothing buried. Term, start, payment, and usage are now four flat lines with no conditional clauses hiding underneath. A term the buyer discovers late is a term that stalls in legal, so this version has nothing left for them to find. Sharpener: connect your quoting tool and I will pull the real line items instead of the flat number you typed.

## Go further
The manual version proves the shape works. Here is the scaled version once it does.

- **Draft on stage change.** Trigger this in Salesforce or HubSpot the moment a deal hits Proposal stage, so the draft is waiting before the AE opens it.
- **Pull the buyer's words automatically.** Connect Gong or your email tool so the problem recap comes from the call transcript, not a rep's paraphrase.
- **Route straight to send.** Wire the finished draft into your e-signature tool via a scheduled Claude task, so the AE reviews and sends instead of building from scratch.

The proposal still needs a human signature on the strategy. This just gets it to their desk faster.

## Make it yours
Fork it. Change the sections, the pricing frame, the value metric, the send format. The point is not to send someone else's template. It is to send yours, faster, grounded in what the buyer actually told you. Built by an operator. Customize it, break it, make it better.
