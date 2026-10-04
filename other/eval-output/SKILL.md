---
name: coordinator:eval-output
description: Score a research output on the 5-criteria rubric.
version: 1.0.0
---

# Evaluate Research Output

## Usage
/coordinator:eval-output <path-to-research-output>

## Process
Dispatch a Sonnet agent (model: sonnet, tools: Read, WebFetch, Write) with the rubric
(`${CLAUDE_PLUGIN_ROOT}/pipelines/deep-research/eval-rubric.md`) and the research output at the
provided path: sample 3-5 cited URLs via WebFetch to verify citation accuracy, score each of the
5 criteria with a 0.0-1.0 score and 2-3 sentence justification, and give an overall
pass/marginal/fail grade. Present the scores to the PM.

## Notes
- This is a post-hoc quality check, not a gate. Use it to calibrate prompt improvements.
- Start by running it on recent pipeline outputs to establish a baseline.
- Anthropic found a single LLM call with a single prompt was most consistent.
