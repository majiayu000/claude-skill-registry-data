---
name: responsive-art-direction
description: Design each breakpoint as its own composition instead of stacking the desktop columns. For every element decide whether it moves, crops, shrinks, recomposes or disappears; set type scale, density and touch targets per width; check that the hierarchy still reads. Use when building or reviewing a layout for phone and tablet, especially heroes, image-led sections, pricing and dashboards.
---

# /responsive-art-direction

The default responsive layout is: take the desktop columns and stack them. It always fits and is rarely right. A hero image that sat beside the headline ends up a screen below it. A two-plan pricing table becomes a long scroll where the second plan is never seen. A dashboard's sidebar takes the whole first screen. Responsive art direction means deciding, for each width, what the page should be there.

## Purpose

Produce a deliberate composition at phone, tablet and desktop widths, where every important element has a decided role at each width, and the most important thing is still the most visible.

## Use when

- Building a new page or section that has images, multiple columns, or a strong first screen.
- A phone layout "works" but feels like the desktop page squeezed.
- Reviewing a design that was only drawn at desktop width.

## Don't use when

- You're looking for defects (overflow, tiny text, small targets). Use `/responsive-audit` first; this skill assumes nothing is broken.
- The section is a simple single column of text. Stacking is the right answer there.

## Inputs

- The desktop design, or the current page, captured at 390, 768, 1280 and 1920 (`/screenshot-iteration` has the script).
- The one thing each section must communicate. If you don't know it, you can't decide what survives on a phone.
- The real content: actual image crops, real text lengths, real data. Placeholder text hides the problems.

## Process

### 1. Rank each section's elements

For every section, list its elements and rank them: what must be seen first, what supports it, what's optional. On a phone, the first item gets the first screen.

### 2. Decide each element's behaviour, per width

For every element, choose one behaviour at each width:

| Behaviour | When it's right | Example |
|---|---|---|
| **Stays** | It's essential and fits. | A headline, the primary action. |
| **Moves** | Its position served a desktop layout, not the content. | An image beside the text goes below it, or above it if it carries the message. |
| **Re-crops** | The subject still matters, the frame doesn't fit. | A wide hero image cropped to the subject, not just scaled down. |
| **Shrinks** | It's supporting, and smaller still reads. | A decorative illustration at 70% width. |
| **Recomposes** | The arrangement itself must change. | A 3-column feature grid becomes a swipeable row, a table becomes stacked rows, a sidebar becomes a menu. |
| **Disappears** | It's decoration, or duplicates something else on the page. | A second illustration, a background flourish, a repeated call to action. |

Write this down as a small table per section before touching the CSS.

### 3. Set type and density per width

- **Type:** the largest headline should still be dramatic on a phone, but measure it: no single word should be cut, and two to three lines is the usual maximum. Use `clamp()` with a real minimum.
- **Density:** phones need fewer things per screen, not the same things smaller. Cut secondary text, merge small items, and give the remaining ones room.
- **Spacing:** vertical gaps between sections shrink less than you'd think; cramped sections read as one.

### 4. Check touch and reach

- Interactive targets at least 44×44px, with space between neighbours.
- Primary actions within thumb reach on the first screen when they matter.
- Nothing important only on hover.

### 5. Check the in-between width

Tablet (around 768) is where most layouts fail: too wide for the phone layout, too narrow for the desktop one. Decide it on purpose. Often the right answer is the phone layout with more room, or a two-column version of something that's three columns on desktop.

### 6. Capture and judge

Capture all four widths and check one question at each: **is the most important thing still the most visible?** Then run `/responsive-audit` for defects.

## Acceptance criteria

- Every section has a written behaviour (stays, moves, re-crops, shrinks, recomposes, disappears) for its key elements at phone and tablet.
- At 390 wide, each section's most important element is visible without scrolling past something less important.
- Images are cropped for each width where the subject matters, not only scaled.
- No headline word breaks mid-word; touch targets are at least 44px.
- The 768 layout was designed, not inherited.

## Common failure modes

- **Stack by default.** Every multi-column section becomes a single column in source order, regardless of importance.
- **Shrink everything.** The desktop composition at 40% scale: tiny type, tiny images, the same number of elements.
- **Hiding content that matters** to save space, instead of recomposing it.
- **Keeping decoration that only worked at desktop width:** an illustration that now sits alone between two sections.
- **Forgetting tablet:** the phone layout stretched to 768, or the desktop layout crushed to it.
- **Testing with placeholder content,** so real names, prices and translations break the layout later.

## Final self-review

- Did I decide each key element's behaviour at phone and tablet, rather than letting it stack?
- Is the most important thing visible first at 390?
- Did the images get crops, not just smaller sizes?
- Does 768 look designed?
- Did I run `/responsive-audit` afterwards for defects?

## Copyable instruction

```text
Art-direct this layout for phone and tablet; don't just stack the desktop columns.
1. Capture it at 390, 768, 1280 and 1920 wide.
2. For each section, rank its elements: what must be seen first, what supports it, what's optional.
3. For each key element, decide its behaviour at phone and tablet: stays, moves, re-crops,
   shrinks, recomposes (e.g. grid to row, table to stacked rows) or disappears. Write it down first.
4. Set headline size, density and spacing per width; phones get fewer things, not smaller things.
5. Keep touch targets at least 44px and nothing important hover-only.
6. Design 768 on purpose.
Verify by capturing again: at each width the most important thing must be the most visible.
```
