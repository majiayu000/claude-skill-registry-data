---
name: frontend-design-custom
description: Apply exact design standards to any UI component or page. Use when building web components, landing pages, dashboards, React components, or any UI. Triggers.
---

Colors: #FF6B35 primary, #0A0A0F background, rgba(255,255,255,0.04) surfaces
Typography: Inter, -0.02em tracking, 48-64px hero, 15-16px body
Spacing: 64px sections, 24px card padding, 16px border radius
Dark mode: Never flat black. Depth through gradients, glows, borders.

## Rules
- Functional components + hooks only
- shadcn/ui for primitives, never build from scratch
- Tailwind CSS, dark mode first
- Zustand for global state, no prop drilling
- cn() for conditional classes
- next/image for all images
