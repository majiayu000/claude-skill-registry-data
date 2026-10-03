---
name: so-what-test
description: Translate analysis findings into an actionable insight using three labeled sections (Process, Result, Insight). Use when the user has data but needs a recommendation, when an analysis ends without action, or step 5 of a strategic analysis.
---

# The "So What?" Test

## Concept

Most analyses fail at the last step. People surface findings, lay out data, and stop — leaving the reader to figure out what it means and what to do. The "So What?" test forces you to close the loop: every finding must lead to an action specific enough to assign.

A finding without a "so what" is trivia. A finding with a "so what" is a recommendation.

## Required output format

Three explicitly labeled sections, in this order:

```markdown
**Process:** [What specific data, workflow, or factor was analyzed.]

**Result:** [The objective outcome — numbers, signals, observations.]

**Insight:** [The underlying reason this matters + the immediate action. Specific enough to assign to a person with a deadline.]
```

## Defaults & flex points

| Default | When to flex |
|---|---|
| Process is one or two clauses | Don't flex — long preamble buries the answer. |
| Result has numbers or specific observations | Don't flex — vague Results undermine the Insight. |
| One Insight per block | If multiple actions are warranted, write multiple So What blocks rather than one Insight with three bullets. |
| Insight names who, what, and by when | Don't flex — that's the test. |

**The assignability test:** could you copy your Insight into an assignment to a named person with a deadline, and would they know what to do? If not, rewrite it.

## Example — HR / people analytics

**Problem:** Mid-level engineering attrition has risen for three consecutive quarters. The VP of Engineering wants to know why and what to do.

### Bad

**Process:** Looked at attrition data.

**Result:** Attrition went up.

**Insight:** We should focus on retention.

(Process is too vague. Result has no number. Insight is unassignable. Three failures.)

### Better

**Process:** Joined exit-interview transcripts (n=24) with promotion-cycle data, comp-band placement, and manager-tenure data for all mid-level engineers (L4–L5) who left between Q2 of last year and Q1 of this year. Compared to a control cohort of L4–L5 engineers who stayed.

**Result:** 18 of the 24 leavers (75%) cited "no clear path to promotion" as a top-3 reason in their exit interview. Of those 18, 14 had been at level for >24 months — twice the median tenure-at-level (12 months) for the staying cohort. Comp-band placement was median or above for 17 of 18, ruling out pay as a primary driver.

**Insight:** This is a promotion-velocity problem, not a comp problem. The mid-level leavers we lost most often had been stuck at level for 24+ months — well beyond the band's expected tenure — without a clear path forward. **Action:** by end of next month, the VPE and Head of People run a calibration review of every L4–L5 engineer at level for >18 months (estimated 31 people); identify which are promotion-ready, which need a stretch project to close gaps, and which are genuinely capped. Communicate outcomes to managers by mid-quarter, then track 6-month retention of the cohort. Owner: VPE, with People partnering. Target: cut mid-level attrition from 18% to below 11% by year-end.

(Process is specific. Result has numbers, comparisons, ruled-out alternatives. Insight is assignable: who, what, by when, what success looks like.)

## Common mistakes

- **"Insight" that's a Result restated.** "Insight: attrition is high" — no, that's the Result.
- **Action without a target.** "Improve retention" — for whom? By how much? Good Insights answer those.
- **Strategy without specificity.** "We need to invest in talent development" is a slogan, not an insight.
- **Long preamble in Process.** Process should be tight. Save the substance for Result and Insight.

## When to use this skill alone vs. as part of the full analysis

- **Standalone:** when the user has data and findings already and needs help converting them into a recommendation.
- **As part of full analysis:** `strategy-consultant` — the So What? test is step 5 of 5, where everything lands.

---

## Acknowledgment & License

Adapted from **Analyst Academy** on YouTube — [5 Consulting Frameworks to Solve Any Problem](https://www.youtube.com/watch?v=uCmTk06aM70). MIT-licensed; see [LICENSE](../../LICENSE).
