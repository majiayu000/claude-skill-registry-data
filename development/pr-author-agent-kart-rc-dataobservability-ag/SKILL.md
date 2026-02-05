---
name: pr-author-agent
description: >
  AI-powered PR Author Agent that transforms Observability Diff Plans into Pull Requests.
  Use when: (1) Generating instrumentation code from Scout Agent output,
  (2) Creating OTel configuration, correlation headers, lineage specs,
  (3) Scaffolding telemetry validation tests,
  (4) Creating GitHub/GitLab PRs with observability artifacts.
  Triggers: "generate PR from diff plan", "create instrumentation PR",
  "scaffold observability code", "generate OTel config", "create telemetry PR".
---

# PR Author Agent

The PR Author Agent transforms Observability Diff Plans (produced by Scout Agent) into complete Pull Requests containing instrumentation code, configuration, tests, and documentation. It operates as the code generation layer of the Instrumentation Autopilot system.

## Core Responsibilities

1. **Diff Plan Parsing**: Parse and validate Scout Agent output
2. **Template Selection**: Choose archetype-specific templates based on Diff Plan
3. **Code Generation**: Generate OTel interceptors, correlation headers, middleware
4. **Lineage Spec Creation**: Create YAML specs defining input/output data mappings
5. **Contract Stub Generation**: Create data contract definitions with SLOs
6. **Test Scaffolding**: Generate telemetry validation tests
7. **Runbook Generation**: Create operational runbooks from templates
8. **PR Creation**: Create GitHub/GitLab PR with all artifacts

## Workflow

Execute PR generation in this sequence:

### Step 1: Parse Diff Plan

Read the Observability Diff Plan JSON from Scout Agent:
- Extract `repo`, `archetypes`, `tech_stack`, `gaps`, `patch_plan`
- Validate plan against schema in `references/diff-plan-schema.md`
- Check confidence threshold (default >= 0.7)
- Reject low-confidence plans with appropriate error message

### Step 2: Select Templates

For each gap in the plan:
1. Match `gap.template` to template library in `references/templates/`
2. Determine language from `tech_stack.language`
3. Load template files for the specific archetype
4. Prepare variable context for interpolation

### Step 3: Generate Artifacts

For each template, generate:
- **Code files**: Interceptors, wrappers, middleware, handlers
- **Config files**: application.yaml, go.mod additions, pom.xml dependencies
- **Spec files**: lineage/*.yaml, contracts/*.yaml
- **Test files**: *_test.java, *_test.py, *_test.go
- **Docs**: RUNBOOK.md

### Step 4: Apply Patch Plan

Execute patch operations from the Diff Plan:
- `add_dependency`: Append dependencies to build files
- `merge_config`: Merge configuration into existing files
- `create_file`: Create new files with generated content
- `modify_file`: Apply targeted modifications to existing files

### Step 5: Create Pull Request

Using GitHub/GitLab API:
1. Create branch: `autopilot/observability-{repo}-{timestamp}`
2. Stage all generated and modified files
3. Create commit with structured message
4. Create PR with description from template
5. Apply labels: `autopilot`, `observability`, `{archetype}`
6. Request reviewers based on CODEOWNERS
7. Emit CloudEvent for downstream processing

## Template Library

Templates organized by language and archetype:

```
references/templates/
├── java/
│   ├── kafka-consumer-otel/
│   │   ├── OtelKafkaConsumerInterceptor.java.tmpl
│   │   ├── pom-dependency.xml.tmpl
│   │   └── application-config.yaml.tmpl
│   ├── kafka-producer-otel/
│   │   ├── OtelKafkaProducerInterceptor.java.tmpl
│   │   └── pom-dependency.xml.tmpl
│   ├── kafka-producer-headers/
│   │   ├── CorrelationHeaderInterceptor.java.tmpl
│   │   └── HeaderPropagator.java.tmpl
│   ├── spring-boot-otel/
│   │   ├── OtelAutoConfiguration.java.tmpl
│   │   └── application-otel.yaml.tmpl
│   └── grpc-otel/
│       ├── OtelGrpcServerInterceptor.java.tmpl
│       └── OtelGrpcClientInterceptor.java.tmpl
├── python/
│   ├── kafka-otel/
│   │   ├── otel_kafka_wrapper.py.tmpl
│   │   └── requirements-otel.txt.tmpl
│   ├── airflow-openlineage/
│   │   ├── openlineage_config.py.tmpl
│   │   └── dag_lineage_decorator.py.tmpl
│   └── spark-openlineage/
│       ├── spark_lineage_listener.py.tmpl
│       └── requirements-lineage.txt.tmpl
├── go/
│   ├── kafka-sarama-otel/
│   │   ├── otel_sarama_wrapper.go.tmpl
│   │   └── go-mod-dependency.txt.tmpl
│   ├── gin-otel/
│   │   ├── otel_gin_middleware.go.tmpl
│   │   └── go-mod-dependency.txt.tmpl
│   ├── echo-otel/
│   │   ├── otel_echo_middleware.go.tmpl
│   │   └── go-mod-dependency.txt.tmpl
│   ├── grpc-otel/
│   │   ├── otel_grpc_interceptor.go.tmpl
│   │   └── go-mod-dependency.txt.tmpl
│   └── chi-otel/
│       ├── otel_chi_middleware.go.tmpl
│       └── go-mod-dependency.txt.tmpl
└── common/
    ├── lineage-spec/
    │   ├── kafka-lineage.yaml.tmpl
    │   ├── spark-lineage.yaml.tmpl
    │   └── airflow-lineage.yaml.tmpl
    ├── contract-stub/
    │   ├── data-contract.yaml.tmpl
    │   └── slo-definition.yaml.tmpl
    ├── runbook/
    │   └── RUNBOOK.md.tmpl
    └── test/
        ├── telemetry_test.java.tmpl
        ├── telemetry_test.py.tmpl
        └── telemetry_test.go.tmpl
```

## Variable Interpolation

Templates use `${VAR}` syntax for variable substitution:

| Variable | Source | Example |
|----------|--------|---------|
| `${SERVICE_NAME}` | Diff Plan repo name | `orders-enricher` |
| `${SERVICE_URN}` | Computed from repo/namespace | `urn:svc:prod:commerce:orders-enricher` |
| `${NAMESPACE}` | Kubernetes namespace or project | `commerce` |
| `${INPUT_TOPIC}` | Detected from code analysis | `orders_raw` |
| `${OUTPUT_TOPIC}` | Detected from code analysis | `orders_enriched` |
| `${OWNER_TEAM}` | CODEOWNERS or default | `orders-team` |
| `${CONSUMER_GROUP}` | Detected from config | `orders-enricher-cg` |
| `${SCHEMA_ID}` | Schema Registry lookup | `orders.v3` |
| `${OTEL_VERSION}` | Latest stable or pinned | `1.32.0` |
| `${TIMESTAMP}` | Current ISO timestamp | `2026-01-04T10:30:00Z` |
| `${DIFF_PLAN_ID}` | Unique plan identifier | `dp-abc123` |
| `${CONFIDENCE}` | Diff Plan confidence score | `0.87` |

See `references/variable-mapping.md` for complete variable reference.

## PR Description Template

```markdown
## Autopilot: Observability Instrumentation

This PR was generated by the Instrumentation Autopilot to add observability
instrumentation to this repository based on Scout Agent analysis.

### Summary
- **Archetypes Detected**: ${ARCHETYPES}
- **Confidence Score**: ${CONFIDENCE}
- **Diff Plan ID**: ${DIFF_PLAN_ID}

### Changes
${CHANGES_LIST}

### Gaps Addressed
${GAPS_LIST}

### Files Modified
${FILES_LIST}

### Verification Checklist
- [ ] Code review approved by domain expert
- [ ] Unit tests passing
- [ ] Lineage spec reviewed for accuracy
- [ ] Contract SLOs appropriate for data tier
- [ ] RUNBOOK.md reviewed for operational accuracy

### Next Steps
After merge, the **Telemetry Validator** will automatically verify signals in staging.
Gate 1 checks will run as part of this PR's CI pipeline.

### Need Help?
- [Observability Runbook](./RUNBOOK.md)
- [Instrumentation Autopilot Docs](https://docs.internal/autopilot)
- Contact: #observability-support

---
*Generated by Instrumentation Autopilot v1.0*
*Scout Agent Scan: ${SCAN_TIMESTAMP}*
*PR Author: ${PR_TIMESTAMP}*
```

## Scripts

- `scripts/generate_pr.py`: Main PR generation orchestrator
- `scripts/template_engine.py`: Template interpolation and rendering engine
- `scripts/github_client.py`: GitHub REST API wrapper for PR creation
- `scripts/gitlab_client.py`: GitLab REST API wrapper for MR creation

## References

- `references/diff-plan-schema.md`: JSON schema for input Diff Plans (shared with Scout Agent)
- `references/pr-template.md`: PR/MR description template
- `references/variable-mapping.md`: Complete variable interpolation reference
- `references/templates/`: Archetype-specific code templates

## OpenSpec Integration

For Windsurf development:
- `assets/openspec/project.md`: Project context and conventions
- `assets/openspec/specs/pr-author-agent/spec.md`: PR Author Agent specification
- `assets/openspec/AGENTS.md`: Workflow instructions for AI assistants

Initialize OpenSpec: `openspec init` then select Windsurf integration.

## Windsurf Workflows

- `assets/windsurf/workflows/pr-author-generate.md`: Generate PR from Diff Plan
- `assets/windsurf/workflows/pr-author-template.md`: Create new archetype template
- `assets/windsurf/workflows/pr-author-test.md`: Test generated code locally

## Integration Points

| System | Integration | Purpose |
|--------|-------------|---------|
| Scout Agent | Event bus subscriber | Receive Diff Plans (Kafka: `autopilot.scout.diff-plan-created`) |
| GitHub | REST API v3 + GraphQL | Create branches, commits, PRs |
| GitLab | REST API v4 | Create branches, commits, MRs |
| Schema Registry | REST API | Validate schema compatibility |
| Template Store | File system / S3 | Load and cache templates |
| CI Gatekeeper | CloudEvents | Emit PR creation events |

## Configuration

```yaml
pr_author:
  # Feature flags
  enabled: true
  auto_create_pr: true
  require_human_review: true

  # Template settings
  templates_path: "/opt/autopilot/templates"
  default_otel_version: "1.32.0"

  # Git settings
  default_branch: "main"
  branch_prefix: "autopilot/observability"
  pr_labels: ["autopilot", "observability"]

  # Confidence threshold
  confidence_threshold: 0.7

  # GitHub configuration
  github:
    app_id: ${GITHUB_APP_ID}
    installation_id: ${GITHUB_INSTALLATION_ID}
    private_key_path: "/etc/autopilot/github-app-key.pem"

  # GitLab configuration (alternative)
  gitlab:
    access_token: ${GITLAB_ACCESS_TOKEN}
    api_url: "https://gitlab.company.com/api/v4"

  # Event bus
  kafka:
    bootstrap_servers: "${KAFKA_BOOTSTRAP_SERVERS}"
    consumer_group: "pr-author-agent"
    input_topic: "autopilot.scout.diff-plan-created"
    output_topic: "autopilot.pr-author.pr-created"
```

## Event Schema

### Input Event (from Scout Agent)
```json
{
  "specversion": "1.0",
  "type": "autopilot.scout.diff-plan-created",
  "source": "urn:autopilot:scout-agent",
  "id": "evt-abc123",
  "time": "2026-01-04T10:30:00Z",
  "datacontenttype": "application/json",
  "data": {
    "diff_plan_id": "dp-abc123",
    "repo": "orders-enricher",
    "repo_url": "https://github.com/company/orders-enricher",
    "confidence": 0.87,
    "diff_plan": { ... }
  }
}
```

### Output Event (to CI Gatekeeper)
```json
{
  "specversion": "1.0",
  "type": "autopilot.pr-author.pr-created",
  "source": "urn:autopilot:pr-author-agent",
  "id": "evt-def456",
  "time": "2026-01-04T10:31:00Z",
  "datacontenttype": "application/json",
  "data": {
    "diff_plan_id": "dp-abc123",
    "pr_number": 42,
    "pr_url": "https://github.com/company/orders-enricher/pull/42",
    "branch": "autopilot/observability-orders-enricher-1704364200",
    "files_changed": 8,
    "archetypes": ["kafka-microservice", "spring-boot"],
    "gaps_addressed": ["missing_otel", "missing_lineage_spec"]
  }
}
```

## Error Handling

| Error | Handling | Retry |
|-------|----------|-------|
| Invalid Diff Plan | Reject with validation errors | No |
| Low confidence | Log warning, skip PR creation | No |
| Template not found | Fall back to generic template | Yes, with fallback |
| GitHub API rate limit | Exponential backoff | Yes, 3 attempts |
| Git conflict | Rebase and retry | Yes, 1 attempt |
| Schema validation failure | Add warning to PR | No |

## Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `pr_author_plans_received` | Counter | Diff Plans received |
| `pr_author_prs_created` | Counter | PRs successfully created |
| `pr_author_prs_failed` | Counter | PR creation failures |
| `pr_author_templates_rendered` | Counter | Templates rendered |
| `pr_author_generation_duration_seconds` | Histogram | Time to generate PR |
| `pr_author_confidence_score` | Gauge | Latest plan confidence |

## Testing

Run unit tests:
```bash
pytest tests/ -v
```

Run integration tests:
```bash
pytest tests/integration/ -v --github-mock
```

Test template rendering:
```bash
python scripts/template_engine.py --test --template kafka-consumer-otel
```
