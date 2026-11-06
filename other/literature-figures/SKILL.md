---
name: literature-figures
description: Generate English static scientific figures from existing literature data, including curved networks, cluster timelines, and citation bursts.
---

# Scientific Literature Figures

Read [shared contract](../../references/shared-contract.md). Use standard plotting tools; do not use image generation for data-driven scientific charts.

Select the data-specific renderer:
- Curated library.json + networks.json: plot_scientific.py.
- Zotero screening outputs: refine_maps.py for curved maps.
- WoS outputs: wos_figures.py for co-citation, burst bars and cluster timelines.

Pass --output ANALYSIS_DIRECTORY. All renderers emit PNG/SVG/PDF. Do not rebuild data merely to change curves, typography or palette. Disclose display edge filtering separately from the full analysis graph. Preserve isolated components, node/edge semantics and the input provenance.

For style requests, prefer natural layouts, restrained curved links, transparent cluster envelopes and collision-aware labels. Rings, red outlines and time colors must correspond to computed quantities with explicit legends. Never add plausible-looking connections. Visually inspect all delivered figures; apply actual journal specifications when supplied.
