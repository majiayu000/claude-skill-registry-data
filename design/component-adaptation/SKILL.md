---
name: component-adaptation
description: Take a component copied from a library and make it belong to your product, without losing what made it good. Identify the essential interaction, separate the replaceable tokens from the behaviour, adapt type, colour, content and size, then test themes, keyboard and reduced motion. Use after copying a component from Vitrine or any other library into a real project.
---

# /component-adaptation

A copied component looks right in the library because everything around it was designed for it. In your product it arrives with another font, another accent colour, demo copy and a size chosen for a showcase. Left as it is, it looks pasted in. Rewritten from scratch, it loses the interaction that made it worth copying. Adaptation is the middle path: keep the idea, change the surface.

## Purpose

Make a copied component visually and verbally part of the product, while preserving its interaction, its states and its accessibility.

## Use when

- You've copied a component into a project and it doesn't look like the rest of the product yet.
- A component's demo content, colours or fonts are still in the code.
- Several copied components need to share one design language.

## Don't use when

- You're building a component from scratch. Use `/component-author`.
- The component doesn't fit the job at all. Pick a different one rather than bending this one into another component.
- You only need to fix a bug inside it.

## Inputs

- The component's source files and its original demo, running, so you can compare.
- The product's design tokens: colours, fonts, radii, spacing, shadows, button styles (`/design-system-consistency` helps find them).
- The real content it will show: actual labels, data, lengths, languages.
- Where it will live: the section, the surrounding components, light and/or dark theme.

## Process

### 1. Name the essential interaction

Write one sentence: what does this component do that makes it worth having? "The indicator stretches toward the next tab before the old one lets go." "The pricing ruler makes the price follow your usage." That sentence is what you must not break.

### 2. Sort the code into three piles

Read the source and label what you find:

- **Behaviour to keep:** the state logic, the motion that explains something, keyboard handling, ARIA attributes, reduced-motion handling, the cleanup of listeners and timers.
- **Tokens to replace:** colours, fonts, radii, shadows, spacing, durations that are only style.
- **Content to replace:** demo labels, names, numbers, images, links.

If a value sits in both piles (a duration that is part of the interaction's feel), keep it and adjust carefully.

### 3. Replace tokens with the product's own

Swap each style value for the product's token or CSS variable. Prefer existing tokens over new values. Match:

- **Type:** the product's font families, sizes and weights; the component's labels should look like the product's labels.
- **Colour:** the product's accent, surface and text roles, in both themes if the product has two.
- **Shape:** the product's radius and border style.
- **Buttons and inputs** inside the component: use the product's own button and field styles if they exist.

### 4. Replace content with real content

Use the real labels, data and lengths. Check the longest real value, an empty state, and a single item. Demo content always fits; real content often doesn't.

### 5. Fit it into its place

Set its size for the section it lives in, not for a showcase. Check that it doesn't fight its neighbours: one moving element per section is usually enough.

### 6. Test what you might have broken

- The essential interaction from step 1 still works and still feels the same.
- Keyboard: every control reachable, visible focus, the same order as before.
- Screen reader names and states still make sense with the new content.
- `prefers-reduced-motion`: the still version still looks designed.
- Both themes, if the product has them.
- Phone width.

## Acceptance criteria

- The essential interaction sentence still holds.
- No demo content, demo colours or demo fonts remain in the component.
- Every replaced style value uses an existing product token, or a new token added deliberately.
- Keyboard, focus, reduced motion and (if applicable) both themes were tested after the change.
- Side by side with the product's other components, it looks like it belongs.

## Common failure modes

- **Restyling the interaction away.** Changing a duration or an easing that was the whole point, because it "looked a bit much".
- **Half-adapted:** the product's colours with the library's font and radius.
- **New one-off values** instead of the product's tokens: a slightly different purple, a 13px radius.
- **Demo content left behind** in a tooltip, an empty state or an alt text.
- **Broken accessibility** after replacing elements: a `button` turned into a styled `div`, an `aria-label` that still names the demo.
- **Oversized for its context:** the showcase size kept, so it dominates a section that has other jobs.

## Final self-review

- Can I still describe the essential interaction in one sentence, and does it still happen?
- Is every colour, font, radius and shadow a product token?
- Is any demo content left?
- Did I test keyboard, reduced motion, both themes and 390px?
- Does it look like it was built for this product?

## Copyable instruction

```text
Adapt this copied component to our product without losing what makes it good.
1. Write one sentence describing its essential interaction; that must keep working.
2. Sort its code into: behaviour to keep (state, meaningful motion, keyboard, ARIA, reduced motion),
   style tokens to replace, and demo content to replace.
3. Replace style values with our existing tokens (fonts, colours, radii, spacing, our button styles).
   Don't invent new one-off values.
4. Replace demo content with real content; test the longest value, empty and single-item states.
5. Size it for the section it lives in.
Verify: the interaction still works, keyboard and focus, reduced motion, both themes, 390px wide.
Do not rewrite the component or remove its motion to make it "simpler".
```
