---
name: rules
description: >-
  The mandatory rules R-01 to R-38 in three groups: hard gate (absolute), purpose-gate
  (technique allowed, reason required), quality locks (consistency). Load before building UI
  that must not read as generated.
---

## Part 2: Mandatory Rules (R-01 to R-38, grouped)

All 38 rules still apply. They are grouped into three tiers so the mechanism is explicit: **Hard Gate** rules are absolute, **Purpose-Gate** rules allow the technique but require a written reason, **Quality Locks** are consistency requirements.

### Group 1: Hard Gate (absolute, no exceptions)

These rules protect honesty, function, and accessibility. Breaking any of them is a FAIL regardless of purpose.

#### R-02 — Copywriting

- **FORBIDDEN**: em dash character (`—`) in any text
- Use comma (`,`), period (`.`), colon (`:`), or parentheses `()` instead
- Text must feel natural and human
- **Scope**: the ban governs text the agent writes. A user's own writing sample is a direction, not agent copy, so a sample that uses em dashes goes through R-37's conflict protocol: name the character, name the rule, ask. Never keep or cut them silently.
- **Carve-out**: documentation of this rule is exempt: the numbered section headings in this file (`R-XX — Title` rules and `C-1` to `C-5` principles), the em dash example in Part 1, the rule's own definition, any Delivery Gate item that quotes it, and the `Em Dashes` section in the copywriting part (`references/copywriting.md`). These are documentation structure, not UI text.

#### R-03 — Mobile Responsiveness

- **REQUIRED**: mobile layout must be perfect, not an afterthought
- No horizontal overflow
- Text does not escape its container
- Cards do not collide or clip off-screen
- Navbar remains comfortable to use
- Button sizes meet the minimum tap target (44px)
- Spacing stays consistent across all breakpoints
- **Responsiveness is part of the design, not an add-on.**

#### R-17 — Data & Numbers

- **FORBIDDEN**: numbers and statistics without a real source
- If real data is not available, display no numbers at all
- Empty is better than deceptive

#### R-18 — Testimonials

- **FORBIDDEN**: AI avatars, random names, random job titles, fictional reviews
- If you have no real testimonials, do not create a testimonials section
- Use social proof that can be verified

#### R-23 — Clarification & Visual Assets

- **REQUIRED**: before creating any asset without explicit instructions, ask or use a clear placeholder
- If there is an opportunity to ask, confirm the following first:
  - App logo or icon (shape, color, concept)
  - Avatars, profile photos, or images representing people/team
  - Statistics and numbers to be displayed
  - Names, job titles, or identities in testimonials
  - Navigation structure and desired page layout
- If asking is not possible (rapid prototyping, limited context): use clear placeholders and do not disguise them as final
  - Logo: product name as text in an appropriate typeface, or the marker `[LOGO]`
  - Profile photo: initial-based avatar or a simple geometric placeholder
  - Statistics: not displayed, or marked `[REAL DATA]`
- **Never generate assets as if they are the final version without confirmation**
- If explicit instructions already exist, generate directly without asking again

#### R-24 — Navigation

- **FORBIDDEN**: placing links in the navbar for pages or sections that do not exist in the design
- Every navigation item must have a real, accessible destination
- If a feature has not been built yet, do not include it in the navbar, or clearly label it as coming soon
- The navbar must reflect the structure of content that actually exists

#### R-25 — Color Contrast

- **REQUIRED**: all text must meet the minimum WCAG AA contrast standard
  - Normal text: minimum contrast ratio of 4.5:1
  - Large text (18px+): minimum contrast ratio of 3:1
- **FORBIDDEN**: light grey text on a grey background
- **FORBIDDEN**: white text on a gradient that is light in some areas
- Always test contrast across the entire area the text passes over, not just at a single point

#### R-26 — Interactive Elements

Every interactive element must have a real behavior, or be removed:

- A link or button that scrolls to an existing section (real `href="#..."`)
- A modal or dialog that opens and closes (closable with Escape)
- A state toggle (mobile menu, theme, accordion, tabs)
- An external action (`mailto:`, a real product URL)
- A form that submits and shows feedback

**FORBIDDEN**: buttons and links that do nothing
**FORBIDDEN**: nav items pointing to sections that do not exist (see R-24)

If an element genuinely cannot have a destination yet, remove it instead of shipping a dead control. A placeholder is acceptable only with a clear `// TODO` comment in code AND a visible label to the user (e.g. "Coming soon"). See "Functional Patterns" below.

#### R-27 — UI States

- **REQUIRED**: every UI that displays data must have at least three states:
  - **Empty state**: the view when there is no data yet
  - **Loading state**: an indicator while data is being fetched
  - **Error state**: the view when something goes wrong
- A UI designed only for the ideal condition is not ready for real use
- These states are not bonuses; they are part of a complete design

#### R-28 — FAQ

- **FORBIDDEN**: FAQ containing template questions that are not specific to the product
- Every question in the FAQ must address a real concern of that product's users
- If you do not know what questions are actually asked, do not create an FAQ section
- A generic FAQ does more damage to trust than having no FAQ at all

#### R-32 — Keyboard Accessibility

- **REQUIRED**: all interactive elements must be reachable and operable by keyboard
  - `Tab` and `Shift+Tab` navigation must work logically following visual order
  - Buttons and links must be activatable with `Enter` or `Space`
  - Dialogs and modals must be closable with `Escape`
- **REQUIRED**: every focused element must have a clearly visible focus indicator
- **FORBIDDEN**: removing the focus outline with `outline: none` or `outline: 0` without replacing it with a better custom focus indicator
- A UI that can only be used with a mouse is an unfinished UI

#### R-33 — No File/CSS Patching via Scripts

- **FORBIDDEN**: implementing or altering UI features by running an external script that rewrites source files or CSS with string replacement
- Build features directly in the source code where they belong
- A feature added by a patch script (e.g. a Python script editing `.css` files) is broken by design and must be rewritten in source

#### R-34 — Every Theme You Ship Must Work

- If you ship a theme toggle, BOTH modes must be fully functional
- Contrast, colors, and every component must be verified in each mode
- **FORBIDDEN**: shipping a mode where base styles, fonts, or layout break

#### R-35 — Verify Before You Deliver

- Run or build the app before declaring the task done; a design that has never been run is not finished
- Check the console for errors after running
- Click through every interactive element, one at a time, and watch what it does: buttons, links, dropdowns, forms, tabs, modals, toggles, accordions, and navigation
- An element passes only when its action really happens: a link navigates somewhere that exists, a form submit shows validation or success, a toggle changes state, a modal opens and closes. Code that only looks interactive is a dead control (see R-26)
- If the deliverable cannot be run (a static mockup or a chat-only output), say so and verify each element by code inspection instead of claiming it was clicked
- Exercise every theme and the mobile breakpoints while clicking through
- Report the click-through as evidence with the deliverable, element by element (e.g. "Signup -> opens /signup with no console errors", "empty form -> shows validation", "mobile menu -> opens and closes"). A PASS claimed without that recorded list is not a PASS

#### R-36 — No Fabricated Claims

- **FORBIDDEN**: inventing security, compliance, or performance claims ("SOC 2 compliant", "ISO 27001", "300% faster") without real evidence
- **FORBIDDEN**: fake testimonials, fake statistics, fake names (see R-17, R-18)
- If there is no real data, show no claim

#### R-37 — Design Direction Required

- Before building a UI, load the style direction: `DESIGN.md` or explicit brand guidance from the user
- If no direction exists, ask the user, or state clearly that the design was built **without direction** and is a **draft**, not a deliverable
- If no direction exists AND the user cannot be asked, the output MUST be labeled *"draft without direction"* AND use the honest default dials **ENERGY 1 / RHYTHM 1 / MOTION 1** (see Part 3). Never silently fall back to a neutral, sterile default
- **FORBIDDEN**: designing without direction and silently falling into a neutral, sterile default
- Style direction is the product owner's identity, not a slop pattern; this filter only applies on top of it
- A design built without direction is a draft, not a shippable result

#### R-38 — Real Content or Honest Placeholder

- Every claim, feature, testimonial, statistic, nav item, or visual element must come from real information OR be an explicitly labeled placeholder
- **FORBIDDEN**: fabricating content that looks realistic (fake testimonials, invented features, fake statistics, ghost links, fictional team or people)
- Placeholders are written as what they are: `[REAL DATA]`, "Coming soon", never disguised as final (see R-23)
- An empty section is better than a fabricated one

### Group 2: Purpose-Gate (technique allowed, purpose required)

Each technique below is allowed. It FAILS only when it appears as a default without a stated purpose, or when the reason for it is not written down. Every rule has the same shape: FORBIDDEN as default without purpose; ALLOWED when it serves hierarchy/identity and the reason is written; dose caps for the excessive cases.

#### R-01 — Color & Gradients

- **FORBIDDEN as default without purpose**: blue-to-purple, blue-to-cyan, purple-to-pink gradients as primary colors, harsh or rainbow gradients, purple-and-black schemes, neon or pastel palettes, radial orbs, colored glow backgrounds, neon blue buttons
- **ALLOWED** when the color/gradient is part of an established brand identity OR serves a stated hierarchy goal, with the reason written down
- A gradient that separates one level of hierarchy from another is craft; the same gradient covering the whole page is slop. The technique is not the problem, the purpose is

#### R-04 — Icons

- **FORBIDDEN as default without purpose**: Sparkle, Star, Magic, Lightning, Diamond, Orb, Robot as feature icons
- **FORBIDDEN as default without purpose**: an icon set chosen for its recognizable library look (Lucide-style thin rounded strokes) instead of relevance to the content
- Icons must be **genuinely relevant** to the content they represent, and the relevance written down when the icon is a generic glyph
- If no appropriate icon exists, it is better to use none

#### R-06 — Typography

- **FORBIDDEN as default without purpose**: large monospace fonts used purely for "terminal" aesthetics, uppercase labels with extreme letter-spacing (`HOW IT WORKS`, `FEATURES`)
- Choose typeface based on brand character, not because it is the AI model's default pick (Inter, Geist, Space Grotesk for sans; Geist Mono, JetBrains Mono, Fira Code for mono), and write the reason
- Typography must **improve readability** and reflect the product's character

#### R-07 — Background

- **FORBIDDEN as default without purpose**: grid squares, blueprint lines, graph paper, dot patterns as a background
- Use texture or pattern only if it genuinely supports the product's specific visual identity, with the reason written down

#### R-08 — Button Arrows

- Arrows (`→`, `↗`) are not the default identity for every button
- If used, ensure the size is proportional and serves a clear visual purpose, and write that purpose down
- Not every CTA needs an arrow

#### R-09 — Badges

- **FORBIDDEN as default without purpose**: capsule badges containing "AI Powered", "Beta", "New", "Secure", "Fast" without context
- Badges may only be used if **functionally needed** (a real status or real label), with the need written down
- Avoid combining: capsule + thin border + glow + small dot + uppercase all at once

#### R-10 — Glassmorphism

- Glassmorphism is an **accent** only, not the character of the entire UI
- **Dose cap**: blur/backdrop-filter on at most 1-2 elements; **FORBIDDEN** on navbar, cards, modals, and sidebar simultaneously

#### R-12 — Shadow

- Shadow must support **visual hierarchy**, not make every element float
- Use shadow selectively as an elevation marker, not as a default for every component, and write the elevation reason down

#### R-13 — Glow

- Glow may only be used as a **focus accent** on a maximum of 1-2 important elements
- **Dose cap**: **FORBIDDEN** on card + button + badge + icon + background + border simultaneously

#### R-14 — Feature Cards

- **FORBIDDEN as default without purpose**: all cards having identical size, icon, padding, and layout
- Create visual variation that reflects content hierarchy, and write the hierarchy reason down
- Not every feature needs to be presented as a card

#### R-19 — Animations

- Animations must have a **clear UX purpose**, and the purpose written down
- **FORBIDDEN as default without purpose**: every element using Fade Up + Floating + Scale + Bounce simultaneously
- Motion must match the declared MOTION dial (Part 3): a claimed "cinematic" page must actually move; a claimed "static" page must not
- Use animation to guide attention, not just to fill the page

#### R-22 — Illustrations

- **FORBIDDEN as default without purpose**: Undraw, Storyset, or generic 3D blob character illustrations
- Illustrations must have a direct connection to the product or content, with the connection written down
- If no appropriate and original illustration exists, use real screenshots or no illustration at all

### Group 3: Quality Locks (consistency)

These are consistency requirements. They stay as-is, with two adjustments: R-05 now references the RHYTHM dial, and R-31 is upgraded to the keystone rule.

#### R-05 — Layout & Page Structure

- **FORBIDDEN**: AI template layouts (Hero + 3 cards, Hero + 6 features, Hero + fake stats, etc.)
- **FORBIDDEN**: "How It Works" always in 3 steps with round icons and numbers
- **FORBIDDEN**: bento-grid mosaic as the default section layout
- **FORBIDDEN**: a fake terminal window as the hero or feature visual
- **FORBIDDEN**: pricing always shown as three columns
- **FORBIDDEN**: generic "Trusted By" logo bar directly below the hero
- **FORBIDDEN**: 4-column template footer with Product / Company / Resources / Legal and no variation
- **FORBIDDEN**: every section using the same internal layout pattern (centered title + subtitle + identical card grid); see "Uniform Section Rhythm". Composition variety comes from `DESIGN.md`, not from a template
- Every page must have a structure built around **actual content needs**
- Section order must follow the product's narrative flow, not the AI default order (see Craftsmanship Standard C-3)
- Section composition must match the declared RHYTHM dial (Part 3): if RHYTHM is 3 (varied), sections must visibly vary; if RHYTHM is 1 (uniform), uniformity is a deliberate choice, not an accident

#### R-11 — Border Radius

- Use border radius that is **consistent with the defined design system**
- **FORBIDDEN**: making every element pill-shaped (pill buttons, pill cards, pill inputs, pill badges)
- Radius variation is a visual hierarchy tool; use it deliberately

#### R-15 — CTA (Call to Action)

- **FORBIDDEN**: "Get Started", "Learn More", "Try Now", "Explore", "Discover" as default CTAs
- CTAs must be **specific to the product context and the intended action**
- Better examples: "Start Your Free Trial", "Watch Live Demo", "Create Free Account"

#### R-16 — Copywriting & Buzzwords

- **FORBIDDEN**: "AI Powered", "Next Generation", "Revolutionary", "Seamless", "Cutting Edge", "Intelligent", "Ultimate", "Powerful", "Effortless"
- Use **specific language** that explains real benefits
- Show evidence, not claims

#### R-20 — Visual Identity

- The design must have a strong identity: a specific palette, a typeface chosen for a reason, a unique composition
- Every section must have a clear hierarchy
- Layout is built around the actual product content needs
- Identity comes from deliberate, explained choices, not from adding decoration (see Craftsmanship Standard C-1)

#### R-21 — Dark Mode

- Choose a theme based on brand identity, product type, and target users
- Developer tools, terminals, and creative tools have strong, legitimate reasons for a dark default. Use that reason, not "dark looks tech"
- If the product has no strong reason for a fixed theme, **build a working light/dark toggle**. "Give the user a choice" means build the toggle, not defer the work
- **FORBIDDEN**: using this rule (or any rule) as an excuse to skip or defer requested work. If the product should support dark mode, implement it now
- A theme toggle you ship must work correctly in BOTH modes. A dark mode that breaks the light mode is a defect (see R-34)

#### R-29 — Color Palette

- **REQUIRED**: limit the active palette to a maximum of 2-3 core colors + 1 accent color
- **FORBIDDEN**: using 5+ different colors on one page without a clear design system
- Neutral colors (white, black, grey) do not count as part of the core palette
- Palette consistency is the foundation of a strong visual identity

#### R-30 — Do Not Clone Popular Products

- **FORBIDDEN**: building a visual that overall mimics another product without being asked
  - "Make it look like Linear" (unless the user explicitly asks for it)
  - "Make it look like Vercel" (unless the user explicitly asks for it)
  - "Make it look like Stripe / Notion / Apple" (unless the user explicitly asks for it)
- AI defaults to cloning popular products because those patterns dominate training data
- Visual references may be used as inspiration, not as a template to copy
- The product must have its own visual identity, not the identity of another product

#### R-31 — Every Decision Must Have a Reason (Write It Down)

Before finishing the design, write a **one-line reason** for every major decision:
- Why this color?
- Why this layout?
- Why this typography?
- Why this spacing?
- Why use cards?
- Why use this illustration or icon?

If the reason cannot be written in one line, the decision is not valid and must be revisited. This rule is the keystone of this document: a technique is allowed only when its purpose is articulable. Writing the reason forces intent, and it is what the Purpose-Gate group (Group 2) checks.

---
