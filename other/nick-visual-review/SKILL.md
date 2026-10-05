---
name: nick-visual-review
description: Full automated QA suite — visual design review + UAT functional testing. Screenshots every viewport, analyzes against Nick's design system, then runs functional UAT (navigation, links, forms, buttons, auth flow, accessibility, performance, console errors, responsive testing). Use after every deployment.
metadata:
  openclaw:
    requires:
      bins: ["npx"]
---

# Visual Review + UAT

## When to Use
- After EVERY deployment (called automatically by nick-project-orchestrator's post-deploy step)
- When Nick asks to review a site's design or test it
- When Nick shares a URL and asks for feedback
- When iterating on a project and need to verify changes

## Process

### Step 1 — Capture Screenshots (Visual Review)
Run the visual review script:

```bash
node skills/nick-visual-review/scripts/review.js <URL> /tmp/review-<project-name>
```

This captures:
- **8 screenshots:** full-page + above-fold at 4 viewports (mobile 375px, tablet 768px, laptop 1280px, desktop 1920px)
- **Page metadata:** title, h1, meta description, OG image, image alt-text audit, font sizes used
- **Console errors:** any JS errors on the page

### Step 2 — Run UAT (Functional Testing)
Run the UAT script:

```bash
node skills/nick-visual-review/scripts/uat.js <URL> /tmp/uat-<project-name>
```

This performs:
- **Page load + performance:** Load time, status code, DOM metrics
- **Internal navigation:** Visits up to 20 internal routes, flags broken ones (4xx/5xx), screenshots broken pages
- **Link audit:** Discovers all internal + external links
- **Form audit:** Finds all forms, checks inputs have labels, identifies missing required attributes
- **Button/CTA audit:** Discovers all buttons, checks touch target sizes (min 44x44px)
- **Auth flow detection:** Finds login/signup pages, verifies email/password/submit fields exist
- **Accessibility:** Images without alt text, heading hierarchy, skip links, lang attribute, h1 count
- **Mobile responsiveness:** Tests on iPhone viewport — checks horizontal scroll, text size
- **Console errors:** Captures all JS errors across pages
- **Network errors:** Captures failed requests
- **Auto-grading:** A/B/C/D/F based on issue severity

### Step 3 — Analyze Screenshots with Vision
Use the `image` tool to analyze each screenshot. Review against nick-design-system standards:

```
For each viewport, check:
```

#### Typography
- [ ] Headlines are large, declarative, sans-serif
- [ ] Body text is 16px+ on all viewports
- [ ] Heading hierarchy is clear (visual distinction between h1/h2/h3)
- [ ] No more than 2 font families visible
- [ ] Letter-spacing and line-height look comfortable

#### Color & Contrast
- [ ] Brand accent color is used intentionally (CTAs, highlights)
- [ ] No generic AI gradients or SaaS-purple
- [ ] Text contrast appears sufficient (especially on dark backgrounds)
- [ ] Color palette feels cohesive and branded
- [ ] Dark/light section alternation creates rhythm

#### Layout & Spacing
- [ ] Generous whitespace between sections
- [ ] Content doesn't feel cramped on any viewport
- [ ] Consistent alignment and grid structure
- [ ] Hero section commands attention (full/near-full viewport)
- [ ] Footer is comprehensive, not an afterthought

#### Navigation
- [ ] Nav is clean, structured, visible
- [ ] Mobile nav is a full-screen overlay (not tiny dropdown)
- [ ] Nav signals depth if there are multiple sections

#### Responsive
- [ ] No horizontal scroll at any viewport
- [ ] Content reflows properly at each breakpoint
- [ ] Touch targets look adequate on mobile (44x44px minimum)
- [ ] Images don't overflow or distort
- [ ] Text remains readable at all sizes

#### Components
- [ ] Buttons have proper padding, not pill-shaped
- [ ] Cards have consistent heights in grids
- [ ] Forms have clear labels (not floating labels)
- [ ] Interactive elements have visible hover/focus indicators

#### Anti-Patterns (Flag ANY of these)
- Generic AI gradients
- Cookie-cutter SaaS template look
- Stock photography
- Decorative blobs or amorphous shapes
- Tiny hamburger dropdown menus
- Rounded-full pill buttons
- Low contrast text
- Sloppy responsive (content breaking/overflowing)
- Floating label inputs
- "Built with template" energy

### Step 4 — Review UAT Results
Read `/tmp/uat-<project-name>/uat-results.json` and analyze:
- Pages checked and any broken routes
- Form issues (missing labels, missing inputs)
- Button touch target violations
- Auth flow completeness
- Console and network errors
- Performance metrics
- Accessibility findings
- Mobile responsiveness issues
- Auto-assigned grade

### Step 5 — Check Visual Metadata
Review `page-meta.json`:
- [ ] Page has a title
- [ ] Exactly 1 h1 tag
- [ ] Meta description exists
- [ ] OG image exists
- [ ] All images have alt text (flag count of missing)

### Step 6 — Generate Combined Report
Present findings to Nick in this format:

```
## QA Report: [Project Name]
URL: [url]

### Overall Grade: [A/B/C/D/F]
Visual Grade: [grade] | Functional Grade: [grade]

### ✅ What's Working
- [list strengths — design + functionality]

### 🔴 Critical Issues
- [anything that blocks usage]

### 🟡 Major Issues
- [significant problems — broken routes, auth issues, responsive failures]

### 🔵 Minor Issues
- [polish items — accessibility, SEO, small visual tweaks]

### 📊 Functional Results
- Pages tested: [count]
- Broken routes: [count]
- Forms found: [count] | Form issues: [count]
- Buttons/CTAs: [count] | Touch target violations: [count]
- Auth flow: [detected/not detected] | [complete/incomplete]
- Console errors: [count]
- Network errors: [count]
- Load time: [ms]

### 🎨 Design System Compliance
- Typography: [pass/fail + notes]
- Colors: [pass/fail + notes]
- Spacing: [pass/fail + notes]
- Components: [pass/fail + notes]
- Responsive: [pass/fail + notes]
- Anti-patterns detected: [list any]

### 📱 Responsive
- Mobile (375px): [pass/fail + notes]
- Tablet (768px): [pass/fail + notes]
- Laptop (1280px): [pass/fail + notes]
- Desktop (1920px): [pass/fail + notes]

### ♿ Accessibility
- Images without alt: [count]
- Heading hierarchy: [correct/skipped]
- Lang attribute: [yes/no]
- Skip link: [yes/no]

### 🔧 Recommended Fixes (Priority Order)
1. [highest priority fix]
2. [next fix]
...

### Screenshots
[Share key screenshots — especially any showing issues]
```

### Grading Scale
- **A:** Matches design system. Looks like a top-tier enterprise site. Ship it.
- **B:** Solid but has minor issues. 1-2 small fixes needed. Still shippable.
- **C:** Noticeable design system violations. Needs iteration before it represents Nick well.
- **D:** Significant issues — layout problems, anti-patterns present, responsive breakage.
- **F:** Does not meet standards. Needs rebuild of affected sections.

## Rules
- Be honest. If it looks like generic AI output, say so.
- Always include screenshots in the report so Nick can see what you see.
- Run BOTH scripts (visual review + UAT) on every review. Never skip UAT.
- Prioritize fixes: critical (blocks usage) > major (broken routes, auth, responsive) > minor (polish, a11y, SEO).
- If grade is C or below, offer to fix the issues immediately.
- Don't just flag problems — explain WHY they're problems and WHAT the fix is.
- If UAT catches broken routes or auth issues, those are CRITICAL — fix before showing Nick.
- After fixing issues, re-run both scripts to verify fixes landed.
