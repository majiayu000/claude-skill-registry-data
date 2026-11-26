---
name: design-workflows
description: Design and refine interfaces, motion, brand systems, and sourced brand assets using Kernel’s recorded design conventions.
license: MIT
---

# Design Workflows

Select the procedure matching the user's task from the index below. Read only that procedure and any resources it explicitly needs. Resource paths in a procedure are relative to that procedure's folder; run bundled scripts from that folder when its commands assume a working directory.

Follow the user's current instructions and the target repository's conventions before Kernel defaults. Treat examples, framework choices, and project adapters as conditional guidance. Match validation to the actual change. Existing authorization persists; ask only when a required decision or permission is missing. Loading a procedure does not authorize publishing, deployment, or other external changes.

- [Kernel Design](references/kernel-design/WORKFLOW.md) — use when designing, changing or reviewing UI in a project: brand and token decisions, accessibility, redesigns, Figma sync, and Charles's recorded style rules.
- [Kernel Animate](references/kernel-animate/WORKFLOW.md) — use when building, reviewing or auditing animation code, or naming a motion effect.
- [Brand Asset Sourcing](references/brand-asset-sourcing/WORKFLOW.md) — use when a project needs logos or icons for brands named in its data, with a source manifest.
- [Web Designs](references/web-designs/WORKFLOW.md) — use when a page should borrow a known site's visual language; supplies 54 real design systems as CSS values.
- [Tailwind CDN Static Page](references/tailwind-cdn-static-page/WORKFLOW.md) — use for the mechanics of a no-build, single-file page: Tailwind Play CDN, import maps, local checks.

Single-file HTML pages: the `claude-design` skill drives the design process; Web Designs supplies a brand's look; Tailwind CDN Static Page covers only CDN mechanics and defers to `claude-design` for process; Kernel Design applies when the page belongs to a project with a shared design system.
