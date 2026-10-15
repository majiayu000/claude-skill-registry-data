---
name: derive-quality-vision
description: Read quality-profile, nfr-spec, logical architecture, and physical architecture to produce quality-vision.yaml — a vision statement plus per-ISO-25010-characteristic entries carrying vision narrative, target level, design linkage, concrete named tooling, quantified thresholds, and lifecycle gates. Merges and extends the prior quality-standards artifact.
version: 0.1.0
user-invocable: false
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# derive-quality-vision

> **DEPRECATED for /arch (#403).** This skill is no longer part of the /arch pipeline. quality-vision is no longer a separate artifact — its work is folded into the refined quality-profile produced by `refine-quality-profile`. The refined QP carries every relevant ISO 25010 characteristic; delivery mechanisms live in physical-architecture's `nfr_delivery[]` blocks. This file is retained because `/codify` still references the quality-vision artifact shape through `infer-quality-vision-from-code`; aligning /codify with the new /arch contract is a separate follow-on. Do NOT invoke this skill in new /arch runs.

> **Defect 23 — Decision Surfacing Discipline (DSD):** This skill emits a `decision-manifest-derive-quality-vision.yaml` alongside its primary artifact. Every inferred decision produced during execution is recorded in the manifest with tier, grounding source, recommendation, and alternatives. The orchestrator drives the tiered surfacing flow after this skill completes.

Called by `tech-designer` during `arch` Stage 4. Produces `quality-vision.yaml` at `{product_base}architecture/quality-vision.yaml`.

## Purpose

Quality vision is the merged successor to the prior `quality-standards.yaml`. It adds the "why we care" narrative (the vision) to the existing "how CI will catch it" enforcement section. The output answers two questions per ISO 25010 characteristic: (1) What does quality mean for this product in this characteristic? (2) Exactly how does the architecture, the tooling, and the CI pipeline deliver and enforce it? Vague language ("use a linter", "test thoroughly") is a blocking failure (F8).

## Input

Receive from the tech-designer agent. All paths resolve against `{product_base}` supplied by the play via JSON contract.

- `quality_profile_path` (path, required) — `{product_base}specification/quality-profile.yaml`
- `nfr_spec_path` (path, required) — `{product_base}architecture/nfr-spec.yaml` (NFR entries carry delivery mechanisms and verification methods that feed into design_linkage and tooling)
- `logical_architecture_path` (path, required) — `{product_base}architecture/logical-architecture.yaml` (component IDs for design_linkage)
- `physical_architecture_path` (path, required) — `{product_base}architecture/physical-architecture.yaml` (stack picks for tooling selection)
- `project_profile_path` (path, required) — `{product_base}user-provided/project-profile.yaml` (QP dimensions: QP-1 through QP-11 + team profile)
- `ltm_quality_path` (path, required) — `{ltm_base}knowledge/quality/` (per-QP-dimension standard sets at each level)
- `output_path` (string, required) — `{product_base}architecture/quality-vision.yaml`
- `decision_manifest_path` (path, required) — `{product_base}architecture/decision-manifest-derive-quality-vision.yaml`

## Process

### 1. Read inputs

- Parse `quality-profile.yaml` → each ISO 25010 characteristic with `relevance`, `target`, and `rationale`. Build a list of characteristics with `relevance != not_applicable` — these all require entries in the output.
- Parse `nfr-spec.yaml` → NFR entries grouped by `characteristic`. These are the concrete delivery mechanisms and verification methods already decided — use them as the primary source for `design_linkage` and `tooling` fields.
- Parse `logical-architecture.yaml` → component IDs and responsibilities (for design_linkage component references).
- Parse `physical-architecture.yaml` → stack picks (frontend, backend, data stores, observability, auth_infra, library_pins) — tooling is derived from these.
- Parse `project-profile.yaml` → QP dimensions (QP-1 Testing Depth, QP-2 Code Review, QP-3 Documentation, QP-4 CI/CD, QP-5 Observability, QP-6 Accessibility, QP-7 Security Testing, QP-8 Performance Testing, QP-9 Privacy, QP-10 Data Quality, QP-11 Tech Debt Governance) for selecting tooling level.
- Read `{ltm_quality_path}/_index.md` and the relevant per-dimension files for the QP levels declared in the project profile. LTM is the primary source for tooling standards at each level.

### 2. Validate pre-conditions

- Confirm `quality-profile.yaml` has at least one characteristic with `relevance != not_applicable`. Zero → structured failure with `what_failed: empty_quality_profile`.
- Confirm `nfr-spec.yaml` is present. Missing → structured failure with `what_failed: missing_nfr_spec`. NFR spec must precede quality vision — design_linkage cites NFR IDs.
- Confirm `physical-architecture.yaml` is present. Missing → structured failure with `what_failed: missing_physical_architecture`.

### 3. Enumerate characteristic entries

Build the complete list of ISO 25010 characteristics to cover. Every characteristic from `quality-profile.yaml` with `relevance != not_applicable` is mandatory. Characteristics with `relevance = not_applicable` are explicitly excluded and noted:

```yaml
excluded_characteristics:
  - characteristic: portability
    reason: "quality-profile.portability.relevance = not_applicable — single-platform product"
```

For each mandatory characteristic, enumerate the decisions needed:
- **Vision synthesis**: what narrative statement explains why this characteristic matters for this product
- **Target level**: quantified (numeric, percentage, named standard) — echoed from quality-profile or adjusted
- **Design linkage**: which components and NFR entries deliver it
- **Tooling**: specific named tools with versions from the stack
- **Thresholds**: numeric gates (e.g., "80% coverage", "p95 ≤ 500ms", "zero critical vulnerabilities")
- **Lifecycle gates**: when CI / code review / monitoring enforces the threshold

Each of these fields except "echoed target" is an inferred decision — record in manifest.

### 4. For each characteristic: derive vision entry

**Step 4a. Vision narrative.** Write a 2-5 sentence narrative that explains why this characteristic is important for this specific product. Draw from:
- The quality-profile `rationale` field for this characteristic
- The product's epic success scenarios that depend on this characteristic
- The business risk of failing this characteristic (from epic failure scenarios)

**Step 4b. Target level.** Echo the intake target from quality-profile. If nfr-spec.yaml has adjusted the target for any NFR under this characteristic, note the adjustment and cite the NFR ID.

**Step 4c. Design linkage.** Identify which architectural elements deliver this characteristic:
- Logical component IDs from `logical-architecture.yaml` that are responsible
- NFR IDs from `nfr-spec.yaml` that address this characteristic
- Pattern references (forward-ref to design-patterns.yaml if applicable)

**Step 4d. Tooling.** Select specific named tools from the physical stack + LTM quality catalog at the declared QP level:
- Must use stack-consistent tooling (if backend is Node.js + TypeScript, don't prescribe pytest)
- Must name the tool and version (no "a linter", no "a test framework")
- Draw from `physical-architecture.yaml:library_pins` and `observability` for named products

**Step 4e. Thresholds.** Express every enforcement threshold as a measurable value:
- Coverage: "≥ 80% line coverage on new code"
- Performance: "p95 ≤ 500ms, p99 ≤ 1s at 100 concurrent users"
- Accessibility: "Lighthouse accessibility score ≥ 95; zero axe-core critical violations"
- Security: "Zero critical severity findings in SAST; zero known CVEs in production dependencies"

**Step 4f. Lifecycle gates.** State where and when each threshold is enforced:
- pre-commit hook, PR CI gate (blocking), nightly CI gate, pre-deploy gate, periodic audit
- Name the tool and the stage for each gate

### 5. Derive quality-vision.yaml

**vision_statement** — top-level narrative across all relevant characteristics:
```yaml
vision_statement: >
  {A 3-5 sentence statement that synthesizes the quality direction for this product.
  Names the two or three most critical ISO 25010 characteristics for this product and why,
  and commits to how the architecture ensures they are delivered and enforced throughout
  the development lifecycle.}
```

**characteristics** — one entry per relevant ISO 25010 characteristic:
```yaml
characteristics:
  - characteristic: performance_efficiency
    relevance: high      # echoed from quality-profile
    vision: >
      Users of this product are time-sensitive — checkout abandonment spikes when
      latency exceeds 800ms (EPIC-commerce-catalog failure scenario). Performance
      efficiency is the primary technical constraint that drove stack selection
      (SSR, edge caching, connection pooling) and must be continuously enforced
      to avoid silent regressions as feature count grows.
    target_level: "p95 API response ≤ 500ms; p95 page load ≤ 1.5s (Lighthouse LCP)"
    design_linkage:
      components: [comp-auth-service, comp-api-gateway]
      nfrs: [NFR-001]
      patterns: []  # populated when derive-design-patterns runs
    tooling:
      - name: "k6 OSS"
        version: "0.49.x"
        purpose: "API load testing — 100 VU ramp, p95 assertion"
        install_via: "npm"
      - name: "Lighthouse CI"
        version: "12.x"
        purpose: "Page load performance via LCP / FCP / CLS metrics"
        install_via: "npm"
    thresholds:
      - "API p95 response ≤ 500ms at 100 concurrent users"
      - "Page LCP ≤ 1.5s on simulated 4G (Lighthouse score ≥ 90 performance)"
      - "p99 API response ≤ 1500ms (hard failure threshold)"
    lifecycle_gates:
      - gate: "CI gate — blocking on PR to main"
        tool: "k6 in CI"
        threshold: "p95 ≤ 500ms"
      - gate: "CI gate — blocking on PR to main"
        tool: "Lighthouse CI"
        threshold: "LCP ≤ 1.5s; performance score ≥ 90"
      - gate: "Nightly regression"
        tool: "k6 scheduled job"
        threshold: "p99 ≤ 1500ms"

  - characteristic: security
    relevance: critical
    vision: >
      This product handles PII, payment data, and session credentials. A security
      failure is both a regulatory risk (GDPR, PCI DSS) and a trust-destroying event.
      Security must be enforced at every layer: static analysis catches code-level
      vulnerabilities, dependency scanning prevents supply-chain attacks, and runtime
      auth infra enforces AAL2 MFA for every account.
    target_level: "NIST 800-63B AAL2; zero OWASP Top 10 findings; PCI DSS scope minimized"
    design_linkage:
      components: [comp-auth-service, comp-mfa-handler]
      nfrs: [NFR-003]
      patterns: []
    tooling:
      - name: "Semgrep OSS"
        version: "1.x"
        purpose: "SAST — custom rules for auth bypass and injection patterns"
        install_via: "pip"
      - name: "npm audit"
        version: "bundled with Node.js 22"
        purpose: "Dependency vulnerability scanning"
      - name: "OWASP ZAP"
        version: "2.14.x"
        purpose: "DAST on staging environment weekly"
      - name: "Gitleaks"
        version: "8.x"
        purpose: "Secret scanning on every commit"
        install_via: "homebrew / CI plugin"
    thresholds:
      - "Zero critical or high severity SAST findings on PR (Semgrep)"
      - "Zero known CVEs in production dependencies (npm audit)"
      - "Zero secrets committed to repository (Gitleaks)"
      - "OWASP ZAP DAST: zero high-risk findings on staging"
    lifecycle_gates:
      - gate: "CI gate — blocking on PR"
        tool: "Semgrep OSS"
        threshold: "zero critical/high findings"
      - gate: "CI gate — blocking on PR"
        tool: "npm audit"
        threshold: "zero critical CVEs"
      - gate: "Pre-commit hook"
        tool: "Gitleaks"
        threshold: "zero secrets"
      - gate: "Weekly scheduled CI"
        tool: "OWASP ZAP"
        threshold: "zero high-risk findings on staging"

  - characteristic: maintainability
    relevance: high
    vision: >
      A team of 4 will evolve this product over multiple release cycles. Without
      enforced modularity, code quality degrades faster than features accumulate.
      Maintainability gates ensure that the bounded context boundaries defined in
      logical-architecture.yaml are not silently eroded by cross-context imports,
      and that coverage and complexity thresholds keep the codebase navigable.
    target_level: "Modular: zero cross-context imports; ≥ 80% line coverage new code; max cyclomatic complexity 10"
    design_linkage:
      components: [comp-auth-service, comp-api-gateway]
      nfrs: [NFR-004]
      patterns: []
    tooling:
      - name: "ESLint 8"
        version: "8.x"
        purpose: "Linting with Airbnb + import/no-restricted-paths for cross-context boundary enforcement"
        install_via: "npm"
      - name: "dependency-cruiser"
        version: "16.x"
        purpose: "Import graph validation against bounded context rules"
        install_via: "npm"
      - name: "Jest 29"
        version: "29.x"
        purpose: "Unit testing + coverage threshold enforcement"
        install_via: "npm"
      - name: "SonarCloud"
        version: "SaaS"
        purpose: "Cyclomatic complexity + cognitive complexity + code smell gates"
    thresholds:
      - "Zero cross-bounded-context imports (dependency-cruiser)"
      - "≥ 80% line coverage on new code (Jest)"
      - "≥ 60% line coverage on touched files"
      - "Cyclomatic complexity ≤ 10 per function (SonarCloud)"
      - "Zero new code smells of severity ≥ Major (SonarCloud)"
    lifecycle_gates:
      - gate: "CI gate — blocking on PR"
        tool: "ESLint + dependency-cruiser"
        threshold: "zero cross-context imports; zero lint errors"
      - gate: "CI gate — blocking on PR"
        tool: "Jest coverage"
        threshold: "≥ 80% line coverage new code"
      - gate: "CI gate — blocking on PR merge to main"
        tool: "SonarCloud quality gate"
        threshold: "zero new majors; cyclomatic complexity ≤ 10"
```

### 6. Emit decision manifest

Write `decision-manifest-derive-quality-vision.yaml` to `{decision_manifest_path}` BEFORE writing the primary artifact.

**Decisions to record** (decision_id prefix: `D-dqv-`):

These decisions carry forward from the prior `derive-quality-standards` skill's `D-dqs-` decision set, renumbered to `D-dqv-`, and extended with vision-specific decisions:

| decision_id | decision_type | What is being decided |
|-------------|---------------|-----------------------|
| `D-dqv-001` | `tooling-variant-pick` | When multiple tooling options are listed in LTM for the same QP dimension and level (e.g., Jest vs Vitest, Semgrep vs SonarCloud SAST), which is selected and why |
| `D-dqv-002` | `threshold-adjustment` | When an LTM baseline threshold is adjusted based on project profile risk appetite or epic failure scenarios (e.g., "≥80% line coverage" vs "≥75%"), the adjusted value and the driver |
| `D-dqv-003` | `enforcement-venue-selection` | For each gate, whether enforcement is "CI gate (blocking)", "CI gate (non-blocking)", "pre-commit hook", or "periodic audit" — and what drove the choice |
| `D-dqv-004` | `iso-25010-mapping` | How each standard is mapped to a specific ISO 25010 characteristic (e.g., "k6 load test → performance_efficiency") |
| `D-dqv-005` | `gap-finalization` | For each ISO 25010 characteristic from the quality profile, whether the standard set covers it completely or a gap exists, and the gap description if present |
| `D-dqv-006` | `vision-narrative-synthesis` | For each characteristic, the framing of the vision narrative — which driver (business risk, compliance mandate, user experience impact) is the lead sentence |
| `D-dqv-007` | `design-linkage-mapping` | How each characteristic is connected to specific logical components, NFR entries, and anticipated patterns — when the mapping requires reasoning rather than direct echo |

```yaml
schema_version: "1.0"
skill: "derive-quality-vision"
generated_at: "{ISO8601}"
decisions:
  - decision_id: "D-dqv-001"
    decision_type: "tooling-variant-pick"
    tier: high | mid | low
    grounding_source:
      kind: kb_path | web_citation | none
      ref: "{KB file path | URL | null}"
      excerpt: "{optional short quote when kind=kb_path}"
    recommendation: "{the tooling variant selected and the QP dimension it serves}"
    alternatives_considered:
      - alt: "{alternative tooling variant}"
        why_not: "{one-line dismissal reason}"
    agent_reasoning_summary: "{2-3 sentence explanation}"
    user_response: null
    user_response_detail: null
  # ... one entry per decision type, with additional entries per individual decision instance
```

### 7. Write primary artifact

Write `quality-vision.yaml` to `{output_path}`:

```yaml
slug: "<from project_profile.name>"
status: DRAFT
created_at: "<ISO-8601>"
play: arch
skill: derive-quality-vision
upstream_artifacts:
  quality_profile_path: <echoed>
  nfr_spec_path: <echoed>
  logical_architecture_path: <echoed>
  physical_architecture_path: <echoed>
vision_statement: >
  ...
characteristics: [...]
excluded_characteristics: [...]
tooling_summary:
  - name: "Jest 29"
    purpose: "unit testing and coverage"
    install_via: "npm"
  - ...
```

### 8. Self-validation against constraints

Before returning:
- C7/F7: verify every characteristic from `quality-profile.yaml` with `relevance != not_applicable` has an entry in `characteristics`. Any missing characteristic → structured failure with `what_failed: F7_orphan_characteristic` and the characteristic name.
- C7/F7: verify every entry has ALL required fields populated: `vision`, `target_level`, `design_linkage`, `tooling` (non-empty list), `thresholds` (non-empty list), `lifecycle_gates` (non-empty list). Any empty field → structured failure with `what_failed: F7_incomplete_entry`.
- C8/F8: scan every `tooling` entry for vague language patterns: "a linter", "a test framework", "some monitoring tool", "thoroughly", "regularly". If any vague phrase found → structured failure with `what_failed: F8_vague_tooling` and the offending entry.
- C8/F8: scan every `thresholds` entry for non-quantified language: "good performance", "high coverage", "secure enough". If any non-quantified threshold found → structured failure with `what_failed: F8_vague_threshold`.
- F19: verify manifest has entries for all inferred decisions with tier, grounding_source, recommendation, and alternatives_considered populated.

### 9. Return output contract

```yaml
quality_vision:
  path: <written path>
  vision_statement_present: true
  characteristics_covered: <int>
  characteristics_excluded: <int>
  total_profile_characteristics: <int>   # covered + excluded must equal this
  entries_with_complete_fields: <int>    # must equal characteristics_covered
  vague_language_violations: 0          # must be 0 — any > 0 triggers F8
  tooling_items_total: <int>
  lifecycle_gates_total: <int>
decision_manifest:
  path: <written path>
  decisions_recorded: <int>
```

## Outputs

```yaml
outputs:
  - path: "{product_base}architecture/quality-vision.yaml"
    required: true
  - path: "{product_base}architecture/decision-manifest-derive-quality-vision.yaml"
    required: true
```

## Constraints

- NEVER skip a relevant ISO 25010 characteristic. Every characteristic from the quality profile with `relevance != not_applicable` must have an entry. Orphan characteristics are F7 violations.
- NEVER use vague language. "Use a linter" is invalid; "ESLint 8 with Airbnb config + import/no-restricted-paths" is valid. "Test thoroughly" is invalid; "Jest 29 with ≥80% line coverage on new code, CI blocking gate on PR" is valid. This is F8.
- NEVER omit `enforcement` / `lifecycle_gates`. Standards without gates are aspirations, not architecture.
- NEVER propose tooling that contradicts the physical stack. If the backend is Node.js + TypeScript, do not prescribe pytest or coverage.py.
- ALWAYS include `design_linkage` per entry — this is the merge contribution that separates quality-vision from quality-standards. Every characteristic must trace to at least one component or NFR ID.
- ALWAYS include `drivers` for security-critical and performance-critical entries — auditors expect to trace from standard to business requirement.
- ALWAYS write the manifest before writing the primary artifact.
- NEVER commit an inferred decision to quality-vision.yaml without recording it in the decision manifest first.
- NEVER tag a decision `tier: high` unless the `grounding_source.kind` is `kb_path` AND the referenced KB file exists.
- ALWAYS include `alternatives_considered` with at least one entry per decision. If genuinely no alternative, state "none — only candidate" explicitly.
- NEVER emit `source_type: agent_default_unilateral`.
- Read LTM quality knowledge first for tooling standards at each QP level. Use the declared QP dimensions from project-profile.yaml to select the appropriate standard level.

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
| Related | `core/components/agents/tech-designer.md`, `core/components/skills/derive-nfr-spec`, `core/components/memory/knowledge/quality/` |
