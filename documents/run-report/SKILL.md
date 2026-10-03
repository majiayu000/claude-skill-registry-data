---
name: run-report
description: Generate the styled HTML closeout report after a run, round, or notable package landing — what shipped, what changed visually (before/after renders), gate numbers as tables/plots, time+cost breakdown. Owner-preferred format for reviewing completed work. Delegate mechanical assembly to the grunt tier where possible; Claude writes the judgment sections.
---

# run-report

Produces a single self-contained HTML file the owner reads to understand what a
run actually accomplished. This is the owner's preferred review artifact —
"perfectly captures exactly what was completed and implemented and changed".

## When

- End of an orchestrator run / overnight session (alongside the standup).
- After a visually-significant package lands (BSDF, caustics, denoiser…).
- On request ("show me what happened").

## Content contract (sections in order)

1. **Headline** — one paragraph: what shipped, what failed, what's parked.
2. **Landed PRs** — table: PR, package, one-line change, gate numbers
   (from `gh pr list --state merged` + PR bodies; spec `Status:` lines).
3. **Visual evidence** — before/after render pairs for anything that changed
   pixels. Sources: `test_results/`, verifier PNG outputs, refbank renders.
   Embed images as base64 data URIs (self-contained file; downscale to ≤800px
   wide, skip if >2MB total). Every image gets a one-line caption saying what
   to look at. No renders changed → say so explicitly, don't pad.
4. **Gate numbers** — the measured values vs thresholds (parity max dev, SSIM,
   furnace ratios, perf ceilings). Table per package; plot only when a trend
   over ≥4 points exists (use inline SVG, no external libs).
5. **Time & cost** — wall time per phase (from ledger timestamps), delegated
   open-model token cost (from delegate transcripts), CI minutes.
6. **Parked / failed** — what didn't land and the one-line why + where it's
   tracked (spec, issue, memory).

## House style

Start from `template.html` in this skill dir (same design system as prior
reports the owner approved: light/dark aware, `--accent`/`--accent2` palette,
`.scroll` tables, `.badge` verdicts). Title = `<run date> — Astroray run
report`. Keep it one file, no external requests.

## Division of labor

- **Claude (you):** gather evidence (gh, git log, ledger, test_results),
  write sections 1 and 6 (judgment), pick which renders matter.
- **Delegate (grunt tier, optional):** mechanical HTML assembly from your
  structured notes — give it the template + a JSON/markdown outline of every
  section's content and verify the rendered result yourself before delivery.
- Deliver via `SendUserFile` (display: render). Save a copy under
  `.astroray_plan/docs/reports/<date>-<slug>.html` so reports accumulate.

## Anti-patterns

- Screenshotting numbers into prose — put measured values in tables verbatim.
- Embedding full-res renders — downscale; the report is for reading, not
  pixel-peeping (link the file path for that).
- Padding: no "risks and next steps" boilerplate the owner didn't ask for.
