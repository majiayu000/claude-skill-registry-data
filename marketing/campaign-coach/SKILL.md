---
name: campaign-coach
description: Turn a finished outbound campaign into a readout your sending agent can actually read. It rebuilds the decisions behind the campaign, ties every number back to one of them, separates what worked from why it worked, and writes one specific change into the list, the angle library, or the instructions. It also names what it could not answer and the one field to start logging so the next readout can. Trigger on "review my campaign", "campaign readout", "how did my last campaign do", "why did that campaign work", "what worked in this campaign", "campaign retro", "campaign post mortem", "analyze this campaign export", "what should I change before the next send", "what should I test next", "coach my outbound agent", "close the loop on outbound", "my agent never learns", or after any outbound campaign finishes. This is for a FINISHED campaign and the one change to make next. For step-by-step drop-off inside a live sequence, use sequence-performance-analyst instead.
---

# Campaign Coach

## What this does
You coach your reps. Nobody coaches your agents.

Your outbound agent has been running for months. It has made a decision on every email it sent, the list it built, the angle it picked, the words it wrote, and not one of those decisions has been reviewed by anything. A rep on that record would be on a plan by now. So the same lesson gets re-taught by hand every time somebody notices it, instead of the agent learning it once.

This skill runs the review. It takes one finished campaign, rebuilds what the agent actually decided, attaches the outcome to each decision, and produces one change specific enough to write back. Reply rate tells you a campaign worked. This tells you why, or tells you honestly that the data cannot say why yet and what to start capturing.

**One campaign, one loop.** It will not blend tiers or roll up a quarter. A blended number hides which motion failed, which is the whole reason nothing gets learned.

## Where this came from
Built live on **Build Better**, the Sell Better series, on 2 September 2026, with Eric Nowoslawski of Growth Engine X taking one real outbound campaign apart on screen. It broke in the place this skill now warns you about, which is why the readout separates what is evidenced from what is only a hypothesis.

- The episode: `https://thesalesoperator.ai/e/ep-004`
- The live event page: `https://content.sellbetter.xyz/live-events/build-better-the-gtm-system-that-improves-itself`

Watching the build is optional. The skill stands on its own.

## Try it in 60 seconds
A sample campaign ships with this skill so you can see the output before you export anything of your own.

1. Grab `sample-campaign.csv` from the skill folder.
2. Say: **"run the campaign readout on this"** and attach it.
3. Read what comes back, then look at the last two blocks. The carry-over is the change. The logging gap is why your own first run will be thinner than this one.

The sample is deliberately small, 60 sends. Watch the skill call it directional rather than conclusive. That is the behaviour you want on your own data too.

## What you'll need
You do not need to connect anything to get value today. A CSV export from your sender is enough.

- **Works today with**: a campaign export with one row per send. Even sends, replies and the list it came from produce a real readout.
- **More powerful with your list build**: the filters the list was built on turn "this worked" into "this filter worked."
- **More powerful with your copy**: the angle and the variant per send is what makes the why answerable at all.
- **Sharper with a CRM**: replies become meetings and opportunities, so you can tell a good reply rate from a good campaign.
- **Sharper with the agent's own instructions**: the readout can be written as the exact diff to the file the agent reads.

## How this runs at your connection level
The skill never depends on a connector. It reasons over the campaign in front of it and gets more precise as you connect the decisions behind it.

- **Bring your data**: paste or point at a campaign export. You get the full readout today, with the unanswerable parts named as unanswerable.
- **Connect your tools**: it reads the sender, the list build and the CRM, so the numbers trace all the way back to a filter and forward to a meeting.
- **Just exploring**: no campaign yet? Ask for the empty readout and the definitions starter, so you can see the shape and set your terms before your first send.

Every run ends with one change, one target, and one thing to start logging.

## Customize this for yourself
This was built for an operator running outbound with an agent or an automation in the middle of it. None of the defaults are sacred. Set these to your setup and the readout speaks your language.

| Set this | What it is | Default / Example |
|---|---|---|
| SENDER | where campaigns run and export from | Instantly, Smartlead, Apollo, Outreach, Salesloft, HubSpot |
| LIST_HOME | where the list gets built and filtered | Clay table, Apollo saved search, a SQL view, a CSV |
| ANGLE_HOME | where your angles and offers are written down | a doc, a Notion database, a folder of markdown |
| INSTRUCTION_HOME | the file the sending agent actually reads | CLAUDE.md, a system prompt, a sequence template |
| CRM | where a reply becomes a meeting | Salesforce, HubSpot, Pipedrive, none |
| TIERS | how you segment campaigns before you compare them | broad, focused, niche |
| POSITIVE_REPLY | what counts as a win, not just a response | see the definitions starter, and write your own |
| COMPARABLE | what makes two campaigns fair to compare | same tier, same offer, within 90 days |
| MIN_SENDS | the floor under which the readout is directional, not conclusive | 300 sends, or 30 replies |
| COPY_CONSTRAINTS | the rules your copy runs under | a word cap, one ask per email, no links in email one |
| FILTER_FLOOR | how many filtering layers a list needs before you trust it | set it once you have run this twice |
| WRITE_BACK | who accepts a change before it reaches the agent | a person, always |

**WRITE_BACK does not move.** An agent that silently rewrites its own targeting is how a team loses the plot. The skill proposes; a person accepts; then it writes.

## The method

### 1. Name the campaign and the tier
One finished campaign. Name it, name its tier, name the offer. If the export contains more than one campaign, it stops and asks which one, because broad, focused and niche fail for different reasons and a blended number hides which one failed.

### 2. Rebuild the decisions before you look at any number
This is the step everyone skips, and skipping it is why readouts change nothing. Before a single metric, reconstruct what the agent actually chose:

- **The list it built.** What filters produced this set. Firmographics, technographics, a trigger, a hand-built account list.
- **The angle it picked.** What problem the email claimed they had, and what it offered.
- **The words it wrote.** The variant, and the constraints the copy ran under.

A number that cannot be attached to one of these three is a number the agent cannot use. Anything that cannot be reconstructed gets listed as unknown, not guessed.

### 3. Attach the outcome to each decision
Not one reply rate. Outcomes cut by the decisions from step 2, so each number rides with the choice that produced it. Reply rate by filter. Reply rate by angle. Reply rate by variant. Where the CRM is connected, the same cuts carried through to meetings, because a good reply rate on a bad list is a good reply rate.

Every figure carries its denominator. A 12 percent reply rate on 25 sends is three replies and it is not a finding.

### 4. Separate what worked from why it worked
Two lists, never blended.

- **Evidenced.** The difference is visible in the data and the sample supports it.
- **Hypothesis.** A plausible reason that this campaign cannot confirm. It is written as a question with the test that would settle it.

Most first runs are mostly hypotheses. That is the honest answer and it is the point. The reason a campaign worked usually lives nowhere, not in the reply, not in the CRM, not in the agent, because nobody captured it.

### 5. The carry-over
One change. Specific enough to write back, aimed at exactly one target:

- **The list**, a filter to add, drop, or tighten.
- **The angle library**, an angle to retire, promote, or bound to a segment.
- **The instructions**, a constraint the agent must obey on the next send.

It is written as the edit to the file, not as advice. "Add a headcount growth filter" is advice. "In LIST_HOME, add: headcount growth over 10 percent in the last 6 months" is a change.

If nothing in the data supports a change, it says so and stops. A forced change is worse than none.

### 6. The logging gap
The most useful output of a first run. What the readout could not answer, and the single field to start capturing so the next one can. Usually the angle, the variant, or the filter set, recorded at send time rather than reconstructed after.

This is what turns one review into a loop. Without it, the next readout is as blind as this one.

### 7. The human gate
The readout is presented for a yes or a no on each proposed change. Nothing reaches LIST_HOME, ANGLE_HOME or INSTRUCTION_HOME until you accept it. Accepted changes are written as a dated entry so the next readout can tell whether the change did anything.

## Quality gates
- No number without the decision it traces to. Reply rate on its own is a scoreboard, not coaching.
- Every figure carries its denominator, and anything under MIN_SENDS is labelled directional.
- Evidenced and hypothesis are never blended. A guess is labelled a guess.
- One campaign, one tier. It refuses to roll up.
- No metric is invented. If the export does not contain it, it is listed as missing, not estimated.
- At most one carry-over change per run, aimed at one named target. If the data supports none, it proposes none.
- Every run ends with a logging gap, even a clean one.
- Nothing writes back without a person accepting it. WRITE_BACK is off and stays off.

## Output (example)

```
CAMPAIGN READOUT · "Ops leaders, Q3 trigger" · tier: focused · 1,240 sends

THE DECISIONS BEHIND IT
  List       6 filters. Headcount 200-1000, hiring an ops role in 90d,
             uses a named billing tool, US, not a current customer, not in
             an open opp.
  Angle      "Your billing ops is a headcount problem you can stop hiring for."
  Copy       78 words avg, one ask, no link in email one.
  Unknown    Which variant each send used. Not recorded at send time.

WHAT HAPPENED
  Sends 1,240 · replies 71 (5.7%) · positive 22 (1.8%) · meetings 9 (0.7%)

  BY FILTER
    hiring an ops role in 90d      41 of 380 replied   10.8%   positive 16
    no hiring trigger              30 of 860 replied    3.5%   positive  6
  BY ANGLE
    headcount angle                only angle used. No comparison available.

WHY IT WORKED
  EVIDENCED
    The hiring trigger is doing the work. 3x the reply rate and 73% of the
    positives came from 31% of the sends. n=380, the gap holds.
  HYPOTHESIS
    The 78 word cap may be carrying some of this. This campaign cannot say,
    every email ran under the same cap. Test: hold the trigger, run one arm
    at 120 words.

THE CARRY-OVER · one change · target: LIST_HOME
  Add as a required filter, not a boost:
      hiring an ops role in the last 90 days
  Everything without it replied at 3.5% and produced 6 positives from 860
  sends. That is the floor you are paying for.

THE LOGGING GAP · start capturing: variant ID at send time
  Every "why" question this readout could not answer came back to not knowing
  which words went to whom. One field fixes it and makes the next readout
  twice as useful.

ACCEPT? The change above writes to LIST_HOME. Nothing has been written yet.
```


## What a thin export gets you
Worth knowing before you run it, so a thin first result reads as a data problem rather than a skill problem.

| What your export has | What you get | What you cannot get |
|---|---|---|
| Sends and replies only | The totals, and an honest statement that nothing here traces to a decision | Any why. Any carry-over change |
| Plus the list attributes you filtered on | Reply rate by filter, and usually one real carry-over | Why the copy worked |
| Plus the angle and variant per send | The copy questions become answerable | Whether a reply became money |
| Plus the CRM outcome | The full readout, and the ability to catch a filter that lifts replies and produces nothing | |

If you only ever add one thing, add the list attributes. That is the difference between knowing a campaign worked and knowing what to change.

## The definitions starter
The readout is only as good as your terms. An agent cannot apply a definition nobody wrote down, and every argument about whether a campaign worked is really an argument about one of the lines below.

Copy this into wherever your agent reads its instructions, usually a `CLAUDE.md`, a system prompt, or a file your sequence template points at. Fill it in once. Leave a line blank rather than guessing, because the readout will flag a blank and quietly trust a guess.

```
# Campaign definitions

POSITIVE_REPLY
  A reply worth the next email, not just a response.
  Ours:
  Ruled on already: referral to a colleague / "circle back in Q3" /
  auto reply naming a successor / reply from someone not on the list.

TIER
  Campaigns only compare fairly within a tier.
  Broad   = ?   testing whether the angle carries at all
  Focused = ?   testing whether the trigger is real
  Niche   = ?   testing whether the research pays for itself

COMPARABLE
  Two campaigns are fair to compare when:
  (example: same tier, same offer, both fully sent, within 90 days)

FILTERING_LAYER
  One condition a record passes to make the list.
  Ours on a typical list: 1. 2. 3.
  Required removes a record. A boost only reorders. Mark which is which.
  Our floor: leave blank until two readouts have run. It is a finding.

COPY_CONSTRAINTS
  Word cap:            Asks per email:
  Links in email one:  Claims we will not make:
  Personalization floor (what must be true, not just a merge field):

IT_WORKED
  The outcome the campaign is judged on. Pick the furthest down the funnel
  you can actually measure.
  Ours:
  Minimum sample before we call anything:

DECISION_SURFACES
  Where a lesson has to land for the agent to read it next time.
  The list:            accepted by:
  The angle library:   accepted by:
  The instructions:    accepted by:
  Nothing writes to these without a person accepting it.
```

The full version, with the edge cases and a worked example for every term, is `DEFINITIONS.md` beside this file:
`https://github.com/heath-gtm/Skill-Builder/blob/main/skills/campaign-coach/DEFINITIONS.md`

## Worked setups
`EXAMPLES.md` beside this file carries four setup levels and the cuts per campaign type:
`https://github.com/heath-gtm/Skill-Builder/blob/main/skills/campaign-coach/EXAMPLES.md`

The short version:

- **Level 1, a CSV.** One row per send, plus the list attributes you filtered on. That last part is what most people leave out, and leaving it out is why most readouts change nothing.
- **Level 2, add the list layer.** Your sender knows what happened. Your list layer knows why those people were on the list. The readout lives in the join. If you connect one more thing, connect the list.
- **Level 3, add the CRM.** This is what separates a good reply rate from a good campaign. A filter can lift replies and produce nothing.
- **Level 4, point it at the instructions.** The carry-over gets written as the diff to the file the agent reads, instead of a note you transcribe.

The method never changes. What changes is what you cut the numbers by: a trigger campaign cuts by has-trigger against no-trigger, an angle test cuts by angle with the list held constant, a broad send cuts by firmographic band, a named account list cuts by research depth and says directional and means it.

If you have neither file, run the skill anyway. It will tell you which definitions it had to assume.

Sample data: `https://github.com/heath-gtm/Skill-Builder/blob/main/skills/campaign-coach/sample-campaign.csv`
