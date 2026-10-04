---
name: build-rokkor-broadcast-sites
description: "Design, build, or refactor websites in the Rokkor Broadcast language, derived from the public-facing ROKKOR design system. Use for use the visual language of a finely made radio: a ceremonial dial, calm paper surfaces, and small moments of signal movement. Includes narrative guidance, design tokens, page structure, a responsive static starter, safe scaffolding, and publication checks. Adapt the system to the user's brand instead of cloning names, logos, copy, or proprietary content."
---

# Rokkor Broadcast Site Builder

Build sites around this thesis: **Use the visual language of a finely made radio: a ceremonial dial, calm paper surfaces, and small moments of signal movement.**

## Workflow

1. Inspect the target content, brand, framework, and deployment boundary.
2. Read [references/narrative.md](references/narrative.md) to establish the story, voice, and information sequence.
3. Read [references/design-system.md](references/design-system.md) before defining tokens or components.
4. Read [references/prompt-recipes.md](references/prompt-recipes.md) for an intake or cross-tool handoff.
5. Reuse [assets/starter](assets/starter) for a new static build; translate the token relationships into an existing healthy framework.
6. Apply [references/quality-gates.md](references/quality-gates.md) before delivery.
7. Never publish, deploy, merge, or replace an existing design without explicit authorization.

## Core decisions

- Write the central audience tension in one sentence before styling.
- Give every page a dominant action and every section a distinct reader question.
- Preserve this pack's compositional relationships while changing names, imagery, and exact palette for the user's identity.
- Use real metrics only when the user provides or verifies them.
- Mark demonstrations, mock data, proposed mechanisms, and confirmed capabilities honestly.
- Prefer semantic HTML, progressive enhancement, visible focus, reduced motion, and useful narrow-screen layouts.
- Never copy authentication flows, private dashboards, personal data, secrets, internal URLs, or source-site configuration into a public build.

## Starter

Generate a dependency-free site:

```bash
node scripts/scaffold.mjs --output ./my-site --name "Northstar" --tagline "A clear promise for a specific audience." --accent "#8e1f1f"
node scripts/audit.mjs ./my-site
```

Customize `site-data.js` first. It is the public content contract; layout code should remain stable until the narrative is correct.
