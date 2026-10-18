---
name: design-psychology
description: Web UX & Conversion Psychology framework based on Self-Made Web Designer (Chris McCoy) and Ran Segall (Flux Academy). Implements 3-Brain Persona Alignment (Survival, Emotional, Rational), Mental Model Layout Familiarity, MAYA Principle pattern breaks, Cognitive Chunking (3-4 item Working Memory Rule), Luxury White Space ("Space is Wealth"), Signature Niche Positioning, and the Oliver Smithies "Wander Off" experimental directive.
triggers:
  - /design-psychology
  - design-psychology
  - design psychology
  - ux psychology
  - maya principle
  - cognitive chunking
---

# Web UX & Conversion Psychology Framework (`design-psychology`)

This skill applies fundamental behavioral psychology, cognitive science, conversion optimization, luxury positioning, and legendary designer habits to web design based on Chris McCoy's (Self-Made Web Designer) and Ran Segall's (Flux Academy) master frameworks.

*Ecosystem Integration:* This skill works in synergy with **`design-setup`** (page layout structuring), **`design-rules`** (CSS/Tailwind micro-rules), and **`design-audit`** (conversion audit).

---

## 🧠 Subconscious Processing & The 3-Brain Persona Model

Out of 1,000,000,000 bits of sensory information reaching the human brain every second, **only 10 bits enter conscious awareness**. Over 99.9% of user decisions are made subconsciously.

When a user visits a website, their brain behaves as **3 Internal Personas** voting in strict sequential order:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 3 INTERNAL BRAIN PERSONAS                                   │
├───────────────────────────────────┬───────────────────────────┬────────────────────────┤
│ 1. The Survival / Safety Brain    │ 2. The Emotional Brain    │ 3. The Rational Brain  │
│    (Votes FIRST: Mental Models)   │    (Votes SECOND: Dopamine)│    (Votes LAST: Logic) │
└───────────────────────────────────┴───────────────────────────┴────────────────────────┘
```

---

## 🛡️ 1. Brain Persona #1: The Survival / Safety Brain (Mental Models)

* **Primary Concern:** Safety, low cognitive effort, zero confusion, instant predictability.
* **Voting Order:** **Votes FIRST.** If Brain #1 feels confused or unsafe, the visitor bounces immediately without reading the content.

### 1.1 The Psychological Rule of Mental Models
Users arrive at your website with a pre-existing blueprint in their heads built from every website they have ever visited in their lives:
* Logo at **Top-Left**
* Navigation at **Top-Right / Center**
* Primary Hero & CTA at **Top-Center**
* Footer & Policies at **Bottom**

### 1.2 Anti-Pattern: Breaking Mental Models
Never be "over-creative" with structural layouts or navigation locations. Moving core navigation (e.g. placing mobile menus at unconventional bottom corners) breaks the user's mental model, triggering cognitive alarm for Brain #1 and causing instant bounce rates.

### 1.3 💎 "Space is Wealth" (Perceived Value & Cognitive Breathing Room)
Vast, intentional white space signals high perceived value and prestige to Brain #1. Cluttered designs packed edge-to-edge trigger low-cost discount perception. Generous white space reduces cognitive fatigue, allowing visitors to digest content frame-by-frame.

```markdown
✅ RULE: Keep macro page layouts strictly predictable and familiar while utilizing generous white space to convey premium value.
❌ ANTI-PATTERN: Cramming information edge-to-edge or moving navigation into non-standard hidden locations.
```

---

## ⚡ 2. Brain Persona #2: The Emotional Brain (MAYA Principle & Pattern Interrupts)

* **Primary Concern:** Delight, excitement, emotional resonance, dopamine hits.
* **Voting Order:** **Votes SECOND.**

### 2.1 The Safety vs. Boredom Conflict
If Brain #1 makes 100% of the design decisions, the website becomes so safe and predictable that **Brain #2 gets bored and leaves**. 

### 2.2 The MAYA Principle (Most Advanced Yet Acceptable)
Designers must balance safety and excitement using the **MAYA Principle**:
> **Keep the overall layout structure 100% predictable (for Brain #1), but deliberately break tiny micro-patterns inside the structure (for Brain #2) to trigger pleasant, unexpected dopamine hits.**

### 2.3 Micro-Interaction & Signature Calling Card Directives
* **Subtle Hover Reactions:** Buttons that respond with unexpected elegance on hover (e.g., subtle color shift, smooth icon nudge).
* **Scroll Parallax & Scaling:** Images or background layers that scale by 2-3% as the user scrolls past.
* **Signature Calling Card Technique:** Implement one signature superpower technique (e.g. GSAP ScrollTrigger, Spline 3D element, or custom WebGL shader) consistently across projects as your visual calling card.

```html
<!-- MAYA Pattern Interrupt Example (Predictable Card + Subtle Hover Scale) -->
<div class="group relative overflow-hidden rounded-2xl border border-neutral-200 bg-white p-6 transition-all duration-500 hover:border-neutral-400 hover:shadow-xl">
  <!-- Micro Pattern Interrupt: Image scales 3% on hover -->
  <div class="overflow-hidden rounded-xl">
    <img src="/product-preview.jpg" class="h-48 w-full object-cover transition-transform duration-500 group-hover:scale-105" />
  </div>
  <h3 class="mt-4 text-xl font-bold tracking-tight">Predictable Clean Headline</h3>
</div>
```

---

## 📊 3. Brain Persona #3: The Rational / Logic Brain (Chunking & Justification)

* **Primary Concern:** Logic, price/value comparison, justification for an emotional purchase decision.
* **Voting Order:** **Votes LAST.** (Brain #1 and #2 have already made the emotional choice; Brain #3 validates the decision).

### 3.1 Cognitive Capacity Constraint (The 3-4 Item Rule)
The human working memory can only process **3 to 4 items simultaneously** before dropping earlier information. Displaying an unorganized list of 10+ features causes cognitive overload and decision paralysis.

### 3.2 The Rule of Cognitive Chunking
Group complex information into 3 or 4 distinct visual chunks (similar to grouping 10-digit phone numbers into 3-3-4 chunks).

### 3.3 Pricing Tier Incremental Comparison Rule
NEVER list 20 identical bullet points repeatedly across multiple pricing tiers. Force Brain #3 to dig through a haystack to find differences damages conversion.
* **Execution Directive:** List base features once in the entry tier, then present higher tiers using **Incremental Comparison**:
  * *"Everything in Basic PLUS [3 key upgraded features]"*.

---

## 🧪 4. Legendary Designer Mastery Directives

### 4.1 Signature Niche Positioning
Never try to be everything to everyone. High-value clients hire designers specifically for their **distinct visual signature and specific style niche**. Build personal/prototype projects in your exact signature style rather than taking on projects that dilute your visual brand.

### 4.2 Reps Over Perfectionism
Perfectionism is a silent killer. You must ship a high volume of work to move from "decent" to "legendary" status. Accept shipping C+ iterations in practice to build the muscle memory required for A+ execution.

### 4.3 The Oliver Smithies "Wander Off" Rule
Pro designers MUST schedule dedicated time just to explore irrational experiments and creative ideas outside of paid client work. Unconstrained creative exploration prevents creative burnout and generates non-obvious design breakthroughs for real projects.

---

## 📊 Psychology Audit Scorecard

When analyzing or building UIs, the agent MUST evaluate the user experience against this 3-Brain Persona Scorecard:

```markdown
# 🧠 UX Psychology Audit Report

## 📈 Executive Psychology Score: [90 / 100]

| Brain Persona | Target Goal | Status | Key Observations & Recommendations |
| :--- | :--- | :---: | :--- |
| **Brain #1: Survival / Safety** | Layout Predictability & Mental Models | ✅ PASS | Logo top-left, nav top-right. Zero friction layout. Generous white space. |
| **Brain #2: Emotional Brain** | MAYA Pattern Interrupts & Micro-Delight | ⚠️ WARN | Layout is safe, but hover states are flat. Add subtle scale micro-interactions. |
| **Brain #3: Rational Brain** | Cognitive Chunking (3-4 Items Max) | ✅ PASS | Pricing features grouped incrementally. Zero cognitive overload. |
```
