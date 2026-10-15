---
name: standards-match
description: "Look up Florida K-12 standard codes and text for a grade, subject, and topic. Do NOT use to write lessons or activities (use objective-write)."
---

# standards-match

Returns the 1–5 most relevant Florida standards for a given topic/grade/subject. No generation — lookup and return only. Used by lesson-planner, assessment-designer, and any skill needing verified standard codes before generating content.

## Input

```json
{
  "grade":   "4",
  "subject": "Math",
  "topic":   "fractions on a number line",
  "max":     3
}
```

`grade`: K–12 or grade band (e.g. "6-8"). `subject`: Math, ELA, Science, Social Studies, ELD, etc.
`topic`: keyword phrase or short description. `max`: how many standards to return (default 3).

## Output

```json
{
  "tool": "standards-match",
  "query": {"grade": "4", "subject": "Math", "topic": "fractions on a number line"},
  "standards": [
    {"code": "MA.4.FR.1.1", "description": "Model and express a fraction including mixed numbers...", "source": "FL B.E.S.T.", "confidence": "high"},
    {"code": "MA.4.NSO.1.1", "description": "Express how the value of a digit changes...", "source": "FL B.E.S.T.", "confidence": "medium"}
  ],
  "match_method": "keyword | L1_cache | uncertain",
  "human_review_required": true,
  "note": "Verify codes against CPALMS before citing in any artifact."
}
```

`match_method` is `unified_index` when the unified offline index is built
(`python3 tools/offline_index.py --standards "<topic>" --grade <g> --subject <s>` — a deterministic
zero-token SQLite/FTS5 lookup that returns only the matching rows; see `canonical-sources/index/README.md`),
`L1_cache` for the standards-only cache (shared/cache/cache.py), `keyword` for tools/fl_lookup.py direct
search, `uncertain` when no index is built and the match is model-inferred. **Prefer the index** — it
returns verbatim canonical rows (~100–350 tokens) instead of loading the ~470k-token standards corpus or
recalling from memory, so it cannot fabricate a code. Never fabricate a standard code — return empty
`standards` and explain in `note` instead.

## How to use this atom

```
"Find the top 3 Florida B.E.S.T. Math standards for grade 4 fractions on a number line."
→ standards-match returns the JSON above
→ caller passes standards[] to objective-write or activity-generate
```

## Do NOT use this atom for
- Generating any instructional content (use objective-write, activity-generate)
- NGSSS or Common Core lookup (label the framework in `subject` if non-BEST)
- Confirming whether a standard was repealed — route to standards-updater

## Pipeline note
Output conforms to `references/metadata-schema.md`. Follows `references/method.md` at the Standards step only. No Generation or Differentiation step — this atom stops at Standards Alignment and returns. `human_review_required: true` because model-inferred matches are not guaranteed correct.
