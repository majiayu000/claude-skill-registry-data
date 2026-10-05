---
name: qruiq-icon-generator
description: Generate a project icon from scratch — read the codebase to understand what the project does, draft a prompt, render via OpenRouter (gpt-5.4-image-2), score the result against a rubric, iterate until it scores ≥ 90/100, then derive the full favicon set, web manifest, OG card, and HTML head snippet. Use this skill whenever the user mentions creating an icon, logo, favicon, app icon, social card, brand mark, or asks for "生成图标 / 做个 icon / make a logo / 来个 favicon" — even when they don't say "icon" explicitly (e.g. "this site needs a brand mark", "we still need something to show in browser tabs", "give us an OG image"). Prefer this skill over freeform image generation for any project that already has source code on disk, because the value comes from grounding the visual in the actual project.
---

# Icon Generator

End-to-end: project context → prompt → image → critique → iterate → asset bundle.

## When this skill runs

The user's project lives in the current working directory. They want a brand mark for it: a square icon, the favicon set, optionally a web manifest, head snippet, and Open Graph card. The icon should *come from* the project — its purpose, its name, its vibe — not from a generic prompt.

You are the orchestrator. You read the project, draft prompts, call generation scripts, judge images yourself with vision, and decide when to stop.

## Inputs the user might give you

- Nothing — just "make me an icon". Read the project and infer everything.
- A name override: "call it Lumen, not what's in package.json"
- A style hint: "playful", "technical", "minimalist line art", "matches our existing #5B21B6 brand"
- A budget: "iterations=5" (default 3) or "threshold=85" (default 90)

If they give a style hint, treat it as load-bearing — don't drift away from it across iterations.

## Workflow (7 steps)

### 1. Verify environment

Check `OPENROUTER_API_KEY` is set. If not, stop and tell the user — don't try to proceed.

For Pillow, this is more nuanced because macOS Homebrew Python is PEP 668-locked and `pip install Pillow` will refuse without `--break-system-packages`. So:

1. Try `python3 -c "import PIL"` — if it works, use plain `python3` for the rest of the workflow.
2. If it fails, check for a cached venv at `~/.cache/icon-generator-venv/bin/python` — if present, use that.
3. If neither exists, create the venv once: `python3 -m venv ~/.cache/icon-generator-venv && ~/.cache/icon-generator-venv/bin/pip install --quiet Pillow`. Then use `~/.cache/icon-generator-venv/bin/python` for all script calls in this run and going forward.

Bind the chosen python to a variable (e.g. `PY=~/.cache/icon-generator-venv/bin/python` or `PY=python3`) and use it consistently when invoking the scripts. Don't ask the user to do this — it's a one-time setup that takes ~5 seconds.

### 2. Understand the project

Read in this order, stopping when you have enough:

1. `README.md` (or `README.*`) — usually the richest source
2. `package.json` `description` + `name`, or `pyproject.toml`, or `Cargo.toml`
3. The app's root layout / index page if it's a web project (`app/layout.tsx`, `pages/_app.tsx`, `src/App.tsx`, `index.html`) — for tagline / title metadata
4. A glance at top-level directory structure to confirm what kind of thing it is (CLI? web app? library? game?)

What you're trying to extract:

- **Name** (display name, not the npm slug)
- **One-line purpose** (what does this thing do for whom?)
- **Tone** (technical, playful, serious, whimsical, premium…)
- **Existing brand cues** (any color in tailwind config, any logo reference, any existing favicon to replace)

If the project is sparse (empty README, generic name) ask the user one short clarifying question rather than inventing a brand.

### 3. Draft the prompt

Read `references/prompt-guide.md` for the prompt template and the principles behind it. The short version: square format, single focal subject, generous negative space, works at 16×16, transparent or simple flat background, no text inside the icon.

Show the prompt to the user before generating — one line, plain English. Example: *"I'm going to ask for: a minimalist line-art compass rose in deep indigo on transparent background, soft inner glow, geometric, balanced, no text. Good?"* This is a 5-second confirmation, not a design review — it lets them course-correct cheaply.

### 4. Generate

Run `scripts/generate_icon.py`:

```bash
python3 scripts/generate_icon.py \
  --prompt "<prompt>" \
  --output ".icon-generator/iter-1/master.png" \
  --model "openai/gpt-5.4-image-2"
```

The script writes the PNG and prints JSON with the path and the model that actually produced it (it falls back to `openai/gpt-image-1` if the primary model 404s, so you'll know if that happened).

Use `.icon-generator/` as a scratch directory at the project root. It holds iteration outputs and the rubric evaluations. Don't commit it — add it to `.gitignore` if you create one.

### 5. Score

Read the generated image with the `Read` tool — Claude Code's vision sees it directly. Score it against this rubric (sum to 100):

| Dimension          | Max | What you're judging |
|--------------------|----:|---------------------|
| Recognizability    |  25 | Would a stranger guess what the project does, or at least feel its category? |
| Simplicity         |  20 | Does it survive at 16×16 without becoming mush? Mentally squint. |
| Distinctiveness    |  15 | Memorable, not a stock-photo cliché. Avoids "AI slop" giveaways. |
| Composition        |  15 | Balanced, properly centered, comfortable padding, square-friendly. |
| Aesthetic quality  |  15 | Clean execution, no artifacts, no warped letterforms, no half-rendered limbs. |
| Brand fit          |  10 | Matches the tone you extracted in step 2 and any user style hint. |

Be honest. A "looks fine" image is usually a 75 — that's not good enough. Reserve 90+ for icons you'd actually ship. Write a 1-2 sentence critique focused on *what would push it from N to 95*, not generic praise. Save the scoring to `.icon-generator/iter-N/score.json`:

```json
{"score": 78, "breakdown": {...}, "critique": "Works at large sizes but the inner glow turns into a smudge below 32×32 — try without the glow effect."}
```

### 6. Iterate or settle

Default threshold is 90, default max iterations is 3. The user can override either.

- **Score ≥ threshold**: settle, move to step 7.
- **Score < threshold AND iterations remaining**: regenerate. Critically — *fold the critique into the prompt*, don't just retry the same prompt. The critique is the whole point of iteration. If two consecutive iterations score within 3 points of each other with similar critiques, stop early and present the best one — you've plateaued.
- **Iterations exhausted without hitting threshold**: pick the highest-scoring image, tell the user the score, show them the critique, and ask whether to (a) ship as-is, (b) burn another N iterations, or (c) let them rewrite the prompt themselves.

Tell the user the score after each iteration in one sentence. They don't need the full breakdown unless they ask. Example: *"Iteration 2: 84/100 — colors nailed but the symbol is too literal. Trying once more with more abstraction."*

### 7. Generate the asset bundle

Once an icon is settled, run the asset generator:

```bash
python3 scripts/make_assets.py \
  --master ".icon-generator/final/master.png" \
  --out-dir "<auto-detected output dir>"
```

**Auto-detect output dir** by checking, in this order:
1. `public/` (Next.js, Vite, CRA, Astro)
2. `static/` (SvelteKit, Hugo, Gatsby, Eleventy)
3. `app/` (Next.js app router public sometimes lives here, but only as fallback)
4. If none exist, create `public/` and use it.

The script writes:

- `favicon.ico` (16/32/48 multi-resolution)
- `favicon-16x16.png`, `favicon-32x32.png`
- `apple-touch-icon.png` (180×180)
- `android-chrome-192x192.png`, `android-chrome-512x512.png`
- `icon.png` (the master, useful for README badges and link previews)

Then run `scripts/make_og.py` to composite the icon onto a 1200×630 social card with the project name. Use the dominant color from the icon as the background — the script extracts it via Pillow's `quantize`. If the user gave a brand color, use that instead.

```bash
python3 scripts/make_og.py \
  --master ".icon-generator/final/master.png" \
  --title "<project display name>" \
  --tagline "<one-line purpose>" \
  --out "<out-dir>/og-image.png"
```

Then write the static helpers (no script needed — just template substitution):

- `<out-dir>/site.webmanifest` — populate from `assets/webmanifest.template.json`
- Print the HTML head snippet to the user from `assets/head-snippet.template.html` — they paste it into their root layout. Don't edit their layout file unsolicited; printing it lets them see exactly what's being added.

### Final report

End with a short summary the user can scan in 5 seconds:

```
Icon: 92/100 (iteration 2)
Output: ./public/
  favicon.ico, favicon-{16,32}x{16,32}.png
  apple-touch-icon.png
  android-chrome-{192,512}x{192,512}.png
  icon.png, og-image.png
  site.webmanifest
HTML snippet printed above — paste into <head>.
```

## Bundled resources

- `scripts/generate_icon.py` — OpenRouter image gen, with fallback model handling. Stdlib only (urllib).
- `scripts/make_assets.py` — Pillow resizes + `.ico` packing. All sizes in one pass.
- `scripts/make_og.py` — Pillow composite for the 1200×630 OG card with auto-extracted brand color.
- `assets/webmanifest.template.json` — populate `{{NAME}}`, `{{SHORT_NAME}}`, `{{THEME_COLOR}}`, `{{BG_COLOR}}`.
- `assets/head-snippet.template.html` — populate `{{BASE_PATH}}` (usually empty / `/`) and `{{THEME_COLOR}}`.
- `references/prompt-guide.md` — the prompt template and *why* each constraint matters; consult before drafting the prompt.
- `references/asset-spec.md` — spec for every output file (size, purpose, where it's referenced).

## Common pitfalls (read these — saves you re-doing the work)

- **Don't generate text inside the icon.** Image models render text unreliably and it'll fail at 16×16 anyway. Project name lives in the OG card and the `<title>` tag, not the favicon.
- **Don't generate at OG dimensions.** Image models constrain output to a few sizes. Generate the icon at 1024×1024, then composite the OG card from the icon — the text will be crisp and you control the layout.
- **Don't skip step 3.** Showing the user the prompt before spending a generation is cheap insurance against producing 3 iterations of the wrong concept.
- **Don't average critiques across iterations.** Each iteration's critique is about *that specific image*. Apply it to the next prompt; don't dilute it.
- **Don't edit the user's `app/layout.tsx` or `index.html` unsolicited.** Print the snippet, let them paste.
