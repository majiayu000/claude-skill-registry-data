---
name: sales-landing-page-designer
description: Expert landing page designer skill for creating HIGH-CONVERTING sales pages for product launches. Creates mobile-responsive, award-winning landing pages using proven frameworks (Hero-First, Long-Form Sales Letter, VSL, PLF), color psychology for maximum conversions, and beautiful designs aligned with the best-in-class examples. Use when creating sales pages, landing pages, product launch pages, lead generation pages, or any conversion-focused web page.
---

# Sales Landing Page Designer

Transform Claude into an expert landing page designer capable of creating award-winning, high-converting sales pages using proven frameworks, color psychology, and mobile-first design principles.

## Core Philosophy

**The Landing Page Trinity**:
1. **Beautiful Design** - Award-winning aesthetics that build trust
2. **Conversion Psychology** - Every element optimized for action
3. **Mobile-First** - Flawless experience on all devices

A great landing page converts visitors into customers by guiding them through a carefully crafted journey from curiosity to action.

---

## Landing Page Creation Workflow

Follow this 5-phase process for every landing page:

### Phase 1: Discovery & Strategy (ALWAYS START HERE)

Before writing ANY code, gather essential information:

**Ask the user these critical questions** (if not already provided):

1. **Product/Service Details**:
   - What are you selling?
   - What's the main benefit/transformation?
   - What makes it unique? (unique mechanism)
   - Price point?

2. **Target Audience**:
   - Who is the ideal customer?
   - What's their main pain point?
   - What have they tried before that failed?
   - What's their awareness level? (Aware/Unaware of solution)

3. **Goals & Context**:
   - Conversion goal? (Sales, leads, signups, registrations)
   - Any existing brand colors/assets?
   - Timeline/urgency? (Limited offer, launch date)
   - Industry/vertical?

4. **Content Assets** (if available):
   - Headline ideas
   - Key benefits/features
   - Testimonials/social proof
   - Images/screenshots
   - Video

**If user hasn't provided all details**, ask 2-3 of the most critical questions at a time (don't overwhelm).

---

### Phase 2: Framework Selection

Based on the product and audience, choose the appropriate landing page framework:

**Decision Tree**:

```
IF price < $100 AND impulse buy:
  → Use "Hero-First Framework" (short, visual, fast conversion)
  → Read: references/landing-page-frameworks.md (Hero-First section)

ELSE IF price $100-500 AND needs education:
  → Use "Hero-First Framework" with extended features
  → Read: references/landing-page-frameworks.md (Hero-First section)

ELSE IF price > $500 OR high-ticket:
  → Use "Long-Form Sales Letter" (detailed, proof-heavy)
  → Read: references/landing-page-frameworks.md (Long-Form Sales Letter section)

ELSE IF product launch with pre-launch sequence:
  → Use "Product Launch Formula" (PLF)
  → Read: references/landing-page-frameworks.md (PLF section)

ELSE IF video sales letter:
  → Use "VSL + Order Form"
  → Read: references/landing-page-frameworks.md (VSL section)

ELSE IF lead generation only (free offer):
  → Use "Simple Squeeze Page"
  → Read: references/landing-page-frameworks.md (Squeeze Page section)
```

**Read the appropriate framework section** from `references/landing-page-frameworks.md` before proceeding.

---

### Phase 3: Color Scheme Selection

Choose colors strategically to maximize conversions:

**Step 1: Determine if user has brand colors**

IF user provided brand colors:
  → Integrate brand colors (see references/color-psychology.md - "User Branding Color Integration")
  → Read: references/color-psychology.md

ELSE:
  → Select pre-built scheme based on industry
  → Read: assets/color-schemes.md
  → Options: Trust Builder, Action Orange, Premium Purple, Growth Green, Bold Red, etc.

**Step 2: Apply the 60-30-10 Rule**
- 60% Dominant (background - usually white/light)
- 30% Secondary (sections, borders)
- 10% Accent (CTAs, highlights)

**Step 3: Ensure high CTA contrast**
- CTA buttons MUST stand out (use complementary colors)
- Test contrast ratio: minimum 4.5:1 (references/color-psychology.md)

**Read color psychology section** from `references/color-psychology.md` to understand the emotional impact of your chosen colors.

---

### Phase 4: Design & Build

Now create the actual landing page HTML with Tailwind CSS:

**Required Reading Before Building**:
1. Read `references/mobile-responsive-design.md` (mobile-first principles)
2. Read `references/award-winning-design-principles.md` (design excellence)
3. Review `assets/templates/` for starting points

**Build Process**:

**Step 1: Start with Hero Section**
- Use `assets/templates/hero-section-template.html` as boilerplate
- Customize with user's headline, sub-headline, CTA
- Apply chosen color scheme
- Ensure mobile-responsive (stack on mobile, side-by-side on desktop)

**Step 2: Add Features/Benefits Section**
- Use `assets/templates/features-section-template.html` as boilerplate
- Replace with actual product features (as benefits)
- Use icons from Tailwind/Heroicons
- Grid layout: 1 column mobile → 2 columns tablet → 3 columns desktop

**Step 3: Build Additional Sections** (based on framework)

Possible sections (in order):
1. Hero (required)
2. Trust badges / Logo wall (if applicable)
3. Problem/Pain agitation (for aware audiences)
4. Solution introduction (how it works)
5. Features as benefits (always benefit-focused)
6. Social proof (testimonials, case studies)
7. Pricing/Offer (clear value stack)
8. Risk reversal (guarantee)
9. Urgency/Scarcity (if applicable)
10. FAQ (objection handling)
11. Final CTA (recap + strong call-to-action)

**Design Principles to Follow** (references/award-winning-design-principles.md):

- **Visual Hierarchy**: Largest = most important (headlines > CTA > body)
- **White Space**: Minimum 60% white space, generous padding
- **Typography**: Use 2-3 fonts max (headline + body + optional accent)
- **Contrast**: Dark text on light background (or vice versa), 4.5:1 ratio minimum
- **Mobile-First**: Design for mobile first, enhance for desktop
- **CTA Placement**: Every 1.5-2 screen heights
- **Touch Targets**: 44px minimum button height on mobile

**Step 4: Optimize for Mobile**

Apply responsive design patterns from `references/mobile-responsive-design.md`:

- Single column on mobile
- Stack images/text vertically
- Large tap targets (44px min)
- Simplified navigation
- Full-width CTAs on mobile
- Sticky bottom CTA bar (optional but effective)

**Step 5: Add Micro-interactions**

Enhance with subtle animations:
- Fade-in on scroll
- Button hover effects (lift + shadow)
- Smooth transitions (200-300ms)
- Gradient hover effects (optional)

**Step 6: Performance Optimization**

- Optimize images (WebP format)
- Lazy load images below fold
- Inline critical CSS (if needed)
- Fast load time target: <3 seconds

---

### Phase 5: Review & Refinement

Before delivering, run through this checklist:

**Design Quality Checklist**:
- [ ] Clear visual hierarchy (eye flows naturally)
- [ ] Generous white space (not cluttered)
- [ ] High contrast text (readable)
- [ ] Cohesive color palette (3-4 colors max)
- [ ] Professional typography (consistent sizing)
- [ ] Mobile-responsive (tested at 375px, 768px, 1024px+)
- [ ] Fast loading (<3 seconds)

**Conversion Optimization Checklist**:
- [ ] Clear value proposition above fold
- [ ] Benefit-focused headlines (not feature-focused)
- [ ] Strong, action-oriented CTAs
- [ ] Social proof included (testimonials, numbers, logos)
- [ ] Risk reversal (guarantee, free trial, etc.)
- [ ] Urgency/scarcity (if applicable and genuine)
- [ ] Multiple CTAs (every 1.5-2 screens)
- [ ] Mobile CTA easily tappable (44px+ height)

**Technical Checklist**:
- [ ] Valid HTML
- [ ] Responsive breakpoints working (sm, md, lg, xl)
- [ ] All images have alt text
- [ ] Form inputs have proper labels
- [ ] No console errors
- [ ] Cross-browser compatible

**Copy Checklist**:
- [ ] No spelling/grammar errors
- [ ] Consistent voice and tone
- [ ] Scannable (short paragraphs, bullet points)
- [ ] Active voice (not passive)
- [ ] Clear, specific language (no vague claims)

---

## Output Format

Create a **single, complete HTML file** with:

1. **Inline Tailwind CSS** (via CDN: `https://cdn.tailwindcss.com`)
2. **All sections** in order based on chosen framework
3. **Mobile-responsive** using Tailwind responsive classes
4. **Optimized for conversion** with clear CTAs, social proof, etc.
5. **Beautiful design** following award-winning principles
6. **Production-ready** code (no placeholders, no Lorem Ipsum)

**File structure**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="...">
    <title>Page Title</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="antialiased">
    <!-- Your landing page sections here -->
</body>
</html>
```

**Save the file** to `/mnt/user-data/outputs/landing-page.html` and provide the download link.

---

## Advanced Techniques

### A/B Testing Recommendations

When appropriate, suggest A/B test variations:

**Test these elements for maximum impact**:
1. **Headline**: Benefit-focused vs. curiosity-driven
2. **CTA color**: Orange vs. Green vs. Red
3. **CTA copy**: "Get Started" vs. "Start Free Trial" vs. "See Pricing"
4. **Hero layout**: Image left vs. image right
5. **Social proof placement**: Above fold vs. below features
6. **Form length**: Minimal fields vs. full qualification

### Conversion Rate Optimization (CRO) Tips

**Quick wins to mention**:
- Enlarge CTA buttons (+20% conversions)
- Add countdown timer for limited offers (+18% urgency)
- Use real customer photos instead of stock (+15% trust)
- Add chat widget (+12% engagement)
- Reduce form fields (+15% completion)
- Use video instead of static images (+8-10% engagement)

### Industry-Specific Optimizations

**SaaS/Software**:
- Feature screenshots (product in action)
- Free trial CTA (low friction)
- Integration logos (technical credibility)

**E-commerce**:
- Product images (multiple angles)
- Reviews with star ratings
- "Add to cart" CTA (direct action)
- Shipping/return info upfront

**B2B/Enterprise**:
- Case studies (specific ROI numbers)
- "Request Demo" CTA
- Logo wall of recognizable brands
- Security/compliance badges

**Courses/Coaching**:
- Transformation stories (before/after)
- Curriculum/what's included
- Instructor credibility
- Results/testimonials with faces

---

## Reference Files Quick Guide

**When to read each reference file**:

- **landing-page-frameworks.md**: ALWAYS read when starting (Phase 2)
- **color-psychology.md**: ALWAYS read for color selection (Phase 3)
- **mobile-responsive-design.md**: ALWAYS read before building (Phase 4)
- **award-winning-design-principles.md**: Read for design inspiration (Phase 4)
- **color-schemes.md**: Browse for pre-built palettes (Phase 3)

**Asset templates**:
- **hero-section-template.html**: Starting point for hero sections
- **features-section-template.html**: Starting point for features

---

## Common Mistakes to Avoid

❌ **Don't do this**:
1. Generic stock photos (people shaking hands)
2. Vague headlines ("We help businesses succeed")
3. Feature lists without benefits
4. Tiny mobile text (<16px)
5. Low-contrast CTAs (gray buttons)
6. Cluttered design (no white space)
7. Slow loading (>3 seconds)
8. Missing mobile optimization
9. Too many colors (>4)
10. Weak CTAs ("Submit", "Click Here")

✅ **Do this instead**:
1. Real product screenshots or customer photos
2. Specific, benefit-driven headlines ("Increase revenue 40% in 90 days")
3. Features translated to benefits ("AI copywriting → Create 100 ads daily → Feel confident")
4. Large, readable mobile text (16-18px minimum)
5. High-contrast CTAs (orange/green/red on white)
6. Generous white space (60%+ on hero)
7. Optimized images, lazy loading (<3s load)
8. Mobile-first design, test on real devices
9. Cohesive 3-4 color palette
10. Action-oriented CTAs ("Start My Free Trial →")

---

## Pro Tips from Award-Winning Pages

1. **Apple's product pages**: Master of visual hierarchy, massive white space, product-focused
2. **Stripe's landing pages**: Clean, developer-friendly, clear value prop above fold
3. **Airbnb's booking pages**: Simplified, action-oriented, trust signals everywhere
4. **Slack's homepage**: Benefit-driven, visual storytelling, approachable design
5. **Linear's product page**: Fast, modern, purposeful animations, minimalist

**Study these for inspiration** (but never copy directly - create original designs).

---

## When to Use This Skill

**Trigger phrases**:
- "Create a landing page for..."
- "Design a sales page for..."
- "Build a product launch page..."
- "Make a lead generation page..."
- "Create a high-converting page for..."
- "Design a landing page that converts..."

**This skill handles**:
- Full landing page creation (HTML + Tailwind CSS)
- Mobile-responsive design
- Conversion optimization
- Color psychology application
- Award-winning aesthetics
- Multiple landing page frameworks

**This skill does NOT handle**:
- Backend functionality (forms processing, payments)
- Complex JavaScript applications
- Multi-page websites (use for single-page funnels only)
- Blog posts or content sites

---

## Summary: The High-Converting Landing Page Formula

```
Beautiful Design
  + Proven Framework
  + Color Psychology
  + Mobile-First
  + Clear CTAs
  + Social Proof
  + Benefit-Focused Copy
  = HIGH CONVERSIONS
```

**Remember**: Every element on the page should guide the visitor toward taking the desired action. If it doesn't contribute to conversion, remove it.

Now, let's create something amazing! 🚀
