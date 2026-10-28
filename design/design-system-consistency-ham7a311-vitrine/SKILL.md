---
name: design-system-consistency
description: Before adding a new style, component or pattern, look for the one the project already has and decide whether reusing it is right. Covers buttons, cards, headings, colours, radii, shadows and spacing, and flags the fifth card treatment or the new shade of purple before it ships. Use before building any new UI in an existing project, and when reviewing a change that adds styles.
---

# /design-system-consistency

Most visual inconsistency isn't a bad decision; it's a forgotten one. Someone needs a card, doesn't find the existing card, and writes a new one with a slightly different radius, border and shadow. Repeat that for a year and the product has five cards, four greys, three heading styles and two primary buttons. The site looks generated, because nothing in it was chosen twice.

This skill is the habit of looking before inventing.

## Purpose

Keep a product's visual language small and consistent by reusing existing patterns where they fit, and by making any genuinely new pattern a deliberate, named decision.

## Use when

- You're about to add a new section, component, card, button, badge or colour to an existing project.
- Reviewing a change that adds CSS or new class combinations.
- A page "looks off" next to the others and you suspect drift.

## Don't use when

- The project has no design system yet. Start one with `/theme-system`.
- You're intentionally designing a one-off moment (a hero, a campaign page) and have decided so. Note it, and keep it scoped to that place.

## Inputs

- The thing you're about to add, described in one sentence ("a highlighted card for the company plan").
- The project's tokens file or theme (CSS variables, Tailwind theme, design tokens).
- The project's existing shared components: buttons, cards, headings, inputs, badges.
- Two or three existing pages that are closest to what you're building.

## Process

### 1. Name what you need, not how it looks

"A way to make one plan read as the higher tier", not "a purple glowing card". The need leads to existing options; the look leads straight to new CSS.

### 2. Search for the existing pattern

Look in this order:

1. **Shared components.** Is there already a button, card, heading block or badge that does this job?
2. **Neighbouring pages.** How did the closest existing page solve the same problem?
3. **Tokens.** Which colour, radius, spacing and shadow values exist?

To see what's actually in use, this small helper lists the colours, radii and shadows that appear in the source, most frequent first. It's an aid for the search, not the point of the skill. Save it as `inventory.mjs` in a scratch directory and run `node inventory.mjs ./src`:

```js
// Lists colours, radii and shadows used in source files, most frequent first.
import fs from "node:fs";
import path from "node:path";

const files = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === "node_modules" || e.name.startsWith(".")) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (/\.(css|tsx?|jsx?)$/.test(e.name)) files.push(p);
  }
})(process.argv[2] ?? "./src");
const count = (re) => {
  const m = new Map();
  for (const f of files) for (const x of fs.readFileSync(f, "utf8").match(re) ?? []) m.set(x, (m.get(x) ?? 0) + 1);
  return [...m].sort((a, b) => b[1] - a[1]).slice(0, 25);
};
console.log("colours", count(/#[0-9a-fA-F]{6}\b|rgba?\([^)]*\)/g));
console.log("radii", count(/rounded(?:-[a-z0-9[\].]+)?|border-radius:\s*[^;]+/g));
console.log("shadows", count(/shadow(?:-[a-z0-9[\]/_.,()%-]+)?|box-shadow:\s*[^;]+/g));
```

Long tails in this output (a colour used once, a radius used twice) are usually drift worth reviewing.

### 3. Decide: reuse, extend or create

| Decision | When | What to do |
|---|---|---|
| **Reuse** | An existing pattern does the job. | Use it as it is. This is the usual answer. |
| **Extend** | It nearly does: it needs one variant or one prop. | Add the variant to the shared pattern, so everyone gets it. |
| **Create** | Nothing does the job, and the job is real. | Make it a named, shared pattern with tokens, not a one-off in a page file. |

Choosing "create" needs a sentence saying why reuse and extend don't work.

### 4. Check the new thing against the system

If you created or extended something, check:

- Does it use existing colour, radius, spacing and shadow tokens?
- Is it distinguishable from the existing patterns by its **role**, not by a slightly different value?
- Does it follow the same naming, file location and API style as its siblings?

### 5. Flag drift you find on the way

While searching, note near-duplicates (two card styles that differ by 2px of radius, three greys within a few percent of each other). Report them. Don't fix them in the same change unless asked; mixing cleanup into feature work makes both harder to review.

## Acceptance criteria

- The change uses existing components and tokens wherever they fit.
- Every new pattern has a written reason why reuse and extend didn't work.
- No new colour, radius or shadow value was added without becoming a token.
- Near-duplicates found during the search are listed.

## Common failure modes

- **Inventing by default:** writing new CSS before searching.
- **The near-duplicate:** a new card or button that's 90% the same as an existing one, with slightly different values.
- **Decoration as hierarchy:** adding a new glow, gradient or badge style to make one thing more important, when the system's size, weight and spacing could do it.
- **Treating the inventory as the job:** running a token scanner and stopping there, without deciding anything.
- **Over-abstracting:** turning a genuine one-off into a configurable shared component that nothing else uses.

## Final self-review

- What did I search before building, and what did I find?
- For each new style, why couldn't I reuse or extend an existing one?
- Are all values tokens?
- Does the new thing differ from its siblings by role, not by accident?
- Did I list the drift I found?

## Copyable instruction

```text
Before adding any new UI, look for what the project already has.
1. Describe what you need by its job ("make one plan read as higher tier"), not its look.
2. Search, in order: shared components, the closest existing pages, the design tokens.
3. Decide for each need: reuse an existing pattern (default), extend it with a variant, or create a new
   shared pattern. If you create, write one sentence on why reuse and extend don't work.
4. Use existing tokens for every colour, radius, spacing and shadow; add a token rather than a one-off value.
5. List near-duplicates you notice (similar cards, close greys) but don't fix them in this change.
Don't make something more important with a new glow, gradient or badge when size, weight or spacing can do it.
```
