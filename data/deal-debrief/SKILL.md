---
name: deal-debrief
description: Run a real win/loss debrief on a single deal, not a shrug. It reconstructs what actually moved the deal, what nearly killed it, and the one repeatable lesson, then captures it so the next deal is run better instead of relearned the hard way. Built for B2B sales teams, customizable to your CRM and your deal process. Trigger on "debrief this deal", "why did we win", "why did we lose", "win/loss on this one", "what should we learn from this deal", or any single-deal retrospective.
---

# Deal Debrief

## What this does
Takes one closed deal, won or lost, and pulls the lesson out of it before it fades. It rebuilds the timeline from first touch to close, separates what actually moved the deal from what only felt important, names the moment it nearly died, and lands on a single repeatable lesson worth carrying to the next deal. Then it captures that lesson in a form the team can reuse, so the same mistake is not paid for twice.

## What you'll need
You do not need to connect anything to get value today. Bring the deal and the skill runs now. Connect the tools below and it pulls the history automatically and adds detail you cannot paste by hand.

- Works today with: what you paste about the deal. How it started, what happened along the way, why it closed the way it did, and who was involved. Your own recollection is enough to start.
- More powerful connected to a CRM: it reads the stage history, close date, amount, and the activity trail automatically, so the timeline is real, not remembered.
- Sharper with a meeting or email tool: pulls what was actually said at the turning points, so the debrief is grounded in the record, not the story you tell yourself.
- Sharper with a product-analytics tool: on trials, shows whether usage matched the story the deal told.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you tell it today and gets more powerful as you connect tools. It never invents an event or a cause it cannot see. A gap is a question it asks you, not a fact it makes up.

- **Bring your data**: paste the deal story. The skill runs the full debrief today on what you remember. No connection required.
- **Connect your tools**: the same skill pulls the stage history, the activity, and the turning-point conversations automatically. Same debrief, less effort, grounded in the record.
- **Just exploring**: no deal to debrief? Get the framework, the fields it reads, and a worked example on a sample deal, so you can see the shape before you bring a real one.

Every run ends with the one thing that would sharpen the next: a date to confirm, a conversation to attach, a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org running a staged pipeline. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| STAGE history | how you see the deal's path | Opportunity stage history, close date |
| OUTCOME field | won, lost, or no-decision | StageName, Closed Won / Closed Lost |
| LOSS_REASON field | why it closed the way it did | Loss Reason, Competitor field |
| ACTIVITY sources | where the touch trail lives | Task, Event, meeting or email tool |
| CAPTURE target | where the lesson is written | your notes, a shared doc, a deal wiki |
| LESSON_SCOPE | how broadly a lesson should apply | this rep, this segment, the whole team |

The point is one lesson you will actually reuse, not a form nobody reads. Set the capture target to where your team will actually see it.

## The method

### Reconstruct the timeline (what happened, in order)
Lay the deal out from first touch to close: the stages, the dates, the key conversations, the moments something changed. Use the record where you have it. A debrief built on memory alone remembers the story, not the deal.

### What actually moved it (separate cause from noise)
Name the two or three things that genuinely moved the deal toward its outcome. Strip out what felt important at the time but changed nothing. A win from a warm intro is a different lesson than a win from a great demo. Be honest about which it was.

### What nearly killed it (the near-death moment)
Every deal has a moment it almost went the other way. Name it. What caused it, what recovered it or failed to, and whether you saw it coming. This is usually where the real lesson lives.

### The one repeatable lesson (single, portable)
Land on exactly one lesson that would change how the next deal is run. Not five. One, stated so plainly that another rep could apply it without you in the room. If you cannot say it in a sentence, it is not the lesson yet.

### Capture it (so it is not relearned)
Write the lesson where the team will actually find it, tagged to the situation it applies to. A lesson that lives only in one rep's head gets paid for again by the next rep. Capture turns one deal's cost into everyone's edge.

## Quality gates
- The timeline is built from the record where it is available, and clearly marked where it rests on memory.
- What moved the deal is separated from what only felt important, honestly, even when the honest answer is luck.
- The debrief lands on exactly one repeatable lesson, stated portably, not a list of five.
- Loss reasons name what actually happened, never a tidy category that hides it.
- Any date or amount carried from the deal is shown as given or sourced, never invented.

## Output (example)
```
DEAL DEBRIEF · Acme Corp · CLOSED WON · $60K (illustrative)

Timeline
  Day 0    Inbound from a webinar
  Day 12   Demo to VP Ops (the eventual champion)
  Day 34   Stalled in legal for 3 weeks
  Day 61   Signed after an exec-to-exec call

What actually moved it
  1. The champion sold it internally while we were out of the room.
  2. The exec call broke the legal stall. The demo did not close it.

What nearly killed it
  The legal stall. We had no second thread and no exec sponsor until
  day 55. We got lucky the champion held on.

The one repeatable lesson
  Line up the exec sponsor before legal, not after the stall. Waiting
  cost us three weeks and nearly the deal.

Captured to: team deal wiki, tagged "mid-market, legal stall"
```

## Where the inputs come from
The dates, the amount, and the account above are examples, illustrative only, not a real deal. The timeline and the turning points come from what you paste or from a connected CRM, meeting, or email tool. The lesson is yours to write; the skill forces it down to one and asks for the record behind it. It does not invent an event to make the story cleaner.

## Example chat
Here is the skill running on a real closed deal, start to finish.

**You:** Debrief the Acme deal. We just closed it and I want to know what actually worked before I forget.

**Claude:** Rebuilt the timeline from the CRM stage history and your recap.
```
DEAL DEBRIEF · Acme Corp · CLOSED WON · $60K (illustrative)
What actually moved it: the champion sold it internally while we were out
of the room; the exec call broke a 3-week legal stall.
What nearly killed it: the legal stall. No second thread until day 55.
```
The one repeatable lesson: line up the exec sponsor before legal, not after the stall.

**You:** Capture that so the team actually sees it.

**Claude:** Wrote it to the deal wiki, tagged "mid-market, legal stall," so the next rep hitting a legal stall finds this before repeating it. One sharpener: connect the meeting tool so next debrief pulls the actual exec-call quote instead of your recollection of what got said.

## Go further
The read is step one. Here is where an operator takes it once the manual version proves out.

- **Trigger a debrief on every closed deal automatically.** Wire a scheduled Claude task to fire whenever an opportunity flips to Closed Won or Closed Lost in Salesforce.
- **Surface past lessons before the next deal starts.** Connect the deal wiki to your CRM so a rep entering a similar deal sees prior lessons tagged to that situation.
- **Pull the turning-point quotes automatically.** Connect Gong so the near-death moment gets the actual transcript excerpt instead of a paraphrase.

One deal's cost, captured once, becomes the whole team's edge.

## Make it yours
Fork it. Change the structure, the loss categories, where the lesson gets captured. The point is not to fill in someone else's win/loss form. It is to make sure the next deal is run better than this one. Built by an operator. Customize it, break it, make it better.
