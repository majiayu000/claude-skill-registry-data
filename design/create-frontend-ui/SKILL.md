---
name: create-frontend-ui
description: Build distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, dashboards, React components, HTML/CSS layouts, or styling/beautifying any web UI. Avoids generic AI aesthetics. Uses shadcn UI MCP for components.
---

<objective>
Guide creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

This skill activates the designer mindset: analyze context, commit to a bold aesthetic direction, then execute with precision. The output should be memorable and feel genuinely designed for the specific context.
</objective>

<essential_principles>

<design_thinking>
**Before coding, analyze and commit:**

1. **Purpose**: What problem does this interface solve? Who uses it?
2. **Tone**: Pick an extreme direction:
   - Brutally minimal, maximalist chaos, retro-futuristic
   - Organic/natural, luxury/refined, playful/toy-like
   - Editorial/magazine, brutalist/raw, art deco/geometric
   - Soft/pastel, industrial/utilitarian
3. **Constraints**: Framework, performance requirements, accessibility needs
4. **Differentiation**: What makes this UNFORGETTABLE? The one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work—the key is intentionality, not intensity.
</design_thinking>

<anti_slop_checklist>
**NEVER use these generic AI aesthetics:**

**Typography (always avoid):**
- Inter, Roboto, Arial, system-ui, sans-serif defaults
- Any font that "just works" without character

**Color (always avoid):**
- Purple/violet gradients on white backgrounds
- Evenly-distributed, timid palettes without hierarchy
- Generic blue (#0066CC) as primary without justification

**Layout (always avoid):**
- Predictable card grids with equal spacing
- Cookie-cutter hero sections
- Standard sidebar + content patterns without variation

**Ask yourself**: Would a designer cringe at this? If yes, rethink it.
</anti_slop_checklist>

<shadcn_integration>
**Before building custom components, check shadcn UI MCP:**

```
1. Search for relevant components:
   mcp__shadcn__search_items_in_registries(registries: ["@shadcn"], query: "button")

2. View component details:
   mcp__shadcn__view_items_in_registries(items: ["@shadcn/button"])

3. Get usage examples:
   mcp__shadcn__get_item_examples_from_registries(registries: ["@shadcn"], query: "button-demo")

4. Get install command:
   mcp__shadcn__get_add_command_for_items(items: ["@shadcn/button"])
```

Use shadcn components as a foundation, then STYLE them distinctively. The component logic is reusable; the aesthetics must be unique.
</shadcn_integration>

<implementation_complexity>
**Match code complexity to aesthetic vision:**

- **Maximalist designs**: Elaborate code, extensive animations, layered effects, custom cursors, grain overlays
- **Minimalist designs**: Restraint and precision—careful spacing, refined typography, subtle transitions
- **The rule**: Elegance comes from executing the vision well, not from complexity alone
</implementation_complexity>

</essential_principles>

<quick_start>
**Immediate workflow for any frontend build:**

1. **Analyze** the request—what's the purpose and audience?
2. **Commit** to a bold aesthetic direction (don't hedge)
3. **Check shadcn** for reusable components
4. **Load references** for the chosen aesthetic
5. **Implement** with distinctive typography, color, motion, and composition
6. **Verify** against the anti-slop checklist

**For aesthetic inspiration and code samples:**
Read [references/aesthetics-gallery.md](references/aesthetics-gallery.md)

**For typography choices:**
Read [references/typography-guide.md](references/typography-guide.md)

**For color, motion, and composition:**
Read [references/design-system.md](references/design-system.md)
</quick_start>

<routing>
**Load references based on task:**

| Task | References to Load |
|------|-------------------|
| Building any UI | aesthetics-gallery.md + design-system.md |
| Font selection questions | typography-guide.md |
| Animation/motion work | design-system.md (motion section) |
| Color palette creation | design-system.md (color section) |
| React/Svelte/RN/Tailwind | framework-patterns.md |
| Full page/app build | All four references |

**After reading references, implement with the aesthetic direction committed.**
</routing>

<reference_index>
All domain knowledge in `references/`:

**Aesthetic Examples:** aesthetics-gallery.md (extensive code samples for each direction)
**Typography:** typography-guide.md (font pairings, anti-patterns)
**Design System:** design-system.md (color, motion, composition, visual details, UX guidelines)
**Framework Patterns:** framework-patterns.md (React, Svelte, React Native, Tailwind best practices)
</reference_index>

<success_criteria>
A successful frontend implementation:

- [ ] Has a clear, committed aesthetic direction (not hedged or safe)
- [ ] Uses distinctive typography (NOT Inter, Roboto, Arial, or system fonts)
- [ ] Has intentional color hierarchy (dominant + sharp accents)
- [ ] Includes purposeful motion (staggered reveals, hover states that surprise)
- [ ] Passes the anti-slop checklist (no generic patterns)
- [ ] Is production-grade and functional
- [ ] Would make a designer say "this was designed, not generated"

**CRITICAL**: No two outputs should look the same. Vary themes, fonts, and aesthetics across generations.
</success_criteria>
