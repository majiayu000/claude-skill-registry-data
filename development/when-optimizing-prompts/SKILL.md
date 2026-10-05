---
name: when-optimizing-prompts
description: Prompt-debugging loop skill. Use when Codex should diagnose why an existing prompt fails and improve it step by step instead of rewriting blindly.
---

# When Optimizing Prompts

Use this skill when a prompt already exists and the problem is inconsistency, hallucination, brittleness, or cost.

## Workflow
- Start from concrete failure cases.
- Change one lever at a time.
- Keep a test set for future comparisons.

## Deliverables
- An improved prompt plus changelog.
- A compact regression test set.

## Guardrails
- Do not optimize by endlessly adding instructions.
- Do not claim success without tying it to failure cases.
