---
name: engineer-ai-ide-plugin
description: >-
  Design and build complete AI-IDE plugins bundling skills, MCP tools and hooks
  with packaging, manifests, marketplaces and per-IDE validation. Use when the
  user wants to create, design or package a multi-component plugin. Not for a
  standalone skill.
---

# AI IDE Plugin Engineer

Use this skill when the user asks for an installable plugin for one or more AI
IDEs, or asks to package a plugin with manifests, marketplace metadata, assets,
skills, apps, MCP servers, hooks, agents, or validation.

For a single element, prefer the focused skill:

- MCP tool/server only -> `engineer-plugin-mcp`
- Plugin hook adapters only -> `engineer-plugin-hooks`
- Plain skill/command/agent authoring without plugin packaging -> devtools authoring skills

Packaging belongs in this skill. Do not delegate manifest, marketplace, asset,
root/data discovery, or install-layout work to a separate packaging skill.

## Official Docs First

Do not treat this skill as a full specification. Before implementation, open the
current official docs for each requested IDE and cite or link the pages used in
the output.

Fetch only the sections needed for the current task. Do not request entire docs
pages unless the user explicitly asks for exhaustive reference material. Do not
spawn subagents just to fetch docs; open the smallest relevant official page(s)
directly, summarize the verified facts, then produce the requested design or
implementation.

- Claude Code plugins: https://code.claude.com/docs/en/plugins
- Claude Code plugin reference: https://code.claude.com/docs/en/plugins-reference
- Codex plugin overview: https://developers.openai.com/codex/plugins
- Codex plugin build guide: https://developers.openai.com/codex/plugins/build
- Cursor MCP: https://cursor.com/docs/mcp
- Cursor extension API: https://cursor.com/docs/extension-api
- Cursor hooks: https://cursor.com/docs/hooks
- OpenCode plugins: https://opencode.ai/docs/plugins/
- Agent Skills standard: https://agentskills.io/

If the target IDE is not listed, find its official plugin, extension, MCP, hook,
or marketplace docs first. If no official docs exist, say that explicitly and
separate verified facts from assumptions.

For Claude Code + Codex plugin tasks, start with only:

- https://code.claude.com/docs/en/plugins
- https://developers.openai.com/codex/plugins/build

Open reference pages only if the task requires exact fields not present in those
two pages.

## Workflow

1. Classify the request.
   - Design, plan, evaluate, or "help me design" -> output a design only; do
     not create files.
   - Create, implement, scaffold, write files, or modify this repo -> implement
     after the design is clear.
   - A concrete plugin name or feature list does not make a request an
     implementation request. The verbs decide.
   - For design-only requests, finish with the design response. Do not create
     directories, manifests, sample servers, hook files, or marketplace files.
2. Define the plugin contract.
   - Name, purpose, target IDEs, scope, trust model.
   - Elements: skills, commands, apps, agents, MCP servers, hooks, assets, scripts.
   - External effects: filesystem writes, network calls, browser control, credentials.
3. Read official docs for each target IDE.
   - Confirm plugin entrypoints, manifest fields, supported surfaces, install
     scopes, validation commands, and trust prompts.
   - Record doc links in the design or implementation notes.
4. Split shared vs IDE-specific code.
   - Shared: skill bodies, policy logic, MCP implementation, schemas, assets.
   - IDE-specific: manifests, app wiring, marketplace files, hook wrappers,
     MCP wiring, agent formats, local install commands, trust or approval flows.
   - Never reuse one IDE's hook or MCP config as another IDE's contract unless
     the current official docs explicitly say the formats are compatible.
   - When a requested worker, agent, or subagent must ship inside a Codex plugin,
     model that behavior as one or more bundled skills under `skills/<name>/SKILL.md`.
     Do not design Codex plugin `agents/` or `subagents/` components unless current
     official Codex plugin docs explicitly add that surface. If standalone Codex
     custom agents are relevant, describe them as separate `.codex/agents/*.toml`
     configuration outside plugin packaging.
5. Choose behavior surfaces.
   - Prefer MCP for tool-like integrations when each target IDE supports it.
   - Use hooks or native plugin events for lifecycle policy, blocking, audit,
     and context injection.
   - Use skills or rules for reusable instructions and user workflows.
6. Design packaging in the main plan.
   - Keep one canonical source tree and emit IDE-specific install files.
   - Generate native manifests per IDE instead of forcing one manifest to fit all.
   - For Codex, two manifest formats coexist; name the one you pick and why.
     In both, plugin apps are wired through an `.app.json` file referenced by an
     `apps` field — name that file and that field in the layout and the plan.
     - Portable: root `plugin.json`, Codex settings under
       `extensions.com.openai`, so `extensions.com.openai.apps` references
       `./.app.json`; bundled MCP servers live in a root `mcp.json` (no dot).
     - Legacy compatibility fallback: `.codex-plugin/plugin.json`, whose `apps`
       references `.app.json` and whose `mcpServers` references `.mcp.json`.
   - Include marketplace files only for IDEs that support them.
   - Keep manifest paths relative to the plugin root where the host requires it.
   - Put assets near the consuming manifest, skill, wrapper, or app config.
7. Design runtime paths.
   - Prefer host-provided plugin root/data variables when documented.
   - Use compatibility aliases only when the official docs confirm them.
   - Fall back to deterministic script-location discovery for local-only builds.
8. Define validation before writing implementation files.
   - Validate manifests with host validators when available.
   - Validate MCP with non-interactive probes where supported.
   - Validate hooks or native plugin events in an interactive or trusted session
     when the host requires trust review.
   - Include install, enable, reload, and smoke-test commands for each target IDE
     when official docs provide them.

## Required Output

For design-only requests, produce:

- Official docs consulted.
- Current-doc verification statement for manifest, hook, MCP, packaging, and validation details.
- Plugin element inventory.
- Canonical file layout.
- IDE-specific packaging and install plan.
- MCP, app, hook, skill, agent, asset, and data contracts as applicable.
- Validation matrix by IDE.
- Risks and open questions.

Keep design output concise. If a doc page is slow or unavailable, cite the
intended official URL, mark the exact fields as "verify before implementation",
and continue with a conservative design instead of starting implementation.

For implementation requests, create files in this order:

1. Shared implementation and schemas.
2. Skills, agents, assets, and docs.
3. IDE-specific wrappers, manifests, marketplace files, and install config.
4. Validation fixtures or smoke-test scripts.
5. Project documentation updates.

## Rules

- Do not call the result universal unless the user asks for a specific universal format and the official docs support it.
- Do not hard-code one IDE as the runtime unless the user limits the target.
- Do not rely on one IDE's plugin root variables for another IDE.
- Do not duplicate policy logic per IDE. Wrap shared logic with thin adapters.
- Keep MCP tool names and schemas stable; IDE event names may differ.
- Treat trust prompts, approvals, and enablement as product behavior.
- Keep exact manifest fields, marketplace schemas, and event payloads in the implementation notes with links to official docs, not copied wholesale into this skill.

## Host Anchors To Verify

Use these only as starting points; always verify against official docs before
writing files.

- Claude Code: plugins use `.claude-plugin/plugin.json`; components can include
  skills, agents, hooks, MCP servers, LSP servers, monitors, settings, and assets.
- Codex: plugins use a root `plugin.json` with `extensions.com.openai`, or the
  legacy `.codex-plugin/plugin.json` fallback; bundled surfaces can include
  skills, apps, MCP servers, hooks, assets, and marketplace metadata.
- Cursor: MCP is the main documented extension surface for external tools; project
  and global `mcp.json` plus extension API may apply.
- OpenCode: plugins are JavaScript or TypeScript modules loaded locally or from
  npm; hooks and custom tools are programmatic.
