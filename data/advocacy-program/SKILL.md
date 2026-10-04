---
name: advocacy-program
description: Turn happy customers into references, case studies, and referrals, on purpose instead of by accident. Reads who is happy enough to ask, picks the right ask, sets the value exchange, and builds a pipeline of advocacy over time. Built for B2B customer success teams, customizable to your product and your program. Trigger on "build an advocacy program", "who can be a reference", "find case study candidates", "ask for a referral", "customer advocacy pipeline", or any reference-and-referral planning.
---

# Advocacy Program

## What this does
Turns your happiest customers into references, case studies, and referrals as a system, not a scramble the week before a launch. It finds who has earned enough goodwill to ask, matches each one to the right ask, sets a fair value exchange so it is not a favor, and runs the whole thing as a pipeline with stages, not a one-time beg. Advocacy is a program you build, not a mood you catch.

## What you'll need
You do not need to connect anything to get value today. Bring what you know about your accounts and the skill runs now. Connect the tools below and it pulls signals automatically and adds ones you cannot paste by hand.

- Works today with: what you can describe. Which accounts are happy, who the champions are, what results they have seen, and what you need (references, stories, referrals). Paste a list or describe your book.
- More powerful connected to a CRM: pulls account health, tenure, and value, so the ask goes to the right accounts.
- Sharper with a product-analytics tool: confirms a "happy" account is actually a deeply adopted one, not a quiet one.
- Sharper with a survey or feedback tool: adds satisfaction signals so you ask the people who already told you they are glad.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never invents a satisfaction signal it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: describe your accounts and champions. The skill builds the full advocacy slate today on your real book. No connection required.
- **Connect your tools**: the same skill pulls health, adoption, and satisfaction automatically and adds signals you cannot paste by hand (real usage depth, survey scores, tenure). Same output, less effort, sharper.
- **Just exploring**: no book yet? Get the framework, the ask ladder, and a worked example on sample accounts, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a signal to add or a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org running a customer marketing motion. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | your CRM of choice |
| HEALTH field | how you read account health | health score, green/yellow/red |
| CHAMPION field | how you tag your advocate | contact role, relationship strength |
| ASK_LADDER | the asks, easy to heavy | review, reference call, case study, referral |
| VALUE_EXCHANGE | what the customer gets back | exposure, swag, credits, exec access |
| SATISFACTION | your happiness signal | survey score, renewal, expansion |
| PIPELINE_STAGES | how you track an advocate | Identified, Asked, Committed, Live, Nurtured |

Run any advocacy model you like. The skill matches ask size to relationship strength, so point it at your own health and champion signals, not anyone else's.

## The method

### Who to ask (earn the right)
Not every happy account is an advocate. Rank on three things: they are getting real results, the relationship has a named champion, and you have banked more goodwill than you are about to spend. Only then do you ask. Asking a shaky account for a public story is how you lose it.

### Match the ask to the relationship
Asks come in sizes. A quick review is light. A reference call is medium. A named case study is heavy. A referral is a favor with your reputation attached. Start light, earn the heavy ones. Do not open with the biggest ask on a new relationship.

### The value exchange
Advocacy is a trade, not a donation. Name what the customer gets: exposure to their market, access to your executives or roadmap, credits, a genuine thank-you that helps their own career. If you cannot name what they get, you are asking for a favor, and favors do not scale.

### The advocacy pipeline
Treat advocates like a pipeline with stages: Identified, Asked, Committed, Live, Nurtured. An advocate is not one-and-done. The customer who did a story this quarter is your reference next quarter, if you nurture them instead of disappearing.

### Cadence and no-burnout rule
Space the asks. The same three logos cannot carry your whole program, and over-asking a good advocate burns them out. Rotate. Keep a bench. One heavy ask per advocate per period, tracked.

## Quality gates
- No ask to an account that is not both happy and stable. Verify the health signal first.
- The ask size matches the relationship strength. No heavy ask on a light relationship.
- Every ask names what the customer gets back. No naked favors.
- No advocate carries more than one heavy ask per period. Rotate the bench.
- "Happy" is backed by a real signal (renewal, adoption, survey), never a hunch.

## Output (example)
```
ADVOCACY PIPELINE, one book
Need: 2 case studies, 3 reference calls, an intro to a similar buyer

Ready to ask
  Account A  champion strong, deeply adopted, renewed 2x
             -> heavy ask: named case study. Exchange: conference speaking slot.
  Account B  champion strong, high survey score
             -> medium ask: reference call. Exchange: early roadmap access.
  Account C  happy, newer relationship
             -> light ask: a review. Exchange: a public thank-you + swag.

Not yet
  Account D  results good but no named champion. Build the relationship first.

Nurture
  Account E  did a story last quarter. Send the results it drove. Do not re-ask yet.
```
(Accounts and details are illustrative.)

## Where the numbers come from
The ask ladder and the one-heavy-ask-per-period rule are defaults, not laws. They suited a mid-market customer marketing motion. If your advocates are enterprise and rare, slow the cadence. The logic does not change. The thresholds are yours.

## Example chat
**You:** I need 2 case studies and 3 reference calls this quarter. Who in my book can actually carry that?

**Claude:** Ran your book against the ask ladder.
```
Ready to ask
  Account A  champion strong, deeply adopted, renewed 2x
             -> heavy ask: named case study. Exchange: conference speaking slot.
  Account B  champion strong, high survey score
             -> medium ask: reference call. Exchange: early roadmap access.

Not yet
  Account D  results good but no named champion. Build the relationship first.
```
The thing worth flagging: Account C looked like your best case-study candidate on paper (biggest logo, great results), but they already carried a heavy ask last quarter, so asking again this soon burns them instead of earning the story.

**You:** Good catch, I forgot about that. What do I do with Account D?

**Claude:** Hold it. No named champion means no one owns carrying your ask internally, so it's not ready for any ask yet, light or heavy. One sharpener: connect your CRM's health field and I'll re-rank the whole "ready to ask" list automatically as accounts renew or expand instead of you re-checking it by memory each quarter.

## Go further
Picking asks by hand works for one quarter's list. Here's how an operator keeps the pipeline running.

- **Track the bench automatically.** Wire Salesforce or HubSpot health and renewal fields into a scheduled Claude task that refreshes the ask ladder every Monday, so no advocate gets a second heavy ask before their rotation is up.
- **Catch the goodwill signal live.** Connect Gong or your survey tool so a glowing call or a high NPS score drops the account straight into "ready to ask" instead of waiting for someone to remember.
- **Close the loop into content.** Feed a completed case study into your content-repurposing skill so one advocacy win becomes a LinkedIn post, a nurture email, and a sales one-pager automatically.

Advocacy stops being a fire drill once the pipeline runs itself.

## Make it yours
Fork it. Change the ask ladder, the value exchange, the stages. The point is not to run someone else's playbook. It is to run yours, faster, so advocacy stops being a fire drill and becomes a pipeline. Built by an operator. Customize it, break it, make it better.
