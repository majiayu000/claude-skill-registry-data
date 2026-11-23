---
name: charles-unreasonable-craft
description: Award-level web/app design, no AI slop. Use when the user wants design that could win Awwwards Site of the Day or an Apple Design Award, says it should "wow" or look stunning, premium, or world-class, says it can't look AI-made, or asks for a site, landing page, app screen, prototype, redesign, animation, or polish pass held to that bar. Not for routine UI fixes or small tweaks.
effort: max
---

# Unreasonable Craft

Go above and beyond with the design. Don't settle for the first idea, or for what you think counts as "good" design. That's AI slop. Push past what you think is creatively possible. Hold an uncommon, excessively high bar for craft and attention to detail, with unreasonable standards. Violating the letter of this skill is violating its spirit.

**The bar:** good enough to win Site of the Day on awwwards.com (for websites) *and* an Apple Design Award (for apps). It really needs to be that good. Anything less falls short, and you say so.

Paths here are relative to this skill's folder. The scripts need Node 18+, ffmpeg, and Google Chrome; their packages are in `scripts/node_modules` (if that's missing, run `npm install --prefix <this skill's folder>/scripts`).

## Load first

- **`interface-craft`** (Josh Puckett's Interface Craft), every time. In Claude Code, load it with the Skill tool. Elsewhere, read `../interface-craft/SKILL.md`, then the references it points to for the task.
- **Disney's 12 principles of animation**: squash and stretch, anticipation, staging, straight-ahead vs. pose-to-pose, follow-through and overlapping action, slow in / slow out, arcs, secondary action, timing, exaggeration, solid drawing, appeal. Apply them to UI motion on purpose, and be able to name which principle each animation uses.
- When they fit: `apple-design` (physical, interruptible motion and materials), `animate` / `animate-expo` (building motion), `emil-design-eng` (component polish). They sit next to this skill (`../<name>/SKILL.md`).

## Design from a system

Everything you make should come from one coherent system, and you should stay faithful to it. To find that system, in order:

1. **The project's design system** (tokens, theme, components, style guide), if there is one.
2. **Otherwise, the project's existing UI.** Reuse what's already there so the new work feels like it always belonged.
3. **Otherwise (a new project), one you invent.** Build a rough system from the chosen direction (color tokens, type, spacing, radii, elevation, motion, a few core components), write it down as tokens, and design from it.

Be bold *within* the system. Fill gaps in its own language, propose changes instead of drifting silently, and treat anything off-system as a bug.

## Track it

Copy this checklist into your plan or todo list and tick it off as you go. The work isn't done while a box is open.

```
- [ ] Explore: 3+ directions rendered side by side; one picked, with reasons
- [ ] System: found, inferred, or invented, and written down as tokens
- [ ] Assets: generated with today's best models, art-directed, optimized
- [ ] Polish: every value on purpose, copy in the user's voice, every screen size
- [ ] Verify: captured, measured, and read frame by frame
- [ ] Critique: one round by a fresh critic (more only if the user asked), fixes verified
- [ ] Final pass: zero mistakes
```

Keep a design log in the project: the direction and why, the system, every critique round's scores and fixes, and open issues. Use the project's own place for design reviews if it has one (such as `docs/reviews/`); otherwise create `docs/design/<topic>-<date>/`. Long sessions get summarized, and the log is how you keep your place: after a summary or a restart, reread this file and the log before going on.

## 1. Breadth first: explore every direction

Before committing to anything, run a breadth-first search over the possible design decisions. For each axis, write down several distinct options, including at least one creative risk that might take things somewhere unexpected:

- Concept and narrative: what feeling or metaphor holds the whole thing together?
- Layout and composition, grid, rhythm, negative space
- Typography: faces, scale, leading, tracking, numerals
- Color: palette, neutrals, contrast, light/dark behavior
- Motion: entrances, transitions, gestures, interruptibility, and which signature moment people will remember
- Interaction and micro-interactions, plus states (empty, loading, error, success)
- Texture, depth, materials, imagery, iconography

**Prefer creative risks over the conventional.** If an option is what "everyone else's AI" would produce (centered hero with a gradient blob, generic card grid, default Inter at default tracking, fade-up-on-scroll for everything), treat it as a red flag, not a safe pick. Name the obvious choice so you can deliberately go past it.

**Render the directions; don't just describe them.** For a new page, screen, or product, build at least three genuinely different directions as quick, rough prototypes and put them side by side on one comparison page. Problems a description hides show up the moment it's rendered.

Spend a real amount of time here brainstorming and planning how to knock this out of the park, before you polish anything. Then pick the direction(s) and state why each one beats the alternatives. When the user wants to choose, show them the comparison page with your recommendation. On a new project, turn the chosen direction into the system (see Design from a system) before designing any screens.

## 2. Generate assets that bring the vision to life

Don't settle for stock, placeholder, or CSS-only stand-ins when a generated asset would make the vision land. That includes imagery, textures, illustrations, video, 3D, sound design, voice, and music.

Find the keys yourself (fal, Google / Gemini's Nano Banana, ElevenLabs, OpenAI, Replicate, and similar), and use the latest and best models as of today's date, never a model from memory. Read `references/assets.md` for how to find keys without exposing them, pick models, art-direct the results, and ship them light.

## 3. Depth: polish to an extreme

Once the direction is set, go extremely deep on polish. This covers **everything**: animations, transitions, alignment (optical as well as mathematical), spacing, colors, typography, icons, borders, shadows, radii, states, edge cases, responsive behavior, and reduced motion. Literally everything.

- Every value should be chosen on purpose. No framework defaults left in by accident.
- Every animation should have a purpose, a named principle, a tuned curve and duration, and a clean interruption path.
- Consistency is the biggest sign of care. Anything that's the odd one out reads as a bug.

**Copy: say less.** Cut redundancy. Every heading, label, and line of body text has to earn its place. If the design already says it, the text shouldn't repeat it. No subtitle that restates the title, no description that paraphrases the button, and no "feature" text that a visual already shows.

**Copy: sound like the user wrote it, not AI.** Write in the user's voice. Learn it from the project's voice or tone guide if there is one, otherwise from text they wrote themselves: existing product copy, the README, their own messages. Match their vocabulary, rhythm, and directness (not their typos), and keep it specific and concrete, with a point of view. It should never read as AI-written, and what reads as AI-written keeps changing, so judge against *today's date*, not what read as AI six months ago. Check the current date. If you're unsure what currently reads as machine-written, search for recent discussion of AI writing tells before you write the copy. When a phrase comes too easily, it's probably a cliché.

**Every screen size.** It has to be award-level at every size, not just the one you designed at. Check phone, tablet, laptop, and wide desktop, plus the awkward widths in between (e.g. 360, 390, 768, 1024, 1280, 1440, 1920+). For native apps, check the smallest and largest devices and Dynamic Type. Recompose layouts for each size class rather than just shrinking them. Type scale, spacing, motion distances, and touch targets should all adapt. Hover-only interactions need a touch equivalent.

## 4. Verify every frame: measure, don't eyeball

When the design pass is done, verify **every page, every animation, every detail, frame by frame**, against this bar. Don't assume anything works, and don't trust your eye: it misses the 1–2 pt errors that make a design feel off. Read `references/verification.md`, then:

- Capture everything at full resolution: every page, state, theme, and screen size (`scripts/web-frames.mjs` for the web, `scripts/sim.sh` for the iOS Simulator).
- Read every animation as a contact sheet, frame by frame, including the in-between frames, not just the first and last (`web-frames.mjs --motion`, or a `sim.sh` recording through `scripts/sheet.mjs`).
- Measure spacing and alignment from the captures with `scripts/edges.mjs`, against the checks in the reference.
- For each screen, ask honestly: *would this win an Apple Design Award? Would it get Site of the Day on Awwwards?* If the honest answer is "not yet", write down exactly what's holding it back.

## 5. Critique: one round unless the user asks for more

Read `references/critique.md`. Have a fresh critic, with no stake in the work, score it harshly against the real juries' criteria (Awwwards for sites, the Apple Design Award categories for apps). Fix what it finds, biggest first, and verify the fixes. That's one round. Do one round unless the user asks for more, as a number of rounds or a bar ("keep going until it's a 9"), and then do what they asked. Naming the award as the goal ("so it could win Site of the Day") isn't a request for more rounds; every job aims there.

When you stop, report the score, what you fixed, the moments that make someone say "wow" (or that there aren't any yet), and what still stands between the work and the bar. "Clean" and "fine" don't meet it, so say so plainly and let the user decide whether to go another round.

## 6. Final pass: zero mistakes

Sweat the details. Before calling it done, do one last slow, complete pass over everything. Assume a mistake is hiding somewhere and hunt for it until there are no mistakes left:

- No console errors or warnings, failed requests, broken links, missing or unoptimized assets, layout shift, or flashes of unstyled content (`web-frames.mjs` writes these to `console.txt`)
- No typos, inconsistent capitalization, widows or orphans, or leftover placeholder text
- Nothing invented and presented as real: no made-up stats, customers, reviews, or testimonials
- Correct metadata, favicon, social preview image, and page titles
- Accessibility basics: contrast, focus states, alt text, reduced motion
- Performance is smooth: 60fps+ animations and fast first paint

## Red flags: you're settling

| Thought | Reality |
|---|---|
| "This looks good enough" | Good enough is slop. The bar is award-winning. |
| "This is the standard pattern for this" | Standard is what everyone ships. Explore past it. |
| "I'll pick the first strong idea" | You skipped the breadth-first search. Go back. |
| "Describing the directions is enough" | Render them. Problems hide in descriptions. |
| "The animation works" | Did you check it frame by frame? Which Disney principle does it use? |
| "It looks right to me" | Measure it. The eye misses the 1–2 pt errors the user will notice. |
| "It's aligned, the numbers match" | Optical alignment beats mathematical alignment. Look again. |
| "I verified the main page" | Every page, every state, every animation, at every screen size. |
| "I'll score it myself" | You're the least objective critic there is. Use a fresh one. |
| "A little more copy will explain it better" | If it needs explaining, fix the design. Cut the text. |
| "This phrasing sounds polished" | Polished-sounding is often today's AI tell. Would the user say it this way? Make it specific. |
| "It looks right on my viewport" | Check the awkward widths and the smallest device. |
| "This custom value looks better than the token" | Stay on-system. Propose a change to the system instead of a one-off. |
