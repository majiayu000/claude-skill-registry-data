---
name: codex-slides-research
description: Compatibility entry point for researching a current topic into a source-backed Markdown brief and turning it into a Codex Slides outline or rendered deck. Use for market, competitive, policy, technical, academic, or other presentation requests that need current facts, figures, comparisons, or citations.
---

# Codex Slides Research

The canonical `codex-slides` sibling skill owns the complete workflow. Use
`deep_research` when MCP is available; otherwise run CLI command `research` at
`../codex-slides/scripts/codex-slides.mjs`. Preserve its Markdown and citations
so the user can review or edit the evidence before slide generation.

For the default interactive workflow, first open the Codex Slides home screen
in the Codex Browser, submit the research request there, and keep the created
project visible while its research, outline, style, and render checkpoints
advance. Use the lower-level sequence below only for CLI automation, recovery,
or a user-requested headless workflow:

1. If a research workflow fits, call `list_scenarios` / CLI `scenarios` and
   pass the selected `scenarioId` into `deep_research` / CLI `research` with
   one to four rounds. This carries the scenario's evidence contract into the
   search brief.
2. Call `create_outline` / CLI `outline` with `researchDoc` set to the reviewed brief.
3. Revise the draft with `revise_outline` / CLI `revise-outline` when needed.
4. Call `render_deck` / CLI `render` only after the outline is accepted.
5. Call `open_codex_slides` / CLI `open` and navigate the returned project
   resource or URL in the in-editor Browser for visual verification.

For an explicitly requested unattended fast path, call `create_deck` with
`research: true`. Do not claim a brief is source-backed when its returned
Markdown has no source links.

For a durable outline revision or render that should survive navigation, use
`start_project_run`, then retain and track its `runId` while the Browser remains
on the matching checkpoint.
