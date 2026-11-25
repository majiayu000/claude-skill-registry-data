---
name: generate-image
description: Generate new raster images and edit existing ones via fal.ai (GPT Image 2.5, Nano Banana 2.1) — illustrations, product photos, hero art, UI mockups, background removal. Use whenever the user asks to generate/create/make an image, produce a photo or illustration for a page, get a before/after edit of an existing image ("add X", "remove Y", "change the color of Z" while keeping everything else the same), or strip/remove a background — even if they don't say "fal.ai" or name a model, and also when they do name one ("with Nano Banana", "use GPT Image"). For logos, icons, or anything that should ship as SVG, prefer the generate-svg skill.
compatibility: Claude Code with Bun 1.4 or later and a fal.ai API key in FAL_KEY.
---

# generate-image

Wraps fal.ai image generation/editing behind one CLI: `${CLAUDE_SKILL_DIR}/scripts/generate-image.ts`.
Requires a fal.ai key in `FAL_KEY` — if it's missing the script exits with a clear error, ask the user to export it in their shell — never ask them to paste the key into the chat.

Run it with Bash, e.g.:

```
bun ${CLAUDE_SKILL_DIR}/scripts/generate-image.ts generate --prompt "..." --output ./out.png
```

If the shell says `bun` isn't found, Bun isn't installed. Stop and ask the user to install it from
https://bun.com/docs/installation and restart Claude Code. Don't replace the script with other tools or
code of your own: the checks it runs before a paid call and on the result would be lost.

The script prints the final path, dimensions, and byte size — that's the confirmation the file exists; no need for a separate `ls`/read-back step unless you need to inspect pixels.

Files you make only to inspect a result (crops, alpha masks, previews) go in the project's work
folder: `media-generation/` inside the project's own scratch folder if it has one (`.scratch/`,
`tmp/`), otherwise `.media-generation/` holding a `.gitignore` that contains `*`, so git never sees
it. Never `/tmp` or a folder next to the project.

## generate — text to image

```
generate-image.ts generate --prompt "<description>" --output <path>
  [--model gpt-image-2.5|nano-banana-2.1] [--aspect-ratio 1:1|2:3|3:2|3:4|4:3|4:5|5:4|9:16|16:9|21:9]
  [--quality low|medium|high|xhigh|max] [--resolution 1K|2K|4K] [--remove-background]
  [--format jpeg|png|webp] [--output-quality 1-100] [--max-width N]
```

**If the user names a model, use it** ("with Nano Banana", "via GPT Image"). Otherwise pick:

| Model | Cost (~1 MP) | Pick it for |
|---|---|---|
| `gpt-image-2.5` (default) | `--quality low` ~\$0.005 · `medium` (default) ~\$0.01 · `high` ~\$0.05 · `max` ~\$0.21 | almost everything: hero art, illustrations, product shots, anything with readable text, posters, UI mockups, diagrams. Top-ranked model for both generation and editing |
| `nano-banana-2.1` | `--resolution 1K` (default) ~\$0.04 · `2K` ~\$0.06 · `4K` ~\$0.13 | images that must be physically large (2K/4K for print or full-bleed retina heroes), the same character or product kept consistent across several images, and photoreal scenes where a second opinion helps |

`gpt-image-2.5` quality: `low` for drafts and peripheral filler, `medium` for normal page images, `high` when text in the image or fine detail is the point, `max` only when the user asks for the very best. Its pixel count stays around 1 MP; for more pixels use `nano-banana-2.1 --resolution 2K/4K` — there is no separate upscale tool.

**Wrong tool for vector deliverables:** everything here outputs raster pixels. A logo, icon set, or favicon that should scale cleanly belongs to the `generate-svg` skill (true SVG output).

The output is always re-encoded on save in the format of the `--output` extension (`.jpg`/`.jpeg`, `.png` or `.webp`; anything else is rejected). `--format` is optional and must agree with the extension. Quality defaults to 85 — a ~1MP JPEG lands ~150–400KB. Use `--output-quality` / `--max-width` to control size directly instead of a separate resize/convert pass (see the `process-image` skill for that).

`--quality` only applies to `gpt-image-2.5` and `--resolution` only to `nano-banana-2.1`; passing either to the other model is an error. Unknown models, aspect ratios and out-of-range numbers fail before anything is sent, so nothing is billed for a typo.

The script prints the saved path, dimensions, actual format and size, plus a temporary `Result URL` that can be passed straight to `--image-url` of a follow-up `edit` or `remove-background`.

**A paid result is never lost.** As soon as fal.ai accepts a job the script prints its request ID and a ready `resume --model … --request-id … --output …` command on stderr. If the download fails or the run is interrupted, run that command — it fetches the already-paid result. Don't rerun the original command: that generates (and bills) again.


`--remove-background` strips the background right after generation (extra ~\$0.018 Bria call) and saves a transparent cutout — use for banner subjects, product shots, stickers. The output must be `.png` or `.webp` — a `.jpg` output is rejected up front, since JPEG has no alpha channel. If generation succeeds but background removal returns nothing, the script fails (it never saves the opaque original as if it were a cutout) and prints a `remove-background --image-url …` command that retries only the removal. A plain high-contrast studio background is auto-appended to the prompt for a clean cutout unless the prompt already mentions a background.

## edit — instruction-based edit of an EXISTING image

The only way to get a true before/after of the *same* image — `generate` always draws a new subject, so two generations never share the same scene/face/product. Use `edit` to add, remove, or change one detail while everything else stays put.

```
generate-image.ts edit --prompt "<what to change>" --output <path>
  (--source <path> | --image-url <url>)
  [--model gpt-image-2.5|nano-banana-2.1] [--quality low|medium|high|xhigh|max] [--resolution 1K|2K|4K]
  [--no-match-source-size]
  [--format jpeg|png|webp] [--output-quality 1-100]
```

Pass exactly one of `--source` or `--image-url`. A local source is read and checked before the paid call.

Describe only the change ("add extended eyelashes", "remove the logo from the mug", "make the walls sage green") — the rest of the image is preserved by the model. `gpt-image-2.5` is the default and the top-ranked editor (same quality tiers and prices as `generate`); use `nano-banana-2.1` when the user asks for it or the result must be 2K/4K.

By default a result that came back larger than a local `--source` is shrunk to the exact source dimensions so a before/after pair lines up. It is never stretched to a different aspect ratio and never upscaled — that would fake detail the model didn't produce; the script keeps the native frame and says so. Editing a large source (say a 4K master)? Use `--model nano-banana-2.1 --resolution 2K` or `4K`, otherwise the edit comes back at ~1K. Pass `--no-match-source-size` to always keep the raw edited frame. Not applied with `--image-url`.

## remove-background — cut out an existing image

```
generate-image.ts remove-background --output <path>.png|.webp
  (--source <path> | --image-url <url>)
  [--format png|webp] [--output-quality 1-100] [--max-width N] [--keep "<what to keep>"]
```

Works on any existing photo or picture, including photos of people. Bria keeps what it judges to be the main subject. When the image has several people or objects, or the user names what to keep, pass `--keep` with a short plain-English description: `--keep "only the woman on the left"`, `--keep "the person and the dog"`, `--keep "without the lamp"`. It costs ~\$0.03 instead of ~\$0.018.

Uses Bria RMBG 2.0 (~\$0.018/image), outputs a cutout with transparency — for product photos, compositing, or isolating a subject in an image you already have. If you're about to *generate* a new image that needs a transparent background, prefer `generate --remove-background` instead — prompting the model for a clean high-contrast backdrop gives RMBG a much better cutout than removing the background from an arbitrary existing photo.
