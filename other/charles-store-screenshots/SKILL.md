---
name: charles-store-screenshots
description: "Design and render App Store (and Play Store) screenshot sets that look like the best on the store: a two-frame hook, frames that bleed into one world, one named signature move, real app UI at its best moment, characterful type and one brand personality chosen from five style lanes (fun / gen z, chaotic, clean / editorial, aesthetic, Y2K). Each set is one HTML strip built from real captures, real photos and generated objects, rendered to exact 1320 x 2868 PNGs and checked at search-result size. Use when someone wants App Store screenshots, product-page or store-listing creative, screenshot concepts or variations, a redesign of an existing set, or a critique of one."
---

# Store screenshots

A screenshot set is one strip of frames designed as one picture. Frames 1–2 are the hook: one composition that makes people want the rest. Every seam is crossed, so the set feels like a single world you scroll through, and each later frame shows one real moment of the app. Sets are built in HTML, so type and real UI stay crisp, with generated objects and real photos composited in, and rendered to Apple's exact size.

Before planning, read [references/craft.md](references/craft.md): the lane tree, hook techniques, seam recipes, type, copy and the tells. For reference sets, read [references/swipe.md](references/swipe.md).

## The bar

Every set passes all ten. Each exists because breaking it made sets look templated, generated, unreadable or unconvincing.

1. **Frames 1–2 are one hook.** One photo, scene, object, headline or sentence crosses the seam between them, and together they say what the app is and why it's worth it. Frame 1 alone still shows the app's name or face and its promise. Why: the opening spread is what nearly everyone sees. One image across it reads as a poster, and the half that continues pulls the swipe. Ads and some search layouts show frame 1 alone, so it can't lean on frame 2.
2. **Every seam is crossed, and nothing is cut by one by accident.** Each seam is crossed by a continuous background, or by an object, person, phone or type. At least half the seams are crossed by a distinct shape (an object, a person, a phone, type, a drawn line or a shaft of light), not only by a flat ground. Alternating frame colours are fine when something crosses the colour change.
   - A shape that crosses shows a recognisable piece on both sides: at least 60 px (180 in the export) on the smaller side.
   - Anything that doesn't cross stays at least 12 px from the seam, and from the strip's two ends unless it bleeds off them by 60 px or more.
   - Type crosses only between words, never through one.

   Why: continuity makes the set one world, and a row of separate cards reads as a template. But the store sets every frame apart with a gap beside it, so a 20 px sliver of a shoe, a sun or a cover at a frame's edge reads as a cropping mistake, not a crossing. `render` prints a CHECK line for each sliver or near-miss.
3. **One idea per frame after the hook, six words or fewer.** One headline of at most six words, plus an optional eyebrow of at most four. In the chaotic lane, one lead line obeys this; bubbles and stickers are texture and must read as part of the picture, never as a second headline. Why: Hick's law. A set is glanced at, not read, so every extra phrase competes with the one that sells.
4. **Readable at search size.** Headlines are at least 40 px on the 440 px frame in a bold sans, and at least 46 px for serifs or light weights. Anything the user must read is at least 16 px. Text contrast against what's directly behind it is 4.5:1 or more. Why: in search a frame shrinks to about 115 pt wide, and below these sizes text drops under iOS's 11 pt minimum and becomes texture.
5. **Real UI at its best moment.** Every frame after the hook, and usually frame 2, shows a real capture from the app, never redrawn UI. Crop it or size it to the moment the feature pays off (the PR, the rank, the answer). The screen is at least 300 px wide, or the crop fills at least 70% of the frame width. Why: the real screen is the proof. Mock UI reads as fake, and a whole screen shrunk into a phone can't be read.
6. **A named signature move in every frame.** Name the move in five words or fewer before designing, e.g. "the number is the hero", and show it in every frame. After rendering, run the logo-swap test: if a competitor's logo would fit the set unchanged, the move isn't strong enough. Why: the move is what makes the set recognisable without its logo. Without one, sets slide back to the category template.
7. **One system, one rhythm.**
   - Up to three colours plus one accent.
   - Two typefaces at most.
   - One device treatment: a phone, frameless cards or floating UI.
   - One light direction.
   - One emphasis per headline, done the same way all set long.
   - Between frames, change exactly one variable: background colour, scale, crop, or light/dark.

   Why: consistency reads as a real brand, and one changing variable keeps the swipe interesting without breaking it.
8. **Real people, generated things.** Faces and bodies come from real photos you have the rights to (the app's coach, team or users). Generate only objects, materials, skies, worlds and lettering. Never generate a real person, and never alter a real person's body. Why: generated people carry the tells (hands, skin, eyes) that make a set read as AI, and editing someone's body is a line we don't cross.
9. **None of the tells.** Check every frame against the list in craft.md. Why: each tell makes a set read as generated or templated, and one is enough.
10. **Real proof where people decide.** Show the strongest proof the listing has, in this order: an Apple award (Editors' Choice, App of the Year, Apple Design Award), a rating with its volume ("4.8 ★ · 974K ratings"), a chart rank with its category, a named press quote. Put one or two of them in frames 1–2, as one line or a laurel pair at least 16 px tall, smaller than the headline and clear of it. Why: social proof and authority are the strongest trust levers a listing has, and search shows only the first three frames, so proof saved for the last frame reaches few people. A rating without its volume reads as a claim; the volume makes it a crowd.

Never print a rating, user count, award or press mention that isn't real and current. When the app has none yet, the proof is the people behind it and true product facts.

## Run it

Needs Python 3 with Playwright, Pillow and requests, plus Google Chrome. Art needs `OPENAI_API_KEY` and cutouts need `FAL_KEY`, either in the environment or in a `.env` in or above the working folder.

```bash
python3 <skill>/scripts/shots.py render <set.html> [--scale 2]            # frames/, preview.jpg, search.png
python3 <skill>/scripts/shots.py art "<prompt>" --out art/x.png [--transparent] [--size 1536x1024] [--ref img]
python3 <skill>/scripts/shots.py cutout <photo> <out.png>                # BiRefNet
python3 <skill>/scripts/shots.py font "Instrument Serif:ital@0;1" --out fonts/
python3 <skill>/scripts/shots.py board <set-dir>... --out board.html [--embed]   # search view + full strips
```

### 1. Brief

Write `brief.md` before designing anything.
- The app in one sentence, who it's for, and its personality in three words.
- Features ranked by what users value (the owner, reviews, the paywall's list), not by build order.
- Real assets:
  - UI captures from the current build with demo data, 1206 × 2622 or larger
  - photos of people you have the rights to, at the largest size that exists. App assets are often downscaled crops, so find the originals: a photo enlarged more than about 1.3× looks soft at full size.
  - the logo, brand fonts and colours
  - any 3D or illustration assets the app already ships
- True facts you may print: counts, program lengths, tiers. Check each one in the app's data or with the owner before listing it, and note what must not be claimed. A set built on a wrong brief prints the mistake eight frames wide.

Why: every later choice traces back to this, and assets the app already owns are more distinctive than anything generated.

### 2. Choose the lane, the hook and the move

Walk craft.md's lane tree, choose one hook technique, name the signature move, and pick the levers from craft.md's Psychology table. Write all four in the comment at the top of the set's `set.html` (`lane:`, `hook:`, `move:`, `levers:`), as in `assets/template.html`. Why: a lever chosen up front gets designed in; one noticed afterwards gets bolted on.

### 3. Write the frames

In that same comment, give one line per frame: the headline (six words or fewer, with the emphasised word marked), the capture and its crop, and what crosses the seam to the next frame. The default story for eight frames:

| Frame | Shows |
| --- | --- |
| 1–2 | The hook |
| 3 | The core action |
| 4 | Its payoff |
| 5 | The guidance, coach or intelligence |
| 6 | Progress or community |
| 7 | Depth or personalisation |
| 8 | The closer: the strongest remaining reason, the people behind the app, or a brand moment |

Reorder it by the brief's ranking. Write every headline as a result or an experience, using craft.md's patterns.

### 4. Make the art

- **Real photos:** `cutout`, then check the matte at hair, fingers and anything held. A subject that its source photo crops (at the waist, at a hand) must sit against a frame edge on that side; it can't float or cross a seam there. Grade colour and light to the set's light direction (CSS filters or a graded copy), and add a contact shadow where the subject meets a surface.
- **Generated art:** `art`, using craft.md's prompt formula. Always pass the set's palette hexes, light direction and material. Use `--transparent` for objects and generate two of each, then keep the better one. Reject any image with a tell and regenerate it; never work around a tell in the layout.
- Keep everything in `art/`. Each generated file keeps its prompt in a `.json` sidecar.

### 5. Build the strip

Copy `assets/base.css` and `assets/template.html` into the set's folder.
- **Structure:** one `.strip` holding N `.frame` sections of 440 × 956 CSS px.
- **Placement:** put everything in strip coordinates with `.at` (`--f`, `--x`, `--y`), so an element that crosses a seam is a single element. Use `.span` for backgrounds that run through several frames.
- **UI:** `.phone` and `.phone.matte` for devices, `.card` for frameless captures, and `.crop` for magnifying part of a capture.
- **Fonts:** load them locally (`font`, or the brand's files) so nothing loads over the network at render.

### 6. Render and check

Run `render`. Then look, in this order:

1. **`preview.jpg`:** is it one world? Is the move in every frame? Does every seam cross? Look up each CHECK line `render` printed in the frames themselves: its boxes include rotation and transparent padding, so some are false alarms, but every real sliver or near-miss gets fixed.
2. **`search.png`:** can every headline be read? Does each frame keep an edge on both the white and the black rows?
3. **Two frames at full size:** type crispness, cutout edges, UI legibility.

Write `review.md` with a pass or fail for each of the ten bar items and every tell, the frame where each named lever shows, plus the logo-swap test.

### 7. Fix

Fix only what failed, then re-render and re-check. You're done when all ten pass and no tell appears. A set that passes but looks like its category's average isn't done: strengthen the move or the hook and render again.

### 8. Show

Run `board` across the sets and open it for the user. It opens with every set's first three frames at search size, on light or dark, because that is where sets compete; below that is each full strip with its lane and move. Before showing it, look at that search view yourself: a set that disappears beside the others needs a stronger hook.

## Several versions at once

- Plan every version in one table first: lane, hook technique, move, palette, typefaces, device treatment. When two rows look alike, change the table before you build.
- No two versions share a lane plus hook pair, a signature move, a background colour family, or the device that crosses their seams (two sets bridged by photo prints read as one idea twice).
- With five or more versions, cover at least four of the five lanes, and include light, dark and saturated sets.
- Every version gets the full bar. One weak version lowers the whole board.

## Other devices

| Device | Frame (CSS px) | Render | Export |
| --- | --- | --- | --- |
| iPhone 6.9" | 440 × 956 | `--scale 3` | 1320 × 2868 |
| iPad 13" | 1032 × 1376 | `--scale 2` | 2064 × 2752 |
| iPhone Duo (outer display) | 466 × 678 | `--scale 3` | 1398 × 2034 |

Set `--fw` and `--fh` on `:root` to the frame size. `render` flags any size the store doesn't take.
- Use each device's own captures: the iPad layout, or the Duo's outer display with its status rail. Never put an iPhone capture in a bigger frame. Why: each device's set is shown to people holding that device, and a scaled phone screen reads as an app that wasn't made for it.
- Recompose for the canvas. The headline size, the screen's width, the hero's scale and where seam objects sit all change with the frame's shape.
- Generate every device from one script with per-device numbers, so the copy and art stay identical and one edit reaches all of them.
