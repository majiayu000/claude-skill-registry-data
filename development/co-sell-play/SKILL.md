---
name: co-sell-play
description: Run a co-sell with a partner on a named account and actually close together, not just trade a lead. It maps the account across both companies, sets who owns what so nothing falls between you, builds the joint value story neither of you tells alone, and plans the path to close so the partner is a force in the deal, not a spectator. Built for B2B partnerships and sales teams, customizable to your CRM and your co-sell motion. Trigger on "run a co-sell", "co-sell on this account", "map the account with our partner", "who owns what in this joint deal", "joint value story", or any partner co-sell request on a named account.
---

# Co-Sell Play

## What this does
Takes one named account and a partner and builds the co-sell: it maps who each side knows and covers inside the account, sets clear ownership so the deal does not fall into the gap between two companies, writes the joint value story neither of you can tell alone, and plans the path to close so both teams are pulling. A co-sell that is just a traded lead and a hope is not a co-sell. This makes the partner a force in the deal.

## What you'll need
You do not need to connect anything to get value today. Bring the account and the partner and the skill runs now. Connect the tools below and it pulls the context automatically and adds signals you cannot paste by hand.

- Works today with: what you paste about the account and the partner. Who you each know, where the deal stands, and what each company sells into it. A short account picture is enough to start.
- More powerful connected to a CRM: it reads your contacts, the open opportunity, and stage automatically, so the account map and the close plan match the real deal.
- Sharper with a meeting or email tool: shows who on your side is actually engaged and who has gone quiet, so the coverage map is real, not aspirational.
- Sharper with an enrichment source: fills in the roles and reporting lines so you can see the gaps only the partner can cover.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you tell it today and gets more powerful as you connect tools. It never invents a relationship or a contact it cannot see. A gap is a question it asks you, not a name it makes up.

- **Bring your data**: paste the account and partner picture. The skill builds the full co-sell play today on your real deal. No connection required.
- **Connect your tools**: the same skill pulls contacts, the opportunity, and engagement automatically. Same play, less effort, grounded in who is really moving.
- **Just exploring**: no live deal? Get the framework, the fields it reads, and a worked example on a sample account, so you can see the shape before you bring a real one.

Every run ends with the one thing that would sharpen the next: a partner contact to confirm, a thread to open, a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org co-selling into a buying committee with a partner. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| PARTNER role | how the partner shows up in the deal | tech alliance, reseller, referral, SI |
| STAGE field | the opportunity stage | Opportunity.StageName |
| CONTACT ROLES | how you see who is on a deal | OpportunityContactRole |
| ENGAGEMENT source | where replies and touches live | Task, Event, email or meeting tool |
| OWNERSHIP model | how you split the deal | who leads, who supports, who owns close |
| ENRICHMENT | source for roles and reporting lines | your enrichment connector |

Your co-sell motion is yours. The skill maps and splits against the model you set, not a generic one.

## The method

### Map the account across both companies
Lay the account out and mark who each side knows: your contacts, the partner's contacts, and the roles still uncovered by either of you. The whole reason to co-sell is coverage neither side has alone. Find the room the partner is already in that you are not, and the reverse. Name the overlap and the gaps.

### Set who owns what (so nothing falls between you)
The fastest way to lose a co-sell is both sides assuming the other has it. Assign it plainly: who leads the relationship, who runs the technical proof, who owns the commercial conversation, who drives the close. Write it down where both teams can see it. Ambiguity is where joint deals go to die.

### Build the joint value story (neither of you tells alone)
The point of the partnership is a story bigger than either product: the combined outcome for the customer, why the two together beat either alone or a point tool. Write the version the customer hears, in their terms, with the roles each company plays. If the pitch is two vendors taking turns, you have a bake-off, not a co-sell.

### Plan the path to close (both teams pulling)
Lay out the steps to signature and mark which company drives each: the joint discovery, the technical validation, the business case, the procurement path. Put dates on the near ones. Flag the risks only the partner can clear and the ones only you can. A shared close plan is what turns a traded lead into a won deal.

### Keep both sides accountable (before the deal drifts)
Set the checkpoint that proves the co-sell is live: a joint meeting held, a partner-driven thread opened, a step the other company owns and delivered. If a side goes quiet, the deal is quietly reverting to single-company, and you re-engage now, not at the next partner sync.

## Quality gates
- The account map names the roles uncovered by either side, not only the ones already known.
- Every deal step has one named owner, never "we will figure it out."
- The joint value story is the customer's outcome, never two vendor pitches stapled together.
- Engagement claims are grounded in real touches where that data exists, and flagged as assumption where it is not.
- Any name, role, or figure carried in is shown as given or sourced, never invented. Sample numbers are illustrative only.

## Output (example)
```
CO-SELL PLAY · Acme Corp x Partner (illustrative)

Account map
  Role            You        Partner    Status
  Champion        Dana       -          engaged (yours)
  Econ buyer      -          CFO        engaged (partner's) <- lean here
  Tech evaluator  Sam        -          engaged
  Procurement     -          -          UNCOVERED <- neither side

Ownership
  Relationship lead   Partner (owns the CFO)
  Technical proof     You
  Close / commercial  You lead, partner supports

Joint value story
  Combined outcome the CFO buys, not two product pitches

Next moves:
  1. Use the partner's CFO access to open the economic thread.
  2. You own the technical proof; partner joins the readout.
  3. Cover procurement now. Neither side has it yet.
```

## Where the inputs come from
The OWNERSHIP model and the roles above are defaults and examples, illustrative only, not real people or a real deal. They suited a mid-market co-sell into a committee. The method does not change when your account does. Set the ownership split, the partner role, and the contact roles to your real motion and the play maps itself around it.

## Example chat
Here is the skill running on a real named account and partner.

**You:** We're co-selling Acme Corp with our SI partner. Map it and tell me where we're exposed.

**Claude:** Read's done. You have one uncovered seat that's already blocking the deal.
```
Role            You     Partner   Status
Champion        Dana    -         engaged (yours)
Econ buyer      -       CFO       engaged (partner's)
Procurement     -       -         UNCOVERED
```
Procurement is uncovered by both sides, and that's usually where a joint deal stalls at signature, not at the pitch. Neither team has assumed ownership of it yet. One sharpener: confirm with the partner who their procurement contact actually is, right now it's an assumption, not a name.

**You:** Set ownership across the deal so nothing falls between us.

**Claude:** Done. Splitting by who already has the room.
```
Relationship lead   Partner (owns the CFO)
Technical proof     You (owns Dana + Sam)
Close/commercial    You lead, partner supports
Procurement         UNASSIGNED, still open
```
The gap is real: nobody owns procurement yet. One sharpener: put a joint checkpoint on the calendar this week where both sides confirm who's closing that gap, before it becomes the reason the deal slips a quarter.

## Go further
The read is step one. Here's where an operator takes it once the manual version proves out.

- **Turn the account map into a living record.** Connect Salesforce so the coverage map updates automatically as contacts and roles get added, instead of going stale after this snapshot.
- **Catch the silent partner before the deal does.** Point a scheduled Claude task at Slack and email threads weekly and flag any owned step that's gone quiet more than 5 days.
- **Give the partner a self-serve view.** Stand up a shared Slack canvas with the account map and ownership table so both sides see the same gaps in real time, not at the next sync.

You built the read once; now it runs itself.


## Make it yours
Fork it. Change the ownership model, the roles, the close steps. The point is not to run someone else's co-sell script. It is to make the partner a force in the deal instead of a lead you traded and forgot. Built by an operator. Customize it, break it, make it better.
