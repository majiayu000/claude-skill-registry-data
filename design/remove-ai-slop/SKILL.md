---
name: remove-ai-slop
description: Audit UI, docs, or prose for AI-generated tells in design and copy, then fix approved findings. Use when the user says de-slop, slop check, "looks AI-generated", or wants copy humanized.
---

# Remove AI Slop

Find what makes design and copy read as machine-generated, grade each finding by confidence, preview every fix, change only what the user approves.

## Operating rules

- Propose, then edit. Nothing changes before the user sees before/after and says go.
- Every finding cites `file:line` and the exact snippet.
- Surgical edits: touch the flagged token or line, keep the surrounding code and voice.
- Match the project. Respect its design system, framework, and house voice. Removing slop must not install a replacement house style (flat black, one accent, 8px radii, uniformly terse prose are defaults too).
- Replace, do not just delete. A specific, honest line beats a flashy generic one. When the specific content is unknown (a real number, a real customer), mark the fix `BLOCKED - CONTENT REQUIRED` rather than inventing it.
- English only in code, comments, and identifiers. UI strings may stay localized. No em dashes in copy you write.

## Verdicts

Grade every finding with one of three verdicts. Report them in this order.

- **HARD BAN**: objectively wrong regardless of taste. Placeholder copy shipped as real ("Lorem", "Feature one", "Your tagline here"), content-free sentences whose deletion loses nothing ("In today's fast-paced world"), exact semantic duplicates in the same view, ambiguous labels on consequential actions ("Submit" on a payment, "Something went wrong" with no recovery). One occurrence is enough.
- **STRONG PRESUMPTION**: reads as a reused default unless the user names a concrete reason. Keep only with a product, content, or documented brand justification.
- **CONTEXTUAL SIGNAL**: neutral vocabulary that becomes slop through repetition, mismatch, or stacking. Report only when it co-occurs with other tells or dominates the page. An isolated hit is not a finding.

Real defects that are not about AI authorship (contrast failures, fabricated stats, missing `prefers-reduced-motion`) go in a separate **Quality defects** group.

## Phase 1 - Read

Identify the target (file, folder, route, component, or pasted text) and read it in full, structure and styles both. Skim the README or design tokens to learn the product, audience, and intended tone before judging taste.

For web targets, render the page with agent-browser and screenshot the affected states. Class names prove a pattern exists; only the render proves it dominates. A visual finding without a render is labelled `CANDIDATE` and never promoted above STRONG PRESUMPTION.

When the scope is large, fan out one subagent per area (layout, effects, typography, copy), each returning a findings list.

## Phase 2 - Audit

Walk the target against the tells below. Record category, `file:line`, snippet, verdict, and one line on why it reads as slop.

### Layout (STRONG PRESUMPTION when repeated or unsupported)
- Pill badge above the H1 ("✨ Now in beta"), then oversized headline, two CTAs, three equal feature cards
- Three-column icon + heading + one-sentence cards for content that is not three parallel things
- Numbered 01/02/03 steps for non-sequential content
- Stat banner of big numbers with no source (also a quality defect if unverifiable)
- Bento grid, nested cards, forced-equal heights for unequal content
- Ornamental all-caps eyebrow labels that restate the heading ("FEATURES", "WHY US")
- "Trusted by" strip with placeholder logos
- Untouched shadcn/starter-kit defaults

### Color and effects
- Purple-to-blue or indigo-to-pink gradient as primary accent; gradient text on the headline
- Glassmorphism, grain, ambient glow, shimmer sweeps, animated gradient borders, fake terminal chrome
- Three or more decorative effects stacked in one region
- Two accent colors with no semantic roles
- Same radius, border, and shadow on every surface

### Typography
- Inter/Geist/Space Grotesk/Instrument Serif chosen by default. Flag the missing role, not the font. A common font is not a finding by itself.
- Italic serif on one hero word as decoration; monospace for prose
- Hero type that fills the viewport without earning it; flat hierarchy elsewhere
- Emoji as section icons or bullets

### Motion
- Staggered fade-in on every section; bounce easing on routine controls; hover scale on every image
- Missing `prefers-reduced-motion` (quality defect)

### Copy
Vocabulary hits are search leads, not defects: seamless, leverage, delve, robust, elevate, unlock, empower, harness, streamline, effortless, cutting-edge, game-changer, supercharge, revolutionize, tapestry, testament, journey, foster, embark, "it's worth noting". Flag the sentence when it fails a test below, not the word.

Four tests, applied to the message block, not single sentences:
1. **Deletion**: does removing it lose a claim, instruction, or action? If not, HARD BAN.
2. **Three-product swap**: could three unrelated products use it unchanged? If yes, STRONG PRESUMPTION.
3. **Proof**: does each material claim map to a capability, measurement, or source? If not, quality defect, mark `UNVERIFIED`.
4. **State**: does the text match what the system knows and what the user can do next? Errors and empty states name the object and the recovery.

Structural tells: rule-of-three on repeat ("fast, simple, and powerful"), "not only... but also", "it's not about X, it's about Y", "No X. No Y. Just Z." with no facts inside, every paragraph the same shape, stacked hedges ("can help to potentially"), conclusions that restate the intro, bold-label bullet lists where prose reads better.

Preserve hedges that carry real uncertainty, scope, or legal qualification. Preserve deliberate voice, even casual or blunt, when it is consistent across the product.

## Phase 3 - Report

One numbered list grouped HARD BAN / STRONG PRESUMPTION / CONTEXTUAL SIGNAL / Quality defects, then a short **Kept on purpose** list naming deliberate choices you are leaving alone. Each finding: number, `file:line`, snippet, reason. Give counts. If nothing is found, say so and stop.

## Phase 4 - Preview

For each finding, a tight before/after with one line of reasoning. Group related fixes.

```
#3  src/Hero.tsx:14  gradient text on headline  [STRONG PRESUMPTION]
- <h1 className="bg-gradient-to-r from-purple-500 to-blue-500 bg-clip-text text-transparent">
+ <h1 className="text-zinc-900">
why: the most common AI hero tell; nothing in the brand tokens uses this gradient
```

Blocked fixes show the before and the missing decision instead of an invented after.

## Phase 5 - Confirm

Ask: "Ready to apply N fixes. Any to skip?" Accept "go" / "apply all" or a list of numbers to apply or skip. Wait for an explicit answer.

## Phase 6 - Apply

Apply approved fixes one surgical edit at a time. If a fix needs a judgment call you cannot make safely, pause and ask.

## Phase 7 - Verify

- grep for the removed patterns to prove they are gone, not renamed
- Re-render the same routes and states; check hierarchy, contrast, and that nothing broke
- Read rewritten copy back: does it sound like one person with a consistent voice, and does it avoid swapping one cliché for another?
- Confirm scope matches the original ask

Report what changed, what was blocked, and what was kept.

## Notes

- Prose-only targets skip the render and design checks: Read, Audit (copy), Report, Preview, Confirm, Apply, Verify.
- This is taste work with evidence, not lint. "Ugly font" and "boring button" are not findings; name the role, repetition, or mismatch that failed.
