---
name: readme-polish
description: Audit a GitHub README and rewrite it using modern 2025-2026 patterns — centered header, badges, hero image, GitHub alert callouts, emoji-prefixed features, expandable details, Mermaid diagrams, tables over dense prose. Produces a scannable README that works for a 10-second skim and a deep dive.
---

# Readme Polish

## Overview

Modern GitHub READMEs are **scannable first, readable second**. A skimmer should understand what the project does, who it is for, and how to install it in 10 seconds. Motivated readers get more detail from collapsibles, tables, and follow-up sections.

This skill takes an existing README (or a blank slate) and rewrites it using the visual and layout patterns that well-regarded 2025-2026 open-source projects have converged on. It does **not** invent the content; content comes from the project itself. It shapes how that content is presented.

## When to Use

- A README is a text wall with no visual anchors and no one can tell what the project does from a first glance.
- An OSS release is about to ship and the README has not been pass-edited for discoverability.
- The README mixes reference material with quickstart, so the install path is buried.
- Publishing badges, adding a hero image, or restructuring sections would measurably help adoption.
- A practitioner with social credibility wants the README to convey both "this is legit" and "here is how to use it" without competing for attention.

## When NOT to Use

- The README already follows the patterns below and the content is fine. Do not thrash for style.
- The project is internal / private / never published. No audience to optimize for.
- The project needs documentation at site-level scale (tutorials, API reference, cookbook). README polish only covers the repo root; use Sphinx / MkDocs / Docusaurus for real docs sites.

## Phase 1: Audit the current README

Before editing, classify what is there against the modern-README checklist. The goal is to identify which patterns are missing, which are misapplied, and which content should be moved, collapsed, or deleted.

Use [`references/checklist.md`](references/checklist.md) as the audit grid. For each row, mark present / absent / broken.

Key audit questions:

1. **First-paint (above-the-fold)**: is the project name, one-line tagline, badges, and install command visible before the reader has to scroll? If not, content above those is displacing them.
2. **Credentials placement**: is there a 100+ word maintainer bio blocking the first section? Move it into a `> [!NOTE]` callout or footnote.
3. **Why-section shape**: if the README has a "Why you'd use this" or scenario block, are the items narrative (cause / effect, before / after) or feature-shaped? Narrative content reads warmer as bold-lead paragraphs; feature claims read cleaner as emoji-prefixed bullets. Pick one pattern per section.
4. **Install path clarity**: can the reader find a single working install command in under 5 seconds? If not, there is probably too much pre-install framing.
5. **Reference material above-the-fold**: are limitations, related projects, detailed repo layout, maintenance policy visible before install? They should be collapsed.
6. **Visual anchors**: does the first screen have badges, a hero image, or a diagram? Without at least one, the README feels like documentation instead of a product page.
7. **Examples block (What This Looks Like)**: does the README show what the project LOOKS LIKE in practice (screenshot, file tree, themed diagram, before / after, mock)? If yes, do 3+ examples each use a different visual format, or are three monospace blocks stacked in a row? The latter reads as a text wall regardless of content quality.
8. **Themed Mermaid**: if Mermaid diagrams exist, do they use `%%{init: ...}%%` to match brand palette, or do they render with the default red/orange/blue and clash with the rest of the page?
9. **Heading case**: is Title Case applied consistently across all H2 and H3? Sentence-case headings mixed with Title Case headings read as AI-generated or unedited (agent-style RULE-G).
10. **Version-boundary honesty**: if a release ships primitives that are not yet wired, does the README name the boundary explicitly (what works today, what is queued), or does it present roadmap claims as shipped behavior?
11. **Anchor hygiene**: do dot-nav links resolve to real sections (GitHub's auto-generated anchor rules: lowercase, hyphens for spaces, strip punctuation)?

## Phase 2: Apply modern patterns

See [`references/patterns.md`](references/patterns.md) for the full catalog with copyable snippets. Summary of the highest-impact patterns:

### Hero / first-paint
- **Centered header** via `<div align="center">`. Title, one-line tagline, badge row, dot-separated nav, one-liner elevator pitch.
- **Shield.io badges** for package version (PyPI, npm), license, CI status, GitHub stars. Keep to 4-5; more than that becomes noise.
- **Dot-separated nav links** (`[Install](#install) · [Workflow](#workflow) · [Features](#features)`) below badges. Helps skimmers jump.
- **Hero image** — a PNG or SVG that makes a skimmer stop scrolling. Two paths:
  - HTML mockup rendered via headless Chrome → PNG (good for feature grids, dashboards). See `ci-mockup-figure` skill for capture workflow.
  - `<picture>` tag with light/dark variants for logos. Required only when the project has a logo/wordmark.
- **Maintainer credibility** in a `> [!NOTE]` callout, not a prose paragraph. Ideal length: 2–3 sentences with verifiable signals (package stars, citations, institutional affiliation).

### Content body
- **GitHub alert callouts** for emphasis: `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`, `> [!CAUTION]`, `> [!IMPORTANT]`. Each renders as a colored box with an icon. Do not overuse — one per major section at most.
- **Emoji-prefixed one-liner bullets** for "What you get" / "Features" when items are feature claims. Each bullet = 1 emoji + bolded feature name + one-line takeaway. 5–8 bullets is the sweet spot.
- **Bold-lead scenario paragraphs** for "Why you'd use this" when items are narrative (cause / effect, before / after). Pattern: `**Bold lead sentence.** Setup. Without X, problem. With X, fix.` Reads warmer than emoji-bullet lists when content is story-shaped.
- **"What This Looks Like" examples block** between How It Works and Install — 3 to 5 examples, each in a different visual format (screenshot / file tree / themed Mermaid / HTML 2-col before-after / terminal mock). The format-variety rule is the whole point; three monospace blocks in a row defeat it. See `patterns.md`.
- **HTML 2-col `<table>` for rich before/after comparisons** — markdown tables cannot carry blockquotes, italic, or `<mark>` tags inside cells; HTML tables can. One per README is enough.
- **Tables over dense bullets** for reference material (comparison, decision matrices, scenario → command). Tables read faster than bullets when the content is inherently tabular.
- **Themed Mermaid** for architecture, flowcharts, and sequence diagrams — use the `%%{init: ...}%%` config block at the top to match brand palette. The default red / orange / blue clashes with most modern brand colors and reads as cookie-cutter. Do not use Mermaid as the hero image; it lacks the visual weight a polished mockup carries.
- **Version-boundary honesty** as a content principle: when v0.4.0 ships primitives but the wiring is in v0.4.x, name the split explicitly. Roadmap claims belong in a "What's Next" section pointing at the changelog, not in the install / How It Works flow.
- **Collapsible `<details>` blocks** for platform-specific variants, limitations, related projects, repo layout, FAQ, anything reference-shaped.
- **Back-to-top anchor** (`<a name="readme-top">` + `<a href="#readme-top">↑ back to top</a>`) at the bottom of long READMEs.

### Structure
- **Above-the-fold (first ~40 lines)**: centered header → badges → nav → hero image → maintainer callout → tagline → elevator pitch.
- **Middle**: quickstart + install, "what you get" bullets, optional "why / philosophy" narrative.
- **Below**: day-to-day usage, contribution notes, limitations, related projects, license.
- **Collapsed into `<details>`**: platform-specific install variants, repo layout, opinionated-and-why, limitations, related projects, maintenance policy.

## Phase 3: Verify

Before publishing, verify the rewrite actually renders on GitHub (not just in PyCharm / VS Code preview).

- [ ] Push to a branch and view on GitHub. GitHub-specific features that do **not** render in most local previews: `> [!NOTE]` callouts, Mermaid diagrams (themed and unthemed), `<picture>` light/dark media queries, autogenerated heading anchors for non-ASCII text, HTML `<table>` with markdown blockquotes inside cells.
- [ ] Click every dot-nav link. Broken anchors are the most common bug introduced by rewrites.
- [ ] Check the README at different viewport widths (desktop, narrow / mobile). Tables with long cells may overflow; hero images should be `width="100%"` or responsive.
- [ ] Confirm badges show live status (not a broken image). Shield.io URLs are case-sensitive for package names.
- [ ] If the project has multiple surfaces (README + RTD landing + `README.zh-CN.md`), run a cross-surface drift pass. Tagline, How It Works structure, Pack-CLI claims, and What's Next paragraph should agree across surfaces. The `implement-review` skill handles this via "Cross-variant drift check."
- [ ] If any colored elements were customized (badge color, Mermaid theme, MkDocs CSS), verify WCAG AA contrast (≥ 4.5:1 for normal text against background) for both light and dark themes. Codex / Copilot reviews compute the ratios on request.
- [ ] If the README references a rendered asset (PNG / GIF), verify the source file (HTML / tape) and the render helper (`_render_*.py` / `_render_*.sh`) are committed alongside it. Reproducibility matters for future rerenders; pinned Docker digests beat `:latest` tags.
- [ ] Run `git diff --cached --check` before committing to catch trailing whitespace.

## Common Pitfalls

- **Over-badging.** More than 5-6 badges reads as clutter, not signal. Prioritize: package version, license, CI status, maybe stars or download count.
- **Emoji overload.** Every section header with an emoji becomes noise. Reserve emoji for the one-liner feature bullets.
- **Hero image that is just the logo.** A modern hero communicates what the project does (feature grid, animated demo, flowchart), not just the project name.
- **Callout abuse.** If every third paragraph is `> [!NOTE]`, none of them stand out. Use callouts only for "this is the one thing you must not miss" moments.
- **Collapsibles hiding the install command.** The install path must always be visible. Collapsibles are for reference material, not the critical path.
- **Dot-nav pointing to missing anchors.** GitHub auto-generates anchors from heading text — lowercase, hyphens for spaces, strips most punctuation. Always verify post-rewrite.
- **All-monospace examples in a row.** Tree + code block + terminal mock stacked together read as a text wall regardless of content quality. Vary the visual format across adjacent examples (PNG, ASCII tree, themed Mermaid, HTML 2-col, terminal mock).
- **Narrative scenarios forced into feature bullets.** If each item needs setup, problem, and fix, use bold-lead paragraphs. Emoji bullets are for compact feature claims.
- **Rich before/after squeezed into a markdown table.** Markdown tables cannot carry blockquotes, `<mark>`, or multi-paragraph commentary reliably. Use the HTML 2-col table pattern and keep blank lines inside each `<td>`.
- **Multi-surface README drift.** README, RTD landing, and bilingual variants diverge unless they are reviewed as variant targets. Keep tagline, How It Works, Pack CLI, and What's Next aligned.
- **Roadmap presented as today's behavior.** "v0.4.0 ships X" without naming what is queued for v0.4.x reads as overpromise to attentive readers and to Codex / Copilot reviewers. Mark version boundaries explicitly.
- **Default Mermaid in a branded README.** Red error / orange warning / blue info clash with most modern brand colors. Add `%%{init: {'theme': 'base', 'themeVariables': {...}}}%%` at the top of every Mermaid block.
- **Sentence-case headings mixed with Title Case.** Pick one and hold it across all H2 and H3. Sentence-case sub-headings inside a Title Case context (or vice versa) read as machine-generated. agent-style RULE-G says Title Case.
- **Asset rendered once, source not committed.** Hero PNG without the HTML source, GIF without the vhs tape, banner PNG without the render helper — every rendered asset becomes brittle. Commit the source AND a `_render_*.py` / `_render_*.sh` helper alongside.
- **PyCharm preview false confidence.** PyCharm's built-in markdown renderer does not render `> [!NOTE]`, Mermaid, `<picture>` media queries, or HTML `<table>` with markdown blockquotes inside cells. Only GitHub's renderer is authoritative.

## Integration with Other Skills

- **`ci-mockup-figure`** — use it to design and render the hero image when the README needs a custom feature-grid, architecture diagram, or pack-architecture pipeline. That skill handles the HTML-to-PNG capture workflow via Playwright.
- **`implement-review`** — run a Codex review on the staged README rewrite before pushing. Lens: `general` / `docs`. Focus: first-read flow, anchor validity, content accuracy, version-boundary honesty, agent-style compliance, cross-surface drift if multi-surface. Plan on 2-4 review rounds for a substantial overhaul; expect findings to drop from High / Medium in early rounds to Low polish in late rounds.
- **`agent-style`** — the writing rule pack governs the README prose: 21 rules total, 12 classic + 9 LLM-observed. RULE-G specifically governs Title Case across H2 / H3; RULE-B forbids casual em-dash; RULE-E forbids paragraph-closing summaries; RULE-F enforces consistent terms. Use the public [agent-style rule pack](https://github.com/yzhao062/agent-style/blob/main/docs/rule-pack.md) for the full reference and run a self-audit before requesting external review.

## Output

A rewritten `README.md` (and optional hero assets under `docs/`) that:
- Reads cleanly in under 10 seconds for the tagline + install path
- Has badges, dot-nav, hero image, at least one callout, and at least one collapsible
- Keeps all prior content (moved or collapsed, not deleted) unless the content was stale or duplicated
- Renders correctly on GitHub (the only renderer that matters)

See [`references/patterns.md`](references/patterns.md) for full pattern snippets and [`references/checklist.md`](references/checklist.md) for the audit grid.
