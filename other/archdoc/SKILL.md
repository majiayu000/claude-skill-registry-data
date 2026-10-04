---
name: archdoc
description: Generate docs/architecture.pdf — a concise document covering the architecture, workflow, dependencies, and operational environment, embedding the SVGs produced by the diagrams skill. Use when the user asks for an architecture document, design doc, or system overview PDF.
---

# Architecture document generator

Produce `docs/architecture.pdf`: concise (target 5-8 A4 pages), current, and
visual. The three diagrams from the `diagrams` skill are the backbone; the
prose fills in what pictures can't say. Never describe architecture from
memory — read the code first.

## Process

1. **Freshen the diagrams.** If `docs/diagrams/temporal.svg`, `infra.svg`, or
   `flow.svg` are missing — or the workflow/worker/chart files changed since
   they were generated — run the `diagrams` skill first. This document must
   embed diagrams that match the code it describes.
2. **Gather facts** from the same sources of truth the diagrams skill lists
   (workflows.py, activities.py, worker.py, shared.py, helm values,
   .env.example, Makefile), plus `requirements.txt`, `requirements-dev.txt`,
   `VERSION`, and `tests/`.
3. **Rasterize the diagrams** for embedding with cairosvg at print sharpness
   (`scale=1.4`) into the session scratchpad — not ImageMagick (it drops SVG
   features). Embed the PNGs, not the SVGs (WeasyPrint's own SVG support is
   partial).
4. **Author one self-contained HTML** in the scratchpad. Sections, in order:
   - Overview: what the system does, one paragraph + the artifact outputs.
   - Temporal architecture: embed temporal.png; prose on queues/pools/caps
     and why (per-resource quota protection), worker roles via WORKER_QUEUES.
   - Execution flow: embed flow.png; prose on ordering, parallelism,
     retry/heartbeat/resume behavior, fail-fast validations.
   - Cloud infrastructure: embed infra.png; prose on the resource group
     contents, images, public/private storage split.
   - Dependencies: Azure services table + Python packages (runtime and dev).
   - Operational environment: endpoints (Temporal frontend DNS, UI via
     admin.sh), config/secrets model (.env locally, helm secrets.yaml to
     Kubernetes Secrets, runtime listKeys, API-key gate), scaling knobs
     (replicas x per-pod caps), and the day-to-day commands (make targets,
     test.sh, admin.sh, local worker/start).
   Style: match output-template.html's look (same palette #16324f/#2a6fb0,
   Helvetica, A4 @page with page numbers). Full-width images, each with a
   short caption. Keep prose tight — bullets over paragraphs.
5. **Render** with WeasyPrint to `docs/architecture.pdf`. Include the project
   VERSION and generation date on the title header.
6. **Verify**: the file starts with `%PDF`; rasterize 2-3 pages with
   ghostscript (`gs -sDEVICE=png16m`) and visually inspect for overflowing
   text, blank/missing images, or awkward page breaks. Fix and re-render
   before finishing.
