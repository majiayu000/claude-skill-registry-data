---
name: demo-script
description: Turn a generic product tour into a buyer-specific demo that only shows what they told you hurts. Maps every feature you plan to show to a problem the buyer actually stated, writes the "so what" for each moment, and flags the trap of feature-dumping before you fall into it. Built for B2B sales teams, customizable to your product and your discovery. Trigger on "build a demo script", "prep for the demo", "what should I show", "map features to pain", "stop me from feature dumping", or any pre-demo planning pass.
---

# Demo Script

## What this does
Builds a demo script for one specific buyer, not a tour. It takes the problems the buyer stated in discovery and, for each thing you plan to show, forces a link back to one of those problems. Every moment gets a "so what" in the buyer's terms. Anything that does not map to a stated problem gets cut, because that is where demos go to die.

## What you'll need
You do not need to connect anything to get value today. Bring your discovery notes and your feature list and the skill runs now. Connect the tools below and it pulls the buyer's own words for you.

- Works today with: the problems the buyer told you (paste your discovery notes) and the features you are considering showing. The skill does the mapping and the cutting.
- More powerful connected to a meeting or transcription tool: it pulls the buyer's exact quotes from the discovery call, so each feature maps to something they actually said, not something you hope they meant.
- Sharper connected to a CRM: it reads the qualification fields on the deal and orders the demo around the decision criteria that will actually get it bought.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the discovery you give it today and gets sharper as you connect tools. It never maps a feature to a problem the buyer did not raise. A feature with no stated problem behind it is a cut, not a slide.

- **Bring your data**: paste your discovery notes and your candidate feature list. The skill returns the mapped script, the "so what" per moment, and the cut list today. No connection required.
- **Connect your tools**: the same skill pulls the buyer's own quotes from the call and the criteria from the deal, so the mapping is grounded in what they said. Same output, less guessing.
- **Just exploring**: no deal yet? Get the mapping structure, the "so what" prompts, and a worked example on a sample buyer, so you can see the shape before you build one.

Every run ends with the one feature you were about to show that you should cut, and why.

## Customize this for yourself
This was built for a B2B SaaS org that demos a multi-feature platform. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| PRODUCT areas | the features you can demo | your modules, your workflows |
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| MEETING source | where discovery is recorded | your meeting or transcription tool |
| DISCOVERY fields | where stated pain lives | your qualification fields |
| CRITERIA field | the buyer's decision criteria | Decision_Criteria custom field |
| DEMO length | how long you actually have | 30 min (re-tune to your slot) |
| PROOF assets | what backs each claim | case snapshot, metric, live data |

Map to the problems your buyer stated, not to your feature roadmap. The skill shows what earns its place in the room.

## The method

### One problem per moment
Every feature you plan to show must map to exactly one problem the buyer stated. Write the problem in their words on the left, the feature on the right. If the left side is blank, the feature does not go in the demo. This is the whole discipline.

### The "so what" per moment
For each mapped moment, write the "so what" in the buyer's terms: what changes for them, not what the button does. "You click here" is a feature. "This is the 6 hours a week your reps stop losing" is a so-what. Illustrative, but that is the register.

### The cut list
Everything that did not map to a stated problem goes on an explicit cut list, so you can see what you are tempted to show and why it is dangerous. Showing it dilutes the moments that matter and invites questions you did not need.

### Order for the decision, not the product
Sequence the demo around the buyer's decision criteria, strongest pain first. Open on the thing that hurts most, not the thing your product happens to open on. Land the highest-stakes moment while attention is full.

### The feature-dump trap
The failure mode is showing everything the product does to prove it is powerful. It reads as insecure and it buries the two moments that would have closed the deal. The script names this trap explicitly and keeps you to the mapped moments.

## Quality gates
- No feature in the script without a stated buyer problem mapped to it.
- Every moment has a "so what" written in the buyer's language, not the product's.
- The cut list is shown, not hidden, so the feature-dump temptation is visible.
- The demo is ordered by pain and decision criteria, not by product menu order.

## Output (example)
```
DEMO SCRIPT · illustrative buyer
Order  Stated problem (their words)        Show this            So what
1      "Reps lose hours building lists"    Prospecting view     Gives back ~6 hrs/wk/rep
2      "We can't tell what's working"      Sequence analytics   Kills the guesswork on cadence
3      "Handoffs drop the ball"            Shared deal view     Nothing slips between AE and CSM

Cut list (do not show):
  - Admin settings deep-dive. No stated problem. Feature dump.
  - Reporting API. Not raised. Save for a technical follow-up.

Open on moment 1. It is their loudest pain. Do not lead with the tour.
```

## Where the inputs come from
The one-problem-per-moment rule and the cut list are the defaults that keep a demo from becoming a tour. The demo length, the feature areas, and the proof assets are yours. If you have 15 minutes, the mapping matters more, not less. The discipline is the same. The script is yours.

## Example chat
Here is the skill running on a real discovery-to-demo handoff, start to finish.

**You:** Build a demo script, here's my discovery notes and the features I was going to show. [pastes notes]

**Claude:** Mapped every feature to a stated problem and cut what did not.
```
1  "Reps lose hours building lists" -> Prospecting view -> Gives back ~6 hrs/wk/rep
2  "We can't tell what's working"   -> Sequence analytics -> Kills the cadence guesswork

Cut list:
  - Admin settings deep-dive. No stated problem. Feature dump.
  - Reporting API. Not raised. Save for a technical follow-up.
```
The catch: two of the five features you planned to show never came up in discovery. Showing them would have buried the two moments that actually map to what the buyer said hurts.

**You:** Order it for a 20-minute slot, I only have 20 minutes now, not 30.

**Claude:** Cut to the two highest-stakes mapped moments and opened on the loudest pain, list-building, since attention is fullest at the start. One sharpener: connect your meeting tool so next time the mapping pulls the buyer's exact quote instead of your paraphrase of the notes.

## Go further
The read is step one. Here is where an operator takes it once the manual version proves out.

- **Pull discovery quotes automatically.** Connect Gong or another transcript tool so each mapped feature carries the buyer's exact words, not a typed recap.
- **Order around the real decision criteria.** Connect the CRM's qualification fields so the script sequences by what the deal record says matters most, not a default order.
- **Catch feature-dump before the call.** Wire this as a pre-demo check in Slack: a rep pastes their planned agenda and gets the cut list back before they open the screen share.

Show only what they told you hurts. Cut the rest before the call, not during it.

## Make it yours
Fork it. Change the mapping, the "so what" prompts, the order logic. The point is not to run someone else's demo. It is to show this buyer only what they told you hurts, and to cut the rest. Built by an operator. Customize it, break it, make it better.
