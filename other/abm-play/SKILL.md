---
name: abm-play
description: Turn a target account list into a real account-based play, not a spray. It tiers the accounts, sets the research angle per tier, builds the multi-thread across marketing and sales, and orchestrates the touches so the account feels one coordinated motion instead of a rep and a marketer working past each other. Built for B2B revenue teams, customizable to your CRM and your channels. Trigger on "build an ABM play", "account-based plan for this list", "how do I run ABM on these accounts", "tier my target list", "coordinate marketing and sales on these accounts", or any account-based planning request.
---

# ABM Play

## What this does
Takes a list of target accounts and builds the play to work them: it tiers the accounts by fit and potential, sets the research angle each tier deserves, plans the touches across marketing and sales so more than one person is reaching in, and orchestrates the timing so the account experiences one coordinated motion, not scattered noise. The output is a play a rep and a marketer can run together this week, not a strategy deck.

## What you'll need
You do not need to connect anything to get value today. Bring your account list and the skill runs now. Connect the tools below and it pulls the context automatically and adds signals you cannot paste by hand.

- Works today with: the accounts you paste or upload. Names, and whatever you know about fit, size, and where you already have a foothold. A plain list is enough to start.
- More powerful connected to a CRM: it reads the account fields, open opportunities, and existing contacts automatically, so the tiers and threads match the real book.
- Sharper with an intent or web source: adds buying-signal data so the play leads with the accounts already leaning in.
- Sharper with an enrichment source: fills in the buying committee so the multi-thread plan names real roles, not guesses.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the list you give it today and gets more powerful as you connect tools. It never invents an account signal it cannot see. A gap is a question it asks you, not a number it makes up.

- **Bring your data**: paste or upload the accounts. The skill builds the full play today on your real list. No connection required.
- **Connect your tools**: the same skill pulls fit, opportunities, contacts, and intent automatically. Same play, less effort, grounded in live signal.
- **Just exploring**: no list yet? Get the framework, the exact fields it reads, and a worked example on sample accounts, so you can see the shape before you feed it.

Every run ends with the one thing that would sharpen the next: a field to add, an intent source to connect, a role to confirm.

## Customize this for yourself
This was built for a B2B SaaS org running tiered ABM into a buying committee. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| MAP | marketing automation / email platform | your MAP |
| TIERS | how many account tiers | 3 (1:1, 1:few, 1:many) |
| FIT fields | what defines a strong account | ICP fields, firmographics |
| INTENT source | buying-signal data | your intent, web, or ad platform |
| CHANNELS | where touches land | email, ads, social, direct mail, events |
| ORCH_WINDOW | days a play's touches should land within | 10 (re-tune to your motion) |

Your tier definitions are yours. The skill tiers against the fit and potential rules you set, not a generic model.

## The method

### Tier the list (not every account gets the same play)
Sort the accounts into tiers by fit and potential, not by alphabetical luck. Tier 1 accounts earn a 1:1 play with real research behind it. Tier 2 accounts get a 1:few play grouped by a shared pain. Tier 3 accounts get a 1:many play that runs on programs. Name why each account sits where it does, so the effort follows the prize.

### Set the research angle (per tier)
Tier 1 accounts deserve a specific hook: a trigger event, an initiative, a named priority you can point to. Tier 2 accounts share an angle across the group. Tier 3 accounts run on the ICP-level message. Write the angle, not just the fact. An angle is a reason this account should care now. A tool like Deepline can pull the firmographic and committee research that feeds the tier-1 angle.

### Build the multi-thread across marketing and sales
For each tier, name who reaches in and how. Marketing runs the air cover: ads, content, nurture to the committee. Sales runs the ground game: personalized outreach to the named roles. List the roles the account needs on side, the economic buyer, the champion, the technical evaluator, and mark who owns opening each thread. Single-threaded ABM is just outbound with a bigger logo.

### Orchestrate the touches (land together, not scattered)
Sequence the touches inside a window so the account feels one motion, not a marketer and a rep arriving on different days with different stories. Air cover warms, the human follows while it is warm, the follow-up references the same angle. Set the window and the order. Coordination is the whole point of account-based; without it you have two campaigns wearing a trench coat.

### Set the trigger to advance (from air cover to human)
Define the signal that moves an account from program to person: an ad engagement, a content download, a site visit from a target role. When it fires, the rep reaches in with the same angle the program was running. The message can carry the account and persona context so the human touch does not restart the conversation. That is the handoff that converts attention into a meeting.

## Quality gates
- Every account sits in a tier with a named reason, never sorted by size alone.
- Tier 1 accounts carry a specific angle tied to a real trigger, never a generic value line.
- The thread map names the roles still dark, not only the ones already engaged.
- Marketing and sales touches share one angle and land inside the orchestration window, never as two disconnected campaigns.
- Any account signal or contact carried in is shown as given or sourced, never invented. Sample figures are illustrative only.

## Output (example)
```
ABM PLAY · 12 target accounts (illustrative)

Tiering
  Tier 1 (1:1)     3 accts   named initiative + committee mapped
  Tier 2 (1:few)   5 accts   grouped on a shared pain
  Tier 3 (1:many)  4 accts   ICP program only

Tier 1 · Acme Corp
  Angle       new VP hired, mandate to consolidate tooling
  Air cover   committee ads + case-study nurture (marketing)
  Ground      champion + economic buyer outreach (rep)
  Threads     champion: engaged   econ buyer: DARK <- open next
  Window      touches land within 10 days, air cover leads

Next moves:
  1. Launch tier-1 air cover Monday; rep outreach follows Wed while warm.
  2. Open the economic-buyer thread on Acme via the champion.
  3. Group tier-2 accounts on the shared pain; one nurture, five accounts.
```

## Where the inputs come from
TIERS (3), ORCH_WINDOW (10 days), and the fit rules are defaults, not laws. They suited a mid-market ABM motion. The accounts, roles, and triggers above are examples, illustrative only, not real companies. The method does not change when your list does. Set the tiers, the channels, and the window to your motion and the play shapes itself around it.

## Example chat
**You:** I've got 12 target accounts for Q3. Can you tier them and build the play?

**Claude:** Tiered. 3 accounts earned Tier 1.
```
Tier 1 (1:1)     3 accts   named initiative + committee mapped
Tier 2 (1:few)   5 accts   grouped on shared pain
Tier 3 (1:many)  4 accts   ICP program only
```
Acme Corp is Tier 1: new VP hired with a mandate to consolidate tooling, that's the angle. Champion is engaged, economic buyer is still dark, that's the open thread. The catch worth flagging: two of your "Tier 1" picks only had size going for them, no real trigger, so I dropped them to Tier 2 until you can name why now matters.

**You:** Good catch. What about sequencing the touches?

**Claude:** Air cover (committee ads plus nurture) leads Monday, rep outreach follows Wednesday while it's still warm, both carrying Acme's same angle. One sharpener: connect an intent source and I'll flag which Tier 3 accounts are already leaning in, so you're not running the same program blind to which ones are actually warm.

## Go further
The tiering and thread map prove the model works on paper. Here's the scaled version.

- **Auto-tier the whole pipeline.** Connect Salesforce or HubSpot and a scheduled Claude task re-tiers the list nightly as fit fields and open opportunities change.
- **Watch for the advance trigger.** Wire Clay or an ad platform to flag ad engagement or a target-role site visit, then message the rep in Slack the moment an account is ready to move from air cover to human.
- **Keep the angle consistent everywhere.** Feed the tier-1 angle into your sequencer (Outreach, Salesloft) so every touch, air cover and ground game, references the same trigger instead of drifting into generic copy.

Coordinated once by hand, coordinated forever by the system.

## Make it yours
Fork it. Change the tiers, the channels, the orchestration window. The point is not to run someone else's ABM template. It is to make your best accounts feel one coordinated motion instead of noise. Built by an operator. Customize it, break it, make it better.
