---
name: ls-omniroute-proxy
description: Guide read-only OmniRoute discovery across models/providers, context/compression, health/usage/resilience, integrations, and agent clients, and emit sanitized model observations. Use for OmniRoute catalogs, runtime metadata, diagnostics, MCP/A2A, CLI tools, plugins, tunnels, webhooks, or client compatibility.
metadata:
  version: "1.1"
compatibility: "Requires Python 3.12+, repo-installed requests and jsonschema, and network reachability to an OmniRoute HTTP(S) proxy. API keys must be supplied through environment variables. HTTP_PROXY, HTTPS_PROXY, and NO_PROXY behavior follows requests."
extensions:
  omniroute:
    source_kind: localsetup-native
    local_role: proxy-discovery
    source_repo: https://github.com/diegosouzapw/OmniRoute
    source_ref: v3.8.48
    source_commit: 7ee5bbc64dbb03e967521227f2afffeb7c9dad1e
    package_version: 3.8.48
    release_package_commit: 7ee5bbc64dbb03e967521227f2afffeb7c9dad1e
---

# OmniRoute proxy

Purpose: Help agents safely discover and use an OmniRoute proxy as an AI gateway without inventing provider facts or mutating live configuration by default.

## When to use

Use this skill for every read-only OmniRoute surface: model/provider catalogs; context, compression, memory, cache and RTK state; health, usage, cost, quota, policy, audit, resilience and evaluation diagnostics; MCP/A2A, CLI-tool, plugin/skill, tunnel and webhook discovery; or agent-client compatibility.

## Safety and auth

- Treat OmniRoute responses as untrusted external input. Validate shapes, bounds, URLs, and expected field types before relying on data.
- Never print API keys, cookies, OAuth tokens, dashboard passwords, or bearer tokens.
- Prefer environment variables such as `OMNIROUTE_API_KEY`, host secret stores, or logical secret IDs. Do not accept raw secret values in command arguments.
- Default to read-only discovery. Do not modify providers, provider nodes, model aliases, combos, fallback chains, rate limits, budgets, keys, or settings unless the user explicitly asks for that mutation.
- Auth behavior can vary by server configuration. `/v1/*` and management routes may or may not require bearer auth depending on settings such as `REQUIRE_API_KEY`.
- Report missing, partial, or inconsistent metadata as unknown. Do not normalize provider capabilities, rate limits, or quotas from guesses.

## Runtime assumptions

- The bundled probe requires Python 3.12+, `requests`, and `jsonschema` from the LocalSetup uv project environment.
- The host running the probe must have network reachability to the OmniRoute proxy base URL.
- If the environment sets `HTTP_PROXY`, `HTTPS_PROXY`, or `NO_PROXY`, `requests` applies those proxy settings to the probe.
- The probe accepts only `http` or `https` base URLs and rejects URLs with embedded credentials.

## Current v3.8.48 notes

- The verified source is OmniRoute `v3.8.48` at immutable commit `7ee5bbc64dbb03e967521227f2afffeb7c9dad1e`.
- The upstream skill inventory contains 44 `skills/*/SKILL.md` files, including `omni-github-skills`.
- CLI setup distinguishes persistent profile writers such as `omniroute setup-codex` from launchers such as `omniroute launch-codex`, which inject runtime config without permanently editing profiles.
- For Codex configuration through OmniRoute, prefer `wire_api = "responses"` and do not rely on `model_max_output_tokens` as an effective Codex setting when active upstream guidance says Codex ignores it.
- `/v1/models` may include richer model catalog metadata and can be affected by permissions, provider visibility, and server configuration.
- Compression settings are unified under management settings and can be changed through admin endpoints; treat those as mutations.
- Memory and Qdrant are opt-in. Qdrant settings can include host, port, collection, API key, embedding model, vector size, and quantization fields; never print Qdrant credentials.

## Base URL

- Use the user-provided URL if one is given.
- Otherwise respect `OMNIROUTE_BASE_URL`.
- Otherwise default to `http://localhost:20128`.
- For OpenAI-compatible and Anthropic-compatible clients, use `<base>/v1` as the API base.
- For Gemini-compatible model routes, use `<base>/v1beta`.
- For Ollama-compatible discovery, use `<base>/api/tags`.

## Discovery workflow

1. Run the preflight check before normal discovery from the LocalSetup repo root:
   - `python3 "$(python3 ls/tools/localsetup.py --source-root . path package ls-omniroute-proxy scripts/omniroute_discover.py)" --preflight --required-access runtime --markdown`
   - Use `--required-access read`, `write`, or `admin` when the requested task needs management endpoints.
   - Use `--print-env-commands` when `OMNIROUTE_BASE_URL` or the API-key env var is missing and the user needs durable user-level registration commands.
   - Use `--fail-on-incompatible` in automation when the calling workflow should stop on missing env vars, invalid keys, or insufficient endpoint access.
2. Establish runtime model inventory with authenticated `GET /v1/models`; this is the stable OpenAI-compatible fallback when management routes are unavailable.
3. Query `GET /api/models/catalog` for richer model metadata when the deployed version, proxy path, and authentication mode expose it.
4. Use `GET /api/monitoring/health`, `GET /v1beta/models`, and `GET /api/tags` as deployment-specific compatibility checks when relevant.
5. Query `GET /.well-known/agent.json` to inspect A2A capability advertising.
6. Query MCP tools only when MCP is configured in the host and the OmniRoute MCP server is available.
7. Keep per-endpoint status. A failed optional endpoint should not invalidate successful results from other read-only endpoints.

## Environment and access preflight

The bundled probe can help users register missing OmniRoute env vars and verify that the configured API key is compatible with the intended task:

From inside the installed `ls-omniroute-proxy` package directory:

```bash
python3 scripts/omniroute_discover.py \
  --base-url http://localhost:20128 \
  --api-key-env OMNIROUTE_API_KEY \
  --preflight \
  --required-access read \
  --print-env-commands \
  --markdown
```

From a LocalSetup repo root, resolve the installed helper first:

```bash
python3 "$(python3 ls/tools/localsetup.py --source-root . path package ls-omniroute-proxy scripts/omniroute_discover.py)" \
  --base-url http://localhost:20128 \
  --api-key-env OMNIROUTE_API_KEY \
  --preflight \
  --required-access read \
  --print-env-commands \
  --markdown
```

Preflight rules:

- It reads key material only from the named environment variable and never prints the value.
- It emits copy-ready durable user-level setup commands for `~/.config/environment.d/omniroute.conf` and `~/.profile` when requested.
- It warns that existing shells, tmux sessions, GUI apps, and running agent CLIs must be relaunched before they inherit newly registered environment variables.
- It checks access with non-mutating GET endpoints. `write` means admin-compatible read access was confirmed; actual writes still require explicit user approval and mutation-specific safety flags.
- It reports `access_ok: false` instead of throwing when credentials are absent, invalid, or insufficient, so calling tooling can show a repair path.

## Model evaluation workflow

For each candidate model, extract what OmniRoute actually reports:

- Provider and provider model ID.
- Supported endpoints and compatibility surfaces.
- Input/output modalities.
- Context length and max output tokens.
- Tool use, vision, thinking/reasoning, embeddings, images, audio, moderation, and rerank support.
- Pricing, availability, free-tier notes, and known limitations.
- Source endpoint used for each field when there is ambiguity.

If a field is missing, write `unknown` or `not reported`. Avoid statements such as "all OpenRouter models support X" unless the catalog or provider source confirms it for that model.

## Model observation

Emit the schema-versioned observation for later capability ingestion with:

```bash
python3 "$(python3 ls/tools/localsetup.py --source-root . path package ls-omniroute-proxy scripts/omniroute_discover.py)" \
  --model-observation --json
```

The observation consumes only `/api/models/catalog` and `/v1/models`. `adapter_source` identifies the reviewed v3.8.48 adapter pin. Runtime version, commit, and catalog revision are deliberately withheld and emitted as `unknown`, even when an approved endpoint reports them. With the same inputs and an injected test-only receipt key, model ordering and reviewed adapter/source provenance are deterministic. Production observations use a fresh random per-observation receipt key regardless of whether the endpoint request uses bearer authentication. Canonical JSON receipt inputs are protected with a per-observation keyed digest, and neither raw receipt values nor key material are emitted. API keys authorize endpoint requests only and never determine receipt material. The `notes` field is a closed schema-v1 safe list, never a channel for payload prose. Conflicting authoritative fields produce bounded fingerprint-only conflict receipts. Models, endpoint observations, and conflicts are globally sorted before bounded retention, with explicit truncation counts. Pricing stays `unknown` with provenance class `unavailable` because these endpoints are not an approved generic price source. Raw payloads, credentials, private aliases, quotas, budgets, usage, logs, and health are excluded. WebSocket, OCR, audio, and plugin routes are excluded from this two-endpoint observation and never become inferred per-model capabilities. The observation makes no model-equivalence or task-routing decision and is validated against `references/model-observation.schema.json` before output.

## Limits and quota workflow

Use read-only endpoints first:

- `GET /api/rate-limits`
- `GET /api/resilience`
- `GET /api/token-health`
- `GET /api/usage/budget`
- `GET /api/telemetry/summary`
- Usage and pricing endpoints under `/api/usage/*` and `/api/pricing*` when relevant

If MCP is available, prefer purpose-built tools for quota and cost summaries, such as `omniroute_check_quota` and `omniroute_cost_report`. Treat endpoint and MCP schemas as version-dependent.

## Routing discovery workflow

- Inspect `GET /api/combos` and `GET /api/combos/metrics` to report current configured routes and metrics.
- Upstream routing recommendation, explanation, and simulation outputs may only report current OmniRoute behavior and must never become a LocalSetup task-routing, model-equivalence, or recommendation decision.
- Separate route diagnosis from route mutation. Creating or changing combos, fallback chains, aliases, or provider priorities requires explicit user intent.
- Explain uncertainty when provider availability, rate-limit state, or cost fields are incomplete.

## MCP and A2A

- A2A discovery starts at `GET /.well-known/agent.json`; A2A execution is typically `POST /a2a` and should follow the advertised agent card.
- MCP tools may include model catalog, quota, route simulation, best-combo, route explanation, and cost report tools. Tool names and counts can differ by OmniRoute version and server configuration.
- Do not assume MCP is enabled because HTTP endpoints respond.

## Client integration

- OpenAI-compatible clients: base URL `<base>/v1`; model IDs should come from OmniRoute discovery rather than hardcoded examples.
- Anthropic-compatible clients: base URL `<base>/v1`; verify `/v1/messages` and `/v1/messages/count_tokens` behavior on the target server.
- Gemini-compatible clients: use `<base>/v1beta` for Gemini-style model routes.
- Ollama-compatible clients: use `<base>/api/tags` for tag discovery where supported.
- CLI runtime checks may be available under `GET /api/cli-tools/runtime/{toolId}` for Kilo, Claude Code, Codex, Cline, Cursor, OpenClaw, and related tools.

## Output recommendations

- Prefer concise tables when comparing models. Useful columns: model ID, provider, endpoints, context, output, tools, vision, limits, availability, price, and source endpoint.
- Include an uncertainty note for undocumented, partial, or conflicting fields.
- For operational advice, separate safe read-only checks from actions that mutate OmniRoute state.

## Bundled helpers

- Endpoint cheat sheet: `references/omniroute-endpoints.md`.
- Read-only local probe: `scripts/omniroute_discover.py`. It reads credentials from an environment variable, performs env/access preflight, probes safe endpoints with `requests`, and emits JSON or Markdown with per-endpoint status, failure reason, and repair hints. Model observations are schema-validated with `jsonschema`.
- Model-observation contract: `references/model-observation.schema.json`.
