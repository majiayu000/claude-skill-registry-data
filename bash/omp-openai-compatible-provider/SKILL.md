---
name: omp-openai-compatible-provider
description: "Use when adding a LAN or self-hosted OpenAI-compatible model (GPUStack, vLLM, LiteLLM, LM Studio) to omp or its roles, or 'unable to get local issuer certificate' or 'models.yml validation failed'."
---

# Wiring a self-hosted OpenAI-compatible endpoint into omp

Goal: make a self-hosted inference endpoint selectable in omp with **correct**
metadata, then optionally bind it to model roles. Never guess capabilities —
every field below is cheap to measure, and wrong metadata degrades silently.

## 1. Find the endpoint before asking for it

Users often already have it wired into a sibling tool. Check, in order:

- `process.env` for `*_API_KEY` / `*_BASE_URL` (a key present with no URL is a strong signal)
- `reg query HKCU\Environment` (persisted user env on Windows)
- Shell profiles: `~/Documents/PowerShell/*.ps1`, `~/.bashrc`, `~/.zshrc` — and any
  helper script they dot-source
- Sibling agent configs: `~/.config/opencode/**`, `~/.codex/config.toml`, `~/.continue/config.json`

Grep those for the vendor name. This beats DNS guessing and LAN/ARP scanning, which
is slow, noisy, and beyond what was asked.

## 2. Probe capabilities before writing config

Run against the real endpoint. Each probe maps to a config field:

| Probe | Field it decides |
| --- | --- |
| `GET {base}/models` | model ids; whether discovery is viable at all |
| `POST` chat with `max_tokens: 99000000` | `contextWindow` — the 400 error states `max_model_len` verbatim |
| chat with a `tools[]` + `tool_choice: auto` | `supportsTools`; measure latency here too |
| chat with `chat_template_kwargs: {enable_thinking: false}` | `thinking.requiresEffort: false` (only if reasoning comes back null/empty) |
| chat with `chat_template_kwargs: {reasoning_effort: "low"\|"high"}` | `compat.qwenTemplateReasoningEffort`; compare CoT length to confirm it's honored |
| streaming chat, collect `delta` keys | `compat.reasoningContentField` (`reasoning`, `reasoning_content` or `reasoning_text`) |
| chat with an inline `image_url` data URI | `input: [text, image]` — generate a solid-color PNG and ask its color; a 200 alone proves nothing |

## 3. Internal CA: the leaf-only chain trap

Symptom: PowerShell/`Invoke-RestMethod` works, omp fails with
`unable to get local issuer certificate`.

Cause: the server sends **only the leaf**. .NET fetches the missing intermediate via
AIA; Bun/Node cannot. The CA is not necessarily missing from the Windows store.

Fix — export the CA chain and point `NODE_EXTRA_CA_CERTS` at it:

1. `TcpClient` + `SslStream` to grab the leaf, then `X509Chain.Build()` (Windows does
   the AIA fetch).
2. Write every chain element **except the leaf** as PEM to `~/.omp/agent/certs/<name>.pem`.
3. `setx NODE_EXTRA_CA_CERTS "%USERPROFILE%\.omp\agent\certs\<name>.pem"`.

Export CA certs only, never the leaf — short-lived leaves (24–48h ACME/step-ca) rotate
constantly; CA certs last years, so rotation stays invisible. Check `valid_from`→`valid_to`
before alarming anyone about a near expiry date: a 48h window with 35h left is healthy
automation, not an outage.

`NEVER` disable TLS verification in persisted config. `rejectUnauthorized: false` is
acceptable *only* as a throwaway reachability probe, never carried into `models.yml`.

Verify the var is load-bearing: run the same omp turn with and without it. Discovery may
pass from cache while inference fails — test an actual completion, not just `models find`.

## 4. models.yml shape

```yaml
providers:
  <provider-id>:
    baseUrl: https://host/<openai-surface>
    apiKey: SOME_API_KEY      # env var NAME, else used literally; "!cmd" runs a command
    api: openai-completions   # openai-responses only if /v1/responses exists
    authHeader: true
    discovery:
      type: openai-models-list
      injectV1: false         # baseUrl already ends in the version segment
    modelOverrides:
      <model-id>:
        contextWindow: 262144
        maxTokens: 32768
        reasoning: true
        input: [text, image]
        supportsTools: true
        tokenizer: qwen3
        cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }
        thinking:
          mode: effort        # REQUIRED, and so is efforts
          efforts: [minimal, low, medium, high]
          defaultLevel: low
          requiresEffort: false
        compat:
          thinkingFormat: qwen-chat-template
          reasoningContentField: reasoning
```

Gotchas:

- Any validation error disables the **whole file**. omp prints
  `models.yml validation failed — custom providers disabled` and drops every custom
  provider, not just the broken one. Run `omp models find <provider>` after every edit.
- `thinking.mode` is **mandatory**
  (`effort`|`budget`|`google-level`|`anthropic-adaptive`|`anthropic-budget-effort`), and so
  is `thinking.efforts` (legacy `levels` or `minLevel`+`maxLevel` also pass). Schema verified
  against omp v18.2.11 source, 2026-09-24.
- `modelOverrides` are re-applied *after* discovery, so discovery + overrides compose:
  new deployments appear automatically, pinned ids keep corrected metadata.
- Prefer discovery over hand-listed `models:` — the cluster's deployments change.
- `requiresEffort: false` only after verifying an explicit thinking-off request; otherwise
  `:off` gets clamped to the lowest effort.

### GPUStack specifically

Docs: `/v1-openai` is the OpenAI surface; `/v1` is an alias **except `models`, which is
reserved for management APIs**. Some v2 deployments answer OpenAI-shaped on both — verify by
comparing entry keys on each path. Prefer `/v1-openai`: `discovery.type: openai-models-list`
depends on `GET {baseUrl}/models`, and that's the one endpoint documented as reserved.

The built-in `vllm` provider path does not help here — GPUStack returns `meta: null` with no
`max_model_len`/`context_length`, so context must be hand-set from the 400-error probe.

## 5. Roles

`~/.omp/agent/config.yml` → `modelRoles`, values are `provider/model[:effort]`.

Sensible local-model targets: `tiny` (session titles) and `commit` — use `:off`, no CoT
needed. `smol` at `:low`. Leave `default`/`slow`/`plan`/`task` on the frontier model: `task`
drives subagents that make real edits.

`advisor` is a judgment call, not a freebie — it runs the session watchdog, so local means a
lower catch rate. Call it out and let the user veto.

## 6. Verify — all four, in order

```bash
omp models find <provider>                     # metadata correct?
omp models refresh && omp models find <p>      # cold discovery, not cache
omp -p "reply with only: OK" --model <p>/<id>  # live turn
omp -p "use your bash tool to run 'echo x'" --model <p>/<id>:off   # tools + :off
omp -p "reply OK" --model @smol                # role resolution
```

`setx` reaches only new processes — tell the user to restart their omp session.
