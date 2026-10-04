---
name: evolve-integrate
description: Integrate AICP with new external systems — fleet projects (openfleet via cluster peering), cloud backends (new OpenRouter model, new Anthropic feature), monitoring stack (new Prometheus exporter, new Grafana dashboard), CI/CD (GitHub Actions, GitLab CI). Adds capability rather than evolves existing — use this when bringing in a NEW integration; use `evolve-api-version` for evolving an existing API. Loads when the operator says "integrate AICP with X" / "add a new backend" / "connect to Y system" / "add Z to monitoring".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# evolve-integrate

Add a new external system integration to AICP. The "integrate" stage of
the lifecycle: NEW capability via NEW dependency, distinct from evolving
an existing API (`evolve-api-version`) or migrating data
(`evolve-migrate`).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: "integrate AICP with X", "add a new backend", "connect
  to Y system", "add Z to monitoring", "wire up <new external service>"
- **Backend integration**: adding a new model provider (e.g., new
  OpenRouter model variant, new Anthropic feature)
- **Fleet integration**: connecting AICP to openfleet machines (per
  CLAUDE.md `## Infrastructure target`)
- **Tooling integration**: adding GitHub Actions, GitLab CI, Codecov, etc.

Do NOT load when:

- The concern is versioning an EXISTING API (load `evolve-api-version`)
- The concern is migrating an EXISTING integration (load `evolve-migrate`)
- The concern is the implementation pattern itself (load
  `architecture-propose` for design, then THIS skill for the integration)

## Operations

### Operation 1 — Author the integration decision

**When**: a new integration is being considered.

**Process**:

1. Per Knowledge Evolution Standards, author a decision page at
   `wiki/decisions/00_inbox/integrate-<system>.md`:
   - WHY: what does this integration enable that AICP doesn't have today?
   - ALTERNATIVES: at least 2 (e.g., "build it ourselves", "use existing
     similar system")
   - REVERSIBILITY: can we remove the integration without breaking AICP?
   - DEPENDENCIES: what new packages/services/configs are pulled in?
2. Get operator approval before implementing
3. The decision page is the contract for what gets built

**Quality bar**: NEVER skip the decision page for a new integration.
Integrations create dependencies; future operators need to know WHY
the dependency exists.

### Operation 2 — Wire the integration into AICP

**When**: decision approved; build the integration.

**Process**:

1. Choose surface for the integration:
   - **Backend**: add to `aicp/backends/<name>.py` (matches existing
     `localai.py`, `claude_code.py` shape)
   - **MCP tool**: per `infra-api` skill + audit criteria, default to
     CLI+Skills unless legitimate cross-conversation use case
   - **Monitoring exporter**: add to `aicp/core/prometheus.py` or
     extend Grafana dashboards
   - **CI**: add `.github/workflows/<name>.yml` or equivalent
2. Implement following AICP conventions (snake_case, type hints, docstring,
   tests in `tests/`)
3. Add config keys to `config/default.yaml` if the integration is
   tunable; document in `.env.example` if env vars are needed
4. Add a test in `tests/` exercising the integration (mock the external
   service for unit tests; provide a smoke-test fixture for integration tests)

**Quality bar**: integration code follows AICP patterns; test coverage
exists; config is operator-discoverable. NEVER ship without these.

### Operation 3 — Document the integration for operators

**When**: integration is shipped; operators need to know how to use it.

**Process**:

1. Add a row to CLAUDE.md `## Tech Stack` if the integration adds a
   runtime dependency
2. Add a section to relevant skill (e.g., new backend → mention in
   `aicp-model-mgmt` related skills table)
3. Update `.env.example` with any new secrets/tokens
4. If the integration affects deployment, update `config-deploy` skill
   reference
5. Add to CHANGELOG

**Quality bar**: an operator running `git pull` should be able to
discover the integration from documentation alone. Code-only integration
is operationally invisible.

### Operation 4 — Test the integration end-to-end

**When**: pre-merge verification.

**Process**:

1. Unit tests pass: `pytest tests/test_<integration>.py` (mocked external)
2. Integration smoke test: run with the real external service connected
   (or a docker-compose fixture if available)
3. `aicp --check` shows the integration in its status output (if applicable)
4. `aicp --self-test` includes the integration probe (if applicable —
   add a `_probe(...)` call in `_run_self_test()`)

**Quality bar**: integrations that aren't covered by `--check` or
`--self-test` are operationally invisible at runtime; add the probe.

## Gotchas

- **Detection**: agent adds an integration without authoring a decision page.
  **Rule**: every new integration gets a decision page in
  `wiki/decisions/00_inbox/`.
  **Reasoning**: integrations create dependencies; without the decision
  page, future operators inherit the dependency without context for WHY.

- **Detection**: agent defaults a new tool to MCP without applying the audit criteria.
  **Rule**: per the MCP audit + CLI-beats-MCP lesson, default new
  exposures to CLI+Skills.
  **Reasoning**: AICP has too many MCP tools already (per audit);
  adding more without justification compounds the schema overhead.

- **Detection**: agent adds an integration without updating `--check` or `--self-test`.
  **Rule**: integrations that affect runtime should be discoverable via
  `--check` (reachability) and `--self-test` (functional).
  **Reasoning**: invisible integrations make operator diagnostic harder
  — they can't tell if the integration is healthy.

- **Detection**: agent adds new env vars without updating `.env.example`.
  **Rule**: every new env var goes in `.env.example` with comment
  explaining purpose.
  **Reasoning**: undocumented env vars are operational landmines (per
  the `config-env` skill).

- **Detection**: agent skips reversibility consideration in the decision page.
  **Rule**: every integration's decision page must answer "can we remove
  this without breaking AICP?" — and if not, why is the dependency
  acceptable.
  **Reasoning**: integrations accumulate; without reversibility analysis,
  AICP becomes brittle over time.

## Reference exemplars

- `aicp/backends/localai.py` — backend integration shape (the canonical
  pattern for new backends)
- `aicp/backends/claude_code.py` — second backend example, including
  subprocess invocation pattern
- `wiki/decisions/01_drafts/localai-over-ollama-vllm-for-multi-model-orchestration.md` —
  example of an integration decision page (alternatives + rationale)
- `tests/test_*.py` — integration test patterns
- `.github/workflows/` (if exists) — CI integration shape
- `wiki/decisions/00_inbox/aicp-mcp-tool-surface-audit-2026-04-19.md` —
  the audit criteria for whether to expose via MCP vs CLI

## Domain context

AICP has 2 backend integrations today (LocalAI + Claude Code) and several
optional ones (OpenRouter, fleet peers via planned cluster peering).
The `aicp/backends/base.py` interface defines the contract new backends
must satisfy. Cloud backends require careful secrets handling
(per `config-secrets` skill). Fleet integrations require cluster peering
(planned per CLAUDE.md `## The Mission` Stage 4 partial).

## Related skills

| Skill | When to use |
|-------|-------------|
| `architecture-propose` | When the integration requires significant architectural design |
| `infra-api` | When the integration adds a new API surface |
| `config-secrets` | When the integration requires new secrets/tokens |
| `config-env` | When the integration adds new env vars or config keys |
| `infra-monitoring` | When integrating monitoring tools specifically |
| `evolve-migrate` | When the integration replaces an existing one (migration) |
| `evolve-api-version` | When the integration is a new VERSION of an existing API |
