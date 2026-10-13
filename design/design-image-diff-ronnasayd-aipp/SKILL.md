---
name: design-image-diff
description: >
  Use this skill whenever the user wants to compare a design mockup/wireframe/Figma screenshot
  with a frontend implementation screenshot to identify visual differences and generate a list
  of changes needed. Triggers include: "compare design with implementation", "find differences
  between design and code", "what's different from the mockup", "design review", "pixel comparison",
  "why doesn't my implementation match the design", "QA visual comparison", "design vs screenshot",
  or any time two images are provided where one is a design reference and the other is a rendered UI.
  Always use this skill when the user uploads two images and asks what needs to change to make
  one look like the other — even if they don't mention "design" explicitly.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Design Diff Skill

Compare a **design reference image** (Figma, Sketch, mockup, wireframe) with an **implementation screenshot** and produce a structured, actionable list of visual differences the developer needs to fix.

---

## When This Skill Applies

- User uploads two images: one design, one implementation
- User asks: "what's different?", "what needs to change?", "why doesn't it match?"
- Visual QA / design review workflows
- Any pixel-diff or layout comparison task

---

## Step-by-Step Process

### Step 1 — Identify which image is which

If the user hasn't labeled the images:

- **Design** image: typically has cleaner aesthetics, may show a Figma frame, may have annotations, or look like a polished mockup.
- **Implementation** image: typically looks like a browser/app screenshot, may have real content, browser chrome, or dev tool artifacts.

If it's truly ambiguous, ask the user: _"Which image is the design reference and which is the implementation?"_

### Step 2 — Systematic Visual Inspection

Analyze both images across these categories **in order**. Check each category even if it seems fine — differences hide in overlooked areas:

| #   | Category                     | What to look for                                                                |
| --- | ---------------------------- | ------------------------------------------------------------------------------- |
| 1   | **Layout & Spacing**         | Padding, margins, gaps between elements, overall page width/max-width           |
| 2   | **Typography**               | Font family, font size, font weight, line height, letter spacing, text color    |
| 3   | **Colors**                   | Background colors, text colors, border colors, icon colors, hover/active states |
| 4   | **Components**               | Buttons (size, radius, padding, shadow), inputs, cards, modals, badges          |
| 5   | **Imagery & Icons**          | Icon set, icon size, image aspect ratio, placeholder vs real images             |
| 6   | **Borders & Shadows**        | Border width, border radius, box shadows, dividers                              |
| 7   | **Alignment**                | Left/center/right alignment of text and elements, vertical centering            |
| 8   | **Responsive / Breakpoint**  | If visible, note differences in how content reflows                             |
| 9   | **Missing / Extra Elements** | Things present in design but absent in implementation, or vice versa            |
| 10  | **Micro-details**            | Opacity, cursor style, focus rings, scrollbar styling                           |

### Step 3 — Format the Output

Produce a structured diff report in this format:

---

## 🎨 Design Diff Report

### Summary

_One sentence overview of how close the implementation is._

### Differences Found

For each difference, output a block like this:

**[#] Category — Short title**

- 📐 **Design:** _what the design shows_
- 💻 **Implementation:** _what the current implementation shows_
- 🔧 **Fix:** _concrete, copy-paste-ready CSS or code suggestion when possible_

---

### Step 4 — Prioritization

After listing all differences, add a **Priority Summary** section:

```
🔴 High priority (visible, breaks design intent): #1, #3, ...
🟡 Medium priority (noticeable but secondary): #2, #5, ...
🟢 Low priority (minor polish): #4, ...
```

### Step 5 — Optional: Code Snippet Section

If the user's stack is known (React, Tailwind, plain CSS, etc.), add a **Quick Fix Snippets** section with ready-to-use code for the top 3 high-priority items.

---

## Output Principles

- **Be specific, not vague.** Instead of "the button looks wrong", say "button border-radius should be 8px, currently appears to be 0px".
- **Estimate values when exact values aren't visible** — use visual judgment and standard scales (4px grid, Tailwind classes, etc.). Flag estimates with `~`.
- **Never say "looks fine"** for a category without actually checking it.
- **Use developer language** — CSS property names, Tailwind class names, or design token names where appropriate.
- **Avoid subjective adjectives** like "ugly" or "bad". Be neutral and precise.

---

## Edge Cases

- **Low-resolution images**: Note that measurements are estimates and recommend the developer inspect with browser devtools.
- **Dark mode / theming**: If one image is dark mode and the other is light mode, flag this as a context difference before diffing.
- **Animated / interactive states**: Static screenshots can't capture hover states. If differences might be in interactive states, note this caveat.
- **Partial screenshots**: If only a section of UI is shown, scope the diff to what's visible and say so.
- **Design with annotations/redlines**: Use annotation values as ground truth for measurements.

---

## Example Output Snippet

**[1] Typography — Heading font weight**

- 📐 **Design:** `font-weight: 700` (bold heading, visually heavy)
- 💻 **Implementation:** `font-weight: 400` (regular weight, looks too light)
- 🔧 **Fix:** `h1 { font-weight: 700; }` or Tailwind: `font-bold`

**[2] Colors — Primary button background**

- 📐 **Design:** Vibrant blue, approximately `#2563EB`
- 💻 **Implementation:** Muted gray-blue, approximately `#6B7280`
- 🔧 **Fix:** `.btn-primary { background-color: #2563EB; }` or Tailwind: `bg-blue-600`

**[3] Spacing — Card internal padding**

- 📐 **Design:** ~24px padding on all sides
- 💻 **Implementation:** ~8px padding, content feels cramped
- 🔧 **Fix:** `.card { padding: 24px; }` or Tailwind: `p-6`
