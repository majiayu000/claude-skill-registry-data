---
name: warm-path-finder
description: Before any cold touch on a target account, find and rank every warm way in. Inventories your team's collective network, customers, past colleagues, investors, and community overlap, scores each path, picks one connector, and writes the forwardable intro request. Built for B2B sellers, customizable to your network sources and CRM. Trigger on "warm intro path", "who can intro me", "bridge before cold", "warm path into this account", "find a referral path".
---

# Warm-Path Finder

## What this does
Takes a target account and answers one question before you write a single cold message: who do we already know who can walk us in? It inventories every plausible path, scores each one, picks the single best connector, and drafts the intro request that connector can forward in ten seconds. If no path clears the bar, it tells you to go cold and names the signal to anchor on. This skill runs before trigger-outreach: trigger-outreach turns a buying signal into a timely cold touch, while this skill decides whether you need to go cold at all by finding the warm path first.

## What you'll need
You do not need to connect anything to get value today. Bring your target list and what you know about your own network, and the skill runs now. Connect the tools below and it maps paths you would never find by hand.

- Works today with: your target account list, the names of the people on your team, your customer list, and a manual LinkedIn mutual-connections check on the buying contacts. Paste it or upload a CSV.
- More powerful connected to a network-mapping tool (The Swarm or similar): it maps your whole team's collective network against the account automatically.
- Sharper with a CRM: surfaces which current customers and past deals touch the account.
- Sharper with LinkedIn Sales Navigator: pulls mutual connections and past-colleague overlap at scale.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the data you give it today and gets more powerful as you connect tools. It never claims a relationship it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste your target accounts, your team roster, and your customer list. Add what a manual LinkedIn mutual-connections check turned up. The skill inventories, scores, and ranks the paths today. No connection required.
- **Connect your tools**: the same skill pulls network overlap, customer relationships, and colleague history automatically from a network-mapping tool, your CRM, and Sales Navigator. Same output, wider net, sharper.
- **Just exploring**: no target list yet? Get the six path sources, the scoring model, and a worked example on sample data, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next run sharper, a source to add or a tool to connect.

## Customize this for yourself
This was built for a B2B sales team selling into mid-market accounts. Set these to your world:

| Set this | What it is | Default / Example |
|---|---|---|
| PATH SOURCES | which of the six sources you can actually check | team network, customers, past colleagues, investors/advisors, community, shared vendors |
| STRENGTH THRESHOLD | minimum path score before you ask for the intro | 6 of 9 (re-tune to your market) |
| ONE-PATH RULE | max simultaneous intro requests per account | 1, always 1 |
| INTRO-REQUEST TEMPLATE | your forwardable blurb format | 3 sentences: who you are, why this buyer, the ask |

The sources are a menu, not a mandate. Check the ones your team can actually see into, and be honest about which ones you cannot.

## The method

### Inventory every path
For each target account, sweep six sources: your team's collective network (everyone's connections, not just yours), current customers who could refer, past colleagues of the buying committee members, investors and advisors you share, community and event overlap, and vendors you both use. List every named person who bridges you to the account. No name, no path.

### Score each path (three dimensions, 1 to 3 each)
- Strength: how well does the connector actually know the buyer? Worked together beats met once.
- Relevance: does the connector's relationship map to the buyer's world? A former teammate of the decision maker outranks a friend of someone two floors away.
- Willingness: will this person actually make the intro, promptly? A happy customer says yes. A dormant contact stalls.
Sum the three. A path below your STRENGTH THRESHOLD does not get asked.

### Pick one path per account
Rank the scored paths and pick exactly one. Never spray intro requests across multiple connectors for the same account. Two people asking the same buyer about you looks desperate and burns both relationships. Hold the second-best path in reserve in case the first declines.

### Write the forwardable blurb
Draft the intro request so the connector can forward it in ten seconds without editing. Three sentences: who you are, why this specific buyer should care, and the small ask. The connector adds one line of their own endorsement on top. If they have to rewrite your blurb, you wrote it wrong.

### The fallback rule
When no path clears the STRENGTH THRESHOLD, do not force a weak intro. Go cold instead, anchored to a specific signal, and hand off to trigger-outreach with the signal named. A weak intro is worse than a good cold message. A warm intro skips the trust-building a cold sequence spends weeks earning, but only when the warmth is real.

## Quality gates
- Never claim a relationship you cannot verify. A shared connection on LinkedIn is a lead to check, not a path to score, until someone confirms they actually know the buyer.
- One intro request per account at a time. The reserve path waits until the first path declines or goes quiet for a week.
- The connector always sees the final message before it sends. They are lending you their reputation. No surprises.
- If the fallback fires, the handoff must name the signal the cold message will anchor on, not just "go cold."

## Output (example)
```
WARM PATHS · Meridian Logistics (sample data)
Rank  Connector        Source           Str  Rel  Will  Total  Verdict
1     Dana Okafor      customer (CFO    3    3    3     9      ASK. Worked with their
                       at Bluecrest)                            VP Ops for 4 years.
2     Sam Whitfield    past colleague   2    3    2     7      RESERVE
                       (your AE Priya)
3     Jordan Liu       shared investor  1    2    2     5      BELOW BAR. Do not ask.

The play: one request, to Dana. Forwardable blurb drafted below.
Reserve: Sam, only if Dana declines.

FORWARDABLE BLURB (for Dana):
"Priya leads sales at Fieldstone, they help ops teams cut carrier
invoice errors. Given what Meridian is doing with the new 3PL
rollout, she thought a 20-minute conversation with your VP Ops
could be worth it. Open to a quick intro?"
```

## Example chat
Here is the skill running on a target account, start to finish.

**You:** Find me a warm path into Meridian Logistics. Here's my team list and customer list. [pastes]

**Claude:** Swept the six sources. Three named paths found, scored, and ranked. Dana Okafor, the CFO at your customer Bluecrest, worked directly with Meridian's VP Ops for four years and scores 9 of 9. Sam Whitfield is a past colleague of your AE Priya and holds at 7, reserve. Jordan Liu, a shared investor, scores 5, below your bar of 6, do not ask. The play is one request to Dana, and the forwardable blurb is drafted. One check before you send: confirm with Priya that Sam actually knows the buyer, not just the logo.

**You:** What about Ridgeway Freight? I don't think we know anyone there.

**Claude:** Confirmed. All six sources came up empty, no path clears the bar. Fallback rule applies: go cold, but anchored. Ridgeway posted a Head of Carrier Operations role last week, that is the signal. Hand this to trigger-outreach and open on that hire, not on your product. One sharpener: connect The Swarm so the sweep covers your whole team's network automatically instead of the two lists you pasted.

## Go further
The manual sweep is step one. Here is where an operator takes it once the ranked list proves out.

- **Map the whole team's network, not just yours.** Connect The Swarm so every teammate's relationships get swept against every target account automatically, including the connections nobody remembers they have.
- **Pull mutual connections at scale.** Connect LinkedIn Sales Navigator so past-colleague overlap with the buying committee comes from live data instead of a one-account-at-a-time manual check.
- **Let customers surface themselves.** Connect your CRM and Common Room so current customers with ties to a target account get flagged the moment the account enters your list.
- **Close the loop in Slack.** Post each week's ranked paths and pending intro requests to a Slack channel so connectors get thanked and stalled requests get a nudge.

A path list goes stale fast. People change jobs. Refresh the sweep before every push.

## Make it yours
Fork it. Change the sources, the threshold, the blurb format. The point is not to run someone else's playbook. It is to run yours, faster. Built by an operator. Customize it, break it, make it better.
