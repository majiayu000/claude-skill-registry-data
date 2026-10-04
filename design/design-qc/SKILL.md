---
name: design-qc
description: Visual QC of a running UI — captures screenshots via `openwolf designqc`, then reviews them against modern UI standards (DevSkyy dashboard) or SkyyRose brand canon (WP theme). Use when the user asks to check, evaluate, or improve the design/UI of the DevSkyy app or the SkyyRose theme. Do NOT use for choosing or migrating a component framework (that is `reframe`) or for building net-new UI from scratch (that is `frontend-design` / `fashion-theme-architect`).
---

## When to use

- The user asks to check, evaluate, or improve the design/UI of a running surface — the DevSkyy
  dashboard (`frontend/`, localhost:3000) or SkyyRose theme pages.
- After a batch of UI edits, when a before/after visual pass is wanted prior to deploy.
- `.wolf/OPENWOLF.md` routes "Design QC" requests here (auto-trigger on matching requests).

**When NOT to use:**

- Component-framework selection or migration → `reframe` skill.
- Designing/building net-new UI → `frontend-design` / `fashion-theme-architect`.
- Post-deploy production verification → `node scripts/verify-live-playwright.mjs` spec gate or the
  deploy-and-verify agent. This skill reviews captured pixels; any severity claim about production
  requires its own `[live]` probe (bug-287).

## Inputs

Required before starting. **Absent input = STOP** — never fabricate a review (fail-open is bug-230, ×6):

1. **Capture CLI** — `command -v openwolf` returns a path. Observed 2026-07-29: the global install at
   `/Users/theceo/.npm-global/bin/openwolf` was a *broken symlink* (package removed) — treat that as
   absent. When absent: say so, and do NOT review from memory or from the historical
   `.wolf/designqc-archive/` shots. Fallback capture only if a real target is reachable: the
   Playwright MCP screenshot tool (`browser_take_screenshot` / `playwright_screenshot`).
2. **A running, reachable target** — the command auto-detects a dev server (or starts one from
   package.json); pass `--url <url>` only if auto-detection fails. No reachable target → nothing to
   capture → STOP.
3. **For SkyyRose theme QA: canon inputs** — `docs/design/visual-pattern-shortlist.md` (the screened
   motion-pattern list) and the brand tokens `#B76E79` / `#0A0A0A` / `#C0C0C0` / `#DC143C` /
   `#D4AF37`. Shortlist missing → do not improvise the pattern screen; stop and name the gap.

## Procedure

1. Preflight the capture tool (`command -v openwolf`) — absent → STOP per Inputs.
2. Run `openwolf designqc` via Bash. It saves compressed JPEG screenshots to
   `.wolf/designqc-captures/`; full pages are captured as sectioned viewport-height images
   (`<route>__<viewport>_top.jpg`, `_section2`, …, `_bottom`).
3. Read the captured screenshots from `.wolf/designqc-captures/` with the Read tool.
   **Token awareness:** each screenshot costs ~2500 tokens (JPEG quality 70, max width 1200px).
   For large apps, limit captures with `--routes / /specific-page`.
4. Evaluate against the criteria for the surface:
   - **DevSkyy dashboard** (Shadcn UI, Tailwind, clean React patterns): spacing and whitespace
     consistency · typography hierarchy and readability · color contrast and accessibility (WCAG) ·
     visual hierarchy and focal points · component consistency · whether the design reads "dull" or
     "white-coded" (generic, no personality).
   - **SkyyRose WordPress theme** — the generic list does NOT apply; this is a brand-locked
     luxury-streetwear storefront, not a dashboard. Replace it with:
     - Cross-reference every animated/motion element against `docs/design/visual-pattern-shortlist.md`
       — is it one of the 176 screened patterns, or an unscreened improvisation? Flag anything that
       reads generic-SaaS (glassmorphism dashboards, gradient-blob-on-white heroes,
       Inter/Space-Grotesk-as-safe-default) — the shortlist exists to keep this theme out of that
       territory.
     - Grep new CSS/JS for cut fonts (`Cormorant Garamond`, `Playfair Display`, `Bebas Neue`,
       `Yellowtail`) in **live `font-family` declarations** — hard fail regardless of how the design
       looks. (A name-only grep false-positives on migration comments — see Failure modes.)
     - Every motion/animation carries a `prefers-reduced-motion: reduce` fallback — not optional here.
     - Hex values trace to the real tokens listed in Inputs, not placeholder colors left over from a
       sourced pattern spec.
     - "Dull or white-coded" becomes: does it read as Kith / Oaklandish / Culture Kings / Fear of God
       / Palm Angels, or does it drift toward European-luxury-serif or generic streetwear-template
       territory?
5. Deliver specific, actionable findings — each anchored to a `file:line` or a named screenshot, with
   an evidence-scope tag (`[repo]` for source reads, `[repro]` for checks run this session). No
   `[live]` probe → no production-severity wording.
6. If the user approves, implement the fixes. Theme CSS/JS edits require a `.min` rebuild
   (`cd wordpress-theme && npm run build`) — production serves `.min`, so a source-only edit ships
   nothing.
7. Re-run the capture and compare before/after screenshots for the changed routes.

## Verification

Run these before reporting; each can return "no".

1. Cut-font gate — live declarations only, not mentions:

```bash
grep -rnE "font-family[^;}]*(Cormorant Garamond|Playfair Display|Bebas Neue|Yellowtail)" \
  wordpress-theme/skyyrose-flagship/assets/css/ --include='*.css'
```

**PASS:** exits 1 (zero matches). Observed passing 2026-07-29. `[repro]`

2. Reduced-motion coverage heuristic — animation files with no in-file fallback:

```bash
grep -rlE '@keyframes|animation:' wordpress-theme/skyyrose-flagship/assets/css/ --include='*.css' \
  | grep -v '.min.css' | xargs grep -L 'prefers-reduced-motion'
```

**PASS:** empty output. Any file listed is a flag at `[repo]` scope — a global reduce block in
another enqueued file can still cover it, so trace coverage before asserting a defect.

3. After implementing theme fixes, rebuild and run the theme gate:

```bash
cd wordpress-theme && npm run build && npm run verify:theme
```

**PASS:** both exit 0. `[test]` A gate that errors or times out has NOT passed — its zero-findings
output is an artifact; re-verify by hand (bug-230).

4. Capture freshness: at least one `.jpg` in `.wolf/designqc-captures/` with an mtime after this
   run started — reviewing archive shots is a stale-state verdict, not QC.

## Worked example

Real run, this worktree, 2026-07-29. Check 2 (reduced-motion heuristic):

```bash
$ grep -rlE '@keyframes|animation:' wordpress-theme/skyyrose-flagship/assets/css/ --include='*.css' \
    | grep -v '.min.css' | xargs grep -L 'prefers-reduced-motion'
wordpress-theme/skyyrose-flagship/assets/css/main.css
wordpress-theme/skyyrose-flagship/assets/css/agency-tier-visuals.css
```

Two real files carry animation with no in-file reduce fallback — flagged `[repo]`, handed to the
theme owner to either add the fallback or point at the covering global reduce block. Severity stays
"flag": no `[live]` probe was run.

Same session, check 1: a *name-only* grep for the cut fonts matched
`assets/css/fonts.css:14` — a comment documenting the 2026-07-10 migration ("Bebas→Anton,
Yellowtail→Pacifico (BR)"), not a live declaration. The `font-family`-scoped grep above exited 1.
Diff the match *contents*, not just the match count, before calling a violation.

A prior capture set exists at `.wolf/designqc-archive/` (e.g. `about__desktop_top.jpg`, 50.6K) —
useful as a naming reference for the sectioned-capture format, never as review input.

## Failure modes

- **Capture CLI silently absent** — `openwolf` resolved to a broken symlink on 2026-07-29 `[repro]`.
  Proceeding to "review" without fresh pixels is the fail-open pattern (bug-230): absent input =
  STOP, not a default.
- **Reviewing `.wolf/designqc-archive/` instead of fresh `.wolf/designqc-captures/`** — archive
  shots are frozen history; verdicts drawn from them describe a past deploy, not the tree under
  review.
- **Name-grep for cut fonts flags a doc comment** — real instance at `fonts.css:14`. Scope the grep
  to `font-family` declarations, and read the matched line before reporting.
- **Reduced-motion heuristic over-claims** — it is per-file; a global reduce block elsewhere can
  cover a listed file. Report at `[repo]` scope and trace before escalating.
- **Severity scope-jump** — screenshots of a dev server say nothing about production. "Production
  bug" wording requires a `[live]` probe (bug-287).
- **Theme fix without `.min` rebuild** — production serves `.min`; editing only the source ships
  nothing. Always `cd wordpress-theme && npm run build` and re-verify both files.
- **Token blowout on large apps** — every screenshot is ~2500 tokens; use `--routes` to cap the set
  instead of skipping the read (an unread capture is an unreviewed capture, not a pass).
