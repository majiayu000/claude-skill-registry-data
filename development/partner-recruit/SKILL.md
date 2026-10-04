---
name: partner-recruit
description: Recruit a channel or tech partner and actually activate them, not just sign them. It scores who fits, writes the mutual-value pitch in their terms, builds the enablement that makes them productive, and plans the first co-marketing or co-sell motion so the partnership produces something in the first quarter instead of going dark after the kickoff. Built for B2B partnerships teams, customizable to your CRM and your partner program. Trigger on "recruit a partner", "does this partner fit", "pitch a partnership", "activate a new partner", "partner enablement plan", "first co-marketing motion", or any partner recruiting or activation request.
---

# Partner Recruit

## What this does
Takes a prospective channel or technology partner and builds the recruit-to-activate plan: it scores whether they actually fit, writes the mutual-value pitch in their language rather than yours, lays out the enablement that gets their team productive, and plans the first joint motion so the partnership ships something real in its first quarter. Most partnerships die between the signed agreement and the first deal. This is built to cover that gap.

## What you'll need
You do not need to connect anything to get value today. Bring the partner and the skill runs now. Connect the tools below and it pulls the context automatically and adds signals you cannot paste by hand.

- Works today with: what you paste about the partner. Who they are, who they sell to, what they sell, and why you think there is a fit. A short profile is enough to start.
- More powerful connected to a CRM: it reads your accounts and overlap automatically, so the fit case is grounded in shared customers and shared ICP, not a hunch.
- Sharper with an enrichment source: fills in the partner's size, focus, and the people you need to reach on their side.
- Sharper with a meeting or email tool: tracks whether the activation is actually happening or quietly stalling after the kickoff.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you tell it today and gets more powerful as you connect tools. It never invents an overlap or a contact it cannot see. A gap is a question it asks you, not a fact it makes up.

- **Bring your data**: paste the partner profile and context. The skill builds the full recruit-and-activate plan today. No connection required.
- **Connect your tools**: the same skill pulls the account overlap, the partner firmographics, and the activity automatically. Same plan, less effort, grounded in real overlap.
- **Just exploring**: no partner in mind yet? Get the framework, the fields it reads, and a worked example on a sample partner, so you can see the shape before you bring a real one.

Every run ends with the one thing that would sharpen the next: an overlap to confirm, a contact to add, a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org running a channel and tech-partner program. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| PARTNER type | channel, tech, referral, reseller | tech / channel |
| FIT traits | what makes a partner worth the effort | ICP overlap, reach, motivation, capacity |
| OVERLAP source | where shared accounts / ICP live | CRM accounts, partner list match |
| ENRICHMENT | source for partner firmographics + contacts | your enrichment connector |
| ACTIVATION window | days to first joint motion | 90 (re-tune to your program) |
| FIRST_MOTION | the initial joint play | co-marketing webinar or co-sell on 3 accounts |

Your definition of a good partner is yours. The skill scores against the traits you set, not a generic profile.

## The method

### Score the fit (before you court them)
Not every logo is a partner worth the effort. Score the prospect on four things: do they sell to your ICP, do they have real reach into it, are they motivated to move (a gap in their offering you fill), and do they have the capacity to actually sell or build. A partner with reach but no motivation will sign and stall. Name the difference.

### Write the mutual-value pitch (in their terms)
A partner does not care about your quota. Write the case in their language: what this does for their revenue, their retention, or their product gap, backed by the account overlap you can show. Lead with what they get, evidence it with shared customers or ICP, then name what you need from them. If the pitch is all about you, it will not land.

### Build the enablement (make them productive)
A signed partner who cannot explain your value is not activated. Lay out the minimum they need to sell or build: the one-pager, the pitch, the demo path, the person on your side they call. Keep it small enough that a busy partner rep will actually use it. Enablement they will not open is not enablement.

### Plan the first joint motion (ship something this quarter)
Pick one concrete first motion and put a date on it: a co-marketing webinar, a joint content piece, or a co-sell on a short list of overlap accounts. One shared win in the first quarter proves the partnership to both sides and earns the next one. A partnership with no first motion is a press release, not a channel.

### Set the activation checkpoint (catch the stall early)
Define the signal that the partnership is real: a registered deal, a co-marketing asset shipped, a partner rep who pitched unprompted. If the checkpoint passes empty inside the window, you have a stalled partner, and you re-engage or reallocate now, not a year later at a QBR.

## Quality gates
- No partner is called a fit without evidence of ICP overlap and motivation, not just a nice logo.
- The pitch leads with the partner's gain and evidences it, never opens with your quota.
- Enablement is scoped to what a busy partner rep will actually use, never a document dump.
- Every plan names a dated first motion, not an open-ended intention.
- Any overlap, contact, or figure carried in is shown as given or sourced, never invented. Sample numbers are illustrative only.

## Output (example)
```
PARTNER RECRUIT · Northstar Consulting (illustrative)

Fit score
  Sells to ICP     yes    serves the same mid-market buyer
  Reach            high   ~40 accounts in our ICP
  Motivation       yes    gap in their stack we fill
  Capacity         medium small team, needs light enablement
  Verdict          RECRUIT (tech + referral)

Mutual value
  For them   new revenue line + stickier customers
  Evidence   11 shared ICP accounts, 2 already our customers
  For us     reach into their installed base

First motion (within 90 days)
  Co-sell on 3 overlap accounts, joint webinar to their list

Next moves:
  1. Send the mutual-value pitch led with their retention gain.
  2. Ship the one-pager + demo path; name their single point of contact.
  3. Lock the webinar date. First win before the quarter closes.
```

## Where the inputs come from
The FIT traits and the ACTIVATION window (90 days) are defaults, not laws. They suited a mid-market channel program. The partner, overlap, and figures above are examples, illustrative only, not a real company. The method does not change when your program does. Set the traits, the first motion, and the window to your program and the plan shapes itself around it.

## Example chat

**You:** Northstar Consulting reached out about partnering. Worth pursuing?

**Claude:** Scored the fit before writing anything.
```
Fit score
  Sells to ICP     yes    serves the same mid-market buyer
  Reach            high   ~40 accounts in our ICP
  Motivation       yes    gap in their stack we fill
  Capacity         medium small team, needs light enablement
  Verdict          RECRUIT (tech + referral)
```
Reach is high, but the piece that actually matters here is motivation: they have a real gap we fill, not just a nice logo willing to sign. A partner with reach and no motivation signs and goes quiet.

**You:** Draft the pitch and the first move.

**Claude:** Here's the pitch, led with their gain first.
```
For them: new revenue line + stickier customers
Evidence: 11 shared ICP accounts, 2 already our customers
First motion (90 days): co-sell on 3 overlap accounts, joint webinar to their list
```
Sharpener: connect the CRM so the 11-account overlap comes from real shared-account matching instead of a manual pull, and so the activation checkpoint at Day 90 gets tracked instead of relying on someone remembering to check.

## Go further
The scoring and the pitch prove the fit. Here's the version that catches the stall a signed partnership usually hits after the kickoff.

- **Track the checkpoint automatically.** A scheduled Claude task checks Salesforce at Day 90 for a registered deal or a shipped co-marketing asset, and flags a stalled partner before it reaches a QBR.
- **Find the overlap without the manual pull.** Connect the CRM so shared-account matching runs live, and the mutual-value pitch is always grounded in the current book, not a stale export.
- **Route the enablement where the partner rep actually works.** Drop the one-pager and demo path into a shared Slack channel with the partner instead of a document they have to go dig up.

Recruiting the partner is the pitch. Activating them is the part that needs the follow-through built in.

## Make it yours
Fork it. Change the fit traits, the first motion, the activation window. The point is not to run someone else's partner program. It is to make sure the partners you sign actually produce instead of going dark after the kickoff. Built by an operator. Customize it, break it, make it better.
