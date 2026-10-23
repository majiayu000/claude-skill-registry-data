---
name: aigent-asset-gallery-system
description: Build AIgent-style resource, prompt, repo, creator-stack, or operator-kit gallery pages with scroll chapters, sticky nav, mobile-safe reveals, plain-English descriptions, clickable external links, accurate counts, and premium 3D/Spline backgrounds.
---

# AIgent Asset Gallery System

Use this skill for pages that present lists of assets: repos, prompts, tools, creator stacks, operator kits, skills, or templates.

## Structure

1. Group assets into clear chapters.
2. Put a sticky top nav above the chapters.
3. On desktop, let the chapter header stick while the list scrolls.
4. On mobile, do not use a second sticky chapter header; the top nav is enough.
5. Cards reveal one at a time as the user scrolls.

## Count Rule

Never overstate inventory.

- Count cards from the rendered source.
- Compare stated count to actual count.
- Update both page copy and data source.

## Copy Rule

Descriptions should explain why a normal operator cares.

Bad:
`Vision-first DOM abstraction for browser workflows.`

Better:
`Lets an AI use websites even when normal automation breaks.`

## Card Rule

- The card title should be linked if there is a URL.
- Put the diagonal arrow beside the title, inside the same link.
- Do not create a dead icon button.
- Card click can expand details, but it must not block the title link.
- Tags should be short and scannable.

## Mobile Rule

- Active nav chip centers itself.
- Cards and headers appear early, not after the user has almost passed them.
- No horizontal page scroll.
- Body text stays readable.

## Background Rule

The 3D scene is atmosphere and orientation. It should not make cards harder to read. Increase the dark veil behind dense lists.

## Verification

Check:

- Actual card count.
- Every external link opens.
- Mobile nav scrolls horizontally.
- No sticky overlap.
- First card in each chapter appears with the chapter intro.
