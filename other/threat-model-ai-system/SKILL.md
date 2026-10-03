---
name: threat-model-ai-system
description: Build evidence-backed threat models for LLM, RAG, multimodal, model-serving, and agentic systems. Use when designing or reviewing an AI architecture, mapping trust boundaries and abuse paths, prioritizing security controls before release, or updating a threat model after a model, data source, tool, identity, or deployment change.
---

# Threat Model an AI System

Produce an architecture-specific threat model that another engineer can verify and act on. Treat framework taxonomies as coverage aids, not substitutes for system evidence.

Read [methodology](references/methodology.md) before mapping threats or assigning framework labels.

## Safety boundaries

- Work read-only unless the user explicitly authorizes a controlled test.
- Confirm the system, environment, identities, data, and third parties in scope before probing anything.
- Use synthetic canaries instead of real secrets, personal data, credentials, or harmful content.
- Do not exercise destructive tools, production writes, denial-of-service paths, or third-party targets.
- Do not call the system secure, compliant, or free of a threat because evidence is unavailable.
- Mark legal, privacy, safety, and business-impact questions for the responsible owner instead of inventing an answer.

## Workflow

1. **Frame the decision.** Record the business purpose, users, deployment context, risk tolerance, assessment date, owners, and requested decision.
2. **Fingerprint the system.** Record model and provider, model version or snapshot, system/developer prompt locations, orchestrator, retrieval stack, memory, tools, identities, stores, network paths, guardrails, logging, and deployment revision. Mark unavailable values as unknown.
3. **Build the architecture model.** Trace data and control flow from every input through preprocessing, retrieval, model inference, output handling, tool execution, persistence, and downstream consumers. Mark trust boundaries and privilege transitions.
4. **Identify assets and adverse outcomes.** Name the data, credentials, decisions, actions, availability, integrity, privacy, intellectual property, and human safety properties that require protection. Describe concrete loss events.
5. **Enumerate abuse paths.** Start from plausible attacker positions and trace complete paths to an adverse outcome. Include direct and indirect inputs, poisoned dependencies or knowledge, cross-tenant access, unsafe outputs, excessive agency, identity abuse, and monitoring failure when applicable.
6. **Validate against evidence.** Tie every premise to code, configuration, architecture, IAM, logs, tests, or an owner-confirmed fact. Separate observed, inferred, assumed, and unknown facts.
7. **Prioritize and treat.** Rate likelihood and impact using declared criteria. Identify existing controls, control gaps, recommended changes, control owner, verification method, residual risk, and target date.
8. **Check coverage.** Cross-check the completed model against the framework mappings in the methodology. Add only applicable threats and explain exclusions.

## Evidence rules

- Assign a stable evidence ID to every cited artifact.
- Record an absolute path, repository revision, URL, query, screenshot, log interval, or configuration identifier that lets another reviewer locate the evidence.
- Quote only the minimum lines or fields needed and redact secrets.
- Distinguish `verified`, `inferred`, `assumed`, `unknown`, and `not tested`.
- Require at least one evidence reference for every finding and risk rating.
- State contradictions between documentation and implementation instead of silently choosing one.
- Recheck drift-prone evidence close to delivery.

## Output contract

Return one report containing:

1. Scope, authorization, decision, date, assessors, and limitations.
2. System fingerprint and a Mermaid data-flow diagram with trust boundaries.
3. Asset, actor, entry-point, privilege, and dependency inventory.
4. Abuse-path register with preconditions, steps, affected assets, adverse outcome, evidence, likelihood, impact, confidence, and framework mapping.
5. Existing-control and control-gap analysis.
6. Prioritized treatment plan with owner, verification test, and residual risk.
7. Coverage matrix and explicit `unknown`, `not tested`, and out-of-scope sections.

Write each actionable finding as: `ID | title | severity | confidence | affected component | preconditions | abuse path | expected control | observed state | evidence | impact | recommendation | regression test | framework mapping`.

## Quality gate

Do not finalize until:

- Every diagram element and trust boundary has a source or an explicit assumption.
- Every high or critical risk reaches a concrete adverse outcome through a plausible path.
- Every finding cites evidence and every recommendation names a verification test.
- Ratings use declared likelihood and impact criteria rather than intuition alone.
- Taxonomy-only, duplicate, and non-applicable threats are removed or explicitly excluded.
- Unknowns, untested paths, and residual risks remain visible in the executive summary.
- The report makes no compliance or security guarantee.
