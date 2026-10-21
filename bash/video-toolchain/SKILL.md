---
name: video-toolchain
description: Check the local toolchain required by the kit's video and animation skills before starting a render - Node.js, ffmpeg, Python with numpy and Pillow, headless Chrome (CHROME_PATH / PLAYWRIGHT_CHROME aware), optional Ruby - and fail with one clear remediation line per missing tool. Use before any reel, cartoon, animation or film task that renders frames locally (kinetic-reel, painted-animation, the lemo-opuscar pointer workflow).
---

# Video toolchain

A prerequisite gate for every kit skill that renders video frames locally. Run it
**before** scaffolding a project or telling the user a video can be made: a render
that dies at frame 300 because ffmpeg or Chrome is missing wastes the whole run.

```bash
uv run --no-project .agents/skills/video-toolchain/scripts/video_toolchain.py
uv run --no-project .agents/skills/video-toolchain/scripts/video_toolchain.py --json   # machine-readable
# overrides: --python <binary>   --chrome <path>
```

Exit 0 = every required tool present. Exit 1 = at least one required tool
missing; each missing tool prints a `fix:` line with its remediation (install
command or env var to set). The check is read-only and stdlib-only: it only
probes tools already on the machine (the uv candidate for numpy + Pillow may
provision its package cache on first use; no project file is touched).

## What it probes

| Tool | Probe | Required by |
|---|---|---|
| node | `node --version` | kinetic-reel, painted-animation (npm install, render.mjs) |
| ffmpeg | `ffmpeg -version` | every render skill (frame encoding) |
| python + numpy + Pillow | `import numpy, PIL` via `--python`, the uv env (`uv run --no-project --with numpy --with pillow`), `python`, `python3` | lemo-opuscar styles (`paper.py` texture helpers) |
| chrome | `--chrome` > `CHROME_PATH` > `PLAYWRIGHT_CHROME` > standard install paths > PATH | headless Chrome rendering (`render.mjs`) |
| ruby | `ruby --version` | optional - motion-graphics-music-video only; never fails the run |

Notes:

- **Output size discipline** (from the live 2026-10-19 rehearsal): the default
  kinetic-reel encode produces roughly 100 MB for a 17 s film - after each
  successful render, also produce a web copy (`ffmpeg -vf scale=1600:900 -crf 23
  -preset slow -movflags +faststart`) before delivering.
- **Paid or keyed upstreams stay opt-in**: anything needing an API key (for
  example the FAL_AI_API_KEY env var referenced by motion-graphics-music-video)
  is never vendored or run by this check; the key name alone may appear in docs.
- The Chrome probe never writes anything and never launches a browser session;
  it only verifies the executable exists. The render skills launch it headless.
- Onboarding audit, per-repo decisions and the lemo-opuscar pointer workflow:
  `docs/video-skills-2026-10-19.md` in the agents-kit repository.

## Exit contract for the calling skill

1. `video_toolchain.py` exit 1 -> stop, report the missing tools and their
   `fix:` lines to the user, do not attempt the render.
2. Exit 0 -> proceed; re-check only when a tool invocation later fails with
   "not found" (PATH may differ in nested shells).
