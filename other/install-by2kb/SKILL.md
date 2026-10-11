---
name: install-by2kb
description: Install, configure, update, or diagnose by2kb for an Agent user. Defaults to local faster-whisper and local Markdown; use a cloud ASR provider only when the user explicitly chooses one.
---

# Install by2kb

Install by2kb as an independent CLI package, then install its adapter into the active
Agent. Do not clone or inspect the by2kb source repository as an installation method.

## Before changing the system

1. Confirm the target machine is controlled by the user.
2. Check for Python 3.12+, `pipx`, `ffmpeg`, `ffprobe`, `by2kb`, and the Agent host.
   Check `uv tool list` too if uv is available; keep using the existing package
   manager, rather than creating a second installation. A command missing on Windows
   may be a PATH issue: inspect `Get-Command`, `uv tool dir --bin`, or
   `py -m pipx environment` as applicable, and check the gateway's environment.
3. If by2kb already has configuration, do not replace it. Run
   `by2kb doctor --json`, explain any failures, and preserve the current ASR and
   knowledge-base choices unless the user asks to change them.

## Default: local Agent installation

Use this path unless the user explicitly requests cloud ASR:

1. Install from PyPI with
   `pipx install "by2kb[asr-whisper,youtube]"`.
2. Create a cloud-free Agent configuration with
   `by2kb init --preset agent-local`. This selects local faster-whisper, Bilibili and
   YouTube sources, Agent-hosted summarization, and a local Markdown library.
3. Before downloading a Whisper model, tell the user its name and that the download
   can be large. Continue only after the user agrees, then run
   `by2kb models install`.
4. For Hermes, inspect `hermes plugins list` first. If the by2kb plugin is already
   installed, keep it and use `skill_view("by2kb:install-by2kb")` when available.
   Only for a new legacy/copy-based adapter install, run `by2kb agent install hermes`.
   Then run `by2kb doctor --json`. Catalog submission is pending; do not assume the
   bare catalog name is already available.
5. Restarting a running Agent can interrupt the current conversation. Ask before
   restarting it, then verify the gateway and ask the user to send one test video URL.

If pipx reports that by2kb is already installed, try `pipx upgrade by2kb`. If an old
direct-URL installation remains pinned or its virtual environment is broken, explain
the problem and ask before uninstalling and reinstalling it. Never delete a pipx
environment manually without explicit user approval.

## Upgrade without losing personalization

Treat `$BY2KB_HOME` (normally `~/.by2kb`) and the configured knowledge-base folder as
user-owned state. An upgrade must preserve `config.toml`, `.env`, `by2kb.db`, downloaded
models, custom Skills, and every knowledge artifact.

1. Inspect `by2kb version`, `pipx list`, and `by2kb doctor --json` first.
2. Run `pipx upgrade by2kb`. Do not run `by2kb init`, `by2kb init --force`, or rewrite
   configuration during an ordinary upgrade.
3. Inspect `hermes plugins list` and the installation source. For a catalog plugin,
   use `hermes plugins update by2kb`; for a Git-pinned plugin, let the user choose a
   new exact commit through Hermes. Never overwrite either with the CLI installer.
   Only a legacy/copy-based adapter may be refreshed with
   `by2kb agent install hermes --force`. If ownership is unclear, stop and inspect it.
4. Run `by2kb doctor --json` again and report any migration or restart requirement.

The Hermes adapter directory is program-owned. Put a personalized runtime Skill at
`$BY2KB_HOME/skills/video-to-knowledge/SKILL.md`, or set `BY2KB_HERMES_SKILL` to an
explicit file; both take precedence over the packaged Skill and survive adapter
replacement. Other enrichment Skills belong under `$BY2KB_HOME/skills` and already
take precedence over packaged defaults.

## Optional: cloud ASR

Use this path only when the user chooses Doubao ASR or cannot run Whisper locally:

1. Install `pipx install "by2kb[asr-doubao,youtube]"`.
2. Run `by2kb init` in a trusted local terminal and select `doubao` when prompted.
3. Do not ask the user to paste TOS or ASR credentials into an IM conversation. The
   initializer stores secrets in the local by2kb `.env` file.
4. Install the Agent adapter and run `by2kb doctor --json` as above.

Stop and report the exact failed check when a required runtime, credential, permission,
model download, or Agent restart needs user action. Do not weaken permissions or switch
providers merely to make diagnostics pass.
