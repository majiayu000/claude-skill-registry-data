---
name: readability
description: "Body copy sized and spaced for comfortable reading."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, typography]
    category: web
    related_skills: [web-design, typographic-scale, content-hierarchy]
    web_designer_stages: [copy, font]
---

# Readability Skill

Body copy sized and spaced for comfortable reading: large enough to read at arm's length, with enough leading for the eye to track from line to line, and lines short enough that the eye does not lose its place. This skill sets those measures for all body copy. It does not choose the typefaces, set the heading scale, or write the copy itself.

This skill is load-on-demand only. The web-designer coordinator loads it for its stages and it never auto-loads. It never contacts the user directly — the coordinator is the only router.

## When to Use

- For all body copy, articles, product descriptions and long forms.
- Especially on mobile, where small text fails first.
- When the copy stage needs body measures, or the font stage needs body size and leading recorded.
- When long text reads as a wall of dense text and the eye loses its place.
- When a page's body copy was set below 16px and needs bringing up to the minimum.

It is NOT for choosing fonts, setting heading sizes, or judging the finished page — the visual judger checks the measures and the content judger checks the copy.

## Prerequisites

- The run is active and the coordinator loaded this skill for the copy or font stage.
- The font decision is made, so body size and leading are set on the chosen body face.
- The copy stage has the page text, or the font stage has the scale to record against.
- The long-form content is known, so the measures are set for the longest text, not the shortest.

## How to Run

1. Set body text at 16–18px minimum, never below 16px.
2. Set line-height to 1.5–1.7.
3. Cap the measure with max-width or ch units, so lines run about 45–75 characters.
4. Check the measures at phone width first: small text fails on mobile before it fails on desktop.
5. Read a long passage at arm's length on phone and desktop: if the eye loses its place, the measure or the leading is wrong.
6. Watch for walls of dense text: long unbroken paragraphs need the measure and leading to carry them, and short paragraphs are no substitute for a cap.
7. Record body size, line-height and measure in the font stage record, and apply them to the pages in the copy stage record.
8. Re-check after any font change: a new body face can read smaller at the same size, so the minimum must hold on the chosen face.
9. Leave long text alone once the measures hold: no line that runs past the point where the eye loses its place.
10. Apply the measures to product descriptions and long forms, not only to articles.
11. Check the measure where the container is widest: very wide screens stretch lines past 75 characters unless the cap holds.
12. Confirm no body copy sits below 16px anywhere, including captions and helper text that reads as body.

## Quick Reference

- Body text: 16–18px minimum; never below 16px.
- Line-height: 1.5–1.7.
- Line length: about 45–75 characters (50–75 per NN/g-derived guides; Butterick 45–90).
- Judger flags: body under 14px, tight leading, lines over 80 characters.
- Cap measure with max-width or ch units.
- Check phone width first: small text fails on mobile before it fails on desktop.
- Read at arm's length: paragraphs must track without strain on phone and desktop.
- The measures apply to articles, product descriptions and long forms alike.
- A new body face can read smaller at the same size — re-check the minimum on the chosen face.
- No body copy sits below 16px anywhere, including captions and helper text.
- The measure holds where the container is widest.

## Procedure

### 1. What it is

Body text at 16-18px minimum, line-height 1.5-1.7, and lines of about 45-75 characters (50-75 per NN/g-derived guides; Butterick 45-90), so long text can be tracked without strain.

### 2. How Hermes applies it

Hermes sets body >=16px, line-height >=1.5, caps measure with max-width/ch, and its judger flags <14px body, tight leading or >80-character lines.

### 3. What it returns to the stage

- Copy stage: `pages` — the page copy with body measures applied; `meta` — the page metadata carrying the body measures.
- Font stage: `families` — the chosen typefaces the body measures are set on; `scale` — the type scale including body size and line-height.

The measures are the value both stages record. The copy record carries the pages the measures apply to; the font record carries the size and leading values themselves. If a record key is missing, the stage does not complete.

### 4. Good looks like

Paragraphs read comfortably at arm's length on phone and desktop; no wall of dense text; lines end before the eye loses its place.

## Pitfalls

- Body text below 16px, or below 14px where the judger flags it outright.
- Tight leading under 1.5, which makes lines blur together on long text.
- Lines over 80 characters, where the eye loses its place returning to the next line.
- A measure capped on desktop but uncapped on mobile, where small text fails first.
- Setting the measures on one page and leaving the rest to defaults.
- Decorative body faces that read badly at 16px, however good they look at display size.
- A measure set in pixels on a fixed container that cannot narrow, so lines stay long on wide screens.
- Leading that holds for short paragraphs but tightens on long articles, where strain builds up.
- Body size raised for desktop and never checked at phone width, where it fails first.
- Long forms given the same treatment as short labels, so the text users must read longest is the hardest to read.
- A measure capped in ch units but never checked against the widest container.
- Leading set once for body and never checked on the longest articles, where strain builds up.

## Verification

- Body text is 16px or larger on every page, at phone and desktop widths.
- Line-height is 1.5 or larger throughout body copy.
- No body line runs over 80 characters; most run 45–75.
- Paragraphs read comfortably at arm's length on phone and desktop.
- The measures hold on articles and long forms, not only on short copy.
- The measures are recorded in the font stage and applied in the copy stage.
- No body copy sits below 16px anywhere, including captions and helper text.
- The measure holds where the container is widest.

The skill does the work and the visual judger checks the measures. The skill never grades its own output.

## Coordinator wiring

Loaded by stages: copy, font. Returns: `pages`, `meta` (copy stage); `families`, `scale` (font stage). Judger boundary: the visual judger checks body size, leading and line length; the content judger checks the copy itself.
