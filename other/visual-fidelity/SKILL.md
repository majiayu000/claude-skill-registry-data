---
name: visual-fidelity
description: Use when a page emitted by kivo-creator must be proved against its design - rendering the block markup on the local site, screenshotting every section at 390 and 1440 px with the project's Playwright, pixel diff against the references (2 percent per section by default), style check of exact values, lint for arbitrary values and inline styles, and up to three fix rounds before handing the report to the person. For emitting the page use block-scaffolding-from-design.
license: MIT
compatibility: Node 20+ and Playwright in the target project. Creates a local page through the runner; never on a shared or production site.
---

# Visual fidelity

Prove fidelity with numbers. `verify.mjs` produces `fidelity.md`; you fix what it reports, at most three rounds.

## When to use

- After `block-scaffolding-from-design`, or after any change to a block used by a `/creator` page.
- "Does it match the design?", "verify the page".
- Not for choosing blocks or writing them.

## Inputs required

1. `.creator/<run>/` with `page.html`, `emitted.json`, specs and references.
2. The local site URL and runner (session context). Local development only.
3. Playwright in the project (same as `html-ingest`).
4. The kivo-creator plugin root (two levels above this skill's folder).

## Procedure

1. Put the page on the local site:

   ```bash
   {{runner.wp}} post create .creator/<run>/page.html --post_type=page --post_status=publish --post_title="creator <run>" --post_name=creator-<run> --porcelain
   ```

   Keep the printed id. Get the URL with `{{runner.wp}} post list --post__in=<id> --post_type=page --field=url`.
2. Verify:

   ```bash
   node <kivo-creator>/scripts/verify.mjs --run=.creator/<run> --url=<page url> --project=.
   ```

   Defaults: widths 390 and 1440, threshold 0.02. The section selector is the one `emit.mjs` recorded in `emitted.json` (the adapter default, `[data-block]` for ACF Composer blocks, which scaffolded blocks print). If existing blocks do not print it, pass `--selector` with the wrapper they do print (or pass it to `emit.mjs` once), and say so in the report.
3. Read `.creator/<run>/fidelity.md` and the diff images in `verify/` (red pixels = different).
4. Fix, smallest cause first: a wrong token or utility, a missing field value, spacing from the wrong scale step, an image not imported. Never fix a diff with an arbitrary value, an inline style or a hard-coded string.
5. Update the page (`{{runner.wp}} post update <id> .creator/<run>/page.html`) when `page.html` changed, then run step 2 again. Stop after three rounds.
6. Hand `fidelity.md` to the person with what was fixed and what is left. Delete the page afterwards when the person agrees (`{{runner.wp}} post delete <id> --force`).

## Verification

- `verify.mjs` exits 0 (`PASS`), or the person accepted the remaining rows after round three.
- The lint section of `fidelity.md` says `None.`

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `found N elements for [data-block]` | Existing blocks do not print `data-block`, or a block renders twice | Pass `--selector`; check nested blocks |
| Every row is `no reference` | Figma source without `FIGMA_TOKEN` for references | Run `figma-ref.mjs` with a token, or accept a style-and-lint-only report |
| Large diff on image areas only | Media not imported (ids still `null`) | Import media (block-scaffolding-from-design step 5) |
| `size differs` on every row | Fonts not loaded, or a different container width | Load the project's fonts on the page; compare with the right template |
| Style mismatch on font size at 1440 | A token maps to the wrong step | Fix the token mapping or ask for a new token |

## Escalation

After three rounds, or when a fix needs a design decision (a new token, a new variant, changing a shared block), stop and hand the report to the person.
