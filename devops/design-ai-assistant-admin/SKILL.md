---
type: Skill
name: design-ai-assistant-admin
description: Manage AI assistant configurations and peer-to-peer mesh network connections in the NV oOS Pro Toolkit. Covers assistant creation, model configuration, provider setup, peer discovery, mesh networking, and cross-assistant communication. Use when creating or editing AI assistants, configuring model providers, setting up peer connections, managing mesh network topology, or debugging assistant behavior.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# NV oOS AI Assistant Administration

> **Accuracy note (2026-09-15):** this skill was rewritten after a live
> verification pass against plugin v1.1.79 (`includes/assistants/`,
> `includes/cli/`, `includes/rest/`) and the Design Stack deployment. Every
> meta key, command, and route below is code-verified. The previous version
> of this skill documented `_assistant_*` / `_peer_*` meta keys that the
> plugin has never stored — do not use them.

## When to use this skill

Trigger when ANY of the following is true:

- Creating, editing, or deleting AI assistant configurations.
- Changing an assistant's model provider (OpenAI, Gemini, Anthropic, Ollama, etc.).
- Configuring an assistant's system prompt, temperature, or tool access.
- Setting up or removing peer-to-peer federation records between WordPress sites.
- Listing all assistants with their current model, provider, and status.
- Querying which tools are enabled for a specific assistant.
- Debugging assistant behavior — checking configuration, tool access, or peer routing.
- Managing assistant-specific vector store or memory settings.
- Cloning an assistant configuration for testing or staging environments.

## Mental model

Two CPT-backed entity types, plus a small set of verified interfaces:

```
AI ASSISTANT  (CPT: mcp_ai_assistant)         AI PEER  (CPT: ai_peer)
├── title / post_status                        ├── title
├── _wp_mcp_ai_provider                        ├── _wp_mcp_ai_peer_mcp_url
├── _wp_mcp_ai_model                           ├── _wp_mcp_ai_peer_capabilities
├── _wp_mcp_ai_system_prompt                   ├── _wp_mcp_ai_peer_health_status
├── _wp_mcp_ai_tools (serialized slug array)   ├── _wp_mcp_ai_peer_last_verified
├── _wp_mcp_ai_credentials (hashed tokens)     ├── _wp_mcp_ai_peer_site_url
└── mcp_ai_required_capability                 └── … (see peer meta table)

INTERFACES (in order of reliability):
1. WP-CLI   wp mcp-ai assistant|credential|tool|provider|chat|health|log …
2. REST     https://<site>/wp-json/mcp-ai/v1/chat  +  /mcp (JSON-RPC)  +  /tools
3. Admin UI assistant CPT editor + federation pages
4. toolkit_cpt MCP tool — Pro-only, not guaranteed to be exposed
```

**Relationships:**

- An **AI Assistant** (`mcp_ai_assistant`) is one row per assistant persona.
  Model, provider, prompt, temperature, and the assigned tool-slug array all
  live in `_wp_mcp_ai_*` post meta (plus `mcp_ai_required_capability`).
- An **AI Peer** (`ai_peer`) is a federation-directory record pointing at a
  remote MCP server: MCP/OpenAPI URLs, JWKS URI, capabilities, quotas, and a
  health status that is refreshed by verification runs. Peers only render in
  the admin federation page when `enable_federation_directory` is on.
- **`toolkit_cpt`** (`WP_MCP_AI_Pro_Tool_CPT`,
  `addons/pro/includes/tools/infrastructure/class-wp-mcp-ai-pro-tool-cpt.php`)
  is the generic CPT CRUD MCP tool (group `wordpress-core`, `pro` capability
  flag). It is NOT the single interface: it may be absent from a given
  deployment's `tools/list`. Always verify it exists before scripting against
  it; WP-CLI and the REST routes are the always-available paths.

## WP-CLI command surface (verified against includes/cli/)

| Command | Purpose |
|---|---|
| `wp mcp-ai assistant list [--status=any\|publish\|draft\|trash] [--format]` | List assistants (title, status, legacy model column — see quirk below) |
| `wp mcp-ai assistant get <id> [--format=json]` | Post-level details; only shows `mcp_ai_*`-prefixed meta (quirk below) |
| `wp mcp-ai assistant create --title=<t> [--status=publish] [--model] [--system-prompt] [--porcelain]` | Create assistant; `--porcelain` prints the new ID |
| `wp mcp-ai assistant update <id> [--title] [--status] [--model] [--system-prompt]` | Update assistant |
| `wp mcp-ai assistant delete <id> [--force] [--yes]` | Trash or permanently delete |
| `wp mcp-ai assistant export <id> [--file=<name.json>]` | Export config JSON (stdout or uploads/mcp-ai/exports/) |
| `wp mcp-ai assistant import [--file=<name.json> \| --stdin] [--porcelain]` | Import from exports dir or stdin |
| `wp mcp-ai credential list [<assistant-id>] [--format]` | List issued credentials |
| `wp mcp-ai credential issue <assistant-id> [--user=<id>] [--porcelain]` | Issue token; `--porcelain` prints `cred_xxxxx.SECRET` once |
| `wp mcp-ai credential revoke <assistant-id> <credential-id> [--yes]` | Revoke a token |
| `wp mcp-ai tool list [--status=enabled\|disabled] [--format=ids]` | **Discover assignable tool slugs** (registry + enabled state) |
| `wp mcp-ai tool enable <slug>` / `wp mcp-ai tool disable <slug> [--yes]` | Toggle global tool availability |
| `wp mcp-ai provider list` / `provider test <slug>` / `provider models <slug>` | Provider config status, connectivity test, model list |
| `wp mcp-ai chat "<message>" [--assistant=<id>] [--model] [--provider] [--stream] [--format=json]` | One-shot chat via the model router |
| `wp mcp-ai health` / `wp mcp-ai log` / `wp mcp-ai cache clear` / `wp mcp-ai version` | Diagnostics |
| `wp mcp-ai toolkit list \| enable <key> \| disable <key>` (Pro) | Pro toolkit settings keys (`enable_crm_toolkit`, …) — **not** assistant CRUD |

There is **no** `wp mcp-ai peer` command — peer records are edited via post
meta or the admin UI. (Older versions of this skill claimed `peer list` /
`peer test`; those commands do not exist in v1.1.79.)

### CLI quirks you will hit (code-verified)

- `assistant create|update --model=…` and `--system-prompt=…` write legacy
  `mcp_ai_model` / `mcp_ai_system_prompt` meta keys. The chat runtime reads
  `_wp_mcp_ai_model` / `_wp_mcp_ai_system_prompt`, so those flags currently
  have **no runtime effect** — set the `_wp_mcp_ai_*` keys explicitly.
- `assistant list` reads `mcp_ai_model` (usually empty) and `assistant get`
  only collects meta keys starting with `mcp_ai_`, which misses every
  `_wp_mcp_ai_*` key. Inspect real config with `wp post meta get` instead.
- `wp mcp-ai provider list` and `wp mcp-ai chat` fatal on builds before the
  CLI fix in #6625 (see Known Issues).

## Verified meta keys

### `mcp_ai_assistant`

Constants in `includes/assistants/class-wp-mcp-ai-assistant-cpt.php`:

| Key | Type | Purpose |
|---|---|---|
| `_wp_mcp_ai_provider` | string | Provider slug (`openai`, `gemini`, `anthropic`, `deepseek`, `ollama`, …) |
| `_wp_mcp_ai_model` | string | Model identifier (`gpt-4o-mini`, `gemini-2.5-flash`, …) |
| `_wp_mcp_ai_temperature` | float | Sampling temperature |
| `_wp_mcp_ai_system_prompt` | string | Persona / system prompt |
| `_wp_mcp_ai_tools` | array (serialized) | Assigned tool slugs — must be a real PHP array |
| `_wp_mcp_ai_credentials` | array | Issued credentials (hashed). Never hand-edit |
| `_wp_mcp_ai_classification` | string | Information label; defaults to `internal` |
| `mcp_ai_required_capability` | string | Capability gate for tool calls — **no `_wp_` prefix** (`manage_options`, `edit_posts`) |
| `_wp_mcp_ai_vector_store_id` | string | OpenAI vector store for RAG |
| `_wp_mcp_ai_memory_files` | array | Memory file attachment IDs |
| `_wp_mcp_ai_corpus_name` | string | Corpus name for knowledge routing |
| `_wp_mcp_ai_tool_shortcuts` | array | Tool shortcut definitions |
| `_wp_mcp_ai_harness_profile` | array (JSON) | Agent-harness profile (memory summary etc.) |

### `ai_peer`

Constants in `includes/class-wp-mcp-ai-ai-peer-cpt.php`:

| Key | Type | Purpose |
|---|---|---|
| `_wp_mcp_ai_peer_mcp_url` | string | Remote MCP endpoint URL |
| `_wp_mcp_ai_peer_openapi_url` | string | Remote OpenAPI spec URL |
| `_wp_mcp_ai_peer_jwks_uri` | string | JWKS URI for token verification |
| `_wp_mcp_ai_peer_capabilities` | mixed | Advertised capabilities |
| `_wp_mcp_ai_peer_regions` | mixed | Serving regions |
| `_wp_mcp_ai_peer_data_tags` / `_wp_mcp_ai_peer_policy_tags` | mixed | Data / policy tags |
| `_wp_mcp_ai_peer_quotas` / `_wp_mcp_ai_peer_price_hints` | mixed | Quota and pricing metadata |
| `_wp_mcp_ai_peer_health_status` | string | Health state (`healthy`, …) |
| `_wp_mcp_ai_peer_latency_p50` | mixed | p50 latency |
| `_wp_mcp_ai_peer_last_verified` | string | Last verification timestamp |
| `_wp_mcp_ai_peer_last_error` | string | Last verification error |
| `_wp_mcp_ai_peer_site_name` / `_wp_mcp_ai_peer_site_url` | string | Remote site identity |
| `_wp_mcp_ai_peer_wellknown_url` | string | `/.well-known/` discovery URL |
| `_wp_mcp_ai_peer_verification_data` | mixed | Verification payload |

## Verified provisioning recipe (Design Stack)

This is the end-to-end path that actually works on the Design Stack deployment:

```bash
# 0. In the Design Stack WP container, wp requires --allow-root.
#    (In this repo's own compose: docker compose run --rm wp-cli …)

# 1. Discover assignable slugs before assigning.
wp mcp-ai tool list                  # base registry: slug + enabled + capability
wp mcp-ai toolkit list               # Pro toolkit settings keys

# 2. Create the record.
wp mcp-ai assistant create --title="Brand Assistant" --status=publish --porcelain
# → prints the new assistant ID (call it <id>)

# 3. Set runtime meta. The CLI's --model/--system-prompt write legacy keys the
#    runtime ignores — set the _wp_mcp_ai_* keys explicitly:
wp post meta update <id> _wp_mcp_ai_provider openai
wp post meta update <id> _wp_mcp_ai_model gpt-4o-mini
wp post meta update <id> _wp_mcp_ai_temperature 0.7
wp post meta update <id> _wp_mcp_ai_system_prompt "$(cat assistant-system-prompt.md)"
wp post meta update <id> _wp_mcp_ai_classification internal
wp post meta update <id> mcp_ai_required_capability manage_options

# Tools is a serialized PHP array. wp post meta update would store a string,
# which breaks tool resolution — use wp eval for that one key:
wp eval 'update_post_meta(<id>, "_wp_mcp_ai_tools", array("web_search", "deep_research", "create_post"));'

# 4. Issue the credential (prints cred_xxxxx.SECRET exactly once).
wp mcp-ai credential issue <id> --porcelain
```

## Verification checklist (what actually works)

1. **MCP JSON-RPC handshake** — `POST /wp-json/mcp-ai/v1/mcp` with
   `Authorization: Bearer <TOKEN>`:

   ```json
   {"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"zed","version":"1"}},"id":1}
   ```

   Then `tools/list` — expect exactly the slugs you assigned (empty list ⇒
   `_wp_mcp_ai_tools` was never set as an array).

2. **REST chat smoke test** (the reliable fallback when `wp mcp-ai chat` fatals):

   ```bash
   curl -s -X POST http://localhost:8092/wp-json/mcp-ai/v1/chat \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"assistant_id": <id>, "messages": [{"role":"user","content":"Reply with exactly: OK"}]}'
   ```

   `messages` is required; `assistant_id` is optional (int or string);
   optional `options` object accepts `provider`, `model`, `temperature`,
   `stream`, `response_format`.

3. **Inspect persisted config** — `wp post meta get <id> _wp_mcp_ai_provider`
   etc. Do not trust `wp mcp-ai assistant get` for meta (legacy-key caveat).

## Known issues (observed on Design Stack, 2026-09)

- **`wp mcp-ai provider list` and `wp mcp-ai chat` fatal** (PHP 8) on builds
  before the CLI fix: `format_output()` passed an inline array literal to
  `WP_CLI\Formatter`'s by-reference constructor, and `chat` constructed the
  model router with zero args. Fixed in #6625 (merged to alpha-working;
  ships after v1.1.79). Workarounds on older builds: provider config status
  → NV oOS settings page; provider connectivity →
  `wp mcp-ai provider test <slug>`; chat → the REST smoke test above.
- **`assistant create|update --model/--system-prompt`** write legacy keys the
  runtime does not read (see CLI quirks). Always set `_wp_mcp_ai_*` explicitly.
- **`--allow-root`** is required for `wp` inside the Design Stack WP container.
- **`toolkit_cpt` may be missing** from `tools/list` on a given deployment
  (Pro tool with a `pro` capability flag). Check availability before
  scripting against it; WP-CLI + REST are the fallback.

## Critical Rules

- `_wp_mcp_ai_tools` must be a **real PHP array** (serialized). Set it with
  `wp eval` / `update_post_meta()`, never `wp post meta update` (string).
- `mcp_ai_required_capability` has **no `_wp_` prefix** — unlike every other
  assistant key. Getting this wrong silently falls back to default gates.
- Credential tokens print **once** (`credential issue --porcelain`); never log
  them or commit them. Hashes live in `_wp_mcp_ai_credentials` — never edit.
- Provider/model slugs must match `wp mcp-ai provider list` and the model
  catalog; a mismatched pair fails at runtime, not at assignment time.
- Peer records are only meaningful when `enable_federation_directory` is on;
  health is maintained by verification runs, not by editing the post.
- Verify with the checklist above after every change — `assistant get` does
  not show you the runtime configuration.

## Common Mistakes

```
WRONG — assigning tools via wp post meta update
wp post meta update 42 _wp_mcp_ai_tools '["web_search", "deep_research"]'
// Stores a STRING. is_array() checks in tool resolution fail → tools/list [].
RIGHT — wp eval 'update_post_meta(42, "_wp_mcp_ai_tools", array("web_search", "deep_research"));'

WRONG — relying on assistant create --model to configure the runtime
wp mcp-ai assistant create --title="Bot" --model=gpt-4o
// Writes mcp_ai_model. The runtime reads _wp_mcp_ai_model → default model used.
RIGHT — create with --title/--status, then set _wp_mcp_ai_model via wp post meta update.

WRONG — trusting assistant get for configuration audits
wp mcp-ai assistant get 42
// Collects only mcp_ai_*-prefixed meta; misses _wp_mcp_ai_* keys entirely.
RIGHT — wp post meta get 42 _wp_mcp_ai_provider (one key at a time, or wp eval get_post_meta).

WRONG — exposing a credential in a Zed config file or chat log
// Tokens are bearer credentials; treat like API keys. Store via design-vault.
```

## Cross-References

- Run `mcp-ai-wpoos-plugin` for MCP bridge setup, JSON-RPC examples, and the
  WP-CLI provisioning recipe with the chat REST smoke test.
- Run `design-pro-workflow-builder` to create workflows that chain assistants.
- Run `design-pro-schedule-manager` to schedule recurring assistant health checks.
- Run `design-vault` to securely store credential tokens.
- Run `design-team-management` to assign assistants to teams or roles.
- Run `design-crm` if the assistant is used for CRM automation.
- Run `design-project-management` if the assistant manages projects or tasks.
- Run `wp-security-audit` on any assistant-facing endpoint — exposed
  assistants are attack surfaces.
- Run `wp-security-secrets` to audit credential handling.
- Run `design-elementor-mcp-connection` to connect Elementor MCP servers to
  an assistant via the MCP Apps metabox/slash-command (per-assistant remote
  MCP tool bridging) — this skill covers assistant config, not MCP app
  connections.

## What This Skill Does NOT Cover

- MCP bridge tool calling mechanics — use `mcp-ai-wpoos-plugin` for JSON-RPC.
- Chat UI configuration (shortcodes, Elementor widgets) — see the plugin's
  chat UI documentation.
- Provider API key management — NV oOS Settings page or `design-vault`.
- Vector store file upload and management — Files API tools.
- Agent memory system internals — `retrieve_agent_memory` / `store_agent_context`.
- Workflow builder orchestration — `design-pro-workflow-builder`.
- Peer wire protocol (SSE, message format) — this skill covers peer
  *configuration*, not the transport.
- Multi-site WordPress network administration — `remote_wp_connection`.
- MCP App connections to remote MCP servers (e.g. Elementor MCP) —
  `design-elementor-mcp-connection`.

## References

- Assistant CPT + meta constants: `includes/assistants/class-wp-mcp-ai-assistant-cpt.php`
- Peer CPT + meta constants: `includes/class-wp-mcp-ai-ai-peer-cpt.php`
- CLI commands: `includes/cli/class-wp-mcp-ai-cli-assistant-command.php`,
  `…-credential-command.php`, `…-tool-command.php`, `…-provider-command.php`,
  `…-chat-command.php`, `addons/pro/includes/cli/class-wp-mcp-ai-pro-cli-toolkit-command.php`
- `toolkit_cpt` MCP tool: `addons/pro/includes/tools/infrastructure/class-wp-mcp-ai-pro-tool-cpt.php`
- REST chat endpoint: `includes/rest/class-wp-mcp-ai-rest-chat-controller.php`
- REST namespace (`mcp-ai/v1`): `includes/class-wp-mcp-ai-rest.php`
- Credential store: `includes/class-wp-mcp-ai-credentials.php`
