---
name: verify-oceans-admin
description: Verify the Oceans LLM admin control plane and backend gateway against the real local stack, seeded demo data, and bounded live providers when required. Use for user-path checks of sign-in, models, API keys, observability, usage costs, spend controls, batches, agent sessions, request logs, Anthropic Messages thinking and effort compatibility, MCP registry and tool access, OpenRouter routing, guardrails, and Skills storage.
compatibility: Requires mise, git, lsof, and Chromium via `mise run //ui:e2e:install`; macOS or Linux.
---

# Verify Oceans Admin

Use this skill to drive the embedded TanStack Start admin UI through the gateway. The primary surface is the browser UI at `/admin`. The gateway API is a secondary surface for health checks, saved-state confirmation, bounded MCP tool calls, and bounded live LLM requests when the change affects the request path.

Read [features/README.md](./features/README.md) before you choose a proof. Use the exact feature recipe for the path under test.

## Plan

Start from the diff, not from memory. From the repository root:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin plan            # against origin/main
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin plan HEAD~1 --json
```

`plan` maps every changed and untracked path through [features/routing.json](./features/routing.json). It prints `RUN <feature>` with the recipe and `drive` command (or `manual recipe`), flags paid proofs, and lists `SKIPPED` paths with a reason. When nothing reaches a runtime surface, it prints `SKIP: no runtime surface`; report that line instead of launching a stack. `UNMAPPED` paths need a decision. Pick the feature the path affects, run that proof, and add the glob to `routing.json` in the same change. `plan` needs no run ID and starts nothing.

## Launch

Run all commands from the repository root. `control-oceans-admin` finds `mise` on `PATH` or at `~/.local/bin/mise`; set `MISE_BIN` if it lives elsewhere. Select a unique run ID:

```bash
export OCEANS_VERIFY_RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$$"
export OCEANS_VERIFY_GATEWAY_PORT=38090
export OCEANS_VERIFY_UI_PORT=33010
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin launch
```

`launch` requires `lsof` for listener and checkout ownership checks. It runs the existing `mise run dev-stack` task with alternate ports through `GATEWAY_PORT` and `UI_PORT`, refreshes this checkout's gitignored `gateway.db` with the local demo seed, and records process IDs under `/tmp/oceans-admin-verification/$OCEANS_VERIFY_RUN_ID/`. It refuses to start if either selected port is in use or another gateway process has this repository as its working directory. A listener counts as this run's only when its working directory belongs to this checkout's git root, so a stack from another worktree that takes a selected port during startup fails the launch instead of being adopted. The launch also fails as soon as the dev stack exits, for example when its gateway cannot bind the port.

`dev-stack` receives `OPENAI_API_KEY` and `OPENROUTER_API_KEY` from fnox through its `secrets` grant in root `mise.toml`, not from the launching shell. Without a terminal, as when an agent runs `launch`, mise runs fnox without its daemon or 1Password prompts. Run `mise run secrets-sync` in the checkout first; new worktrees receive its encrypted cache through `.worktreeinclude`. Otherwise mise refuses to start the stack and names the key fnox could not resolve.

The refresh never recreates `gateway.db`, so rows that earlier runs created stay: onboarding users, audit entries, and the disabled servers every MCP proof leaves behind (servers have no delete API, so cleanup disables them). For a clean database, such as before capturing docs screenshots, run `mise run //crates/gateway:reset-local-demo` or move `gateway.db` aside before launch.

The instance is ready when `launch` prints `ready` and both `/readyz` and `/api/v1/health` answer. The sign-in URL is `http://127.0.0.1:$OCEANS_VERIFY_GATEWAY_PORT/admin/login`. Protected feature routes remain under `/admin/*`.

For Skills storage, set `OCEANS_VERIFY_SKILLS=true` before launch. The harness starts native RustFS through the `rustfs` mise profile and creates a private run-local configuration, database, and synthetic service-account key. See [features/skills.md](./features/skills.md) for the full recipe. This option leaves `gateway.db` unchanged.

This checkout cannot run two verification stacks safely because ordinary runs would both write `gateway.db`. The checkout lock also applies to Skills verification. A stack in another checkout has a separate database and is safe when ports differ. Do not drive a pre-existing instance.

Teardown uses the recorded process IDs:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin cleanup
```

### Shared machine state

- **Cargo output.** Root `mise.toml` sets `CARGO_TARGET_DIR={{config_root}}/target` in `[env]`, and mise applies it over the caller's shell, so exporting `CARGO_TARGET_DIR` before `launch` or `drive` has no effect. Final binaries such as `debug/gateway` and `debug/oceans` stay in this checkout's `target/`, so a build in another checkout cannot replace the binary a proof is using. Intermediate artifacts go to a central per-checkout build dir through `CARGO_BUILD_BUILD_DIR`.
- **pitchfork version warning.** mise supervises daemons through one per-user pitchfork supervisor shared by every checkout. If the `pitchfork` CLI was upgraded since that supervisor started, commands warn about a CLI and supervisor version mismatch. The warning is harmless for verification. Do not restart the supervisor from a verification run, because that stops daemons other checkouts rely on. When nothing else needs them, the user can run `pitchfork supervisor stop` and let the next `mise` daemon command start a current one.

## Doctor

Run the read-only doctor check before browser work and whenever the UI looks stale:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin doctor
```

Doctor confirms that the selected gateway and UI ports are still owned by their recorded listener PIDs and that those processes run from this checkout, checks `/readyz`, and records the gateway service version from `/api/v1/health`. The short-lived launcher PID can exit after mise has started both listeners. A failed ownership check means this instance is not safe to drive.

## Drive

The harness is `control-oceans-admin`. It uses the repository's installed Playwright package and Chromium. It drives ARIA roles, accessible labels, route paths, and existing test IDs from `crates/admin-ui/web`.

Prove the Models path:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin drive models
```

The Models driver runs the idempotent `mise run //ui:e2e:install` task to ensure Chromium is available. It then opens the protected `/admin/api-keys` route, captures its redirect to sign-in, signs in as the seeded `admin@local` user, follows the `Models` sidebar link, checks the displayed count against rendered rows and the total count against the read-only admin models response, checks the always-visible `Intelligence Index` against that response, checks every platform-admin `Model info` section, enables the optional `Context window` and `Capabilities` columns, and opens `Client config` for `gpt-6-astra`.

Prove the Leaderboard and Agent Harnesses paths together:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin drive observability
```

The Observability driver opens the protected Leaderboard route, signs in, and compares both the
Leaderboard and Agent Harnesses desktop tables with their production admin API responses for the
seeded 7-day window. It selects the 31-day range on both pages and repeats the comparison. The proof
also requires the new leaderboard columns, harness token columns, a Mastra row with its Lobe icon,
and an Oh My Pi row with its white `omp.sh` mark.

Features whose routing entry says `manual` have no driver yet. Follow their recipe with any browser automation your harness offers (Playwright via `mise exec -- node`, a built-in browser, or an MCP browser). Apply the same proof rules as a driver: capture the entry action, capture the resulting state, and check API parity. Save screenshots into the run's evidence directory, then write the proof with `control-oceans-admin record` (see [Proofs](#proofs)). The admin UI is server-rendered, so wait for network idle after each navigation before you fill fields; values typed before hydration are silently discarded. Read counts only after the list re-renders, not straight after the URL changes.

For other features, follow the exact stable handles in the feature map. Extend the driver with a named command before you report a new path as automated.

Prove backend gateway routing and generated-tool guardrails through OpenRouter:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin drive backend-gateway
```

The Backend Gateway driver opens the real API Keys page, creates a temporary user key limited to `deepseek-v4.1-flash`, evaluates one synthetic destructive command without executing it, and sends one bounded forced-tool Chat Completions request through OpenRouter. It confirms the request-linked guardrail decision and request-log attempt, writes sanitized evidence, revokes the key, and confirms that the revoked key is rejected. Use [features/backend-gateway.md](./features/backend-gateway.md) for the exact contract.

Prove service tiers through OpenRouter:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin drive service-tiers
```

The Service Tiers driver creates a temporary key for the tier canary models, checks tier discovery and four free rejections (unknown tier, conflicting fields, policy-blocked tier, no route for the tier), then sends six short paid requests: default, priority and flex A/B on `gpt-6-luna`, the route-forced `gpt-6-luna-fast`, Anthropic `speed: "fast"` on `claude-haiku-5.5`, and a streamed priority request. It compares OpenRouter's per-token prompt cost across tiers, checks the requested and served tier in each request log, screenshots the request detail, and revokes the key. Use [features/service-tiers.md](./features/service-tiers.md) for the exact contract.

Prove the inference endpoints and the OpenCode plugin in real clients:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin drive harness-integration
```

The plan selects this proof for changes to the chat, Responses and Messages handlers, model discovery, generated client configs, and `packages/opencode-oceans`. The driver needs a run ID and `OPENROUTER_API_KEY`, but no launched stack: `tests/harness-integration` builds the gateway from this checkout and starts a temporary one. It runs the harness x model matrix (OpenCode plugin, Pi, Oh-My-Pi and Claude Code with GPT-6 Luna, Claude Haiku 5.5 and Gemini 4 Hydrogen), the per-harness MCP checks, and the packed-plugin suite, and records one check per test. Use [features/harness-integration.md](./features/harness-integration.md) for the exact contract.

Prove the MCP registry, Tool Sets workbench, grants, and live tool routing:

```bash
export OCEANS_VERIFY_MCP_CANDIDATES_FILE=/absolute/path/to/mcp-candidates.json
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin drive mcp
```

Read [features/mcp.md](./features/mcp.md) before launch. It defines the required gateway credential aliases and the candidate file. The aliases must be exported in the launching shell; `launch` records their names, and the driver trusts that record rather than its own environment. The MCP driver creates temporary servers, two tool sets, and one API key through the UI. One server points at `https://unreachable.invalid/mcp` to prove how a failed discovery is reported without contacting a real host. It verifies saved membership, independent drafts, client configurations, grant enforcement, direct and aggregate tool calls, and invocation records. The API key UI requires one explicit model grant; the driver selects one model but sends no model request. This proof uses public access or static upstream credentials and does not test OAuth consent or token refresh.

Prove Skills storage and ownership with Oceans and native RustFS:

```bash
# Set OCEANS_VERIFY_SKILLS=true before the launch command.
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin drive skills
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin evidence skills
```

Read [features/skills.md](./features/skills.md) before launch. This proof drives regular-user namespace claims, ZIP uploads, file previews, version and default changes, and browser downloads. It compares saved API state and archive digests, verifies shared reads and owner-only updates, and checks service-account restrictions. It sends no LLM request.

## Live LLM requests

For `/v1/messages`, thinking/display/effort controls, native transport mapping or Messages streaming changes, follow [Anthropic Messages](./features/anthropic-messages.md). The planner selects `anthropic-messages` in addition to applicable live/request-log proofs. Run its offline gate before the live pass:

```bash
mise exec -- node .agents/skills/verify-oceans-admin/scripts/check-messages.mjs \
  --output "/tmp/oceans-admin-verification/$OCEANS_VERIFY_RUN_ID/evidence/messages-regressions.json"
```

The gate requires the native thinking matrix and general gateway regression suites to pass; zero tests or missing named regressions fail. It is an offline helper, not a browser driver or live-native-provider proof. The recipe pairs that evidence with one public Messages canary, its real Request Logs UI/API result, and key revocation. Reuse the same canary for `live-llm-requests`; do not make extra paid requests just to satisfy multiple planned feature IDs. OpenRouter Claude routes use native Messages; explicitly record when Vertex/Bedrock access or a full Claude Code session remains unverified.

Read-only control-plane verification is the default and does not call an upstream provider. Add one short, paid live request when the change affects request routing, provider authentication, request or response translation, streaming, tool calls, usage accounting, request logging, provider error mapping, or another behavior that a configured model list cannot prove. Do not add a paid request for UI-only, documentation-only, seed-only, or unrelated configuration changes.

Use [features/live-llm-requests.md](./features/live-llm-requests.md) for the exact recipe. Prefer `deepseek-v4.1-flash` through OpenRouter for generic request-path changes, and `claude-haiku-5.5` through OpenRouter for `/v1/messages` changes. Keep every canary at `max_tokens` 4096 or less. For Bedrock-specific request-path testing, use gateway model `gpt-oss-120b-bedrock`, which routes to Bedrock Mantle model `openai.gpt-oss-120b`. Do not use `openai.gpt-5.6-luna`; it is not enabled for this AWS account. Run both providers only when provider parity is the behavior under test.

Keep each prompt synthetic and small. Limit the output, create a temporary gateway API key with access only to the selected model, and revoke it after the proof. Never print or save raw gateway or provider credentials. For Bedrock Responses requests, set `store: false` unless stored-response behavior is the subject of the test.

A request to verify a request-path or provider change permits one bounded canary when the required local credential is available. Credential presence alone does not justify paid calls for other work. If a canary is outside the stated task, report it as an available paid check instead of running it.

## Proofs

Every proof is a `*-proof.json` file in the run's evidence directory with one shared envelope. Drivers write it through [scripts/proof.mjs](./scripts/proof.mjs). A driver replaces its proof file with a failing placeholder before it starts the browser and writes the real envelope when it finishes or fails, so a crashed attempt never leaves an older passing proof behind.

| Field | Meaning |
|---|---|
| `schemaVersion` | Envelope version, currently `1`. |
| `runId`, `harness`, `gatewayVersion` | Which run, which agent harness (`OCEANS_VERIFY_HARNESS`, else `claude` under Claude Code, `ci` under CI, or `unknown`), and which gateway build. |
| `gitSha`, `dirty` | `HEAD` and whether the working tree had changes when the proof ran. Informational. |
| `sourceHash`, `sourceFiles` | Hash of the path, Git file mode, and content of every file that `routing.json` sends to these features. This is what `--require-current` compares, so a proof survives a commit or an unrelated edit and goes stale only when its own code changes. |
| `launchSourceHash` | The same hash over the snapshot `launch` saved, or `null` without one. When it differs from `sourceHash`, the stack ran older code than the proof claims, and `--require-current` marks the proof stale. `--require-current` also rejects a proof with no launch snapshot, so record manual proofs under a launched run ID. Relaunch after editing routed files. |
| `featureIds` | IDs from `features/routing.json`. |
| `method` | `driver` or `manual`. |
| `verdict` | `pass`, `fail`, or `blocked`, derived from `checks`. A required `fail` wins over a required `blocked`; optional checks never decide it; no required checks means `fail`. |
| `checks[]` | `{ id, status, required?, observed?, expected?, note? }`, one per assertion. |
| `artifacts[]` | Screenshots and ARIA snapshots in the evidence directory that back the checks. A proof whose artifacts are missing does not count. |
| `details` | The driver's own sanitized payload: counts, IDs, and the action log. |

Use `blocked` only for a named missing prerequisite, such as an unset credential alias, and put the prerequisite in the check's `note`. A product or harness defect is `fail`.

Record a manual recipe after you capture its screenshots:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin record usage-costs \
  --check "kpis-match-spend-report=pass:4 of 4 KPIs" \
  --check "owner-filter=blocked:no owner with spend in the seed" \
  --optional "export-download=pass" \
  --artifact 01-usage-costs.png --artifact 02-usage-costs-30d.png
```

`record` is for features whose `routing.json` proof is `manual`; it refuses a feature that has a driver. `--check` is required and `--optional` is not. Each takes `id=pass|fail|blocked[:note]`. At least one `--artifact` that exists in the evidence directory is required. `--file name-proof.json` overrides the default `<feature>-proof.json`. Record before `cleanup`, which removes the recorded gateway version. Notes and details must never contain keys, cookies, tokens, prompts, or responses.

`evidence` reads the envelopes rather than checking for file names:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin evidence models mcp --require-current
```

It prints one `PASS` or `FAIL` line per feature and exits non-zero unless every named feature's newest proof is from this run, has `verdict: pass`, and still has all its artifacts. With `--require-current`, it also fails a proof whose `sourceHash` no longer matches the working tree, whose stack was launched from different source, or that has no launch snapshot. Any other option is rejected, so a misspelled flag fails instead of skipping the freshness check. With no feature names, it checks every proof in the run. `observability` and `live-llm` remain aliases for `leaderboard agent-harnesses` and `live-llm-requests`.

`report` writes the run as Markdown for the pull request:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin report --plan
```

It produces one table row per feature from its newest proof, as `evidence` reads it, with the verdict, check counts, failing or blocked notes, a `⚠ stale` marker, and evidence files. A proof that cannot count for another reason (another run, missing artifacts, or a verdict that disagrees with its checks) shows as `❌ invalid` with the reason. With `--plan [base-ref]`, it adds `Planned but not verified` for every feature that `plan` selected without a current passing proof, plus unmapped paths and skip reasons. Paste the output under the PR description instead of writing a free-form summary.

## Evidence

Evidence is written to `/tmp/oceans-admin-verification/$OCEANS_VERIFY_RUN_ID/evidence/`. Keep the run ID in the verification report. The Models proof produces:

- `01-login.png` and `01-login.aria.txt` for the user entry state.
- `02-models.png` and `02-models.aria.txt` for the resulting model list.
- `03-model-info.png` and `03-model-info.aria.txt` for the selected model Access detail.
- `04-model-columns.png` and `04-model-columns.aria.txt` for the optional desktop columns.
- `05-model-client-config.png` and `05-model-client-config.aria.txt` for generated client configuration.
- `models-proof.json` with one check per assertion; `details` holds the visited URLs, displayed, rendered, total, and API counts, model ID, and action log.
- `stack.log` beside the evidence directory for launch and runtime diagnostics. Cleanup redacts seeded passwords and raw demo API-key secrets from this log.

The Observability proof produces:

- `01-observability-login.png` and `01-observability-login.aria.txt` for the protected entry state.
- `02-leaderboard-7d.*`, `03-leaderboard-31d.*`, and `03b-leaderboard-mobile.*` for API parity and responsive presentation.
- `04-agent-harnesses-7d.*` and `05-agent-harnesses-31d.*` for the two Agent Harnesses ranges.
- `observability-proof.json` for feature IDs `leaderboard` and `agent-harnesses`; `details` holds the production API leaders, rendered table values, ranges, chart series counts, Mastra/Oh My Pi icon checks, and action log.

A valid proof exercises the real browser path. It captures the action and resulting state, not only a final screenshot. It also confirms rendered data through the production admin API used by the UI. Do not use internal state setters or test-only endpoints. The local demo seed is the production seed boundary for these development commands; no provider call is required for Models, Leaderboard, or Agent Harnesses.

A live canary is separate evidence. Name the gateway model, provider, endpoint family, and observed request-log record. A rendered configured provider or successful health check is not live-provider proof.

The Backend Gateway proof produces:

- `01-backend-api-keys.png` and `01-backend-api-keys.aria.txt` for the authenticated key-management entry state.
- `backend-gateway-canary-proof.json` with checks for key creation, the direct audit, the tool call, the request-linked decision, the request-log attempt, and key revocation; `details` holds the gateway model, provider, upstream model, request ID, status, usage presence, tool count, guardrail rule, payload capture mode, and action log.
- No prompt, response, gateway key, provider credential, or authorization header.

The Service Tiers proof produces:

- `service-tiers-request-log-priority.png` and `service-tiers-request-log-downgrade.png`, with `request-log-payloads` masked.
- `service-tiers-proof.json` with checks for key creation, discovery, each rejection, each paid request, request-log tiers, the request detail, and key revocation; `details` holds the served tier per request and the request-log ID with its requested and served tier.
- No prompt, response, gateway key, provider credential, or authorization header.

The Harness Integration proof produces:

- `harness-integration-results.json`, the vitest JSON report.
- `harness-integration-proof.json` with one check per test and `plugin-live-usage`; `details` holds each live plugin request with its request-log ID, requested and served tier, tokens, and OpenCode and Oceans cost. A skipped test is an optional `blocked` check.
- `harness-integration.log` beside the evidence directory, with the suite and temporary gateway output. It holds no gateway key or provider credential.

The MCP proof produces:

- Screenshots and ARIA snapshots for sign-in, discovery, the failed-discovery overview and toast, the menu disable and enable, saved membership, independent drafts, client configuration, mobile layout, grants, and filtered invocation lists.
- `mcp-proof.json` with one check per candidate plus discovery-feedback, menu-disable, menu-enable, workbench, grant, tool-call, and cleanup checks; `details` holds candidate results, saved IDs, grant checks, request and invocation IDs, transport type, result-marker counts, the negative-auth controls (an authentication error on a tool call, or discovery rejected with its HTTP status), and cleanup actions. A candidate whose `OCEANS_MCP_DISCOVERY_*` alias was not set for the launched gateway, according to the run's `stack-env.json`, is recorded as `blocked` without being registered.
- No raw key, authorization header, tool arguments, or tool-result payload in the proof JSON. Invocation detail is inspected in memory and is not captured.

An optional candidate failure does not change the verdict but remains a reported gap. Check `control-oceans-admin evidence mcp` before and after stack cleanup.

The Skills proof produces:

- `01-skills-login.*`, `01b-skills-bundled.*`, `02-skills-before.*`, `03-skills-file-preview.*`, `04-skills-new-version.*`, `05-skills-owner-default.*`, `06-skills-other-owner.*`, and `07-skills-catalog-after.*` screenshots and ARIA snapshots.
- `skills-proof.json` with one check per step plus `user-cleanup`; `details` holds the storage scope, saved IDs, version digests, caller checks, and action log.
- After stack teardown, cleanup adds a `storage-cleanup` check to `skills-proof.json` confirming that the run's object prefix is empty and its database was removed. A failed storage cleanup turns the verdict to `fail`.
- No gateway key, RustFS credential, password, or authorization header in proof artifacts.

Mocks are valid only when the production boundary already isolates an external system. This Models proof uses no mock. Do not interpret a rendered configured provider as proof that its credentials or live upstream service work.

## Cleanup

Always run cleanup after success and after each failed attempt:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin cleanup
```

Cleanup sends termination only to the process IDs recorded by this run, and only when the process still owns its port and runs from this checkout. It reports and skips a recorded listener from another checkout. It removes the run's control files and checkout lock. It does not remove `evidence/` or `stack.log`, and it does not delete `gateway.db`. For an opt-in Skills run, it also removes the run-specific RustFS object prefix and private database/config/token, then stops RustFS only if this run started the recorded process. RustFS credentials, its data directory, and other object prefixes remain intact.

Confirm that proof survived teardown:

```bash
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin evidence backend-gateway --require-current
.agents/skills/verify-oceans-admin/scripts/control-oceans-admin report --plan
```

Name the features you verified so `evidence` requires a passing proof for each one.

## Helpers

The executable helper is [scripts/control-oceans-admin](./scripts/control-oceans-admin). Its supported commands are:

```text
control-oceans-admin plan [base-ref] [--json]
control-oceans-admin launch
control-oceans-admin doctor
control-oceans-admin drive models
control-oceans-admin drive observability
control-oceans-admin drive backend-gateway
control-oceans-admin drive service-tiers
control-oceans-admin drive harness-integration
control-oceans-admin drive mcp
control-oceans-admin drive profile
control-oceans-admin drive skills
control-oceans-admin record <feature-id> --check id=status[:note] --artifact file [...]
control-oceans-admin evidence [feature-id...] [--require-current]
control-oceans-admin report [--plan [base-ref]]
control-oceans-admin cleanup
```

The browser implementations are [scripts/drive-models.mjs](./scripts/drive-models.mjs), [scripts/drive-observability.mjs](./scripts/drive-observability.mjs), [scripts/drive-backend-gateway.mjs](./scripts/drive-backend-gateway.mjs), [scripts/drive-service-tiers.mjs](./scripts/drive-service-tiers.mjs), [scripts/drive-mcp.mjs](./scripts/drive-mcp.mjs), [scripts/drive-profile.mjs](./scripts/drive-profile.mjs), and [scripts/drive-skills.mjs](./scripts/drive-skills.mjs). The MCP driver uses [scripts/mcp-browser.mjs](./scripts/mcp-browser.mjs) and [scripts/mcp-canary.mjs](./scripts/mcp-canary.mjs), and validates its candidate file with [scripts/mcp-candidates.mjs](./scripts/mcp-candidates.mjs). `plan` runs [scripts/plan-verification.mjs](./scripts/plan-verification.mjs). `record`, `evidence`, and `report` run [scripts/proof-cli.mjs](./scripts/proof-cli.mjs) over the envelope in [scripts/proof.mjs](./scripts/proof.mjs).

Offline regression tests (no stack, no upstream calls):

```bash
mise exec -- node --test .agents/skills/verify-oceans-admin/scripts/*.test.mjs
```

Call the drivers through `control-oceans-admin` so they receive the recorded URL, evidence path, credentials, and gateway version.

[scripts/drive-harness-integration.mjs](./scripts/drive-harness-integration.mjs) runs the client suite instead of a browser. `control-oceans-admin` gives it the evidence path, a source snapshot taken before the suite builds the gateway, and the `gateway` crate version.
