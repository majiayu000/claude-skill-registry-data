---
name: ux-psychology
description: Apply UX psychology principles to frontend design. Use when designing UI components, improving user experience, increasing conversion, or making design decisions. Covers 43 psychological concepts including cognitive biases, behavioral patterns, visual design principles, and engagement techniques. Triggers on requests like "design a pricing page", "improve signup flow", "increase engagement", or "apply psychology to UI".
---

# UX Psychology for Frontend Design

Apply psychological principles to create more effective, engaging user interfaces.

## Workflow

### 1. Identify Design Goal

Determine the primary objective:
- **Conversion**: Pricing, signup, checkout
- **Engagement**: Retention, time-on-site, repeat visits
- **Usability**: Task completion, error reduction
- **Trust**: Credibility, security perception

### 2. Select Relevant Concepts

Based on goal, consult the appropriate reference file:

| Goal | Reference File | Key Concepts |
|------|---------------|--------------|
| Conversion | `references/cognitive-biases.md` | Anchoring, Loss Aversion, Framing |
| Engagement | `references/engagement.md` | Gamification, Variable Reward, Social Proof |
| Usability | `references/behavioral-patterns.md` | Cognitive Load, Progressive Disclosure, Default Effect |
| Visual Appeal | `references/visual-design.md` | Aesthetic-Usability, Visual Hierarchy |

### 3. Apply Concepts to Design

For each selected concept:
1. Read the detailed pattern from reference file
2. Identify specific UI elements to apply it to
3. Implement with code examples provided

## Quick Reference: 43 Concepts

### Cognitive Biases (→ `references/cognitive-biases.md`)
Anchoring Effect, Confirmation Bias, Expectation Bias, Familiarity Bias, Framing Effect, Halo Effect, Loss Aversion, Sunk Cost Effect, Survey Bias

### Behavioral Patterns (→ `references/behavioral-patterns.md`)
Cognitive Load, Decision Fatigue, Default Effect, Foot-in-the-Door, Goal Gradient Effect, Intentional Friction, Nudge Effect, Progressive Disclosure, Reactance, Reactive Onboarding, Selective Attention, Temptation Bundling, Zeigarnik Effect

### Visual Design (→ `references/visual-design.md`)
Aesthetic-Usability Effect, Banner Blindness, Visual Hierarchy, Visual Anchor, Skeuomorphism, Serial Position Effect, Priming Effect

### Engagement (→ `references/engagement.md`)
Curiosity Gap, Decoy Effect, Doherty Threshold, Empathy Gap, Endowment Effect, Gamification, Hawthorne Effect, Labor Illusion, Peak-End Rule, Pygmalion Effect, Scarcity, Social Proof, User Delight, Variable Reward

## Common Design Patterns

### Pricing Page
```
Applied concepts:
- Anchoring: Show highest-priced plan first
- Decoy Effect: Make middle plan look like best value
- Social Proof: "Most Popular" badge
- Visual Anchor: Highlight recommended plan visually
```

### Signup Flow
```
Applied concepts:
- Foot-in-the-Door: Start with email only, ask details later
- Cognitive Load: One task per screen
- Goal Gradient: Show progress bar
- Default Effect: Pre-select recommended options
```

### E-commerce Product Page
```
Applied concepts:
- Scarcity: "Only 3 left in stock"
- Social Proof: Reviews and ratings
- Loss Aversion: "Don't miss out..."
- Aesthetic-Usability: High-quality product images
```

## Ethical Guidelines

### Dark Patterns to Avoid
- False scarcity claims
- Hidden fees
- Difficult cancellation flows
- Manipulative loss aversion messaging
- Forced opt-ins

### Ethical UX Design
- Prioritize user benefit
- Provide transparent information
- Respect user choice
- Build trust over tricks

## Source

Based on: https://www.shokasonjuku.com/ux-psychology
