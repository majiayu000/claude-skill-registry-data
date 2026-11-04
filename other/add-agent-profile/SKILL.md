---
name: add-agent-profile
description: >-
  Add or change a Greenhouse Agent profile. First decide whether a system preset is needed at all:
  most requests are a custom Agent (run_profiles row), a profile pack, a plugin's agent context or a
  sprouty.yaml edit. When a preset really is needed: YAML in apps/api/src/profiles, profile.ts
  constants, agent-profiles.md, the guard test and the client's hard-coded ids move together. Use for:
  add an agent / new profile / new assistant / change the system prompt, 加个 agent, 新增 profile,
  做个新助手, 改系统提示词. Red lines: access is only level + rich_output, no options or extends in
  YAML, built-in YAML uses tools: [], prompts never restate dynamic tool rules.
---

# Add or change an Agent profile

Source of truth: apps/api/src/profiles/AGENTS.md (inventory and rules) and apps/api/src/profiles/agent-profiles.md (architecture, tool matrix, i18n, rich output). On conflict those win.

## Step 0: you probably do not need a preset
- The directory holds two YAMLs on purpose: `sprouty.yaml` (the only preset, DEFAULT_PROFILE_ID, /api/chat) and `desktop.yaml` (hidden runtime profile for /api/agent and /api/mcp; never listed, renaming it needs a data migration).
- Different model: the model is chosen per turn beside the composer (`POST /api/chat` `model`, checked by isChatModelAllowed()); never a new profile.
- Different prompt or narrower tools for some people: a custom Agent (below), the normal path.
- A deployment's own set: a profile pack, `packs.profiles` in greenhouse.config.ts (a later directory wins for the same id).
- Plugin behavior the model should know: the plugin's agentContext or promptContext, never a profile.
- Better wording for everyone: edit sprouty.yaml; there is no second copy.
- External agents (MCP clients, CLIs) use /api/agent or /api/mcp, never a dedicated profile.

## Custom Agents
- One current-configuration row in run_profiles; `version` counts edits; references are `custom:<id>@<version>` and any pin ≤ version resolves to the current configuration.
- Sessions and automations pin on creation (pinProfileIdForUser(), profiles/access.ts); execution rechecks owner, super or team sharing.
- `base_profile_id` must be a preset (isValidCustomBaseProfileId()); the base supplies only `access.rich_output` and the model fallback.
- Private by default; only a super shares it with the team (`PUT /api/profiles/custom/:id/sharing`); tools only narrow the member's own.
- API: /api/profiles/custom (apps/api/src/routes/profiles.ts); UI: the custom agents section of the client's Automations place (apps/client/src/automations/agents.ts, agent-editor.web.tsx).
- resolveProfileAsync() throws for a missing custom Agent or version; it never falls back to Sprouty.

## Step 1: the YAML (only for a real preset)
```yaml
id: xxx
name: Xxx
version: 'YYYY-MM-DD'
description:            # plain string or { zh, en } (source locale zh)
  en: …
  zh: …
access:
  level: internal       # internal | hidden
  rich_output: true
model:
  id: flash             # default for headless paths only; options live in config/models.yaml
tools: []               # built-ins derive tools from the member and active plugins
system_prompt: |
  …
```
- `access` holds only `level` and `rich_output`; session requirements belong to each runtime or route.
- No `options`: temperature, thinking, max_tokens belong to config/models.yaml (resolveModelConfig()).
- No `extends`; reuse prompt text by editing sprouty.yaml.
- The rich-output block guide exists once, RICH_OUTPUT_GUIDE (packages/utils/src/prompts.ts), appended by enrichSystemPrompt(); never restate it.
- Prompts never restate rules of dynamically assembled tools; name only `is_global: true` tools or tools the profile declares.
- `name` and `description` with an unknown locale key or an empty string fail loading; `system_prompt` is never localized.
- The system prompt holds only session-stable content (prompt caching); per-turn content goes elsewhere.

## Step 2: move these together
- `apps/api/src/profiles/<id>.yaml` (loadAllProfiles() scans the directory).
- `apps/api/src/profiles/profile.ts`: PRESET_PROFILE_IDS (array order is picker order), DEFAULT_PROFILE_ID, CUSTOM_BASE_PROFILE_IDS.
- A YAML without its constant is an Agent nobody can pick; a constant without its YAML fails at boot with `Profile not found`.
- `apps/api/src/profiles/agent-profiles.md`: architecture and tool matrix.
- `tests/api/agent-profiles.test.ts`: YAML count and names, legacy mapping, valid custom bases, single rich-output copy, no extends, keyless models out of the picker.
- The universal client hard-codes `sprouty`: new-Agent base (apps/client/src/automations/agents.ts), automation default (apps/client/src/automations/editor.web.tsx), Sprouty ids (apps/client/src/data/home.ts).

## Step 3: tools and models
- Built-in profiles derive tools at runtime (resolveEffectiveTools narrows; resolveUserTools is the member's allow-set); never pin optional plugin tool ids in YAML.
- A custom Agent's `tools` only narrows; `meta.builtin` tools join its filter without widening permissions.
- `GET /api/profiles` returns `models: listChatModels()`, which omits models without a reachable provider; an unreachable custom `model_id` falls back to the base preset's model.

## Step 4: legacy ids map, never migrate
- normalizeProfileId() maps retired preset, team and eval ids to `sprouty` and `local-dev` / `local-pi` to `desktop`; stored values stay as they are; never recreate YAML for them.

## Gate
```bash
pnpm typecheck
pnpm lint
TEST_DATABASE_URL=<loopback test db> pnpm test
(cd apps/client && pnpm typecheck)   # when client hard-coded ids changed
```
- Check by hand: resolveProfileAsync() resolves the profile; a non-hidden preset appears in the client's Agent pickers.

## Checklist
- [ ] Custom Agent, pack, plugin context or a sprouty.yaml edit ruled out; reason for a new preset recorded in profiles/AGENTS.md
- [ ] access only level + rich_output; no options, no extends, no second rich-output guide
- [ ] No restated dynamic tool rules or false capability claims in the prompt
- [ ] YAML, profile.ts, agent-profiles.md, agent-profiles.test.ts and client ids moved together
- [ ] Gate green
