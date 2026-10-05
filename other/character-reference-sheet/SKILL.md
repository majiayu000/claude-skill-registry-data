---
name: character-reference-sheet
description: Compatibility entry for older character-sheet requests. Route the complete request to create-character, which now owns canonical sheet creation and the full eight-image character production pack. Do not submit an independent generation run from this Skill.
---
# Character Reference Sheet Compatibility Entry

`create-character` now owns character reference creation and downstream character assets as one consistency-controlled workflow.

## Catalog

- Display name: Character Reference Sheet
- Categories: Character
- Status: Ready
- Route label: Compatibility redirect to Create Character
- Tone: ink
- Short description: Redirect legacy character-sheet requests to the canonical character workflow without creating a duplicate run.
## What this skill does

- Preserves compatibility for older character-sheet requests.
- Redirects execution to Create Character, which owns the canonical sheet and optional expansion.

## How to use

Use this compatibility entry only when an existing integration or prompt explicitly selects `character-reference-sheet`; new requests should select Create Character.

#### Redirect a legacy request

```text
Use character-reference-sheet for this older integration and preserve the supplied character brief.
```

When this legacy Skill is selected:

1. Redirect the request to `$create-character` without submitting a generation task here.
2. Preserve the user's character brief, supplied references, style, ratios, and scene requirements.
3. Let `$create-character` submit only the canonical multi-panel character design sheet first with `batchCount: 1`.
4. After QA, ask whether the user wants the seven derived assets. Submit them without adding a client-side post-QA confirmation and bind the canonical URL into every request. If the URL is unavailable, recover it from the original accepted task-1 operation and execution instead of stopping immediately or regenerating the sheet.
5. Do not create a separate legacy sheet or a ninth image.

## User-facing output

- Media type: Compatibility redirect
- Default quantity: No independent output; `$create-character` returns 1 canonical sheet by default and optionally expands to 8 total images after confirmation
- Model policy: Owned by `$create-character`
- Downstream use: Backward-compatible routing only
