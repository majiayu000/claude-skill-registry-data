---
name: uiux-review-skill
description: >-
  UI/UX design review — 13-axis rubric (AslanMazhidov, RNT56, Nielsen
  heuristics, anti-default AI detection) with Playwright capture protocol.
license: MIT
compatibility: opencode
category: Framework
---

## What I do

I provide the reusable domain knowledge for UI/UX design review. I am loaded by `uiux-reviewer-subagent` and define:

1. **Evidence-first methodology** — the gate rule that all findings must pass
2. **Playwright capture protocol** — standardized evidence collection
3. **13-axis review rubric** — the core review instrument
4. **Finding schema** — structured output format
5. **Severity rubric** — Critical / Major / Minor disposition
6. **References** — source attribution and licensing

This skill is **review-only**. I do not modify code, generate fixes, or produce new UI. For fixes, the parent agent delegates to `responsive-audit-subagent` (mechanical responsive fixes) or the `build` agent.

## When to use me

Use this skill when:
- Reviewing UI screenshots for visual design quality
- Auditing a live web application against usability heuristics
- Checking design-system consistency across components
- Evaluating accessibility basics (deep dives delegate to `accessibility-a11y-skill`)
- Detecting generic AI-generated design patterns
- Reviewing TSX/CSS/Tailwind source for design-token adherence

Do **not** use me for:
- Mechanical responsive breakpoint fixes (use `responsive-audit-subagent`)
- Full WCAG 2.1 AA compliance audits (use `accessibility-a11y-skill` directly)
- Creating new UI (use `frontend-design-skill`)
- Generating wireframes (use `wireframer-skill`)

---

## §1. Evidence-First Methodology

Every review follows this pipeline:

```
Capture → Structured Understanding → Specialized Review → Synthesis → QA Gate → Report
```

### The Gate Rule (Hard Constraint)

**Findings without an evidence reference (screenshot + viewport + selector) are rejected at the gate.**

A finding must include:
- A screenshot file path (or source file path + line range for code-only findings)
- The viewport at which the issue was observed (e.g., `mobile 375x812`)
- A CSS selector, DOM path, or component name locating the issue

Findings missing any of these are not included in the report. This prevents hallucinated issues from code-only inference and ensures every finding is verifiable.

### QA Gate

Before synthesis, every finding is checked:
1. Does it have an evidence reference? → If no, **reject**
2. Is the evidence vision-derived — a native multimodal read by the reviewer, `image-analyzer-subagent` output (for screenshots), or direct code inspection (for source)? → Visual claims with NO vision-derived backing (fabricated or code-inferred pixel claims), **reject**
3. Is the severity assignment consistent with the rubric? → If inconsistent, **reclassify**

Only findings passing all three checks reach the report.

---

## §2. Playwright Capture Protocol

For live URL targets, capture evidence in this order. The protocol borrows the `networkidle` wait discipline and reconnaissance-then-action pattern from [anthropics/skills/webapp-testing](https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md).

### Step 1: Navigate and Stabilize

```typescript
await page.goto(url, { waitUntil: 'networkidle' });
// Wait for any client-side hydration / lazy content
await page.waitForLoadState('networkidle');
```

`networkidle` is **critical** before any inspection — without it, screenshots capture partial renders and computed styles miss lazy-loaded values.

### Step 2: Capture at Three Breakpoints

| Breakpoint | Viewport | Use case |
|------------|----------|----------|
| Desktop | 1440 x 900 | Primary desktop review |
| Tablet | 768 x 1024 | iPad portrait, surface transitions |
| Mobile | 375 x 812 | iPhone size, touch-target checks |

For each breakpoint:
- Resize the viewport
- Wait for re-layout (`await page.waitForTimeout(500)` or `networkidle`)
- Capture above-the-fold screenshot
- Capture **full-page** screenshot for long pages (stitch if needed)

### Step 3: Accessibility Tree Snapshot

```typescript
const snapshot = await page.accessibility.snapshot();
// Serialize to JSON for review
```

Provides the semantic structure as a screen reader would perceive it — essential for axis 12 (Nielsen heuristic 4: consistency and standards) and accessibility basics (axis 10).

### Step 4: Computed-Style Extraction (Design Tokens)

Borrowed pattern from [component-census](https://github.com/somekiwiplease/component-census). Walk the DOM and extract:

| Token type | How to extract |
|------------|----------------|
| **Colors** | `getComputedStyle(el).color`, `backgroundColor`, `borderColor` — collect unique values |
| **Fonts** | `fontFamily`, `fontSize`, `fontWeight`, `lineHeight` |
| **Spacing** | `padding`, `margin`, `gap` values |
| **Radii** | `borderRadius` |
| **Shadows** | `boxShadow` |
| **Custom properties** | All CSS variables defined on `:root` and used values |

Deduplicate and produce a token inventory. Compare against the project's declared design tokens (Tailwind config, CSS variables, theme file). Drift = axis 4/8 finding.

### Step 5: Component Inventory

Group elements by visual similarity (buttons, CTAs, form inputs, nav items, cards, badges). Use clustering heuristics on computed styles. Surface inconsistencies (e.g., 5 different button heights).

---

## §3. The 13-Axis Review Rubric

The rubric combines four sources. Every axis has a concrete checklist with DOM/CSS verifiable items.

### Axes 1-6: Visual Design (adapted from AslanMazhidov/design-review-skill, MIT)

#### Axis 1 — Typography
- [ ] Size hierarchy: h1 → h2 → h3 → body shows clear contrast (rule of thumb: 1.25-1.5x scale)
- [ ] Line-height: 1.4-1.7 for long-form body text; tighter (1.1-1.3) for headings
- [ ] Line length: 50-75 characters for paragraphs (check `max-width` on text containers)
- [ ] Font pairing: max 2 typefaces; verify no accidental third font from imports
- [ ] Weight consistency: same heading level uses same weight across pages

#### Axis 2 — Color & Contrast
- [ ] WCAG AA contrast: body text ≥ 4.5:1 against background; large text (≥18pt or 14pt bold) ≥ 3:1
- [ ] Palette discipline: ≤ 3-4 accent colors beyond neutrals
- [ ] State visibility: hover, active, disabled, focus states are visually distinct
- [ ] Color independence: information is not conveyed by color alone (icons, text, patterns)
- [ ] Dark mode parity (if applicable): no hardcoded black-on-white assumptions

#### Axis 3 — Rhythm & Space
- [ ] Vertical rhythm: consistent spacing between related sections vs unrelated
- [ ] Section padding: predictable scale (8pt system: 8, 16, 24, 32, 48, 64)
- [ ] CTA breathing room: primary actions have clear surrounding whitespace
- [ ] Grouping: related items are closer than unrelated (Gestalt proximity)
- [ ] No "orphan" elements: last item of a group doesn't sit alone in next visual row

#### Axis 4 — Composition & Hierarchy
- [ ] Primary eye target matches primary message (verify via squint test on screenshot)
- [ ] F-pattern or Z-pattern legibility for content-heavy pages
- [ ] Proximity grouping: form fields with their labels, buttons with their actions
- [ ] Grid alignment: elements align to a shared grid; no off-by-a-few-pixels drift
- [ ] Visual weight distribution: balance left/right or intentional asymmetry

#### Axis 5 — Responsive
- [ ] No horizontal overflow on mobile (`scrollWidth > clientWidth` check)
- [ ] Mobile body font ≥ 14px (16px preferred)
- [ ] Touch targets ≥ 44 x 44 px (WCAG 2.5.5)
- [ ] Hero / above-the-fold not cropped or unreadable on mobile
- [ ] No unintended stacking order changes across breakpoints

#### Axis 6 — Polish
- [ ] Border-radius consistency (e.g., all cards use same radius)
- [ ] Natural shadow direction (consistent light source)
- [ ] Icon style and weight consistency (outline vs filled, line weight)
- [ ] Images not stretched (`object-fit` correct)
- [ ] No Lorem Ipsum or placeholder content in shipped UI
- [ ] Hover/focus micro-interactions present and consistent

### Axes 7-11: UX & Business (adapted from RNT56/design-review-workflow, PolyForm-NC — inspiration only)

#### Axis 7 — First Impression
- [ ] Above-fold hierarchy: user understands the page purpose within 5 seconds
- [ ] Immediate comprehension: headline answers "what is this?"
- [ ] CTA clarity: primary action is obvious
- [ ] Visual priority: most important element has highest visual weight

#### Axis 8 — UX/Navigation
- [ ] Page classification: page type is identifiable (landing, app, form, list, detail)
- [ ] Navigation clarity: user knows where they are in the site/app structure
- [ ] Route inventory: all paths from this page are discoverable
- [ ] Repeated section patterns: consistent header/footer/nav across pages
- [ ] Breadcrumbs or back buttons where appropriate

#### Axis 9 — Conversion & Trust
**Apply only when target is marketing, landing, or conversion surface. Skip for internal tools, admin panels, or purely functional UI.**

- [ ] Proof: testimonials, case studies, metrics visible
- [ ] Reassurance: guarantees, return policies, security badges
- [ ] Portfolio narrative: work examples accessible
- [ ] Service persuasion: value proposition stated clearly
- [ ] Contact paths: easy access to human contact
- [ ] Risk reduction: free trial, demo, money-back signals

#### Axis 10 — Accessibility Basics
**Deep dives delegate to `accessibility-a11y-skill`. This axis is a surface scan only.**

- [ ] axe-core-style automated checks pass (run via Playwright if available)
- [ ] All images have `alt` text (or intentional empty alt for decorative)
- [ ] Form inputs have associated labels
- [ ] Color contrast samples pass (overlaps with axis 2)
- [ ] Findings link to specific elements via evidence refs

#### Axis 11 — Performance Perception
- [ ] Loading states visible for async operations
- [ ] Skeleton screens or spinners for >200ms operations
- [ ] Browser navigation timing in acceptable range
- [ ] No layout shift (CLS) after initial render
- [ ] Images use lazy loading where appropriate

### Axis 12: Nielsen's 10 Heuristics (Gap-Fill — not in any existing skill)

Each heuristic mapped to concrete DOM/CSS checks.

| # | Heuristic | DOM/CSS verification |
|---|-----------|----------------------|
| 1 | Visibility of system status | Loading indicators present for async; save confirmation visible; active nav item styled distinctly; form submission shows pending state |
| 2 | Match between system and real world | Labels use user language not developer jargon; error messages avoid stack-trace language; icons are universally recognizable |
| 3 | User control and freedom | Undo available for destructive actions; cancel buttons on multi-step flows; back button works; escape closes modals |
| 4 | Consistency and standards | Same component looks same everywhere; design tokens used (not hardcoded values); follows platform conventions (e.g., primary action right-aligned on desktop) |
| 5 | Error prevention | Confirm dialogs before destructive actions; input validation before submit; disabled state for invalid forms; autocomplete on appropriate fields |
| 6 | Recognition rather than recall | Options visible (not hidden in dropdowns unless >7); placeholders paired with persistent labels; recently used items surfaced |
| 7 | Flexibility and efficiency of use | Keyboard shortcuts available; smart defaults pre-filled; frequent actions accessible in ≤2 clicks |
| 8 | Aesthetic and minimalist design | Signal-to-noise ratio high; no decorative elements competing with content; whitespace intentional not accidental |
| 9 | Help users recognize, diagnose, recover from errors | Error messages state what happened in plain language; suggest a fix; don't blame the user; field-level errors not just form-level |
| 10 | Help and documentation | Contextual help icons where needed; onboarding for first-time use; help searchable |

### Axis 13: Anti-Default AI Design Detection (Gap-Fill — sourced from anthropics/skills/frontend-design, Apache 2.0)

Flag the six "generic AI design clusters" that signal unmodified AI output. None are inherently wrong — but their presence without intentional variation suggests the UI was generated and not designed. An explicit brief request for the look is a valid brand reason — note it in the finding rather than flagging it as a defect.

#### Cluster A — Cream + Serif
- Background: warm cream / off-white (`#fdfcf7`, `#faf8f1`, `#F4F1EA` family)
- Type: serif headlines (Playfair Display, EB Garamond, Cormorant)
- Body: clean sans-serif
- Accent: terracotta / warm clay (`#D97757` — an AI vendor's own interaction color)
- Visual signal: editorial / boutique aesthetic
- **Flag if**: combo used without obvious brand reason

#### Cluster B — Dark + Acid Green / Vermilion / Violet
- Background: near-black or tinted near-black (`#0B0B0B`, `#111`)
- Accent: neon/acid green (`#00ff88`, `#22c55e` family), vermilion, or electric violet (`#8b5cf6`, `#a855f7`)
- Type: geometric sans-serif (Inter, Geist)
- Monospace accents for "tech" feel
- **Flag if**: tech aesthetic without warmth or brand differentiation

#### Cluster C — Broadsheet / Newspaper
- Layout: multi-column grid, dense text blocks
- Heavy horizontal rules, zero border-radius
- Serif type, often Times-like
- Justified text alignment
- **Flag if**: news metaphor doesn't match product purpose

#### Cluster D — SaaS-card kit
- Content chopped into identical rounded cards, one border-radius on everything regardless of hierarchy
- Same soft shadow (`rgba(0,0,0,.1)`) under each card; gradient washes as decoration
- **Flag if**: hierarchy flattened into uniform tiles without a card-metaphor reason

#### Cluster E — Template chrome
- ALL-CAPS tracked eyebrow labels above every heading
- Meta strings joined with middle-dot separators (`A · B · C`); labels built as `WORD — fragment` with a spaced em dash
- Monospace for small data labels; `→` appended to link and button text
- **Flag if**: chrome appears regardless of subject — decoration instead of encoded information

#### Cluster F — Default hero
- Opening move: big number + small label + supporting stats + gradient accent
- **Flag if**: the hero recites this template instead of opening with the subject's most characteristic element

**Disposition**: findings under axis 13 are typically Minor (NOTE) unless the AI-cluster aesthetic actively harms usability. Phrase findings as observations, not blockers: "UI follows the dark+acid-green cluster (axis 13B) — consider whether this aligns with brand intent or is unmodified AI output."

---

## §4. Finding Schema

Every finding is structured for machine parsing. Use this exact field set.

```yaml
target:
  url: <string, optional — for live URL findings>
  file: <string, optional — for source findings, path:lines>
  viewport: <enum: desktop 1440x900 | tablet 768x1024 | mobile 375x812 | source-only>
  selector: <string — CSS selector, DOM path, or component name>
axis: <integer 1-13>
observation: <string — what is observed, factual>
impact: <string — user or business consequence>
recommendation: <string — specific CSS class, structural change, or design-token value>
severity: <enum: Critical | Major | Minor>
evidence:
  screenshot: <string — file path>
  match_index: <integer — 0-based, for screenshots with multiple matches>
confidence: <enum: High | Medium | Low>
```

### Field constraints
- `severity` MUST be one of: `Critical`, `Major`, `Minor` (no other values)
- `confidence` MUST be one of: `High`, `Medium`, `Low`
- `axis` MUST be an integer 1-13
- Either `url` or `file` is required; both may be present
- `evidence.screenshot` is required for visual findings; may be omitted for source-only findings (with `viewport: source-only`)
- `selector` is always required — no finding without a locatable target

### Example finding (Critical)

```yaml
target:
  url: https://example.com/login
  viewport: mobile 375x812
  selector: "input[name='password']"
axis: 10
observation: "Password input has no associated <label> element; placeholder is used as the only label."
impact: "Screen readers announce the field as 'unlabeled'; password autofill may fail; WCAG 2.1 Level A failure (1.3.1 Info and Relationships)."
recommendation: "Add <label for='password'>Password</label> above the input; keep placeholder as hint text. Reference: accessibility-a11y-skill for full label patterns."
severity: Critical
evidence:
  screenshot: /tmp/uiux-review/login-mobile.png
  match_index: 0
confidence: High
```

### Example finding (Minor)

```yaml
target:
  file: src/components/Button.tsx:42
  viewport: source-only
  selector: "<Button variant='secondary'>"
axis: 6
observation: "Secondary button uses border-radius: 6px; primary uses 8px. Inconsistent radius across button variants."
impact: "Minor visual inconsistency; users may not consciously notice but the UI feels less polished."
recommendation: "Standardize on a single radius token, e.g., --radius-button, and apply to both variants."
severity: Minor
evidence: {}
confidence: High
```

---

## §5. Severity Rubric

The severity determines downstream action.

| Severity | Qualification | Disposition | Example |
|----------|---------------|-------------|---------|
| **Critical** | Accessibility blocker (WCAG A failure), broken core task flow, unreadable content, destructive action without confirmation | **BLOCK** — must fix before release | Password field with no label; checkout button does nothing; body text 3:1 contrast |
| **Major** | Significant UX friction, design-system violation, heuristic 1/3/4/5/6/9 failure, inconsistent component patterns | **WARN** — should fix, can defer with TODO + ticket | Form with no validation; buttons with 5 different heights; nav item doesn't show active state |
| **Minor** | Polish issues, spacing inconsistencies, minor typography tweaks, axis 13 AI-cluster observations | **NOTE** — good to know | Border-radius drift 6px vs 8px; line-height 1.38 instead of 1.4; cream+serif cluster without brand reason |

### Severity vs Confidence

Severity and confidence are independent:
- **Severity** = how bad the issue is
- **Confidence** = how sure the reviewer is that the issue is real

A Critical finding with Low confidence is still Critical — it just means the reviewer should request more evidence before acting.

---

## §6. References

This skill adapts patterns from the following open-source projects. No code was copied from PolyForm-NC sources; they are credited as design inspiration only.

| Source | License | What we adapted |
|--------|---------|-----------------|
| [AslanMazhidov/design-review-skill](https://github.com/AslanMazhidov/design-review-skill) | MIT | Axes 1-6 (typography, color/contrast, rhythm/space, composition/hierarchy, responsive, polish); "never guess from code" rule; Playwright capture at 3 breakpoints |
| [RNT56/design-review-workflow](https://github.com/RNT56/design-review-workflow) | PolyForm Noncommercial 1.0.0 | **Inspiration only — no code copied.** Evidence-first architecture; axes 7-11 (first impression, UX/navigation, conversion & trust, accessibility basics, performance perception); finding schema with evidence references; QA gate concept |
| [anthropics/skills — frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | Apache 2.0 | Axis 13 anti-default AI design cluster detection (cream+serif, dark+acid-green, broadsheet); self-critique discipline |
| [anthropics/skills — webapp-testing](https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md) | Apache 2.0 | `networkidle` wait before capture; reconnaissance-then-action Playwright pattern (§2) |
| [somekiwiplease/component-census](https://github.com/somekiwiplease/component-census) | MIT | Design-token extraction pattern (colors, fonts, spacing, radii, shadows) in §2 Step 4; component inventory by visual similarity |

### Attribution summary

- **Axes 1-6**: AslanMazhidov (MIT)
- **Axes 7-11**: RNT56 (PolyForm-NC — inspiration only)
- **Axis 12** (Nielsen's heuristics mapping): Original gap-fill — not present in any single existing skill
- **Axis 13** (AI cluster detection): Anthropic frontend-design (Apache 2.0)
- **Playwright protocol**: Synthesized from AslanMazhidov + Anthropic webapp-testing + component-census
- **Finding schema**: Adapted from RNT56 (PolyForm-NC — inspiration only)
- **Severity rubric**: Original, aligned with `code-review-subagent` conventions

## Related Skills

- **frontend-design-skill**: Peer — creates new UI; this skill reviews existing UI
- **accessibility-a11y-skill**: Deep-dive delegation target for axis 10 surface findings
- **wireframer-skill**: Produces baselines for structural drift comparison
- **civiltekk-react-quality-skill** (routes `hooks-antipatterns` + `render-antipatterns`): Source for axis 12 (Nielsen heuristic 4) findings in React/Next.js projects
