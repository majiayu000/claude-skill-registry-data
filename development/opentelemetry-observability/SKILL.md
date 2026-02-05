---
name: opentelemetry-observability
description: Instrument services with OpenTelemetry and reliable signal pipelines
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
model: sonnet
x-version: 3.2.0
x-category: operations
x-vcl-compliance: v3.1.1
x-cognitive-frames:
  - HON
  - MOR
  - COM
  - CLS
  - EVD
  - ASP
  - SPC
---




## STANDARD OPERATING PROCEDURE

### Purpose
Design and implement OpenTelemetry collection, instrumentation, and validation so traces, metrics, and logs are actionable.

### Trigger Conditions
- **Positive:** Add or improve OpenTelemetry instrumentation; Standardize telemetry schema across services; Harden collectors/pipelines with SLOs
- **Negative:** Performance debugging without instrumentation changes (route to performance-analysis); Pure infrastructure build (route to infrastructure); Vendor-specific dashboard asks without pipeline changes (route to production-readiness)

### Guardrails
- Structure-first: keep SKILL.md aligned with examples/, tests/, and any resources/references so downstream agents always have scaffolding.
- Adversarial validation is mandatory: cover boundary cases, failure paths, and rollback drills before declaring the SOP complete.
- Prompt hygiene: separate hard vs. soft vs. inferred constraints and confirm inferred constraints before acting.
- Explicit confidence ceilings: format as 'Confidence: X.XX (ceiling: TYPE Y.YY)' and never exceed the ceiling for the claim type.
- MCP traceability: tag sessions WHO=operations-{name}-{session_id}, WHY=skill-execution, and capture evidence links in outputs.
- Avoid anti-patterns: undocumented changes, missing rollback paths, skipped tests, or unbounded automation without approvals.

### Required Artifacts
- SKILL.md (this SOP)
- examples/ for instrumentation
- tests/ for telemetry validation
- resources/ for collectors

### Execution Phases
1. **Baseline signals**
   - Inventory services, runtimes, and existing telemetry
   - Identify critical user journeys and SLOs
   - Capture schema and attribute standards

2. **Design OTEL pipeline**
   - Plan exporters, collectors, sampling, and resource attributes
   - Define security, retention, and cost controls
   - Prepare rollout stages and fallback options

3. **Instrument and deploy**
   - Add or refine instrumentation with context propagation
   - Deploy collectors/agents with configs per environment
   - Enable logging/metrics/traces validation and alerts

4. **Validate and tune**
   - Run data-quality checks (cardinality, loss, latency)
   - Validate SLOs/SLIs and alert thresholds
   - Document runbooks and continuous improvement loops

### Output Format
- Instrumentation plan mapped to key journeys
- Collector topology and configuration references
- Schema/attribute standards and governance notes
- Validation report on data quality and SLOs
- Runbook for operations, tuning, and fallbacks

### Validation Checklist
- Sampling/resource impact reviewed and acceptable
- Data quality verified for completeness and latency
- SLOs/SLIs defined with alert thresholds
- Security and retention controls documented
- Confidence ceiling stated for telemetry readiness

Confidence: 0.70 (ceiling: inference 0.70) - OpenTelemetry SOP applies structured rollout and verification
