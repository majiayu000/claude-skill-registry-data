---
name: help
description: >-
  Answer questions about Shipyard itself — commands, SY_*/ACLI_* config knobs, which model an
  agent uses, workflow behavior, diagnosis recipes — by reading the plugin's own docs and citing
  the source. Never reads the tracker or the target repo's code.
argument-hint: "[question about Shipyard]"
---

Answer a question about how Shipyard (this plugin) works. `$ARGUMENTS` is the question; if empty, say what this can answer and give two or three example questions instead of guessing at intent.

This skill inherits caller model/effort. It only reads the plugin's own bundled files below — never the tracker, never the target repo's code or its board. A question about the target codebase or a ticket belongs to `/sy:explain` or the tracker skill, not this one.

## Sources, read only what the question needs

Every read and grep target below is rooted at `${CLAUDE_PLUGIN_ROOT}` — a normal (non-`--plugin-dir`) install runs commands with the *user's repo* as cwd, so a bare relative path silently reads nothing or the wrong file.

1. `${CLAUDE_PLUGIN_ROOT}/docs/configuration.md` — every setting: layer, default, required?, meaning. Authoritative for "where do I configure X" / "what setting controls Y". For what a given repo *actually* resolves to, call the `show_config` tool rather than quoting a default.
2. `${CLAUDE_PLUGIN_ROOT}/agent-guide.md` — concepts, install/config walkthrough, **Diagnosis recipes** (symptom → cause → fix).
3. `${CLAUDE_PLUGIN_ROOT}/README.md`, `${CLAUDE_PLUGIN_ROOT}/docs/usage.md`, `${CLAUDE_PLUGIN_ROOT}/docs/installation.md`, `${CLAUDE_PLUGIN_ROOT}/docs/github-setup.md` — the loop, day-to-day usage, one-time setup.
4. The specific `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md` or `${CLAUDE_PLUGIN_ROOT}/agents/<name>.md` the question names or implies — read it directly rather than guessing at its behavior.

If none of the above cover it, grep `${CLAUDE_PLUGIN_ROOT}/skills/` and `${CLAUDE_PLUGIN_ROOT}/agents/` for the topic before giving up.

## Answer

State the answer first, then cite it as a repo-relative `file:line` (e.g. `docs/configuration.md:12`) — that's what the user can actually open, even though the read above went through `${CLAUDE_PLUGIN_ROOT}`. If the question spans a setting and where it's consumed — "what model does gate use" — give both: the setting (`models.agents.gate.model`, `docs/configuration.md`) and the consumer (`skills/ship/references/immutable-gate.md`), reading the actual current line rather than assuming one — the file shifts over time and a pinned line number is a snapshot, not ground truth. For a "what is my config actually set to" question, prefer calling the `show_config` tool, which reports each value with the layer it came from, over quoting a default from the docs.

If nothing in the plugin's files answers it, say so plainly and point at the nearest real doc — never infer or fabricate a variable name, default, or behavior.
