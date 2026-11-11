---
name: reel-scorecard
description: "Reads trial-reel and TikTok results at 72 hours and says which hook won each idea, which reel to graduate to the main feed (the creator taps it), which hooks to kill and which ideas to retire, using matched windows and one data source so numbers are comparable. Pulls Zernio analytics read-only (or a CSV export), joins them to the trial-post ledger, and writes SCORECARD.md plus a weekly learning log that changes at most one rule a week. Use for 'scorecard', 'which hook won', 'what should I graduate', '72 hour results', 'how did the trials do'."
author: Johann (@johannships)
version: 1.0.0
---

# Reel scorecard: the 72-hour read

Last step of the pipeline: idea -> script -> record -> "the card is in" -> edit -> `trial-post` -> **reel-scorecard**,
and it feeds the next `reel-ideation` run (winning hooks and formats get copied again, losers retire).

## Requirements

Claude Code (or Claude.ai with a CSV export pasted). The Zernio MCP connector for read-only analytics, and the
`trial-post` ledger (`$HOME/.trial-post/ledger.jsonl`), which carries each post's idea and hook ids.
`cp config.example.json config.json` to change the thresholds.

## Rules that keep the numbers honest

- **Same source, same window.** Only Zernio numbers against Zernio numbers, only 72 to 96 h old against each other.
  Instagram insights lag up to 48 h, TikTok fills in 24 to 48 h: a 24 h look is a peek, never a decision.
- **Views are shown, never used alone.** Instagram: skip rate and hold (average watch / length) decide. TikTok:
  completion rate first, For You share next to it.
- **No peak without its decay.** Quote a number with its window and date, or do not quote it.
- **Follows are not in the API for reels.** The creator checks follows for the finalists in the app before graduating.

## Steps

1. **Pull (read-only).** For every ledger post 72+ h old: `mcp__zernio__analytics_get_analytics` with `post_id`
   (or with `platform` + `from_date` for a batch, paginated). Save each result to `scorecard/raw/<date>-<n>.txt`.
2. **Score.** `python3 scripts/scorecard.py --ledger $HOME/.trial-post/ledger.jsonl --analytics scorecard/raw/*.txt --out scorecard/<date>.md`
3. **Read it out** to the creator, short: per idea, the winning hook and why (skip, hold), graduate candidates
   (max 2 a day so the main feed is not flooded), kills, retirements, and what is not in the window yet.
4. **Graduation is the creator's tap**: Instagram app > the trial reel > "Share to everyone". There is no API for
   it. One graduation per idea. Never re-upload the trial file through another scheduler (duplicate content);
   a main-feed repost of a winner is a new cut or a new take.
5. **Weekly learning log** (once a week): for every idea with 2+ hooks scored, which hook TYPE won (callout, belief
   flip, proof...), which format, which opening visual. Append to `scorecard/LEARNING-LOG.md`. Change at most ONE
   rule per week, and only after 3+ tests agree. Feed the winners to the next `reel-ideation` run.

## Default thresholds (config.example.json; tune with your own numbers after two weeks)

| decision | Instagram rule |
|---|---|
| graduate candidate | lowest skip AND hold >= 28% AND skip < 55% AND >= 1,000 views |
| split | best skip and best hold on different hooks: the creator picks |
| tie | skip within 2 points (skip rate is an estimate) |
| kill | skip >= 65%: that hook never graduates and is not reused on that idea |
| retire the idea | every hook >= 60% skip and under ~1,300 views |

These come from one creator's account; they are a starting point, not a law.

## Output

```
scorecard/
  raw/<date>-<n>.txt     saved analytics results (never edited)
  <date>.md              the scorecard
  LEARNING-LOG.md        one dated block per week, the one rule changed (if any) and the tests behind it
```

## Failure handling

- A post missing from analytics: it may still be processing; list it under "not in window yet".
- Ledger has no idea/hook ids (old posts): add them by hand to the ledger lines, or score those posts by eye.
- Numbers look impossible (skip 0, views 0 after days): say so, do not decide on them, check the post in the app.
