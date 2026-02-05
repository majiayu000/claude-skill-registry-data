---
name: creating-landing-pages
description: Use when building marketing landing pages or SaaS homepages - provides a systematic workflow for hero-first design, animation patterns, social proof, and section expansion that creates consistent, professional results
---

# Creating Landing Pages

## Overview

Build landing pages hero-first. The hero section sets colors, typography, and spacing that AI uses consistently for the rest of the site. Spend 50% of effort here.

## When to Use

- Building a new marketing site or SaaS landing page
- Redesigning an existing homepage
- Creating product launch pages
- Need consistent design across multiple sections

## Workflow

### 1. Hero Section (50% of time)

Start with a reference-based prompt:

```
Create the hero section for my {app_type} called {name} in the style of {reference_site}.

Include:
- Nav bar with logo and links
- Eyebrow text (small label above headline)
- Headline and subheadline
- Primary and secondary CTA buttons
- Social proof element
- Hero visual/illustration
```

**Pro tip:** Include a screenshot of the reference site for significantly better results.

### 2. Icons

Use Iconify with a specific icon set:

```
Use Iconify {icon_set_name} for all icons.
```

| Icon Set | Style | Best For |
|----------|-------|----------|
| Lucide | Clean, minimal | General use |
| Solar | Modern, bold | SaaS products |
| HeroIcons | Outlined/solid | Professional apps |
| Iconoir | Thin, elegant | Design tools |
| Phosphor | Versatile weights | Flexible needs |

### 3. Animations

**Entry animations** (add to hero and each section):

```
Animate fade in, slide in, blur in, element by element.
Use 'both' instead of 'forwards'.
Don't use opacity 0.
```

**Why these specifics:**
- `animation-fill-mode: both` - Applies styles before AND after animation
- Avoiding `opacity: 0` - Prevents flash of invisible content
- Element-by-element - Creates professional staggered reveal

**Advanced animations:**

```
Add beam animation connecting {element_a} to {element_b}.
Add subtle sonar pulse effect on the {element}.
Add gradient border that animates on hover.
```

### 4. Social Proof

Place in hero or immediately below:

```
Add social proof with {star_rating} and {review_count}.
Include logo marquee with {company_logos}.
Animate the logos with marquee animation looping infinitely
using duplicated items and alpha mask.
```

### 5. CTAs and Buttons

Default buttons are basic. Stand out with:

```
Change main button to {paste_code_from_uiverse_or_codepen}.
Add a 1px border beam animation around the pill-shaped
main button on hover.
```

**Resources for unique buttons:**
- [UIVerse](https://uiverse.io) - Copy-paste button components
- [CodePen](https://codepen.io) - Search "button animation"

### 6. Background Effects

For animated backgrounds, use [Unicorn Studio](https://unicornstudio.ai):
1. Remix an existing template
2. Export and embed
3. Layer behind hero content

### 7. Section Expansion

Once hero is complete, add sections by referencing the existing design:

```
Adapt a new {section_type} section. Match the existing
color scheme, typography, and spacing. Change texts,
names and numbers to fit {your_content}.
```

**Common section types:**
- Features (grid or alternating)
- How it works / Action plan
- Pricing table
- Testimonials
- FAQ accordion
- Final CTA
- Footer

**Pro tip:** Insert a screenshot of your current hero when prompting for new sections.

### 8. Human Touch

AI creates structure. You refine:
- Headlines - Use ChatGPT to brainstorm alternatives
- Feature copy - Make benefits specific, not generic
- CTAs - Test different action verbs
- Images - Use Midjourney + Nano Banana Pro for custom visuals

## Quick Reference Prompts

| Task | Prompt |
|------|--------|
| Hero | `Create hero section for {app} in style of {reference}` |
| Icons | `Use Iconify {Solar/Lucide/Phosphor}` |
| Entry animation | `Animate fade in, slide in, blur in, element by element. Use 'both' instead of 'forwards'. Don't use opacity 0.` |
| Logo marquee | `Animate logos with marquee animation looping infinitely using duplicated items and alpha mask` |
| Beam effect | `Add beam animation connecting {a} to {b} with subtle sonar decorations` |
| New section | `Adapt a new {type} section, match existing styles` |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting with features instead of hero | Hero first - it sets the design system |
| Using default buttons | Reference UIVerse/CodePen for standout CTAs |
| Generic animations | Use specific animation prompts with `both` fill mode |
| Inconsistent new sections | Always reference existing design or screenshot |
| Skipping social proof | Add ratings, logos, or testimonials in/near hero |
| Over-animating | Subtle > flashy. Entry animations + 1-2 special effects |

## Section Checklist

- [ ] Hero with all elements (nav, eyebrow, headline, CTA, social proof, visual)
- [ ] Consistent icon set throughout
- [ ] Entry animations on each section
- [ ] Social proof visible above fold
- [ ] Unique button styling
- [ ] Features section
- [ ] How it works / process
- [ ] Testimonials or case studies
- [ ] Pricing (if applicable)
- [ ] FAQ
- [ ] Final CTA
- [ ] Footer with links

## Animation CSS Reference

```css
/* Entry animation base */
@keyframes fadeSlideIn {
  from {
    opacity: 0.01; /* Not 0 - prevents flash */
    transform: translateY(20px);
    filter: blur(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

.animate-entry {
  animation: fadeSlideIn 0.6s ease-out both;
}

/* Stagger children */
.stagger > *:nth-child(1) { animation-delay: 0.1s; }
.stagger > *:nth-child(2) { animation-delay: 0.2s; }
.stagger > *:nth-child(3) { animation-delay: 0.3s; }
/* ... */
```
