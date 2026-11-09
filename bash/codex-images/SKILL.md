---
name: codex-images
description: Batch-generate raster images through Codex CLI and its built-in image_gen. Use when the user needs several images at once, prompt arrays, catalog variants, or images built from reference pictures (YouTube thumbnails, product shots).
---

Needs the Codex CLI installed and signed in: check `codex --version` and `codex login status`. If either fails, read [references/setup-codex.md](references/setup-codex.md) and guide the user through it before going on.

Install the bundled CLI at the target repo root (`scripts/image_gen` is in this skill's folder). If `.codex/scripts/image_gen` already exists, inspect it before replacing.

```bash
mkdir -p .codex/scripts
cp <this-skill-folder>/scripts/image_gen .codex/scripts/image_gen
chmod +x .codex/scripts/image_gen
```

Default output: `.codex/scripts/output/<batch-name>-<timestamp>/` with `NNN-clean-name.png`, `logs/job-NNN.log`, and `manifest.json` (`copied[]`: path, promptIndex, prompt, name). Prefer `{ "name", "prompt" }` objects for stable names.

```bash
.codex/scripts/image_gen --name hats --prompts '["prompt one", "prompt two"]'
.codex/scripts/image_gen --out .codex/scripts/output/tshirts --prompts '[{"name":"men-white-crew-tee","prompt":"..."}]'
.codex/scripts/image_gen --name catalog --prompts prompts.json --concurrency 3
.codex/scripts/image_gen --name cap-variants --prompt "..." --count 3
.codex/scripts/image_gen --prompts prompts.json --dry-run
```

`--prompts` accepts a JSON string array, a `{name,prompt}` array, a file of either, or newline prompts.

Reference images (thumbnails, a face, a product): keep the source images read-only and copy the ones you need locally first. One named prompt object per final image; never pack multiple concepts into one job or one `--count`. Every prompt must list absolute local paths and tell the nested Codex job to pass them to `image_gen` as `referenced_image_paths`. Dry-run, then run; `manifest.json` must have one successful copy per prompt.

Catalog prompts: inspect the app taxonomy/filters first. No person, mannequin, face, text, logo, or checkerboard unless asked. Closed shirts: full front, closed neckline, no open placket.

Keep upload/import in the target repo. After generation, verify prompt count == copied images, usable dimensions, and unique hashes. Stop after returning the output dir and `manifest.json` path.
