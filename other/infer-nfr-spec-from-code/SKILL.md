---
name: infer-nfr-spec-from-code
description: Infer the NFR spec from scan-index.json during /codify by reading framework idioms, dependency manifests, deploy configs, and CI signals to reconstruct what non-functional requirements the shipped code already enforces — per-NFR target, delivery mechanism (named library / middleware / layer), and verification method — with every entry traced to concrete evidence paths. Used exclusively by tech-architect in the /codify play.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# infer-nfr-spec-from-code

Called by `tech-architect` during /codify AFTER `infer-physical-architecture-from-code` and `infer-quality-profile-from-code` (or the equivalent quality-profile proposal) have produced their artifacts. Produces `architecture/nfr-spec.yaml` at `{stm_base}/{issue}/evidence/codify/proposals/architecture/nfr-spec.yaml`.

## Purpose

In greenfield /arch, `derive-nfr-spec` translates intake quality targets into a per-NFR contract — "what SHOULD the NFRs be". In brownfield /codify, the NFRs have already been implemented (partially or fully) as rate limiters, retries, health checks, auth middlewares, caches, tracing SDKs, and CI gates. This skill inverts the semantics: it reconstructs "what ARE the enforced NFRs" from the code that delivers them.

Every NFR entry in the output MUST name a specific mechanism delivering it (a library pin, a middleware at a named layer, a deploy-time configuration block) and a specific verification method (a test file pattern, a CI job, a monitor endpoint). NFR entries without both fields are not emitted as primary — they land as `knowledge_gaps`. Invented targets are forbidden: if no evidence signals a concrete target, the NFR class is recorded as a gap for the /codify checkpoint, never fabricated.

Grounding: every primary NFR traces to at least one scan-index path (dependency manifest, framework idiom match, deploy config, CI file, rg hit). Grounding is the boundary between inference and invention.

## Input

Receive from tech-architect via JSON contract.

- `scan_index_path` (path, required) — `scan-index.json` produced by scan-codebase.
- `related_proposal_paths` (block, required):
  - `quality_profile_path` — prior `architecture/quality-profile.yaml` proposal from test-engineer in /codify.
  - `physical_architecture_path` — prior `architecture/physical-architecture.yaml` proposal.
  - `logical_architecture_path` — prior `architecture/logical-architecture.yaml` proposal.
- `stm_base` (path, required) — STM root resolved from `.garura/core/config.yaml` `stm.base-path`.
- `issue` (str, required) — issue number driving /codify.
- `output_path` (path, required) — `{stm_base}/{issue}/evidence/codify/proposals/architecture/nfr-spec.yaml`.
- `decision_manifest_path` (path, required) — `decision-manifest-infer-nfr-spec-from-code.yaml` alongside the artifact.
- `ltm_context` (block, required) — `{product_base, core_base, query_domains, locked_artifacts}`. Presence triggers the Resolution Protocol.
- `resolution_trace_path` (path, required) — where `resolution-trace.yaml` is written.

## Process

1. **Validate inputs.** Confirm `scan_index_path` exists and parses as JSON. Confirm each path under `related_proposal_paths` exists and parses as YAML. Missing/malformed scan-index → structured failure `scan_index_missing`. Missing related proposal → structured failure `missing_related_proposal` with the offending path.

2. **Execute LTM Resolution Protocol R3** per `core/components/memory/standards/rules/resolution.md`. Query domains: `quality`, `performance`, `security`, `reliability`, `observability`. R3 runs against KB patterns for well-known NFR delivery mechanisms (rate-limit middlewares, retry libraries, tracing SDKs, auth packages) so the skill can map a library pin to the NFR class it delivers. Write the trace to `resolution_trace_path`.

3. **Load scan-index sections used.** The following scan-index sections are the sole code-derived input:
   - `manifests` — package.json, pyproject.toml, go.mod, Gemfile, pom.xml dependency lists.
   - `patterns.framework_idioms` — per-file matches for framework-specific symbols (e.g., `express-rate-limit`, `helmet()`, `@CircuitBreaker`, `opossum`, `p-retry`).
   - `patterns.naming_suffix_counts` — for observability class hints (`*Tracer`, `*Metric`, `*Logger`).
   - `patterns.test_framework_signals` — for verification mapping.
   - `entry_points` — for locating `/health`, `/healthz`, `/readyz`, `/metrics`.
   - `config_files` — for deploy-time config: rate-limit thresholds, CDN configs, autoscale blocks, timeout settings, CSP headers, multi-region settings.
   - `docs` — for ADR mentions of SLO budgets / multi-region intent.
   - `git` — for CI file churn indicating active security/quality gates.

   If any referenced section is absent from scan-index, record that axis as `insufficient` and carry a meta warning; do not fabricate.

4. **For each NFR class, score signals and infer concrete targets.** Six NFR classes; each has an explicit signal → concrete-NFR mapping table.

   ### 4a. Performance
   - Rate-limit middleware matches in `framework_idioms` (`express-rate-limit`, `@fastify/rate-limit`, `django-ratelimit`, `golang.org/x/time/rate`) → infer target: "p95 latency < 500ms under rate-limit enforced at N req/{window}" where N/window come from the matched config block when extractable; otherwise target records the library pin and marks threshold as `insufficient`.
   - Caching libs in `manifests` (`redis`, `ioredis`, `memcached`, `node-cache`, `django-redis`) → infer target: "hot-path read latency < cold-path latency by cache hit ratio"; delivery mechanism names the library and the code path (module from scan-index) where it is used.
   - CDN / edge config in `config_files` (Cloudflare `wrangler.toml`, Fastly `fastly.toml`, CloudFront block in Terraform) → infer target: "static asset TTFB regional SLO < {edge-default}"; mechanism names the CDN product.
   - Timeout configs in `config_files` or framework_idioms (`axios.defaults.timeout`, `requests.get(timeout=...)`, `http.Client{Timeout:...}`) → infer target: "upstream call timeout N ms"; mechanism is the HTTP client configuration.
   - Verification method: map to `k6` / `autocannon` / `locust` when found in manifests, else `grafana dashboard` when `grafana` found in config_files, else marked `insufficient` and listed in knowledge_gaps.

   ### 4b. Reliability
   - Retry libs in `manifests` (`p-retry`, `async-retry`, `tenacity`, `resilience4j-retry`, `backoff`) → infer target: "transient failure auto-retried up to N attempts with backoff"; mechanism names the library and the wrapping module.
   - Circuit-breaker libs in `manifests` / `framework_idioms` (`opossum`, `resilience4j-circuitbreaker`, `pybreaker`, `gobreaker`) → infer target: "failing dependency isolated within {threshold} failures"; mechanism names the library.
   - Health check endpoints discovered via rg / scan-index scan for `/health`, `/healthz`, `/readyz`, `/live` in `entry_points` → infer target: "liveness/readiness probe responds < 1s"; mechanism names the endpoint path and the handler file.
   - Monitoring deps (`@sentry/*`, `newrelic`, `datadog-api-client`, `sentry-sdk`) → infer target: "runtime errors captured and alerted"; mechanism names the SDK + its init file.
   - Verification method: CI pipeline health-check job when present in `config_files`, else uptime monitor config when present, else `insufficient`.

   ### 4c. Security
   - `helmet` / `@fastify/helmet` / `secure` (python) in manifests → infer target: "standard security headers applied on every response"; mechanism names the middleware and its mount point.
   - CSRF libs (`csurf`, `django.middleware.csrf`, `csrf-protect`) → infer target: "CSRF protection on state-changing routes"; mechanism names the middleware.
   - Auth libs (`passport`, `next-auth`, `django-allauth`, `devise`, `spring-security`) → infer target: "authentication enforced on protected routes"; mechanism names the auth library and the guard/middleware.
   - Rate-limit (same matches as performance) → doubles as security NFR "brute-force resistance via request throttling".
   - Secrets-scanning in CI (`gitleaks`, `trufflehog`, `detect-secrets` in `config_files` under `.github/workflows/` or equivalent) → infer target: "no secrets committed to repo"; mechanism names the scanner job.
   - Content-Security-Policy in `config_files` or helmet config blocks → infer target: "CSP header enforced with directives: {extracted}".
   - Verification method: SAST tool in CI when found (`semgrep`, `bandit`, `codeql` workflow), dependency audit (`npm audit`, `pip-audit`, `snyk`), else `insufficient`.

   ### 4d. Scalability
   - Worker pool libs (`bull`, `bullmq`, `celery`, `sidekiq`, `rq`, `asynq`) → infer target: "work offloaded to N worker processes"; mechanism names the queue lib + its worker module.
   - Queue deps (`amqplib`, `kafkajs`, `redis` used as queue, `nats.js`) → infer target: "async request decoupling via {queue product}".
   - Autoscale configs in `config_files` (k8s HPA yaml, Railway autoscale block, Render `autoscaling.yaml`, Fargate autoscale) → infer target: "horizontal scale up to N replicas on {metric}"; mechanism names the autoscale definition file.
   - Verification method: load test rig when present (k6, artillery, locust), else `insufficient`.

   ### 4e. Observability
   - Tracing libs in `manifests` (`@opentelemetry/api`, `@opentelemetry/sdk-*`, `opentelemetry-python`, `datadog-trace`) → infer target: "distributed traces emitted for all inbound requests"; mechanism names the OTel SDK + its init file.
   - Metrics libs (`prom-client`, `prometheus-client` (python), `micrometer`) → infer target: "metrics exposed on /metrics scraped by {collector}"; mechanism names the metrics lib + endpoint.
   - Logging libs with structured format (`pino`, `winston` with json formatter, `structlog`, `zap`, `slog`) → infer target: "structured logs emitted at INFO+ with request-id correlation"; mechanism names the logger lib.
   - Verification method: dashboard/alert configs in `config_files` when present; else grep `naming_suffix_counts` for `*Tracer`, `*Metric`; else `insufficient`.

   ### 4f. Availability
   - SLO markers in `docs` (ADR or README mentions of "SLO", "uptime target", "availability budget") → infer target literally from the cited SLO statement; mechanism is the ADR reference.
   - Multi-region configs in `config_files` (Terraform `aws_region` with multiple providers, Cloudflare multi-region blocks, Vercel `regions: ["iad1","fra1"]`) → infer target: "service reachable from {N} regions"; mechanism names the deploy config.
   - Verification method: synthetic monitor config when present, else uptime pinger in `config_files`, else `insufficient`.

5. **Score confidence per NFR entry.**
   - `high` — at least one primary signal (library pin OR config block) AND a verification signal.
   - `medium` — at least one primary signal but no verification signal (or vice versa).
   - `low` — only an indirect signal (e.g., naming suffix counts without a library pin).

   NFR entries with zero signals are not emitted — they become `knowledge_gaps` entries naming the NFR class and listing the scan-index sections that were checked but empty.

6. **Cross-reference related proposals.** For every primary NFR entry, verify the delivery mechanism can be anchored to a component ID from `logical_architecture_path` or a stack pick from `physical_architecture_path` or a quality target from `quality_profile_path`. When an anchor exists, cite it in the NFR's `ref` field. When no anchor exists in the related proposals, mark the NFR with `anchor_status: "unbound"` and record as a mid-tier decision for the checkpoint (the /codify user will confirm the binding).

7. **Write decision manifest.** Emit BEFORE the primary artifact. One entry per inferred NFR and per `knowledge_gap`:
   ```yaml
   decisions:
     - decision_id: "D-infer-nfr-{class}-{nnn}"
       decision_type: "nfr-inference | knowledge-gap-declaration | anchor-binding"
       tier: 1 | 2 | 3
       grounding_source:
         kind: "scan_index_path | kb_path | none"
         ref: "scan-index.json#/<jsonpointer> | {kb file path} | null"
       recommendation: "{the inferred target + delivery mechanism + verification}"
       alternatives_considered:
         - alt: "{alternative interpretation of the signal}"
           why_not: "{why the inferred interpretation was chosen}"
       confidence: "high | medium | low"
   ```

8. **Write primary artifact.** YAML at `output_path`. See Output below.

9. **Write resolution trace** per `core/components/memory/standards/rules/resolution.md` schema to `resolution_trace_path`.

10. **Self-validation.**
    - Every primary NFR has non-empty `delivery_mechanism.ref` AND `verification_method.tool`. Missing either → demote to `knowledge_gaps`; do not emit as primary.
    - Every NFR with no signals is in `knowledge_gaps`, not invented as a target.
    - Every primary NFR has at least one `evidence` path that resolves in scan-index.
    - Decision manifest has one entry per primary NFR and per knowledge_gap.

## Output

Primary artifact at `output_path`:

```yaml
meta:
  source_type: "inferred_from_code"
  evidence:
    - "scan-index.json#/manifests"
    - "scan-index.json#/patterns/framework_idioms"
    - "scan-index.json#/config_files"
    - "scan-index.json#/entry_points"
    - "scan-index.json#/docs"
  confidence: "high" | "medium" | "low"
  learning_category: "quality"
  sub_category: "performance"
  tier: 1
  related_proposal_paths:
    quality_profile_path: <echoed>
    physical_architecture_path: <echoed>
    logical_architecture_path: <echoed>
  scan_status_warning: null

nfr_spec:
  performance:
    - id: "nfr-perf-001"
      stated_target: "p95 latency < 500ms enforced via 100 req/min rate limit"
      delivery_mechanism:
        type: "middleware"
        ref: "express-rate-limit@7.x at src/server/app.ts (gateway layer)"
        anchor: "logical-architecture:comp-api-gateway"
        anchor_status: "bound"
      verification_method:
        type: "load_test"
        tool: "k6 (found in manifests)"
        scenario: "ramp to 150 VU; assert p95 ≤ 500ms and rate-limiter rejects excess"
      evidence:
        - "scan-index.json#/manifests/package.json/dependencies/express-rate-limit"
        - "scan-index.json#/patterns/framework_idioms/rateLimit"
      confidence: "high"
  reliability: [...]
  security: [...]
  scalability: [...]
  observability: [...]
  availability: [...]

knowledge_gaps:
  - nfr_class: "availability"
    reason: "no SLO markers in docs, no multi-region config in config_files, no synthetic monitors detected"
    scanned_paths:
      - "scan-index.json#/docs"
      - "scan-index.json#/config_files"
    checkpoint_question: "Is availability an explicit NFR for this product? If yes, what is the target uptime and where is it enforced?"
```

Decision manifest at `decision_manifest_path` (schema above).

Resolution trace at `resolution_trace_path` per resolution.md schema.

No product LTM writes. All output is under STM.

## Failure Modes

- `scan_index_missing` — `scan_index_path` does not exist or is not valid JSON.
- `missing_related_proposal` — any path in `related_proposal_paths` does not exist or is not valid YAML. Return the offending path; the orchestrator ensures /codify sequences proposals correctly.
- `insufficient_signal` — every NFR class returned zero signals. Proceed with an empty `nfr_spec` and every class recorded in `knowledge_gaps`; set `meta.confidence: low` and `scan_status_warning: "no NFR signals detected — all classes deferred to user at checkpoint"`. Do NOT fabricate.
- `ltm_resolution_failed` — Resolution Protocol raised an error; halt and return the trace path for triage.
- `output_parent_missing` — `output_path` parent cannot be created; return structured failure.

## Boundaries

- Read-only against the codebase. The scan-index and the three related proposals are the sole inputs — this skill does NOT open source files directly.
- Signals not listed in step 4 MUST NOT be invented. If scan-index lacks a signal for an NFR class, that class is a `knowledge_gap`, not an invented target.
- No writes outside `{stm_base}/{issue}/evidence/codify/proposals/architecture/` and the companion files (decision manifest, resolution trace).
- Never emit a primary NFR without BOTH a named `delivery_mechanism.ref` AND a named `verification_method.tool`. Ambiguity is a `knowledge_gap`, not a guess.
- Never tag an NFR `confidence: high` unless a primary signal AND a verification signal are both present in scan-index.
