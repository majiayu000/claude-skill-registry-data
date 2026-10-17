---
name: rails-incident-engineering
description: "Use when operating, diagnosing, or reviewing production Rails systems through incident response: alert triage, diagnostic context, incident timelines, runbooks, safe production debugging, mitigation, recovery verification, and post-incident learning."
license: MIT
---

# Rails Incident Engineering & Operational Debugging

## Purpose

Treat production incident response as an engineered lifecycle rather than ad-hoc debugging.

This skill sits above request observability and reliability controls:
- rails-observability owns telemetry primitives such as request IDs, error reporting, instrumentation, logs, metrics, and health semantics.
- rails-reliability-engineering owns SLI/SLO/error-budget design, failure containment, degradation, overload, and recovery objectives.
- this skill owns how an agent turns operational signals into a bounded incident response: detect, triage, establish impact and scope, build a timeline, choose safe diagnostics, mitigate, verify recovery, and capture durable learning.

Core flow:
alert / symptom -> affected contract -> scope -> change correlation -> hypothesis -> safe evidence -> reversible mitigation -> recovery verification -> timeline/evidence -> follow-up

The objective is not merely to find an exception. The objective is to restore the affected contract safely while preserving enough evidence to explain what happened and prevent recurrence.

## Activate when

- diagnosing a production Rails incident or recurring operational failure;
- reviewing alerts, paging thresholds, or alert fatigue;
- designing or updating operational runbooks;
- correlating logs, metrics, traces, request IDs, job IDs, message IDs, and deployment metadata;
- determining incident scope, severity, or user impact;
- debugging production behavior without restarting or mutating the system unnecessarily;
- coordinating mitigation and recovery verification;
- reviewing an incident timeline or post-incident review;
- converting an incident finding into tests, instrumentation, guardrails, or architecture changes;
- investigating failures that cross HTTP, background-job, broker, database, or external-service boundaries.

Do not activate this skill merely because code needs ordinary local debugging. Use the narrowest debugging or implementation skill when there is no operational incident lifecycle.

## Repository inspection

Inspect before choosing an incident procedure:
1. Rails/Ruby/runtime versions and deployment topology;
2. existing rails-observability instrumentation, logging, request IDs, error reporters, and health endpoints;
3. existing rails-reliability-engineering SLOs, error budgets, alerts, degradation, and recovery objectives;
4. dashboards, alert definitions, notification routes, and ownership metadata;
5. request, job, message, database, and dependency correlation conventions;
6. deploy/release markers, feature flags, rollback/roll-forward mechanisms, and runtime configuration;
7. existing runbooks, on-call documentation, escalation paths, and incident severity definitions;
8. audit/security constraints for production access;
9. safe read-only diagnostic tooling and access controls;
10. existing post-incident records, recurring failure patterns, and known workarounds.

Do not invent a second request ID, alternate severity taxonomy, duplicate dashboard, or broad logging format when the repository already has an established contract.

## Incident lifecycle

Use explicit operational states:
detected -> acknowledged -> triaging -> diagnosed enough to act -> mitigating -> verifying -> recovered -> monitoring -> closed -> learning actions tracked

For each state, preserve:
- owner;
- affected user journey or system contract;
- current scope/impact;
- leading hypothesis;
- evidence supporting or contradicting it;
- current mitigation;
- next decision point;
- time of significant changes.

Avoid parallel unowned investigations. Separate evidence gathering from mutation and mitigation authority when the organization requires it.

## Triage procedure

Start with user impact, not the loudest log line.

Classify:
- what is failing;
- which user journey or operational contract is affected;
- when it started;
- current versus baseline error, latency, and saturation;
- affected routes, jobs, message consumers, tenants, regions, providers, or versions;
- whether the issue is growing, stable, or recovering;
- whether a recent deploy/config/data change correlates with onset;
- whether a safe mitigation exists.

Useful triage record:
symptom -> affected contract -> scope -> onset -> change correlation -> dependency/resource signal -> current hypothesis -> next evidence

Do not declare root cause during initial triage unless evidence already supports it. Distinguish symptom, contributing factor, trigger, and root cause.

## Alert actionability

An alert should drive an operator action.

For each alert, define:
- signal and measurement window;
- affected user/system contract;
- threshold or anomaly rule;
- urgency/severity;
- expected operator action;
- diagnostic links/context;
- owner/escalation path;
- suppression/deduplication behavior;
- recovery condition.

Avoid alerts for metrics with no available action. Avoid paging on every raw exception when the same condition is better represented by a user-impact SLI, burn rate, saturation signal, or bounded operational state.

After an incident, review whether the alert fired too early, too late, too often, without enough diagnostic context, without a useful action, or not at all.

## Diagnostic context

Operational debugging should make correlation cheap.

Prefer a stable context chain:
incident -> deployment/config version -> request/job/message identifiers -> trace/correlation identifiers -> controller/action or job/consumer -> dependency call -> database/resource signal -> failure event

Reuse existing repository identifiers. Do not create unrelated identifiers per subsystem.

Diagnostic context should be bounded, searchable, privacy-aware, consistent across request/job/message transitions, and low-cardinality where it becomes a metric dimension.

Never add credentials, authorization headers, tokens, secrets, or unnecessary sensitive payloads merely to improve incident diagnosis.

## Incident timeline

Build a factual timeline from observed timestamps and durable evidence.

Capture:
- first known symptom;
- first alert;
- acknowledgement;
- relevant deploy/config/data changes;
- scope expansion or contraction;
- diagnostic discoveries;
- mitigation actions;
- recovery evidence;
- monitoring period;
- incident closure.

Prefer timestamps from telemetry, deployments, control-plane records, and operator actions over memory.

Separate observed facts from interpretation. Record hypotheses as hypotheses until corroborated.

## Hypothesis-driven debugging

For each leading hypothesis, record:
1. evidence that would support it;
2. evidence that would falsify it;
3. the narrowest safe query or inspection that can discriminate;
4. what observation changes the next decision.

Example: hypothesis = connection-pool saturation; support = pool wait time and active connections rise with latency; falsify = pool remains below capacity while dependency latency rises; next evidence = pool utilization plus dependency timing for the same interval.

Do not add broad logging or mutate production state to collect weak evidence when existing telemetry can answer the question.

## Safe production debugging

Prefer, in order:
1. existing dashboards and structured telemetry;
2. read-only log/error search;
3. read-only application/resource inspection;
4. bounded diagnostic queries;
5. controlled, reversible configuration or feature changes;
6. rollback, roll-forward, or traffic controls when justified;
7. state-changing interventions only with explicit ownership and recovery awareness.

Before a production command or code change, identify blast radius, required privilege, reversibility, concurrency/duplicate-execution risk, data mutation, auditability, and user-visible effect.

Never execute destructive SQL, arbitrary code, mass data edits, or broad logging changes merely because they might reveal the cause.

## Mitigation and recovery

Choose the smallest reversible mitigation that protects the critical user journey.

Candidate controls include rollback/roll-forward, feature flag disablement, traffic reduction or load shedding, dependency isolation, queue pause/drain controls, degraded behavior, concurrency reduction, and temporary provider routing changes.

A mitigation is not recovery. Verify recovery at multiple levels:
process healthy AND dependency behavior healthy AND user-facing SLI recovered AND backlog/queue state stable AND no hidden error/data-integrity regression

Use rails-reliability-engineering for recovery objectives and rails-production-runtime for lifecycle mechanics.

Do not close an incident solely because error logs stopped increasing.

## Runbooks

A runbook is an executable operator guide, not a narrative explanation.

A useful runbook contains purpose and affected contract, prerequisites/access requirements, detection signals, diagnostic commands or queries, decision points, mitigation steps, stop conditions, recovery verification, rollback/undo procedure, escalation ownership, dashboard/log links, and known limitations.

Commands must state scope, expected output, and safety implications. Prefer small decision trees over long unstructured checklists.

## Cross-boundary incidents

For issues spanning services or asynchronous execution, preserve the chain:
request -> job -> message -> consumer -> external provider -> database

Correlate request/correlation ID, job ID, message/event ID, causation ID where available, deployment/version, dependency/provider, and tenant/account scope where permitted.

Use rails-api-integration for HTTP/provider failures; rails-active-job for queue/retry semantics; rails-event-driven-messaging for message lifecycle, lag, retries, and replay; rails-distributed-systems for ownership, consistency, and cross-service failure models.

Do not infer causality solely because two systems emitted errors at similar times.

## Security during incidents

Incident urgency does not remove security boundaries.
- preserve authorization when using operator tools;
- minimize production data access;
- redact sensitive values in incident artifacts;
- treat exported logs and screenshots as potentially sensitive;
- record emergency access and state changes where required;
- do not disable security controls globally as a first response;
- coordinate with rails-security and rails-security-engineering for abuse, unauthorized access, secret exposure, or trust-boundary failures.

## Post-incident review

A useful review answers:
- What user/system contract was affected?
- What happened, in sequence?
- What evidence supports the causal chain?
- Which controls detected, contained, or failed?
- Which factors made detection or mitigation slower?
- Which decisions were reversible and which were not?
- What prevented earlier detection or safer mitigation?
- Which action items reduce recurrence, detection time, mitigation time, or blast radius?

Separate contributing conditions from individual blame.

Every material action item should have an owner, concrete change, verification method, and connection to the observed failure mode.

Do not create dozens of vague follow-ups. Prefer a small set of high-leverage changes.

## Incident-to-engineering feedback loop

Convert material incidents into durable engineering changes:
incident -> missing/weak signal -> missing/weak control -> regression/resilience test -> telemetry/runbook update -> architecture/design improvement

Examples include request regressions, correlation fixes, SLO/alert changes, retry/breaker reviews, safer recovery automation, invariants, and reconciliation tests.

Do not treat the incident document as the final artifact if the failure can be prevented or diagnosed by changing the system.

## Reference example

Incident response as executable checks: a runbook script that gathers the exact evidence the runbook names, in one command.

```ruby
# lib/tasks/incident.rake
namespace :incident do
  desc "Collect first-five-minute evidence for a suspected payment incident"
  task evidence: :environment do
    since = 1.hour.ago

    puts "failed charges (last hour): #{Charge.failed.where(updated_at: since..).count}"
    puts "provider latency p95:       #{Metrics.p95("provider.request", since..)}"
    puts "sidekiq queue depth:         #{Sidekiq::Queue.new("billing").size}"
    puts "recent deploys:              #{Deploy.where(created_at: since..).pluck(:sha).join(", ")}"
    # Mitigation comes next (feature flip, queue pause); evidence is collected first,
    # and every claim in the incident channel cites a command that produced it.
  end
end

# bin/rails incident:evidence > evidence.txt
```

## Agent review checklist

- [ ] existing observability and reliability conventions inspected
- [ ] affected user/system contract identified
- [ ] incident scope and onset are evidence-based
- [ ] severity/urgency follows repository conventions
- [ ] symptom is distinguished from hypothesis and root cause
- [ ] diagnostic context uses existing identifiers
- [ ] sensitive data remains filtered
- [ ] hypotheses have discriminating evidence
- [ ] production diagnostics are bounded and reversible where possible
- [ ] mitigation protects critical work and has an undo/exit path
- [ ] recovery is verified with user-impact and system signals
- [ ] timeline is based on durable timestamps
- [ ] runbook contains actionable commands and safety limits
- [ ] post-incident actions have owners and verification
- [ ] material findings become tests, telemetry, controls, or design changes

## Anti-patterns

- treating the first exception as the root cause;
- paging on every raw error without an operator action;
- inventing new correlation IDs during the incident;
- changing production code broadly to gain diagnostic visibility;
- executing destructive queries to see what happens;
- disabling authentication/security controls as a generic mitigation;
- declaring recovery from one healthy process check;
- closing incidents without preserving the timeline;
- creating postmortem actions with no owner or verification;
- blaming individuals instead of improving the system.

## Verification

Verify the incident workflow at the smallest owning boundary.

For skill changes, run repository validators and the focused incident-engineering system test.

For operational changes, verify alert firing/resolution, diagnostic context, runbook executability and safety, mitigation reversibility, recovery criteria, and action-item traceability.

Never claim that an incident is fully understood merely because symptoms disappeared. Preserve uncertainty and explicitly state unverified causal assumptions.

## Source foundation

Primary framework guidance:
- Rails Error Reporting: https://guides.rubyonrails.org/error_reporting.html
- Rails Active Support Instrumentation: https://guides.rubyonrails.org/active_support_instrumentation.html
- Rails Debugging Applications: https://guides.rubyonrails.org/debugging_rails_applications.html
- Rails Configuring Applications: https://guides.rubyonrails.org/configuring.html

Repository composition:
- `rails-observability` skill
- `rails-reliability-engineering` skill
- `rails-production-runtime` skill
- `rails-event-driven-messaging` skill
- `rails-distributed-systems` skill

Use the repository's actual runtime, telemetry, access, deployment, and incident-management conventions as the operational authority.

## Rails incident engineering changes

For production incident and operational-diagnostics changes:
- resolve the affected user/system contract before investigating individual exceptions;
- inspect existing observability, reliability, runtime, deployment, alerting, runbook, and access conventions before adding new operational mechanisms;
- distinguish symptom, trigger, contributing factor, hypothesis, and evidence-backed root cause;
- preserve existing request/job/message/dependency correlation identifiers instead of creating parallel IDs;
- make alerts actionable with an owner, diagnostic context, response, and recovery condition;
- prefer existing telemetry and bounded read-only diagnostics before production mutation;
- evaluate blast radius, privilege, reversibility, auditability, and user impact before every state-changing mitigation;
- verify recovery through user-impact SLIs and relevant dependency/backlog/data-integrity signals, not only process health;
- build incident timelines from durable timestamps and label hypotheses separately from observed facts;
- make runbooks executable, bounded, reversible, and explicit about stop conditions;
- convert material incidents into owned, testable changes to code, telemetry, alerts, runbooks, resilience controls, or architecture;
- do not disclose secrets or disable security boundaries as a generic incident response technique.
