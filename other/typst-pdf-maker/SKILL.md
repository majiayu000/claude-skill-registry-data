---
name: typst-pdf-maker
description: "\"Generate professional, high-quality PDF documents with Typst. Use for reports, academic papers, resumes, structured documents, mathematical typesetting, code-rich documents, precise layouts, and CJK typography when Markdown-to-PDF is insufficient. Select one skill-owned asset or compatible Typst Universe base before adding packages. Route ordinary presentation requests to Manus Slides/PPTX unless the user explicitly requires Typst-generated PDF slides.\""
compatibility: opencode
---

# Typst PDF Maker

For the commands below, replace `<skill-dir>` with the **absolute directory containing this loaded `SKILL.md`**, using its actual read path or the current runtime Skill catalog locator. Keep the quotes, including when the path contains spaces. Use a path accessible on the computer executing the command; do not derive it from the shell working directory or assume an installation root. Bundled documentation links resolve from the file containing the link. For the examples, replace `<report-dir>` and `<markdown-report-dir>` with your chosen absolute output directories on the active computer, and `<source-md>` with the absolute path to the input Markdown file. These are document paths, independent of the Skill installation directory; keep their quotes too.

Use Typst for polished, structured PDF documents that require precise typography or layout control. Do not use this skill as the default presentation channel: route ordinary slide requests to Manus Slides/PPTX, and reserve Typst slide engines for explicit Typst or PDF-slide requirements.

## Prerequisite

Check the installed CLI before attempting installation:

```bash
typst --version
```

Only install Typst if that command fails. Preserve the original tested download-based fallback exposed by `scripts/generate_pdf.py`; do not reinstall when the CLI is already available. Discover required fonts with `typst fonts`; never guess a font family.

## Routing workflow

Treat routing as one deterministic planning step rather than repeated package browsing during authoring.

1. Build a compact **content manifest** and save it as `.typst-content-manifest.json` in the working directory. Complete it before planning: inspect the source and acceptance criteria once, and record every observable package-triggering feature. Do not run the planner with a partial manifest. Use the planner's real keys rather than inventing synonyms:

   ```json
   {
     "task_kind": "new-document",
     "output": "pdf",
     "signals": ["ieee"],
     "hard_constraints": [],
     "content_features": {
       "code_blocks": 0,
       "defined_terms": 0,
       "portrait_images": 0
     }
   }
   ```

   Use `task_kind: "markdown-to-pdf"` for an existing Markdown source, `"existing-typst"` for an existing Typst project, `"presentation"` for ordinary slides, and `"typst-presentation"` only for explicit Typst/PDF slides. Put a user-named template ID, publication format, or observable document-class signal in `signals`; leave it empty for a general report. Put package-triggering evidence in `content_features`, not in prose outside the manifest.
2. Run the deterministic planner once after the manifest is complete. This is the normal way to find templates and packages: it reads `references/routing-catalog.json` without loading the entire catalog into conversational context. Freeze the resulting plan when base initialization or authoring begins. Rerun only to resolve the plan's recorded `ambiguous` or `needs-confirmation` question, after a user or publication hard constraint changes, or after an explicitly recorded blocked/patch-required condition changes. A late optional visual idea is not a rerouting reason.

   ```bash
   python3 "<skill-dir>/scripts/plan_document.py" \
     .typst-content-manifest.json \
     --output .typst-build-plan.json
   ```

3. If the output plan has `reused: true`, continue without rescanning the ecosystem. The planner reuses a plan only when the content manifest, Typst version, and catalog version produce the same fingerprint.
4. If the plan redirects ordinary presentation, slide, PPT, or PPTX work, exit this skill and use Manus Slides/PPTX. Continue here only for explicit Typst, PDF slides, or a named Typst slide engine.
5. Follow the selected base exactly. The planner chooses one existing project, one required Universe template, or one skill-owned built-in asset before choosing enhancements.
6. If the plan is `ambiguous` or `needs-confirmation`, ask its single recorded question and rerun the planner after updating the manifest. Do not initialize or import candidates before the ambiguity is resolved.
7. Treat files under `assets/` as **built-in assets**, not Universe templates. Use `report-entry.typ` for a native report and `markdown-entry.typ` for an existing Markdown source.
8. Apply Class A semantic necessities automatically; apply the single recorded Class B low-risk local visual enhancement when present; require confirmation for Class C structural or style-owning changes.
9. Respect the plan's one-owner result for each conflict group, including slide engine, code block, content box, diagram, chart, and text-wrap groups. Let the selected template own global page geometry and typography unless a user or publication constraint has higher priority.
10. Apply paragraph and section rhythm in this order: user or publication hard constraints, template global layout, package component rules, skill-owned theme, then generic starting values. Only for the built-in native report, an agent-owned multi-paragraph component, an explicit restyle request, or diagnosis of agent-owned rhythm, read `references/layout-rhythm.md` once. Do not load or apply its profiles to venue templates, slides, résumés, invoices, cards, dense reference sheets, captions, tables, lists, or package internals by default.
11. Stop before initialization or import when the plan is `blocked`. Apply an explicitly recorded known patch before preflight when the plan is `patch-required`.
12. Run one **minimum compile preflight** for the selected base and exact imports; do not compile every candidate. Record the preflight result in `.typst-build-plan.json`, then reuse that plan during authoring and repair instead of rerouting.

### How to locate and execute the selected base

The catalog is a registry, not a directory containing downloaded template source files. The planner is the lookup layer. Read `.typst-build-plan.json` after planning and follow this table:

| Plan result | Required action |
|---|---|
| `channel: "manus-slides-pptx"` | Exit this skill and use Manus Slides/PPTX. |
| `state: "ambiguous"` or `"needs-confirmation"` | Ask only the plan's `question`, update the manifest, and rerun. Do not initialize anything yet. |
| `state: "blocked"` | Stop before initialization and report `base.block_reason`. |
| `state: "patch-required"` | Apply only `base.patch_note`, then run the minimum compile preflight. |
| `base.kind: "asset"` | Use the matching `prepare_document.py` workflow documented below. `base.path` is relative to `<skill-dir>` and identifies the skill-owned entry; it is not relative to the document project or shell working directory. |
| `base.kind: "universe-template"` | Run `base.init_command` after replacing `<output-dir>` with the project directory. This command is derived from the exact `base.universe_ref`, for example `typst init @preview/charged-ieee:0.1.4 my-paper`. |
| `base.kind: "existing-project"` | Preserve the existing project's entry points and style ownership; do not initialize a second base. |
| `base.kind: "universe-package"` used as an explicit slide engine | Use `base.universe_ref`, inspect that package's public entry API, and run its minimum sample compile. Do not treat it as a local template file. |

For every selected enhancement, use its exact `universe_ref` from `enhancements`, `optional_idea`, or confirmed `confirmation_candidates`. Import that exact reference, then inspect the package's documented public symbols; do not guess exported function names. Do not search the filesystem for any of the 30 Universe templates or 43 packages. Typst retrieves their source when the exact Universe reference is initialized or imported.

Read `references/routing-catalog.json` directly only when diagnosing why a route was selected, explaining available candidates to the user, or maintaining the registry. During ordinary generation, the planner is the only catalog reader.

## Native professional report

Prepare a portable project from the shared report theme and native entry. Do not copy individual asset files manually or recreate the global style from scratch.

```bash
python3 "<skill-dir>/scripts/prepare_document.py" report \
  "<report-dir>" \
  --title "Report title" \
  --subtitle "Optional subtitle" \
  --author "Manus AI"
```

Edit `<report-dir>/main.typ` after the generated title page, outline, and page-counter reset. The entry imports the colocated `report-theme.typ`, which owns page defaults, typography, paragraph rhythm, headings, code blocks, links, and figure breaking. The native entry uses the R4 chapter-emphasis report rhythm by default: no first-line indent, `0.84B` paragraph spacing, and level-specific heading spacing relative to the body size `B`. For continuous longform prose, select `rhythm: "longform"` to use the T1 no-indent profile with a visible `0.65B` paragraph gap. Follow the ownership and profile rules in `references/layout-rhythm.md` instead of changing unrelated template or package styles. For non-trivial authoring, repair, or verification, read `references/production-workflow.md` once after routing; do not reload it during every edit cycle.

Before migrating Markdown or HTML into native Typst, map source syntax deliberately. Markdown `**bold**` becomes Typst `*bold*`; literal heading numbers must be removed when automatic heading numbering is active; HTML tables must become Typst tables.

Author a coherent, dependency-closed batch before compiling; do not compile after every heading, paragraph, table row, or small edit. Compile earlier only when a global style owner, cross-reference graph, package API, page geometry, or another high-risk dependency needs confirmation. After one failed compile, classify diagnostics by root cause and repair independent errors in one batch before recompiling.

Use discrete compilation by default. The wrapper prints bounded short diagnostics, writes the complete diagnostic stream from that compile to an artifact, and evaluates strict mode against the untruncated stream:

```bash
python3 "<skill-dir>/scripts/generate_pdf.py" \
  "<report-dir>/main.typ" --strict
```

Use `--diagnostics full` only when the short stream lacks enough source context. Do not automatically run both formats. Reserve `--watch` for an explicitly requested human continuous-editing session; autonomous editing uses discrete compile gates.

After a successful compile, run the deterministic verifier with a document-appropriate profile. Keep its JSON report as an artifact and return only the one-line summary to conversational context. When the report is `PASS`, do not separately rerun `pdfinfo`, `pdftotext`, `pdffonts`, or `pdfimages` checks already covered by that profile. Use a direct inspection command only to diagnose a reported `FAIL`, `WARN`, or `UNKNOWN`, or to answer a requirement the verifier does not represent:

```bash
python3 "<skill-dir>/scripts/verify_pdf.py" \
  "<report-dir>/main.pdf" --profile text-document
```

During iteration, visually inspect changed pages, adjacent reflow pages, affected navigation pages, and high-risk pages. Finish in standard review mode with a strict compile, deterministic verification, and the representative contact-sheet set produced by `scripts/render_review.py`; inspect individual pages only when a sheet flags a concern. Escalate to exhaustive every-page review only when the user explicitly requests it, sampled pages reveal a systemic defect, the verifier reports an anomaly needing visual diagnosis, or a theme, page-geometry, or global-pagination change invalidates the sample. Read `references/production-workflow.md` for the gate model, review modes, and context policy. Read `references/typst-patterns.md` only when the required layout feature is not already demonstrated by the prepared project.

## Existing Markdown source

Prepare a portable project that copies the source to `source.md`, binds the Markdown entry to that local path, and records the original path in `.typst-document.json`:

```bash
python3 "<skill-dir>/scripts/prepare_document.py" markdown \
  "<source-md>" \
  "<markdown-report-dir>"
```

Compile the prepared entry:

```bash
python3 "<skill-dir>/scripts/generate_pdf.py" \
  "<markdown-report-dir>/main.typ" --strict
```

Treat the Markdown entry as an adapter, not a second theme. It imports `report-theme.typ`, maps Markdown mathematics through a dedicated math package, normalizes auto-width Markdown tables, and intentionally leaves first-line indentation disabled so Markdown block separation remains natural. Extend the entry for title-page behavior; do not merge or duplicate global style blocks.

Preserve the original advanced `cmarker.render` controls when custom mapping is required: use `h1-level` for heading-level mapping, `raw-typst` for explicitly trusted Typst injection, and `scope` to override element rendering. Do not enable raw Typst injection for untrusted Markdown.

## Existing Typst project or Universe base

Preserve the existing project's base and ownership before adding packages. For a required Universe template, initialize only the exact version selected by the build plan, inspect its generated entry points, and run the minimum compile preflight before editing content. Do not assume the newest package version is compatible with a template that pins older transitive dependencies.

Import only the package and exact version selected by the build plan. Typst retrieves missing Universe packages during compilation; no separate manual package installation is required.

The original résumé guidance named both `basic-resume` and `modern-cv`. The verified routing catalog pins `basic-resume`; if the user explicitly requires `modern-cv`, first verify its current Universe identifier and exact version, add that validated record to the catalog, and run the minimum compile preflight. Do not silently substitute or initialize an unverified legacy name.

## Best practices

- **Fonts:** Run `typst fonts | grep -i <keyword>` and use the exact installed family name; do not guess. For CJK documents, specify an installed CJK fallback after the Latin family, for example `#set text(font: ("Libertinus Serif", "Noto Serif CJK SC"))`. If a selected Universe template reports missing fonts, classify the result as a visual-fidelity warning rather than claiming exact fidelity.
- **Single source of numbering:** Let Typst number headings and figure captions when numbering is enabled. Do not duplicate automatic heading or figure numbering, and do not write literal prefixes such as `= 1.1 Introduction` or `caption: [Figure 1: ...]` on top of automatic numbering.
- **Markup mode versus code mode:** In code mode, nested function calls do not receive another `#`. Arguments inside `#function(...)` and braces in `context { ... }` are code mode; use patterns such as `context { set text(...); grid(...) }` and call `align(...)` or `if condition [ ... ]` without another `#`. Content blocks such as `context [ ... ]` use `#align`, `#set`, and `#if`. Follow the mode already opened by the surrounding syntax.
- **Paragraph properties:** `leading` and `first-line-indent` belong to `par`, not `text`; `spacing` also belongs to `par`. Use `#set par(leading: 0.87em, spacing: 0.84em)`, never `#text(leading: ...)`. Treat these as R4 values relative to body size, not universal constants; the built-in R4/T1 profiles and optional R1–R3 report alternatives are documented in `references/layout-rhythm.md`.
- **Page background:** Use `#set page(fill: color)` for a solid page color. Use `page(background: content)` for content layers such as watermarks, not for a bare color. Read `references/typst-patterns.md` §§1 and 10 for both patterns.
- **Links:** `link` does not accept a `fill` parameter. Apply link color through a show rule such as `#show link: set text(fill: accent)`.
- **Debugging:** When compilation fails, read the bounded diagnostic summary and reported source line before changing code. Group diagnostics by likely root cause; repair independent diagnostics from the same compile in one batch, but repair a cascade-producing syntax or import error first. Read the complete diagnostic artifact only when the summary is insufficient. Do not replace working structure speculatively. Recompile the smallest failing entry and finish with a strict build.
- **Images:** Use a `rect` placeholder while an image is unavailable. Use `figure(image(...))` for normal flowing images and an explicitly selected wrapping package for text wrap. In normal content flow, do not use absolute placement; never use `place(...)` as a substitute for flowing layout. Read `references/typst-patterns.md` §§5–6 for the full decision tree.
- **Universe packages:** Do not install packages manually. Use the exact `universe_ref` emitted by the build plan; Typst retrieves the package during initialization or compilation. Inspect the package's public API before choosing imported symbols.

## Default delivery scope

Deliver the requested PDF and only the additional artifacts the user or acceptance criteria explicitly require. Do not generate a coverage report, README, source archive, or prose visual-review notes by default. Keep diagnostic, verifier, and review-manifest artifacts in the working project unless the user requests them.

## Verification checklist

| Check | Required evidence |
|---|---|
| Build | Strict compilation exits successfully with no warnings. |
| Deterministic PDF verification | The selected `verify_pdf.py` profile reports no failures; unavailable inspection tools are recorded as `UNKNOWN`, not silently treated as pass. |
| Plan reuse | A matching `.typst-build-plan.json` is reused without reloading the ecosystem catalog. |
| Numbering | Automatic and literal heading or figure numbers are not duplicated. |
| Page flow | No unintended blank pages; referenced figures and tables remain near their discussion. |
| Cross-references | Labels resolve to the correct targets rather than placeholders. |
| Tables | Wide tables remain readable; long tables break correctly and repeat headers when required. |
| Fonts | CJK text renders without missing glyphs; font warnings are disclosed when fidelity changes. |
| Ownership | One global base owns the document, and no conflict group has multiple active owners. |
| Custom rhythm | If paragraph or section rhythm was overridden, inspect a dense body page and confirm that template- and package-owned spacing remains intact. |
| Navigation | The executed asset path, template initialization command, and package references match the selected plan exactly. |
| Visual review | Standard mode records representative and high-risk pages in the review manifest; exhaustive every-page coverage is required only after an explicit escalation trigger. |

## Bundled resources

| Resource | Responsibility |
|---|---|
| `assets/report-theme.typ` | Shared visual theme for both built-in entry paths; implements R4 report and T1 longform rhythm profiles relative to body size. |
| `assets/report-entry.typ` | Native report skeleton with metadata, title page, outline, running header, and main-body reset. |
| `assets/markdown-entry.typ` | Markdown adapter with source loading, math mapping, and table normalization. |
| `scripts/plan_document.py` | Creates or reuses `.typst-build-plan.json` from a compact content manifest. |
| `scripts/prepare_document.py` | Deterministically assembles a portable native or Markdown project. |
| `scripts/generate_pdf.py` | Compiles Typst files with bounded terminal diagnostics, complete diagnostic artifacts, strict mode, and an explicit human watch mode. |
| `scripts/verify_pdf.py` | Runs profile-based deterministic PDF checks and writes a compact JSON artifact; a PASS replaces duplicate manual checks but does not replace visual QA. |
| `scripts/render_review.py` | Deterministically renders selected pages or explicit exhaustive coverage into contact sheets and writes a compact review manifest. |
| `references/production-workflow.md` | On-demand gate model, context-hygiene rules, diagnostic escalation, standard-versus-exhaustive visual review, and default delivery scope. |
| `references/routing-catalog.json` | Machine registry for 43 packages, 30 Universe templates, and 2 built-in assets. The planner reads it during ordinary routing; read relevant entries directly only for route diagnosis, candidate explanation, or registry maintenance. |
| `references/typst-patterns.md` | On-demand syntax patterns. Read §1 for fonts/page fill, §§4–4b for tables, §§5–6 for image placement, §6b for columns, §6c for blockquotes, §7 for math/code, §9 for Universe imports, and §10 for watermarks/transparency. |
| `references/layout-rhythm.md` | R4/T1 defaults, optional R1–R3 report alternatives, relative spacing mechanics, ownership limits, edge cases, local scoping, and dense-page QA. |
