---
name: debug-trace-analysis
description: Use to reconstruct PonyBunny failure paths from logs, traces, state, and runtime evidence in order to identify the first bad transition.
---

# Debug Trace Analysis

## Use this skill when
- a run failed
- execution got stuck
- behaviour is inconsistent
- a retry loop appeared
- the root cause is unclear

## Goals
- reconstruct the timeline
- find the first divergence
- separate root cause from downstream symptoms
- support a minimal correct fix

## Process
1. Define the symptom.
2. Gather identifiers and evidence.
3. Reconstruct the timeline.
4. Compare expected versus actual transitions.
5. Find the first divergence.
6. Identify root cause.
7. Propose a fix.
8. Recommend hardening.

## Output contract
Return:
- symptom
- evidence
- timeline
- divergence point
- root cause
- fix
- hardening recommendations
