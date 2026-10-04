---
name: scbe-demo-lab-builder
description: Build public-facing demos, research surfaces, and monetized launch pages for SCBE using Figma concepts, frontend implementation, browser validation, deployment, and research-output packaging. Use when turning a product idea, benchmark, experiment, or internal tool into a public demo hub, interactive lab, landing page, benchmark board, or research domain.
---

# SCBE Demo Lab Builder

Build public-facing demos, research surfaces, and monetized launch pages for SCBE.

## Workflow

1. Classify the demo objective.
- `live-demo`: runnable surface such as the arena, flux lab, telescope, or context board
- `research-surface`: benchmark board, math explainer, or confirmed-results page
- `launch-surface`: homepage, feature page, or offer page with a clear CTA

2. Select the minimal stack.
- Design: use installed `figma` or the Figma connector for concept frames; use `figma-implement-design` when turning a chosen design into implementation guidance.
- Build: use `frontend-skill` for general UI scaffolding; use `living-codex-browser-builder` when the demo behaves like an AI-native tool or sidepanel surface.
- Validate: use `playwright` for smoke flows, links, and CTA checks.
- Publish: use `vercel-deploy` for standalone demo apps; use repo-hosted static pages when GitHub Pages is the target.
- Monetize: use `scbe-monetization-thought-to-cash` to keep one core offer, one upsell, and one KPI path.
- Archive outputs: use `notion-research-documentation` or repo docs to separate confirmed outputs from active experiments.

3. Build the demo as packets.
- Packet A: choose the audience, one pain point, one proof surface, and one CTA.
- Packet B: produce a Figma concept, banner, or diagram.
- Packet C: implement the smallest public surface that carries the idea.
- Packet D: validate navigation, forms, links, and copy.
- Packet E: connect pricing, offer, or benchmark download.
- Packet F: publish or stage in `demos/` and `research/`.

4. Keep the domain structure clean.
- Put launchable surfaces in `demos/`.
- Put benchmark summaries, math explainers, and evidence pages in `research/`.
- Keep confirmed results separate from exploratory claims.
- Prefer static hosting if the page does not need a backend.

5. Output contract.
- demo brief
- selected skill stack
- page or route map
- monetization path
- validation checklist
- publish handoff

## Multi-agent use

- Use `multi-agent-orchestrator` only when design, implementation, validation, or documentation can run as independent packets.
- Keep one owner per mutable surface.
- Reserve shared files for an integration packet.

## Guardrails

- Do not invent benchmark claims or proof language for synthetic experiments.
- Do not create server-dependent demos when a static page and outbound links are enough.
- Do not bury pricing or CTA logic; make the money path explicit.
- Do not overload the landing page; branch deeper material into nested routes.

## Resources

- Read `references/demo-stack-and-packets.md` for stack recipes and packet patterns.
