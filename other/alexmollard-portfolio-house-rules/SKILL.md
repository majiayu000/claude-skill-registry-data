---
name: alexmollard-portfolio-house-rules
description: "Use when editing anything in D:/AlexMollard, Alex Mollard's portfolio site and CV: copy, a project entry, cutting a weak project, the CV, Australian spelling, em dashes, build_mode, the owner's title, shipped titles or education, Unity or DreadedEscape wording, or verifying a change there with npm build/preview."
---

# Alex Mollard portfolio house rules

Standing conventions for `D:/AlexMollard`. This file states the rules; each procedure
lives in the skill it names.

Repo: Astro 6 static + Tailwind v4, single page `src/pages/index.astro`, content
collection in `src/content/projects/*.md` (schema `src/content.config.ts`). Remote
`AlexMollard/alexmollard-portfolio`.

## Identity facts (owner-confirmed, do not re-derive)

- **Senior Generalist Programmer at Big Ant Studios**, Melbourne. Promoted recently;
  every surface must say this exact title. Shipping since 2022.
- **8 shipped titles**: Cricket 22/24/26, AFL 23/26, Rugby 25, Rugby League 26, TIEBREAK.
  Derived at build time from `category: Professional` minus `domain: Tools` - never hardcode.
- **Advanced Diploma of Professional Game Development, AIE Melbourne**, plus heavily
  self-taught. Credit both; do not say self-taught alone.
- LinkedIn `https://au.linkedin.com/in/alex-mollard` (returns HTTP 999 to bots - that is
  LinkedIn's anti-scrape code, not a dead link). Email `alexmollard@protonmail.com`.
- **Unity**: real prior experience (Frozen Depths, and 2019-2020 C# projects) but the owner has
  **not used it in years** and does **not** prototype in it; they prototype in their own C++
  engines. Never imply current/daily Unity use.
- **DreadedEscape**: included, but as an *unfinished weekend prototype* with two friends -
  UE5 replication + Steamworks experience. Never "shipped", never a finished game.

## Writing rules (site and CV)

- **Never use em dashes (`—`) or `&mdash;`.** Use ` - `. This is absolute, CV and site.
- **Australian English**: behaviour, visualisation, colour, centred, ageing, optimisation,
  customisable, analyse. But `program`, and keep project names as-is
  (`RS3 Grand Exchange Analyzer` matches the repo). Never touch CSS `--color-*`,
  `color:` properties, `theme-color`, or Tailwind class names when sweeping spelling.
- Serial comma, first person, past tense, complete sentences. No self-deprecation.
- Every claim traces to repo content or an owner statement. Nothing invented.
- **Collapse, never cut.** Weak/early projects fold into the `Early Work (2019-2022)` entry
  with one bullet each (name, year, technique). Deleting a project outright is forbidden.
- `performance_metrics` holds only real figures. Process statements ("Commercial release
  pipeline") get deleted, and the key removed if nothing measurable remains.
- No boilerplate reused across the sports titles - each describes its own certification work.

## Authorship disclosure (non-negotiable)

- Schema: `build_mode: Hand-written | Agent-directed` (default `Hand-written`) plus a
  `build_note`. Agent-directed as of 2026-09-24: AetherCore, RS3 Analyzer, Crash
  Twinsanity Improved, Ironvellum, and this portfolio. Source of truth:
  `grep -l '^build_mode: Agent-directed' src/content/projects/*.md`.
- Agent-directed projects show an `Agent-directed` chip on the card and in the case-study
  header, plus a "How it was built" block in the Overview tab.
- The owner is the architect/reviewer; agents implement. Framing rule: this is a *selling point*
  (direction + verification floor), never an apology.
- `build_note` is always a `>-` block scalar. To add or change a disclosure, follow
  `portfolio-agent-authorship-disclosure`; it holds the YAML colon trap.

## CV

`scripts/cv.html` is the source; `public/alex-mollard-cv.pdf` is its printed output,
linked from the hero and the footer through `cvHref`. It must stay one page. When a fact
changes on the site (title, shipped titles, contact), make the same edit in `cv.html` and
reprint. To print it and prove one page, follow `portfolio-cv-pdf-from-site-content`.

## Verify before claiming

Build with `npm run build`, serve it with `npm run preview` (background job,
localhost:4321; stop any dev server first, it defaults to the same port), then check in
a headless browser. The dev server is for iterating;
claims come from the built preview.

- git-bash: plain `npm run preview`. Never `cmd.exe /c npm.cmd ...` - MSYS rewrites `/c`
  into a path, so cmd opens an interactive shell, reads EOF and exits 0 having run
  nothing (verified 2026-09-24).
- PowerShell: `cmd.exe /c npm.cmd run preview`.

Geometry claims need numbers: tile gap `liHeight - imgHeight`, contrast ratios computed
from the real hex values, card counts from the DOM.

## Other procedures here

- Project detail overlay (tabs, focus, zoom, mobile wrap): `portfolio-project-overlay-tabs`.
- Whole-site review as a hiring artifact: `portfolio-hiring-artifact-audit`.
