---
name: ha:verify
description: Verify Home Assistant changes — format, lint, typecheck, hassfest, and test in one loop. Use after implementation, before PRs, or after fixing bugs.
effort: low
---

# Verification Loop

Project-aware verification for Home Assistant (Python core/custom integrations + Lit ha-frontend). Detects the target checkout and reads `manifest.json`/`quality_scale.yaml` (or `package.json` for the frontend) to discover the domain, tier, and available tools before running anything.

## Iron Laws

1. **Detect the target before running** — Identify the checkout first (HA core / custom integration / ha-frontend); never run `mypy homeassistant/...` in a frontend repo, never run `yarn lint` in a core checkout
2. **Prefer the project's own gates** — `prek run` bundles the format/lint/hassfest layer; run it instead of the individual binaries when it is configured
3. **Prefer `prek`/`script/*` over raw binaries** — If `script/lint` or a `prek` config exists, use it over invoking `ruff`/`mypy` directly
4. **Run in dev-loop order** — `ruff format` → `ruff check --fix` → `mypy` → `hassfest` → `pytest`; later steps assume earlier ones pass
5. **Ask before the full suite** — Targeted domain tests run automatically; the whole-repo test run and `--snapshot-update` need user confirmation
6. **NEVER report success without showing actual command output** — "should work" is not verification

## Step 0: Project Discovery (ALWAYS FIRST)

Determine the target with the three-way detection, then read the domain metadata. See `${CLAUDE_SKILL_DIR}/references/project-discovery.md` for full patterns.

| Target | Test |
|---|---|
| HA core checkout | `[ -f homeassistant/__init__.py ] && [ -d script ]` |
| Custom integration | `custom_components/*/manifest.json` glob matches |
| ha-frontend | `package.json` present with `"name": "home-assistant-frontend"` |

**Discover the domain** (core/custom): the changed integration under `homeassistant/components/<domain>/` or `custom_components/<domain>/`; read `manifest.json` for `requirements`/`dependencies` and `quality_scale.yaml` for the tier (Bronze/Silver/Gold/Platinum) — the tier sets the coverage bar.

**Discover tools** (core/custom): `ruff`, `mypy`, `pytest`, `python3 -m script.hassfest`, `prek`. (frontend): `yarn lint`, `yarn lint:types`, `yarn test`.

**Discover the composite runner**: `prek run` bundles format + lint + hassfest via the pre-commit hooks (prek replaced pre-commit 2026-01). If a `.pre-commit-config.yaml` is present, `prek run --all-files` is the one-shot analog of a project `check` script.

Report discovery:

```
Target: HA core checkout | domain: mealie | tier: Bronze (coverage bar 100% config_flow)
Project tools: ruff ✓ | mypy ✓ | hassfest ✓ | pytest ✓ | prek ✓
Composite runner: prek run (bundles ruff-format, ruff, hassfest)
Strategy: prek run, then mypy + pytest --cov for the domain
```

## Verification Sequence

**CRITICAL**: Before using ANY discovered gate or composite command, verify it works:

1. Check the tool is importable / on PATH — a venv may not be activated (`script/setup` may not have run)
2. Run the command — if it fails with "command not found" or an import error, fall back to individual steps
3. Log the fallback: "prek run failed (venv not set up?), falling back to individual steps"

**If a composite gate exists** (`prek run`): Try it. If it fails, fall back to individual steps.

**Otherwise** (or after fallback): Run individual steps, skipping unavailable tools.

### Step 1: Format

`ruff format .` (or the touched files) — always. Check-only with `ruff format --check .`; 88-char line length is enforced.

### Step 2: Lint

`ruff check . --fix` — always. Auto-fixes import order (F401), unused variables (F841), and the `ASYNC` blocking-call rules; review what it rewrote.

### Step 3: Typecheck

`mypy homeassistant/components/<domain>/` — always (strict is opt-in per component).

> **`mypy.ini` is hassfest-generated — NEVER hand-edit it.** Adding a component to the strict list happens through hassfest, not by editing the ini. Enabling strict typing surfaces **type violations that were always there** as errors — no separate pass needed. If a previously-green component fails after being added to strict typing, suspect a newly-detected violation, not a regression. Read the message literally (expected vs actual type); it is almost always a real bug. See `python-idioms/SKILL.md`.

### Step 4: Manifest / strings / icons / quality-scale

`python3 -m script.hassfest --domain <domain>` — always (core/custom). Validates `manifest.json`, `strings.json`, `icons.json`, and `quality_scale.yaml`. This gate is unique to Home Assistant and it is non-negotiable.

### Step 5: Test + coverage

`pytest tests/components/<domain>/ --cov=homeassistant.components.<domain> --cov-report term-missing` — use the domain's test dir. Coverage bar: **config_flow 100%** (merge-blocking), **Silver+ 95%** overall.

### Step 6: Snapshot review

If the diff touches entity platforms with syrupy snapshots, regenerate and **review the `.ambr` diff** before committing: `pytest tests/components/<domain>/ --snapshot-update`. Never blind-accept snapshot changes — a wrong state or attribute will pass silently.

### Step 7: Additional Test / Translations Offer

After core verification passes, offer the slower or broader runs. **Ask the user**:

```
Core verification passed. Additional runs available:
1. pytest tests/components/<domain>/ --snapshot-update — regenerate .ambr (review the diff)
2. python3 -m script.translations develop — translations dev loop
3. pytest (whole-repo suite) — ~long
Run any of these? [1/2/3/skip]
```

Frontend equivalent (ha-frontend checkout): `yarn lint`, `yarn lint:types`, `yarn test`.

Skip unavailable tools with: "hassfest: ⏭ Not a core/custom checkout".

## Quick Reference

| Step | Command | Condition |
|------|---------|-----------|
| Discovery | Detect target + read manifest/quality_scale | Always first |
| Composite | `prek run` | If a pre-commit config exists |
| Format | `ruff format .` | Always |
| Lint | `ruff check . --fix` | Always |
| Typecheck | `mypy homeassistant/components/<domain>/` | Always (core/custom) |
| Manifest/strings | `python3 -m script.hassfest --domain <domain>` | Always (core/custom) |
| Test | `pytest tests/components/<domain>/ --cov=homeassistant.components.<domain> --cov-report term-missing` | Always |
| Snapshot | `pytest tests/components/<domain>/ --snapshot-update` | If entity snapshots changed (review diff) |
| Frontend | `yarn lint`, `yarn lint:types`, `yarn test` | ha-frontend checkout |
| Full suite / translations | Ask user | Pre-PR |

## Usage

1. Run `/ha:verify` — discovery happens automatically
2. Core checks run in dev-loop order, adapted to the detected target
3. After pass, offered snapshot regen, translations dev loop, and the full suite
4. Commit only after all chosen checks pass
