---
name: geo-setup
description: "Initialize or repair the GEO-SEO Codex runtime for plugin and classic installer modes. Creates a Python virtual environment, installs requirements, verifies bundled scripts/templates, and explains optional PDF/browser dependencies."
---

# GEO Runtime Setup Skill

## Purpose

Use this skill when a GEO workflow needs bundled Python utilities, dependencies, templates, or PDF tooling and the runtime is missing or uncertain. It supports both installation modes:

- **Plugin mode:** skills are loaded from a `geo-seo-codex` plugin checkout/cache, while scripts, schema templates, and report templates remain in that plugin root.
- **Classic installer mode:** files are copied under `~/.codex/skills/geo/`, with sub-skills under `~/.codex/skills/geo-*/` and optional agents under `~/.codex/agents/`.

Do not require `~/.codex/agents/geo-*.toml` for setup. Agents are the preferred full-audit acceleration path when available; plugin-only installs must still work through skills fallback.

---

## Runtime Root Resolution

Resolve `GEO_ROOT` before running scripts:

1. If `CODEX_GEO_ROOT` is set and contains `scripts/`, use it.
2. If this skill was loaded from a plugin path like `<plugin-root>/skills/geo-setup/SKILL.md`, use `<plugin-root>`.
3. If the current repository contains `scripts/` and `requirements.txt`, use that repository root.
4. Fall back to the classic installer path: `${CODEX_HOME:-$HOME/.codex}/skills/geo`.

If no root contains `scripts/fetch_page.py`, stop and ask the user to install the plugin or run `install.sh` / `install-win.sh`.

---

## Setup Workflow

Run the equivalent of this shell flow in the user's environment:

```bash
GEO_ROOT="${CODEX_GEO_ROOT:-}"

if [ -z "$GEO_ROOT" ]; then
  for candidate in "$PWD" "$PWD/.." "$PWD/../.." "${CODEX_HOME:-$HOME/.codex}/skills/geo"; do
    if [ -f "$candidate/scripts/fetch_page.py" ]; then
      GEO_ROOT="$(cd "$candidate" && pwd)"
      break
    fi
  done
fi

if [ -z "$GEO_ROOT" ] || [ ! -f "$GEO_ROOT/scripts/fetch_page.py" ]; then
  echo "GEO runtime root not found. Set CODEX_GEO_ROOT to the geo-seo-codex plugin/repo root."
  exit 1
fi

if [ "$GEO_ROOT" = "${CODEX_HOME:-$HOME/.codex}/skills/geo" ]; then
  GEO_RUNTIME_DIR="$GEO_ROOT"
else
  GEO_RUNTIME_DIR="${CODEX_GEO_RUNTIME_DIR:-${CODEX_HOME:-$HOME/.codex}/geo-seo-codex}"
fi

mkdir -p "$GEO_RUNTIME_DIR"

if command -v python3 >/dev/null 2>&1; then
  GEO_SYSTEM_PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
  GEO_SYSTEM_PYTHON="python"
elif command -v py >/dev/null 2>&1; then
  GEO_SYSTEM_PYTHON="py"
else
  echo "Python 3.8+ is required."
  exit 1
fi

"$GEO_SYSTEM_PYTHON" -m venv "$GEO_RUNTIME_DIR/.venv"

if [ -x "$GEO_RUNTIME_DIR/.venv/bin/python" ]; then
  GEO_PYTHON="$GEO_RUNTIME_DIR/.venv/bin/python"
else
  GEO_PYTHON="$GEO_RUNTIME_DIR/.venv/Scripts/python.exe"
fi

"$GEO_PYTHON" -m pip install --upgrade pip
"$GEO_PYTHON" -m pip install -r "$GEO_ROOT/requirements.txt"

echo "GEO_ROOT=$GEO_ROOT"
echo "GEO_RUNTIME_DIR=$GEO_RUNTIME_DIR"
echo "GEO_PYTHON=$GEO_PYTHON"
```

On Windows, run the commands from Git Bash. If the user prefers the classic installer, use `./install-win.sh` instead.

---

## Verification

After setup, verify:

```bash
"$GEO_PYTHON" "$GEO_ROOT/scripts/fetch_page.py" https://example.com page
test -f "$GEO_ROOT/templates/geo-report-template.html"
test -f "$GEO_ROOT/templates/geo-report-style.css"
test -f "$GEO_ROOT/schema/organization.json"
```

Report the resolved `GEO_ROOT`, `GEO_RUNTIME_DIR`, and Python version.

---

## Optional Dependencies

PDF reports require:

- `pandoc`
- Google Chrome, Microsoft Edge, Chromium, or another compatible headless Chromium executable

Screenshot/browser features may require:

```bash
"$GEO_PYTHON" -m playwright install chromium
```

These are optional. If unavailable, core audit, schema, crawler, llms.txt, citability, and reporting workflows should still run without PDF/browser output.
