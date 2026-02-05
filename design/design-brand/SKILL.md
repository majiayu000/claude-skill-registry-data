---
name: design-brand
description: Use this skill when creating UI components, writing copy, designing layouts, or making any visual/brand decisions for the Planted website. Ensures consistency with Planted's challenger brand voice (inspired by Oatly's approach) and the established design system.
---

# Planted Design & Brand System

This skill codifies Planted's visual identity and brand voice. Use it whenever making design decisions, writing copy, or creating new UI components.

## Brand Philosophy: The Planted Way

Planted follows a **challenger brand approach** inspired by John Schoolcraft's work at Oatly. We're not a faceless corporation with a logo - we're humans talking to humans about making food choices that are good for bodies and planet.

### Core Principles

1. **Be Human, Not a Logo**
   - Write like a person, not a brand guideline
   - Self-deprecating humor > corporate polish
   - Transparency about imperfections builds trust

2. **Consistently Inconsistent**
   - There's consistency in our inconsistency
   - Oscillate between scientific facts and playful absurdity
   - Keep people engaged with the unexpected

3. **Entertainment First, Preaching Never**
   - Make sustainability the fun choice, not the guilt choice
   - Lead with entertainment, embed the message
   - 90% funny, 10% serious (the exact ratio is classified)

4. **Show, Don't Tell**
   - Prove things through action, not claims
   - Data and transparency > marketing speak
   - If we're not good at something, say it before critics do

---

## Visual Design System

### Color Palette

```css
/* Primary Brand Colors */
--planted-purple: #61269E;      /* Trust, authority, premium feel */
--planted-purple-dark: #4A1D7A; /* Hover states, depth */
--planted-green: #8BC53F;       /* Action, growth, vitality */
--planted-cream: #FFF8F0;       /* Warmth, background, approachability */

/* Accent Colors */
--planted-pink: #FF69B4;        /* Playfulness, surprise */
--planted-orange: #FF8C42;      /* Energy, appetite appeal */

/* Neutral Colors */
--planted-charcoal: #2D2D2D;    /* Text on light backgrounds */
--planted-black: #1A1A1A;       /* Primary text */
--planted-white: #FFFFFF;       /* Cards, contrast */

/* Semantic Usage */
--planted-action: var(--planted-green);   /* CTAs, success states */
--planted-trust: var(--planted-purple);   /* Primary brand moments */
--planted-warmth: var(--planted-cream);   /* Backgrounds, approachability */
```

### Typography

**Display & Headlines:** VC Henrietta (serif)
- Hero text: `clamp(3rem, 12vw, 8rem)`, line-height: 0.88
- Page headers: `clamp(3rem, 12vw, 6rem)`, line-height: 0.92
- Section titles: `clamp(2rem, 8vw, 4rem)`
- Weight: 700, letter-spacing: -0.02em to -0.03em

**Body & UI:** Galano Grotesque (sans-serif)
- Body: 1rem, line-height: 1.6
- Small text: 0.85rem
- Micro text: 0.75rem
- Weight: 400 for body, 700 for emphasis

**Typography Rules:**
- Headlines should feel like they're breaking out of the grid
- Body copy should be readable and warm
- Mix uppercase sparingly (badges, micro-labels only)

### Spacing System (8-Point Grid)

```css
--space-xs: 0.5rem;   /* 8px - tight spacing */
--space-sm: 1rem;     /* 16px - default gap */
--space-md: 1.25rem;  /* 20px - comfortable */
--space-lg: 1.5rem;   /* 24px - section padding */
--space-xl: 2rem;     /* 32px - major sections */
--space-2xl: 3rem;    /* 48px - hero spacing */
--space-3xl: 4rem;    /* 64px - page sections */
--space-4xl: 5rem;    /* 80px - major breaks */
--space-5xl: 6rem;    /* 96px - hero areas */
```

### Border Radius

- Buttons: `100px` (pill shape)
- Cards: `1.25rem` (20px)
- Badges: `100px` (pill)
- Images in cards: Match card radius or slightly less

### Shadows

```css
/* Card shadow (subtle) */
box-shadow: 0 4px 20px rgba(0,0,0,0.06);

/* Card hover shadow */
box-shadow: 0 16px 32px rgba(0,0,0,0.1);

/* Button shadow (purple) */
box-shadow: 0 8px 24px rgba(97, 38, 158, 0.3);

/* Button hover shadow */
box-shadow: 0 12px 32px rgba(97, 38, 158, 0.4);

/* Green button shadow */
box-shadow: 0 8px 24px rgba(107, 191, 89, 0.4);
```

### Animation & Motion

```css
/* Easing curves */
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);  /* Primary - snappy, premium */
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);   /* Symmetrical transitions */
--ease-out: cubic-bezier(0.25, 0.46, 0.45, 0.94); /* Subtle deceleration */

/* Durations */
--duration-fast: 0.2s;    /* Micro-interactions */
--duration-normal: 0.3s;  /* Standard transitions */
--duration-slow: 0.5s;    /* Emphasis moments */
```

**Animation Principles:**
- Prefer `transform` and `opacity` for performance
- Hover states: `translateY(-3px to -6px)` lift effect
- Active states: `scale(0.97)` press effect
- Reveals: `translateY(24px)` to `translateY(0)` with fade

---

## Component Patterns

### Buttons

```html
<!-- Primary (purple, for main CTAs) -->
<a class="btn btn-primary">Find Products</a>

<!-- Secondary (outlined, for secondary actions) -->
<a class="btn btn-secondary">Learn More</a>

<!-- Green (for positive actions, sustainability) -->
<a class="btn btn-green">Calculate Your Impact</a>
```

**Button Behavior:**
- Hover: Lift up 3px, enhance shadow
- Active: Scale down to 97%
- Always use `100px` border-radius (pill shape)
- Minimum touch target: 44px

### Cards

**Product Cards:** Dual-state reveal (packaging to dish on hover)
**Recipe Cards:** Image zoom on hover, subtle lift
**Content Cards:** White background, rounded corners, soft shadow

### Product Card Colors

Each product has an assigned color that creates gradient backgrounds:
- `terracotta`: #E8C4B8 to #D4A894
- `yellow`: #F5E6B8 to #E8D494
- `purple`: #C4B8E8 to #A894D4
- `olive`: #C8D4B8 to #B4C494
- `burgundy`: #D4B8C4 to #C494A8
- `teal`: #B8D4D4 to #94C4C4
- `coral`: #F5D4C8 to #E8B8A4
- `navy`: #B8C4D4 to #94A8C4
- `green`: #C4E8C4 to #94D494
- `orange`: #F5D4B8 to #E8B894
- `red`: #F5C4C4 to #E8A4A4

---

## Brand Voice & Copy Guidelines

### The Planted Tone

We oscillate between two modes:

**Mode A: Scientific-Factual**
- Data-driven statements
- Specific numbers (not vague claims)
- Transparency about process
- "Our chicken contains 24g of protein per 100g"

**Mode B: Playful-Human**
- Self-aware, occasionally absurd
- Acknowledges its own marketing
- Speaks like a friend, not a brand
- "You're still reading? We're flattered."

### Copy Principles

1. **Question Everything (Including Yourself)**
   - "Is this the best plant-based chicken? We think so. But we're biased."
   - Self-deprecation disarms skepticism

2. **Make Them Complicit**
   - "You actually read the fine print? Total success."
   - Create a sense of shared secret/intelligence

3. **Be Specific, Never Vague**
   - NOT: "Made with quality ingredients"
   - YES: "Made with pea protein from farms in France"

4. **Embrace Imperfection**
   - "We're working on making this better. Here's where we're at."
   - Transparency about limitations builds more trust than claims of perfection

5. **Entertainment as Entry Point**
   - Lead with the joke, embed the message
   - Sustainability should feel exciting, not like homework

### Headlines

Headlines should feel unexpected:
- **Bold statements:** "Plants That Wanted To Be Chicken"
- **Questions:** "What If Dinner Didn't Have Drawbacks?"
- **Self-aware:** "This Is Marketing (But Also True)"
- **Conversational:** "Hi. We Make Food From Plants."

### CTAs

CTAs should be active and clear:
- "Find Planted" (not "Store Locator")
- "See All Products" (not "Browse Our Range")
- "Get Cooking" (not "View Recipes")
- "Tell Us What You Think" (not "Submit Feedback")

### Forbidden Phrases

Never use:
- "Premium quality" (show it, don't say it)
- "Delicious" (subjective, let them decide)
- "Revolutionary" (let others say it)
- "100% natural" (vague and overused)
- "For a better planet" (preachy)
- "Guilt-free" (implies guilt exists)

Instead:
- Show the quality through specifics
- Describe taste with sensory details
- Explain what makes it different
- State environmental facts with data
- Frame choices as positive, not avoiding negative

---

## Accessibility Requirements

- Touch targets: Minimum 44px
- Color contrast: Meet WCAG AA minimum
- Focus states: Visible and clear
- Motion: Respect `prefers-reduced-motion`
- Images: Always include meaningful alt text

---

## Implementation Checklist

When creating new components or pages:

- [ ] Colors match the defined palette
- [ ] Typography uses correct font families and sizes
- [ ] Spacing follows the 8-point grid
- [ ] Buttons use correct styles and behaviors
- [ ] Animations use defined easing curves
- [ ] Copy follows voice guidelines
- [ ] Accessibility requirements met
- [ ] Mobile-first responsive approach

---

## Reference Files

- `planted-astro/src/styles/global.css` - CSS variables and shared styles
- `planted-astro/src/layouts/Layout.astro` - Font declarations
- This document for brand voice and design rationale
