---
name: pypi-imgsqueeze
description: "Python library and CLI imgsqueeze (v0.1.1) — compress the PNG, JPEG and WebP images of a blog once, in place, and record each finished image in a <image>.json sidecar so it is never compressed again. Use after adding or replacing blog images, or to check, pin, or clean up compressed images. Public API: optimize, check, pin, doctor, Report, Result, get_preset, read_sidecar."
---

# imgsqueeze

Compresses blog images in place: PNG with pngquant + oxipng, JPEG and WebP with Pillow. A result is kept only when it saves at least `min_gain` (PNG and JPEG 5%, WebP 10%); otherwise the original stays. Every processed image gets a sidecar `<image>.json` holding the sha256 of its final content; while it matches, the image is skipped by every later run, with any preset. Needs Python 3.11+, and [mise](https://mise.jdx.dev/getting-started.html) for PNG only (pngquant 3.0.3 and oxipng 10.2.1 are installed with mise on first use).

## Workflow for agents

1. After adding or replacing images, run `uvx imgsqueeze optimize <absolute paths of images or folders...> --json`.
2. Read `summary` in the JSON. Report any `error` results to the user. On exit code 3, pass the install instructions printed on stderr to the user; non-PNG images were still processed.
3. Commit each image together with its `.json` sidecar.
4. Never edit or delete a sidecar by hand. Remove orphans with `imgsqueeze doctor <dir> --delete-orphans`.
5. If the user says an image is over-compressed: have them restore the original (e.g. `git checkout`), then run `optimize --preset light` on it, or `imgsqueeze pin <path>` to keep it as is. Deleting the sidecar instead would compress the compressed image again.

Optional: `imgsqueeze check <dir>` exits 1 while some image has no matching sidecar, which suits a pre-commit hook.

## Import

```python
from imgsqueeze.api import optimize
import imgsqueeze.api as imgsqueeze     # then imgsqueeze.optimize
```

## Public API

Commands (problems with one image never raise; they become a result status):

- `optimize(inputs: list[Path], preset: str = "normal", min_gain: float | None = None, jobs: int | None = None, dry_run: bool = False) -> Report` — compress every image found that is not done. Raises `ValueError` for a bad argument.
- `check(inputs: list[Path]) -> list[CheckItem]` — which images are done, without compressing.
- `pin(inputs: list[Path]) -> list[PinItem]` — write a `pinned` sidecar so an image is kept as it is.
- `doctor(inputs: list[Path], delete_orphans: bool = False) -> DoctorReport` — orphan sidecars, pending images, leftover temp files.

Results:

- `Report(results: list[Result], tools: list[ResolvedTool])` — `.summary -> dict[str, int]` (`total`, one count per status, `bytes_saved`); `.missing_tools -> bool`.
- `Result(path, status, format, preset, before, after, sidecar_status, error, missing_tools, warnings: tuple[str, ...])` — `.gain -> float | None` (`1 - after / before`).
- `CheckItem(path, done: bool, sidecar_status, warning)`.
- `PinItem(path, status, error)` — status is `PIN_PINNED`, `PIN_ALREADY_DONE` or `PIN_ERROR`.
- `DoctorReport(orphans, deleted, pending, temp_files: list[Path])` — `.ok -> bool`.

Statuses (strings): `STATUS_OPTIMIZED` `"optimized"`, `STATUS_NO_GAIN` `"no_gain"`, `STATUS_ALREADY_DONE` `"already_done"`, `STATUS_CONFLICT` `"conflict"`, `STATUS_UNSUPPORTED` `"unsupported"`, `STATUS_ERROR` `"error"`; `RESULT_STATUSES` lists them. Sidecar-only: `STATUS_PINNED` `"pinned"`.

Presets: `PRESETS: dict[str, Preset]`, `PRESET_NAMES = ("light", "normal", "aggressive")`, `DEFAULT_PRESET = "normal"`, `DEFAULT_MIN_GAIN = {"png": 0.05, "jpeg": 0.05, "webp": 0.10}`, `get_preset(name: str) -> Preset`, `Preset(name, png_quality: tuple[int, int], jpeg_quality: int, webp_quality: int)`.

Sidecars: `Sidecar(final_size, original_size, preset: str | None, sha256, status, tool)`, `read_sidecar(image_path: Path) -> Sidecar | None`, `sidecar_path(image_path: Path) -> Path`, `InvalidSidecarError`.

External tools: `resolve_tool(spec: ToolSpec) -> ResolvedTool`, `PNGQUANT`, `OXIPNG` (`ToolSpec`), `ResolvedTool(name, path, version)`, `ToolUnavailableError`.

## CLI

The command is `imgsqueeze` (`uvx imgsqueeze ...` without installing; `.venv/bin/imgsqueeze` in a project venv). `imgsqueeze -h` lists the subcommands; every one that takes paths also accepts `--stdin` and `--json`.

## More detail

For full API docs see `ref/public-api.md`. For full CLI args, JSON output, and exit codes see `ref/cli.md`.
