---
name: nick-visual-design-review
description: Visual UI review, browser-based design QA, and product-effectiveness critique for Nick's apps using Chromium/Playwright. Use when reviewing a live page or deploy to judge not just visual polish, but whether the interface supports clarity, trust, activation, conversion, responsiveness, and the product's strategic wedge. Best used after build/deploy to push a UI from acceptable to excellent with evidence from screenshots and browser inspection.
---

# Nick Visual Design Review

Use this as the visual QA companion to `nick-design-director`.

## Core job

Review the real rendered interface and judge whether it helps the product win.

Do not stop at "looks nice" or "looks generic." Evaluate whether the UI:
- communicates value quickly
- supports the core workflow
- builds trust
- reduces activation friction
- strengthens conversion moments
- feels intentional on desktop and mobile

## Non-negotiables

- Review the actual rendered interface, not just code.
- Check desktop and mobile views.
- Use screenshots as evidence.
- Call out generic/template-looking UI directly.
- Give specific fixes, not vague taste opinions.
- Judge product effectiveness, not just aesthetics.
- Be honest when the UI is polished but strategically weak.

## Strategic review lens

When possible, review against these inputs:
- ICP / buyer
- end user vs economic buyer
- core workflow
- product wedge
- trust sensitivity
- activation moment
- monetization / conversion moment

If these are unclear, state the assumptions.

## Required workflow

1. Open the target page in Chromium/Playwright.
2. Capture desktop screenshot.
3. Capture mobile screenshot.
4. Review first impression and value hierarchy.
5. Review activation/conversion clarity.
6. Review trust, readability, composition, and interaction cues.
7. Review responsiveness and mobile intent.
8. Produce critique with prioritized fixes.
9. Re-review after improvements when needed.

## What to evaluate

### 1) First impression
Check:
- does the page feel credible in the first few seconds?
- is the product type obvious?
- is the main promise clear?
- does it feel like a real product or a starter template?

### 2) Value hierarchy
Check:
- can the eye tell what matters first?
- is the headline/value message specific enough?
- are supporting elements helping or competing?
- is there a clear focal path?

### 3) Activation clarity
Check:
- is the next step obvious?
- do onboarding/start states reduce friction?
- does the user know how to get to first value?
- are empty states useful or dead?

### 4) Conversion clarity
Check:
- are CTAs clear and appropriately weighted?
- does the page earn trust before asking for commitment?
- are offer/pricing/demo/request actions visually and strategically supported?
- is there unnecessary friction at the moment of action?

### 5) Trust and credibility
Check:
- does the interface feel safe, accurate, and deliberate?
- are money, data, approvals, or sensitive actions presented with enough care?
- do labels, numbers, and confirmations feel trustworthy?
- are there signs of sloppiness that reduce confidence?

### 6) Composition and polish
Check:
- spacing rhythm
- typography hierarchy
- panel/card balance
- component consistency
- visual restraint vs noise
- whether the screen feels composed instead of assembled

### 7) Mobile quality
Check:
- spacing collapse on small screens
- tap target size
- stacked layout clarity
- readability without zooming
- CTA visibility
- whether the product still feels intentional on mobile

## Product-type review rules

### Landing pages / marketing pages
Review for:
- specificity of headline and subhead
- credibility / proof placement
- objection handling
- CTA timing and weight
- section flow
- whether the design supports conversion rather than just looking modern

### SaaS dashboards / app surfaces
Review for:
- clarity of core workflow
- usefulness of dashboard modules
- data hierarchy
- scan speed
- next-action clarity
- whether the UI helps users accomplish work faster

### Fintech / admin / trust-heavy flows
Review for:
- calmness and control
- precision in labels and numbers
- safe-feeling form/action flows
- confirmation quality
- trust cues around sensitive actions
- whether the design feels reliable enough to act on

## Default output

Use this structure unless there is a better fit:

### Overall verdict
- premium and effective / polished but weak / usable but generic / needs major work

### What is working
- strongest elements
- what already feels credible, clear, or premium

### What is weak or generic
- where the UI feels template-like, confusing, low-trust, or low-conviction

### Product-effectiveness issues
- value clarity
- activation friction
- conversion friction
- trust issues
- workflow confusion

### Desktop issues
- key desktop-specific problems

### Mobile issues
- key mobile-specific problems

### Top fixes in priority order
- specific design/UX changes to make
- prioritize changes that most improve trust, activation, and clarity

### Screenshot artifacts
- desktop screenshot
- mobile screenshot
- any additional evidence

## Quality bar

A strong review should:
- distinguish polish from actual product effectiveness
- identify whether the UI helps the product wedge land
- explain why something feels generic, not just that it does
- surface trust/conversion/activation problems clearly
- provide fixes the build/design skill can actually use

## References

Read these as needed:
- `references/review-lens.md` for visual evaluation criteria
- `references/mobile-review.md` for mobile-specific checks
- `references/premium-vs-generic.md` for quality bar guidance
- `references/report-template.md` for final critique structure

## Bundled scripts

- `scripts/init_visual_review.sh` — create a visual review report stub
- `scripts/generate_ui_fix_plan.sh` — create a prioritized UI improvement plan
