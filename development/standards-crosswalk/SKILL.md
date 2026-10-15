---
name: standards-crosswalk
description: "Map a standard to its closest equivalent in another framework, or report an honest gap. Do NOT use to check a code is current (use standards-match); never invent codes."
---

# standards-crosswalk

Maps a standard to its nearest equivalent in a different framework (e.g., FL B.E.S.T. to Common Core, or vice versa). Returns the match with confidence and a rationale. Never fabricates codes.

## Input

```json
{
  "standard": {"code": "MA.4.FR.1.1", "framework": "FL B.E.S.T.", "text": "Model and express a fraction, including mixed numbers and fractions greater than one, with the denominator 10 as an equivalent fraction with the denominator 100."},
  "target_framework": "Common Core"
}
```

## Output

```json
{
  "tool": "standards-crosswalk",
  "crosswalk": {
    "source": {"code": "MA.4.FR.1.1", "framework": "FL B.E.S.T."},
    "target": {"code": "4.NF.C.5", "framework": "Common Core", "text": "Express a fraction with denominator 10 as an equivalent fraction with denominator 100..."},
    "match_confidence": 0.9,
    "rationale": "Both standards address converting tenths to hundredths at grade 4; FL B.E.S.T. also includes mixed numbers explicitly",
    "differences": "FL B.E.S.T. explicitly includes mixed numbers and fractions > 1; CCSS addresses this implicitly"
  },
  "human_review_required": true
}
```

## Do NOT use this atom for
- Fabricating standard codes that do not exist
- Guaranteeing exact equivalence (standards differ across frameworks)
- Replacing curriculum director review of crosswalk decisions

## Pipeline note
Follows `references/method.md` at the Analysis step (standards crosswalk). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — crosswalk accuracy must be verified by a curriculum specialist.
