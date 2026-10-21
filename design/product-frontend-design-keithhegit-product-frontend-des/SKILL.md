---
name: product-frontend-design
description: "Run Product Design and Frontend Design as one UI/UX collaboration workflow. Use when the user invokes Product Design + Frontend Design, asks for a UI/UX redesign, asks to make an interface more user friendly, designs a plugin panel, or wants a product flow turned into polished frontend UI."
---

# Product + Frontend Design

Use this skill as the shortcut entry for the combined UI/UX workflow.

When this skill is active, also use the underlying Product Design and Frontend Design skills if they are available in the current environment. This shortcut does not replace those skills; it fixes their collaboration order and quality bar.

## Required Order

1. Use Product Design first, starting from `product-design:index` when available.
   - Confirm the product, user, core task, design brief, experience loop, interaction states, empty states, error states, and acceptance criteria.
   - For new UI without a visual target, run the Product Design brief gate before implementation.
   - If visual exploration is needed, present options before coding.

2. Use Frontend Design second.
   - Translate the approved experience into concrete layout, visual hierarchy, copy, controls, responsive behavior, and screenshot-level polish.
   - Choose one signature element that makes the interface easier to understand.
   - Keep the rest of the UI restrained and consistent with the host product.

3. Implement only after the experience direction is clear.
   - Follow the existing app design system and local component patterns.
   - Avoid exposing implementation terms to non-professional users.
   - Verify with screenshots or GUI retest in addition to type/build checks.

## Vocabulary Rule

Prefer words users already understand. Hide implementation terms unless the screen is explicitly for developers.

For each product, define a small vocabulary map during Product Design:

- What the system calls the thing internally.
- What the user should see in the UI.
- Which technical terms must stay hidden.

Avoid exposing implementation terms like internal IDs, tool calls, manifests, indexes, provider errors, or storage internals in ordinary UI.

## New User Rule

For first-time or non-professional users, the first screen must answer:

- What is this?
- Why should I use it?
- What should I do first?
- What happens after I click the main button?
- How do I recover if nothing is ready yet?

Empty states must include examples, next-step buttons, and a plain-language success path.

## Output Contract

Before implementation, produce a concise UI/UX brief with:

- Target user and core job.
- Experience loop.
- Vocabulary map.
- First-screen structure.
- Empty, loading, success, and error states.
- Visual direction and one signature element.
- Verification plan, including screenshot or GUI retest.
