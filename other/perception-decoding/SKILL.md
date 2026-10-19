---
name: perception-decoding
description: "Use for reusable perception decoding recipes in software and coding-agent work."
---

# Perception & state decoding — recipes (generic tier)

On-demand recipes (2). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Separate OCR coordinate-calibration bugs from glyph bugs; render the frame and read off positions
`generic` · **negative result** · ⚠ _session-derived, unverified_

When EVERY text field on a view is misread by the same offset, suspect a GLOBAL screen-coordinate calibration error, not per-field glyph bugs: the dominant OCR failure was text y-positions systematically ~10px off (role name at y=28 not y=18, room name at y=56 not y=46). Layout/offset bugs are a different root cause from glyph-level bugs (wrong glyphs in the font table, false ambiguous-pair entries, a wrong binarization threshold), and treating one as the other wastes effort. Before touching parser constants, render the frame to an image and read off the actual (y, x, color) of each text block. Watch scan-window edges: scanning chat from chatY+2 instead of chatY+1 dropped the oldest message by one pixel of the glyph top row, so verify the window covers the FULL glyph height (ascenders live in the top row).
  <sub>sources: opencode:ses_20b179f2fffeJe4vpbx2D4tWuR, opencode:ses_21f8ce4f6ffe6Uh3krQPdNOwZe</sub>

#### 2. Tiny bitmap-font OCR: read coords/metrics from the renderer, use two-sided scoring, and handle ambiguous pairs, trailing space, odd-x centering
`generic` · ⚠ _session-derived, unverified_

Read the server's RENDER routine for ground-truth glyph metrics and start positions (an authoritative cheaper source than reverse-engineering from captures), and understand a fuzzy-matcher's error metric before blaming it: an OCR maxErrors=2 looked loose ('2 of 4 chars') but meant 2 mismatched PIXELS across the whole ~60-pixel string, and on a near-black screen every opaque 'IMPS' pixel mismatches, making accidental matches far harder than they appear. Tiny bitmap-font OCR has recurring failure modes: (1) S/5 and O/0 are ambiguous -- return raw text plus as_text()/as_numeric() helpers and let the caller disambiguate by context. (2) Naive 'fraction of glyph on-pixels present' scoring lets a subset glyph (A's pixels all lie within 8's) falsely score 1.0 -- use two-sided/false-positive-aware scoring that ALSO penalizes target-colored pixels the glyph says should be OFF (missing foreground + unexpected extras, tie-break on opaque-pixel count), the model the up-to-date sibling bot used. (3) A '4 empty columns = space' rule misreads the void past text end as endless spaces up to max_chars -- stop once no glyph content follows a detected space, since the renderer emits no trailing spaces. (4) Centered text can start on an odd x that a step-2 scanner skips entirely ('Hades' at x=54, 'Hello' returns None) -- scan centered text in steps of 1, and verify each field because working view-detection does NOT imply working field extraction. A trailing marker can carry semantic state -- a role name's trailing '*' denotes leader, so strip it from the name AND set an is_leader flag.
  <sub>sources: opencode:ses_1ffe75d89ffeHvW4p2ARluHh51, opencode:ses_200ab2780ffe2Zt927TZY4Y8Yf, opencode:ses_204eb0641ffeIAD293yQHlSd61, opencode:ses_20c066070ffeBjXMnfQULai0Lw</sub>
