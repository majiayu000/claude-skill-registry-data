---
name: 21st.dev Magic MCP
description: Generate premium React+TS+Tailwind UI components from natural language via 21st.dev Magic MCP server
recall_keywords: [21st, magic component, generate component, ui component, component library, design system, /ui, generate ui, create component, magic mcp, svgl, brand logo]
---

# 21st.dev Magic MCP — Component Generation Skill

## What It Is

21st.dev Magic is an MCP server that generates modern, production-ready UI components from natural language descriptions. It accesses 21st.dev's curated component library and outputs React + TypeScript + Tailwind CSS code directly into your project.

## How to Invoke

Describe the component you need naturally. The MCP server tools will be available when the server is running. Common invocation patterns:

```
"Generate a hero section with animated text reveal and gradient background"
"Create a responsive navigation bar with transparent-to-solid scroll effect"
"Build a pricing card grid with hover animations"
"Design a testimonial carousel with star ratings"
```

## Available Capabilities

### Component Generation
- Hero sections, navbars, footers
- Cards, grids, pricing tables
- Forms, inputs, modals, dialogs
- Chat interfaces, AI prompt boxes
- Animated elements, loading states
- Dashboard layouts, sidebars

### SVGL Integration
- Professional brand logos as SVG components
- Consistent sizing and color options
- Search by brand name

## Best Practices for Prompting

### DO
- Be specific about layout: "3-column grid on desktop, single column on mobile"
- Mention animations: "fade in on scroll with staggered delay"
- Specify colors: "use brand primary `#C9A035` as accent, `#0D1B3E` for text"
- Reference style: "luxury aesthetic, not generic SaaS"
- Include interaction: "hover lifts card with shadow, button has magnetic effect"

### DON'T
- Don't say just "make a card" — specify what kind, what content, what style
- Don't forget responsive behavior — always mention mobile/tablet/desktop
- Don't skip accessibility — mention ARIA labels, keyboard navigation
- Don't ignore RTL — specify if Arabic/RTL support is needed

## Integration with Projects

Generated components land as `.tsx` files. To integrate:

1. Check the component's dependencies (framer-motion, gsap, etc.)
2. Place in your project's component directory (e.g., `src/components/ui/`)
3. Update imports to match your project's alias paths
4. Adjust Tailwind classes to match your design tokens
5. Add RTL support if bilingual (Arabic/English)

## When to Use 21st.dev vs Hand-Coded

| Use 21st.dev Magic | Hand-Code Instead |
|---|---|
| Standard UI components (cards, navbars, forms) | Highly custom animations with GSAP timelines |
| Quick prototyping | Components tightly coupled to app state |
| Starting point that you'll customize | Complex multi-step forms with validation logic |
| Design inspiration and patterns | Performance-critical components |
| Brand logos via SVGL | Components with heavy business logic |

## Combining with Other Skills

- **premium-web-design**: Use 21st.dev for base components, then apply premium animation patterns
- **frontend-design**: 21st.dev generates; frontend-design reviews and refines
- **impeccable**: Apply polish and micro-interactions after generation
- **tailwind-patterns**: Ensure generated Tailwind matches project design tokens

## Configuration

MCP server configured in `~/.claude/settings.json`:
```json
{
  "@21st-dev/magic": {
    "command": "npx",
    "args": ["-y", "@21st-dev/magic@latest"],
    "env": {
      "API_KEY": "${TWENTY_FIRST_DEV_API_KEY}"
    }
  }
}
```

API key stored in `~/.claude/.env` as `TWENTY_FIRST_DEV_API_KEY`. Get a key at https://21st.dev/
