---
name: litestar-build
description: "Auto-activate for uv build, hatch build, PyApp, PYAPP_*, wheel assets, GitHub release matrices, cargo-zigbuild, or python-build-standalone. Not for runtime deployment."
---

# litestar-build

Build-side packaging patterns for Litestar applications: how to produce a **self-contained wheel** that embeds the Vite/Bun frontend, how to wrap that wheel in a **PyApp onefile** binary, and how to wire the whole pipeline into **GitHub Actions** CI and releases.

This skill is the counterpart to [litestar-deployment](../litestar-deployment/SKILL.md) — build is about producing artifacts, deployment is about running them.

## The Core Idea: One Wheel, Self-Contained

A Litestar wheel is the single source of truth for a release. It contains:

- Python code (`src/py/app/` or `app/`)
- SQL migrations, Jinja templates, INI configs
- The **built** Vite/Bun frontend bundle (JS, CSS, HTML, images)
- Email templates rendered from React/MJX to static HTML

Once produced, that wheel can be:

1. `pip install`ed into a container (litestar-deployment).
2. Wrapped in a **PyApp** binary (`dist/<app>`, `dist/app-x86_64-linux-gnu`) for zero-dep distribution.
3. Uploaded to PyPI or a private index.

All three paths assume the wheel is **already complete** — no `bun run build` happens at deploy/install time.

### Why bundle assets into the wheel (and not serve from a CDN)

| Property | Bundled wheel | External CDN |
| --- | --- | --- |
| Deploy artifacts | 1 (`.whl` or binary) | 2+ (wheel + CDN upload) |
| Version alignment | Atomic — API and UI lock-step | Easy to skew; rollback is painful |
| PyApp onefile | Required — the binary embeds the wheel | Not possible — binary can't fetch CDN URLs at install time |
| Offline/air-gapped | Works | Doesn't |
| Dev server startup | Instant (files on disk next to package) | Fine |
| Frontend-only deploys | Rebuild + redeploy wheel | Push to CDN only |

For **most Litestar apps that ship as a product** (CLIs, internal tools, enterprise installers), bundled-in-wheel is correct. Projects like [litestar-fullstack-inertia](#example-projects) and [litestar-fullstack](#example-projects) all bundle.

### Why litestar-vite configs look the way they do in reference apps

This is the piece most developers miss. The Vite/litestar-vite configs in the reference apps are **deliberately set up so the Vite output lands inside the Python package directory** — because that's what makes the wheel pick them up automatically.

**litestar-fullstack** (`src/js/web/vite.config.ts`):

```ts
export default defineConfig({
  build: {
    outDir: path.resolve(__dirname, "../../py/app/server/static/web"),  // ← inside src/py/app/ (the Python package)
    emptyOutDir: true,
  },
  plugins: [
    litestar({
      bundleDir: path.resolve(__dirname, "../../py/app/server/static/web"),
      hotFile: path.resolve(__dirname, "../../py/app/server/static/web/hot"),
    }),
  ],
})
```

**litestar-fullstack-inertia** — in `litestar-vite` v0.30+, Python `ViteConfig(paths=PathConfig(bundle_dir=...))` is the single source of truth and writes `.litestar.json` on startup/CLI invocation so `litestar({ input: [...] })` in `vite.config.ts` inherits `bundleDir` and `hotFile` automatically:

```python
def get_vite_config() -> ViteConfig:
    """Configure litestar-vite to emit assets inside the app/ Python package."""
    return ViteConfig(
        paths=PathConfig(
            root=BASE_DIR.parent,
            bundle_dir=Path("app/domain/web/public"),
            resource_dir=Path("resources"),
        ),
    )
```

**Advanced reference pattern** — same approach: Vite and the offline-report build write to `src/py/<app>/server/public/` and `src/py/<app>/domain/web/static/reports/offline/`, both under the package root.

Contrast with a naïve `vite build` that writes to `./dist/` at the repo root: those files are **outside** the package directory listed in `[tool.hatch.build.targets.wheel] packages = [...]`, so Hatchling silently drops them. The wheel ships without a frontend.

Rule: **Vite's `outDir` and litestar-vite's `bundle_dir` must point inside one of the Python packages that Hatchling is told to include.** Everything else flows from that.

## Code Style Rules

- Emit all compiled frontend bundles (`PathConfig.bundle_dir` / Vite `build.outDir`) inside a Python package directory included by Hatchling (`app/...` or `src/py/<pkg>/...`).
- Choose exactly one Hatchling asset inclusion strategy (`[tool.hatch.build.targets.wheel.force-include]` OR `ignore-vcs = true`) — never combine both.
- Guard custom Hatchling build hooks (`BuildHookInterface.initialize`) with `if version == "editable": return` so `uv sync` succeeds before frontend assets are built, and exclude `tools/build` from `mypy` and `pyright`.
- Run asset compilation, static template generation, and license collection before `uv build --wheel --clear`.
- Treat `PYAPP_*` configuration variables (`PYAPP_PROJECT_PATH`, `PYAPP_PYTHON_VERSION`, `PYAPP_DISTRIBUTION_EMBED`, `PYAPP_DISTRIBUTION_VARIANT_GIL`, `PYAPP_SKIP_INSTALL`) as compile-time inputs to `cargo build` / `cargo zigbuild`; at runtime, inspect `os.getenv("PYAPP")` (`"1"` or path when running under Pass-Through) to detect PyApp execution.
- Use `cargo zigbuild --release --target <arch>-unknown-linux-gnu.2.17` with `BZIP2_SYS_STATIC=1` and `LZMA_API_STATIC=1` when building portable Linux PyApp binaries.

## Quick Reference

| Topic | Reference | Key Commands |
| --- | --- | --- |
| Wheel build + asset bundling | [references/wheel-assets.md](references/wheel-assets.md) | `uv build --wheel --clear`, `[tool.hatch.build.targets.wheel.force-include]`, `ignore-vcs = true` |
| PyApp — simple (hatch-binary) | [references/pyapp-simple.md](references/pyapp-simple.md) | `uv run hatch build --target binary` |
| PyApp — advanced (offline + custom install dir) | [references/pyapp-advanced.md](references/pyapp-advanced.md) | `tools/bundler.py build`, `cargo zigbuild` |
| GitHub Actions CI (test matrix) | [references/github-ci.md](references/github-ci.md) | `astral-sh/setup-uv@v7`, `oven-sh/setup-bun@v2`, composite actions |
| GitHub Actions release | [references/github-release.md](references/github-release.md) | matrix onefiles, `cargo-zigbuild`, `gh release create` |
| Upgrading Python / PyApp | [references/upgrading.md](references/upgrading.md) | Files to edit in sync |

## Canonical Makefile Build Graph

Every Litestar app with bundled assets has some variant of this:

```makefile
.PHONY: install build-assets build-wheel build-onefile

install:                          ## Install Python + JS deps
	@uv sync --all-groups
	@cd src/js/web && bun install --frozen-lockfile

build-assets:                     ## Build frontend into the Python package
	@uv run app assets install
	@uv run app assets build

build-wheel: build-assets         ## Self-contained Python wheel
	@uv build --wheel --clear

build-onefile: build-wheel        ## Single-file PyApp binary
	@./tools/scripts/build-onefile-package.sh
```

The dependency chain is **load-bearing**: `build-onefile` depends on `build-wheel`, which depends on `build-assets`. Running them out of order produces an empty or broken artifact.

### The two-variant story

Real projects have multiple JS build outputs that all need to land in the wheel:

```makefile
js-build-all: js-build-web js-build-offline-report
build-wheel: generate-licenses build-templates js-build-all
	@uv build --wheel --clear
```

Each `js-build-*` target emits into a distinct subdirectory of the Python package (`src/py/<app>/server/public`, `src/py/<app>/domain/web/static/reports/offline`, etc.). Because they're all inside the package, a single `uv build --wheel --clear` captures everything.

<workflow>

## Workflow

### Step 1: Point Vite output inside the Python package

Configure `ViteConfig(paths=PathConfig(bundle_dir=Path("app/domain/web/public")))` in Python so `.litestar.json` bridges the target directory to `litestar-vite-plugin`. If `vite.config.ts` overrides `build.outDir` directly (monorepo or standalone Vite build), set `build.outDir` and `litestar({ bundleDir, hotFile })` to an absolute path inside your Python package (`src/py/<pkg>/...` or `<pkg>/...`). **Do not** let Vite default to `./dist/`.

### Step 2: Choose a Hatchling bundling strategy

- **`force-include`** (inertia): List the built-asset directory explicitly under `[tool.hatch.build.targets.wheel.force-include]`. Built assets stay `.gitignore`d. Explicit, auditable.
- **`ignore-vcs = true`** (SPA): Tell Hatchling to ignore `.gitignore`. All package files ship. Simpler; requires discipline to keep dev junk out of package dirs.
- **Optional custom Hatchling hook**: If you add a `BuildHookInterface` subclass to run `bun run build` during `uv build`, guard `initialize(version, build_data)` with `if version == "editable": return` so `uv sync` does not trigger a frontend build during editable installs.

See [references/wheel-assets.md](references/wheel-assets.md) for full config.

### Step 3: Wire Makefile targets

Create `install`, `build-assets`, `build-wheel`. Make the wheel target **depend** on the asset target. Pass `--clear` to `uv build --wheel --clear` so stale wheels in `dist/` never get picked up by downstream packaging steps.

### Step 4: Add PyApp (if shipping a binary)

Decide which flavor:

- **Simple**: add `[tool.hatch.build.targets.binary]` to `pyproject.toml` and run `uv run hatch build --target binary`. Good when end-users have PyPI access. See [pyapp-simple.md](references/pyapp-simple.md).
- **Advanced**: write a `tools/bundler.py` that pre-installs deps into a `python-build-standalone` archive, patches PyApp's `src/app.rs` for a custom install dir, then runs `cargo zigbuild`. Good for air-gapped distribution or bespoke install locations. See [pyapp-advanced.md](references/pyapp-advanced.md).

### Step 5: Add GitHub Actions CI

Start with a reusable `test.yml` that accepts `python-version` + `coverage` inputs. Call it from `ci.yml` across a matrix. Use `astral-sh/setup-uv@v7` and `oven-sh/setup-bun@v2`. See [github-ci.md](references/github-ci.md).

For larger projects, factor `setup-python` and `setup-node` into `.github/actions/` composite actions.

### Step 6: Add release workflow

Trigger on `v*` tags. Run the test matrix first. Then build the wheel once. Then build PyApp onefiles in a per-target matrix (`x86_64-unknown-linux-gnu`, `aarch64-unknown-linux-gnu`, Apple, Windows). Upload to `gh release create`. See [github-release.md](references/github-release.md).

</workflow>

<guardrails>

## Guardrails

- **Vite/bun output must land inside a Python package directory.** Otherwise Hatchling drops it. Set `PathConfig.bundle_dir` (and any explicit Vite `build.outDir`) to a path under `src/py/<pkg>/` or `<pkg>/`.
- **`uv build` runs last.** Assets, licenses, templates, OpenAPI TypeGen all run **before** `uv build --wheel --clear`.
- **Pick one bundling strategy.** `force-include` or `ignore-vcs = true`, not both. Mixing them causes duplicate-file warnings and unpredictable wheel contents.
- **Skip editable installs in custom Hatchling hooks.** If a custom `BuildHookInterface` runs in `pyproject.toml`, short-circuit when `version == "editable"` and exclude the hook directory from `mypy`/`pyright` unless `hatchling` is in the typecheck environment.
- **PyApp `PYAPP_*` config vars are build-time, not runtime.** `PYAPP_PROJECT_NAME`, `PYAPP_PYTHON_VERSION`, `PYAPP_DISTRIBUTION_EMBED`, `PYAPP_DISTRIBUTION_VARIANT_GIL` are consumed when `cargo build` compiles PyApp — not when the resulting binary runs. At runtime, PyApp sets `PYAPP=1` (or the executable path when `PYAPP_PASS_LOCATION=1`) inside the spawned Python process.
- **PyApp version upgrades touch multiple files.** `pyproject.toml`, `build-onefile-package.sh`, `.github/workflows/release.yml`, `tools/bundler.py`. See [upgrading.md](references/upgrading.md).
- **`cargo-zigbuild` for portable glibc.** Plain `cargo build` on a modern Linux runner produces binaries that fail on older distros (glibc too new). Use `cargo zigbuild --target x86_64-unknown-linux-gnu.2.17` to link against glibc 2.17 (CentOS 7-era). Required for broad compatibility.
- **Static-link native deps in PyApp.** Set `BZIP2_SYS_STATIC=1` and `LZMA_API_STATIC=1` before `cargo zigbuild`, or patch `Cargo.toml` to add `features = ["static"]`. Otherwise the onefile fails to load on systems without matching `libbz2.so` / `liblzma.so`.
- **Pin `uv` and `bun` versions in CI.** Use exact pinned versions (e.g., `UV_VERSION=0.11.6` and `BUN_INSTALL_VERSION=bun-v1.3.12`). Drift in either breaks reproducible builds.
- **Create placeholder asset dirs in CI.** Hatchling's `force-include` target fails if `app/domain/web/public` or `src/py/app/server/static/web` doesn't exist at wheel/editable-build time. CI jobs that don't build the frontend (lint, mypy, pyright) still need `mkdir -p <asset-dir>` before `uv sync`.
- **Never commit built frontend output.** Keep `bundle_dir` paths in `.gitignore`. CI rebuilds them on every run. Reason: JS builds are non-deterministic across machines and cause noisy diffs.
- **Coverage on one Python version only.** Multiple versions uploading the same `coverage.xml` silently stomp each other. Pin it to one version in your matrix (`if: matrix.python-version == '3.12'`).
- **Disk cleanup on self-hosted runners.** GitHub's `ubuntu-latest` has ~30GB free; building wheels + PyApp + Docker images can blow past that. Aggressive cleanup before the build job is routine.

</guardrails>

<validation>

## Validation Checkpoint

Before claiming "the wheel builds":

- [ ] `make build-wheel` succeeds in a clean checkout (after `make install`)
- [ ] `unzip -l dist/*.whl | grep -E '\.(js|css|html)$'` shows the built frontend
- [ ] The wheel installs cleanly (`uv pip install dist/*.whl` in a fresh venv)
- [ ] `python -c "import app; app.run()"` (or equivalent) serves assets with no extra steps
- [ ] `.gitignore` excludes the built asset directory
- [ ] `PathConfig.bundle_dir` (and any explicit Vite `build.outDir`) resolves inside a Python package dir
- [ ] Hatchling config uses exactly one of `force-include` OR `ignore-vcs = true`

Before claiming "the PyApp binary works":

- [ ] `dist/<app> --help` runs on the build machine
- [ ] The binary is ≥ 50 MB (much smaller means it's not embedding Python)
- [ ] On Linux, `ldd dist/<app>` shows ≤ libc / libm / libpthread (no `libbz2`, no `liblzma`)
- [ ] A network-isolated `docker run --rm --network=none gcr.io/distroless/cc-debian12:nonroot /opt/dist/<app> --help` succeeds (proves no runtime PyPI fetches)
- [ ] The install dir (`~/.<app>/runtime/` or similar) is created on first run and re-used on second run

Before claiming "CI works":

- [ ] Python matrix covers minimum + stable + latest (e.g., 3.11, 3.12, 3.13)
- [ ] `make build-wheel` runs in CI and the resulting wheel is uploaded as an artifact
- [ ] Pre-commit / ruff / mypy / pyright / slotscheck run on every PR
- [ ] Release workflow is gated on CI (`needs: [lint, test]`)
- [ ] A tag push produces wheel + onefiles + GitHub release in one run

</validation>

<example>

## Example

```toml
[build-system]
build-backend = "hatchling.build"
requires = ["hatchling"]

[tool.hatch.build.targets.wheel]
packages = ["app"]

[tool.hatch.build.targets.wheel.force-include]
"app/domain/web/public" = "app/domain/web/public"

[tool.hatch.build.targets.binary]
pyapp-version = "0.29.0"
python-version = "3.13"
scripts = ["app"]

[tool.hatch.build.targets.binary.env]
PYAPP_DISTRIBUTION_EMBED = "1"
PYAPP_FULL_ISOLATION = "1"
PYAPP_UV_ENABLED = "1"
```

### Example Projects

- **[litestar-fullstack-inertia](https://github.com/litestar-org/litestar-fullstack-inertia)** — monolithic `app/` layout, Inertia.js + React 19, `force-include` bundling, `hatch build --target binary` for 4-platform PyApp.
- **[litestar-fullstack](https://github.com/litestar-org/litestar-fullstack)** — nested `src/py/app/` + `src/js/web/` layout, React + TanStack Router SPA, `ignore-vcs = true` bundling, React Email templates.

</example>

## References Index

- [Wheel Build + Asset Bundling](references/wheel-assets.md)
- [PyApp — Simple (hatch-binary)](references/pyapp-simple.md)
- [PyApp — Advanced (offline, custom install dir, portable glibc)](references/pyapp-advanced.md)
- [GitHub Actions — CI (Test Matrix)](references/github-ci.md)
- [GitHub Actions — Release](references/github-release.md)
- [Upgrading — Python, PyApp, python-build-standalone](references/upgrading.md)

## Official References

- <https://ofek.dev/pyapp/> — PyApp documentation (all `PYAPP_*` env vars)
- <https://github.com/ofek/pyapp> — PyApp source (patch target: `src/app.rs`)
- <https://hatch.pypa.io/latest/config/build/> — Hatchling build config
- <https://hatch.pypa.io/latest/plugins/builder/binary/> — Hatch binary builder (simple PyApp)
- <https://docs.astral.sh/uv/concepts/projects/build/> — `uv build` reference
- <https://github.com/astral-sh/python-build-standalone/releases> — Portable Python archives
- <https://github.com/rust-cross/cargo-zigbuild> — cargo-zigbuild for portable glibc
- <https://bun.sh/docs/cli/install> — Bun install and lockfile

## Cross-References

- [litestar-deployment](../litestar-deployment/SKILL.md) — runtime deployment (Dockerfiles, K8s, Railway, Cloud Run, systemd) that consumes the artifacts this skill produces
- [litestar-vite](../litestar-vite/SKILL.md) — Vite plugin config (asset pipeline details, TypeGen, HMR)
- [litestar-granian](../litestar-granian/SKILL.md) — Granian ASGI server (what the wheel's entry-point starts)
- [litestar settings](../litestar/references/settings.md) — env-driven `@dataclass` settings that work both in-wheel and as a PyApp binary

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [CI/CD](../litestar-styleguide/references/ci-cd.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
