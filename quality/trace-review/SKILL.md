---
name: trace-review
description: Use to review whether traces, logs, and runtime evidence are sufficient to explain behaviour and support debugging or verification.
---

# Trace Review

## Use this skill when
- evaluating evidence quality
- debugging failures
- reviewing observability coverage
- deciding whether a run is diagnosable

## Goals
- ensure execution can be reconstructed
- identify blind spots in tracing
- improve failure diagnosis and evaluation quality

## Review criteria
- are the relevant identifiers present
- can the execution path be reconstructed
- are key transitions visible
- are side effects visible
- are retries distinguishable
- are errors surfaced clearly
- is the trace enough for future diagnosis

## Output contract
Return:
- trace strengths
- missing trace elements
- impact of the blind spots
- recommended improvements
