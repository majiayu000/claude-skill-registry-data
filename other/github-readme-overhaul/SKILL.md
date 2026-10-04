---
name: github-readme-overhaul
description: Use when writing, rewriting, branding, visually overhauling, or optimizing a GitHub README.md for installs, downloads, stars, marketplace conversion, OSS adoption, or immediate product value, including badges, hero graphics, tagline, pain-point messaging, quickstart, terminal demos, screenshots, GIFs/videos, and README-native visual assets.
metadata:
  last_updated: "2026-05-26"
---

# GitHub README Overhaul

Turn a README into a GitHub-native conversion surface: visitors should understand the pain, see the fix, trust the proof, and know how to install within the first screen.

## Core Behavior

When the user asks for a compelling README, the agent should rewrite the README as a branded mini case study with clear install intent, infographic-level visual proof, and tight copy, even if the user says "landing page," "viral," or "pull out all the stops." Borrow landing-page strategy, but do not create a fake website inside Markdown or walls of text.

## Required Inputs

Inspect the repo before writing:

1. Existing `README.md`, package metadata, manifests, screenshots, docs, examples, CI, releases, and install paths.
2. Product category: CLI, library, app, extension, agent skill, MCP server, GitHub Action, plugin, template, SaaS, or internal tool.
3. Real proof: terminal demo video/GIF, screenshot, terminal output, benchmark, before/after, testimonials, stars/downloads, examples, supported platforms.
4. Install path: one command, marketplace link, package manager, Docker, browser extension store, VS Code Marketplace, Claude plugin install, GitHub template, or hosted URL.

If proof is missing, create a placeholder task or asset brief, but do not invent metrics.

## Above-the-Fold Formula

Use this order unless the repo strongly suggests a better one:

1. Logo or compact wordmark if available.
2. H1 with product name.
3. Tagline that names the painful job and the promised outcome.
4. Badge row with only meaningful, maintained badges.
5. Hero proof: terminal demo, screenshot, terminal panel, flow diagram, benchmark chart, or before/after graphic.
6. One-line install or primary CTA.
7. Three concrete value bullets.

The first screen should answer: "What is this, why do I care, can I trust it, and how do I try it?"

## Reference Router

Read only what the task needs:

| File | When to Read |
| --- | --- |
| `references/strategy.md` | README narrative, conversion structure, viral/adoption mechanics |
| `references/badges.md` | Badge selection, ordering, sources, and anti-spam rules |
| `references/visual-system.md` | Hero graphics, screenshots, diagrams, GitHub rendering constraints |
| `references/infographics.md` | Compelling README infographics, proof graphics, and visual density rules |
| `references/terminal-demo.md` | Terminal demo video/GIF planning, recording, scripting, export, and embedding |
| `references/copy-patterns.md` | Taglines, pain-point framing, CTAs, section copy patterns |
| `references/quality-gate.md` | Final review checklist and failure modes |

## README Structure

Default section order:

```markdown
<brand/logo>

# Product Name

> Pain-point tagline with outcome.

<badge row>

<hero proof visual>

<install command or marketplace CTA>

## Why this exists
## See it work
## Install
## Quick start
## What you get
## Examples
## How it works
## Configuration
## Comparisons / tradeoffs
## Roadmap
## Contributing
## License
```

Collapse or reorder sections when the product needs a simpler path. For libraries, quickstart moves higher. For visual tools, screenshots move higher. For developer tools, terminal proof moves higher.

## Visual Rules

- Design for GitHub Markdown rendering, dark/light mode, mobile width, and skim reading.
- Prefer a sequence of strong proof visuals over long explanatory sections.
- Use actual product UI, terminal output, diagrams, or screenshots when possible.
- For CLI/dev tools, strongly consider a short terminal demo as the hero proof.
- For complex developer tools, use infographic blocks like before/after, architecture, savings, workflow, and supported surfaces.
- Store assets under `assets/readme/` or the repo's existing docs asset folder.
- Use Mermaid for maintainable diagrams when it fits.
- Use SVG/PNG only when visual polish matters or Mermaid is too limited.
- For generated visuals, prompt for "GitHub README documentation graphic, not a website."

Do not add nav bars, pricing cards, fake CTA buttons, huge landing-page sections, or marketing graphics that do not explain the product.

## Copy Density Rules

- Replace paragraphs with labeled visuals, short callouts, tables, and examples.
- Keep each section to one job: pain, proof, install, example, or detail.
- Lead sections with the sharpest claim, then prove it visually.
- Prefer one memorable sentence over three explanatory paragraphs.
- If a README already looks visually strong, improve wording, ordering, and proof clarity without flattening the visual system.

## Badge Rules

Use badges as trust signals, not decoration. Prefer:

- package version/downloads
- CI/build
- test coverage only if true and maintained
- license
- marketplace/version/install count
- docs
- supported runtime/platform
- security/audit status when real

Avoid badge soup. Five to eight strong badges usually beat twenty weak ones.

## Viral / Adoption Mechanics

Optimize for immediate value, not begging people to share:

- Show the pain in the first sentence.
- Show proof before abstractions.
- Make install copy-pastable.
- Include a "see it work" example near the top.
- Give users a reason to star through utility: roadmap, examples, templates, updates, or reference value.
- Make screenshots and terminal snippets visually memorable.
- Use a short terminal demo to show time-to-value when the tool is command-driven.
- Make the README easy to quote by using sharp, specific phrasing.

Do not ask readers to share. Do not manufacture hype. Do not exaggerate capabilities.

## Completion Gate

Before saying the README is done:

1. Verify every install command, badge URL, image path, and internal link that can be checked locally.
2. Confirm no invented metrics, fake screenshots, or unsupported claims were added.
3. Check GitHub Markdown constraints: image sizes, table readability, dark/light compatibility, no broken relative paths.
4. Ensure the first screen contains pain, product, proof, and install path.
5. Report what was verified and what still needs a live GitHub render or asset generation pass.

## Red Flags

Stop and revise if you catch:

- "This would look great as a website."
- "We can add badges for everything."
- "No proof exists, so I'll imply traction."
- "The install command is probably right."
- "The hero graphic is pretty but does not explain anything."
- "The README asks for stars or shares before showing value."
- "This section is becoming a wall of text."
- "The visuals are strong, so the copy can stay vague."
