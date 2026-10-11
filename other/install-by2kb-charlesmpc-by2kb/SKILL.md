---
name: install-by2kb
description: Install, configure, update, or diagnose the by2kb CLI for this Hermes plugin. Preserve existing configuration and keep Hermes-managed plugin code separate from CLI upgrades.
---

# Set up by2kb for Hermes

This plugin is already installed. Set up its separate CLI on the same machine and
under the same user as the Hermes gateway. Do not copy or replace the plugin, clone
the repository, or run `by2kb agent install hermes` from this workflow.

## Inspect first

- Check `by2kb version`, Python 3.12+, `ffmpeg`, `ffprobe`, and the available package
  manager. This plugin's staged request-file workflow requires by2kb 0.5.3 or newer;
  do not assume an arbitrary future version is compatible without checking its release notes.
- Check whether by2kb was installed with `pipx list` or `uv tool list`; use that
  manager for upgrades. Do not create a second installation with another manager.
- A missing command can be a PATH problem. On Windows use `Get-Command` and inspect
  `uv tool dir --bin` or `py -m pipx environment` when applicable. The gateway may
  need a restart to inherit a repaired PATH. `BY2KB_COMMAND` may name an absolute
  executable path (not a shell command with arguments).
- Treat `BY2KB_HOME` (default `~/.by2kb`), its `.env`, database, models, custom Skills,
  and the knowledge-base directory as user-owned. Do not display secret values.
- If configuration already exists, run `by2kb doctor --json` and repair only the
  reported problems. Do not run init or change providers just to make checks pass.

## First installation

Explain the dependencies and obtain agreement before installing. Prefer an already
available package manager; either of these installs an isolated CLI, not into Hermes:

```bash
pipx install "by2kb[asr-whisper,youtube]" --python 3.12
# Or, if uv is the chosen manager:
uv tool install --python 3.12 "by2kb[asr-whisper,youtube]"
```

Install ffmpeg/ffprobe using the platform's trusted package manager if missing.
Confirm the knowledge-base location, then, only for a new configuration:

```bash
by2kb init --preset agent-local --library-root "<chosen directory>"
```

Default to local Whisper and agent-hosted summaries; no separate LLM key or TOS
account is needed. Before `by2kb models install`, inspect `by2kb models status`,
explain the selected model and expected download size from its model information,
and obtain agreement. If the size cannot be established, say so rather than inventing it.
Then run `by2kb doctor --json` and explain remaining failures.

Cloud ASR is optional. If the user chooses Doubao, install the `asr-doubao,youtube`
extras using the same package manager and have them run `by2kb init` in a trusted
local terminal to configure TOS and ASR. Do not request secrets in chat. Preserve
existing configuration; changing an existing provider is a separate explicit choice.
The browser fallback is also optional: do not install Playwright or Chromium unless
the user chooses it. Follow the project's browser setup guide for that route.

## Finish and upgrade

- Enable the plugin with `hermes plugins enable by2kb` if needed. Ask before
  restarting an active gateway. Verify the gateway sees the CLI, then ask the user
  to send a test video URL. Do not claim success from installation alone.
- Upgrade the CLI with its existing manager: `pipx upgrade by2kb` or
  `uv tool upgrade by2kb`. Never run init with `--force` during an upgrade.
- For catalog-installed plugin code, use `hermes plugins update by2kb`. For a
  Git-pinned plugin, changing the pin requires an explicitly chosen full commit
  via Hermes install. Never self-update or replace this plugin from PyPI.
- If the installation is pinned to a Git URL, an upgrade may keep that old revision.
  Explain it and ask before migrating to PyPI or uninstalling anything.
- Run doctor again; preserve all user-owned state and stop for unresolved requirements.

After setup, use `skill_view("by2kb:video-to-knowledge")` for manual ingestion.
