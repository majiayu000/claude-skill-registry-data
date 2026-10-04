---
name: derive-nfr-spec
description: Read the upstream quality profile, intent epics constraints block, and physical architecture to produce nfr-spec.yaml — a per-NFR contract that re-states intake targets, records any agent adjustments with rationale, and for every NFR names the specific architectural mechanism that delivers it plus the verification method.
version: 0.1.0
user-invocable: false
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# derive-nfr-spec

> **DEPRECATED for /arch (#403).** This skill is no longer part of the /arch pipeline. nfr-spec is no longer a separate artifact — NFR targets are described in the refined quality-profile produced by `refine-quality-profile`, and NFR delivery mechanisms live in `physical-architecture.yaml.components[].nfr_delivery[]` produced by `derive-physical-architecture`. This file is retained because `/codify` still references the nfr-spec artifact shape through `infer-nfr-spec-from-code`; aligning /codify with the new /arch contract is a separate follow-on. Do NOT invoke this skill in new /arch runs.

> **Defect 23 — Decision Surfacing Discipline (DSD):** This skill emits a `decision-manifest-derive-nfr-spec.yaml` alongside its primary artifact. Every inferred decision produced during execution is recorded in the manifest with tier, grounding source, recommendation, and alternatives. The orchestrator drives the tiered surfacing flow after this skill completes.

Called by `tech-designer` during `arch` Stage 3. Produces `nfr-spec.yaml` at `{product_base}architecture/nfr-spec.yaml`.

## Purpose

Translate the upstream quality profile's ISO 25010 targets and epic performance constraints into a contract that names — for every NFR — the exact architectural mechanism that delivers it. An NFR without a delivery mechanism is a blocking failure (F6). Every intake target is either preserved verbatim or adjusted with documented rationale, and every adjustment is a decision recorded in the manifest.

## Input

Receive from the tech-designer agent. All paths resolve against `{product_base}` supplied by the play via JSON contract.

- `quality_profile_path` (path, required) — `{product_base}specification/quality-profile.yaml`
- `epics_dir` (path, required) — `{product_base}scope/epics/` (the `constraints` block of each epic surfaces performance, security, and reliability requirements not already in the quality profile)
- `logical_architecture_path` (path, required) — `{product_base}architecture/logical-architecture.yaml` (component IDs are the anchor for delivery_mechanism references)
- `physical_architecture_path` (path, required) — `{product_base}architecture/physical-architecture.yaml` (stack picks, data stores, observability, auth infra — these are the delivery mechanisms)
- `project_profile_path` (path, required) — `{product_base}user-provided/project-profile.yaml` (compliance flags, security level, budget sensitivity)
- `output_path` (string, required) — `{product_base}architecture/nfr-spec.yaml`
- `decision_manifest_path` (path, required) — `{product_base}architecture/decision-manifest-derive-nfr-spec.yaml`

## Process

### 1. Read inputs

- Parse `quality-profile.yaml` → each ISO 25010 characteristic entry with `relevance`, `target` (quantified), and `rationale`.
- Glob `{epics_dir}/*.yaml` → per-epic `constraints` blocks; extract any performance targets, rate limits, latency budgets, retry policies, or data retention rules stated as constraints.
- Parse `logical-architecture.yaml` → component list (IDs, names, responsibilities) for forward-referencing delivery mechanisms.
- Parse `physical-architecture.yaml` → data stores, cache, queue, observability, auth_infra, scaling_strategy, deployment_topology, library_pins. These are the named delivery mechanisms.
- Parse `project-profile.yaml` → compliance flags, security level, budget sensitivity, any explicit NFR overrides in the profile.

### 2. Validate pre-conditions

- Confirm `quality-profile.yaml` has at least one characteristic entry with `relevance != not_applicable`. Zero relevant characteristics → structured failure with `what_failed: empty_quality_profile`.
- Confirm `physical-architecture.yaml` is present and has non-empty `data_stores`, `observability`, and `auth_infra` sections. Missing physical architecture → structured failure with `what_failed: missing_physical_architecture`. Physical must exist before NFR spec because delivery mechanisms must reference real stack components.
- Confirm `logical-architecture.yaml` is present with a non-empty `components` section. Missing → structured failure with `what_failed: missing_logical_architecture`.

### 3. Enumerate NFR entries

Build the complete NFR list from two sources:

**Source A: quality-profile.yaml characteristics** — for each characteristic with `relevance != not_applicable`, extract the `target` field as the intake statement. One NFR entry per characteristic target. If a characteristic has multiple sub-targets (e.g., performance_efficiency has p95 and p99 targets), create one NFR entry per quantified target.

**Source B: epic constraints blocks** — glob all epic YAML files and parse each `constraints` section. Extract any constraint that is a measurable non-functional requirement (latency, throughput, error rate, retention, uptime, security control). For each such constraint not already covered by Source A, create an additional NFR entry.

Deduplicate: if the same target appears in both sources, create one NFR entry with both sources cited.

### 4. For each NFR entry: determine delivery mechanism and verification

For every NFR entry:

**Step 4a. Identify delivery mechanism.** Search `physical-architecture.yaml` for a component, product, or configuration that delivers the NFR:
- Performance latency targets → cache (Redis), CDN, read replica, or specific query optimization at comp-ID
- Availability targets → scaling strategy, load balancing, multi-region configuration
- Security targets → auth_infra product, specific library pin, SAST tool configured in CI
- Reliability targets → queue (retry policy), circuit breaker, health check endpoint
- Observability requirements → observability stack products
- Data retention / compliance → specific data store configuration, backup policy

If the delivery mechanism exists in `physical-architecture.yaml` or `logical-architecture.yaml`, cite it by ID. If the mechanism is expected to come from `design-patterns.yaml` (e.g., retry policy, circuit breaker, outbox pattern) but that file does not exist yet — this is intentional. Mark the delivery_mechanism as a **forward reference** with `status: forward_ref_pending_design_patterns` and `expected_pattern: {pattern type}`. The orchestrator resolves forward references after `derive-design-patterns` completes. A forward reference is NOT a failure — it is an explicit dependency declaration.

**Step 4b. Determine if adjustment is needed.** Compare the intake target against the physical architecture's actual capability. If the intake target is unreachable given the chosen stack (e.g., p95 < 50ms with a geographically single-region deployment and no CDN), adjust the target with documented rationale. Adjustments are inferred decisions — record in manifest.

**Step 4c. Assign verification method.** Map each NFR to a test type, monitoring metric, or lint rule:
- Performance → load test (k6, Playwright perf assertions), APM dashboard alert
- Availability → synthetic monitor, uptime alert threshold
- Security → SAST scan, dependency audit, penetration test scope
- Accessibility → axe-core in CI, Lighthouse CI accessibility score gate
- Data integrity → database constraint check, data validation test
- Code quality → linter rule, coverage threshold, complexity gate

### 5. Assemble nfr-spec.yaml

One entry per NFR:

```yaml
nfrs:
  - id: NFR-001
    characteristic: performance_efficiency
    iso_25010_sub: time_behaviour
    statement: "p95 response time for authenticated API requests must not exceed 500ms under normal load"
    target: "p95 ≤ 500ms at ≤ 100 concurrent users"
    source: "quality-profile.performance_efficiency.target + EPIC-user-login-001 constraints.performance"
    adjustment: null   # null means intake target is preserved as-is
    delivery_mechanism:
      type: stack_component
      ref: "physical-architecture.yaml:cache (Redis 7 via Upstash) + data_stores[ds-primary]:read_replica"
      description: "Session cache serves hot-path reads without DB round-trips; read replica offloads reporting queries"
      status: confirmed  # confirmed | forward_ref_pending_design_patterns
    verification_method:
      type: load_test
      tool: "k6 OSS"
      scenario: "100 VU ramp over 5 minutes; assert p95 ≤ 500ms on /api/auth/* and /api/orders/*"
      gate: "CI gate (blocking on main-branch merge)"

  - id: NFR-002
    characteristic: reliability
    iso_25010_sub: availability
    statement: "Production environment must sustain ≥99.5% monthly uptime excluding planned maintenance"
    target: "monthly uptime ≥ 99.5%"
    source: "quality-profile.reliability.target"
    adjustment:
      adjusted_target: "99.5% — down from 99.9% stated in brief"
      rationale: "physical-architecture.yaml:platform_hosts.backend = Railway (single-region); 99.9% requires multi-region active-active which exceeds budget_sensitivity=medium and team_size=4 ops capacity. ADR required."
      driver: "project-profile.budget_sensitivity=medium + team_size=4"
    delivery_mechanism:
      type: scaling_strategy
      ref: "physical-architecture.yaml:scaling_strategy.api + deployment_topology.environments.production"
      description: "Railway autoscale to 3 replicas with health check restart policy; synthetic uptime monitor with PagerDuty alert"
      status: confirmed
    verification_method:
      type: synthetic_monitor
      tool: "BetterUptime + Grafana synthetic"
      scenario: "Ping /healthz every 60 seconds from 2 regions; alert if 3 consecutive failures"
      gate: "On-call alert (non-blocking in CI; operational SLA enforced at deploy)"

  - id: NFR-003
    characteristic: security
    iso_25010_sub: integrity
    statement: "All credential handling must conform to NIST 800-63B AAL2"
    target: "Zero AAL2 violations in security audit; MFA required for all accounts"
    source: "quality-profile.security.target + EPIC-user-login-001 CTC-001"
    adjustment: null
    delivery_mechanism:
      type: stack_component
      ref: "physical-architecture.yaml:auth_infra (NextAuth.js 5 + TOTP MFA)"
      description: "NextAuth.js enforces MFA challenge; TOTP via speakeasy satisfies AAL2 possession factor"
      status: confirmed
    verification_method:
      type: sast_and_penetration
      tool: "Semgrep OSS (SAST) + OWASP ZAP (DAST) + manual pen test before v1 launch"
      scenario: "SAST runs in CI on every PR; DAST runs on staging weekly; pen test scopes auth flows"
      gate: "CI gate SAST (blocking); DAST non-blocking; pen test pre-launch gate"

  - id: NFR-004
    characteristic: maintainability
    iso_25010_sub: modularity
    statement: "Each architectural component must be independently deployable without full-system redeployment"
    target: "Zero forced co-deployments between components in different bounded contexts"
    source: "quality-profile.maintainability.target"
    adjustment: null
    delivery_mechanism:
      type: pattern
      ref: "design-patterns.yaml:layer_level (expected: hexagonal or clean architecture)"
      description: "Hexagonal / ports-and-adapters pattern enforces component isolation; ports are the only cross-boundary interface"
      status: forward_ref_pending_design_patterns
      expected_pattern: "hexagonal"
    verification_method:
      type: dependency_analysis
      tool: "dependency-cruiser + ESLint import rules"
      scenario: "dependency-cruiser enforces no cross-context imports; ESLint import/no-restricted-paths applied per bounded context"
      gate: "CI gate (blocking on PR)"
```

### 6. Emit decision manifest

Write `decision-manifest-derive-nfr-spec.yaml` to `{decision_manifest_path}` BEFORE writing the primary artifact.

**Decisions to record** (decision_id prefix: `D-dnf-`):

| decision_id | decision_type | What is being decided |
|-------------|---------------|-----------------------|
| `D-dnf-001` | `nfr-intake-extraction` | Which quality-profile targets and epic constraints are selected as NFR entries, and how overlapping entries are deduplicated |
| `D-dnf-002` | `target-adjustment` | When an intake target is adjusted (e.g., 99.9% → 99.5%), the adjusted value, the stack constraint that forced it, and the rationale |
| `D-dnf-003` | `delivery-mechanism-assignment` | For each NFR, which physical component, stack product, or pattern is identified as the delivery mechanism — including forward references to design-patterns.yaml |
| `D-dnf-004` | `forward-reference-declaration` | For each NFR whose delivery mechanism is expected from design-patterns.yaml (not yet written), the forward ref is declared with expected_pattern — this is an explicit dependency, not a gap |
| `D-dnf-005` | `verification-method-selection` | The test type, tool, scenario, and gate assigned to each NFR; when multiple testing approaches are valid, which is selected and why |

```yaml
schema_version: "1.0"
skill: "derive-nfr-spec"
generated_at: "{ISO8601}"
decisions:
  - decision_id: "D-dnf-002"
    decision_type: "target-adjustment"
    tier: high | mid | low
    grounding_source:
      kind: kb_path | web_citation | none
      ref: "{KB file path | URL | null}"
      excerpt: "{optional short quote when kind=kb_path}"
    recommendation: "{the adjusted target and the rationale}"
    alternatives_considered:
      - alt: "{alternative: preserve original target}"
        why_not: "{why the original target cannot be met with the chosen stack}"
    agent_reasoning_summary: "{2-3 sentence explanation of the adjustment reasoning}"
    user_response: null
    user_response_detail: null
  # ... one entry per decision type, with additional entries per individual decision instance
```

### 7. Write primary artifact

Write `nfr-spec.yaml` to `{output_path}`:

```yaml
slug: "<from project_profile.name>"
status: DRAFT
created_at: "<ISO-8601>"
play: arch
skill: derive-nfr-spec
upstream_artifacts:
  quality_profile_path: <echoed>
  epics_dir: <echoed>
  physical_architecture_path: <echoed>
  logical_architecture_path: <echoed>
nfrs: [...]
forward_references:
  - nfr_id: NFR-004
    ref_type: design_patterns
    expected_pattern: hexagonal
    resolved: false
```

### 8. Self-validation against constraints

Before returning:
- C6/F6: verify every NFR entry has a non-empty `delivery_mechanism` field. `delivery_mechanism: null` or missing → structured failure with `what_failed: F6_missing_delivery_mechanism` and the NFR ID. Forward references with `status: forward_ref_pending_design_patterns` are acceptable — they are not null.
- F6 completeness: verify every performance constraint from any epic `constraints` block appears as an NFR entry. Any epic constraint not covered → structured failure with `what_failed: F6_uncovered_epic_constraint`.
- F19: verify manifest has entries for all inferred decisions with tier, grounding_source, recommendation, and alternatives_considered populated.

### 9. Return output contract

```yaml
nfr_spec:
  path: <written path>
  nfr_count: <int>
  nfrs_from_quality_profile: <int>
  nfrs_from_epics: <int>
  nfrs_with_adjustments: <int>
  nfrs_with_confirmed_mechanism: <int>
  nfrs_with_forward_ref: <int>
  nfrs_with_no_mechanism: 0     # must be 0 — any > 0 triggers F6
  forward_references:
    - nfr_id: <NFR-NNN>
      expected_pattern: <pattern name>
      resolved: false
decision_manifest:
  path: <written path>
  decisions_recorded: <int>
```

## Outputs

```yaml
outputs:
  - path: "{product_base}architecture/nfr-spec.yaml"
    required: true
  - path: "{product_base}architecture/decision-manifest-derive-nfr-spec.yaml"
    required: true
```

## Constraints

- NEVER emit an NFR without a `delivery_mechanism`. F6 is a blocking failure. If no confirmed mechanism exists yet, use a forward reference to design-patterns.yaml with `status: forward_ref_pending_design_patterns` — that is valid; null is not.
- NEVER adjust an intake target without documenting the rationale and the stack constraint that forced it. Adjustments are decisions; silent adjustments are F4 violations.
- NEVER skip a performance constraint from an epic's `constraints` block. Every measurable non-functional requirement in epics must appear as an NFR entry.
- NEVER skip a relevant ISO 25010 characteristic from the quality profile. Every characteristic with `relevance != not_applicable` must have at least one NFR entry.
- ALWAYS cite the delivery mechanism by its ID from physical-architecture.yaml or logical-architecture.yaml, not by a category term.
- ALWAYS include a `verification_method` with a named tool, scenario, and gate for every NFR. "Test it" is invalid; "k6 load test with 100 VU, p95 assert, CI blocking gate" is valid.
- ALWAYS write the manifest before writing the primary artifact.
- NEVER commit an inferred decision to nfr-spec.yaml without recording it in the decision manifest first.
- NEVER tag a decision `tier: high` unless the `grounding_source.kind` is `kb_path` AND the referenced KB file exists.
- ALWAYS include `alternatives_considered` with at least one entry per decision. If genuinely no alternative, state "none — only candidate" explicitly.
- NEVER emit `source_type: agent_default_unilateral`.

## DSD Compliance (C18/C19)

This skill emits a decision manifest alongside its primary artifact. Every inferred decision
(not user-provided input) lands in the manifest with tier, grounding_source, recommendation,
alternatives_considered, and user_response=null. The orchestrator walks the manifest after
this skill completes and drives the tiered surfacing flow before downstream skills read the
primary artifact. A manifest-free emission is a structural violation (F19).

## Version

| Field | Value |
|-------|-------|
| Version | 0.1.0 |
| Category | architecture |
| Created | 2026-04-15 |
| Related | `core/components/agents/tech-designer.md`, `core/components/skills/derive-physical-architecture`, `core/components/skills/derive-quality-vision`, `core/components/skills/derive-design-patterns` |
