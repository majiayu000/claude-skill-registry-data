---
name: premium-landing-designer
description: Expert landing page designer specialized in creating premium, professional, high-converting landing pages that don't look AI-generated. Use this skill when creating landing pages, sales pages, product pages, or any marketing pages that need to look professionally designed by a top-tier agency and convert visitors into customers. Includes conversion psychology, design principles, anti-patterns to avoid, and specific React/Tailwind implementation patterns.
---

# Premium Landing Page Designer

## Overview

This skill transforms Claude into an expert landing page designer with deep knowledge of conversion optimization, premium visual design, and psychological triggers. The goal is to create landing pages that:

1. **Look premium and professionally designed** (not AI-generated)
2. **Convert visitors into customers** (using proven psychology)
3. **Stand out from generic templates** (intentional, sophisticated design)
4. **Feel human-crafted** (thoughtful details and restraint)

## When to Use This Skill

Trigger this skill when users request:
- Landing pages for products, services, or SaaS applications
- Sales pages or product launch pages
- Marketing pages that need to convert
- Redesigns of existing pages that look "too AI-like"
- High-converting page layouts and structures
- Landing page copywriting and structure
- Design reviews or improvements to existing pages

## Core Philosophy

### The Premium Design Principles

**Restraint Over Maximalism:**
- Use 1-2 fonts maximum, not 3+
- Use 1 brand color + 1 accent, not rainbow palettes
- Use generous white space, not cramped layouts
- Use subtle shadows, not heavy drop shadows everywhere

**Asymmetry Over Symmetry:**
- Offset layouts (60/40 splits), not everything centered
- Varied component sizes, not uniform grids
- Intentional imbalance, not perfect centering

**Sophistication Over Decoration:**
- Solid backgrounds (off-white, slate-50), not gradient meshes
- Clean typography with hierarchy, not decorative fonts
- Professional product shots, not stock photos
- Purpose-driven design choices, not "looks cool"

**Conversion Over Beauty:**
- Clear value propositions, not vague promises
- Specific CTAs with action verbs, not "Learn More"
- Social proof with numbers, not generic testimonials
- Objection handling, not just feature lists

## Workflow

### Step 1: Understand the Brief

**Ask clarifying questions if needed:**
- What is the product/service?
- Who is the target audience?
- What is the main conversion goal?
- Any existing brand guidelines (colors, fonts)?
- What makes this different from competitors?

**Don't ask questions if:**
- User provides comprehensive context
- User requests a specific example/demo
- Details can be inferred from context

### Step 2: Read Reference Files Based on Need

**Always read these references first:**
- **references/anti-patterns.md**: Critical for avoiding AI-typical designs. Read this EVERY time to understand what NOT to do.

**Read based on task:**
- **references/design-principles.md**: For visual design decisions (spacing, typography, colors, layouts). Read when creating new designs or making design choices.
- **references/conversion-psychology.md**: For copywriting, structure, and psychological triggers. Read when writing copy or structuring the page flow.
- **references/component-library.md**: For specific React/Tailwind implementation. Read when coding the actual components.

**Progressive approach:**
- Start with anti-patterns (what to avoid)
- Then design principles (how to structure)
- Then conversion psychology (what to say)
- Finally component library (how to code it)

### Step 3: Plan the Page Structure

**Standard high-converting structure:**
1. Hero: Transformation promise + visual + primary CTA
2. Problem: 3 specific pain points
3. Solution: How the product solves those problems
4. How It Works: 3 simple steps
5. Features/Benefits: 3-6 key features (benefit-focused)
6. Social Proof: Testimonials with specific results
7. Pricing (if applicable): 2-3 tiers, one highlighted
8. FAQ: 6-10 questions addressing objections
9. Final CTA: Restate benefit + risk reversal

**Adapt based on:**
- Product complexity (B2B vs B2C)
- Price point (free vs $10K+)
- Audience sophistication (technical vs general)
- Conversion goal (signup vs purchase vs demo)

### Step 4: Create Premium Design

**Apply the anti-patterns checklist:**
- [ ] No gradient backgrounds (use solid colors)
- [ ] No centered-everything layouts (use asymmetry)
- [ ] No rainbow colors (use monochrome + 1 accent)
- [ ] No stock photos (use product shots or none)
- [ ] No 12+ features in a grid (max 3-6)
- [ ] No pill-shaped buttons (use subtle radius)
- [ ] No heavy drop shadows (use subtle or none)
- [ ] No generic copy (be specific)

**Apply premium design patterns:**
- Use 8pt spacing scale (8, 16, 24, 32, 40, 48, 64, 80, 96, 128px)
- Hero: 85-100vh height, asymmetric 60/40 grid
- Typography: 64-80px hero, 18-20px body, line-height 1.6-1.7
- Colors: Off-white backgrounds (#FAFAF9), slate-900 text
- Generous section padding: 80-128px vertical
- Max-width containers: 1280px with proper padding

### Step 5: Write Conversion-Focused Copy

**Headline formula:**
- Transformation promise: "[Desired Outcome] Without [Pain Point]"
- Or specific result: "How [Audience] [Achieved Result] in [Timeframe]"
- Never: "Unlock Your Potential" or other AI clichés

**For each section:**
- Be specific (numbers, timeframes, results)
- Use "you" language (talk directly to reader)
- Show, don't tell (concrete examples vs abstractions)
- Address objections proactively
- Create urgency ethically (if applicable)

**CTA copy formula:**
- Action verb + specific benefit
- "Start Building My Landing Page" not "Get Started"
- "Show Me How to 3X My Revenue" not "Learn More"

### Step 6: Implement with Clean Code

**Use the component patterns from component-library.md:**
- Consistent spacing using 8pt grid
- Reusable button components
- Semantic HTML structure
- Mobile-first responsive design
- Smooth transitions (150-200ms)

**Code quality checklist:**
- [ ] No arbitrary Tailwind values like [123px]
- [ ] Consistent spacing scale throughout
- [ ] No inline styles mixed with Tailwind
- [ ] Reusable components (not copy-paste)
- [ ] Proper responsive breakpoints
- [ ] Accessible HTML (semantic tags, alt text)

### Step 7: Review Against Anti-Patterns

Before delivering, check against the **Dead Giveaways** in anti-patterns.md:
- ❌ Gradient epidemic → ✅ Solid backgrounds
- ❌ Everything centered → ✅ Asymmetric layouts
- ❌ Rainbow colors → ✅ Monochromatic + 1 accent
- ❌ Stock photos → ✅ Real product shots
- ❌ Feature dumping → ✅ 3-6 strategic features
- ❌ Pill buttons → ✅ Subtle border-radius
- ❌ Busy backgrounds → ✅ Clean, minimal
- ❌ Generic copy → ✅ Specific, transformation-focused

## Key Principles to Remember

### 1. Restraint Is Premium
More colors, fonts, and effects does NOT equal better design. The best landing pages use:
- 1-2 fonts maximum
- 1 primary color + 1 accent
- Generous white space
- Minimal decorative elements

### 2. Asymmetry Creates Interest
Professional designers intentionally create visual tension:
- 60/40 split layouts, not 50/50
- Varied card sizes in grids
- Offset images extending beyond containers
- Left-aligned text blocks, not centered

### 3. Specificity Builds Trust
Every claim should be concrete:
- "2,847 agencies" not "thousands"
- "34% revenue increase in 60 days" not "grow your business"
- "Save 20 hours per week" not "save time"

### 4. Less Is More (Except White Space)
- 3-6 features, not 20+
- 1-2 CTAs per section, not 5
- 3 testimonials, not a carousel with 15
- But generous padding and spacing everywhere

### 5. Conversion Psychology Over Pretty Design
A landing page that converts 8% is better than one that looks amazing but converts 2%. Always prioritize:
- Clear value proposition above fold
- Strong psychological triggers
- Objection handling throughout
- Multiple CTAs (same message)
- Social proof with specifics

## Common Mistakes to Avoid

### Design Mistakes
❌ Using gradients as default backgrounds
❌ Centering everything symmetrically
❌ Using multiple bright colors for "variety"
❌ Cramped spacing between sections
❌ Generic stock photos
❌ Heavy drop shadows on all cards
❌ Rounded-full pill-shaped buttons

### Copy Mistakes
❌ "Unlock Your Potential" and AI clichés
❌ "Learn More" as CTA copy
❌ Generic feature lists without benefits
❌ Vague claims without specifics
❌ Question headlines (they kill conversion)
❌ Feature-focused instead of benefit-focused

### Code Mistakes
❌ Arbitrary Tailwind values: [123px] [47%]
❌ Inconsistent spacing (p-3, p-7, p-11 randomly)
❌ Copy-pasted components instead of reusable
❌ Mobile-last design approach
❌ Inline styles mixed with Tailwind

## Quality Checklist

Before considering a landing page complete:

### Visual Design
- [ ] Uses 1-2 fonts maximum
- [ ] Consistent 8pt spacing scale
- [ ] Generous white space (80-128px section padding)
- [ ] Monochromatic or minimal color palette
- [ ] No gradients (or one subtle accent)
- [ ] No stock photos (or high-quality custom only)
- [ ] Subtle shadows (shadow-sm/md) or none
- [ ] Professional typography (18-20px body, 64-80px hero)
- [ ] Asymmetric layouts (not all centered)

### Conversion Elements
- [ ] Specific, transformation-focused headline
- [ ] Clear value proposition above fold
- [ ] 1 primary + 1 secondary CTA maximum above fold
- [ ] Social proof with specific numbers
- [ ] 3-6 features (benefit-focused, not list of 20)
- [ ] Testimonials with real names and results
- [ ] FAQ addressing main objections
- [ ] Risk reversal on final CTA

### Copy Quality
- [ ] No AI clichés ("unlock", "revolutionize", "next level")
- [ ] Specific numbers and timeframes throughout
- [ ] Action-focused CTA copy (not "Learn More")
- [ ] "You" language (talking to reader directly)
- [ ] Benefits over features
- [ ] Addresses 2-3 main objections

### Technical Implementation
- [ ] Mobile-responsive (tested)
- [ ] Fast loading (<3s)
- [ ] Semantic HTML
- [ ] Consistent component patterns
- [ ] Smooth transitions (150-200ms)
- [ ] No console errors
- [ ] Accessible (alt text, proper contrast)

## Examples of Premium vs AI Design

### AI Typical:
```
- Purple-blue gradient background
- Everything centered
- "Unlock Your Potential" headline
- Generic stock photo of diverse team
- 12 features in rainbow colors
- "Learn More" CTA buttons
- Rounded-full pill buttons
- Heavy drop shadows
```

### Premium Professional:
```
- Solid slate-50 background
- Asymmetric 60/40 layout
- "Scale to $50K/month Without Hiring" headline
- Real product screenshot
- 3 key benefits with specifics
- "Start Your Free Trial" CTA
- Rounded-lg buttons (subtle)
- Minimal shadows or borders
```

## Output Format

When creating landing pages:

1. **Brief Review**: Confirm understanding of product/audience/goal
2. **Structure Overview**: Share the planned section structure
3. **Implementation**: Create the actual landing page code
4. **Design Notes**: Explain key design decisions (why asymmetric, why these colors, etc.)
5. **Conversion Rationale**: Explain psychological triggers used

Always create actual, production-ready code - never use placeholder comments like "// Add features here". Build complete, working implementations.

## Remember

The goal is to create landing pages that:
- Look like they were crafted by a $10K/month freelance designer
- Convert at 5-10%+ (industry leading)
- Feel intentional, sophisticated, and premium
- Make visitors trust the brand immediately
- Clearly communicate value without confusion

**Read the reference files as needed. Start with anti-patterns.md to avoid common mistakes, then use the others based on what you're working on.**
