---
name: govern-artifact
description: "Stamp an artifact with provenance, lineage, and confidence metadata. Do NOT use for quality gating (use quality-check) or content."
---

# govern-artifact

Stamps any artifact with governance metadata: provenance (where it came from), lineage (how it was processed), confidence (how reliable), and evidence (what supports it). Used by document-intelligence after parsing and reusable by any skill producing governed artifacts.

## Input

```json
{
  "artifact": {"type": "lesson_plan", "content": "..."},
  "source_lineage": {
    "origin": "document_intelligence",
    "source_file": "curriculum.pdf",
    "extracted_at": "2026-06-27T10:00:00Z",
    "parser_used": "PyMuPDF"
  },
  "confidence": {"overall": 0.95, "text_recovery": 0.98}
}
```

## Output

```json
{
  "tool": "govern-artifact",
  "governed_artifact": {
    "type": "lesson_plan",
    "content": "...",
    "_provenance": {"origin": "document_intelligence", "source_file": "curriculum.pdf"},
    "_lineage": {"extracted_at": "2026-06-27T10:00:00Z", "parser_used": "PyMuPDF"},
    "_confidence": {"overall": 0.95, "text_recovery": 0.98}
  },
  "human_review_required": true
}
```

## Do NOT use this atom for
- Quality gating or pass/fail validation (use quality-check)
- Content generation or modification (this only adds metadata)
- Security scanning

## Pipeline note
Follows `references/method.md` at the Governance step (metadata attachment). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — provenance and confidence metadata should be verified.
