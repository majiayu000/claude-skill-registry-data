---
name: paper2poster-poster
description: Use when the user wants to turn an academic paper into a conference poster, poster outline, poster copy deck, poster layout brief, poster.yaml style draft, or Paper2Poster-ready generation package. Trigger for paper-to-poster requests involving PDF papers, arXiv links, manuscripts, PPTX posters, conference submissions, research summaries, or the Paper2Poster workflow.
---

# Paper2Poster Poster

Use this skill when the goal is to turn a paper into a readable, credible, poster-ready package instead of a long prose summary.

## Core behavior

Work from the source paper first. Prefer grounded extraction over creative rewriting.

Do not invent:

- metrics that do not appear in the paper
- figure content you have not seen
- ablation claims that are not supported
- author affiliations, funding, or venue details unless supplied

If key information is missing, say so explicitly and continue with labeled assumptions.

## Default workflow

1. Gather inputs.

Collect the paper source plus any constraints that are already available:

- `paper.pdf`, arXiv link, markdown draft, or pasted paper text
- venue, audience, poster dimensions, branding, deadline
- whether the user wants poster copy only or also Paper2Poster execution assets

If the user gave no dimensions, use the defaults in `references/poster-defaults.md`.

2. Choose the output mode.

- Draft mode: produce poster copy, layout guidance, figure recommendations, and a concise runbook.
- Execution mode: additionally prepare a `poster.yaml` draft, a Paper2Poster folder layout, and the exact command the user can run.

3. Extract poster-worthy content from the paper.

Capture:

- title and subtitle candidate
- one-sentence paper claim
- problem and motivation
- method overview
- core figures, tables, and diagrams worth featuring
- strongest quantitative results
- limitations, deployment notes, or future work if they matter

4. Compress for poster reading.

Rewrite for scanability:

- short headers
- bullets over paragraphs
- one idea per bullet
- clear result statements with units and baselines when available
- captions that can stand alone

5. Build the poster package.

Unless the user asks for a different structure, produce:

- `poster_brief.md`: audience, poster goal, assumptions, content priorities
- `poster_copy.md`: final section copy ready for layout
- `poster_layout.md`: panel plan, figure placement, hierarchy, and visual notes
- `poster_runbook.md`: exact next steps for Paper2Poster or manual assembly

If execution mode is requested, also produce `poster.yaml`.

6. Finish with a quality pass.

Check that:

- the poster has a visible narrative from problem to result
- text is shorter than the source summary would naturally be
- the main figure is obvious
- every number can be traced back to the source material
- there is a clear takeaway and contact/QR placeholder if relevant

## Paper2Poster execution guidance

When the user wants a repo-ready Paper2Poster setup, follow the upstream folder and command pattern:

- place the paper at `{dataset_dir}/{paper_name}/paper.pdf`
- place a per-poster `poster.yaml` next to `paper.pdf` if custom styling is needed
- use `python -m PosterAgent.new_pipeline` with poster path, text model, vision model, and poster dimensions

Common options to surface when relevant:

- `--poster_width_inches`
- `--poster_height_inches`
- `--conference_venue`
- `--institution_logo_path`
- `--conference_logo_path`
- `--use_google_search`
- `--max_workers`

If the environment is not ready to run Paper2Poster, still provide the exact command and clearly mark it as unexecuted.

## Output style

Prefer confident but compact deliverables.

- Keep section headers short.
- Prefer bullets to paragraphs.
- Preserve technical meaning.
- Surface assumptions at the top, not buried at the end.
- If the paper is dense, move secondary details into a small "Backup / Appendix" section suggestion rather than bloating the main poster.

## When to read references

- Read `references/inputs-and-deliverables.md` when you need a checklist for missing materials or expected outputs.
- Read `references/poster-defaults.md` when dimensions, panel count, copy density, or layout choices are unspecified.
- Read `references/example-prompts.md` when the user wants a ready-to-paste invocation for Codex or Claude.
