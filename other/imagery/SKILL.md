---
name: imagery
description: "Photography and crops chosen per breakpoint and purpose."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, imagery]
    category: web
    related_skills: [web-design, performance-design, responsive-design]
    web_designer_stages: [direction, build]
---

# Imagery and Art Direction Skill

Choose real, specific photography and illustration that fits the brand, and crop it differently per breakpoint so the subject stays legible everywhere. This skill covers image selection, art direction with per-breakpoint crops, responsive delivery, modern formats, layout stability, and alt text. It does not cover iconography or logo work, and it does not cover video. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For heroes, product shots, galleries and any image that carries meaning or emotion.
- When one crop cannot serve both a mobile screen and a desktop banner.
- When an image is the largest contentful paint element and its loading behaviour decides page speed.
- When an image must be described accurately to screen readers and search engines.
- When a gallery or product shot must stay legible at every size.
- Not for decorative textures that carry no meaning — those take empty alt text and no art direction.
- Not for text baked into an image: text stays as text, so it can be read, searched and translated.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage or stages.
- The design direction is chosen, so imagery matches the direction and the brand.
- The page structure and breakpoints are known, so each crop can be planned per breakpoint.
- The LCP element is identified, so the skill knows which image must never be lazy-loaded.

## How to Run

1. Select one hero image as the key design decision, and choose real, specific photography or illustration that fits the brand for the rest.
   - Prefer a specific image of the real subject over a generic stock image.
   - One hero image carries the page; the rest support it, they do not compete with it.
2. Plan the crop per breakpoint: the subject stays legible on the mobile crop and on the desktop banner, using art direction via the picture element.
   - A tall mobile crop and a wide desktop banner are different crops of the same image, not one crop stretched.
   - Check the subject is legible in each crop before the build.
3. Serve resolution switching via srcset and sizes, in modern formats — WebP, then AVIF where supported.
   - Each breakpoint gets an image sized for it, not the desktop file scaled down.
4. Set explicit width and height on every image so layout never shifts as images load.
   - The reserved space matches the image's aspect ratio at every breakpoint.
5. Lazy-load below-fold images only; never lazy-load the LCP image.
   - The LCP image loads with the page; everything below the fold waits until it is needed.
6. Write specific alt text for every meaningful image — text that could be defended, such as a description of the subject — and empty alt text for decorative images.
   - Alt text names what the image shows, not where it sits on the page.
   - A decorative image takes empty alt text and stays silent for screen readers.
7. Re-check after any fix, and record what changed.
   - A changed crop, format or alt text is re-checked for legibility, weight and accuracy before the stage closes.
   - The LCP image recorded is the one in the final build, and it is not lazy-loaded.

## Quick Reference

- WebP: about 30% smaller than JPEG; AVIF smaller again.
- Alt text: specific, at most 125 characters; empty alt text (`alt=""`) when the image is decorative.
- Width and height: explicit on every image, to prevent cumulative layout shift.
- Lazy-loading: below-fold images only; never the LCP image.
- Art direction: the picture element, with a different crop per breakpoint.
- Resolution switching: srcset and sizes.
- Hero image: one per page, chosen as the key design decision.
- Subjects: real and specific, legible in every crop.
- Formats: WebP about 30% smaller than JPEG, AVIF smaller again.
- Stability: explicit width and height on every image, so layout never shifts.
- Loading: below-fold images lazy-load; the LCP image never does.
- Alt text: specific and accurate, at most 125 characters; empty when decorative.

## Procedure

### 1. What it is

Choosing real, specific photography/illustration that fits the brand, cropping differently per breakpoint (art direction via the picture element), resolution switching via srcset/sizes, modern formats (WebP about 30% smaller than JPEG, AVIF smaller again), explicit width/height to prevent CLS, and specific alt text (at most 125 chars; alt="" if decorative).

### 2. How Hermes applies it

Hermes selects one hero image as the key design decision, serves picture-element crops per breakpoint, lazy-loads below-fold images, never lazy-loads the LCP image, and writes specific alt it could defend ("golden retriever puppy…", not "hero image").

### 3. What it returns to the stage

- `direction` stage record: `directions` and `chosen` carry the imagery choice — the hero image and the art-direction approach — as part of the chosen direction.
- `build` stage record: `files` carries the picture-element markup, srcset and sizes, formats and alt text; `build_log` notes the LCP image and that it is not lazy-loaded; `token_drift` must be empty.

### 4. Good looks like

The subject stays legible on mobile crop and desktop banner; images load fast, never shift layout, and are described accurately to screen readers and search engines.

## Pitfalls

- One crop for every breakpoint: the subject is a speck on mobile or cropped out of the desktop banner.
- Lazy-loading the LCP image: the most important image on the page is deliberately delayed.
- No explicit width and height: images push content down as they load, and the layout shift is measured as CLS.
- Generic alt text such as "hero image": it tells a screen-reader user and a search engine nothing about the image.
- Alt text on a decorative image: noise for screen readers; decorative images take empty alt text.
- Oversized JPEGs where WebP or AVIF would do: the page pays about 30% more weight for the same image, and the LCP time follows.
- A generic stock photo in place of a specific one: the image fits any brand, which means it fits this brand in no particular way.
- Text baked into an image: the words cannot be read by a screen reader, searched, or translated.
- The same desktop file served at every size: a phone downloads a banner-sized image to show it at a fraction of the width.

## Verification

- The subject stays legible on the mobile crop and on the desktop banner.
- Images load fast, with modern formats and right-sized delivery, and never shift layout.
- Alt text is specific and accurate for meaningful images, at most 125 characters, and empty for decorative images.
- Below-fold images lazy-load; the LCP image does not.
- Every image carries explicit width and height, and the reserved space matches its aspect ratio.
- No text is baked into an image.
- The hero image is the one recorded as the key design decision, and the other images support it rather than competing with it.
- Each breakpoint is served an image sized for it through srcset and sizes.
- The picture element carries a different crop per breakpoint, and the subject is legible in each.
- No text is baked into an image.
- The build log names the LCP image and confirms it is not lazy-loaded.
- The stage record carries the final markup, formats and alt text, not earlier drafts.
- The performance judger checks LCP and CLS; the a11y judger checks alt text; the visual judger checks the crops. The skill does the work and the judgers check it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: direction, build. Returns: `direction.chosen` (hero image and art-direction approach, as part of the chosen direction); `build.files` (picture-element markup, srcset, sizes, formats, alt text); `build.build_log` (LCP image named, not lazy-loaded). Judger boundary: performance judger checks LCP and CLS; a11y judger checks alt text; visual judger checks crops and legibility.
