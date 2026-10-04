---
name: generate-visuals
description: Realize every typed [VISUAL:...] placeholder in the cited draft into an actual asset — Playwright screenshots of brand UI, Replicate-generated images (GPT Image 2 default, Nano Banana backup), matplotlib charts. Manual-capture flag for video/external/gif/adult-image. Updates the draft to reference local image paths.
allowed-tools: Read, Write, Edit, Bash
---

> **MANDATORY (board 2026-06-10):** build every generation prompt with the `visual-prompt-craft` skill (9-part anatomy, references/example-prompts.md) BEFORE calling any image model. Write prompts to `images/{slug}/prompts.md`. One-line prompts are a gate failure.


# Generate Visuals Skill

Take every `[VISUAL:type=...;...]` placeholder in the cited draft and produce a real asset on disk for the types we can automate, plus a `manual-capture.md` to-do for the rest. Update the draft to reference the local images so subsequent stages (preview, format-for-publish) treat them as ordinary markdown images.

This is the skill that closes the gap Ryan Law called out in his content-engineering blog: "blog post images are not a solved problem, yet" — solved here for the four types we can automate.

## Board Override: Visual Package Bar

Before running, read:

- `references/eo-blog-routine/visual-system.md`
- `templates/visual-types.md`
- `templates/editorial-principles-visuals.md`

Hard failures:

- empty visual manifest;
- table-only visual set;
- no cover/OG candidate documented in the scorecard;
- no screenshot/action-shot when Pleasur.AI is materially mentioned;
- generated infographic prompts missing from `images/{slug}/prompts.md`;
- Nano Banana/GPT-image output with garbled text, malformed arrows, unreadable labels, or generic stock-art feel.

## Input

For slug `{slug}`:
- `content-pipeline/6-drafts-cited/{slug}.md` — the cited draft with typed placeholders (or legacy `[SCREENSHOT: ...]`)
- `brand-config.md` — product URLs and visual-generation config block
- `../../../templates/visual-types.md` — taxonomy reference
- `../generate-screenshot/references/_archive/ahrefs-products-catalog.md` (legacy non-Pleasur reference) — URL-pattern shape templates only; brand-config product URLs are the primary source for the Pleasur.AI deployment

## Process

1. **Run the dispatcher.** It does everything below in one shot:

   ```bash
   doppler run -- python .claude/skills/generate-visuals/scripts/generate_visuals.py "<slug>"
   ```

   (Drop the `doppler run --` prefix if env vars are exported in the shell.)

2. **What the dispatcher does:**
   - Parses every `[VISUAL:...]` and legacy `[SCREENSHOT:...]` placeholder
   - Dispatches by `type`:
     - `screenshot` → `capture_screenshot.py` (Playwright headless; uses `auth/state.json` if it exists)
     - `image` → `generate_image.py` (Replicate; default `openai/gpt-image-2`, fallback `google/nano-banana`); `safety=adult` is routed to manual-capture instead
     - `chart` → `render_chart.py` (matplotlib)
     - `video`, `external`, `gif` → manual-capture entry only
   - Optimizes every captured PNG via `optimize_image.py` (Pillow lossless re-save)
   - Writes `content-pipeline/images/{slug}/manifest.json` with the typed record of every visual
   - Writes `content-pipeline/images/{slug}/manual-capture.md` with editor instructions for un-automated visuals
   - Rewrites `content-pipeline/6-drafts-cited/{slug}.md` — every `[VISUAL:...]` whose asset succeeded becomes `![alt](images/{slug}/file.png)`. Failed or manual entries keep their typed placeholder.

3. **Tell the user** the manifest path, how many visuals were captured vs. flagged manual, and any failures.

## Output

Under `content-pipeline/images/{slug}/`:
- `screenshot-{n}-{slug}.png` — Playwright captures
- `image-{n}-{slug}.png` — Replicate-generated images
- `chart-{n}-{slug}.png` — matplotlib charts
- `manifest.json` — typed record per visual: `{type, status: captured|manual|failed, path?, source?, prompt?, model?, alt}`
- `manual-capture.md` — editor instructions for video/external/gif/adult-image

Plus an updated `content-pipeline/6-drafts-cited/{slug}.md` with image markdown substituted in.

## Auth setup (one-time)

For Pleasur.AI app pages that require login, run once:

```bash
python .claude/skills/generate-visuals/scripts/setup_auth.py
```

This launches a non-headless browser. Log in to `pleasur.ai`. The script saves cookies + storage state to `.claude/skills/generate-visuals/auth/state.json` (gitignored). Future captures replay that session.

If `state.json` is missing, screenshot captures of authenticated pages will fail and be flagged in `manual-capture.md`.

## Quality checklist

- [ ] The manifest is not empty
- [ ] The visual set is not table-only
- [ ] The article has a cover/OG candidate documented in the scorecard
- [ ] Product-led articles include at least one screenshot/action-shot product proof visual
- [ ] Concept/infographic images use structured prompts and inspect clean labels/arrows
- [ ] Every typed visual placeholder either produced a PNG, succeeded as a chart/image, or appears in `manual-capture.md`
- [ ] No naked `[VISUAL:...]` or `[SCREENSHOT:...]` left in the cited draft for types that should have been captured
- [ ] All captured PNGs are at least 1200px wide
- [ ] manifest.json records `status` per visual (captured/manual/failed)
- [ ] Filenames in `images/{slug}/` are predictable (type-N-slug.png) and referenced from the draft

## Backwards compatibility

Legacy `[SCREENSHOT: description]` placeholders are still recognized and treated as `[VISUAL:type=screenshot;what=description]`. Generated assets are saved with the same naming scheme.

## Failure modes

- **Replicate refuses prompt (content safety)**: `generate_image.py` retries with the backup model; if both refuse, the entry is flagged in `manual-capture.md` with note "API rejected; capture from pleasur.ai/generate"
- **Playwright auth missing**: `capture_screenshot.py` falls back to capturing without auth (public pages render; authenticated pages show login). If the captured image height is suspiciously short, the entry is flagged for editor review.
- **Replicate / Playwright not installed**: dispatcher logs and continues; visuals of those types are flagged manual.

## Auto-capture coverage by type

- **`screenshot`** — auto-captured (patchright headless; uses `auth/state.json` if present).
- **`image`** — auto-generated (Replicate; SFW only).
- **`chart`** — auto-rendered (matplotlib from research data).
- **`external`** — **auto-captured (PLEAA-417, 2026-05-06).** Was manual. Now patchright opens the URL, clips to `selector`, and applies a padded crop. Cloudflare / login walls fall back to `/capture-visuals` (Claude-in-Chrome with a real Chrome session). ToS bypasses are out of scope — if both paths fail the entry stays `failed` and the visuals gate halts.
- **`action-shot`** — routed to `/capture-visuals` (multi-step interactive flows).
- **`video`** — manual. Embedded by URL into Strapi, not produced as a PNG.
- **`gif`** — manual. Requires a screen-recording source the pipeline doesn't have. ffmpeg conversion is a future enhancement.

## Failure → fallback dispatch (PLEAA-417)

When `external` capture fails for one of the bot-block reasons (`cloudflare_challenge_unresolved`, `redirected_to_login`, `navigation_failed`, `image_dimensions_too_small`), the manifest entry stays `status: "failed"` (so `pipeline_gate.py` halts as PLEAA-392 requires) but carries a `fallback` block:

```json
{
  "fallback": {
    "method": "claude_in_chrome",
    "skill": "/capture-visuals",
    "url": "...", "selector": "...", "what": "...", "sub": "..."
  }
}
```

The orchestrator (or an autonomous heartbeat) reads the failed entries, runs `/capture-visuals {slug}` to dispatch the Chrome MCP fallback, and re-runs the gate. If the Chrome path also fails, the entry stays `failed` and the editor handles it manually — we never bypass site protections.
