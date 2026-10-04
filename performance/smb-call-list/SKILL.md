---
name: smb-call-list
version: 1.0.0
description: Rank the top-5 leads worth calling today with tailored, history-grounded talking points and proposed calendar blocks — no auto-send.
author: matrixx0070
tags: [sales, crm, leads, outreach, productivity, prioritization]
capabilities: []
---

# Call List

## When to use
Use this when you start the day and want a focused call list instead of a cluttered pipeline. It surfaces the five leads most likely to move, arms you with what to say, and reserves time to dial.

**Not for:** first-touch scoring of raw inbound (use smb-lead-triage), or bulk CRM hygiene (use smb-crm-cleanup). This assumes leads already exist in the CRM with some history.

## Method
1. Pull open leads and deals from the CRM: last-contact date, deal value, stage, and recent activity (email replies, site visits, form fills).
2. Score each on freshness, intent signals, deal size, and stall risk. Decision point: prefer warm-but-cooling leads (had contact, going quiet) over cold ones with no signal.
3. Select the top five. For each, draft three talking points grounded in real history. Decision point: if a fact is missing, say "no record of X" — never invent a detail.
4. Propose 2-3 calendar blocks that fit around existing meetings, clustering calls to protect focus time.
5. Confirm the blocks with the owner before writing anything to the calendar. Do not send emails or log outreach automatically.

## Example
Lead: Dana Reyes, Northside Dental. Why-now 8/10 — opened your quote email twice this week, deal $14k, stalled 9 days in Proposal. Talking points: (1) reference her question about the 12-month plan, (2) the Q3 install slot she asked about is still open, (3) no record of pricing objection — ask directly. Suggested block: today 10:00-10:30.

## Pitfalls
- **Inventing rapport.** Fabricated "we last spoke about..." details get caught on the call and burn trust — cite only logged facts.
- **Ranking by deal size alone.** A huge cold lead beats a warm mid-size one on paper but not in reality; weight intent.
- **Writing to the calendar unasked.** Always propose blocks and wait for a yes.
- **Over-long lists.** Six-plus "priority" calls means none are; hold the rest in a warm queue.

## Output format
```
Call these 5 today:
1. <name>, <company> — why-now <n>/10 — last contact <date> — deal $__
   - <talking point 1>
   - <talking point 2>
   - <talking point 3>
[...2-5]

Suggested call blocks:
  - <day> <start>-<end>
"Approve these blocks and I'll add them to your calendar."
```

## Reference

### Why-now scoring model (0-10)
Score every open lead on four weighted factors, then rank. This is the engine behind the "why-now n/10" line:

| Factor | Weight | What earns points |
|---|---|---|
| Intent signal | 40% | Opened/clicked your last email, replied, visited pricing page, booked a demo, asked a buying question |
| Stall risk (cooling) | 25% | Was engaged, now going quiet — the "warm-but-cooling" sweet spot; a deal past its avg stage-time scores highest |
| Deal value | 20% | Size relative to your average deal — normalize, don't let one whale dominate |
| Freshness | 15% | Days since last contact; the 24-72h window after a signal is prime, cold >30d scores near zero |

Compute each factor 0-10, multiply by weight, sum. Example: intent 9, stall 8, value 6, fresh 7 → (9×.4)+(8×.25)+(6×.2)+(7×.15) = 3.6+2.0+1.2+1.05 = **7.85 → 8/10**.

### Speed-to-lead and connection benchmarks
- **Call new inbound within 5 minutes** — contact odds drop roughly 8x after 30 minutes and ~10x after the first hour. Fresh form-fills should jump the queue.
- **Best connect windows:** mid-morning ~10-11am and late afternoon ~4-5pm local; worst is right after lunch (1-2pm) and first thing Monday.
- **Persistence:** it takes on average 5-8 dial attempts to reach a prospect, yet most give up after 2. Spread attempts across different days and times before marking "no answer."
- **Voicemail:** leave a message roughly every other attempt, keep it under 20 seconds, and always state a specific reason to call back.

### Talking-point construction (grounded only)
Each of the three points must trace to a logged fact. Use this pattern:
1. **Reference** — a specific prior interaction ("You asked about the 12-month plan on the 3rd").
2. **Value/next step** — something concrete that moves it ("The Q3 install slot you wanted is still open").
3. **Open question** — surface the real blocker ("No record of a pricing objection — is budget the holdup, or timing?").
If a fact is missing, write "no record of X" and turn it into a question. Never fabricate a prior conversation.

### Objection quick-reference
- **"Too expensive"** → reframe to cost-of-inaction or unit economics, don't discount reflexively. Ask what they're comparing against.
- **"Need to think about it"** → isolate the real concern: "Is it the price, the timing, or something about the fit?"
- **"Send me info"** → agree, but book the follow-up call before hanging up ("I'll send it today — can we grab 15 minutes Thursday to walk through it?").
- **"Not right now"** → get a specific date to reconnect and log it; a vague "later" is a lost lead.

### Call-block hygiene
Batch dials into 30-60 minute blocks (call momentum is real — the 4th call is better than the 1st). Cap at 5 priority calls; hold overflow in a named "warm queue" rather than pretending everything is priority. Propose blocks around existing calendar events and cluster them; leave a 5-minute gap between calls for notes.

### Owner-approval gate
This skill proposes calls and calendar blocks only. It never dials, sends an email, or writes to the calendar until the owner approves the blocks. Logging outreach happens after the call actually occurs, at the owner's direction.
