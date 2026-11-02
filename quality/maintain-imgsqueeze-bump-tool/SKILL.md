---
name: maintain-imgsqueeze-bump-tool
description: "Upgrade the pinned version of pngquant or oxipng in imgsqueeze: check the new version is installable through mise, verify the flags and exit codes imgsqueeze relies on, then update the pin, CI, docs and skills together. Use when the user asks to upgrade, bump, or update pngquant or oxipng, or when a newer release of either is out."
---

Move one external binary (`PNGQUANT` or `OXIPNG` in `imgsqueeze/tools.py`) to a new pinned version, proving first that the new version behaves the way imgsqueeze expects.

Read ../maintain-imgsqueeze-base/SKILL.md, then:
- ../maintain-imgsqueeze-base/references/02-compression-engines.md
- ../maintain-imgsqueeze-base/references/03-external-tools.md
- ../maintain-imgsqueeze-base/references/09-tests-and-ci.md

## Step 1: Find the candidate

- Current pin: the `ToolSpec` in `imgsqueeze/tools.py`.
- Latest version: `mise ls-remote conda:pngquant` or `mise ls-remote oxipng`. For pngquant also check that conda-forge has it for osx-arm64 and linux-64 (CI).
- Read the upstream changelog between the two versions. Report anything touching the flags or exit codes below, then **stop for the user's yes** before changing the pin.

## Step 2: Verify the new version in isolation

Install it with `mise install <mise_tool>@<new version>` (this changes no mise config), get its path with `mise which <name> --tool <mise_tool>@<new version>`, and check, as in `02-compression-engines.md`:

- pngquant: `--quality`, `--skip-if-larger`, `--strip`, `--speed`, `--force`, `--output` still exist; exit 98 on a gradient with the normal preset and 99 with quality 95-100; a non-zero code other than 98 and 99 on a corrupt file; and how it treats an ICC profile (currently: converts to sRGB).
- oxipng: `-o 2`, `--strip safe` (and which chunks it keeps), `--threads 1`, `--quiet`, `--out`; that `--out` is written even when nothing improves; that eXIf is dropped.
- `<binary> --version` still prints a `X.Y.Z` version that `tools._VERSION_PATTERN` finds.

Run the existing tests against it without touching the pin: `IMGSQUEEZE_PNGQUANT=<path> mise run cov` (or `IMGSQUEEZE_OXIPNG`). Any behavior change goes back to the user before going further.

## Step 3: Change the pin everywhere

Change these together, in one commit:

- `version=` of the `ToolSpec` in `imgsqueeze/tools.py`.
- The tests that assert the version (`grep -rn "<old version>" tests`: `tests/test_tools.py` and `tests/test_cli.py` today). In `tests/test_tools.py`, the fake override versions that sit just above and just below the pin (`3.0.4`, `3.0.2` for pngquant) must move with it.
- The `mise install` step in `.github/workflows/main.yml`.
- The versions in `README.rst`, `docs/source/` (`grep -rn "<old version>" README.rst docs/source`), `.claude/skills/pypi-imgsqueeze/`, and `.claude/skills/maintain-imgsqueeze-base/references/` (`03-external-tools.md`, `09-tests-and-ci.md`).
- Any measured behavior that changed, in `02-compression-engines.md`.

## Step 4: Verify and report

- `mise run cov` passes at 100% with mise on `PATH`, and `mise run lint` is clean.
- `mise run calibrate` still produces sensible sizes; a quantizer change can shift quality, so mention it if the numbers moved noticeably.
- Report the old and new versions, what was verified, and the files changed. Suggest a changelog entry with `pywf-oss-changelog`. CI only proves the Linux install after the user pushes.
