---
name: evaluating-identity-preservation
description: Scores whether a transformed image preserves the subject's identity (face / pose / composition stability) compared with a reference image. Use after style-transfer, inpaint, or background-replacement steps that involve a subject the user wants to keep recognizable.
when: After any capability Skill that may drift identity (transferring-styles, replacing-backgrounds, inpainting-regions over a subject), before marking the step done.
---

# evaluating-identity-preservation

Deterministic stub evaluator for v1. Takes
`{reference_meta, candidate_meta, constraints}` on stdin and emits
`{pass, score, reasons[], evaluator: "stub-v1"}` on stdout. Designed to be
swapped for a real face-embedding / pose comparator later without changing the
interface.

## Contract

Input:
```json
{
  "reference_meta": {"face_bbox": [0.1, 0.1, 0.4, 0.4], "subject_tokens": ["woman", "red hair"]},
  "candidate_meta": {"face_bbox": [0.12, 0.11, 0.41, 0.41], "subject_tokens": ["woman", "red hair", "scarf"], "denoise": 0.45},
  "constraints":    {"goal": "transfer_style", "preserve": ["face"]}
}
```

Output:
```json
{"pass": true, "score": 0.78, "reasons": [...], "evaluator": "stub-v1"}
```

## Heuristic (v1)

- **face bbox IoU** between reference and candidate ≥ 0.7 → +0.4
- **subject token overlap** ratio (intersect / reference) ≥ 0.5 → +0.3
- **goal-aware denoise sanity**: when `preserve:["face"]` is requested,
  `candidate_meta.denoise ≤ 0.5` → +0.3 (low denoise preserves identity)
- threshold pass: score ≥ 0.6

When the input lacks structure (missing bbox, missing tokens, no constraints),
the evaluator returns `{pass: false}` rather than guessing — callers must
escalate or fall back to the repair loop.

## Scripts

- `scripts/evaluate.py` — stdin → stdout, stdlib only.

## TODO (v2)

Replace `evaluate.py` with a real comparator: face embedding cosine distance
(InsightFace), pose keypoint distance, optional CLIP-image cosine. Routed
through `host/llm/provider.py` for hosted variants.
