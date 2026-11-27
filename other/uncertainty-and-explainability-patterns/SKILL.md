---
name: uncertainty-and-explainability-patterns
description: "Selects how an Artificial Intelligence (AI) feature should communicate confidence, citations, sources, and reasoning for a specific audience and risk level, producing a pattern specification with display rules, thresholds, and an anti-pattern check covering false precision, explanation theater, and citation laundering. Use when deciding whether to show confidence scores; designing citations for a Retrieval-Augmented Generation (RAG) answer; explaining why a model made a recommendation; or users over-trust or ignore AI output."
---

# Uncertainty and Explainability Patterns

> The goal of an explanation is not to look transparent. It is to help the user decide whether to rely on the output.

## What this skill is

A pattern-selection workflow that matches how uncertainty and reasoning are shown to who is looking and what is at stake. It profiles the audience and decision, picks from a catalog of confidence, provenance, and reasoning patterns, sets display thresholds, and checks the design against common anti-patterns. The output is a specification a designer and engineer can implement consistently across a product.

## What it solves

- Confidence percentages that look precise but are not calibrated to real accuracy
- Citation lists that link to sources which do not support the claim
- Long reasoning dumps that users skip, adding noise without improving decisions
- The same explanation shown to a novice consumer and an expert analyst
- Users over-relying on AI output in high-stakes moments, or ignoring it in low-stakes ones

## When to invoke

- Deciding whether and how to display a confidence score or probability
- Designing citations and source display for a search or retrieval answer
- Explaining a model recommendation, ranking, classification, or flag
- Regulatory or internal policy requires explainability for automated decisions
- Research shows users accept wrong answers, or redo work the AI did correctly

## Phase 1: Profile the audience and decision

| Factor | Options |
|--------|---------|
| Audience expertise | Novice / Practitioner / Expert in the domain |
| Statistical literacy | Low / Medium / High |
| Decision stakes | Low (preference) / Medium (rework) / High (money, health, legal, safety) |
| Time pressure | Glanceable (seconds) / Considered (minutes) / Deliberate (audit, review) |
| User can verify independently? | Easily / With effort / Not practically |
| Accountability | Who answers for the decision if the AI is wrong |

The core question per decision: **what does the user need to know to decide whether to rely on this output?**

## Phase 2: Measure before you show

Uncertainty display is only honest if the underlying signal is real.

| Signal source | Use for display? |
|---------------|------------------|
| Calibrated probability (validated against held-out accuracy) | Yes, numeric display allowed |
| Retrieval relevance or grounding check score | Yes, as categorical bands, not raw numbers |
| Self-consistency across multiple samples | Yes, as agreement ("3 of 3 runs agreed") |
| Model self-reported certainty in text | No, not without calibration evidence |
| No signal available | Show provenance instead of confidence |

```
Calibration check: for outputs labeled "High confidence," measured accuracy should be within 5 points of the implied rate
If uncalibrated, collapse to 2-3 categorical bands or remove the confidence display
```

## Phase 3: Select confidence patterns

| Pattern | Best for | Avoid when |
|---------|----------|-----------|
| Categorical band (High / Medium / Low) | Novices, glanceable decisions | Bands are not backed by measured thresholds |
| Numeric probability | Experts with calibrated models | Low statistical literacy or uncalibrated scores |
| Frequency framing ("Right about 8 in 10 times for cases like this") | Mixed audiences, risk communication | Very small sample sizes |
| Visual emphasis (dimming or underlining weak claims) | Long generated text | Color is the only signal (accessibility) |
| Alternatives shown (top 3 options) | Ambiguous inputs, classification | Users need a single action |
| Abstain or ask | Confidence below threshold on high stakes | Low stakes where a best guess is fine |

Threshold rule: define the confidence level below which the feature **abstains or asks** rather than answers. For high-stakes decisions this matters more than any display choice.

## Phase 4: Select provenance and reasoning patterns

| Pattern | What it shows | Best for |
|---------|---------------|----------|
| Inline citation | Claim-level link to the supporting passage | Factual answers, research, policy questions |
| Source card | Title, owner, date, and type of each source | Judging source quality |
| Quote highlight | The exact passage that supports the claim | High-stakes facts users must verify |
| Key-factor explanation | Top 3 inputs that drove a recommendation | Scores, rankings, risk flags |
| Counterfactual | "Would change if X were different" | Decisions users want to contest or improve |
| Step summary | Short list of steps the agent took | Agent actions and multi-step tasks |
| Full trace (on demand) | Detailed reasoning or tool log | Experts, debugging, audit |

Match by profile:

| Profile | Default pattern set |
|---------|---------------------|
| Novice, low stakes | Categorical band or none; source card on demand |
| Novice, high stakes | Abstain-or-ask, quote highlight, clear path to a human |
| Expert, low stakes | Inline citations, full trace on demand |
| Expert, high stakes | Calibrated numeric confidence, quote highlight, counterfactual, audit trace |

Layer it: one glanceable signal by default, evidence one click away, full trace for those who want it.

## Phase 5: Run the anti-pattern check

| Anti-pattern | Symptom | Fix |
|--------------|---------|-----|
| False precision | "87.3 percent confident" from an uncalibrated model | Use bands or remove |
| Explanation theater | Long reasoning text no one reads and no one validated | Replace with key factors or step summary |
| Citation laundering | Link present but passage does not support the claim | Claim-level grounding check; show the quote |
| Uniform confidence | Every answer styled the same regardless of evidence | Vary treatment by evidence strength |
| Disclaimer wallpaper | "AI can make mistakes" on every screen | Specific, contextual cues where risk is real |
| Post-hoc rationalization | Explanation generated separately from the decision | Explain from the actual inputs and features used |
| Color-only signals | Red, yellow, or green with no text | Add labels and icons |

## Output

- Audience and decision profile per surface
- Signal inventory with calibration status
- Selected confidence, provenance, and reasoning patterns per surface
- Abstain-or-ask thresholds for high-stakes decisions
- Layering spec (default, one click, full trace)
- Anti-pattern checklist with pass or fail and fixes

## Operating rules

**Always**
- Verify calibration before showing any numeric confidence
- Tie every citation to the specific claim it supports
- Set a threshold below which the system abstains or asks
- Layer explanations: glanceable first, detail on demand
- Test whether the pattern changes user reliance in the right direction

**Never**
- Display model self-reported certainty as if it were a measured probability
- Use more decimal places than the evidence supports
- Count the number of citations as a proxy for answer quality
- Show the same explanation depth to every audience
- Rely on a generic disclaimer as the trust mechanism
