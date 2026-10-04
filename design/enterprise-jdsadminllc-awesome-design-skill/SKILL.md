---
name: enterprise
description: Large-org professional with data-dense blue-gray layouts and structured hierarchy
---
# Enterprise
## Mission
Serve complex, data-rich workflows through a structured, blue-gray design system built for clarity at scale — think dashboards, data tables, and power-user interfaces.
## Brand
### 🎨 Colors
- `#F8FAFC` — Primary background (cool white)
- `#0F172A` — Primary text / dark surfaces (slate-900)
- `#3B82F6` — Primary accent (blue-500)
- `#64748B` — Secondary text / icons (slate-500)
- `#E2E8F0` — Borders (slate-200)
- `#F1F5F9` — Alternate row / subtle surface (slate-100)
### 🔤 Typography
- Heading font: Inter (Google Fonts)
- Body font: Inter (Google Fonts)
- Type scale: xs 0.75rem / sm 0.8125rem / base 0.875rem / lg 1rem / xl 1.125rem / 2xl 1.25rem / 3xl 1.5rem (compact for data density)
### 📐 Spacing
- Grid: 12-column, 1rem gap, max-width 1440px (wider for data)
- Section padding: 2rem top/bottom (compact)
- Card gap: 1rem
### 🧩 Components
- Buttons: Compact (32-36px height), 6px radius, blue primary / gray secondary / red destructive, icon+label pattern for toolbars
- Cards: White with 1px `#E2E8F0` border, 8px radius, dense internal padding (0.75rem-1rem), stat-focused layouts
- Nav: Sidebar (240px) with icon+label nav items, collapsible sections, bottom user-menu; or top bar with global search
- Hero: Minimal — page title + breadcrumb + action button row; no decorative hero images
- Footer: Utility bar — thin, single row with version, legal, support links
- Tables: Striped rows, sticky headers, sortable columns, monospace for data cells, horizontal scroll container
- Data displays: Stat cards (icon + label + number + delta), inline charts (sparklines), progress bars, status badges
### ♿ Accessibility
- All text passes 4.5:1 contrast (the blue-gray palette is inherently accessible)
- Focus rings: 2px `#3B82F6` outline with 1px offset on all interactive elements
- Keyboard navigation: full tab order, arrow-key navigation in tables and trees
- Minimum font size 0.75rem (0.8125rem recommended for table data)
- Screen-reader labels on all icons, charts, and data visualizations
### ✍️ Writing Tone
- Precise and neutral — use the language of the domain (technical, financial, operational)
- Labels: title case for page titles, sentence case for field labels, ALL CAPS for status badges
- No marketing language — state facts, metrics, and actions directly
## Do / Don't
### ✅ Do
- Design for data density — fit meaningful information above the fold
- Use consistent iconography (single icon set, same size, same stroke width)
- Provide multiple view options: table, card, list views where applicable
- Add inline actions on hover for table rows and list items
- Build clear information hierarchy: primary metric → context → detail → action
### ❌ Don't
- Use decorative elements that consume space without adding information
- Add large hero images or marketing-style sections
- Hide information behind unnecessary clicks — surface data directly
- Use more than 2 accent colors (blue primary, red for destructive/warnings)
- Add animation beyond functional transitions — no decorative motion
## Quality Gates
- All text passes 4.5:1 contrast (target 7:1 for table data)
- Full keyboard navigation verified (tab, arrows, escape, enter)
- All icons have accessible labels (aria-label or sr-only text)
- No font smaller than 0.75rem
- At least one data-dense component present (table, stat grid, or chart)
- All interactive elements have visible focus, hover, and active states