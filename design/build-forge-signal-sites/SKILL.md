---
name: build-forge-signal-sites
description: "Design, build, or refactor premium evidence-first websites in the Forge Signal visual language: cinematic dark editorial layouts, technical research archives, AI product narratives, portfolio systems, searchable findings, status boards, and directly labeled explanatory diagrams. Use when a user asks for a site similar to the CHELATED AI research archive, a high-trust AI or laboratory interface, a polished dark technical site, a research-journal UI, or a reusable Forge-style design system. Supports vanilla HTML/CSS/JS and adaptation to existing frameworks while preserving accessibility, responsive behavior, claim boundaries, and the user's brand identity."
---

# Build Forge Signal Sites

Create sites that feel like an editorial research instrument: monumental enough to carry a big idea, structured enough to audit, and restrained enough to remain credible.

## Start here

1. Inspect the target project, its instructions, existing visual language, content, and deployment path.
2. Determine whether the job is a new site, a redesign, a page addition, or a design-system extraction.
3. Read the references that match the task:
   - Read [references/narrative.md](references/narrative.md) for the creative thesis, voice, and visual rules.
   - Read [references/design-system.md](references/design-system.md) before defining tokens or components.
   - Read [references/page-blueprints.md](references/page-blueprints.md) when choosing page structure or converting source material into a narrative.
   - Read [references/prompt-recipes.md](references/prompt-recipes.md) when the user wants a portable prompt, intake brief, or handoff to another AI tool.
   - Read [references/quality-gates.md](references/quality-gates.md) before implementation and again before delivery.
4. Reuse [assets/starter](assets/starter) for a new static site. Adapt the existing project in place when a coherent framework or design system already exists.
5. Never publish, deploy, merge, or replace an existing design without explicit authorization.

## Core workflow

### 1. Build an evidence inventory

Separate source material into:

- demonstrated facts or shipped capabilities;
- bounded tests and implementation evidence;
- hypotheses and proposed mechanisms;
- blocked work, negative results, and open questions;
- narrative context that is not itself evidence.

Do not use visual polish to upgrade the certainty of a claim. If the project is not research-oriented, map these states to facts, benefits, assumptions, risks, and next actions.

### 2. Write the narrative spine

State the site's central tension in one sentence. Then order the page so a first-time visitor can answer:

1. What is this?
2. Why does it matter?
3. How does it work?
4. What is real now?
5. What remains open?
6. Where can I inspect or act?

Use one dominant idea per section. Prefer a short claim, one explanatory sentence, and a concrete proof surface over generic marketing copy.

### 3. Choose a blueprint

Select the closest blueprint from [references/page-blueprints.md](references/page-blueprints.md):

- evidence archive;
- AI product narrative;
- technical portfolio;
- lab notebook or changelog.

Combine blueprints only when every added section answers a distinct user question.

### 4. Establish the token contract

Define primitive, semantic, and component tokens before styling pages. Preserve the Forge Signal relationships rather than blindly copying colors:

- near-black depth with one restrained atmospheric field;
- high-contrast editorial display type plus technical mono labels;
- hairline borders and square-to-small radii;
- one primary signal accent and explicit evidence-state accents;
- large compositional whitespace balanced by dense audit surfaces;
- motion used as system-state feedback, never as wallpaper.

Use the full token model in [references/design-system.md](references/design-system.md).

### 5. Implement the structural shell

Build semantic landmarks, skip navigation, a clear header, main sections, and a useful footer first. Then add:

- hero and orientation;
- metrics or proof strip only when the numbers are sourced;
- lanes, capabilities, or workstreams;
- directly labeled figures for relationships that prose hides;
- milestones or process sequence;
- evidence/status board;
- searchable archive or project index when the inventory is large;
- source, repository, demo, or contact actions.

Use progressive disclosure for long details. Keep the core conclusion visible without requiring an accordion to open.

### 6. Draw explanatory figures

Use figures when a visitor must understand a transformation, control, hierarchy, or state transition. Favor a three-beat structure:

`problem or input → mechanism or comparison → result or evidence boundary`

Requirements:

- Give every figure a visible title and plain-language caption.
- Label each stage directly; do not rely on a legend alone.
- Pair color with words, line styles, or shapes.
- Distinguish tested paths, proposed paths, and stopped or unresolved paths.
- State when a diagram is explanatory rather than a measured plot.
- Use inline SVG for simple systems and real charts only for real data.
- Keep visible labels at least 11 px and supporting copy at least 13 px where layout permits.

### 7. Add interaction with restraint

Implement only interactions that improve navigation or comprehension: search, evidence filters, anchored deep links, menu disclosure, copy link, theme choice, or a meaningful system-state animation. Keep content usable without animation and respect `prefers-reduced-motion`.

### 8. Validate before handoff

Apply every relevant gate in [references/quality-gates.md](references/quality-gates.md). At minimum:

- verify content and claim lineage;
- validate the exact changed files;
- exercise the rendered site in a real browser;
- inspect desktop, tablet, and phone layouts;
- check keyboard navigation, accessible names, focus visibility, contrast, and reduced motion;
- confirm no clipping, horizontal overflow, failed assets, console errors, secrets, or private paths;
- report local preview, changed files, validation, and publication state separately.

## New static site quick start

Scaffold a dependency-free starter:

```bash
node scripts/scaffold.mjs --output ./my-site --name "Axiom Research" --tagline "Systems you can inspect." --accent "#6fe5f2"
node scripts/audit.mjs ./my-site
```

The scaffold refuses to overwrite a non-empty destination. Customize `site-data.js` before changing layout code; it is the content contract for the starter.

## Adaptation rules

- Preserve the user's identity. Change title treatment, accent relationships, symbols, photography, and language so different brands do not become clones.
- Preserve an existing framework when it is healthy. Translate tokens and component anatomy instead of replacing the stack.
- Keep visual density intentional. Hero sections breathe; evidence surfaces compress.
- Use technical ornament only when it communicates state, coordinates, lineage, sequence, or measurement.
- Avoid default AI aesthetics: gratuitous neon gradients, floating glass cards, endless rounded pills, random particles, fake command lines, and unsupported performance counters.
- Keep every external link, metric, date, paper status, and product claim traceable to user-provided or verified material.

## Delivery options

For a new project, deliver the working site and the token/content contracts. For a design-system request, deliver tokens, component anatomy, page blueprints, and a specimen page. For a prompt-only request, provide the narrative and workflow, but offer the installable skill and starter assets when file delivery is possible.
