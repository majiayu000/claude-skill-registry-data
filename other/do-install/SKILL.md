---
name: do-install
description: Install the maverick CLI tool system-wide from the plugin directory.
user-invocable: true
disable-model-invocation: false
context: fork
---

# Install Maverick CLI

Install the `maverick` CLI from wherever this plugin is loaded — marketplace cache or local dev checkout.

## Execution Context

This skill runs in its own forked context (`context: fork`) — you are
executing it directly; there is no separate agent to dispatch. Follow the
process below exactly and end with a structured result: task, SUCCESS or
FAILURE, what was done, and any warnings.

## Process

1. **Locate the plugin root.** This is the directory containing `pyproject.toml`. If `${CLAUDE_PLUGIN_ROOT}` is set, use that. Otherwise resolve two levels above this `SKILL.md` (i.e. the parent of `skills/do-install/`). Fail with a clear error if `pyproject.toml` is not found at the resolved path.

2. **Run the installer.** From a shell:

       uv run --directory <plugin-root> python -m maverick.install_cli

   The module performs the install procedure end-to-end:
   - verifies `uv` is on PATH
   - verifies `gh` (GitHub CLI) is on PATH — Maverick workflows depend on it for issue and PR operations; the installer fails with platform-specific install instructions if missing
   - verifies `pyproject.toml` exists at the plugin root
   - runs `uv tool install --force <plugin-root>`
   - verifies `maverick` is on PATH (warns about `~/.local/bin` if not)
   - adds `Read(~/.claude/plugins/cache/thermite/maverick/**)` to `~/.claude/settings.json` `permissions.allow` (idempotent)

3. **Verify.** Run `maverick --help` and capture the first line.

4. **Report.** Return a structured result: install path, whether the settings file was modified or already had the permission entry, and any PATH warnings.

<!-- maverick-plugin-version: 4.0.2-dev -->
