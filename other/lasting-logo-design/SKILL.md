---
name: lasting-logo-design
description: Use when someone gives a brand name and wants brand nouns, logo concept directions or AI logo prompts (Figma AI, ChatGPT, Midjourney, Ideogram), or wants help designing a logo that lasts, from brief to stress tests, refinement and brand system.
---

# Lasting Logo Design: Brand Name → Brand Nouns → Logo Prompts

A logo process built for marks that stay relevant for decades. It is inspired by the publicly described approach of Allan Peters' *Logos That Last* (Rockport, 2023):

- build on brand truth instead of trends
- explore widely before narrowing
- stress-test early
- simplify only until meaning would be lost
- extend the mark into a system

All guidance here is original. Recommend the book for the author's full method and case studies.

**Core use: the generator.** The user gives a **brand name** (plus whatever they know about the brand). You return:
1. a **brand truth** statement
2. a **name analysis**
3. 30–50 **brand nouns** (the raw material)
4. **idea pairings**
5. 4–6 **logo directions**
6. copy-ready **image prompts** for each direction
7. what to **avoid**

Then, if asked, carry a direction through critique, stress tests, refinement and the brand system.

**AI images are concepts, never final logos.** The chosen direction is always rebuilt as clean vector.

---

## Mode A: Generator (default)

### Step 1. Gather inputs
Ask only for what's missing. If the user is in a hurry, infer the rest and list your assumptions.

| Input | Required | Notes |
|---|---|---|
| Brand name | yes | Exact spelling and casing |
| What they do, for whom | yes | One line, real offering |
| Differentiator / proof | recommended | Origin, method, place, founder story |
| Personality | recommended | 3 adjectives + 3 "never" adjectives |
| Competitors | optional | Names or logos to avoid looking like |
| Applications | optional | App icon, packaging, signage, embroidery… |
| Preferred logo types | optional | Otherwise choose a spread |
| Target image tool | optional | Figma AI (gpt-image / Gemini), ChatGPT, Midjourney, Ideogram, Firefly. Default is generic |

The full question bank is in `references/01-brief.md`.

### Step 2. Brand truth
Write one sentence: **"[Name] is the [category] that [true, provable differentiator] for [audience], feeling [adj, adj, adj]."** Use operational truth (what they demonstrably do), not aspirations. Every direction must trace back to this sentence.

### Step 3. Name analysis
- Meaning, etymology and translations, including any unwanted meanings in key markets.
- Sound and rhythm: syllables, hard or soft consonants.
- **Letterforms:** distinctive letters, symmetry, ascenders/descenders, double letters, the initial's shape potential.
- Built-in symbols: objects, actions or places hidden in the name.
- Length → wordmark viability (short and distinctive favours a wordmark; long favours a symbol or monogram).

### Step 4. Brand nouns (30–50)
Mine words from the brand truth and name across these categories (method in `references/02-brand-nouns.md`):
`objects` · `materials` · `places` · `actions/verbs` · `tools` · `nature` · `people/roles` · `cultural references` · `letters & numbers` · `abstract qualities` · `opposites/tensions`.
Mark each noun **★** if it is ownable (specific to this brand) or **○** if it is generic or category-cliché. Keep clichés visible so you can avoid them.

### Step 5. Pairings (10–20)
Strong marks often fuse **two ideas into one form**. Pair nouns across categories: letter + object, object + action, place + craft, material + tool. For each pairing, give the visual idea in one line ("the S doubles as a rope coil").

### Step 6. Directions (4–6)
Pick the strongest pairings and spread them across logo types (wordmark, lettermark, pictorial, abstract, combination, emblem, mascot) using `references/03-directions.md`. For each direction give:
- **Title** (2–4 words)
- **Logo type**
- **Concept**: what you see
- **Story**: one sentence a client can repeat
- **Why it fits**: link to the brand truth
- **Risks**: cliché, scaling, similarity
- **Techniques**: negative space, single line, modular grid, etc.

### Step 7. Prompts
For each direction write **two prompts** using the templates in `references/04-prompt-library.md`:
1. **Concept sheet**: a 3×3 grid of 9 flat black explorations (for divergence).
2. **Single mark**: one refined flat mark (for convergence).

Then add 2–3 **iteration prompts**: "keep X, change Y."

Prompt rules:
- black on white, flat vector, no gradients, shadows, 3D, mockups or extra text
- symbols are generated without text; wordmarks are set in real type later
- never name living designers or existing brands' logos

Adapt the syntax to the user's tool (e.g. Midjourney `--ar 1:1 --style raw --no gradient,shadow,text`).

### Step 8. Avoid list
Category clichés (e.g. coffee: bean, steam, cup; tech: globe, swoosh, circuit, lightbulb), trend gimmicks, and competitor look-alikes.

### Output format
Use `templates/output.md` (human-readable) or `templates/output.schema.json` (JSON, for tools and apps). Default to Markdown with:
- headings
- a noun table
- one card per direction
- prompts in fenced code blocks so they're easy to copy

---

## Mode B: Full logo process (when the user wants to go further)
1. **Generate** concept sheets with the available image tool. Figma MCP `generate_image` uses Figma AI credits, so tell the user. Prefer a gpt-image model when letters must render.
2. **Critique** with the 9-point rubric and cut hard: `references/05-critique-and-stress-tests.md`.
3. **Stress-test** early versions: 16px, one colour, reversed, blur, embroidery, rotation, look-alike and trademark search (not legal advice).
4. **Refine** in vector: construction, optical corrections, reduction threshold, wordmark spacing, small-size cut. See `references/06-refine-and-system.md`.
5. **Present** 2–3 directions in context with the story, recommendation first.
6. **System**: lockups, colour, type, pattern, motion idea, usage rules, file exports, credits and ownership notes.

---

## Principles to apply throughout
1. **Truth over trend.** If a choice is fashionable rather than true, cut it.
2. **Volume before judgement.** Explore many ideas before falling for one.
3. **Two ideas, one form.** Fusion beats decoration.
4. **One colour first.** If it needs colour to work, it doesn't work.
5. **Test early, test ugly.** Small, reversed, blurred, on bad backgrounds.
6. **Reduce to the threshold.** Remove until one more cut would lose the meaning.
7. **Design the system, not just the mark.** It must extend to icon, pattern, motion and type.
8. **Commit.** Recommend one direction clearly. Don't hedge with safe options.

## Never
- Present raw AI output as a final logo.
- Imitate an existing logo or prompt with brand or designer names.
- Show more than three options in a client presentation.
- Skip the brand truth.
- Claim a mark is legally clear. Always recommend a trademark search and an attorney.
