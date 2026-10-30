---
name: patterns
description: >-
  AI slop patterns to audit for — colour, layout, components, copy, decoration,
  functionality, identity, accessibility. Load when reviewing generated UI for the usual
  tells.
---

## Part 1: AI Slop Patterns (Warning Signs)

These are the most common patterns found in AI-generated designs. Use this table to **audit** your output: scan for clusters, then ask each one "what does this serve?" A single pattern from this list is fine if it serves a purpose, unless a **Hard Gate** rule in Part 2 forbids it (R-02, R-03, R-17, R-18, R-23 to R-28, R-32 to R-38). What makes a design slop is many of these appearing together with no reason. This is a **diagnostic scan, not a ban list**: Part 1 itself bans nothing, but the Hard Gate rules in Part 2 are absolute, and every other pattern must pass the purpose test (Part 2, Purpose-Gate group).

### Visual & Color

| Pattern | Telltale Signs |
|---------|---------------|
| **Generic Blue-Purple Gradient** | Blue to Purple, Blue to Cyan, Purple to Pink, full-page colored glow background |
| **Excessive Glassmorphism** | Blur on navbar, cards, modals, sidebar all at once |
| **Excessive Border Radius** | Every element is pill-shaped: buttons, inputs, cards, badges, modals |
| **Overly Soft Shadows** | Every component has a large shadow, the whole page feels like it's floating |
| **Glow Everywhere** | Glow on cards, buttons, icons, badges, backgrounds, and borders all at once |
| **AI Default Palette** | Harsh or rainbow gradients, purple-and-black schemes, neon accents, pastel blocks, radial orbs, used as the default color treatment |
| **Background Grid** | Grid squares, blueprint lines, graph paper, dot grids, thin horizontal/vertical lines |
| **Too Much Decoration / Trend-Stacking** | Blob, mesh gradient, glow, noise, pattern, grid with no purpose, especially when multiple trends are stacked (e.g. Glassmorphism + Mesh Gradient + Glow + Monospace + Grid + Rounded UI) |
| **Dark Mode Default for No Reason** | Entire page is dark just because it looks "tech", with no branding consideration |
| **Too Many Colors in Palette** | Using 5-7 different colors on one page without a clear design system |
| **Excessive Accent Color** | One accent color on buttons, icons, badges, links, lines, backgrounds, and glows |
| **Sterile Default** | Flat white/near-white, thin grey borders, small radius, no texture, generic font, no identity. The "safe result" of over-filtering without direction |
| **Skeleton Preview as Product Shot** | Grey placeholder bars / skeleton blocks used as the "product screenshot" in the hero or feature areas |

### Layout & Components

| Pattern | Telltale Signs |
|---------|---------------|
| **Monotonous Layout** | Hero, Subtitle, 2 CTAs, Screenshot, Feature Grid, Testimonials, FAQ, CTA, Footer |
| **Copy-Paste Feature Cards** | Identical size, height, icon, layout, and padding across all cards |
| **Bento Grid** | A mosaic of differently-sized cards filling a section, the default "app-like" layout |
| **Fake Terminal Window** | A styled terminal window with typed-out commands as the hero or feature visual |
| **Uniform Spacing** | Padding, margin, and element gaps are identical across every section |
| **Broken Mobile** | Horizontal overflow, cards clipping off-screen, broken navbar, colliding text |
| **Template Animations** | Every element uses Fade Up, Fade In, Floating, Scale, Bounce |
| **"How It Works" Always 3 Steps** | Round icon + number 1, 2, 3 + short text, always three steps, always the same |
| **"Trusted By" Logo Bar** | Row of generic company logos placed directly below the hero |
| **"Most Popular" Pricing Card** | Middle tier always highlighted with a capsule badge |
| **3 Pricing Tiers** | Always three columns whatever the real pricing structure, with the middle tier highlighted |
| **4-Column Template Footer** | Product / Company / Resources / Legal columns with no variation |
| **Uniform Section Rhythm** | Every section is the same composition: centered title + subtitle + identical card grid, with no variation between sections |
| **Alternating Background Only** | The only variation between sections is flipping the background color every other section |

### Copywriting & Content

| Pattern | Telltale Signs |
|---------|---------------|
| **Em Dash (—)** | "Fast, secure — and built for developers." |
| **Generic CTAs** | Get Started, Learn More, Try Now, Explore, Discover |
| **AI Marketing Buzzwords** | AI Powered, Revolutionary, Next Generation, Seamless, Cutting Edge |
| **Fake Statistics** | 10K+ Users, 99.9% Uptime, 500M Requests, 120+ Countries |
| **Fake Testimonials** | AI avatars, random names, random job titles, fictional reviews |
| **Fabricated Trust Claims** | "SOC 2 compliant", "ISO 27001", "Enterprise-grade security", "300% faster" for a product with no such evidence |
| **Demo Without a Product** | Sells a product that is never shown working: no real demo, no Terms of Service, no Privacy Policy |

### Decorative Elements

| Pattern | Telltale Signs |
|---------|---------------|
| **Generic AI Icons** | Sparkle, Star, Magic, Lightning, Diamond, Cube, Robot, AI Orb |
| **Lucide Icons** | Every icon from the same thin-stroke rounded library (Lucide or a clone), the default icon-set look |
| **Colored Left Stripe** | A thin colored vertical bar on the left edge of cards, rows, or section headers, as decoration |
| **Small Arrows (→ / ↗)** | Placed on almost every button as pure decoration |
| **AI Capsule Badges** | Pill shape, thin border, glow, small dot, uppercase, containing: "AI Powered", "Beta", "New" |
| **Generic AI Typography** | Large monospace headings, HOW IT WORKS uppercase with wide tracking |
| **Typeface Chosen Without Reason** | Font picked because it's the AI default, not because it fits brand character. Popular fonts like Inter are still valid if there's a reason |
| **Generic Illustrations** | Undraw, Storyset, or 3D blob characters with no real connection to the product |

### Functionality & Content

| Pattern | Telltale Signs |
|---------|---------------|
| **Non-Functional Interactive Elements** | Buttons do nothing, dropdowns won't open, forms can't be submitted. AI builds the visuals but forgets the logic |
| **Happy Path Only Design** | No empty state, loading state, or error state. UI looks perfect in screenshots but isn't ready for real use |
| **Irrelevant FAQ** | FAQ contains generic template questions ("Is my data secure?", "Can I cancel anytime?") with no real relevance to the product |
| **Assumed Logo & Profile Photos** | Creating app logos, avatars, or profile photos without explicit instructions, generated purely on assumption |
| **Navbar Links to Nowhere** | Navbar contains links to pages (Features, Contact, About, etc.) that have no actual section or page |
| **File/CSS Patching via Script** | A feature (e.g. dark mode) added by an external script that rewrites source or CSS with string replacement. Signs: a `.py`/`.js` helper doing `str.replace` on `.css` files, "patch" scripts left in the repo |

### Identity & Originality

| Pattern | Telltale Signs |
|---------|---------------|
| **No Visual Identity** | Swap the logo and the design still feels the same; could belong to any product |
| **Clone of Popular Products** | Overall visual that mimics Linear, Vercel, Stripe, Notion, or other popular products without being asked |

### Accessibility

| Pattern | Telltale Signs |
|---------|---------------|
| **Poor Color Contrast** | Grey text on grey background, white text on a gradient that's light in some areas. Looks fine visually but fails WCAG |
| **Not Keyboard Navigable** | UI can only be used with a mouse. Interactive elements can't be reached with Tab, no visible focus state |

---
