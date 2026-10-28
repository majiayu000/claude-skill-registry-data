---
name: engineer-plugin-marketplace
description: >-
  Design AI-IDE plugin marketplaces - requirements, host-specific payloads,
  local dogfood, release sync, and validation. Use when the user wants to create
  or publish a plugin marketplace.
---

# Plugin Marketplace Engineer

Use this skill when the user asks to create, assess, or plan a plugin
marketplace for AI IDE plugins. Focus on marketplace-level distribution:
catalog roots, per-host payloads, release sync, install flows, local dogfood,
cache refresh, trust, and validation.

For a single plugin package, prefer `engineer-ai-ide-plugin`. For one MCP server
or hook adapter, prefer the focused skills listed in
`references/related-skills.md`.

## Evidence First

Before giving implementation details, verify the current official docs for each
target host. Record the consulted links and separate:

- Verified host contract: manifest paths, component fields, marketplace shape,
  install commands, trust prompts, and validation commands.
- Local inference: patterns copied from nearby repos such as flowai,
  flowai-workflow, or FoxCode.
- Unknowns: host features that must be checked before writing files.

Use these official anchors first:

- Claude Code plugins: https://code.claude.com/docs/en/plugins
- Claude Code marketplaces: https://code.claude.com/docs/en/plugin-marketplaces
- Codex plugins: https://developers.openai.com/codex/plugins
- Codex build guide: https://developers.openai.com/codex/plugins/build
- OpenCode plugins: https://opencode.ai/docs/plugins/
- Cursor MCP: https://cursor.com/docs/mcp
- Agent Skills: https://agentskills.io/

## Workflow

1. Classify scope.
   - Marketplace design only -> produce requirements and risks; do not create files.
   - Marketplace implementation -> design first, then create source, build, validate,
     install-smoke, and docs.
   - Existing marketplace audit -> inspect manifests, payload roots, install docs,
     sync scripts, cache behavior, and validation evidence.
2. Define the marketplace contract.
   - Technical marketplace name, display name, owner, repository, license, version
     source, target hosts, supported install scopes, and trust model.
   - Plugin inventory: plugin IDs, descriptions, categories, tags, capabilities,
     auth policy, and source paths.
   - Payload inventory: skills, commands, agents, MCP servers, hooks, apps, assets,
     scripts, binaries, and runtime dependencies.
3. Split shared source from host outputs.
   - Shared source: skill bodies, MCP code, assets, schemas, scripts, docs.
   - Host output: marketplace root, plugin manifest, component paths, hook format,
     MCP config, app config, install commands, cache paths, trust prompts.
   - Do not claim one universal marketplace format unless current docs prove it.
4. Specify packaging transforms.
   - Deterministic file enumeration and sorted output.
   - Version injection from one source.
   - Asset copy near the consuming component.
   - Namespace rewrite for slash commands where the host requires plugin namespaces.
   - Host-specific path rewrite instead of leaking one host's root variables into
     another host.
5. Specify local dogfood.
   - Use a distinct local marketplace name such as `<name>-local`.
   - Preserve disabled plugin state across reinstall.
   - Keep official and local marketplace installs side by side.
   - For Codex, run marketplace registration and plugin add/materialization.
6. Specify validation gates before publishing.
   - Schema/path validation for every marketplace and plugin manifest.
   - Rebuild from source and fail on stale generated files.
   - Byte-deterministic rebuild check.
   - Install smoke in isolated host homes or config dirs.
   - MCP handshake smoke: `initialize` and `tools/list` from installed payload.
   - Hook smoke: parse and execute declared command hooks with synthetic host env;
     mark real trust/enablement as user-reviewed when required by the host.
   - Cache refresh check for same-version local rebuilds.

## Required Output

For design or requirements work, include:

- Official docs consulted.
- Requirements.
- Constraints.
- Anti-patterns.
- Canonical source layout.
- Host-specific output layout.
- Runtime, data, cache, and trust contracts.
- Local dogfood flow.
- Release sync plan.
- Validation gates.
- Risks and open questions.
- Related skills with links; read `references/related-skills.md` when the user
  asks for skill links or when routing adjacent work.

For implementation work, create files in this order:

1. Shared source and schemas.
2. Host-specific marketplace and plugin manifests.
3. Build/sync scripts.
4. Validation and install-smoke tests.
5. User documentation.

## Rules

- Keep generated marketplace payloads out of source control unless the downstream
  repo is intentionally generated.
- Never edit generated `dist/` payloads by hand.
- Never publish from an unvalidated local tree.
- Never overwrite user-disabled plugin state during local reinstall.
- Never require manual config edits when the host supports native plugin wiring;
  if a manual edit is unavoidable, label it as a host limitation.
- Never treat hook trust prompts as implementation noise; they are product
  behavior.
- Never package Codex agents/subagents unless current Codex plugin docs define
  that component. Represent worker behavior as skills when in doubt.
