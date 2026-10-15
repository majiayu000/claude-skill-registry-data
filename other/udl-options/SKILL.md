---
name: udl-options
description: "Suggest UDL checkpoint options (CAST 3.0) for a learning barrier. Do NOT use for IEP accommodations (use accommodation-match)."
---

# udl-options

Maps a learning barrier or activity to specific UDL 3.0 checkpoints (Engagement, Representation, Action & Expression) with concrete classroom suggestions. References the CAST framework with attribution.

> **Read first — boundaries (`references/security-and-safety.md` §3).** UDL options are
> **universal design suggestions, not IEP/504 accommodations** — they carry no legal force, and an
> accommodation a plan requires must come from `accommodation-match` and the plan itself. The
> output is decision support for a teacher to adapt. CAST checkpoint numbers and names are
> **cited, never invented**: if the mapping is uncertain, say so instead of producing a
> plausible-looking checkpoint. **Never request, infer, or include real student data —
> placeholders only.**

## Input

```json
{
  "barrier": "Students struggle to sustain attention during 20-minute reading passages",
  "activity": "Independent close reading of a historical text",
  "grade": "6"
}
```

## Output

```json
{
  "tool": "udl-options",
  "udl_options": [
    {"principle": "Engagement", "checkpoint": "7.2: Reduce threats and distractions", "suggestion": "Break the 20-minute reading into 3 chunks with a 1-minute partner share between each"},
    {"principle": "Representation", "checkpoint": "3.3: Guide information processing", "suggestion": "Provide a graphic organizer for students to fill in key ideas as they read each chunk"},
    {"principle": "Action & Expression", "checkpoint": "5.3: Build fluencies with graduated support", "suggestion": "Offer audio version alongside text for students who benefit from dual-modality input"}
  ],
  "framework": "CAST UDL Guidelines 3.0",
  "human_review_required": true
}
```

## Do NOT use this atom for
- IEP-specific accommodations (use accommodation-match)
- Modifying content rigor (UDL removes barriers, not standards)
- Replacing teacher knowledge of individual student needs

## Pipeline note
Follows `references/method.md` at the Differentiation step (UDL options). Output conforms to `references/metadata-schema.md`. `human_review_required: true` — UDL suggestions must be adapted to the specific classroom context.
