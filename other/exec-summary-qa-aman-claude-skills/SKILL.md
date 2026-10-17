---
name: exec-summary
description: >
  Write an executive summary using the Pyramid Principle SCQA structure. Use when a
  consultant says "write an executive summary", "I need a one-pager for the exec",
  "how do I open this report", "write me the intro for this deck", "draft the cover
  memo", "I need to frame the findings", "executive doesn't have time to read the full
  report", "help me write the storyline", or "write the situation-complication-answer".
  Also trigger when someone has findings or recommendations and needs to communicate
  them top-down to a time-constrained audience.
---

## Overview

Based on **"The Pyramid Principle"** by Barbara Minto. An executive summary is not a summary of what you did - it is a summary of what the reader needs to know and do. The SCQA structure (Situation, Complication, Question, Answer) establishes shared context, creates the tension that makes the reader care, and delivers the answer at the top before the evidence. Executives read the answer first. Everything else is support.

The key insight from Minto: the answer always goes first. Supporting arguments come after, in MECE groups. Never bury the recommendation at the end.

## The SCQA Structure

```
Situation   - What is true today (shared context, no controversy)
Complication - What has changed or is at risk (creates the tension)
Question    - The question the complication raises (implicit or explicit)
Answer      - The answer to that question (your main message)
```

The Situation and Complication together create the story that makes the reader feel the problem. The Answer is your main message - state it without qualification. Supporting arguments live in the body of the document, not the exec summary.

## Workflow

### Step 1: Identify the Main Message

Before writing a word, answer: "If the reader remembers one thing, what should it be?"

The main message is not your topic. It is your point of view about the topic.

- Weak: "This report covers the current state of [your client]'s sales operations."
- Strong: "[Your client]'s sales operations are generating 30% less revenue than they should because of three fixable process failures."

Write the main message as a single sentence. If you cannot state it in one sentence, you do not yet know your main message.

### Step 2: Write the Situation

The Situation is shared, non-controversial context that both you and the reader agree is true. It establishes the stage.

Rules:
- No new information - only what the reader already knows or would immediately agree with
- 1-3 sentences maximum
- Specific, not vague ("In Q3, [your client] processed 14,000 transactions across 3 regions" not "The business has been growing")

Example:
```
[Your client] has operated in [market] for [X] years and currently serves [Y customers]
across [Z regions]. In [year], the organization launched [initiative] with a target of
[goal]. The initiative is now in its [phase] phase.
```

### Step 3: Write the Complication

The Complication is what has changed or what threatens to disrupt the Situation. It is the reason the document exists. It creates the tension that makes the reader care.

Rules:
- One change or threat - not a list
- Specific enough to feel real
- Should naturally prompt the Question

Example:
```
Despite strong market conditions, [your client] missed its [year] revenue target by 18%.
Internal data shows the gap is concentrated in the mid-market segment, where close rates
have declined from 34% to 21% over 12 months.
```

### Step 4: State the Question

The Question is what the Complication forces the reader to ask. Often you can leave it implicit - but making it explicit sharpens the structure.

Implicit version: [skip to Answer]
Explicit version: "The question is: why has mid-market performance deteriorated, and what would reverse it?"

Use the explicit version when the complication is complex or the question might not be obvious.

### Step 5: Lead with the Answer

The Answer is your main message from Step 1. State it directly in the first line after the Question. Do not hedge it. Do not qualify it. Do not save it for the end.

Template:
```
Three fixable process failures are responsible for the revenue gap: [finding 1],
[finding 2], and [finding 3]. Addressing all three over the next [timeframe] would
recover an estimated $[X]M in annual revenue.
```

### Step 6: Structure the Supporting Points (MECE)

After the Answer, list 2-4 supporting points in MECE order (Mutually Exclusive, Collectively Exhaustive). Each point supports the Answer directly.

MECE test:
- Mutually Exclusive: do the points overlap? If yes, consolidate.
- Collectively Exhaustive: do the points together fully support the Answer? If not, add the missing piece.

Template:
```
Three findings support this conclusion:

1. [Finding 1]: [One-sentence summary with key data point]
2. [Finding 2]: [One-sentence summary with key data point]
3. [Finding 3]: [One-sentence summary with key data point]

Full analysis is in the body of this report. Section [X] covers [finding 1],
Section [Y] covers [finding 2].
```

### Step 7: Close with the Recommended Action

The exec summary ends with a clear, specific call to action. What should the reader do, and by when?

Template:
```
We recommend [specific action] by [date]. This requires [key decision or resource].
The full findings and implementation plan are in the attached report.
```

One action. One timeline. If there are multiple actions, list them in priority order and call out the first one.

## Full Template

```
[SITUATION]
[Your client] [brief context - 1-2 sentences establishing current state].

[COMPLICATION]
[What has changed or what is at risk - 1-2 sentences with specific data].

[ANSWER]
[Main message - your point of view, leading with the recommendation or finding, no hedging].

[SUPPORTING POINTS - MECE]
1. [Finding/argument 1]: [One-sentence summary]
2. [Finding/argument 2]: [One-sentence summary]
3. [Finding/argument 3]: [One-sentence summary]

[CALL TO ACTION]
[Specific recommended action] by [date]. [What it requires]. Full analysis follows.
```

Target length: 200-350 words. If it exceeds 400 words, the exec summary has become the report.

## Anti-Patterns

**1. Burying the answer**
Bad: Writing 3 paragraphs of context before stating the recommendation.
Good: State the main message in the first or second sentence after the Complication.
Executives scan documents. If the answer is on page 2, it might not get read.

**2. Situation that is actually a Complication**
Bad: "Sales have declined 18% year-over-year" as the Situation.
Good: "Sales declined 18% year-over-year" as the Complication, with the Situation being the undisputed context that precedes it.
Mixing these creates a confusing opening that does not build tension properly.

**3. Non-MECE supporting points**
Bad: Three bullet points where two overlap or where together they don't fully prove the conclusion.
Good: Test each pair for overlap. Test the set as a whole for completeness.
Overlapping points make the logic feel weak. Gaps leave the reader unconvinced.

**4. Vague call to action**
Bad: "We recommend leadership consider next steps."
Good: "We recommend [your client] launch a 60-day pilot in the mid-market segment by [date], led by [role]."
Vague calls to action produce no action. Specific ones produce decisions.

**5. Summary of activities, not findings**
Bad: "This report presents our analysis of sales operations conducted over 8 weeks..."
Good: "[Your client]'s sales operations are underperforming by $X due to three process failures."
An executive summary that describes your process answers "what did you do?" instead of "what did you find?"

## Quality Checklist

- [ ] Main message identified before writing and stated in one sentence
- [ ] Situation is non-controversial, shared context (no new information)
- [ ] Complication creates genuine tension and contains specific data
- [ ] Answer leads (does not end) the summary
- [ ] Supporting points are MECE - no overlaps, no gaps
- [ ] Supporting points link directly to the Answer
- [ ] Call to action is specific (what, by when, who decides)
- [ ] Total length 200-350 words
- [ ] No methodology description or "in this report we will..." framing
- [ ] Readable without the body of the document
