---
name: cs-health-report
description: Roll up the health of a customer book or segment into moves, not colors. At-risk accounts, renewals due, expansion candidates, and the accounts quietly going dark, each with the one move it needs. Built for B2B customer success teams, customizable to your data and your book. Trigger on "how's my book", "customer health report", "which accounts in my book need attention", "what's up for renewal", "who's going quiet", or any book-health diagnostic.
---

# Customer Health Report

## What this does
Reads a book of accounts and sorts them into the four groups a CSM works from: at risk, renewing soon, ready to expand, and going quiet. Every account that surfaces comes with the one move that changes its trajectory. It is a health rollup that ends in outreach, not a grid of green and red.

## What you'll need
You do not need to connect anything to get value today. Bring your accounts and the skill runs now. Connect the tools below and it pulls them automatically and adds signals you cannot paste by hand.

- Works today with: a list of your accounts, with renewal date, contract value, last activity date, and a health signal or usage figure if you have one. Paste it or upload a CSV.
- More powerful connected to a CRM: it reads the whole book automatically, renewal dates and values included.
- Sharper with a product-analytics tool: adds real usage momentum, so at-risk is behavior, not a guess.
- Sharper with a meeting or email tool: tightens the going-quiet check with real last-touch dates.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a number it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your book (an account export, a renewal CSV). The skill runs the full rollup today on your real numbers. No connection required.
- **Connect your tools**: the same skill pulls the book automatically and adds signals you cannot paste by hand (usage trend, live activity, renewal history). Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org running recurring-revenue accounts. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, a CS platform |
| VALUE field | contract or account value | ARR, MRR, contract value |
| RENEWAL field | when the contract renews | renewal date, term end |
| HEALTH signal | how you read account health | a health score, usage, support load |
| USAGE source | where product momentum lives | a product-analytics tool |
| RENEWAL window | days out that means act now | 90 (re-tune to your cycle) |
| QUIET_DAYS | no-contact days that mean going dark | 30 (re-tune) |

Run any health model you like. The skill sorts your book against your own signals and thresholds, so point it at your fields, not anyone else's.

## The method

### At-risk accounts
An account is at risk when the signals turn: usage falling, support load rising, a health score dropping, a key contact gone. Rank by value at risk, not by count, so the biggest exposure leads. Name why, from a signal you can see.

### Renewals due
Every account inside the renewal window, sorted by date then value. A renewal is not safe because it is far away and not lost because it is close. Show days to renewal and the health signal together, so risk and timing sit on one line.

### Expansion candidates
Accounts healthy and using the product hard enough to grow. Strong usage plus headroom is an expansion signal. Surface the few worth a real conversation, not every green account.

### Going quiet
Accounts with no contact past QUIET_DAYS. Silence before a renewal is the risk that hides, because nothing looks wrong until it is too late. Show days dark and the next date that matters.

### The one move
Each surfaced account gets a single move: book the renewal conversation, run a usage review, open the expansion talk, re-engage a quiet champion. One move per account beats a plan nobody runs.

## Quality gates
- At-risk ranks by value at risk, never by a raw count of flags.
- No "at risk" without naming the signal that turned. A color is not a reason.
- Renewals show days-to-renewal and a health signal on the same line.
- Every surfaced account carries exactly one move, owned and specific.

## Output (example)
```
BOOK HEALTH · 24 accounts, $1.4M ARR
At risk (by value)   3 accounts, ~$180K
  Acme Corp   $90K   usage down 40% over 6 weeks, champion left
  Vertex      $55K   support tickets up, health score falling

Renewals due (90d)   5 accounts, ~$310K
  Blend Labs  $70K   renews in 22d, health steady
  Northwind   $48K   renews in 61d, usage soft

Expansion candidates 2 accounts
  Orbit Inc   $60K   power usage + seats near cap

Going quiet          4 accounts, no contact 30d+
  Delta Co    $32K   dark 44d, renews in 75d

Moves
  1. Acme Corp: book a save conversation this week, name a new champion.
  2. Delta Co: re-open contact before the renewal clock runs down.
  3. Orbit Inc: open the seat-expansion talk on the next call.
```
(Figures illustrative.)

## Where the numbers come from
The renewal window (90 days) and QUIET_DAYS (30) are defaults, not laws. They suited a mid-market SaaS book on annual terms. If your terms are monthly, shorten both. If they run multi-year, widen them. The logic does not change. The thresholds are yours.

## Example chat
Here is the skill running on a real CSM book.

**You:** How's my book looking, 24 accounts?

**Claude:** Rolled up. Your biggest risk isn't the account you'd expect.
```
At risk (by value)   3 accounts, ~$180K
  Acme Corp   $90K   usage down 40% over 6 weeks, champion left
  Vertex      $55K   support tickets up, health score falling

Going quiet          4 accounts, no contact 30d+
  Delta Co    $32K   dark 44d, renews in 75d
```
Acme leads by value at risk, not by a flashing red flag, that's why ranking by dollars instead of raw count matters. Delta Co is the quieter danger: nothing looks broken because the renewal is still 75 days out, but 44 days of silence before a renewal is exactly the pattern that hides until it's too late. One sharpener: connect a product-analytics tool so "usage down 40%" becomes a real trend line instead of a single snapshot comparison.

**You:** Give me the one move for each of those two.

**Claude:** One move apiece, not a plan to triage.
```
1. Acme Corp: book a save conversation this week, name a new champion.
2. Delta Co: re-open contact before the renewal clock runs down.
```
Acme needs a new relationship, not just a check-in, since the champion who left was likely the account's only real advocate. Delta just needs the silence broken now, while there's still runway before the renewal date. One sharpener: connect a meeting tool so "re-open contact" can suggest the actual best contact to reach, not a guess at who's still there.

## Go further
The read is step one. Here's where an operator takes it once the manual version proves out.

- **Refresh the whole book every Monday, automatically.** Point a scheduled Claude task at Salesforce and Amplitude weekly and post the four groups to the CSM team channel before standup.
- **Catch the quiet ones before they go dark.** Set the going-quiet check to fire the moment an account crosses the threshold, not on a weekly cadence, via a Slack alert to the account owner.
- **Turn the moves into sent outreach.** Chain this into comms-agent so "book a save conversation" becomes a drafted email or calendar hold, not just a line on a list.

You built the read once; now it runs itself.


## Make it yours
Fork it. Change the windows, the health signals, the fields. The point is not to run someone else's playbook. It is to run yours, faster. Built by an operator. Customize it, break it, make it better.
