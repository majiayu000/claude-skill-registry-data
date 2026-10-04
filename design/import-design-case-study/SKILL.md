---
name: import-design-case-study
description: Import a case study from a claude.ai/design canvas project (a case-study-*.dc.html file plus its assets) and turn it into a fully-wired, on-brand page in this Gatsby portfolio — new route, downloaded or placeholder images, homepage card, and real diagram-design SVG diagrams for any flowcharts/journeys in the source content. Use this whenever the user pastes a claude.ai/design URL pointing at a case study, says something like "import this case study", "add a new case study from claude design", "convert this .dc.html into a page", or wants to replicate the Flexera/Spektrum case-study import already done on this site. Also trigger if they mention DesignSync, the claude_design MCP, or a project file named case-study-<something>.dc.html, even without an explicit "import" verb.
---

# Import a case study from claude.ai/design

You're given a URL into a claude.ai/design canvas project pointing at one `case-study-<slug>.dc.html` file. The job is to turn that into a real page on this site — not a copy of the design tool's HTML, but this case study's actual content rebuilt with this repo's own components, theme, and conventions.

This is a genuinely multi-step workflow. Don't try to do it in one giant pass — work through the phases below in order, and read the referenced files at the point where you need them rather than all up front (they're detailed, and loading them before you know you need the specifics just crowds your context for no benefit).

## Phase 1 — Pull the content

Read `references/design-import.md` now. It covers: resolving the project ID from the URL, using `DesignSync` to list and fetch files, the 256 KiB read cap that silently corrupts large binary assets (and how to detect that instead of shipping garbage), and how to read a `.dc.html` file that's too long for one preview.

Come out of this phase with: the full text of the target `.dc.html`, every asset it references either downloaded intact or flagged as needing a placeholder, and a mental outline of the case study's sections (hero, problem, research, any flowchart-shaped content, journey, final design, impact/next-steps — the exact section set varies per case study).

## Phase 2 — Handle any oversized assets

For every asset that came back truncated (see Phase 1's detection method), generate a placeholder at its exact source filename with:

```
python3 .claude/skills/import-design-case-study/scripts/make_placeholder.py <path/to/asset.ext>
```

Then tell the user, once, which images are placeholders and why (see the "Talking to the user about placeholders" section in `design-import.md` for how to phrase this without being annoying about it).

## Phase 3 — Rebuild it as a page

Read `references/case-study-conventions.md` now. It covers: where the page/images/homepage-card entries go, the shared `src/components/caseStudy/` kit you should be building on top of (not duplicating), the `tone.ts` color rule and *why* it's load-bearing here (stock Tailwind color classes emit zero CSS on this site's reset theme — a silent failure, not a wrong color), how to translate the source's one-off design-tool colors into the site's real theme, and the verification steps (typecheck, format, dev server, and — important — why you shouldn't trust a Browser-pane screenshot alone in this environment).

This phase is where most of the actual work happens. Match the site's voice and layout patterns from the two existing case studies (`src/pages/case-studies/flexera.tsx`, `src/pages/case-studies/spektrum.tsx`) as living examples of the target shape, but don't copy their specific content structure if this case study's content wants something different — they're references for *how to build*, not a template every case study must fit.

## Phase 4 — Diagrams

If Phase 1 turned up any Mermaid blocks, hand-styled flowchart-as-divs content, or reasoning chains (research finding → decision → outcome, a process lifecycle, a timeline) — don't leave these as prose or ship the source's Mermaid/div version. Read `references/diagram-design-integration.md` and rebuild them as real inline SVG using the diagram-design skill's conventions, already onboarded to this project's own theme (the `nisha-portfolio-coffee-roast` profile — you don't need to re-onboard).

This reference also documents a specific, easy-to-miss bug (the site's global font reset silently overriding a diagram's intended typography via CSS cascade rules) and how to verify you actually avoided it — worth reading even if you think you already know how to set an SVG font.

If the case study has no diagram-shaped content, skip this phase entirely — don't manufacture a diagram just because the skill has a step for it.

## Phase 5 — Wire it up and verify

- Add the homepage card (Phase 3 covers where).
- Add the `Head` export with `SEO` + (if Phase 4 produced diagrams) the Geist font link.
- Run the verification steps from `case-study-conventions.md` in full — typecheck, format, dev server, live DOM checks. A case study that typechecks but was never actually loaded in a browser is not done.
- Summarize for the user: what got built, which images are placeholders and their exact paths (so they know what to replace later), and any content judgment calls you made (Phase 3's "fidelity vs. editorial judgment" section) that they might want to weigh in on.
