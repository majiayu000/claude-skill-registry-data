---
name: design-token-steward
description: Use when a color, spacing, radius, type, or motion value would be introduced or changed in UI — route it through the single tokens source of truth so it cascades, instead of hard-coding a one-off value in a component.
stacks: [node]
domains: [web]
phases: [dev]
tags: [ui, design-tokens, theming, design-system]
scope: kit
---
**When to use.** On any visual value change. *Why:* one-off hex/px values are how a design system rots;
tokens keep "primary" meaning one thing everywhere and make dark/light + rebrands a one-file edit.

**Procedure.**
1. Check whether a token already expresses the value; reuse it.
2. If new, add it to the tokens file with a name and provenance note (why it exists), then reference it.
3. Confirm light **and** dark render; confirm nothing else regressed that consumed the old value.
4. **Done when:** no raw color/space literal in the component diff, and the token resolves in both themes.

**Knowledge:** KNOWLEDGE-LIBRARY.md §A1 (W3C Design Tokens format, Radix Colors).
