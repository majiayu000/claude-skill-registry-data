---
name: design-md
description: "Create an agent-readable DESIGN.md design spec (colours, type, spacing, components, reasoning) before any visual build. Use when the user starts a visual build, asks for a design spec, or says 'DESIGN.md'."
category: Content Creation
license: MIT
version: 1.0.0
---

# DESIGN.md — agent-readable design specs

Learned 2026-10-18 from the getdesign.ai pattern (via @viktoroddy's list post): a DESIGN.md is a written description of a design's colours, type, spacing, components and the reasoning behind them, written for AI coding tools to follow. Same family as AGENTS.md / llms.txt. The failure mode it fixes: agent improvises generic aesthetics because no spec exists.

## The rule

Before building anything visual (site, page, one-pager, artifact, HyperFrames composition):

1. **Look for a DESIGN.md** in the project folder, then `.` (The AI Capitol master brand spec).
2. **If none fits the project**, draft one from a reference (see galleries below) or from an existing shipped artifact, in the format below. Short is fine — one page beats ten.
3. **Build to the spec.** Colours, typefaces, spacing scale and component rules in the spec override taste. If the build needs to deviate, say so and update the spec.
4. **Verify visually** (screenshot/render) against the spec before delivering: type pairing, colour usage, whitespace rhythm.

## DESIGN.md format (the getdesign.ai structure)

```md
# DESIGN.md — <project / brand name>

## Intent
What the design should feel like and why. One or two sentences. Name references
("private-bank document", "editorial magazine") instead of adjectives.

## Colours
- Ink / primary text: #...... (role, not just name)
- Accent: #...... (used sparingly — rules, highlights)
- Paper / background: #......
- Muted text, hairlines, washes: #...... each with its role
Rules: where the accent may appear, what never gets colour.

## Typography
- Display: <serif/sans, weight, sizes, line-height>
- Body: <face, weight, size, line-height>
- Labels: tracking/letter-spacing, case (e.g. small caps +2-3px tracking)

## Spacing & layout
- Page margins, section rhythm, hairline rules vs boxes, column logic
- The whitespace principle for this design (e.g. "air over density")

## Components
- Headings pattern (numbered sections, rules running off headings, etc.)
- Lists (marker style), tables/rows, buttons/CTAs, cards, footers

## Motion (if any)
- Easing, duration bands, what animates and what never does

## Voice in UI copy
- Sentence case vs title case, punctuation habits, words to avoid
```

## Reference galleries (single-element lookups, from the 2026-10-18 list)

Consult the matching gallery when stuck on one element instead of browsing general inspiration:

- DESIGN.md library for AI agents — https://getdesign.ai/
- Social post design — http://posts.design
- Bold mobile websites — http://loadmo.re
- Recent design, daily — http://recent.design
- UI animation & interaction details — http://60fps.design
- Hero sections — http://supahero.io
- Navbars — http://navbar.gallery
- CTAs that convert — http://cta.gallery
- Visual design archive — http://inspora.design

Note: getdesign.ai is a paid library (free tier has copy limits); its DESIGN.md files may be used in own/client projects but not redistributed. Write original specs in the same format rather than copying files verbatim.

## Master's brand spec

- A project or brand DESIGN.md at the workspace root holds the master brand spec for that brand. Use it for anything under that brand unless a project-level DESIGN.md overrides it.

## When to use

Use this skill when the task matches its description above and you need a repeatable, checked workflow rather than an improvised answer.

## Guardrails and quality checks

- Never fabricate facts, numbers, clients or results. Use only sources the user provides or verifies.
- Keep drafts as drafts until a human approves any external send, payment or commitment.
- Check the final output against the workflow above before delivering it, and state anything you could not verify.

## Output format and example

Deliver the result in the structure the workflow defines. Example request: "Use the DESIGN.md skill for my situation: [describe the business, audience and goal]." Example output: a completed, checked deliverable following every step above, with open questions listed at the end rather than guessed.
