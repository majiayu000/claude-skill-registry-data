---
name: trade-journal
description: Use when reviewing trading performance and decisions. Covers what to record, separating process from outcome, identifying real patterns in your own behavior, and turning a review into a rule change.
metadata:
  category: finance
  version: 1.0.0
  tags: [journal, review, process, postmortem, discipline]
---

# Trade Journal

## Purpose

Learn from your own decisions rather than from your outcomes. A profitable trade taken against your rules is a bad trade that will be repeated; a losing trade taken correctly is a good one. Without a journal, these are indistinguishable.

## When to Use

- Recording a trade at entry.
- Reviewing performance over a period.
- After a losing streak, to determine whether the process or the market changed.
- Identifying recurring mistakes.

## Capabilities

- Structured trade recording: thesis, plan, execution.
- Process-versus-outcome separation.
- Pattern identification across trades.
- Rule-adherence tracking.
- Converting findings into rule changes.

## Inputs

- The trades: entry, exit, size, and — crucially — the reasoning at the time.
- The plan as it was stated *before* the outcome was known.
- Market context.

## Outputs

- A record that permits honest review.
- Identified patterns, not anecdotes.
- Specific rule changes with a date.

## Workflow

1. **Record the thesis before the outcome** — At entry, in writing: why, where the stop is, where the target is, and what would prove the thesis wrong. Written afterwards, this is a rationalization, and it will be a flattering one.
2. **Grade the process, not the profit and loss** — Did you follow your rules? That is a binary question with a clear answer, and it is the only one you control.
3. **Categorize by setup and by mistake** — Not by outcome. "Chased an extended entry" is a category. "Lost money" is not.
4. **Review a sample large enough to be meaningful** — Twenty trades minimum. Any five trades can be attributed to anything.
5. **Look for the pattern, not the story** — Are the losses concentrated in one setup? One time of day? Trades taken after a loss? These are behavioral patterns and they recur.
6. **Change one rule, and date it** — Then measure whether it helped. Changing five rules at once means learning nothing.

## Best Practices

- The most common and most costly journaling error is writing the thesis after the outcome is known. Memory is not merely imperfect; it actively reconstructs the past to justify the present.
- Grade every trade against the rules, independently of whether it made money. A rule violation that was profitable is the most dangerous event in trading, because it is reinforced.
- Look for the revenge trade: the position taken immediately after a loss, larger than the rules permit, in a setup you would normally skip. It is nearly universal and it is visible in the data.
- Track the trades you did *not* take. A rule that keeps you out of losers is doing its job, and it is invisible without a record.
- Screenshot the chart at entry. Your memory of what the setup looked like will drift toward whatever justifies the outcome.
- A journal you do not review is a diary. The review is the entire point.

## Examples

**A trade record that permits an honest review:**

```markdown
## 2026-06-14 | LONG NVDA | Momentum breakout

**Written at entry, before the outcome.**

Thesis      : Breaking out of an 8-week base on 2.3x average volume. Relative
              strength +6% vs SPY over 63 days. Earnings are 5 weeks away.
Entry       : 118.40
Stop        : 112.80 (below the base low; the breakout is invalid below it)
Target      : 134.00 (the measured move; 2.8:1 reward-to-risk)
Size        : 340 shares. Risk $1,904 = 0.95% of equity. Within the rules.
Invalidation: A close below 112.80, or a failed breakout that closes back
              inside the base.

Regime check: trend up, volatility contracting. Breakouts are favored. PASS.
Pre-trade gate: PASS (stop set, risk within limit, sector exposure 18%/30%).

---
**Written at exit.**

Exit        : 113.10 on 2026-06-21. Stopped out. -$1,802 (-0.90%).

Process grade: A. The setup met every criterion. The stop was where the thesis
               was invalidated. The size was correct. It was executed as
               planned and it did not work.

Outcome     : Loss.
Lesson      : NONE. This is what a losing trade taken correctly looks like.
              Do not change anything on the basis of this trade. The breakout
              failed. Some do.
```

**The review that finds the actual pattern:**

```text
Q2 review: 47 trades.

By outcome:      21 winners, 26 losers. Net +2.1%.
By process grade: 38 followed the rules, 9 did not.

The finding is in the second line, not the first:

  Rule-following trades (38): +8.4%   win rate 55%   avg R  +0.31
  Rule-breaking trades   (9): -6.3%   win rate 22%   avg R  -0.70

Every rule-breaking trade shares one characteristic: it was entered within
90 minutes of closing a losing position. Seven of the nine were in a setup
graded "C" or worse. Six were oversized.

This is a revenge-trading pattern. It is not a strategy problem; the strategy
made 8.4% this quarter. It is a behavioral problem that cost 6.3%.

Rule change, effective 2026-07-01:
  No new position within 2 hours of closing a losing trade. No exceptions,
  no override. This is a hard gate, enforced in the pre-trade checklist,
  not a resolution to be more disciplined.

Measure: count rule-breaking trades next quarter. Target: zero.
```

## Notes

- The revenge-trading pattern in the example is close to universal among discretionary traders and is invisible without a journal — every individual instance feels justified in the moment.
- The rule change is a mechanical gate, not a resolution. "I will be more disciplined" has never worked for anyone. A rule that cannot be overridden has.
- This is educational material about trading process and review, not financial advice.
