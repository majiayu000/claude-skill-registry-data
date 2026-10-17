---
name: kpi-review
description: Review marketing KPIs and produce an executive summary with insights, anomalies, and recommended actions using the Storytelling with Data framework (Cole Nussbaumer Knaflic). Every review starts with a Big Idea - one sentence capturing the insight, its implication, and why it matters. Use when the user asks for a KPI review, monthly metrics review, marketing dashboard review, "review last month's numbers", quarterly review, performance review, or wants to analyze marketing data. Reads kpis.md and any uploaded data files. For planning a campaign against these numbers, see campaign-brief. For the post-campaign learning loop, see retro. For setting the baseline itself, see brand-context.
metadata:
  grounded_in:
    - "Storytelling with Data - Knaflic"
  reads:
    - knowledge/kpis.md
    - knowledge/learnings.md
    - knowledge/icp/personas.md
  writes:
    - output/kpi-review/
    - knowledge/kpis.md (appends snapshot)
---

# kpi-review

Acts as the user's data strategist. Reads KPIs, spots anomalies, recommends actions. Applies the Storytelling with Data framework (Cole Nussbaumer Knaflic) - every review has one Big Idea, every anomaly has a narrative arc, and every data display has a recommended chart type. Moves from analysis to actions: every review ends with three concrete next steps tied to specific insights, not generic observations.

## Framework: Storytelling with Data

### The Big Idea
Every data communication needs one singular "so what" - a single sentence that captures the insight + its implication + why it matters.

Data: "Our trial-to-paid rate dropped 4 points MoM."
Big Idea: "Our trial-to-paid rate dropped 4 points MoM, which means we're leaving $280K of ARR on the table this quarter unless we fix onboarding."

The Big Idea Worksheet (complete before analyzing):
1. What is the one thing I want the audience to know?
2. What do I want them to DO with that information?
3. Complete this sentence: "We need [audience] to [action] because [evidence]."

### Chart Type Rules
Match the display to the message. Never use 3D charts. Never use pie charts with more than 4 slices.
- Change over time: line chart
- Part of a whole: bar chart (preferred over pie)
- Comparison: bar chart side by side
- Relationship: scatter plot
- Ranking: horizontal bar chart

### Eliminate Clutter
Every element in a chart earns its place. Remove gridlines, legends (annotate directly), dual axes, unnecessary color variation.

### Focus Attention
Use pre-attentive attributes to direct the eye: color, size, position. Make the most important number impossible to miss.

### Narrative Arc for Anomalies
Data without narrative is noise. Every anomaly gets: situation (what happened) - complication (why it matters) - hypothesis (probable cause) - recommendation (what to do next).

## When to use

- "Review last month's KPIs"
- "Run a monthly metrics review"
- "Analyze our Q3 performance"
- "What does this dashboard tell us?"
- "Review our marketing numbers"

## Inputs needed

- **Period**: last week, month, quarter, custom range (default: last calendar month)
- **Data source**: file in `uploads/` (CSV from dashboard), pasted numbers in chat, or read from `knowledge/kpis.md` snapshots
- **Comparison baseline**: prior period, target, or both (default: both)

## Process

1. **Load context.** If `knowledge/kpis.md` does not exist, stop and say: "I need KPI context to run this review. Run `/brand-context` first to define your metrics and targets." Otherwise read it to know which metrics matter and what the targets are. Read `knowledge/learnings.md` for context on prior anomalies and what was tried.

2. **Read the data.** If a CSV or report is in `uploads/`, parse it. If the user pasted numbers, work from chat. If neither, stop and ask: "Drop the data into `uploads/` or paste the numbers here."

3. **Write the Big Idea first.** Before building the review, complete the Big Idea Worksheet:
   - What is the one thing the reader needs to know from this period?
   - What action should they take?
   - Draft the Big Idea sentence: "[metric/trend] which means [implication] unless [action]."
   This becomes the TL;DR. Verify or revise it after analyzing all the data.

4. **Build the review in this format**:

   ```
   # KPI review: <period> (DD-MM-YYYY)

   ## TL;DR - Big Idea (read this if nothing else)
   [One sentence. Insight + implication + action. Readable in 10 seconds.]
   - **What's working**: <one sentence>
   - **What's broken**: <one sentence>
   - **What to do this week**: <one sentence>

   ## Metrics snapshot
   | Metric | Period | Prior | Target | Delta vs prior | Delta vs target | Chart type |
   |---|---|---|---|---|---|---|
   | MRR | $X | $Y | $Z | +12% | -3% | Line (trend) |
   | Pipeline | ... | ... | ... | ... | ... | Bar (comparison) |

   ## What changed and why
   For each metric that moved >10% or missed target by >10%:
   - **<Metric> moved <up/down> <X%>**
     - Situation: what happened, in one sentence
     - Complication: why this matters, what it puts at risk
     - Hypothesis: 2-3 probable causes ranked by likelihood
     - Recommendation: one specific action to validate or fix
     - Confidence: high / medium / low

   ## Anomalies
   For each anomaly, use the narrative arc:
   - **<Anomaly name>**
     - Situation: [what the data shows]
     - Complication: [why it's unexpected or concerning]
     - Hypothesis: [most likely explanation]
     - Recommendation: [what to do or investigate]
   Include: numbers that don't fit the pattern, diverging cohorts, channels that suddenly outperform or underperform, anything requiring a raw data look.

   ## Recommended actions
   Three actions, ranked. Each must connect to a specific Big Idea insight.
   - **What to do**
   - **Which insight it addresses** (tie directly to a finding above)
   - **Effort**: low / medium / high
   - **Expected impact**: which metric, by how much, by when

   1. ...
   2. ...
   3. ...

   ## Open questions
   Things you cannot answer from the data. The user should investigate or pull more data.

   ## What I don't know
   Be explicit about gaps. "I cannot say if the LinkedIn drop is seasonality or algorithm change without comparing to same period last year."
   ```

5. **Propose the snapshot, show it in full, and append to `knowledge/kpis.md` only on explicit
   approval.** Every snapshot line carries its source file and any `[UNVERIFIED]` tag from the
   input. Without this gate, numbers parsed from an arbitrary upload become the permanent
   longitudinal record every future target is measured against, with no provenance.

   Append to `knowledge/kpis.md`: add a snapshot at the bottom of the file:
   ```
   ## Snapshot DD-MM-YYYY
   - MRR: $X
   - Pipeline: $Y
   - <metric>: <value>
   - Big Idea this period: [one sentence]
   ```
   This builds a longitudinal record over time.

6. **Self-check**:
   - TL;DR is the Big Idea - one sentence, readable in 10 seconds, action-oriented
   - Can the reader know what to DO in 10 seconds from the TL;DR? If not, rewrite it.
   - Every anomaly has all four narrative arc elements (situation, complication, hypothesis, recommendation)
   - Every metric in the snapshot table has a chart type note
   - Three actions are concrete (verbs, not "consider") and each tied to a specific finding
   - Confidence levels are explicit
   - "What I don't know" section is not empty (there is always something)

7. **Save** to `output/kpi-review/<DD-MM-YYYY>-<period>.md` with frontmatter:
   ```yaml
   ---
   format: kpi-review
   period: <period>
   start: DD-MM-YYYY
   end: DD-MM-YYYY
   big-idea: <one sentence>
   created: DD-MM-YYYY
   ---
   ```

8. **Offer follow-ups**:
   - Run `/retro` if a campaign just ended
   - Remind the user: "Set a calendar reminder to run `/kpi-review` again on [first of next month]."
   - Update `knowledge/kpis.md` if any targets need to change

## Rules

- Never invent numbers. If the data is incomplete, say so.
- Never recommend an action that is not tied to a specific insight in the review. No generic best practices.
- Every action must connect back to the Big Idea or a named anomaly. If the connection is not obvious, it is the wrong action.
- Confidence levels are required. "MRR dropped because of X" without a confidence label is not a finding.
- The "What I don't know" section is mandatory. If you skip it, you are pretending to know more than you do.
- The Big Idea is mandatory. If every metric looks fine, the Big Idea is "Everything is on track - the one risk to watch is X." There is always a so what.

## Handling [UNVERIFIED] and [NEEDS INPUT] tags

`brand-context` tags any number the user was unsure of as `[UNVERIFIED]`, and several skills tag
gaps as `[NEEDS INPUT]`. Those tags are a contract, and it only works if this skill honours it.

1. **Carry the tag forward.** If a baseline, benchmark or proof point arrives tagged, every figure
   derived from it is tagged too. A target built on an unverified baseline is an unverified target.
2. **Never silently promote.** Do not drop the tag because the number looked confident in the
   source file.
3. **Say it in the output.** List every tagged input in its own line near the top, so a reader
   knows which numbers are measured and which are estimates before they act on them.
4. **A decision that would change if the tagged number were wrong must say so explicitly.**

## Choosing the chart, and what each one asserts (Knaflic)

Cole Nussbaumer Knaflic's rule is that the chart type is an argument, not decoration. Pick by the
claim you are making, and if none of these fits, the claim is not clear enough yet.

| The claim | Chart | Fails when |
|---|---|---|
| This changed over time | Line | Fewer than 5 points, where a line implies a trend that is not there |
| This is bigger than that | Horizontal bar | Categories exceed about 8 and the reader stops comparing |
| This is a share of a whole | Stacked bar, not a pie | More than 3 segments, where the eye cannot rank slices |
| Two things move together | Scatter | The reader will read correlation as cause, so say which it is |
| One number is the headline | Big number plus context | It ships alone, with no baseline or comparison |

## Decision thresholds

| Signal | Threshold | What to do |
|---|---|---|
| Metric moved | Below 10% on a base under 100 | Do not narrate it. Say the volume is too small to read |
| Metric moved | Over 10% on a meaningful base | Investigate, and label the cause a hypothesis unless data names it |
| Confidence in a cause | Low | Say so in the row. Never rank low-confidence causes as though they were findings |
| Actions proposed | More than 3 | Cut to 3. A review with 7 actions produces none |
| A number is `[UNVERIFIED]` | Any | Tag every figure derived from it, and say which decisions change if it is wrong |

## Warning signs, worst first

1. A derived figure with no arithmetic shown. That is the number that gets read aloud in a board meeting.
2. Causes ranked by likelihood when the skill has no access to the ad platform, CRM or site.
3. A recommendation that does not trace to a specific finding in the review.
4. A "What I don't know" section that is empty or generic. If it is empty, it was not attempted.

## Related skills

- `/campaign-brief` for planning against the numbers this review produces
- `/retro` for the post-campaign learning loop, which records causes with evidence tiers
- `/brand-context` owns `knowledge/kpis.md`, including the baselines this review compares against
- `/growth-experiment` when a cause is a hypothesis worth testing rather than acting on
- `/page-cro` when the metric that moved is a page conversion rate

## What this skill cannot know

- Anything not in the data supplied. It has no access to the ad platform, the CRM, or the site
- Whether a metric definition changed mid-period, which is the most common cause of a fake trend
- Whether a cause it lists as probable is real, absent data that names it
- Whether a figure tagged `[UNVERIFIED]` upstream was ever measured
