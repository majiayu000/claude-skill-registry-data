---
name: component-spec
description: >
  Write a component spec for engineering handoff. Use when the user says "component spec",
  "design handoff", "spec this component", "document this component for engineering",
  "Figma handoff", "component documentation", "how do I hand this off",
  or needs to communicate a UI component design to developers
  - even if they don't explicitly say "component spec".
---

## Overview

Based on **"Atomic Design"** by Brad Frost. Frost's atomic design methodology organizes UI into: atoms (basic elements), molecules (groups of atoms), organisms (groups of molecules), templates (page structures), and pages (specific instances). A component spec documents where a component sits in this hierarchy, what it's made of, how it behaves, and how it should be used.

The goal of a component spec is to make the engineering handoff self-contained. A developer should be able to build the component correctly without asking questions.

## Workflow

### Step 1: Classify the component (Atomic Design)

| Level | What it is | Examples |
|-------|-----------|---------|
| Atom | Smallest UI unit, not decomposable | Button, input, icon, label |
| Molecule | 2-3 atoms working together | Search field (input + button), form field (label + input + error) |
| Organism | Complex UI section | Navigation bar, product card, comment thread |
| Template | Page-level layout | Dashboard layout, article layout |

Knowing the level sets expectations for complexity and reusability.

### Step 2: Write the component header

```
Component: [Name]
Atomic level: [Atom / Molecule / Organism]
Status: [Draft / In Review / Production]
Designer: [your name]
Figma link: [URL]
```

### Step 3: Document variants and states
List every variant (different configurations of the same component) and every state:

**Variants:**
- Size variants: small, medium, large
- Style variants: primary, secondary, ghost, destructive
- Content variants: with icon, without icon, with badge

**States:**
- Default
- Hover
- Active/pressed
- Focus (keyboard navigation)
- Disabled
- Loading
- Error
- Success

Provide a Figma frame for every variant x state combination.

### Step 4: Document properties (props)
List every configurable property:

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `label` | string | Yes | - | Button text |
| `variant` | enum | No | primary | Visual style |
| `size` | enum | No | medium | Size variant |
| `disabled` | boolean | No | false | Disabled state |
| `onClick` | function | Yes | - | Click handler |

### Step 5: Document behavior
- What happens on click / tap?
- Are there animations or transitions? (duration, easing)
- What are the keyboard interactions? (Enter, Space, Escape, Tab)
- What happens at min/max content lengths?
- What happens when text is truncated?

### Step 6: Document accessibility requirements
- ARIA role and attributes
- Keyboard navigation behavior
- Screen reader announcement
- Focus management
- Color contrast requirements (WCAG AA minimum)

### Step 7: Document usage rules
When should this component be used? When should it not be used?

```
Use when: [specific contexts]
Don't use when: [anti-use-cases - what to use instead]
```

## Anti-Patterns

**1. Spec without states**
Bad: One static mockup handed off.
Good: Every state documented - default, hover, focus, disabled, error, loading.

**2. No accessibility section**
Bad: "Engineering will figure it out."
Good: ARIA role, keyboard behavior, and contrast requirements specified by design, not guessed by engineering.

**3. Props undocumented**
Bad: Figma file with no prop documentation.
Good: Every configurable property listed with type, required status, and description.

**4. Usage rules missing**
Bad: Component documented without guidance on when to use vs. not use it.
Good: Explicit usage rules prevent misuse and inconsistency across [your product].

## Quality Checklist

- [ ] Atomic level classified (atom/molecule/organism)
- [ ] Figma link to all variants and states
- [ ] All variants documented
- [ ] All states documented (default, hover, focus, disabled, error, loading)
- [ ] Props table complete with types, required flag, defaults
- [ ] Behavior documented (interactions, animations, edge cases)
- [ ] Accessibility: ARIA, keyboard, contrast documented
- [ ] Usage rules: when to use AND when not to use
