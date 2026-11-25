---
name: logo-delivery-preflight
description: Check actual SVG and PNG logo exports against an approved master, required variants and intended backgrounds before delivery. Distinguish technical findings from visual, native-file and print approval.
---

# Logo delivery preflight

Start with the approved master revision and delivery brief. Record a row for **each promised variant**, including missing ones. Do not infer that all files in a folder are approved, or that every logo needs every format. Use the [preflight sheet](assets/preflight.md); keep filled sheets private.

1. Identify the exact master, approval evidence, required variants, sizes, background colours, vector-only requirements and any permitted live text. If the master or brief is unknown, return REVIEW.
2. Inspect each named local SVG vector delivery or single-frame PNG export. Run the read-only helper once per required file and background, from this skill folder:

       python scripts/check_logo.py example-reverse.png --background "#182030" --size 128 128

   Python 3.11+; PNG decoding uses locally available Pillow. Nothing is installed. Use trusted local files, not URLs. The helper neither renders SVG nor fetches resources. Outputs are JSON: CHECKS_PASS (exit 0) means measured checks passed, BLOCK (1) means a required check failed, REVIEW (2) means attention or another inspector is needed. An SVG image element fails the vector-only check even if embedded. If the brief explicitly permits mixed artwork, record that exception with its evidence, never call it pure vector.
3. For SVG, inspect unresolved references, active content, embedded images and live text. Never open active or externally linked artwork in a network-enabled viewer. If structural checks permit, compare the actual export in an offline, script-disabled renderer against the approved master at the intended size. Review glyphs, counters, clear space, clipping and reversed marks. No silent font substitution, outlining or file repairs.
4. For PNG, a different pixel from the background is not proof of legibility. Inspect the mark on **every required background**, including at its smallest requested size. Compare against the approved master visually, not by expecting vector and raster hashes to match. Record which exact bytes were inspected; a changed master or export invalidates the affected review.
5. Report each row as blocked, needs review or verified within the brief. Missing variants block completion. Unsupported native/PDF files, printer specifications, spot colours and native reopening remain unverified without separate evidence. Do not infer print approval, rights or permission to send. Return findings and the smallest next check; do not package, modify or upload artwork.

The helper caps each input at 8 MiB and PNG inspection at 16 million pixels. Use the visual workflow or a separately approved inspector for larger exports. It is a structural preflight, not an SVG sanitizer or a complete rendering engine.
