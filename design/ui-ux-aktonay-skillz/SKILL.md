---
name: UI/UX Pro Max
description: Design and polish beautiful, accessible, product-ready frontend UI.
origin: Betopia
slash: /ui-ux
order: 10
---

# UI/UX Pro Max Skill

Use this skill when the user asks to build, redesign, polish, or review a frontend and the outcome should look visually strong, modern, accessible, and product-ready.

Betopia installs the full UI/UX Pro Max data pack before invoking this skill:

- Runtime path: `.betopia/skills/ui-ux-pro-max/`
- Search entry: `.betopia/skills/ui-ux-pro-max/scripts/search.py`
- Data: `.betopia/skills/ui-ux-pro-max/data/`
- Script layout: `scripts/`, `data/`, and `templates/` match upstream UI/UX Pro Max.

The data pack includes industry reasoning rules, style catalogs, color palettes, typography pairings, UX guidelines, chart guidance, icons, motion patterns, landing-page patterns, product categories, and stack-specific frontend rules. Use the data. Do not rely only on generic taste.

## When To Use

Use for:
- New landing pages, dashboards, portfolios, SaaS apps, ecommerce pages, mobile-style app screens, admin tools, and marketing pages
- Improving an existing frontend that looks plain, unfinished, generic, cramped, or visually inconsistent
- Choosing colors, typography, layout, spacing, motion, icons, component states, or responsive behavior
- Creating or updating design.md, design systems, UI tokens, or reusable component styling

## Workflow

1. Read the current UI context before changing files.
   - For existing projects, inspect the entry component, CSS, design.md, package.json, and relevant component files.
   - For new projects, infer product type, audience, density, brand tone, and primary user workflow from the request.

2. Generate a data-backed design system before implementation.
   Run the UI/UX Pro Max search script with a query containing product type, industry, audience, and style keywords:

   ```bash
   python3 .betopia/skills/ui-ux-pro-max/scripts/search.py "<product industry audience style>" --design-system -f markdown -p "<Project Name>"
   ```

   If `python3` is unavailable, use `python`. For major builds or redesigns, persist the system:

   ```bash
   python3 .betopia/skills/ui-ux-pro-max/scripts/search.py "<product industry audience style>" --design-system --persist -f markdown -p "<Project Name>" --output-dir .
   ```

   For dashboards or dense apps, use density and motion dials:

   ```bash
   python3 .betopia/skills/ui-ux-pro-max/scripts/search.py "internal analytics dashboard" --design-system -f markdown --variance 6 --motion 4 --density 8 -p "<Project Name>"
   ```

3. Supplement with targeted searches when the UI needs more precision.

   Useful domains:
   - `product`: product category patterns
   - `style`: visual styles and implementation checklists
   - `color`: semantic color palettes
   - `typography`: font pairings and Google Fonts
   - `landing`: landing-page section order and CTA strategy
   - `ux`: accessibility, mobile, loading, navigation, and interaction rules
   - `chart`: dashboard and data visualization choices
   - `icons`: icon library/import guidance
   - `gsap`: motion patterns and animation snippets
   - `react`: React performance and UI implementation pitfalls
   - `web`: semantic HTML, forms, focus, ARIA, and browser UI rules

   Example:

   ```bash
   python3 .betopia/skills/ui-ux-pro-max/scripts/search.py "SaaS analytics dashboard filters" --domain ux -n 5
   python3 .betopia/skills/ui-ux-pro-max/scripts/search.py "React responsive layout performance" --stack react -n 5
   ```

4. Define a design direction before implementation.
   Decide:
   - Product category and audience
   - Page purpose and conversion or workflow goal
   - Visual style, density, and motion level
   - Color palette with semantic roles
   - Typography pair or font strategy
   - Layout system and component hierarchy
   Base these decisions on the data-backed search output. If the output conflicts with the request, explain the tradeoff briefly and follow the user.

5. Create or update design.md when the change is substantial.
   Include:
   - Color tokens with exact hex values
   - Typography scale and font families
   - Spacing scale
   - Component visual rules for buttons, cards, inputs, nav, tables, dialogs, empty states, and feedback states
   - Responsive breakpoints
   - Motion rules and accessibility constraints
   If `--persist` generated a `design-system/` folder, read it and keep `design.md` aligned with it.

6. Implement with real UI craft.
   - Use CSS variables or Tailwind tokens consistently.
   - Build complete component states: hover, focus, active, disabled, loading, empty, error, and success where relevant.
   - Use icons where they improve scanning.
   - Use real visual hierarchy: clear primary action, readable text scale, strong grouping, aligned grids, and balanced whitespace.
   - Use responsive layout constraints so text and controls do not overlap at mobile or desktop sizes.
   - Prefer lucide-react icons when available in Betopia-created React projects.
   - For Tailwind or shadcn work, query the relevant stack/domain data before adding classes or components.

7. Match UI style to product type.
   - SaaS, CRM, dashboards, admin tools: compact, information-dense, calm, scannable, operational.
   - Landing pages and portfolios: memorable first viewport, strong media or product signal, clear CTA, social proof.
   - Consumer apps: tactile controls, warm affordances, strong empty states, mobile ergonomics.
   - Data-heavy tools: tables, filters, charts, tabs, summaries, and comparison states.

8. Avoid generic or fragile design.
   - Do not rely on one-color palettes.
   - Do not overuse purple/blue gradients, beige-only themes, dark slate-only themes, or decorative blobs.
   - Do not put cards inside cards.
   - Do not use huge hero typography inside compact tools or dashboards.
   - Do not let text overflow buttons, cards, tabs, sidebars, or mobile layouts.
   - Do not add visible instructional text explaining the UI unless the product needs it.

9. Accessibility and interaction are required.
   - Use semantic HTML and labels.
   - Maintain strong color contrast.
   - Add visible focus states.
   - Use touch-friendly hit areas.
   - Respect reduced-motion where heavy animation is used.
   - Keep keyboard navigation sane for menus, tabs, dialogs, forms, and command surfaces.

10. Verify before finishing.
   - Re-read changed React and CSS files.
   - Check for invalid JSX props, unused imports, missing variables, invalid CSS comments, nested selectors inside :root, and broken responsive rules.
   - Run the project's type/build check when available.

## Output Standard

The result should feel intentionally designed, not merely decorated. Every screen should have a clear layout system, consistent tokens, polished states, and responsive behavior.
