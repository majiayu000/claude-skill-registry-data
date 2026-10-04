---
name: docusaurus-docs-builder
description: Use when creating, redesigning, rewriting, or improving a Docusaurus documentation site, docs portal, developer docs, product docs, API docs, guide site, knowledge base, or documentation landing experience, especially when the user wants engaging, attractive, polished, conversion-aware, visual, MDX-powered documentation rather than plain Markdown pages.
metadata:
  last_updated: "2026-06-11"
---

# Docusaurus Docs Builder

Build Docusaurus documentation that feels like a polished product surface and still works as serious technical documentation.

## Core Behavior

When the user asks for Docusaurus docs, the agent should create a documentation experience with strong information architecture, visual proof, attractive MDX components, runnable examples, search, and verification, even if the source material is messy or text-heavy.

## First Pass

Inspect the project before writing:

1. Existing docs site: `docusaurus.config.*`, `sidebars.*`, `docs/`, `src/pages/`, `src/components/`, `src/css/custom.css`, versioned docs, blog, API references.
2. Product surface: package metadata, README, examples, screenshots, demos, changelog, CLI/API entrypoints, install paths.
3. Audience: new user, evaluator, API consumer, contributor, enterprise buyer, operator, or internal team.
4. Primary conversion: install, sign up, copy config, run command, deploy, migrate, integrate, or understand architecture.

If there is no Docusaurus site, scaffold the smallest fitting site and explain the chosen structure.

## Documentation Strategy

Default shape:

1. **Homepage**: one clear promise, one visual proof, one primary CTA, one secondary CTA.
2. **Docs landing page**: task-oriented entry points, not a file dump.
3. **Getting started**: shortest path to first success.
4. **Guides**: outcome-based workflows.
5. **Concepts**: mental models, architecture, diagrams.
6. **Reference**: APIs, config, CLI, schemas.
7. **Examples**: realistic scenarios with copy-pastable code.
8. **Troubleshooting**: symptoms, causes, fixes.

Use progressive disclosure: quick path first, deep details later.

When the task is "scaffold docs for this project" or "set up docs like spinup-ts" — for either a new project or an existing repo that lacks real docs — start from `references/project-docs-template.md`. It supplies the full directory tree, `sidebars.ts`, `docusaurus.config.ts`, and every page as a placeholder skeleton, plus an adaptation playbook. Drop it in, then change the details to match the actual project.

## Reference Router

Read only what the task needs:

| File | When to Read |
| --- | --- |
| `references/information-architecture.md` | Site maps, sidebar design, docs taxonomy, landing pages |
| `references/project-docs-template.md` | Proven, droppable docs scaffold (tree, sidebars, page skeletons) for bootstrapping a new project or revitalizing an existing repo |
| `references/visual-mdx-patterns.md` | MDX components, cards, callouts, diagrams, code blocks, before/after sections |
| `references/copy-and-conversion.md` | Headlines, CTAs, pain-point framing, page intros, anti-wall-of-text rules |
| `references/top-docs-patterns.md` | Best attributes of elite documentation sites and how to apply them |
| `references/markdown-mdx-reference.md` | Practical Markdown/MDX syntax and Docusaurus content patterns |
| `references/docusaurus-implementation.md` | Config, sidebars, theme, styling, plugins, search, build/deploy |
| `references/quality-gate.md` | Build, links, screenshots, search, mobile, accessibility, claims |
| `references/generated/manifest.json` | Generated snapshots of current official Docusaurus docs |

## Visual Documentation Rules

- No walls of text: turn dense explanations into cards, tabs, diagrams, tables, examples, and callouts.
- Every major page needs a visible job: orient, teach, persuade, reference, troubleshoot, or convert.
- Use screenshots, terminal demos, Mermaid diagrams, architecture strips, and MDX components where they make understanding faster.
- Make navigation task-based: "Install", "Configure auth", "Deploy", "Troubleshoot webhooks" beats internal implementation names.
- Put the shortest working example above deeper explanation.
- Keep visual polish consistent with the product brand, but do not sacrifice docs usability.

## Docusaurus Defaults

- Prefer TypeScript config files when the repo already uses TypeScript.
- Use Docusaurus' built-in docs plugin/theme unless a real requirement demands custom routing.
- Use MDX for custom visual sections and reusable components.
- Use sidebars for guided reading order, not just folder mirroring.
- Use admonitions for important notes, not decoration.
- Use tabs for platform/package-manager variants.
- Use Mermaid for maintainable diagrams when possible.
- Use generated static assets under `static/img/` or repo-standard docs assets.

Check current generated docs before relying on syntax for config, plugins, MDX behavior, search, or deployment.

## Generated Official Docs

Official Docusaurus docs are snapshotted into `references/generated/` by:

```bash
node scripts/update.js
```

Use these snapshots when implementation details may have changed. The generated set should include Docusaurus installation, configuration, docs plugin, sidebars, Markdown/MDX, code blocks, admonitions, assets, styling/layout, themes, search, deployment, versioning, i18n, and plugin pages.

## Completion Gate

Before saying the docs are done:

1. Run the Docusaurus build or the closest available docs build.
2. Verify key routes, sidebar entries, internal links, images, and code blocks.
3. Confirm first-run instructions are copy-pastable and match package metadata.
4. Check the first screen of the homepage/docs landing page for promise, proof, and action.
5. Report what was verified and any browser/live-render check still needed.

## Red Flags

Stop and revise if you catch:

- "I'll just convert the README into docs pages."
- "The sidebar can mirror the folder tree."
- "The homepage can be generic for now."
- "This page needs another long explanation."
- "The code block probably works."
- "The docs build is optional."
- "Pretty cards are enough even if users cannot find the answer."
