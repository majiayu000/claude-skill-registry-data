---
name: renew-social
description: Produce Renew Implant Centre Instagram, Facebook, and Meta ads from the social catalog. Every unit is video, static, or carousel, and every frame stays on the Renew design system. Use when drafting, filming, or reviewing social posts, Reels, stills, carousels, Stories, or paid dental-implant ads.
---

# Renew social and paid ads

Blog posts still follow [renew-blog-writing](../renew-blog-writing/SKILL.md). This skill is for Instagram, Facebook, and Meta ads. The feed and the paid catalog are a mix of video, static, and carousel. Do not ship a week or a campaign that is only one of those.

The catalog is `docs/content/social/`. Entity facts and locked claims stay in [docs/search-visibility.md](../../../docs/search-visibility.md).

## Skills

`pipeline.json` names the skills to open for a stage, and the brand those skills paint.

1. Read `skills.use` and open a skill when its `when` matches the stage and the unit format.
2. Take the line under `take`. Leave the line under `ignore`.
3. The brand is Renew Implant Centre. Colors, type, and the wordmark come from `design-system.json`. A skill supplies a technique. It does not supply a brand.
4. Design skills in that list cover banner layout, token checks, carousel structure, and contrast. Video skills cover Remotion compositions and OpenMontage motion, captions, and cuts. They change how a frame is built. They leave the Renew palette, the two typefaces, and the wordmark alone.

## Design system, every time

1. Read `docs/content/social/design-system.json` before writing a frame, a prompt, or a caption.
2. Colors are token names (`accent`, `carbon`, `aqua-deep`, …). The hex values are copied from `:root` in `src/app/globals.css`. If the CSS changes, update the JSON in the same change. Do not invent a green, a blue, or a gold.
3. Type is DM Serif Display (headlines, weight 400) and Plus Jakarta Sans (labels and body). The wordmark is the word `renew` in the serif and `implants` in small caps. There is no logo file. Do not draw a tooth icon in its place.
4. Light grounds use aqua eyebrows. Dark grounds use lime eyebrows. The CTA is always a fully rounded lime pill with near-black text.
5. A single thin aqua arch stroke is allowed. It reads as a jaw curve, not a logo.
6. Formats are declared in `design-system.json`:
   - `video` is 1080×1920, with a spoken line. The last 2.5 seconds are layout `video-end-card`.
   - `static` is one 1080×1350 frame, also cut to 1080×1080. No voiceover.
   - `carousel` is 1080×1350 slides. The last slide is layout `cta-still`.
7. Call `buildPromptPrefix()` from `src/lib/social-pipeline.ts` for any generated frame. Clinic stills must be paths in `approvedMedia`.

## Produce one unit

1. Pick a `ready` unit from `ads.json` (paid) or `organic-calendar.json` (feed). Skip anything that needs a signed social release.
2. Follow `format`. Video speaks `hook`, `spoken`, and `onScreen`. Static and carousel put `onScreen` and slide lines on the frame and use `body` as the caption. Do not paste the original Gemini hook back in. Do not turn a static or carousel unit into a video to save a setup.
3. The click is `https://renewimplants.vercel.app` plus `ctaHref`. Build it with `absoluteClickHref()` from `src/lib/social-pipeline.ts`. The quiz is about two minutes and nine questions. `www.renewimplants.ca` does not serve that page. On video the phone `613-841-6111` may be spoken. On static and carousel it sits on the card. It is not a second price offer.
4. If `testimonialName` is set, the words must stay a verbatim excerpt of that review in `src/content/testimonials.ts`. Do not show that person’s face.
5. `concept-denture-slip` is a generated older adult with lived-in skin, wrinkles, and laugh lines. No name, no blood, no needles, no extra facial or hand features. The end card is still the design system.
6. Cross-posting follows `distribution.json`. Do not invent a third clinic, a new domain, or a city price page.

## Gate

```bash
npx vitest run src/lib/social-pipeline.test.ts
```

The test fails if a catalog collapses back to one format, a unit leaves the palette, a static or carousel grows a voiceover, a carousel skips the closing card, the copy quotes a price, calls Tom Szarski “Dr.”, says guarantee, or names a patient who is not in the review file.
