---
name: x-plan
description: >-
  Plan the user's week on X - what to post, when to post it, and who to engage
  with. Use when the user says "plan my week", "what should I post", "content
  calendar", "posting schedule", "I have nothing to post about", or wants a
  weekly mix of posts, threads and replies and a list of accounts to engage.
---

# x-plan

The control room. Everything else in this pack executes; this decides what
gets executed. Run it once a week, on the same day.

One tool lives in this folder:

```bash
python3 weights.py          # what X's ranker rewards and punishes, live from X's own code
```

## Input

Read these if they exist: `~/.claude/x/voice.md`, `log.md` (what was posted,
with which formula), `swipe.md` (what is working in the niche, from
`/x-viral`) and the last `/x-audit` result. The plan should not repeat a theme
from the last fortnight, and it should lean on what the user's own evidence
says works.

If they do not exist, ask four things and write them down:

1. What the user sells, and to whom.
2. The three or four topics they want to be known for.
3. What actually happened this week: a number, a client, a mistake, a thing
   they built, an argument. This is where posts come from.
4. Twenty accounts in their niche, from much bigger to about their size.

## What to post

X moves faster than other platforms and rewards presence, but volume is not
the lever people think it is. A working default for a solo account:

| format | per week | job |
| --- | --- | --- |
| **Post** | 5-7 | one idea, one to three lines. The workhorse. `/x-post` |
| **Thread** | 1-2 | the week's best ideas, with steps. `/x-thread` |
| **Quote** | 1-2 | your take on the week's news in the niche |
| **Poll** | 0-1 | only when the answers are next week's post |
| **Video / image** | 1 | a screen recording or a chart beats a stock image |
| **Replies** | 10-30 a day | on other people's posts. `/x-comment`. This is the growth |

Two limits worth knowing: X caps unverified accounts at 50 original posts and
200 replies a day. Nobody should get near either.

For each slot give the topic, the specific angle drawn from what actually
happened this week, and the hook formula number from `../x-post/hooks.json`.
Not a topic, an angle. "AI" is not a plan. "The proposal I lost because the
draft had an em dash in it" is a post.

## What X actually rewards

Run `python3 weights.py` and read the output to the user in one paragraph.
The shape to plan around: replies, quotes and shares are weighted far above
likes, a reply between two accounts that follow each other gets extra, and
mutes, "not interested" and reports are weighted heavily against you. The
file's own comments say these apply to predicted probabilities, not counts,
so do not turn them into "a reply = 10 likes".

Two practical consequences:

- **Plan for replies, not likes.** A post that asks for a reply honestly (a
  specific question, a claim people will argue with) beats a post built for
  applause.
- **Engagement pods do nothing.** X's code comments say engagement only
  counts toward ranking when the post was served in the viewer's home
  timeline; sending people to the post from a group chat has no ranking
  impact.

## When to post

When the user's audience is awake and scrolling, in the audience's timezone:
weekday mornings and lunch are the working default for a professional
audience. Say this plainly as well: **the hour matters far less than the
first line.** If the user is tuning posting times before their hooks work,
they are polishing the wrong thing.

The better timing lever is the hour after posting: be there to reply.

## Who to engage with

A list of 10 for the week, split:

- **5 reach**: bigger accounts whose posts the user can genuinely add to.
  Turn on their post notifications and reply in the first 15 minutes.
- **3 peers**: same size, same niche. They reply back, and replies between
  mutuals are the ones X boosts.
- **2 buyers**: people who could buy. Reply to their posts for weeks before
  any DM, and never pitch in a reply.

## Output

```
WEEK OF SEP 28

MON  9:00   THREAD  #16 Thread Promise  - the 40 viral posts I read, what they shared
TUE  8:30   POST    #9  Time Anchor     - proposals, 5 hours to 20 minutes
WED  12:00  POLL    -                   - "which do you pay for" (answers = Friday's post)
THU  9:00   THREAD  #2  Number Reveal   - 90 days of daily posting, what moved the numbers
FRI  5:00   VIDEO   #15 The Launch      - 40-second screen recording of the new tool
SAT  10:00  POST    #21 The One-Liner   - (from Wednesday's poll result)
SUN  7:00   QUOTE   -                   - the week's biggest niche news, your take

DAILY  20 replies before posting, not after. List below.

ENGAGE  (5 reach / 3 peers / 2 buyers)
  ...

Say "write Tuesday" and I will draft it.
```

Write the plan to `~/.claude/x/plan.md` so the other skills can read it.
Nothing is scheduled or posted anywhere. This is a plan, and the user runs it.
