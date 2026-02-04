---
name: agilab-runbook
description: Runbook for working in the AGILab repo (uv, Streamlit, run configs, packaging, troubleshooting).
license: BSD-3-Clause (see repo LICENSE)
metadata:
  short-description: AGILab repo runbook
  updated: 2026-01-08
---

# AGILab runbook (Agent Skill)

Use this skill when you need repo-specific “how we do things” guidance in `agilab/`: launching Streamlit, regenerating run-config wrappers, debugging installs, or preparing releases.

## Background: Agent Skills (status update 2026-01-08)

- Codex now supports **Agent Skills** using the open **Agent Skills** standard (`SKILL.md` + folder layout).
- Skills support **progressive disclosure**: only name/description load initially; full instructions load when invoked.
- Skill scopes: repo (`.codex/skills/…`), user (`~/.codex/skills/…`), and admin/system (`/etc/codex/skills/…`).
- Security note: skills are executable/context-bearing packages; treat third-party skills as supply-chain inputs (audit, pin versions, prefer sandboxes/approvals).

## AGILab working rules (repo policy)

- **Use `uv` for all runs** so dependencies resolve in managed envs:
  - `uv --preview-features extra-build-dependencies run python …`
  - `uv --preview-features extra-build-dependencies run streamlit …`
- **No repo `uvx`**: do not run `uvx agilab` from this checkout (it will run the published wheel and ignore local changes).
- **Run config parity**: after editing `.idea/runConfigurations/*.xml`, regenerate wrappers:
  - `uv --preview-features extra-build-dependencies run python tools/generate_runconfig_scripts.py`
- **Streamlit API**: do not add `st.experimental_rerun()`; use `st.rerun`.
- **No silent fallbacks**: avoid runtime “auto-fallbacks” between API clients or parameter rewrites; fail fast with actionable errors.

## Common commands (from the runbook matrix)

- Dev UI: `cd "$PROJECT_DIR" && uv --preview-features extra-build-dependencies run streamlit run src/agilab/AGILAB.py -- --openai-api-key "…" --apps-dir src/agilab/apps`
- Apps-pages smoke: `cd "$PROJECT_DIR" && uv --preview-features extra-build-dependencies run python tools/smoke_preinit.py --active-app src/agilab/apps/builtin/flight_project --timeout 20`
- Publish dry-run (TestPyPI): `cd "$PROJECT_DIR" && uv --preview-features extra-build-dependencies run python tools/pypi_publish.py --repo testpypi --dry-run --leave-most-recent --verbose`

## Troubleshooting reminders

- Missing import: check both manager and worker `pyproject.toml` scopes (`src/agilab/apps/<app>/pyproject.toml` and `src/agilab/apps/<app>/src/<app>_worker/pyproject.toml`).
- Installer pip issue: run `uv --preview-features extra-build-dependencies run python -m ensurepip --upgrade` once in the target venv.
