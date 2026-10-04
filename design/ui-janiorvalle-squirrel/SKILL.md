---
name: ui
description: "Use when building new UI with Tailwind: a page, a section, a component, a layout. Loads the design rules that apply and builds against them. For dark mode, responsiveness, component extraction, class cleanup, or markup from an image on existing UI, use those skills instead."
---

# UI

Build new UI that looks like a designer was in the room. The rules live in `references/`, one file per topic. Read the ones that apply before writing any UI code. Err on loading too many. A rule applies even when it's indirect: heading group rules apply to a hero, landing page rules to a single section, surface rules to a dashboard card.

## Steps

1. Look at the request, the target files, the project's conventions, and the components it already has.
2. Read every rule file below that could apply.
3. Build it with the project's framework, component patterns, assets, and Tailwind conventions. Reuse what exists.
4. Check it at mobile and desktop widths and in every interaction state.
5. Run the project's format, lint, typecheck, and tests if it has them.

Keep the human posted with one line before each phase. Not logs, just what you're doing now.

## One rule that applies everywhere

Every layout adapts from mobile to desktop. Use responsive breakpoint classes to change columns, spacing, font sizes, and visibility. `responsive-design.md` has the details.

## Rule files

- `avatars.md`. Profile photos and people images in testimonials, team sections, comments.
- `badges.md`. Badges, tags, pills, status indicators, chips, with or without icons.
- `border-radius.md`. Corner rounding on cards, containers, buttons, images, and nested elements with concentric radii.
- `buttons.md`. Primary and secondary buttons, CTAs, icon buttons, destructive actions, touch targets.
- `colors.md`. Brand and accent colors, neutral palettes, defaults to avoid.
- `copywriting.md`. Punctuation, periods, headings, taglines, subtitles, list items.
- `custom-fonts.md`. Loading fonts by link or import, registering them in `@theme`, feature and variation settings.
- `dark-mode.md`. Dark theme styling, contrast, panels, cards, shadows, headings, images, SVGs.
- `description-lists.md`. `dl`, `dt`, `dd` styling and the weight contrast between term and detail.
- `dashboards.md`. Stat grids, KPI and metric cards, admin panels, analytics views.
- `feature-lists.md`. Feature grids and any section listing several features with titles and descriptions.
- `flexbox-layout.md`. Flex containers and children, `min-w-0`, `shrink-0`, fluid versus fixed, sidebar plus content.
- `footers.md`. Page footers, footer logos and links, social icons.
- `form-controls.md`. Inputs, selects, checkboxes, radios, login and signup forms, search bars, input plus button combos.
- `general.md`. Markup rules and Tailwind authoring rules that apply to everything. Class placement, redundant display classes, `role="list"`, utility preferences, spacing, arbitrary values, variants, deprecated utilities.
- `headers.md`. Site headers, navbars, logos, mobile menus, hamburgers.
- `heading-groups.md`. The headline, subheadline, and eyebrow at the top of a marketing section. Not for articles.
- `icons.md`. SVG icons, sizing, alignment with text, filled versus stroked, inline list icons.
- `images.md`. Photos, thumbnails, screenshots, app mockups, image borders.
- `interactivity.md`. Hover states, transitions, animations, clickable versus not.
- `landing-pages.md`. Whole-page consistency for buttons, fonts, containers, radius, gaps, alignment.
- `login-pages.md`. Login, signup, and password reset pages.
- `logo-clouds.md`. Rows and grids of customer or partner logos.
- `navigation.md`. Tabs, tab bars, pill navs, sidebar navs, breadcrumbs.
- `pagination.md`. Page numbers, previous and next, what to hide on mobile.
- `placeholder-content.md`. Placeholder text, images, and data while building.
- `pricing-cards.md`. Pricing tiers, the emphasized tier, feature lists inside cards.
- `prose-content.md`. Long-form text, articles, blog posts, the `prose` classes.
- `responsive-design.md`. Breakpoints, mobile-first sizing, container queries, overflow.
- `section-layout.md`. Section padding, max widths, vertical rhythm between sections.
- `shadows.md`. When to use shadows, rings instead of borders, what to pair them with.
- `surfaces.md`. Cards, panels, wells, and the background layering between them.
- `svg.md`. Inline SVG, external SVG files, dark mode for each.
- `tables.md`. Table layout, headings, overflow, row dividers.
- `team-sections.md`. Team member grids and cards.
- `testimonials.md`. Quotes, attribution, decorative marks, grids of testimonials.
- `typography.md`. Font sizes and line heights, weights, tracking, measure.
- `font-recommendations.md`. Reference material on font pairings. Load only when the request needs it.
