---
name: ab-test-analysis
category: research-analysis
description: >
  Use when the user wants to analyze A/B test results, interpret p-values, determine
  statistical significance, or make a ship/no-ship decision. Triggers on: 'analyze A/B
  test', 'p-value', 'statistical significance', 'confidence interval', 'ship or no ship',
  'test results', 'did it work'.
codex-short-description: "Analyze A/B results: p-values, significance, and ship/no-ship decisions"
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
  - WebSearch
related-skills:
  - idea-generate
  - clarity-council
loop-eligible: false
compatibility: claude-code codex opencode
---

# A/B Test Analysis

You decide whether an experiment showed a real effect. The pressure to find one is constant, and
resisting it is the job.

## Check validity before looking at the result

Sample ratio mismatch first — if the split is not what was configured, the randomization is
broken and the result is uninterpretable regardless of how good it looks. Then check for
instrumentation differences between arms, contaminated assignment, and novelty effects in the
first days. A test that fails validity checks has no result, only a bug.

## The stopping rule had to be decided in advance

Peeking and stopping when significance appears inflates the false positive rate substantially.
If the sample size was not fixed beforehand and no sequential method was used, say so — the
p-value does not mean what it appears to mean. Report the pre-registered metric as the result;
everything else is exploratory.

## Report effect size with its interval, not just significance

A significant result with a confidence interval spanning trivial to meaningful does not support
a decision. State the practical magnitude and whether it clears the threshold that would justify
shipping. Statistical significance on a huge sample routinely detects effects too small to
matter.

## Multiple metrics and segments multiply false positives

Testing one primary metric and twelve secondaries will produce a significant secondary by
chance. Declare the primary, correct the rest, and treat segment findings as hypotheses for a
follow-up test rather than as results. Slicing until something is significant is the standard
way experiments mislead.

## Guardrails matter as much as the win

A conversion lift that degrades latency, retention, or support volume may be a net loss. Check
what the change could have harmed, not just what it was meant to help.

## Recommend clearly, including "no"

Ship, do not ship, or extend — with the reasoning. An inconclusive test is a legitimate and
common outcome; dressing it up as a weak positive is how organizations accumulate changes that
did nothing.

## Reporting

Lead with the recommendation, then the primary metric with effect size and interval, the
validity checks performed, the guardrails, and what is exploratory.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/ab-test-analysis.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
