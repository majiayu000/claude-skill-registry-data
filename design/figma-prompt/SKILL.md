---
name: figma-prompt
description: Generate a complete Figma Make prompt package — Context Primer, Checkpoint, Section Build Prompts, and Iteration Templates — for any UI page, component, or screen. Uses intent-first prompting and Figma-native vocabulary. Counterpart to the studio-prompt skill, tuned for design artifacts rather than working code.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep
---

Generate a complete Figma Make prompt package for: $ARGUMENTS

$ARGUMENTS should include:
- What you want to design (e.g., "course detail page", "a checkout flow", "an analytics dashboard", "the homepage hero")
- Optionally: business context ("needs to convert visitors to enrolled students")
- Optionally: visual direction ("warm and scholarly", "clean and developer-focused")
- Empty — ask the user what they want to design

---

## When to Use This Skill vs `/studio-prompt`

| Use Figma prompt when… | Use studio-prompt when… |
|------------------------|-------------------------|
| You want a Figma design file for review, handoff, or client presentation | You want a working, deployable React/Next.js app |
| You're exploring visual direction before committing to code | You need real interactivity and data binding |
| The output needs to live in Figma for stakeholder review | The output needs to be run in a browser |
| You want high-fidelity visual polish with frames, layers, and component structure | You want functional code |

**Key difference:** Figma Make outputs Figma frames — visual design artifacts with layers, components, and prototype connections. It does not output deployable code. The studio-prompt skill outputs React + Tailwind components ready to copy into a codebase.

---

## Critical Workflow Difference: No System Instructions

Unlike Google AI Studio, **Figma Make has no persistent "System Instructions" field**. Every session starts fresh. This means:

1. All design system context must be included in your **first message** (the Context Primer)
2. A **Checkpoint prompt** comes second — asking Figma Make to confirm its understanding before generating anything
3. **Section-by-section Build Prompts** come third — one per major section for complex pages, or a single consolidated prompt for simpler features
4. Figma Make uses **Claude Sonnet** as its underlying model — intent-first prompting works, but the output is Figma frames, not prose or code

---

## Process

### Step 1: Gather Context

Before generating, collect the following. If the user provided them in their message, use what's there. If not, ask in a single message — no more than 5 questions, grouped clearly:

**Required:**
1. **What is being designed?** (page, component, screen — be specific)
2. **Business goal:** What does this UI need to accomplish?
3. **User:** Who uses this, and what context do they arrive with?
4. **Success criterion:** How do you know the design worked? (Observable outcome)

**Optional (ask only if not inferable):**
5. **Visual direction:** Any mood, aesthetic reference, or style preference? (Or: "Let Figma Make decide")
6. **Key sections or content:** What information/sections must appear?
7. **Design system:** Existing Figma design system/library to reference? Any color tokens, type styles, or component names to use?
8. **Anything to avoid:** Known anti-patterns, competitor patterns to avoid, specific don'ts?

If the user gives only a rough description, infer what you reasonably can from the platform context and ask only for the gaps.

---

### Step 2: Generate the Prompt Package

Produce four clearly separated sections, formatted for direct copy-paste into Figma Make.

---

## Output Format

```
---
## ✦ CONTEXT PRIMER
*Paste as your FIRST message in Figma Make. Establishes the design system, palette, and vocabulary for the entire session. End with the checkpoint question — do not paste the Checkpoint section separately.*

---
## ✦ BUILD PROMPT(S)
*Paste as your second message, after receiving the checkpoint confirmation. For complex pages: broken into per-section prompts. For simpler features: a single consolidated prompt.*

---
## ✦ ITERATION TEMPLATES
*Use these as follow-up messages during visual refinement.*

---
## ✦ DARK MODE WORKFLOW
*If this design requires a dark-first palette: a step-by-step note on how to achieve this in Figma Make, including plugin recommendations.*
```

---

## Section 1: Context Primer

The Context Primer does the job that System Instructions do in AI Studio — but it must be written as a first chat message, not a persistent setting. It ends with a checkpoint question asking Figma Make to confirm its understanding **before generating anything**.

Write the primer in this order:

### 1.1 Designer Persona
```
You are a [role] working on [platform type]. Your design sensibility reflects [2-3 real product design cultures as shorthand: Linear, Stripe, Vercel, Notion, Apple, The Atlantic, Figma itself, etc.].
```

### 1.2 Design Token System
Unlike AI Studio (where you avoid hex codes to let the AI decide), in Figma Make **hex codes and pixel values are welcome and recommended** — they produce more consistent results than vague color descriptions. Specify:

- **Color palette** — Name each role (Background, Surface, Primary/Accent, Foreground, Muted, Border) with its hex value and role description
- **Typography** — Font families for each role (headings, body, serif/display, mono if needed) and key size/weight pairs for major text styles (H1, H2, Body, Caption, Label)
- **Spacing scale** — Base unit and common values (4, 8, 12, 16, 24, 32, 48, 64px)
- **Border radius** — Card/container radius, button radius, badge/pill radius
- **Shadow/effect tokens** — Key shadows by name (e.g., card shadow, glow shadow, overlay)

**Example:**
```
Design system tokens for this session:

Colors:
- Background: #050505 (near-black base, used for the page field)
- Surface: #0a0a0a (elevated card/container background)
- Primary: #F27D26 (vibrant orange — accent, CTAs, active states only)
- Primary foreground: #141414 (dark text on orange backgrounds)
- Foreground: #FFFFFF (primary text on dark)
- Muted text: #999999 (secondary/supporting text)
- Border: #2E2E2E (visible but quiet dividers and outlines)

Typography:
- Inter — headings, labels, UI text, body copy
- Lora — pull quotes, scripture, blockquotes, devotional passages only
- H1: Inter 56px / Bold / -0.02em letter-spacing
- H2: Inter 36px / Semibold / -0.01em
- H3: Inter 24px / Semibold
- Body: Inter 16px / Regular / 1.7 line-height
- Caption: Inter 13px / Regular / Muted text color
- Quote: Lora 24px / Italic / Foreground color

Spacing: base unit 4px. Common values: 8, 16, 24, 32, 48, 64, 96px
Border radius: 0px on all containers and cards. 9999px on buttons. 4px on badges/pills.
Shadow: Card shadow — 0 1px 3px rgba(0,0,0,0.4). Glow — 0 4px 14px rgba(242,125,38,0.25).
```

### 1.3 Figma-Native Conventions
Tell Figma Make how to structure its Figma output:

```
Figma conventions for this session:
- Use Auto Layout (vertical) for all page sections and content columns
- Use Auto Layout (horizontal) for row layouts, card grids, and navigation items
- Name all top-level frames descriptively: "Hero", "Overview Section", "Course Cards", etc.
- Name components by their role: "Card / Course", "Nav / Sidebar Item", "Button / Primary"
- All interactive elements should have a hover variant and (where applicable) an active/selected variant
- Use Figma's "Fill" for flat backgrounds; use "Gradient" only where the design explicitly calls for gradient
- Do not use placeholder gray boxes for images — use realistic image placeholders with descriptive labels inside
```

### 1.4 Design Principles (3–5 platform-specific)
Write 3–5 crisp design principles that shape every decision in this session. Make them specific to the platform and aesthetic direction. These will guide Figma Make's judgment when the prompt doesn't prescribe exact treatment.

**Example:**
```
Design principles:
- Darkness is gravity, not emptiness — the near-black field should feel weighty and settled
- Orange earns its presence — every instance must be an action, an active state, or a structural signal
- Serif type signals a register shift — Lora appears only in devotional moments, never in body copy
- Sections breathe — generous vertical rhythm separates each conceptual unit
- Sharp edges signal seriousness — 0px radius on containers is intentional; the content provides the warmth
```

### 1.5 Checkpoint Question (close the primer with this)
Always end the Context Primer with this exact type of question:

```
Before you generate anything, confirm your understanding:
1. What design system tokens will you apply throughout this design?
2. What is the primary font for headings and body? What is the secondary font and when do you use it?
3. What is the background color? The primary accent color?
4. What is the border radius on cards? On buttons?
5. What design principles will guide your layout decisions?

Do not generate any frames yet. Only answer these questions.
```

---

## Section 2: Build Prompts

After receiving the checkpoint confirmation, proceed to the build. For complex pages (5+ sections), break into **per-section prompts**. For simpler features (a single component, a modal, a card), a **single consolidated prompt** works fine.

### When to Use Per-Section Prompts

Use per-section prompts when:
- The page has more than 5 distinct sections
- The page is a long-scroll document (article, profile, course page)
- Different sections have meaningfully different layout patterns
- You want to review each section before committing to the next

Use a single consolidated prompt when:
- The feature is a single component (a card, a modal, a form)
- The page is short (hero + 2–3 sections)
- All sections share the same layout pattern

### Per-Section Prompt Structure

Each section prompt follows this template:

```
Generate the [SECTION NAME] section.

Frame name: "[Section Name]"
Width: [1440px desktop / 390px mobile / both]
Background: [token name or hex]

Content:
[Describe what goes in the section — text, images, data, CTAs]

Layout:
[Describe the spatial structure — columns, rows, auto-layout direction, alignment]
[Use Figma vocabulary: "horizontal auto-layout with 24px gap", "2-column grid with 32px gutter", "centered single column 720px max-width"]

Typography:
[Which text styles from our token system apply here — e.g., "The section heading uses H2; body paragraphs use Body; the section label above the heading uses Label in the Primary accent color"]

Variants needed:
[List any variants — hover state for cards, open/closed state for accordion, active/inactive for nav items]

Do not generate the next section yet.
```

### Consolidated Prompt Structure

For simpler features, use this structure:

```
Generate [feature name].

[2–3 sentence business context: why this exists, who uses it, what it must accomplish]

Frame setup:
- Desktop frame: 1440px wide
- Mobile frame: 390px wide (generate both)
- Apply the design system tokens established in our context

Sections (in order):
1. [Section name] — [one sentence: layout type + key content]
2. [Section name] — [one sentence: layout type + key content]
...

Interaction states:
- [Element]: hover state shows [description]
- [Element]: selected/active state shows [description]

Constraints:
- [Any hard requirements — e.g., "The CTA button must be visible without scrolling on desktop"]
- [Any hard avoidances — e.g., "Do not use gradients except in the hero overlay"]
```

### Build Prompt Vocabulary (Figma-Native)

Use these terms — not React/Tailwind vocabulary — when generating build prompts:

| Figma term | Meaning |
|------------|---------|
| `Frame` | Container element (like a div, but in Figma) |
| `Auto Layout (vertical)` | Flexbox column |
| `Auto Layout (horizontal)` | Flexbox row |
| `Gap: 16px` | Spacing between items in auto-layout |
| `Padding: 24px 32px` | Inner padding on a frame |
| `Fill` | Background color |
| `Stroke` | Border (color + weight + position: inside/outside/center) |
| `Corner radius` | Border radius |
| `Effect: Drop Shadow` | Box shadow |
| `Effect: Background Blur` | Backdrop-filter blur (glassmorphism) |
| `Component` | Reusable UI element |
| `Instance` | Copy of a component |
| `Variant` | State variation of a component (hover, active, disabled) |
| `Text style` | Named typography definition |
| `Color variable` | Named color token |
| `Clip content` | overflow: hidden |
| `Constraints` | How element responds to frame resize |

---

## Section 3: Iteration Templates

Generate 8–10 ready-to-use follow-up prompts tailored to the specific feature. Always include these categories:

**1. Typographic hierarchy:**
```
The [section] heading doesn't have enough visual authority — the hierarchy between the section label, heading, and body feels flat. Adjust only the type weight, size ratio, and spacing between these three levels so the hierarchy is immediately legible. Change nothing else.
```

**2. Component refinement:**
```
The [component — e.g., course card / FAQ row / step item] feels too generic. Refine only this component: adjust the [fill / stroke / corner radius / internal spacing / typography treatment] so it feels more consistent with the premium dark aesthetic. Do not change surrounding sections.
```

**3. Spacing/rhythm:**
```
The vertical rhythm in [section] feels [too compressed / too spacious]. Adjust only the internal padding and gap values within this section's Auto Layout so the spacing feels [deliberate and unhurried / tighter and more efficient]. Keep all other sections unchanged.
```

**4. Color application:**
```
The Primary accent color (#F27D26) is appearing too frequently in [section] — it's losing its weight. Reduce its usage to only the highest-priority element in this section (the [CTA / active state / section label]). Change all other accent instances to [the Border color / Muted text color]. Touch only this section.
```

**5. Mobile layout:**
```
On the 390px mobile frame, the [section] layout is not working — [describe what's wrong: columns collapsing awkwardly / text too small / CTA buried]. Rework only the mobile layout for this section. Do not change the 1440px desktop frame or any other sections.
```

**6. Interaction states:**
```
The [element — e.g., card / button / accordion row / nav item] is missing its interaction states. Add hover and active variants to this component only. Hover: [describe the change — e.g., "Surface lightens slightly, stroke becomes Primary color"]. Active/selected: [describe — e.g., "Left-edge indicator bar appears in Primary color"]. Do not regenerate surrounding sections.
```

**7. Surface depth:**
```
The page feels too flat — all surfaces are the same visual depth. Introduce one additional level of surface elevation in [section]: the [card / callout box / sidebar] should feel slightly lifted off the base. Use a subtle stroke and a light drop shadow consistent with our shadow tokens. Change nothing else.
```

**8. Visual rhythm break:**
```
The full-width [Pull Quote / CTA / Scripture] section doesn't feel like a genuine pause in the scroll — it blends into the surrounding content. Increase only the top and bottom padding on this section and adjust the typographic scale upward so it functions as a meditative interruption. Touch only this section.
```

**9. Section label system:**
```
The section labels (the small uppercase/small-caps labels above each section heading) are inconsistent across the page. Standardize them: [uppercase / small-caps], Inter, [12 or 13px], Primary accent color (#F27D26), [6 / 8px] letter-spacing. Apply this treatment to every section label on the page.
```

**10. Content replacement:**
```
Replace all placeholder content in [section] with realistic copy for [domain and audience]. Use [domain-specific guidance — e.g., "theologically grounded language from Alan Hirsch's missional framework"]. Keep all layout, spacing, type styles, and color treatments exactly as they are.
```

**Feature-specific templates** — generate 2–3 more based on the specific feature (e.g., for a long-form content page: sticky sidebar active state, accordion open-state animation, related portal card hover treatment).

---

## Section 4: Dark Mode Workflow

If the design is **dark-first** (as is the case for this platform), include this note in the output:

```
## ✦ DARK MODE WORKFLOW

Figma Make does not natively generate dark mode variants. For this dark-first design, use this workflow:

**Option A — Token-forward (recommended):**
1. Paste the Context Primer with explicit dark hex values as the base palette
2. Figma Make will generate the dark design as the primary design
3. To add a light mode variant later: use the Figma plugin "Shades" or "Dark Mode Creator"
   to generate light-mode color swaps from the existing dark token set

**Option B — Post-generation plugin workflow:**
1. Generate in Figma Make using the dark palette as specified
2. Select all frames, run the "Dark Mode Palette Generator" plugin
3. Manually adjust any swaps that don't translate correctly
4. Create a separate "Light Mode" page in Figma with the swapped palette

**For this design:** The Context Primer above specifies the dark palette as the default. No additional steps needed for initial generation. If a light mode variant is requested, use Option B above.
```

---

## Quality Checklist

Run before finalizing the prompt package:

- [ ] Context Primer includes all 5 parts: persona, token system (with hex values), Figma conventions, design principles, checkpoint question
- [ ] Token system specifies: background, surface, primary/accent, foreground, muted, border — with hex values for each
- [ ] Typography specifies: font families, specific size/weight pairs for H1/H2/H3/Body/Caption/Label
- [ ] Checkpoint question asks Figma Make to confirm understanding before generating
- [ ] Build prompts use Figma-native vocabulary (frame, auto-layout, fill, stroke, variant) — not React/Tailwind vocabulary
- [ ] Build prompts include frame width specification (1440px desktop, 390px mobile)
- [ ] Complex pages are broken into per-section prompts
- [ ] Each section prompt names the frame, specifies layout type, lists required variants
- [ ] Business goal stated before visual direction in the first build prompt
- [ ] Guardrails section includes: no lorem ipsum, WCAG AA contrast, no pure #000/#fff, max 2 typefaces
- [ ] Dark mode workflow section present if the design uses a dark palette
- [ ] At least 8 iteration templates generated
- [ ] All placeholder content guidance is domain-specific (not generic)

---

## Layout Pattern Vocabulary

Use these terms when describing layout in build prompts:

| Pattern | Figma equivalent |
|---------|-----------------|
| `Hero-centric` | Full-width frame, 100vh+, centered or left-aligned content, image fill with overlay |
| `Sidebar + main content` | Horizontal auto-layout: fixed-width sidebar frame + flexible-width content frame |
| `Two-column split` | Horizontal auto-layout, 50/50 or 40/60 width split |
| `Card grid` | Auto Layout (horizontal, wrap), fixed card width, consistent gap |
| `Bento grid` | Auto Layout or manual placement, varying card heights/widths |
| `Stacked sections` | Vertical auto-layout at page level, each section a full-width frame |
| `Compact list` | Vertical auto-layout, tight gap, small text, horizontal item rows |
| `Focused form` | Centered single-column frame, 480–560px wide, vertical auto-layout |
| `Storytelling scroll` | Stacked full-width frames, alternating layouts, strong typographic transitions |

---

## Save the Output

After generating, save to:
```
_docs/figma-prompts/[feature-slug]/PROMPT.md
```

Include the date at the top of the file.

---

## Key Limitations to Know

Inform the user of these Figma Make limitations before they begin:

1. **Custom design system libraries not supported yet** — Figma Make cannot automatically pull from an existing Figma component library. Use the token system in the Context Primer as a substitute.
2. **Low variability on re-generation** — Multiple generation passes tend to look similar. Use iteration templates to refine rather than regenerating from scratch.
3. **Long chat history degrades quality** — Above ~50 messages, Figma Make performance drops. Start a new session for major changes.
4. **Complex scroll behavior is unreliable** — Sticky headers, intersection-based animations, and parallax effects don't render predictably. Describe intent; accept Figma's interpretation as a visual approximation.
5. **Rate limiting** — "Model is overloaded" errors occur during high-traffic periods. Wait 2–5 minutes and retry rather than re-prompting immediately.
6. **Credits** — Failed generations still consume credits. If a prompt fails, diagnose with a clarifying message before retrying.

---

## Example Output Stub (abbreviated)

```
---
## ✦ CONTEXT PRIMER

You are a principal product designer working on a theological formation platform. Your design sensibility reflects the editorial authority of The Atlantic's digital presence, the dark precision of Linear, and the quiet gravitas of a well-designed seminary press.

Design system tokens for this session:

Colors:
- Background: #050505
- Surface: #0a0a0a
- Primary: #F27D26
...

[Full token system]

Figma conventions:
- Use Auto Layout (vertical) for all page sections...

Design principles:
- Darkness is gravity, not emptiness...

Before you generate anything, confirm your understanding:
1. What color is the page background?
...

Do not generate any frames yet. Only answer these questions.

---
## ✦ BUILD PROMPTS

### Section 1: Hero

Generate the Hero section.

Frame name: "Hero"
Width: 1440px desktop (also provide 390px mobile variant)
Background: #050505 with an atmospheric image fill and a left-to-right gradient overlay (#050505 at 92% opacity fading to transparent)

Content:
...

[Full section-by-section prompts]

---
## ✦ ITERATION TEMPLATES

**Typographic hierarchy:**
"The Overview section heading doesn't have enough authority..."

[Full set of templates]

---
## ✦ DARK MODE WORKFLOW

This design is dark-first. No additional dark mode setup needed for initial generation...
```
