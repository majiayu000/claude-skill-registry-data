---
name: codex-imagegen
description: "Generate or redesign raster images (PNG mockups, illustrations, photos, UI design polish) from inside Claude Code by driving Codex CLI's built-in $imagegen, billed to ChatGPT-included usage instead of per-image OpenAI API charges. Use whenever the user wants to create/generate an image, make a mockup or illustration, produce a photo, polish or redesign a UI from a screenshot, or get a PNG out of a session — even if they don't mention Codex or \"imagegen\". This is the preferred image-generation path because Anthropic models cannot generate raster images and this route avoids API billing."
---

# codex-imagegen

Anthropic models are vision-in / text-out — they cannot emit raster pixels. This skill produces real PNGs by delegating to **Codex CLI's `$imagegen`** (the `gpt-image-2` model behind ChatGPT Images), and keeps it on **ChatGPT-included usage** by stripping `OPENAI_API_KEY` from the call so it never silently bills the OpenAI image API.

## Use the script

`scripts/codex-imagegen.sh` runs the whole flow (ChatGPT-auth preflight → concurrency-guarded headless `codex exec` → save to disk → optional exact resize) and prints the saved path:

```bash
"$HOME/.claude/skills/codex-imagegen/scripts/codex-imagegen.sh" \
  --prompt "<what to make>" [--out <name.png>] [--in <image>]... [--size WxH]
```

- `--prompt` — what to generate, or how to redesign the `--in` image.
- `--out` — optional. A bare name/relative path lands in the repo-scoped cclogs dir; an absolute path is used verbatim; omitted auto-names from the prompt. See [Output location](#output-location).
- `--in` — attach an image as vision/edit source; repeatable (e.g. a screenshot to redesign + a brand/style reference).
- `--size` — exact output pixels, e.g. `600x600`. `$imagegen` only emits preset sizes, so the script hard-resizes to your dims — `sips` on macOS, ImageMagick or Pillow on Linux/WSL (warns and keeps native size if none is present).

The script prints the absolute saved path. After it succeeds, **`Read` that PNG** to view/verify it and show the user.

### Generate from scratch

```bash
scripts/codex-imagegen.sh --size 600x600 \
  --prompt "a realistic photo of a grey heron at the water's edge"
```

### Redesign / polish from a screenshot

Pass the screenshot with `--in`. This is the design-polish path: the model works from the *picture*, not the app's source code.

```bash
scripts/codex-imagegen.sh --out redesign.png --in baseline.png \
  --prompt "redesign this pricing table to look premium — keep every number, column, and row identical; improve only spacing, typography, color, and dividers"
```

## Output location

The script saves into the **repo-scoped, Dropbox-synced cclogs dir** — `<cclogs-base>/<repo>/imagegen/` — resolved automatically by `$HOME/.claude/scripts/get-logdir.js` (the same `{logdir}` rule the other skills use; worktree-aware, `_misc/` when outside a git repo). Don't hand-build the path: pass just a filename to `--out`, or omit it. An absolute `--out` overrides this when a specific destination is needed.

`get-logdir` detects the repo with `git rev-parse` **from the current directory**, so invoking the script from a non-repo cwd (a `/tmp` scratchpad, a Dropbox prototype dir) silently routes output to `<cclogs>/_misc/imagegen/` instead of the repo. Pass **`--project-dir <repo-dir>`** to anchor resolution to the repo regardless of where the command runs — e.g. a design-polish loop that screenshots into `/tmp` should pass `--project-dir "$REPO_ROOT"` so mockups still land in `<cclogs>/<repo>/imagegen/`.

## Cost — this burns ChatGPT plan usage fast

Each image costs roughly **90k–100k tokens** of ChatGPT/Codex usage (image turns run ~3–5× heavier than text). Fine for a handful of design explorations; don't loop it dozens of times without telling the user. The script reports the tokens used per call.

## Requirements & caveats

- **Works on macOS and Linux/WSL.** Pure-portable except `--size`, which prefers `sips` (macOS) then ImageMagick (`magick`/`convert`) then Pillow (`python3 -m PIL`) — generation itself needs none of these. `get-logdir.js` already resolves the WSL Dropbox cclogs path. The real per-machine requirement is Codex auth: `$HOME/.codex/auth.json` is **not shared** across machines, so run `codex login` (ChatGPT) once on each (Mac and WSL).
- **Codex must be logged in with ChatGPT** (`codex login status` → "Logged in using ChatGPT"). The script warns if not. If only API-key auth is available, this skill's billing premise doesn't hold — say so rather than silently spending API credits.
- **The env var `OPENAI_API_KEY` would flip Codex to API billing**; the script unsets it per-call to stay on ChatGPT usage. That's the whole point — don't remove that.
- **Never trust exact text/numbers in the output.** Image models regenerate (not pixel-copy) and drift on dense small text — price lists, tables, microcopy are the worst case. Treat a redesign PNG as **visual direction only**; re-key real data from the source and verify before any of it informs production code.
