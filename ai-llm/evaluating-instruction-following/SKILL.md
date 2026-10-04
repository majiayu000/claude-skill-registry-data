---
name: evaluating-instruction-following
description: Scores whether a produced image satisfies the original natural-language instruction. Use after any capability Skill produces a result, to gate acceptance and feed back into the repair loop.
when: After any generation/edit Skill produces an image, before marking the step done.
---

# evaluating-instruction-following

Deterministic stub evaluator for v1. Takes `{instruction, result_meta}` on stdin
and emits `{pass, score, reasons[], evaluator: "stub-v1"}` on stdout. Designed
to be swapped for a vision-LLM call later without changing the interface.

## Contract

Input:
```json
{"instruction": "...", "result_meta": {"goal": "generate", "prompt": "...", "denoise": 0.85}}
```

Output:
```json
{"pass": true, "score": 0.62, "reasons": ["goal matches", "prompt overlap 3/5"], "evaluator": "stub-v1"}
```

## Heuristic (v1)

- goal token from instruction matches `result_meta.goal` → +0.3
- token overlap between instruction and `result_meta.prompt` → +0.1 per term, cap +0.5
- denoise sane for goal → +0.2
- threshold pass: score ≥ 0.5

## TODO (v2)

Replace `scripts/evaluate.py` with a vision-LLM call routed through `host/llm/provider.py`.
