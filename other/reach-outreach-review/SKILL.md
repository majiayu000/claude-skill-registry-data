---
name: reach-outreach-review
description: Reviews your outreach from your own log, with your counts by reason, channel and warm or cold, what you expected and what happened, what the small numbers can and cannot tell you, what you would keep and the one thing to change. Use for "run reach-outreach-review", "outreach review", "what worked in my outreach", "review my prospecting", "is my outreach working", "which messages got replies", "analyse my outreach results", "monthly outreach review", part of the Claude Guide for Outreach Pack by Polar Bear.
---

# Outreach Review

## When To Use
You have no way to tell what worked. A few runs are behind you and you remember the one great reply and nothing else. This answers: what did I expect, what do my own counts show, and what one thing is worth changing?

## When Not To Use
With fewer than two finished runs there is too little to review: keep the log and come back. If you already know the one change you want to try, go to Next Run Test. This is not a comparison with anyone else's results.

## Inputs
- Your Outreach Log for the runs you want to review.
- What you expected before these runs, if you wrote it down, or as you remember it.
- The smallest count below which you do not want any comparison made. You set it.
If you have none of this, I start from counts you give me from memory and mark the whole review "from memory, low confidence".

## Approach
A review of expected against actual, in four questions: what did I expect, what happened, why the difference, what do I keep or change. It is an old practice in teams that learn from their own operations, described here generically. The counts are yours and only yours: reply rates and benchmarks published online come from tool vendors, disagree with each other and are not used. With about ten messages a run, most differences are noise, and the review says so. The failure it prevents: dropping what works because of one silent week.

## Workflow
1. Ask at most three questions: which runs to review, what you expected, and your minimum count for any comparison.
2. Count from the log, as plain numbers: people written to, replies, first calls, do not contact requests; then the same split by reason used, by channel, and by warm path or cold.
3. Show counts, not percentages, wherever a group is below your minimum. "2 of 7" is honest; a percentage of seven is not.
4. Set what you expected beside what happened, line by line. Where there is a gap, list possible explanations as possibilities, including "chance" every time the numbers are small.
5. Say what these numbers cannot tell you: whether one reason is better than another, anything about the people who did not reply, anything about next month.
6. Name what you would keep, with the count behind it, and what looks worth changing.
7. End with one candidate change. One. The rest go on a list for later.

## Output Format
```markdown
# Outreach Review
Runs reviewed: [numbers, dates] | People written to: [count] | Minimum count for comparison: [your number]
## What I expected and what happened
| | Expected | Happened (count) |
|---|---|---|
| Replies | [your expectation] | [count of count] |
| First calls | [your expectation] | [count of count] |
## My counts
| Split | Written to | Replies | First calls |
|---|---|---|---|
| Warm path | [count] | [count] | [count] |
| Cold with a trigger | [count] | [count] | [count] |
| By reason: [reason] | [count] | [count] | [count] |
| By channel: [channel] | [count] | [count] | [count] |
## What these numbers cannot tell me
- [limit, in one line]
## Keep, and one thing to change
Keep: [what, and the count behind it]. Change: [the one candidate change]. Parked for later: [others].
## Decision
[Your name] decides by [date] whether to test the one change in the next runs or keep everything as it is.
```

## Done When
- Every number comes from your log and is shown as a count.
- No percentage appears for a group below your minimum.
- No outside benchmark or rate appears anywhere.
- Exactly one change is proposed, and the limits are stated.

## Quality Bar
- Counts describe your outreach, never the people you wrote to.
- "Chance" is listed as an explanation whenever numbers are small.
- No person is singled out as a good or bad contact.
- A review that says "too little to tell" is a complete review.
- Your own numbers only, with nothing invented; you decide what to keep and what to change.

## Next
Run reach-next-run-test (Next Run Test) to try the one change properly over the next runs.

## About the makers

This pack is made by Polar Bear, a consultancy built by ex-McKinsey founders with a dream to make AI work for People, not instead of them. We help our clients build people systems and AI-first ways of working, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
