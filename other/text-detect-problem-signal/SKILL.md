---
name: text-detect-problem-signal
description: Market listener text.detect_problem_signal classifier
version: 1.0.0
author: PonyBunny
tags: [market-listener, classification, problem-detection]
phases: [execution]
user-invocable: false
disable-model-invocation: false
---

# Skill — text.detect_problem_signal

## Intent
Classify whether a piece of text contains a user-expressed problem, pain, or need.

## Inputs

```yaml
detect_request:
  raw_text: string
  platform: string
```

## Outputs

```yaml
detect_result:
  has_problem_signal: boolean
  signal_markers: string[]
  label: enum [problem, how_to, bug, request, complaint, discussion, showcase, other]
  confidence: number
```

## Tools
- llm.classify

## Policy
- Return ONLY valid JSON.
- Never provide advice or solutions.
- signal_markers must be verbatim snippets (no paraphrase).
- If uncertain, return best guess with low confidence.

## Failure Modes
- Invalid JSON: caller falls back to heuristic detection.
