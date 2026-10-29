---
name: repo-guideline-site
description: Generate or redesign a polished workflow/guidelines website from a repository, especially for CLI tools, operator workflows, and mixed technical audiences. Use when the goal is not generic API docs but a high-quality “how to use this” site with audience-aware onboarding, proof-oriented demos, a deliberate visual direction, task pages, recorded UI review gates, and an evaluation plan.
---

# Repo Guideline Site

Build a site that helps people use a tool. Give them a clear entry point, a fast first success, task-led guidance, and proof that the workflows work. Keep exhaustive reference separate from the teaching path.

## Use this skill when

The requested site teaches workflows for a repository or product, including:

- A docs, workflow, or tutorial site, such as a request to make a repo feel like worktrunk.dev
- A CLI, plugin, workflow tool, internal operator tool, or product with both technical and non-technical audiences
- A non-technical product that needs guided tasks, screenshots, and evidence of how it works
- A redesign where existing documentation is reference-heavy or generic

For pure API reference generation with no workflow teaching, use an API documentation approach instead.

## Workflow

### 1. Inventory the repository

Run `scripts/repo_site_inventory.py <repo-path>` first. Use its output as an evidence map, then inspect the highest-signal sources:

- Root README and installation instructions
- Existing documentation, website, examples, demos, and fixtures
- CLI help, configuration schemas, screenshots, GIFs, videos, and test fixtures
- Release notes or changelog entries that show what users value

When the user names a reference site, inspect its rendered pages. Record transferable patterns; do not copy its exact visual treatment.

### 2. Identify audiences and proof

Before drafting pages, determine and write down:

- Product type: `cli`, `developer-tool`, `library-with-guided-workflows`, `operator-console`, `end-user-app`, or mixed
- Main surfaces: terminal, config files, browser or mobile UI, APIs, or generated artifacts
- Audiences: new evaluator, daily operator, admin, integrator, contributor, or non-technical end user
- Strongest proof: fastest convincing demo, clearest screenshot, best before/after, or most legible task flow

Give each audience an explicit entry path. One undifferentiated path makes the site harder to use.

### 3. Write the plan bundle

Before implementing or rewriting the site, create a stable plan bundle in the target repository, usually `.codex/site-plan/` or `docs/site-plan/`. Include:

- `site-manifest.json`
- `audiences.md`
- `page-inventory.md`
- `media-plan.md`
- `build-test-plan.md`

Follow the schema and field requirements in `references/output-contract.md`. If a relevant fixture or benchmark case exists, run `scripts/evaluate_site_manifest.py --manifest <path> --case <case.json>`.

### 4. Set a visual direction

Record the following before building; do not default to generic documentation theming:

- Purpose and audience tone, such as operator-console, editorial product brief, maker manual, polished enterprise workflow, or playful household guide
- A memorable visual hook
- A product-appropriate display and body typography pairing
- An intentional color palette and atmosphere
- Composition: cards, editorial sections, asymmetry, proof panels, diagrams, or a denser operator layout
- Where motion teaches state or adds delight, and its reduced-motion fallback
- Site-specific visual anti-patterns to avoid

Use an available frontend design skill for inspiration. The portable guidance for this skill is in `references/visual-direction.md`. Record the decision in the plan bundle as `visual-direction.md` or the optional `visual_direction` block in `site-manifest.json`.

### 5. Design the information architecture

Choose a structure that reflects the user journey. A useful default includes:

- **Home / overview:** the promise, proof above the fold, a short quickstart, major workflows, and next steps
- **Getting started:** prerequisites, install, setup, and one meaningful first outcome
- **Core workflows:** 2–5 task pages based on day-to-day use
- **Advanced patterns / integrations:** scaling, automation, plugins, team workflows, or power-user recipes
- **Reference:** command, configuration, schema, or API lookups; generate these when practical
- **FAQ / troubleshooting:** objections, failure modes, environment differences, and recovery paths

Use narrative pages to teach judgment and flow. Keep exhaustive reference separate so users can find exact answers quickly.

### 6. Choose the site stack

Keep the existing docs stack when it is viable. Otherwise, choose a static site generator with suitable content tools. `Astro` or an MDX-heavy stack fits rich media and componentized callouts; `Zola` or a similarly lean generator fits small, fast CLI or Rust/Go sites. Prefer the project's established stack when it already serves the site well.

### 7. Make media testable

Treat media as product proof. Choose capture methods and validation that keep examples repeatable:

- **CLI-heavy products:** use deterministic terminal captures with VHS or an equivalent scripted recorder. Version-control tapes, stabilize output with fixtures, check command demos with text snapshots where possible, and use OCR checkpoints or frame checks for interactive and TUI demos when text snapshots are insufficient.
- **Browser or end-user products:** use browser automation for scripted screenshots or short recordings. Capture desktop and mobile onboarding states, prefer annotated stills when they explain the state better than video, and inspect rendered output after layout changes.
- **Hybrid tools:** combine terminal and UI evidence as needed.

Use `references/media-playbook.md` for detailed guidance.

### 8. Review the rendered site

After the site builds and proof media exists, inspect the rendered site. Do not treat source review as visual verification.

If the `ui-ux-pro-max` skill is available in the `design` plugin, use it as the primary rubric for guideline-site review. Apply the relevant areas: accessibility and heading hierarchy; touch targets and non-hover states; responsive layout and navigation; motion and reduced-motion handling; GIF/video fallbacks; and media dimensions and layout stability. If it is unavailable, use `references/ui-review-checklist.md`.

Record explicit rendered-site review items in `quality_gates`. Add the optional `ux_review` object to `site-manifest.json` when its findings or fixes are worth preserving.

### 9. Write for each audience

For technical audiences, lead with workflow value, make examples copyable, show expected output, and move advanced options to separate pages instead of crowding the quickstart.

For non-technical audiences, use task language, explain specialized terms in a glossary, show empty, partial, and successful states, and include relevant account, privacy, permission, and recovery guidance. Use short paragraphs and make the next action clear.

### 10. Validate the result

Before finishing, confirm each applicable quality gate:

- The site builds, and links and obvious navigation paths work
- The plan bundle passes the manifest evaluator at an acceptable score
- The homepage has at least one proof artifact
- Every P0 workflow has a page and at least one supporting artifact
- Visual changes have been checked on the rendered site
- A rendered UI review records focus and keyboard behavior, responsive layout, and motion and media fallback behavior
- The visual direction is explicit enough for another reviewer to identify drift into generic documentation design

Run the evaluator when a benchmark case or relevant fixture exists. Without one, score the manifest and report which dimensions are weak. Report any quality gate that could not be verified.

## Benchmark patterns

`references/worktrunk-patterns.md` distills the main benchmark. Carry over these principles, not its palette or layout:

- Pair a concise landing claim with immediate proof
- Use narrative pages for workflows and generated pages for reference
- Validate a deliberate media pipeline instead of capturing ad hoc screenshots
- Organize documentation around the user journey rather than code layout

## Scripts

- `scripts/repo_site_inventory.py`: scans repository evidence and classifies product surfaces
- `scripts/evaluate_site_manifest.py`: scores a plan bundle and optionally compares it with fixture expectations

## References

- `references/worktrunk-patterns.md`
- `references/visual-direction.md`
- `references/media-playbook.md`
- `references/output-contract.md`
- `references/eval-rubric.md`
- `references/ui-review-checklist.md`
