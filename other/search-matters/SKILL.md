---
name: search-matters
description: "Searches across all matters by client, employer, insurer, claim type, stage, flags, or document type. Use when Mandy says 'find', 'search', 'which matters have', 'all matters with', 'show me cases where', or asks for filtered views of her caseload."
---

# Search Matters

## Important
- READ-ONLY. No commit.

## Instructions
1. Parse search query. If none: prompt with examples.
2. Search `matters/index.jsonl` for basic fields. For deeper searches (flags, doc types): read `matter.json` per potential match.
3. Present results with match reason. Offer `/matter-status` drill-down.
