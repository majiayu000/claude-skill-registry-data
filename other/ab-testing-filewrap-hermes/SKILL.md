---
name: ab-testing
description: "One variable, one metric, honest reads on live pages."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, testing]
    category: web
    related_skills: [web-design, usability-testing, conversion-cro]
    web_designer_stages: [revisions]
---

# A/B Testing and Experimentation Skill

Splitting live traffic between variants answers one question: which performs better. This skill covers stating the hypothesis in advance, changing one variable, naming one primary metric with guardrails, and reading the result honestly. It does not explain why a variant won; that needs qualitative work alongside it. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- On live pages with enough traffic, to validate a concrete change.
- When a revision round needs to choose between two versions of a headline, call to action, image, form or proof placement.
- When the coordinator needs a test proposal recorded for a delivered page.
- When two directions both look sound and only live traffic can separate them.
- When a revision changes a conversion element and the change should be validated rather than assumed to help.

It is not for fixing an obvious usability bug, and never as a substitute for fixing one. It is not for pages with traffic too low for a reliable result, and it is not a way to prove a lift from a five-user test. It answers "which performs better", not "why".

## Prerequisites

- The run is active, the coordinator loaded this skill for its stage(s).
- The page is live, or the revision classification exists: the revisions stage record holds `classification`.
- The change to test is concrete, and the audience and the metric it should move are both named.
- Traffic is sufficient for a reliable result; where it is not, the skill says so instead of proposing a test that cannot conclude.
- The conversion-cro skill is available, since the test order it proposes is the order this skill follows.

## How to Run

1. State the hypothesis in advance, in four parts: observation, change, audience, metric.
2. Name one primary metric, plus guardrails that would stop the test if they moved the wrong way.
3. Change one variable only. Headline first, then call to action, image, form length, proof placement — in that order.
4. Set sample and duration to cover whole business cycles; do not peek and do not stop early.
5. Read the result honestly, including "no significant difference", and record it with the hypothesis it tested.
6. Pair the result with qualitative work for the why; a winning variant without a reason is a result, not an understanding.
7. If the result is "no significant difference", record it and stop: do not re-run the same test until it turns positive.
8. If a guardrail moved the wrong way, stop the test and record the guardrail breach, even if the primary metric looked good.
9. Record the traffic available alongside the test, so a later reader can see whether the result could conclude.
10. Do not launch a second test on the same page until the first has read honestly; overlapping tests blur the metric.
11. When the test concerns a headline or call to action, confirm the variant wording is the only difference between the two versions.
12. Close the test by recording the read — including 'no significant difference' — against the pre-registered hypothesis.

## Quick Reference

- Hypothesis parts: observation, change, audience, metric — stated in advance.
- Variables changed per test: one.
- Metrics: one primary metric, plus guardrails.
- Sample and duration: adequate, over whole business cycles.
- Conduct: no peeking, no stopping early.
- Test order: headline, then call to action, image, form length, proof placement.
- Answers: which performs better, not why; pair with qualitative work for the why.
- Honest reads: "no significant difference" is a result, not a failure.
- Guardrails: a breach stops the test even when the primary metric looks good.
- Traffic: recorded with the test, so the result's reliability can be judged later.
- Overlap: one test per page at a time; overlapping tests blur the metric.
- Variants: identical except for the single variable changed.

## Procedure

### 1. What it is

Splitting live traffic between variants to answer 'which performs better?' (not 'why?') — hypothesis stated in advance (observation + change + audience + metric), one primary metric plus guardrails, adequate sample/duration over whole business cycles, no peeking/stopping, paired with qualitative work for the why.

### 2. How Hermes applies it

Hermes proposes one-variable tests (headline first, then CTA, image, form length, proof placement), names the hypothesis and guardrails, warns when traffic is too low for a reliable result, and never claims a 5-user test proves a conversion lift.

### 3. What it returns to the stage

The revisions stage record in `gateway/web_designer/machine.py` (`STAGE_RECORDS`) requires `classification`. This skill's work fills that record: the classification names the test proposed (or that no test is warranted, with the reason), the hypothesis in its four parts, the single variable changed, the primary metric and guardrails, and the honest read of any result — including "no significant difference" where that is what the data says. A test proposal without a pre-registered hypothesis is not recorded as a test.

Where traffic is too low for a reliable result, the classification records that instead of a test: the reason, the traffic available, and what would be needed to conclude. That record is the honest output of the stage, not a gap in it. A test that was stopped on a guardrail breach records the breach and the metric that triggered it, so the next revision starts from the breach rather than from the primary metric alone.

The pre-registered hypothesis is the anchor of the whole record: the result is read against it, not against whatever looks interesting afterwards. A result that contradicts the hypothesis is still an honest read, and it is recorded as one. The classification therefore pairs every result with the hypothesis it tested, so a later revision can see what was asked, what was changed, and what the traffic actually said.

### 4. Good looks like

One variable changed, one primary metric, pre-registered hypothesis, result read honestly — including 'no significant difference'.

A test that ends with an honest read is a test that did its job, whatever the read says. The read is the deliverable, not the winning variant. Where the result is 'no significant difference', the record says so plainly, and the next test starts from that read rather than from a re-run of the same question. That discipline is what keeps experimentation honest.

## Pitfalls

- Claiming a 5-user test proves a conversion lift. Five users surface problems; they do not measure lifts.
- Changing several variables at once, so no one knows which change moved the metric.
- Peeking at results and stopping early when a variant looks ahead.
- Running a test on a page with too little traffic for a reliable result, instead of warning that it cannot conclude.
- Using a test as a substitute for fixing an obvious usability bug.
- Reading a win as an explanation of why it won, without qualitative work.
- Treating "no significant difference" as a failed test instead of an honest read.
- Ignoring a guardrail breach because the primary metric looked good.
- Launching a second test on the same page before the first has concluded.
- Letting the variant wording differ in more than the one variable under test.
- Re-running a test that read 'no significant difference' until it turns positive.

## Verification

- The hypothesis was stated before the test, with observation, change, audience and metric.
- Only one variable changed; one primary metric is named, with guardrails.
- The sample and duration covered whole business cycles; no early stop is recorded.
- A result of "no significant difference" is recorded as an honest read, not hidden or re-run until it turns positive.
- A guardrail breach, where one occurred, is recorded with the metric that triggered it.
- Where traffic was too low, the record says so with the reason, instead of proposing a test that cannot conclude.
- Traffic available is recorded with the test.
- No second test overlaps the first on the same page.
- Variants differ only in the single variable under test.
- The content judger checks the related rules: the wording of the headline and call to action under test is judged there. The skill does the work and the judger checks it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: revisions. Returns: revisions stage-record key `classification`, with the hypothesis, single variable, primary metric, guardrails and honest read. Judger boundary: content judger checks the related copy rules.
