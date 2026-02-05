---
name: ci-gatekeeper-agent
description: >
  AI-powered CI Gatekeeper Agent that enforces observability standards in CI/CD pipelines.
  Use when: (1) Generating GitHub Actions/Jenkins pipelines for observability gates,
  (2) Configuring progressive enforcement policies,
  (3) Validating schema compatibility in CI,
  (4) Generating gate status reports.
  Triggers: "create observability gate", "configure CI enforcement",
  "generate gate policy", "check observability compliance".
---

# CI Gatekeeper Agent

The CI Gatekeeper enforces observability standards through CI pipeline checks, implementing progressive gating that converts optional adoption into migration readiness without organizational mandates.

## Core Responsibilities

1. **Gate Policy Management**: Define and enforce gate policies by tier
2. **CI Workflow Generation**: Create GitHub Actions/Jenkins pipelines
3. **Schema Validation**: Check schema compatibility against registry
4. **Status Reporting**: Report gate status to PRs and event bus
5. **Progressive Enforcement**: Manage warn → soft-fail → hard-fail transitions

## Gate Policies

### Gate 1: PR Merge (Pre-Merge)

**Trigger:** Pull Request opened/updated
**Requirements:**
- OTel SDK in dependencies
- Asset URN tags present
- Owner metadata defined
- RUNBOOK.md exists
- Lineage spec present (Tier-1)
- Contract stub present (Tier-1)

**Actions:**
| Tier | On Failure |
|------|------------|
| Tier-1 | Block merge |
| Tier-2+ | Warn only |

### Gate 2: Migration Cutover

**Trigger:** Migration deployment
**Requirements:**
- Signals live in prod (verified)
- Freshness/volume monitors configured
- On-call route established
- Blast radius queryable in Neptune

**Actions:**
| Tier | On Failure |
|------|------------|
| All | Block cutover |

### Gate 3: Post-Cutover (14 days)

**Trigger:** Stability review
**Requirements:**
- Schema change events wired
- Lineage edges present in Neptune
- DQ checks configured (2+ high-value)
- No critical incidents in window

**Actions:**
| Tier | On Failure |
|------|------------|
| Tier-1 | Leadership review |
| Tier-2+ | Warn only |

## GitHub Actions Workflow

Generate `.github/workflows/observability-gate.yaml`:

```yaml
name: Observability Gate
on: [pull_request]

jobs:
  gate-1-baseline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check OTel SDK
        id: otel-check
        run: |
          # Detect language and check appropriate dependency file
          if [ -f "pom.xml" ]; then
            grep -q "opentelemetry" pom.xml && echo "otel_present=true" >> $GITHUB_OUTPUT
          elif [ -f "go.mod" ]; then
            grep -q "opentelemetry" go.mod && echo "otel_present=true" >> $GITHUB_OUTPUT
          elif [ -f "requirements.txt" ]; then
            grep -q "opentelemetry" requirements.txt && echo "otel_present=true" >> $GITHUB_OUTPUT
          fi
          
      - name: Check Lineage Spec
        id: lineage-check
        run: |
          [ -d "lineage" ] && ls lineage/*.yaml && echo "lineage_present=true" >> $GITHUB_OUTPUT
          
      - name: Check Contract Stub
        id: contract-check
        run: |
          [ -d "contracts" ] && ls contracts/*.yaml && echo "contract_present=true" >> $GITHUB_OUTPUT
          
      - name: Check RUNBOOK
        id: runbook-check
        run: |
          [ -f "RUNBOOK.md" ] && echo "runbook_present=true" >> $GITHUB_OUTPUT
          
      - name: Enforce by Tier
        run: |
          TIER=$(yq '.service.tier' lineage/*.yaml 2>/dev/null || echo "2")
          if [ "$TIER" == "1" ]; then
            # Hard fail for Tier-1
            [ "${{ steps.otel-check.outputs.otel_present }}" == "true" ] || exit 1
            [ "${{ steps.lineage-check.outputs.lineage_present }}" == "true" ] || exit 1
          fi
```

## Schema Compatibility Check

```yaml
- name: Schema Compatibility
  run: |
    SCHEMAS=$(find . -name "*.avsc" -o -name "*.proto")
    for SCHEMA in $SCHEMAS; do
      SUBJECT=$(basename $SCHEMA .avsc)
      curl -X POST \
        -H "Content-Type: application/vnd.schemaregistry.v1+json" \
        --data "{\"schema\": \"$(cat $SCHEMA | jq -Rs .)\"}" \
        "$SCHEMA_REGISTRY_URL/compatibility/subjects/$SUBJECT-value/versions/latest"
    done
```

## Gate Status Event

Emit to event bus for tracking:

```json
{
  "event_type": "GateStatusReport",
  "timestamp": "2026-01-04T10:45:00Z",
  "repository": "orders-enricher",
  "pr_number": 142,
  "commit_sha": "abc123def",
  "gate": "gate-1",
  "status": "PASSED",
  "tier": 1,
  "checks": {
    "otel_sdk": {"status": "PASS", "details": "OTel 1.32.0 found"},
    "lineage_spec": {"status": "PASS", "details": "lineage/orders-enricher.yaml"},
    "contract_stub": {"status": "PASS", "details": "contracts/orders_enriched.yaml"},
    "schema_compat": {"status": "PASS", "details": "BACKWARD compatible"},
    "runbook": {"status": "PASS", "details": "RUNBOOK.md present"}
  },
  "next_gate": "gate-2",
  "next_gate_requirements": [
    "Signals live in prod for 7 days",
    "On-call route configured"
  ]
}
```

## Scripts

- `scripts/generate_workflow.py`: GitHub Actions generator
- `scripts/check_gate.py`: Local gate check runner
- `scripts/report_status.py`: Status reporter to PR and event bus

## References

- `references/gate-policies.md`: Complete gate policy definitions
- `references/workflow-templates/`: CI workflow templates
- `references/schema-registry.md`: Schema Registry integration guide

## Configuration

```yaml
ci_gatekeeper:
  enabled: true
  gate_1:
    enforce_tier_1: true
    enforce_tier_2: false  # Warn only
  gate_2:
    stability_window_days: 7
  gate_3:
    grace_period_days: 14
  schema_registry:
    url: "https://schema-registry.internal:8081"
  event_bus:
    topic: "autopilot-events"
```

## Integration Points

| System | Integration | Purpose |
|--------|-------------|---------|
| GitHub | Webhooks + API | PR events, status checks |
| GitLab | Webhooks + API | Alternative VCS support |
| Schema Registry | REST API | Compatibility validation |
| Event Bus | Kafka producer | Gate status events |
| Neptune | Gremlin API | Lineage edge verification |
