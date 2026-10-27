---
name: copilot-plugin-creator
description: 'Create, update, maintain, and evolve GitHub Copilot agent plugins for CLI, VS Code, or both. Use when scaffolding or refining plugin.json, reconciling manifest drift, choosing runtime-specific component fields, wiring plugin components, or governing shared versions across multi-runtime plugins.'
argument-hint: 'Plugin name, runtime (cli|vscode|both), task mode, components, and canonical version/source details'
metadata:
  version: 1.2.0
  author: arisng
---

# Copilot Plugin Creator

Use this skill when the user wants to create, update, maintain, refine, or evolve a GitHub Copilot plugin. It covers greenfield scaffolding, runtime expansion, manifest cleanup, version alignment, and drift repair.

## Outcomes

- Create a new plugin for CLI, VS Code, or both
- Update or refine an existing plugin without violating runtime-specific plugin rules
- Reuse existing artifacts through correct relative paths when appropriate
- Proactively discover and select likely plugin components when users do not specify them
- Keep canonical plugin metadata and runtime/generated manifests aligned
- Reconcile drift between source manifests, mirrors, and shared versions
- Avoid mixing CLI-only assumptions into VS Code plugins
- Generate a minimal, pragmatic `README.md` when creating a new plugin or filling a missing plugin README
- Leave the user with the smallest viable scaffold or maintenance patch for the requested runtime

## Required Inputs

Extract these from the user request. Ask only for missing items that block a correct authoring or maintenance change.

- Plugin name in kebab-case
- Task mode: new plugin, maintenance/refinement, runtime expansion, drift reconciliation, or release/version bump
- Runtime target: `cli`, `vscode`, or `both`
- Short purpose/description
- Which artifacts to bundle: `agents`, `skills`, `commands`, `hooks`, `mcpServers`, `lspServers`
- Whether to reference existing artifacts or create plugin-local placeholders
- Canonical writable source for shared plugin metadata/version if one exists
- Intended use: local development, team sharing, or distributable bundle

## Reference Sources

This skill is self-contained. Use official runtime documentation only when you need to confirm current platform behavior, schema details, or installation mechanics.

- Copilot CLI plugin reference: https://docs.github.com/en/copilot/reference/cli-plugin-reference
- Copilot CLI plugin how-to: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating
- VS Code agent plugins: https://code.visualstudio.com/docs/copilot/customization/agent-plugins

## Workflow

1. Classify the request as new-plugin authoring, existing-plugin maintenance, or both.
2. Determine whether the scope is CLI, VS Code, or both, then inspect all relevant manifests and source-of-truth files.
3. Run deep analysis on user intent and repository context to infer likely plugin components when explicit component lists are missing.
4. Build a candidate component map (`agents`, `skills`, `commands`, `hooks`, `mcpServers`, `lspServers`) and select only components supported by available artifacts.
5. Decide whether the plugin should reference existing artifacts or include plugin-local starter files.
6. For Ralph-like multi-runtime plugins, or any plugin that is really one product with shared behavior, use one canonical workflow/product version and treat runtime/channel identity as derived metadata unless there is a real independent release cadence.
7. Create or update the runtime-specific directory using the repository's established layout. If no layout exists yet, default to `plugins/cli/<name>/` and `plugins/vscode/<name>/`.
8. Write or refine `plugin.json` with only the fields that belong to that runtime and request.
9. If reusing existing artifacts, calculate relative paths from the plugin directory to the real component locations. If starter files are requested, create only the minimum folders/files needed for the declared component paths.
10. Reconcile drift between source manifests, generated/runtime mirrors, and canonical versions. Refresh or validate mirrors instead of hand-maintaining separate per-file semver where possible.
11. Create `README.md` only when the plugin is new, missing one, or the user explicitly asks for it.
12. Summarize what changed, what components were inferred, any version/bump decision, assumptions made, and the next validation step.

## Component Discovery Protocol

Use this protocol whenever component lists are incomplete or omitted:

1. Parse user intent for verbs and nouns that imply capability types (for example: orchestrate -> agents, automation -> hooks/commands, external integration -> mcpServers).
2. Inspect repository/customization context for existing artifacts that match the intent.
3. Produce a short inferred component plan with confidence labels (`high`, `medium`, `low`).
4. Auto-select `high` confidence components and proceed.
5. Ask concise follow-up questions only for `medium` or `low` confidence decisions that materially change plugin shape.

## CLI Plugin Rules

- Prefer `plugins/cli/<name>/plugin.json` unless the repository already uses a different plugin layout.
- Only use official CLI component fields: `agents`, `skills`, `commands`, `hooks`, `mcpServers`, `lspServers`.
- Do not add an `instructions` field to `plugin.json`.
- Prefer relative paths to existing artifacts for repository-internal plugins.
- If the plugin is meant to be packaged, keep the plugin self-contained or compatible with the repository's packaging flow.

## VS Code Plugin Rules

- Prefer `plugins/vscode/<name>/plugin.json` unless the repository already uses a different plugin layout.
- Validate plugin behavior against the current VS Code agent plugin documentation before assuming the CLI schema or install flow applies.
- Treat VS Code agent plugins as preview unless the official docs state otherwise.
- When useful in the final response, mention `chat.plugins.enabled`, `chat.plugins.paths`, and `chat.plugins.marketplaces` for local usage and discovery.

## Decision Points

### Existing artifacts vs placeholders

- Prefer existing artifacts when the user describes a plugin that bundles work already present in the repository.
- Create placeholders only when the user explicitly asks for a starter scaffold or the plugin would otherwise point to non-existent components.

### Single runtime vs both

- If the user requests both runtimes, create separate plugin directories for CLI and VS Code.
- Do not assume the two manifests can be identical.

### Version governance

- Prefer one canonical workflow/product version across runtime variants when the plugin is one product with shared behavior.
- Treat runtime or channel identity as derived metadata, not a separate semver stream, unless the plugin truly ships on independent cadences.
- Avoid independent per-file semver for wrappers or manifests. Prefer one writable source for shared version data plus generated or validated mirrors.
- Maintenance work includes reconciling drift between canonical versions, source manifests, and generated/runtime mirrors.

### Bump triggers

- No bump: docs-only edits, README refreshes, path cleanup, generated mirror resync, or manifest drift fixes that do not change shipped behavior or schema.
- Patch: backward-compatible fix to plugin behavior, packaging, runtime compatibility, or manifest data that changes what users receive.
- Minor: backward-compatible capability addition, new component bundle, additive manifest field, or new supported runtime/channel within the same product.
- Major: breaking rename or removal, incompatible schema/packaging change, or behavior change that requires user migration.

## Completion Checks

- For new plugins, the plugin directory exists in the correct runtime folder.
- For maintenance tasks, all touched manifests stay in the correct runtime folder and use only supported fields.
- `plugin.json` contains a valid name and description after the change.
- Component paths are relative to the plugin directory.
- No CLI-only field is copied into a VS Code manifest without runtime confirmation.
- Any created starter files match the manifest paths.
- Canonical version sources, runtime manifests, and generated mirrors are aligned or intentionally different with a clear reason.
- No separate per-runtime version stream is introduced without an explicit justification.
- If a new plugin or missing plugin README was part of the request, `README.md` exists and is minimal/pragmatic.
- Any paths in `README.md` are relative to the published plugin root (for example `./agents/...`, `./skills/...`), never workspace-absolute.

## README Rules

When creating or replacing `README.md`, keep it short and practical:

- Purpose: 1-2 sentences
- Included components: bullet list with plugin-relative paths
- Usage: minimal install/enable commands relevant to runtime
- Validation: one quick check command or action

Avoid long design explanations, architecture history, or workspace-only path examples.

## Non-Goals

- Do not implement business logic for bundled artifacts unless explicitly requested.
- Do not invent marketplace metadata, publish pipelines, or custom schema fields not requested by the user.
- Do not copy large documentation blocks into `plugin.json` comments or extra markdown files.

## Response Pattern

When you finish:

- State whether you created a new plugin, updated an existing plugin, or both
- State which runtime target was affected
- State whether the plugin reuses existing artifacts or includes placeholders
- State which components were inferred automatically vs explicitly provided by the user
- State the canonical version source and bump decision, or explain why no bump was needed
- Note any runtime-specific differences you had to account for
- Give the next concrete validation command or VS Code setting to use
