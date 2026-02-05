---
name: frontend-delegation
description: Use when touching frontend files to classify visual vs logic changes before acting
---

# Frontend Delegation

Frontend files require classification before action. Visual work goes to Pixel; logic you handle directly.

## The Core Question

Before touching any frontend file, ask:
> "Is this change about **how it LOOKS** or **how it WORKS**?"

- **LOOKS** → DELEGATE to Pixel
- **WORKS** → Handle directly

## Change Type Classification

| Change Type | Examples | Action |
|-------------|----------|--------|
| **Visual/UI/UX** | Color, spacing, layout, typography, animation, responsive breakpoints, hover states, shadows, borders, icons, images | DELEGATE to `pixel` |
| **Pure Logic** | API calls, data fetching, state management, event handlers (non-visual), type definitions, utility functions, business logic | Handle directly |
| **Mixed** | Component changes both visual AND logic | Split: logic yourself, visual to `pixel` |

## Quick Reference Examples

| File | Change | Type | Action |
|------|--------|------|--------|
| `Button.tsx` | Change color blue→green | Visual | DELEGATE |
| `Button.tsx` | Add onClick API call | Logic | Direct |
| `UserList.tsx` | Add loading spinner animation | Visual | DELEGATE |
| `UserList.tsx` | Fix pagination logic bug | Logic | Direct |
| `Modal.tsx` | Make responsive for mobile | Visual | DELEGATE |
| `Modal.tsx` | Add form validation logic | Logic | Direct |

## Visual Keyword Detection

DELEGATE if ANY of these keywords involved:

```
style, className, tailwind, color, background, border, shadow,
margin, padding, width, height, flex, grid, animation, transition,
hover, responsive, font-size, icon, svg, theme, dark-mode
```

## Delegation Prompt to Pixel

When delegating, include:

```
1. TASK: Specific visual goal
2. EXPECTED OUTCOME: What it should look like
3. CONTEXT: File paths, existing styles, design system
4. MUST DO: Visual requirements
5. MUST NOT DO: Don't change logic, don't add dependencies
```

## After Delegation

Verify Pixel's work:
- Does it match the visual requirements?
- Did it follow existing style patterns?
- Did it avoid changing logic?
