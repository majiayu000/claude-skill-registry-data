---
name: image-gen
description: Generate images and videos with two engines the user already owns — Codex CLI's built-in image_gen (images; uses the Codex/ChatGPT login, no OpenAI API key) and Dreamina/jimeng (images AND videos, via the logged-in `dreamina` CLI). Use whenever the user asks to generate, create, draw, or make an image or a video — "text to image", "text to video", "draw me a…", reference-image edits, upscales — or names "codex" or "jimeng"/"dreamina" as the engine. Do NOT use for editing existing local files without generation, or for non-generation tasks.
---

# image-gen — Codex + jimeng image & video generation

Two engines only, each driven by the operator's own login (no API keys in this repo):

| Engine | Modality | Auth | Cost | Speed |
|--------|----------|------|------|-------|
| **codex** | images | Codex/ChatGPT login (no `OPENAI_API_KEY`) | Codex subscription usage | slow (5–10× an API) |
| **jimeng** (Dreamina) | images **and** videos | `dreamina login` session (Douyin OAuth) | account **credits** | async, minutes |

Both wrappers are self-contained **Node** scripts under `scripts/` (no bun, no TypeScript). Run them with `node`.

## Choosing an engine

- **Video** → only **jimeng** (codex can't do video).
- **Image, user named an engine** → use it.
- **Image, no preference** → default to **codex** (no credit spend) unless the user wants jimeng's specific look/models, or a batch where spending credits is fine.
- Reference-image edits: codex `--ref` (style/composition guidance) or jimeng `image2image` (jimeng image-guided editing).

## ⚠️ Before any real run

- **jimeng spends account credits** on every submit. Check balance first: `dreamina user_credit` (or `node scripts/check.mjs`). Warn the user before paid runs; prefer small batches (`--generate_num=1` while testing).
- **codex** consumes Codex subscription usage and is slow — fine for one-offs, avoid huge batches.
- Neither wrapper publishes anything; output stays local.

## codex — images

```bash
node scripts/codex-image.mjs --out <output.png> --prompt "<text>" [--aspect 1:1] [--ref ref1.png ...] [--json]
```

- `--aspect`: `1:1` (default), `16:9`, `9:16`, `4:3`, `2.35:1`.
- `--ref <file>` (repeatable): reference images for style/composition.
- `--prompt-file <path>`: read the prompt from a file instead of `--prompt`.
- **Sandbox**: defaults to Codex's standard `workspace-write` with the output directory as the writable workspace. If an attempt fails on that default, the script retries with `--sandbox danger-full-access` (isolation dropped) so unattended runs don't silently yield nothing — pass `--no-escalate`, or an explicit `--sandbox <mode>`, to prevent that.
- Output: a real PNG at `--out`. Prints `OK codex <path>` (or a JSON line with `--json`).
- Prereq: `codex login` must be live. The script auto-finds `codex` on PATH, else the Codex app binary under `~/AppData/Local/OpenAI/Codex/bin/`.

See `references/codex.md` for troubleshooting (refusals, timeouts, no-image_gen).

## jimeng (jimeng) — images and videos

One runner for every Dreamina async generator. It submits, polls `query_result`, and downloads the media into `--out`.

```bash
# text → image
node scripts/jimeng.mjs text2image --out imgs --prompt="a cat portrait" --ratio=1:1 --resolution_type=2k
# text → video
node scripts/jimeng.mjs text2video --out vids --prompt="a drone shot over dunes" --poll 600
# image-guided edit / upscale / image→video: same pattern, different subcommand + flags
node scripts/jimeng.mjs image2image --out out --prompt="make it watercolor" <dreamina image flags>
```

- First positional arg = the dreamina subcommand: `text2image`, `image2image`, `image_upscale`, `text2video`, `image2video`, `frames2video`, `multiframe2video`, `multimodal2video`.
- Wrapper flags: `--out <dir>` (download target), `--poll <sec>` total wait budget (default 300; raise to ~600 for video), `--interval <sec>` (default 4), `--json`.
- **Every other flag is passed straight through to dreamina** — so use the real dreamina flag names (`--prompt=`, `--ratio=`, `--resolution_type=`, `--model_version=`, `--generate_num=`, per-command image inputs, etc.).
- **Always confirm flags per subcommand first** — models/ratios/resolutions differ by command and version:
  ```bash
  ~/bin/dreamina.exe <subcommand> -h
  ```
- Success = media downloaded into `--out` (paths printed). Timeout prints the `submit_id` so you can resume: `dreamina query_result --submit_id=<id> --download_dir=<dir>`.

See `references/jimeng.md` for the model/ratio matrix, credit notes, and the `AigcComplianceConfirmationRequired` gotcha.

## Setup & runtime (per user — works for teammates too)

This skill is portable: it carries **no credentials**. Each user logs in with their own accounts (codex subscription / jimeng credits are per-account). Login state lives outside the skill (`~/.codex`, `~/.dreamina_cli`), so zipping and sharing the skill folder is safe.

- **Prereqs (each user):** Node (v18+) on PATH; for codex → `codex login`; for jimeng → install `dreamina` + `dreamina login`. Full steps in `SETUP.md`.
- **Readiness check:** `node scripts/check.mjs` reports which engines are ready and what's missing. Run this first on a new machine.
- **Binary resolution (cross-platform, no hardcoding):**
  - `codex`: `--codex` / `$CODEX_BIN` → on PATH → newest `~/AppData/Local/OpenAI/Codex/bin/*/codex.exe` (Windows Codex app).
  - `dreamina`: `--dreamina` / `$DREAMINA_INSTALL_DIR` → `~/bin/dreamina(.exe)` (Windows installer default) → `~/.local/bin/dreamina` (macOS/Linux default) → PATH.

## References

| File | Content |
|------|---------|
| `references/codex.md` | codex engine: how it works, sandbox, error kinds, trade-offs |
| `references/jimeng.md` | jimeng engine: subcommands, models/ratios, credits, async rules |
