---
name: churn-analysis
description: Turn churned and downgraded accounts into an early-warning system. Reads the customers who left or shrank, extracts the themes behind why, builds a warning checklist from the real causes, then reads your active book and flags which accounts look like the ones that just churned. Built for B2B retention teams, customizable to your CRM and your customer data. Trigger on "why do customers churn", "what do churned accounts have in common", "build me a churn early-warning list", "which accounts are at risk of churning", "who looks like a recent churner", or any retention post-mortem.
---

# Churn Analysis

## What this does
Reads your churned and downgraded accounts and pulls out why they left: the themes, the shared conditions, the moments it started slipping. It turns those causes into an early-warning checklist, then runs that checklist across your active book and flags the customers who look like the ones that just walked. The point is not a churn number for the board. It is a short list of current accounts to save while there is still time.

## What you'll need
You do not need to connect anything to get value today. Bring your churned accounts and the skill runs now. Connect the tools below and it pulls them automatically and adds signals you cannot paste by hand.

- Works today with: a list of your churned and downgraded accounts, with segment or size, contract value, tenure, churn or downgrade date, the reason (if captured), and any renewal notes. And, if you have it, a list of your active accounts to score against. Paste it or upload a CSV.
- More powerful connected to a CRM: it reads churn, downgrades, renewal dates, and notes automatically, across the whole book.
- Sharper with a product-analytics tool: adds usage decline, the single strongest churn tell, so a quiet account gets caught before the renewal call.
- Sharper with a support or ticketing tool: adds ticket volume and sentiment, so a frustrated account surfaces early.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a churn reason it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your churned-account list (a CRM export, a churn CSV). The skill runs the full analysis today on your real accounts. No connection required.
- **Connect your tools**: the same skill pulls the data automatically and adds signals you cannot paste by hand (usage decline, ticket sentiment, renewal history). Same output, less effort, sharper.
- **Just exploring**: no data yet? Get the framework, the exact fields it reads, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a field to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org with recurring subscriptions. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| CHURN filter | how you mark a loss of revenue | Status = Churned OR downgraded |
| WINDOW | the churn-date range to analyze | trailing 4 quarters |
| REASON field | your churn-reason picklist | Churn Reason |
| NOTES field | free-text renewal or churn notes | renewal notes, save-attempt notes |
| VALUE field | contract or recurring value | ARR, MRR |
| TENURE field | how long they were a customer | months since first close |
| USAGE source | product engagement over time | logins, active seats, key events |
| MIN_SAMPLE | fewest churns before a theme counts | 5 (raise if you churn a lot) |

Run any churn taxonomy you like. The skill groups your churn into your themes and scores your active book against them, so point it at your fields, not anyone else's.

## The method

### Churn theme extraction
Group every churned and downgraded account across reason, segment, tenure, value, and (if connected) usage. Report only the themes that clear MIN_SAMPLE. For each theme, show the share of churn, the revenue behind it, and the average tenure at churn, so a high-count theme and a high-dollar theme are both visible. Treat a downgrade as churn's early cousin, not a separate story: the same causes usually run underneath.

### Cause vs symptom
Separate what you can see from what actually drove it. A dead login count is a symptom. The cause is usually one of a few things: the champion left, the value was never realized, onboarding stalled, a merger or budget cut hit, or a competitor displaced you. Name the cause, because the checklist has to catch the cause early, not the symptom at renewal.

### Early-warning checklist
Turn the top causes into a short list of observable signals that appear before churn, not at it: usage down X percent over N weeks, champion gone quiet or departed, no executive contact in the last quarter, support tickets spiking, a renewal inside 90 days with no engaged buyer. Each signal is something you can check on a live account today.

### Predictive read (active book)
Run the checklist across your active accounts and score each one by how many warning signals it hits. Return a ranked watchlist, highest risk first, with the exact signals each account trips and how closely it resembles a specific churn theme. This is the payoff: the accounts to save this quarter, named, before the renewal call.

## Quality gates
- No theme reported below MIN_SAMPLE. One angry cancellation is not a pattern.
- Usage-decline claims show the trend, not a single reading. A quiet week is not churn.
- Every at-risk account lists the specific signals it trips, never just a risk score.
- Cause is grounded in a field, a note, or a usage trend, never assumed from the logo.

## Output (example)
```
CHURN ANALYSIS · 23 churned + downgraded, trailing 4 quarters

Churn themes
Theme                        Share   Revenue    Avg tenure
Champion left, no backup     35%     $180K      14 months
Never reached first value    26%     $130K      7 months
Price at renewal             22%     $95K       22 months
Merger / budget cut          17%     $70K       19 months

Early-warning checklist (the signals that came first)
  [ ] Usage down 40%+ over trailing 8 weeks
  [ ] Champion departed or dark 60+ days
  [ ] No exec contact in the last quarter
  [ ] Renewal inside 90 days, no engaged buyer
  [ ] Support tickets spiking

Active accounts that look like recent churners (highest risk first)
Account      Signals tripped                 Resembles
Kestrel Co   usage -52%, champion dark        "champion left"
Alderman     onboarding stalled, low usage    "never reached value"
Pentworth    renewal in 60d, no buyer         "price at renewal"

Next move:
  1. Kestrel. Find a second champion now. The first one is gone.
  2. Alderman. Restart onboarding before renewal. It never got to value.
  3. Add a usage feed. It is your single strongest early tell and it is missing.
```

## Where the numbers come from
MIN_SAMPLE (5), the trailing-4-quarter window, and the usage-decline cutoffs are defaults, not laws. They suited a subscription business with steady churn volume. If you churn a small number of large accounts, widen the window so the themes are not built on a handful of exits. Usage thresholds should match your product's natural rhythm: a weekly tool and a quarterly tool decline differently. The checklist is always built from your own churn, so it warns you about your accounts, not a benchmark's.

## Example chat
**You:** We lost 23 accounts over the last year. What do they actually have in common? Here's the export. [pastes CSV]

**Claude:** Four real themes, not a grab-bag of reasons.
```
Theme                        Share   Revenue    Avg tenure
Champion left, no backup     35%     $180K      14 months
Never reached first value    26%     $130K      7 months

Active accounts that look like recent churners
Account      Signals tripped                 Resembles
Kestrel Co   usage -52%, champion dark        "champion left"
```
The payoff isn't the churn report, it's Kestrel. It hits two of the same warning signals that show up before "champion left, no backup" churn, and it's still active. That's a save attempt you can make this week instead of a postmortem you write in six months.

**You:** What should the team actually check on Kestrel right now?

**Claude:** Find a second champion before the current one is fully gone, that's the exact gap the "no backup" theme names. One sharpener: connect your product-analytics tool so usage decline reads as a trend across weeks instead of the single data point in this export, a quiet week and a dying account look identical without it.

## Go further
Running the postmortem by hand catches this year's pattern. Here's how it starts catching next year's churn before it happens.

- **Score the active book weekly.** Connect Salesforce and Amplitude to a scheduled Claude task that reruns the early-warning checklist against every live account every Monday, not just when someone remembers to ask.
- **Alert on the signal, not the renewal date.** Wire a Slack message to the account owner the moment an account trips two or more warning signals, so the save attempt happens in month two, not the renewal call.
- **Feed saves back into the theme.** Log every successful save in a data store so the checklist itself improves: which signals actually predicted churn versus which ones were noise.

Catching the pattern once is a report. Watching for it every week is retention.

## Make it yours
Fork it. Change the themes, the checklist signals, the thresholds. The point is not to run someone else's playbook. It is to run yours, faster. Built by an operator. Customize it, break it, make it better.
