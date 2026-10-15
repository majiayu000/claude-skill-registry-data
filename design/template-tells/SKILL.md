---
name: template-tells
description: Find the tells that make a website or interface look generated, templated or low-effort - in the copy, the visual design and the code - and replace each one with something specific to the product. Scans the source with a script, reviews screenshots by eye, and returns a ranked list of fixes. Use when a site "looks like every other AI-built site", before a launch, or when reviewing generated UI or copy.
---

# /template-tells

A site looks generated when every decision in it is the default one: the purple gradient, the three icon cards, the headline that could sell any product. No single default is wrong. The tell is that nothing was chosen. This skill finds the defaults and replaces each with a decision.

## What you're looking for

A **tell** is a pattern that appears because it's the easiest output, not because it serves this product. Judge each one with a single question: **could this appear, unchanged, on a competitor's site?** If yes, it's a tell.

### In the copy

- **Vocabulary of nothing:** unlock, elevate, seamless, supercharge, empower, robust, cutting-edge, next-level, world-class.
- **Stock openers:** "In today's fast-paced world", "Whether you're a startup or an enterprise", "Look no further", "Say goodbye to…".
- **The not-just construction:** "It's not just a tool — it's a partner." State the second half on its own.
- **Tricolons everywhere:** "Fast. Simple. Powerful." Three adjectives are a sign no one picked one.
- **Unmeasured numbers:** "10x faster", "thousands of happy teams", "in seconds". Real numbers have units, dates and sources.
- **Placeholders shipped as content:** Lorem ipsum, John Doe, Acme, "Feature one", example.com.
- **Generic buttons:** Get started, Learn more, Submit. A button names its action and its object: "Create workspace", "Compare plans".
- **Emoji as bullets** and ✨ to mean "AI".
- **Em dashes** in every other sentence, and headings phrased as questions the reader never asked.

### In the visuals

- **The default gradient:** purple to blue or pink, behind the hero or inside the headline text.
- **Glass on everything:** backdrop blur on cards, nav, modals and buttons at once.
- **Glow and blobs:** coloured shadows around cards, and blurred colour blobs floating behind the hero.
- **The three-up icon grid:** three cards, each an icon, a two-word title and one line, whether or not there are really three parallel things.
- **One card for everything:** the same large radius and large shadow on every surface, so nothing has a role.
- **Everything centred:** every section is a centred heading, a centred paragraph and a centred button.
- **One typeface, one weight system:** Inter at 400 and 600 everywhere; no type decision was made.
- **Stock social proof:** a logo bar of companies that aren't customers; testimonials with five stars, a first name and a stock avatar.
- **Bento grids and 3D blobs** used as decoration rather than to show anything.
- **Motion as garnish:** every section fades up on scroll by the same amount at the same speed.

### In the code

- Comments that narrate the code ("// Handle the click") instead of explaining why.
- `any`, leftover `console.log`, unused props and variants that were generated "just in case".
- Div soup where a `button`, `nav`, `ul` or `label` belongs.

## 1. Scan the source

Save this as `tells.mjs` in a scratch directory (not in the project) and run it on the source folders:

```
node tells.mjs ./src
```

It lists candidates by group, with file and line. It finds candidates only: a match is a question, not a verdict.

```js
// Template tells: scans source files for the phrases, class patterns and habits that make a site
// read as generated or templated. It finds candidates; a person (or you) decides what to change.
import fs from "node:fs";
import path from "node:path";

const roots = process.argv.slice(2);
if (!roots.length) {
  console.error("usage: node tells.mjs <dir-or-file> [more…]");
  process.exit(1);
}
const EXT = /\.(tsx|jsx|ts|js|html|md|mdx|astro|vue|svelte|css)$/;
const SKIP = /(^|\/)(node_modules|\.next|dist|build|out|\.git|coverage|public)(\/|$)/;

// [id, group, pattern, why]
const RULES = [
  // Copy: the vocabulary of nothing in particular.
  ["buzzword", "copy", /\b(unlock|unleash|elevate|supercharge|empower|revolutioni[sz]e|game[- ]chang\w*|next[- ]level|cutting[- ]edge|state[- ]of[- ]the[- ]art|seamless(ly)?|effortless(ly)?|robust|leverag\w+|synerg\w+|harness the power|take \w+ to the next level|world[- ]class|best[- ]in[- ]class)\b/i, "Says nothing a competitor couldn't also say. Replace with the specific thing it does."],
  ["opener", "copy", /\b(in today'?s (fast[- ]paced|digital|modern) world|whether you'?re an? .{1,40} or an?|look no further|we'?ve got you covered|say goodbye to|say hello to|imagine a world)\b/i, "A stock opener. Start with the claim instead."],
  ["not-just", "copy", /\b(isn'?t|is not|it'?s not) just an? [^.]{1,40}[—,-]+ ?(it'?s|it is)\b/i, "The \"not just X, it's Y\" construction. State Y."],
  ["dive", "copy", /\b(dive (in|into|deep)|deep dive|delve|embark on|journey)\b/i, "Filler verb. Say what the reader will do."],
  ["vague-number", "copy", /\b(10x|100x|lightning[- ]fast|blazing(ly)?[- ]fast|in seconds|thousands of (happy )?(users|customers|teams))\b/i, "An unmeasured number. Use a real one, with its unit and source, or cut it."],
  ["placeholder", "copy", /\b(lorem ipsum|dolor sit amet|john doe|jane doe|acme( corp| inc)?|feature (one|two|three|1|2|3)|your (company|product|brand) (name|here)|example\.com|foo ?bar|user@email)\b/i, "Placeholder content shipped as content."],
  ["sparkle", "copy", /[✨🚀🔥💡⚡️🎉🙌💯]/u, "Emoji as decoration in interface copy. Remove, or use an icon that means something."],
  ["cta-generic", "copy", />\s*(get started|learn more|click here|read more|submit|sign up now|try it free)\s*</i, "A generic button label. Name the action and the object: \"Create workspace\", \"Read the pricing\"."],
  // Visual: defaults that carry the whole design.
  ["gradient-text", "visual", /bg-clip-text[^"'`]*text-transparent|text-transparent[^"'`]*bg-clip-text|-webkit-background-clip:\s*text/, "Gradient-filled headline text. Usually a substitute for a type decision."],
  ["purple-gradient", "visual", /from-(purple|violet|indigo|fuchsia)-\d{3}[^"'`]*(via|to)-(pink|blue|purple|violet|indigo|cyan)-\d{3}/, "The default purple-to-blue/pink gradient."],
  ["glass", "visual", /backdrop-blur(-\w+)?|backdrop-filter:\s*blur/, "Frosted glass. Fine once, with a reason; a tell when every surface has it."],
  ["glow", "visual", /shadow-(purple|violet|indigo|blue|pink|cyan)-\d{3}\/\d+|drop-shadow-\[0_0_|box-shadow:\s*0 0 \d{2,}px/, "Coloured glow shadows as decoration."],
  ["blob", "visual", /blur-3xl|blur-\[1\d{2}px\]|filter:\s*blur\((6|7|8|9)\d|filter:\s*blur\(\d{3}/, "Blurred colour blobs behind the hero."],
  ["uniform-radius", "visual", /rounded-(2xl|3xl)[^"'`]*shadow-(lg|xl|2xl)/, "The same large-radius, large-shadow card everywhere."],
  ["icon-grid", "visual", /grid-cols-3[^"'`]*gap-\d+[\s\S]{0,200}(Icon|<svg)/, "Possible three-up icon grid. Check whether the three items are really parallel."],
  ["center-all", "visual", /text-center[^"'`]*mx-auto[^"'`]*max-w-(2xl|3xl|4xl)/, "Centred hero block. Fine once; a tell when every section is centred."],
  ["stars", "visual", /(★★★★★|⭐️?⭐️?⭐️?⭐️?⭐️?|rating[=:]\s*\{?5\}?)/, "Five stars on every testimonial."],
  // Code: generated-code habits.
  ["narrating-comment", "code", /\/\/\s*(this (function|component|hook) (will |is used to )?|handle the |create a |define the |import (the )?|render the |return the )/i, "A comment that narrates the code. Say why, or delete it."],
  ["any", "code", /:\s*any\b|as any\b/, "An `any` that hides a type decision."],
  ["console", "code", /console\.log\(/, "A leftover console.log."],
];

const files = [];
const walk = (p) => {
  if (SKIP.test(p)) return;
  const st = fs.statSync(p);
  if (st.isDirectory()) for (const f of fs.readdirSync(p)) walk(path.join(p, f));
  else if (EXT.test(p)) files.push(p);
};
roots.forEach(walk);

const hits = [];
for (const f of files) {
  const lines = fs.readFileSync(f, "utf8").split("\n");
  lines.forEach((line, i) => {
    for (const [id, group, re, why] of RULES) {
      const m = line.match(re);
      if (m) hits.push({ id, group, file: f, line: i + 1, match: m[0].trim().slice(0, 60), why });
    }
  });
}

const byId = new Map();
for (const h of hits) byId.set(h.id, [...(byId.get(h.id) ?? []), h]);
for (const group of ["copy", "visual", "code"]) {
  const rules = RULES.filter((r) => r[1] === group && byId.has(r[0]));
  if (!rules.length) continue;
  console.log(`\n## ${group}`);
  for (const [id, , , why] of rules) {
    const list = byId.get(id);
    console.log(`\n${id} · ${list.length} · ${why}`);
    for (const h of list.slice(0, 8)) console.log(`  ${h.file}:${h.line}  "${h.match}"`);
    if (list.length > 8) console.log(`  … and ${list.length - 8} more`);
  }
}
console.log(`\n${files.length} files scanned, ${hits.length} candidates across ${byId.size} tells.`);
```

## 2. Look at it

Numbers miss most visual tells. Take screenshots of every page at desktop and phone width (`/responsive-audit`'s script does this) or open the site, and go section by section:

1. **Cover the logo.** Could this page belong to another company in the same market? Which sections would survive a find-and-replace of the name?
2. **Read only the headings.** Do they say anything specific: a number, a name, a claim that could be wrong?
3. **Squint.** Is every section the same shape (centred text, then cards)? Where is the one place the design commits to something?
4. **Count the effects.** How many surfaces blur, glow, gradient or float? More than one or two is a system of defaults.
5. **Check the people and numbers.** Are the testimonials from people who exist? Are the stats real, dated and sourced?

## 3. Report

Rank findings by how much they make the site feel generic, not by how many times they appear. For each one:

- **Where:** page and section (and file:line when you have it).
- **Tell:** what it is, in a few words.
- **Instead:** the specific replacement, written out. Not "make the copy more specific" but the new sentence. Not "rethink the hero" but what the hero shows instead.

```
1. Home · hero — gradient headline + "Supercharge your workflow"
   Instead: solid ink headline, set larger, with the actual claim:
   "Deploys in 41 seconds, from any branch, to 32 regions."
2. Home · features — three icon cards (Fast / Secure / Scalable)
   Instead: one screenshot of the deploy log with three annotations
   pointing at the parts that are fast, secure and scalable.
3. Pricing · CTA — "Get started"
   Instead: "Start the free plan" and "Talk to sales" as a quieter link.
```

End with **the one decision** that would do the most: usually a single typeface change, a real product image instead of an illustration, or a headline rewritten around a number.

## 4. Fix

If asked to fix, work from the top of the ranked list and change the source directly. Rewrite copy with real specifics; ask the user for facts you don't have (numbers, names, dates) rather than inventing them. Re-run the scan and the screenshots afterwards and report what's left.

## Rules

- **Don't replace one default with another.** Swapping a purple gradient for a teal one fixes nothing. The replacement has to come from the product: its data, its users, its material.
- **Keep what's chosen.** Frosted glass on the one floating toolbar that needs to show what's under it is a decision, not a tell. Say so and move on.
- **Never invent facts.** A fake specific number is worse than an honest vague one.
