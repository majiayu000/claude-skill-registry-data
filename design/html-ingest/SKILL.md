---
name: html-ingest
description: Use when an HTML file, a URL or a published page has to become kivo-creator section specs - rendering it at 390 and 1440 px with the project's own Playwright, splitting it into sections, recording text slots, links, media, computed styles and one reference screenshot per section and width under .creator/<run>/. For a Figma source use figma-ingest; for choosing blocks use section-matching.
license: MIT
compatibility: Node 20+ and Playwright installed in the target project (kivo-creator ships no dependencies). Read-only towards the project; writes only under .creator/.
---

# HTML ingest

Turn a page into neutral section specs. The script does the rendering and the measuring; you review the split and fix it before anything is matched.

## When to use

- "Convert this page / this HTML / this URL into our blocks", "migrate this landing page".
- A `/creator` run whose source is a `.html` file or an `http(s)` URL.
- Not for Figma links (`figma-ingest`), not for choosing blocks (`section-matching`).

## Inputs required

1. The source: a local `.html` file or an `http(s)` URL that the machine can reach.
2. The target project root, with `.roots-stack.json` (kivo-wise `/roots-detect --write`) or the kivo-wise detector JSON.
3. Playwright in the project: `node_modules/playwright` or `@playwright/test`, with Chromium installed (`npx playwright install chromium`). Run the script where the project's own end-to-end tests run Playwright (usually the host); it is a read-only browser run, not a WordPress, Composer or PHP command.
4. The kivo-creator plugin root: the folder that holds `skills/`, `scripts/` and `schemas/` (two levels above this skill's folder).

## Procedure

1. From the project root run:

   ```bash
   node <kivo-creator>/scripts/ingest-html.mjs --source=<file.html | https://...> --project=.
   ```

   Exit 3 means Playwright is missing in the project: show the printed install hint and stop. Never install it without asking.
   When the page already marks its sections (for example `main > section` or `[data-section]`), add `--selector=<css>`: each matching element becomes one section and the heuristic below is skipped.
2. Read the printed list of sections (`id`, `kind`, `chrome`). The split follows these rules (see `scripts/lib/segment.mjs`):
   - content root is `<main>`, else the body after unwrapping single wrappers;
   - `header`, `footer` and `nav` outside `<main>` are `chrome` (kept, never matched);
   - sections are the visible children of the root; pieces shorter than 80 px are merged into the previous section;
   - `kind` and `layout` are inferred; slot values and computed styles are exact.
3. Open every spec in `.creator/<run>/specs/` and compare it with the reference images in `refs/`. Fix by editing the JSON, never by guessing:
   - two designs merged into one section: split the slots into two specs (new `id`, `order`, same `source.ref` plus a note);
   - a wrapper picked as one section: move its children into separate specs;
   - a wrong `kind`: change it and add a note saying why;
   - a value you cannot see in the source: delete the slot. Never invent copy, colours or sizes.
4. Validate: `node <kivo-creator>/scripts/validate-spec.mjs .creator/<run>/specs`.
5. Hand over to `section-matching` with the run folder.

## Verification

- `validate-spec.mjs` prints `ok` for every spec.
- Every non-chrome spec has `refs` for 390 and 1440 (unless the element is hidden at one width; note it).
- The number of non-chrome specs equals the number of sections a person sees on the page.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Exit 3 and an install hint | Playwright not installed in the project | Ask the person; install it as a dev dependency with their package manager and `npx playwright install chromium` |
| Whole page is one section | No `<main>` and several wrappers with more than one child | Run again with `--selector=<css>` for the section container, or split the spec by hand (Procedure step 3) |
| Missing section that appears after scrolling | Lazy content not rendered at `networkidle` | Ask for a static export of the page, or remove the lazy loading in a local copy before ingesting |
| `refs` missing for 390 | The section is hidden on mobile | Keep the spec; note it; verify only checks widths that have references |
| Wrong text in a slot (cookie banner, overlay) | The overlay is part of `<body>` | Delete the overlay's spec or slots; note the decision |

## Escalation

Stop and ask when the page needs a login, when the source is not reachable, or when the person disagrees with the section split and the right split is not visible in the references.
