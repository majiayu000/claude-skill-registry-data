---
name: frontend-audit
description: "Use when the user asks to audit, review, critique, or \"make sure it looks right\" on a deployed web page, component, or Figma mockup — or when they mention visual issues, CRO, conversion rate, design consistency, accessibility, \"feels off\", \"looks bad\", \"make it pop\", \"looks like AI slop\". Triggers on keywords like \"audit the page\", \"review the design\", \"what's wrong with this UI\", \"CRO audit\", \"a11y check\", \"visual hierarchy\", \"typography check\", \"does this look right\". Activation also recommended after any significant frontend change on gotcontext.ai before calling the work done."
---

# Frontend Audit Skill

Run a systematic, opinionated audit of a web page or component before calling frontend work done. Produces a scored report and hands off to **aura-screenshot-clone** when fixes need to be pulled from reference sites.

This skill operationalises the research consensus from 2026 design-audit frameworks (Apexure, ConvertCart, Red Rattler, Nielsen Norman, WCAG 2.2). It runs in ~10 minutes per page and produces a prioritised punch list, not a wall of findings.

## When to use

Invoke when:
- User says "audit", "review", "check", "make sure it looks right", "critique this page"
- User mentions visual issues: "feels off", "looks bad", "looks like mad science", "cluttered", "looks like AI slop"
- User mentions CRO, conversion, accessibility, a11y, WCAG, mobile, visual hierarchy, typography, spacing, whitespace
- **Proactively** after shipping any frontend change on gotcontext.ai. A one-pass audit on the live URL before saying "done" catches issues that CI can't.

## When NOT to use

- Pure code review (logic, state, security) — that's `code-review` / `pr-review-toolkit:code-reviewer`.
- Designing from scratch with no reference — use `frontend-design:frontend-design` or `brainstorming`.
- Cloning a reference pattern — use **aura-screenshot-clone** directly. This skill hands off TO that one when fixes are needed.

## Inputs (pick one)

1. **Live URL** — preferred. Use `mcp__claude-in-chrome__navigate` + `computer action=screenshot` at 1440×900 desktop + 375×812 mobile.
2. **Local dev server** — `npm run dev` then navigate the browser to `http://localhost:3000/...`.
3. **Screenshot(s) attached by user** — skip the browser phase, go directly to the scoring.

Always capture **both desktop (1440×900) and mobile (375×812)**. Mobile-only issues are ~40% of findings on pages built desktop-first.

## The 9-pillar audit

Go through pillars in order. Score each 1–5 (1 = critical / broken, 5 = excellent). Stop and fix anything scoring 1 or 2 before moving on — a broken above-the-fold kills everything downstream.

### Pillar 1 — Above the fold (weight: heaviest)

Nielsen Norman: users spend **57% of viewing time** here. Apexure audits attribute **~40% of all findings** to the first screen.

Answer these three questions in 5 seconds flat:
1. **What is this?** (clear value prop in the H1)
2. **Is it for me?** (named audience or outcome)
3. **Should I trust it?** (at least one proof element — logo bar, stat, testimonial, "as seen in" row)

Red flags:
- Primary CTA below the fold on mobile (375px viewport)
- Multiple competing CTAs above the fold (more than 1 primary + 1 secondary)
- Stacked announcement bars (>1) — they collide and compete with the hero
- Hero headline with orphaned words on their own line ("bill —" alone, "and —" alone)
- No visual proof (chart, screenshot, product shot, badge) — text-only hero on marketing page
- Stale banner content (version numbers, dates that drifted since the last release)

### Pillar 2 — Visual hierarchy & typography

Research consensus (Layout Scene, Inkbot, Clay):
- **Type scale**: 4–7 distinct sizes max. Use a modular ratio (1.25 minor-third, 1.333 perfect-fourth, or 1.618 golden-ratio).
- **H1:body ratio** should be 2.5–4× (e.g. 48–60px H1 against 16–18px body on desktop).
- **Body text minimum 16px.** Not 14px. Not 12px. Small print can go down to 13–14px for true secondary labels.
- **Line height** 1.5× body font size. 1.2–1.3× for headings only.
- **Line length** 50–80 characters (roughly 600–700px for body). Wider causes "tracking errors" where the eye jumps lines.
- **Max 2–3 font families.** Ideally one (Inter, Outfit, etc.) with weight variants.

Red flags:
- Any body text under 16px
- Line height under 1.5× on paragraphs
- More than 3 font families
- Line length > 100ch on desktop (reads like a terminal dump)
- All-caps paragraphs (reduces reading speed 13–20%). All-caps OK only for labels / buttons < 3 words
- H1 same size as H2 (no hierarchy)
- Orphan words / widows on heading line breaks

### Pillar 3 — Spacing & rhythm

Marmeto / Timgraf research:
- Use an **8px baseline grid** (every margin, padding, gap is a multiple of 8px: 8/16/24/32/48/64/96). 4px for fine detail only.
- Section padding vertical: at least **64px desktop / 40px mobile**, preferably 96/56 on marketing pages.
- Card padding: minimum 24px inner on desktop, 16px on mobile.
- Whitespace around primary CTAs: minimum 32px clearance on all sides — crowded buttons convert worse.

Red flags:
- Arbitrary pixel values (13px, 27px, 51px) — signals someone eyeballed instead of using tokens
- Uneven section padding (64px top, 32px bottom on the same section)
- Two elements touching when they shouldn't (summary pills abutting hero with no breathing room)
- Text pressed against card edges (card padding < 16px)

### Pillar 4 — Color & contrast (WCAG 2.2)

From BrowserStack + TheFrontKit + nextool.app:
- **Body text contrast ≥ 4.5:1** against background (AA requirement)
- **Large text (18pt+ bold, 24px+ regular) ≥ 3:1**
- **Interactive element borders / focus indicators ≥ 3:1**
- **Placeholder text** must also meet 4.5:1 — don't use washed-out gray
- **Touch targets ≥ 24×24 CSS pixels** (AA), 44×44px recommended on mobile
- **Never set `outline: none` without an alternative focus style**
- **Never disable pinch-to-zoom** (`user-scalable=no` is a WCAG failure)

Red flags:
- Low-contrast captions (#888 on #000 is only 3.5:1 — fails AA for body)
- Color as the only signal (red-text error without icon / label)
- Hover-only info (mobile has no hover)
- Focus ring removed on interactive elements

**Quick check**: open Chrome DevTools → Lighthouse → Accessibility. Should score **≥ 95**. Also run axe DevTools for rule-level issues.

### Pillar 5 — CTAs & action paths

Apexure + Codivox + ConvertCart:
- **One primary action per page.** Repeat it 2–3 times at decision points.
- **Action verbs, first-person**: "Start saving", "Get my quote" beats "Submit", "Get Started"
- **CTA contrast** with surrounding content — the button should be the highest-contrast element in its section
- **Mobile CTA must be thumb-reachable** without scrolling on 375px viewport
- **Generously sized**: 18–20px font, 12–16px vertical padding. Cramped buttons feel cheap.

Red flags:
- Primary + secondary CTA with same visual weight (user can't tell which is primary)
- Ghost button as the primary CTA (low contrast, gets ignored)
- CTA text length > 4–5 words
- No repeat CTAs — user has to scroll all the way back to the hero

### Pillar 6 — Trust & social proof

Specificity matters. "Trusted by thousands" is noise; "Used by 400+ teams including Stripe, Linear, and Vercel" is signal.

Check:
- **Above the fold**: at least one proof element (logo bar, review count badge, named stat)
- **Near each CTA**: a testimonial, badge, or stat anchored to the specific objection that CTA creates
- **Third-party badges** (G2, Clutch, Trustpilot) beat self-hosted testimonials
- **Numbers**: specific customer counts, uptime %, compression %, time saved — not adjectives

Red flags:
- Zero proof above the fold
- Generic "Happy customers ❤️" sections without names / companies / photos
- Self-declared superlatives ("the fastest", "the best") without evidence
- Stock photo testimonials or obvious AI faces

### Pillar 7 — Performance

Google Core Web Vitals 2026 thresholds (Marmeto, Optimum Web):
- **LCP < 2.5s** (Largest Contentful Paint)
- **INP < 200ms** (Interaction to Next Paint — replaced FID)
- **CLS < 0.1** (Cumulative Layout Shift)
- **TBT < 200ms**, **FCP < 1.8s**, **TTFB < 800ms**

Image rules:
- Hero image: `fetchpriority="high"` + explicit `width`/`height`
- Below-fold images: `loading="lazy"`
- All images: WebP or AVIF (JPEG only for fallbacks)
- All images: explicit dimensions to prevent CLS

Quick check: Chrome DevTools → Lighthouse → Performance. Should score **≥ 90** on desktop.

### Pillar 8 — Mobile / responsive

Test at **320px** (smallest common viewport) and **375px** (iPhone SE / mini).

Red flags:
- Horizontal scrollbar at any viewport ≥ 320px (bleeding content)
- Text pressed against viewport edges (< 16px gutter on mobile)
- Touch targets < 44×44px
- Desktop nav visible on mobile (no hamburger)
- Multi-column layouts that don't collapse properly
- Sticky elements covering more than 15% of mobile viewport

### Pillar 9 — AI-slop smell test

An LLM-generated page has signatures:
- Too many emojis, especially as bullet markers
- Gradient backgrounds on every card (overused by AI defaults)
- Every section has the same structure (label pill → H2 → paragraph → CTA — monotone)
- Generic stock imagery with people in suits pointing at laptops
- "Lorem ipsum"-flavored body copy ("In today's fast-paced digital landscape...")
- Rounded-xl + border + bg-white/[0.02] + backdrop-blur on every surface

Cure: break the rhythm. Some sections should be prose. Some should be data. Some should be full-bleed. Some should be minimal.

## Output format

Produce a single markdown report with this exact structure:

```markdown
# Frontend audit — <page name> — <YYYY-MM-DD>

**Overall score: X/45** (5 per pillar)

## Critical (must fix before ship)
- [ ] <one-line issue> · pillar <#> · score <1-2>
  - Current: <what's there now>
  - Fix: <concrete, actionable>

## High (fix this sprint)
- [ ] <issue> · pillar <#> · score 3

## Polish (nice-to-have)
- [ ] <issue> · pillar <#> · score 4

## Top 3 fixes by impact-to-effort ratio
1. <Fix> — why it matters, est. effort
2. ...
3. ...

## Aura handoff candidates
(issues where pulling a pattern from a reference site is faster than redesigning from scratch)
- <issue> → reference: <URL or site name>
```

Keep the report scannable. Headers and checkboxes, not prose paragraphs.

## Handoff to aura-screenshot-clone

When an audit finding scores ≤ 3 AND the fix is "adopt a pattern from a better site", hand off to the `aura-screenshot-clone` skill:

1. Name the specific component/section that needs redesign
2. Suggest a reference URL (known-to-work list from aura-screenshot-clone skill)
3. Invoke `aura-screenshot-clone` with the reference and the specific remix instruction (e.g. "clone the above-the-fold pattern but keep our measured-data table")

Do **not** invoke aura for issues that are pure copy fixes, pixel-level spacing tweaks, or color contrast adjustments — those are direct edits.

## Audit-loop pattern (after fixing)

After fixing findings:
1. Hard-refresh the live URL (Ctrl+Shift+R)
2. Re-screenshot at both viewports
3. Re-score only the pillars where issues were found
4. Confirm each fix didn't regress another pillar

## Anti-patterns to avoid

- **Endless scope creep** — if the audit finds 25 issues, fix the top 5. Don't boil the ocean.
- **Designing in isolation** — always have a live URL or Figma frame open, not your imagination of the page.
- **Accessibility afterthought** — run axe/Lighthouse BEFORE the aesthetic audit. If body text is unreadable, nothing else matters.
- **Score inflation** — a 4 means "this is good, we'd leave it alone". A 3 means "fixable but not today". If you're rounding everything up to 4, the audit is useless.
- **No before/after** — always screenshot before AND after. The diff is the proof the fix worked.

## Related skills

- `aura-screenshot-clone` — pull design patterns from reference sites (use WHEN audit findings point to a pattern-level fix)
- `frontend-design:frontend-design` — design new components from scratch (use when NO good reference exists)
- `code-review:code-review` — logic/state/a11y code-level review (use alongside, NOT instead of)
- `superpowers:brainstorming` — for scope / strategy before design (audit is downstream of brainstorming)

## References

- Apexure — "The Landing Page Audit Checklist We Use After 3,000+ Projects" (2026)
- ConvertCart — 38-Point Landing Page CRO Checklist (2026)
- Red Rattler Creative — Complete Website Audit Checklist 2026
- Marmeto — Web Design Checklist 2026
- Timgraf — Typography Hierarchy in UI Design 2026
- Layout Scene — Typographic Hierarchy Guide 2026
- Clay.global — Visual Hierarchy in Web Design 2026
- BrowserStack — Design Accessibility Checklist 2026
- TheFrontKit — WCAG AA Checklist for Web Apps 2026
- nextool.app (ANIMA) — Web Accessibility Checklist 2026 (WCAG 2.2)
- Nielsen Norman — F-pattern scanning, above-the-fold attention research
- Optimum Web — 200-Point Technical Audit Checklist 2026
- Inkbot Design — You've Got 3 Seconds (2026)

## Cross-references
- `real-user-qa` — functional ship-readiness pass (severity-filed bugs, YES/NO verdict); run it alongside this visual/CRO audit before any ship call.
- `ui-fix-observe-first` — the fix loop for defects either pass files.
