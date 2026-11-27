---
name: ai-ux-audit
description: "Runs a scored heuristic audit of an Artificial Intelligence (AI) feature across six AI-specific dimensions - transparency, control, feedback, error recovery, expectation-setting, and trust calibration - and produces a severity-ranked fix list with owners. Use when reviewing an AI feature before launch; diagnosing low adoption or high abandonment of a copilot or agent; benchmarking an AI experience against competitors; or preparing a design review for a Large Language Model (LLM) feature."
---

# AI UX Audit

> Classic usability heuristics miss the ways AI features fail. This audit scores the ones that matter.

## What this skill is

A structured heuristic evaluation built for probabilistic products. It scores an Artificial Intelligence (AI) feature on six dimensions that standard heuristics underweight, walks the feature through a fixed set of stress scenarios (not just the happy path), and converts findings into a severity-ranked fix list. The result is a defensible score a team can track release over release.

## What it solves

- Design reviews that only evaluate the happy-path demo output
- AI features that look polished but leave users unable to correct, undo, or verify results
- Over-trust (users accept wrong answers) and under-trust (users redo the work manually) going unmeasured
- Fix lists with no severity logic, so cosmetic issues crowd out trust-breaking ones
- No baseline to show whether the next release improved the experience

## When to invoke

- Pre-launch review of a copilot, assistant, agent, or generative feature
- Adoption is flat or users try the feature once and stop
- Support tickets mention "it made something up" or "I could not undo it"
- Competitive teardown of AI experiences in your category
- Quarterly AI experience health check

## Phase 1: Scope the feature and its job

Document before scoring:

| Field | Example |
|-------|---------|
| Feature and surface | Inline drafting assistant in the ticket editor |
| User and job | Support agent replying to a billing dispute |
| AI role | Suggests / drafts / acts (see `agent-autonomy-level-mapper`) |
| Stakes of a wrong output | Low / Medium / High / Critical |
| Model inputs the user can see | Ticket thread, customer plan, prior replies |
| Success definition | Reply sent with under 2 minutes of edits |

Stakes set the bar. A Critical-stakes feature needs a higher score to pass than a Low-stakes one.

## Phase 2: Run the stress scenarios

Walk the feature through each scenario and capture screenshots or transcripts. A heuristic that is never stressed cannot be scored.

| # | Scenario | What it reveals |
|---|----------|-----------------|
| S1 | Ideal input, clear request | Baseline quality and polish |
| S2 | Ambiguous or underspecified request | Clarification behavior |
| S3 | Request outside capability or policy | Refusal and redirection |
| S4 | Plausible but wrong output (seed one if needed) | Whether users can detect and fix errors |
| S5 | Slow response or timeout | Latency and progress handling |
| S6 | User wants to change or undo the result | Control and reversibility |
| S7 | Returning user, second session | Memory, continuity, expectation drift |

## Phase 3: Score the six dimensions

Score each dimension 0-4 using the anchors below.

| Dimension | 0 - Absent | 2 - Partial | 4 - Strong |
|-----------|-----------|-------------|------------|
| Transparency | No signal that AI produced the output | AI labeled, but inputs and sources hidden | User sees what the AI used and why, at the moment of decision |
| Control | Output is final or applied silently | Can edit, but cannot steer, retry, or undo | Edit, regenerate with direction, undo, and turn off |
| Feedback | No way to signal quality | Thumbs up/down with no visible effect | Specific feedback that changes the next output or is acknowledged |
| Error recovery | Failures are dead ends or silent | Generic error with retry | Failure named, partial work preserved, next best action offered |
| Expectation-setting | No guidance on what it can do | Generic "Ask me anything" | Capabilities, limits, and good inputs shown in context |
| Trust calibration | Uniform confidence regardless of quality | Disclaimers only | Confidence varies with evidence; verification is cheap where stakes are high |

Weight by stakes:

```
Weighted score = sum(dimension score x weight) / (4 x sum(weights)) x 100
Default weights: Error recovery 1.5, Trust calibration 1.5, Control 1.25, others 1.0
For High or Critical stakes: raise Trust calibration and Error recovery to 2.0
```

| Score | Rating | Launch guidance |
|------:|--------|-----------------|
| 85-100 | Strong | Ship |
| 70-84 | Adequate | Ship with fixes scheduled |
| 50-69 | Weak | Fix Severity 1 and 2 before broad release |
| Under 50 | Failing | Do not ship; redesign |

Any dimension scored 0 on a High or Critical-stakes feature is an automatic launch blocker.

## Phase 4: Log and rate findings

For each issue, record scenario, dimension, evidence, and severity:

| Severity | Definition | Example |
|----------|-----------|---------|
| 1 - Trust-breaking | User acts on wrong output without a reasonable chance to notice, or loses work | Agent sends email with invented refund amount |
| 2 - Task-blocking | User cannot complete the job or recover without leaving the feature | Timeout clears the draft |
| 3 - Friction | Job completes, but with avoidable effort or confusion | Must retype the whole prompt to adjust tone |
| 4 - Polish | Cosmetic or consistency issue | Inconsistent "AI" labeling across surfaces |

```
Priority = Severity weight (1=8, 2=4, 3=2, 4=1) x Frequency (1-3) x Reach (1-3)
```

## Phase 5: Build the fix list

Rank by priority. For each fix specify the pattern, not just the problem:

| Rank | Finding | Dimension | Severity | Recommended pattern | Owner | Effort |
|-----:|---------|-----------|---------:|---------------------|-------|--------|
| 1 | | | | | Design / Eng / Model | S / M / L |

Separate fixes into **interface fixes** (design and front end), **behavior fixes** (prompting, retrieval, tool logic), and **policy fixes** (what the AI should not do). Teams often assign model-behavior problems to design, or the reverse.

## Output

- Feature scope card with stakes rating
- Scenario evidence log (S1-S7) with screenshots or transcripts
- Six-dimension scorecard with weighted score and rating
- Severity-ranked fix list split into interface, behavior, and policy fixes
- Launch recommendation with explicit blockers
- Re-audit baseline for the next release

## Operating rules

**Always**
- Run every stress scenario, including a seeded wrong output
- Set stakes before scoring and adjust weights accordingly
- Cite evidence (screenshot, transcript, step) for every score below 4
- Recommend a concrete pattern for each fix
- Re-score against the same scenarios after fixes ship

**Never**
- Score from a scripted demo or marketing video
- Treat a disclaimer as sufficient trust calibration
- Average away a 0 on a high-stakes dimension
- Mix model-quality complaints with interface issues in one undifferentiated list
- Count "users can thumbs-down it" as error recovery
