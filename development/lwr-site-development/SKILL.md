---
name: lwr-site-development
description: "Use this skill when building or customizing sites on the Lightning Web Runtime (LWR) in Experience Cloud — including component authoring, custom theming with --dxp hooks, layout components, and publish lifecycle management. Trigger keywords: build LWR site Experience Cloud, Lightning Web Runtime custom theme, LWR component development community, Build Your Own LWR template, Microsite LWR, lightningCommunity__Theme_Layout, --dxp styling hooks. NOT for Aura-based communities (Build Your Own Aura template). NOT for standard Experience Builder drag-and-drop configuration without code."
category: lwc
salesforce-version: "Spring '26+"
well-architected-pillars:
  - Security
  - Performance
  - Operational Excellence
triggers:
  - "build LWR site Experience Cloud"
  - "Lightning Web Runtime custom theme component"
  - "LWR component development community Build Your Own"
  - "lightningCommunity__Theme_Layout target js-meta.xml"
  - "dxp styling hooks custom CSS Experience Cloud"
tags:
  - lwr
  - experience-cloud
  - lwc
  - theming
  - dxp
  - community
  - lightning-web-security
inputs:
  - "Target site template: Build Your Own (LWR) or Microsite (LWR)"
  - "Component requirements: page content, theme layout, page layout, or navigation"
  - "Branding requirements: custom colors, fonts, spacing, or design system"
  - "Auth model: authenticated vs. public/guest site"
outputs:
  - Compliant LWC component bundle with correct js-meta.xml targets for LWR
  - Custom theme layout or page layout component
  - --dxp CSS hook usage for brand-aligned theming
  - Publish lifecycle guidance and checklist
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-06
---

# LWR Site Development

Use this skill when building components, custom themes, or page/theme layouts for Experience Cloud sites powered by the Lightning Web Runtime (LWR). This covers both the Build Your Own (LWR) and Microsite (LWR) templates and addresses the unique behaviors — publish-time freeze, Lightning Web Security, and --dxp theming hooks — that distinguish LWR from Aura-based sites.

---

## Before Starting

Gather this context before working on anything in this domain:

- Confirm the site template is **Build Your Own (LWR)** or **Microsite (LWR)** — not the legacy Aura-based Build Your Own template. Aura components are completely unsupported in LWR sites.
- Confirm Digital Experiences (formerly Communities) is enabled in the org.
- Know whether the site needs authenticated access, public/guest access, or both — this affects sharing model, guest user permissions, and which `@salesforce` modules are available.
- Confirm the org is Winter '23 or later. New LWR sites are enhanced LWR sites by default (no `/s` in URL, hosted on the enhanced sites and content platform).
- Identify the component role: drag-and-drop page component, theme layout, page layout, or standalone LWC.

---

## Core Concepts

### LWR Templates Are LWC-Only

The Build Your Own (LWR) and Microsite (LWR) templates are based exclusively on the Lightning Web Components (LWC) programming model. Aura components are not supported anywhere in LWR sites — not as page components, theme layouts, or page layouts. This is a hard platform constraint, not a configuration choice.

The Build Your Own (LWR) template provides only essential pages (Home, Error, Login, Forgot Password, Register) and minimal components. Teams must build all content and layout components themselves as LWC bundles. The Microsite (LWR) template includes a responsive layout and pre-configured pages, making it suited for landing pages and event sites that require little additional customization.

### Publish-Time Freeze and Static Serving

LWR sites use a fundamentally different serving model from Aura sites. When a site is published, all JavaScript resources (components, views, framework scripts) are generated, frozen, and served as static, immutable, cacheable resources. The live site serves these frozen resources — it does not fetch current component code dynamically.

This means: **any change to a component, managed package component, custom label, or Apex method signature requires republishing the site before it takes effect.** The preview in Experience Builder always shows the latest code, but the live site does not update until republished.

Practical consequences:
- Bug fixes in LWC code are not live until the site is republished.
- Managed package upgrades are not live until the site is republished.
- Updated custom labels are not live until the site is republished.
- Apex method signature changes can break existing components on the live site if not republished promptly.
- Generated framework scripts are cached for 150 days. Static resources and content assets are cached for 1 day.

### Lightning Web Security (LWS) vs. Lightning Locker

LWR sites use Lightning Web Security (LWS) instead of Lightning Locker. LWS is stricter in some dimensions and more permissive in others:

- **Cross-namespace component imports are supported** — LWC components can import from other namespaces via composition or extension.
- **Global objects are exposed directly** — `document`, `window`, and `element` globals are no longer wrapped in secure proxies, so standard DOM APIs work as expected within a namespace.
- **Third-party library integration is easier** — analytics and charting libraries can interact with DOM elements more naturally.
- **Some DOM properties are still restricted** — `document.domain`, `document.location`, `window.location`, and `window.top` are unsupported in LWS on LWR sites.
- The org-level `Use Lightning Web Security` setting in Session Settings has **no effect** on LWR sites. LWS is always active at the site level, regardless of the org setting.

Existing components built for Aura sites or Lightning Experience may rely on Locker-specific patterns. Test them in an LWR site context before deploying.

### Component Targets and js-meta.xml Registration

Every LWC component used in an LWR site must declare its role via `targets` in its `js-meta.xml` configuration file.

| Target | Role |
|---|---|
| `lightningCommunity__Page` | Drag-and-drop component for use on site pages in Experience Builder |
| `lightningCommunity__Page_Layout` | Page layout (defines regions/slots for page content) |
| `lightningCommunity__Theme_Layout` | Theme layout (defines header, footer, and main content slot) |
| `lightningCommunity__Default` | Used alongside one of the above to expose editable properties in Experience Builder |

For a component to appear in the Components panel in Experience Builder, it must set `isExposed` to `true` and declare `lightningCommunity__Page` in `targets`.

For a component to expose editable properties, it must also declare `lightningCommunity__Default` in `targets` and define `property` elements in a `targetConfig` block. Supported property types: String, Integer, Boolean, Color, Picklist.

Theme layout components must include a default (unnamed) `<slot></slot>` element in their template to define where the main content renders. Named slots define header and footer regions.

Page layout components must declare slot names using `@slot` JSDoc annotations directly before the class declaration.

### --dxp Styling Hooks for Custom Theming

LWR sites use `--dxp` CSS custom properties (styling hooks) for theming. These are global hooks that cascade to base and custom components throughout the site. Setting a single `--dxp` hook can affect dozens of individual component properties at once.

Key hook families:
- `--dxp-g-brand` / `--dxp-g-brand-contrast` — primary brand color (buttons, links, focus states)
- `--dxp-g-root` / `--dxp-g-root-contrast` — page/section background and foreground color
- `--dxp-g-neutral`, `--dxp-g-destructive`, `--dxp-g-success` — semantic colors (configure only via head markup, not the Theme panel)
- Text hooks — heading, body, button, link, and form text styling
- Site spacing hooks — maximum content width, section padding, column and component spacing

In custom components, reference `--dxp` hooks using CSS `var()`:

```css
.my-custom-button {
    background-color: var(--dxp-g-brand);
    color: var(--dxp-g-brand-contrast);
}
```

The Theme panel in Experience Builder declaratively maps to `--dxp` hooks. When the Theme panel is updated, all components referencing those hooks update automatically. For fine-grained overrides, use `--slds-c` hooks alongside `--dxp` hooks.

The branding stylesheets (`dxp-styling-hooks.min.css`, `dxp-site-spacing-styling-hooks.min.css`, etc.) are automatically included in LWR sites created in Summer '21 or later. Older sites must add these to the Head Markup manually.

---

## Common Patterns

### Custom Theme Layout with Brand-Aligned Header and Footer

**When to use:** The team needs a consistent header and footer across all site pages, with full control over navigation, branding, and layout regions — and the default out-of-the-box theme layout does not meet design requirements.

**How it works:**
1. Create an LWC component with target `lightningCommunity__Theme_Layout` in js-meta.xml.
2. Add a default `<slot></slot>` in the template for main content. Add named slots for header and footer regions.
3. Use `@slot` JSDoc annotations before the class declaration to register region names with Experience Builder.
4. Add `data-f6-region` attributes to major layout regions for keyboard/screen reader accessibility.
5. In the component CSS, use `--dxp` hooks for all brand colors and spacing to maintain Theme panel responsiveness.
6. Register the component in a Theme Layout under Settings > Theme in Experience Builder, and assign the theme layout to site pages.

**Why not the alternative:** Hard-coding colors instead of using `--dxp` hooks breaks the Theme panel linkage. Any future brand update requires manual CSS edits across all components instead of a single Theme panel change.

### Page Component with Editable Properties for Experience Builder

**When to use:** A developer needs to build a reusable content component that non-developer site admins can configure directly in Experience Builder without code changes.

**How it works:**
1. Create the LWC component with its business logic in JavaScript and markup in HTML.
2. In js-meta.xml, set `isExposed` to `true`, declare `lightningCommunity__Page` and `lightningCommunity__Default` in `targets`.
3. Define configurable properties in a `targetConfig` for the `lightningCommunity__Default` target. Use camelCase property names (never PascalCase — it breaks coercion).
4. Declare `@api` properties in the JavaScript file matching the js-meta.xml property names.
5. For string properties that need translation in multilingual sites, set `translatable="true"` in the property definition.
6. For screen-responsive properties, set `screenResponsive="true"` and `exposedTo="css"`, then use `--dxp-c-{size}-{property-name}` CSS variables for media queries.

**Why not the alternative:** Skipping `lightningCommunity__Default` means the component appears in the panel but exposes no configurable properties. Site admins must file change requests for any content variation instead of self-serving through Experience Builder.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Need a consistent header/footer across all pages | Create a `lightningCommunity__Theme_Layout` LWC component | Theme layouts define site-wide structure; assigning one per page type is the correct LWR pattern |
| Need different layouts for different page types | Create multiple `lightningCommunity__Page_Layout` LWC components | Page layouts control the slot regions for content; assign per-page in Experience Builder |
| Need brand-responsive colors in a custom component | Use `var(--dxp-g-brand)` and related `--dxp` hooks in component CSS | Hooks cascade from the Theme panel; changing brand color once propagates everywhere |
| Need to integrate a third-party analytics library | Use the `<x-oasis-script>` privileged script tag in Head Markup | LWS allows standard DOM interaction; `<x-oasis-script>` is the supported entry point for global scripts |
| Need navigation between site pages | Import `NavigationMixin` from `lightning/navigation` using `comm__namedPage` or `standard__recordPage` | LWR templates do not support Aura navigation APIs or `standard__namedPage` — use `comm__namedPage` instead |
| Need authenticated and guest access on the same site | Use LWR sites created in Winter '23 or later (authenticated by default, supports public pages) | Pre-Winter '23 unauthenticated sites lack login/authentication support entirely |
| Site shows stale component behavior after a code fix | Republish the site | LWR sites serve frozen, publish-time resources; the live site does not pick up changes until republished |
| Need to support Aura components on the site | Migrate to LWC or use a standard Aura-based template | Aura components are completely unsupported in LWR sites; there is no compatibility layer |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Confirm site template and org context** — Verify the target site uses Build Your Own (LWR) or Microsite (LWR). Confirm Digital Experiences is enabled. Check whether the site was created in Winter '23 or later (enhanced LWR site with no `/s` URL). Identify whether guest/public access is needed (affects guest user preference settings).

2. **Plan component roles and targets** — For each component, determine its role: drag-and-drop content (`lightningCommunity__Page`), page layout (`lightningCommunity__Page_Layout`), or theme layout (`lightningCommunity__Theme_Layout`). Theme and page layout components require slot-based region definitions and `@slot` JSDoc annotations.

3. **Scaffold the LWC bundle and configure js-meta.xml** — Create the component folder with `.html`, `.js`, `.css`, and `.js-meta.xml`. Set `isExposed: true` and the correct `targets`. If the component needs editable properties, add `lightningCommunity__Default` to targets and define `property` elements in `targetConfig`. Use camelCase for all property names.

4. **Implement CSS theming with --dxp hooks** — In the component `.css` file, use `var(--dxp-g-brand)`, `var(--dxp-g-root)`, and related hooks for all brand-dependent colors and spacing. Avoid hardcoded hex values for brand colors. For screen-responsive properties, use the `--dxp-c-{size}-{property}` CSS variable pattern with standard breakpoints (l = desktop, m = tablet ≤64em, s = mobile ≤47.9375em).

5. **Register and configure in Experience Builder** — Deploy the component to the org. In Experience Builder, assign theme layout components under Settings > Theme. Assign page layout components via page settings. Drag-and-drop components appear automatically in the Components panel. Configure editable properties through the component's property panel.

6. **Validate and republish before each delivery** — After every code change, republish the site so the live static bundle includes the updated component. Verify behavior on the live site, not just the Experience Builder preview. Confirm that no Aura component references exist in the deployment. If Apex method signatures changed, republish immediately to prevent live site breakage.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] All components declare the correct `lightningCommunity__*` targets in js-meta.xml — no Aura targets or patterns used
- [ ] No Aura components referenced anywhere in the LWR site deployment
- [ ] Theme layout components include a default unnamed `<slot></slot>` and named slots for header/footer regions
- [ ] Page layout components have `@slot` JSDoc annotations before the class declaration
- [ ] All brand-dependent colors use `--dxp` CSS hooks rather than hardcoded values
- [ ] Property names in js-meta.xml use camelCase (not PascalCase)
- [ ] Navigation uses `lightning/navigation` with `comm__namedPage` — no Aura navigation API usage
- [ ] Site has been republished after all component or schema changes
- [ ] Guest user preferences are configured if any public pages exist
- [ ] LWS restrictions verified: no `document.domain`, `document.location`, `window.location`, or `window.top` usage

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Publish-time freeze catches teams off guard** — In Aura sites, component changes go live immediately. In LWR sites, the live site serves the frozen bundle from the last publish. A bug fix deployed to the org does nothing for live site users until the site is republished. Teams relying on the Experience Builder preview (which always shows current code) do not notice this until they check the live site.

2. **LWS restriction breakage is silent in preview but fails on live** — The Experience Builder preview environment may handle restricted DOM APIs differently from the live LWS enforcement context. Components that access `window.location` or `document.domain` may appear to work in development but produce runtime errors on the live site. Test LWS compliance specifically on a published site, not just in preview.

3. **Dynamic component imports must be statically analyzable** — LWR sites support dynamic LWC imports, but only statically analyzable ones. `import("c/myComponent")` works. `import("c/" + name)` or `import("c/" + componentVariable)` do not work and fail silently or throw at runtime. All dynamic import paths must be literal strings.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| LWC component bundle | `.html`, `.js`, `.css`, `.js-meta.xml` with correct `lightningCommunity__*` targets for Experience Builder registration |
| Theme layout component | LWC with `lightningCommunity__Theme_Layout` target, default slot, named header/footer slots, and `data-f6-region` attributes |
| Page layout component | LWC with `lightningCommunity__Page_Layout` target and `@slot` JSDoc annotations |
| --dxp CSS theming | Component `.css` using `var(--dxp-g-brand)` and related hooks for brand-responsive styling |
| Publish checklist | Ordered list of changes that require site republish before going live |

---

## Related Skills

- `flow-for-experience-cloud` — when flows are embedded in LWR site pages; LWR has specific compatibility requirements for screen flow components
- `navigation-and-routing` — for `lightning/navigation` usage, `comm__namedPage` vs `standard__recordPage` decisions, and URL generation best practices
