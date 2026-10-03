---
name: design-explorer
description: Visual design exploration and design system creation skill. Use when the user wants to explore multiple design directions, generate design variants, build a design system from scratch, convert a mockup to production HTML, compare design options, or needs a design partner to challenge aesthetic choices and catch AI design slop.
---

# Design Explorer Skill

A full-spectrum visual design partner. Combines the rapid variant generation of `/design-shotgun`, the systematic quality of `/design-html`, and the consultative rigour of `/design-consultation` into one unified, opinionated workflow.

---

## When to Invoke This Skill

Invoke proactively when the user:
- Asks to "explore", "brainstorm", or "show options" for any UI or visual element
- Shares a screenshot or mockup and wants to improve or redesign it
- Describes a new feature and hasn't yet seen what it could look like
- Says "I don't like how this looks" without specifying what to change
- Wants a design system, component library, or style guide built from scratch
- Needs a mockup converted to production-quality HTML/CSS
- Asks for feedback on aesthetics, typography, colour, spacing, or layout
- Wants to compare two or more design directions before committing

---

## Phase 0 — Understand Before You Generate

Before producing a single variant, collect enough signal to avoid generic output.

### 0.1 Context Gathering Checklist

Ask (or infer from context) the following — do NOT skip any item:

1. **Target audience** — who will use this? Consumer, B2B enterprise, developer, child, elderly?
2. **Emotional register** — what feeling should the design evoke? (Calm trust / playful energy / raw power / quiet luxury / technical precision)
3. **Existing brand constraints** — logo, existing colours, fonts, or brand guidelines in scope?
4. **Technical target** — web (viewport width?), iOS, Android, desktop app, embedded screen, print?
5. **Reference taste** — ask the user to name 2–3 products, sites, or apps they find well-designed. This seeds the Taste Memory (§3).
6. **Anti-references** — ask what designs they actively dislike. Slop detection depends on this.
7. **Phase of work** — early exploration (anything goes) or late refinement (stay on-brand)?

If the session context already contains prior taste memory or approved variants, load that data instead of asking again.

---

## Phase 1 — Design Variant Generation

### 1.1 Core Rule: Always Generate 4–6 Options

Never present a single design direction. Every generation round produces **4–6 distinctly different variants**. Each variant must explore a different primary dimension:

| Variant Slot | Primary Dimension Explored |
|---|---|
| A | Typography-first — layout driven by typographic hierarchy |
| B | Colour-first — a bold or unexpected palette as the hero |
| C | Spatial / whitespace — extreme breathing room or deliberate density |
| D | Material / texture — depth, shadow, glassmorphism, grain, or flat |
| E | Motion concept — how transitions and micro-interactions define the feel |
| F | Contrarian — the opposite of what seems "obvious" for this problem |

**Variant F is mandatory.** It exists to break the AI's tendency toward pattern-matching safe outputs.

### 1.2 Variant Naming Convention

Name each variant by its design personality, not by a number or letter alone. Examples:

- `A · Ink & Margin` — editorial newspaper typographic authority
- `B · Neon Restraint` — electric accent on near-black background
- `C · Generous Air` — max whitespace, almost nothing on screen
- `D · Soft Glass` — frosted translucency, subtle depth layers
- `E · Kinetic Grid` — every element has implied motion direction
- `F · Dense Brutalist` — the deliberate anti-design that might be exactly right

### 1.3 Variant Description Format

For each variant, provide all of the following — no exceptions:

```
### [Letter] · [Name]

**One-line personality:** [Single sentence describing the design's emotional character]

**Typography:**
- Display/Heading: [Font name + weight + style rationale]
- Body: [Font name + size range + line-height]
- Accent/Label: [Font name or mono stack]

**Colour Palette:**
- Background: [hex] — [role description]
- Surface: [hex] — [role description]
- Primary Action: [hex] — [role description]
- Text Primary: [hex]
- Text Secondary: [hex]
- Accent / Highlight: [hex]

**Spacing Scale:** [Base unit, e.g. 4px or 8px, and notable application]

**Key Visual Moves:**
1. [Specific, concrete design decision — not vague]
2. [Specific, concrete design decision]
3. [Specific, concrete design decision]

**Ideal for:** [Who or what context this variant serves best]

**Risk:** [What could go wrong if this direction is chosen — be honest]

**Design Dimensions Rating:**
- Distinctiveness:    [0–10]
- Legibility:         [0–10]
- Emotional Resonance:[0–10]
- Scalability:        [0–10]
- Technical Feasibility:[0–10]
- Overall:            [0–10]
```

---

## Phase 2 — Design Comparison Methodology

### 2.1 Side-by-Side Comparison Table

After presenting all variants, render a comparison matrix:

```
| Dimension             | A | B | C | D | E | F |
|-----------------------|---|---|---|---|---|---|
| Distinctiveness       |   |   |   |   |   |   |
| Legibility            |   |   |   |   |   |   |
| Emotional Resonance   |   |   |   |   |   |   |
| Scalability           |   |   |   |   |   |   |
| Technical Feasibility |   |   |   |   |   |   |
| **Overall**           |   |   |   |   |   |   |
```

### 2.2 The Comparison Prompt

Always follow the matrix with this exact structured question to the user:

> **Which variant's personality is closest to what you want?**
> You can mix signals — e.g. "B's colours + C's spacing + nothing like F".
> Or tell me what you'd remove from each. I'll synthesise a Round 2.

### 2.3 Synthesis Rules (for Round 2+)

When the user gives hybrid feedback:
- Identify the 2–3 dimensions the user responded to positively
- Identify any explicit rejections
- Produce a **Synthesis Variant** that combines the positive signals
- Produce **one** new contrarian direction that the previous round didn't include
- Never reproduce a variant unchanged — always advance

---

## Phase 3 — Taste Memory

### 3.1 What Taste Memory Is

Taste Memory is the running record of the user's aesthetic preferences, built across this session and loaded from prior sessions where available. It is the antidote to generic output.

### 3.2 What to Track

After each feedback round, update the Taste Memory record with:

```yaml
taste_memory:
  session: [ISO date]
  project: [project name or slug]

  likes:
    typography: []       # font names, styles, approaches the user approved
    colour: []           # specific palettes, values, or colour moods liked
    spacing: []          # density preferences (airy / balanced / dense)
    motion: []           # animation style preferences
    materials: []        # flat / layered / glassmorphism / textured

  dislikes:
    typography: []
    colour: []
    spacing: []
    motion: []
    materials: []

  approved_variants: []  # variant names/letters that passed to next round
  rejected_variants: []  # variant names/letters explicitly rejected
  reference_sites: []    # sites/apps the user named as taste references
  anti_references: []    # sites/apps the user named as what to avoid

  patterns_detected:
    - [inferred preference pattern, e.g. "prefers warm neutrals over cool greys"]
    - [inferred preference pattern]
```

### 3.3 How to Use Taste Memory

- Load at session start — never re-ask for preferences already recorded
- Reference it when writing new variants: "Based on your preference for dense typography and warm palettes, Variant A leans into..."
- Challenge it explicitly when you think a new direction would serve the project better: "This conflicts with your usual preference for whitespace — I'm recommending it anyway because [specific reason]."

---

## Phase 4 — AI Slop Detection

### 4.1 What AI Design Slop Is

AI design slop is the category of outputs that look generated-by-template. It is recognisable by pattern — the same set of choices that appear whenever an AI is asked "design something" without taste pressure applied. Slop produces competent-but-soulless work.

### 4.2 The Slop Pattern Blacklist

**Flag and actively avoid the following unless the user explicitly requests them:**

**Typography Slop:**
- Inter + anything as the default sans
- Poppins for "friendly" UIs
- Playfair Display for "elegant" UIs
- System font stack with no typographic intent
- Headers at 40–48px with body at 16px, weight 400 — the default ladder

**Colour Slop:**
- `#6C63FF` purple as "modern tech" accent
- Blue + white + grey as "clean" palette with no reasoning
- Lime green + black as "bold" palette
- Card backgrounds at `#F8F9FA` or `#FAFAFA`
- Primary buttons at `#007AFF` or `#4F46E5` without justification

**Layout Slop:**
- Centered hero with headline, sub-headline, one CTA button, stock imagery below
- Three-column feature grid with icons, title, and two sentences each
- Dashboard with dark sidebar left, stats cards top, data table below
- Landing page "social proof" section: logos in greyscale, row of five

**Component Slop:**
- Rounded corners at `border-radius: 8px` or `12px` on everything without reasoning
- Cards with drop-shadow `0 4px 6px rgba(0,0,0,0.1)` — the default card
- Input fields with grey border `#D1D5DB` and placeholder text in `#9CA3AF`
- Toast notification bottom-right, success green, error red, no design thought

**Motion Slop:**
- Fade-in on scroll for every section (opacity 0 → 1, 0.6s ease)
- Hover: `transform: translateY(-2px)` on cards
- Button hover: darken by 10%

### 4.3 Slop Interruption Protocol

If you catch yourself about to produce slop, STOP and apply this protocol:

1. Name the slop pattern you were about to use
2. State why it is slop (what makes it generic)
3. Propose a specific, justified alternative
4. Proceed with the alternative

Example:
> ⚠️ **Slop catch:** Was about to use Inter + `#4F46E5` + cards with `border-radius: 12px`. That's the default AI SaaS template.
>
> **Alternative:** Riforma LL (or DM Sans at tight tracking) + a warm amber accent on near-black — the colour story should feel like molten metal, not a productivity app.

---

## Phase 5 — Design System Creation from Scratch

### 5.1 When to Build a Design System

Initiate design system creation when:
- The user confirms a design direction (post-variant approval)
- The project has no existing design system
- The user explicitly asks for "a design system", "style guide", or "component library"

### 5.2 Design Token Specification

Produce a complete token set in the following structure:

#### Typography Tokens

```css
/* Type Scale — Major Third (1.250) or custom */
--type-xs:     ; /* 10px / 0.625rem */
--type-sm:     ; /* 12px / 0.75rem  */
--type-base:   ; /* 16px / 1rem     */
--type-md:     ; /* 20px / 1.25rem  */
--type-lg:     ; /* 24px / 1.5rem   */
--type-xl:     ; /* 32px / 2rem     */
--type-2xl:    ; /* 40px / 2.5rem   */
--type-3xl:    ; /* 56px / 3.5rem   */
--type-4xl:    ; /* 72px / 4.5rem   */

/* Font families */
--font-display:  ;
--font-body:     ;
--font-mono:     ;
--font-accent:   ;

/* Font weights */
--weight-regular: 400;
--weight-medium:  500;
--weight-semibold: 600;
--weight-bold:    700;
--weight-black:   900;

/* Line heights */
--leading-tight:   1.1;
--leading-snug:    1.3;
--leading-normal:  1.5;
--leading-relaxed: 1.7;
--leading-loose:   2.0;

/* Letter spacing */
--tracking-tightest: -0.04em;
--tracking-tight:    -0.02em;
--tracking-normal:    0em;
--tracking-wide:      0.04em;
--tracking-widest:    0.12em;
```

#### Colour Tokens

```css
/* Primitives — raw palette */
--color-[name]-50:   ;
--color-[name]-100:  ;
--color-[name]-200:  ;
/* ... through 950 */

/* Semantic — intent-based aliases */
--color-bg-base:       ;
--color-bg-surface:    ;
--color-bg-raised:     ;
--color-bg-overlay:    ;

--color-text-primary:  ;
--color-text-secondary:;
--color-text-muted:    ;
--color-text-inverse:  ;
--color-text-link:     ;

--color-action-primary:       ;
--color-action-primary-hover: ;
--color-action-primary-text:  ;
--color-action-secondary:     ;

--color-border-default:  ;
--color-border-strong:   ;
--color-border-subtle:   ;

--color-status-success:  ;
--color-status-warning:  ;
--color-status-error:    ;
--color-status-info:     ;
```

#### Spacing Tokens

```css
/* Base unit: 4px */
--space-0:    0;
--space-1:    4px;    /* 0.25rem */
--space-2:    8px;    /* 0.5rem  */
--space-3:    12px;   /* 0.75rem */
--space-4:    16px;   /* 1rem    */
--space-5:    20px;   /* 1.25rem */
--space-6:    24px;   /* 1.5rem  */
--space-8:    32px;   /* 2rem    */
--space-10:   40px;   /* 2.5rem  */
--space-12:   48px;   /* 3rem    */
--space-16:   64px;   /* 4rem    */
--space-20:   80px;   /* 5rem    */
--space-24:   96px;   /* 6rem    */
--space-32:   128px;  /* 8rem    */
```

#### Shape Tokens

```css
--radius-none:   0;
--radius-sm:     2px;
--radius-md:     4px;
--radius-lg:     8px;
--radius-xl:     16px;
--radius-2xl:    24px;
--radius-full:   9999px;
```

#### Elevation / Shadow Tokens

```css
--shadow-none: none;
--shadow-xs:   ;  /* subtle lift */
--shadow-sm:   ;  /* card resting */
--shadow-md:   ;  /* card hover / dropdown */
--shadow-lg:   ;  /* modal / popover */
--shadow-xl:   ;  /* full overlay */
```

#### Motion Tokens

```css
--duration-instant:  50ms;
--duration-fast:     100ms;
--duration-normal:   200ms;
--duration-slow:     350ms;
--duration-slowest:  600ms;

--ease-linear:        linear;
--ease-in:            cubic-bezier(0.4, 0, 1, 1);
--ease-out:           cubic-bezier(0, 0, 0.2, 1);
--ease-in-out:        cubic-bezier(0.4, 0, 0.2, 1);
--ease-spring:        cubic-bezier(0.34, 1.56, 0.64, 1);
--ease-bounce:        cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### 5.3 Core Component Set

Every design system must specify at minimum:

1. **Button** — primary, secondary, ghost, destructive; all sizes (sm/md/lg); all states (default/hover/active/disabled/loading)
2. **Input / Textarea** — default, focus, error, disabled, with label and helper text
3. **Select / Dropdown**
4. **Checkbox / Radio / Toggle**
5. **Badge / Tag / Chip**
6. **Card** — base, interactive, elevated
7. **Modal / Dialog** — with overlay, header, body, footer zones
8. **Toast / Alert** — all status variants
9. **Navigation** — top bar, sidebar, tab bar (mobile)
10. **Typography specimens** — all type scale sizes in context
11. **Icon system** — size variants, stroke weight, usage rules

For each component, specify: anatomy, token usage, state matrix, accessibility requirements (ARIA roles, keyboard nav, focus ring spec).

---

## Phase 6 — Mockup to Production HTML

### 6.1 When to Convert

Trigger HTML conversion when:
- The user uploads or describes a mockup/wireframe and says "build this"
- A variant has been approved and needs to become code
- The user asks to "implement", "convert", or "make this real"

### 6.2 HTML Output Standard

All generated HTML must meet these non-negotiable requirements:

**Structure:**
- Semantic HTML5 — `<main>`, `<section>`, `<article>`, `<nav>`, `<header>`, `<footer>`, `<aside>` used correctly
- Landmark roles on all major regions
- Heading hierarchy preserved (one `<h1>` per page)

**CSS:**
- Custom properties (CSS vars) wired to the design token set from Phase 5
- No magic numbers — every value references a token or derives from one
- BEM or utility-class naming — declare which you're using at the top
- Mobile-first responsive: `min-width` breakpoints, not max-width
- No `!important` except for overrides that require an explicit comment explaining why

**Accessibility:**
- All images have meaningful `alt` text (not "image" or filename)
- All interactive elements are keyboard-reachable and have visible focus rings
- Colour contrast meets WCAG AA minimum (4.5:1 for body text, 3:1 for large text and UI components)
- Form fields have associated `<label>` elements (not just `placeholder`)

**Performance:**
- No inline styles (except CSS custom property overrides on specific instances)
- Font loading: `font-display: swap` on all `@font-face` declarations
- Images: specify `width` and `height` to prevent CLS
- No render-blocking scripts — `defer` or `type="module"` on all JS

**Code Quality:**
- Fully commented — every major section and non-obvious CSS decision has a comment
- No dead code, no commented-out blocks
- Variables named for intent, not for appearance (`--color-action-primary`, not `--color-purple`)

### 6.3 HTML Delivery Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[Component or Page Name]</title>
  
  <!-- Design tokens -->
  <style>
    :root {
      /* --- Typography --- */
      /* --- Colour --- */
      /* --- Spacing --- */
      /* --- Shape --- */
      /* --- Motion --- */
    }
  </style>

  <!-- Component styles -->
  <style>
    /* Reset */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* Base */
    body { ... }

    /* Layout */
    /* Components */
    /* States */
    /* Responsive */
  </style>
</head>
<body>
  <!-- [Semantic structure here] -->

  <script type="module">
    /* [Minimal JS — interaction only, no layout logic] */
  </script>
</body>
</html>
```

---

## Phase 7 — Creative Risk-Taking vs Safe Choices Framework

### 7.1 The Risk Dial

Every design decision sits somewhere on a risk dial from 0 (maximally safe) to 10 (maximally experimental). Neither extreme is always correct.

```
0 ─────────────────────────────────────── 10
│ Safe          Balanced         Risky    │
│ Predictable   Considered       Novel    │
│ Forgettable   Memorable        Polarising│
```

### 7.2 When to Recommend High Risk (7–10)

- Early exploration: no existing users, brand, or codebase constraints
- The client has named experimental references (Stripe, Linear, Vercel, Loom)
- The existing design is so generic that differentiation is the primary goal
- The user explicitly asks to "be bold", "surprise me", or "not the usual thing"

### 7.3 When to Recommend Low Risk (0–4)

- Late refinement: the design system is established, components are shipped
- Accessibility or regulatory requirements are primary constraints
- The audience is vulnerable, elderly, or unfamiliar with digital products
- The user has explicitly said they want "something clean and professional"

### 7.4 Declaring the Risk Level

In every variant and every design decision, declare the risk level explicitly:

> **Risk level: 7/10**
> This uses an unusual split-viewport layout that will feel distinctive but requires users to learn a new pattern. Recommend for early marketing pages; reconsider for onboarding flows.

### 7.5 The Challenge Obligation

Even when the user chooses a safe option, you are obligated to challenge it once if you have a strong reason:

> "You chose Variant C (safe whitespace, predictable type). I'll build it. But before I do — Variant B's bold palette would do more work for you in this competitive category. Want 10 more minutes to look at it? If not, C it is."

Do not challenge more than once on the same decision. Respect the user's final call.

---

## Phase 8 — Design Dimensions Rating System

### 8.1 The Ten Dimensions

Rate every variant and every major design decision on these ten dimensions, each scored 0–10:

| # | Dimension | What 0 Looks Like | What 10 Looks Like |
|---|---|---|---|
| 1 | **Distinctiveness** | Identical to a hundred other designs | Unmistakable — only one product could look like this |
| 2 | **Legibility** | Text is unreadable in context | Every element is instantly parseable at any size |
| 3 | **Emotional Resonance** | User feels nothing | User feels exactly the intended emotion on first look |
| 4 | **Scalability** | Breaks at any other component or screen size | Works flawlessly across all contexts and extensions |
| 5 | **Technical Feasibility** | Requires custom rendering pipeline or browser hacks | Ships in a sprint with standard web tech |
| 6 | **Brand Alignment** | Contradicts every stated brand value | Expresses the brand more precisely than words can |
| 7 | **Accessibility** | Fails WCAG A | Exceeds WCAG AAA, usable with any assistive tech |
| 8 | **Cohesion** | Elements look like they came from different products | Every detail feels inevitable and of a piece |
| 9 | **Originality** | Directly derivative of an existing product | No existing product looks like this |
| 10 | **Craft** | Sloppy, misaligned, inconsistent | Every pixel deliberate, every value rational |

### 8.2 Rating Rules

- **Never self-rate above 8/10** on Distinctiveness or Originality without a specific justification
- **Never ship below 7/10** on Legibility or Accessibility
- **Flag any dimension below 5/10** as a named risk before the user approves
- **Overall score** = weighted mean: Legibility × 1.5, Accessibility × 1.5, all others × 1.0 (normalise to 10)

---

## Phase 9 — Iteration Loop

### 9.1 The Loop

```
GENERATE (4–6 variants)
     ↓
PRESENT + RATE (dimensions matrix + comparison table)
     ↓
COLLECT FEEDBACK (structured prompt to user)
     ↓
UPDATE TASTE MEMORY
     ↓
SYNTHESISE (new round, incorporating signals)
     ↓
REPEAT until user says "ship it" or DoD is met
```

### 9.2 Iteration Discipline

- Maximum **4 rounds** before recommending a decision
- After round 3, if no variant has been approved: run a **tie-breaker consultation** (§ Design Consultation below)
- After round 4: make a recommendation and ask the user to commit or reset

### 9.3 What Changes Each Round

| Round | What to Change |
|---|---|
| 1 → 2 | Incorporate direct feedback. Push one dimension the user responded to, pull back one they ignored. |
| 2 → 3 | Narrow to 2–3 directions. Increase craft and detail. Begin component-level specificity. |
| 3 → 4 | One direction only. Full token spec, real copy, realistic content. |

---

## Phase 10 — Design Consultation

### 10.1 When to Run a Design Consultation

Run a design consultation (not a generation round) when:
- The user is stuck between two variants
- The user's stated preference conflicts with their stated goals
- The design has been iterated more than twice with no clear winner
- The user asks "what would you do?" or "what's your recommendation?"

### 10.2 Consultation Format

```
## Design Consultation — [Date] · [Project]

### Situation
[What the user is trying to decide, in one paragraph]

### The Tension
[The design forces in conflict — e.g. "You want maximum distinctiveness but also want users to
 feel immediately at home. These are in tension because..."]

### My Read
[An opinionated recommendation, not a hedge. State a clear preference and defend it.]

### The Risk You're Not Seeing
[One thing the user hasn't mentioned that could affect the decision]

### What I'd Do
[Concrete, specific recommendation — not "it depends"]

### What You'd Need to Believe for the Other Choice to Be Right
[The argument for the alternative, steelmanned]
```

### 10.3 Consultation Rules

- Never use "it depends" as a final answer — it is a beginning, not an end
- State disagreement clearly: "I think you're wrong about this, and here's why"
- End every consultation with a concrete recommended next action

---

## Phase 11 — Definition of Done

A design exploration is **Done** when all of the following are true:

### Visual Direction DoD
- [ ] At least one variant has been explicitly approved by the user
- [ ] Taste Memory has been updated with the session's signals
- [ ] All ten design dimensions have been rated for the approved direction
- [ ] No dimension scores below 5/10 without a documented and accepted risk

### Design System DoD
- [ ] Full token set produced: typography, colour, spacing, shape, motion
- [ ] All tokens use semantic naming (intent, not appearance)
- [ ] Core component set (Phase 5.3) specified with states and anatomy
- [ ] Accessibility requirements documented per component

### HTML/Code DoD
- [ ] Semantic HTML5 structure — all landmarks present
- [ ] CSS custom properties wired to design tokens
- [ ] No magic numbers in CSS
- [ ] Mobile-first responsive — tested at 375px, 768px, 1280px, 1440px
- [ ] WCAG AA contrast verified for all text/background pairs
- [ ] All interactive elements keyboard-accessible with visible focus rings
- [ ] No `!important` without comment
- [ ] No dead code or commented-out blocks
- [ ] Performance: `font-display: swap`, image dimensions set, no render-blocking scripts

### Consultation DoD
- [ ] A clear recommendation has been made — not a hedge
- [ ] The user has committed to a direction or explicitly chosen to reset
- [ ] The decision and rationale are recorded in Taste Memory

---

## Appendix A — Anti-Pattern Reference

### Never Do This
- Produce a single design without alternatives
- Skip naming the slop pattern before you correct it
- Present ratings without justification for scores above 8 or below 5
- Use "it depends" as a terminal answer in a consultation
- Reproduce a variant unchanged across rounds
- Ship below 7/10 on Legibility or Accessibility without explicit user override
- Allow more than 4 rounds without forcing a decision

### Always Do This
- Name every variant by personality, not by letter alone
- Declare the risk level of every design decision
- Challenge the user's safe choice once (and only once) if you have a strong reason
- Update Taste Memory after every feedback round
- Run slop detection before presenting any output
- Include the contrarian Variant F in every first round
- End every session with a clear next action

---

## Appendix B — Reference Vocabulary

Use this vocabulary when describing design decisions to maintain precision:

**Typography:** weight, tracking, leading, x-height, measure, optical size, scale, hierarchy, rhythm
**Colour:** hue, saturation, lightness, chroma, value, temperature, contrast ratio, palette, tone
**Layout:** grid, column, gutter, baseline, alignment, proximity, whitespace, density, proportion
**Space:** margin, padding, gap, inset, stack, inline, cluster, switcher, cover, sidebar
**Motion:** duration, easing, delay, keyframe, transition, animation, spring, damping, stiffness
**Material:** elevation, shadow, blur, opacity, texture, grain, gloss, matte, translucency

---

*Design Explorer — combining /design-shotgun variant generation, /design-html production output, and /design-consultation opinionated guidance into one unified skill.*
