---
name: ui-polish
description: >
  Four quality gate checklists for frontend: baseline visual, accessibility,
  metadata/SEO, and motion performance. Post-implementation quality gates.
  Trigger: When reviewing UI changes, before merging frontend PRs, during sdd-verify.
license: MIT
metadata:
  author: JNZader
  version: "1.0"
  tags: [ui, accessibility, seo, performance, quality-gates]
  category: code-quality
  source: ibelick/ui-skills
allowed-tools: Read, Bash, Grep, Glob
---

## Purpose

Four quality gate checklists for frontend. Run after implementation, before merge.

---

## Gate 1: Baseline Visual Review

- [ ] Consistent spacing (design system scale)
- [ ] Typography hierarchy (h1 > h2 > h3, no skips)
- [ ] Color contrast WCAG AA (4.5:1 text, 3:1 large)
- [ ] Responsive: 375px, 768px, 1280px
- [ ] No horizontal overflow
- [ ] Loading states for async ops
- [ ] Empty states designed
- [ ] Error states designed
- [ ] Truncation handled (ellipsis, line clamp)

---

## Gate 2: Accessibility

- [ ] All interactive elements keyboard-reachable
- [ ] Visible focus indicators
- [ ] Skip-to-content link
- [ ] Images have alt text (decorative: alt="")
- [ ] Form inputs have labels (not just placeholders)
- [ ] ARIA roles correct (not overused)
- [ ] Color not the only information channel
- [ ] Touch targets 44x44px minimum
- [ ] aria-live for dynamic content
- [ ] Modals trap focus, restore on close

---

## Gate 3: Metadata & SEO

- [ ] Unique page title per page
- [ ] Meta description < 160 chars
- [ ] OG tags: title, description, image
- [ ] Twitter card tags
- [ ] Canonical URL
- [ ] Favicons (16, 32, 180, 192, 512)
- [ ] robots.txt
- [ ] sitemap.xml for public pages
- [ ] JSON-LD structured data
- [ ] html lang attribute

---

## Gate 4: Motion & Performance

- [ ] Animations use transform/opacity only
- [ ] CLS < 0.1
- [ ] Respects prefers-reduced-motion
- [ ] Transitions < 300ms for feedback
- [ ] No blocking animations on page load
- [ ] Images lazy-loaded below fold
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] Bundle size checked

---

## Report Format

```markdown
| Gate | Passed | Total | Status |
|------|--------|-------|--------|
| Visual | 8/9 | 9 | warning |
| Accessibility | 10/10 | 10 | pass |
| Metadata | 9/10 | 10 | warning |
| Performance | 9/9 | 9 | pass |
```

---

## Critical Rules

1. Run ALL 4 gates before merging frontend PRs
2. Accessibility gate is NON-NEGOTIABLE — failures block merge
3. Test at minimum 3 breakpoints: 375px, 768px, 1280px
4. ALWAYS check prefers-reduced-motion for animations
5. CLS > 0.1 or LCP > 2.5s are merge-blocking
