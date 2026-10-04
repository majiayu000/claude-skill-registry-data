---
name: specialist-dispatch
description: "Selects scoped architecture, backend, frontend, security, data, DevOps, QA, docs, performance, or product roles."
---

# Specialist Dispatch

For parallel author workflows, select
`superpowers.dispatching-parallel-agents` or
`superpowers.subagent-driven-development` through `be skills route ID --json`
and read the complete exposed provider. This skill retains Bible's specialist
selection and worker authorization policy separately. Missing providers or
delegation capabilities stay unresolved until the selected profile supplies
them and host exposure is verified.

Use this skill when a task benefits from a specialist lens but does not require
installing a large external agent marketplace.

This skill turns broad agent catalogs into a small Codex-native dispatch layer.
It can be used with subagents when available, or as a checklist for the main
agent when no subagent tool exists.

## Specialist Profiles

Choose the smallest set:

- architect: boundaries, dependency direction, module shape, migration seams;
- backend: APIs, domain logic, persistence, concurrency, errors;
- frontend: UI behavior, state, accessibility, visual quality;
- security: auth, authz, secrets, parser risk, supply chain;
- data: schemas, migrations, analytics, integrity, retention;
- DevOps: CI, deploy, runtime config, observability;
- QA: test plan, regression coverage, edge cases;
- docs: user-facing and operator-facing documentation;
- performance: evidence-led bottleneck analysis;
- product: user workflow, scope, acceptance criteria.

## Dispatch Rules

- Do not spawn a specialist without a concrete question.
- Give each specialist bounded files and expected output.
- Prefer read-only specialist review unless implementation ownership is clear.
- Use `agent-squad` when multiple specialists will work in parallel.
- Use `subagent-result-merge` to consolidate outputs.

## External Worker Roles

Map portable roles to verified providers and models in machine-local
configuration. Default: keep the current selected model; multimodel and quorum
are off. Preserve the parent's model, provider, and authorization. Only the
user's `/multimodel` command selects the budget-author/strong-review workflow.
`/quorum` selects its fixed reviewer roster and voting while keeping the author's
model unchanged. Same-model specialist lanes activate neither mode.
The following roles do not themselves authorize model changes:

- scout: inspect bounded context and return a map of facts;
- reviewer: review an allowed diff and related files with evidence;
- tests-docs: propose tests or documentation as an artifact, without applying it;
- patch-proposer: return a bounded code patch for the parent to inspect and apply;
- local-helper: perform a bounded task in the locally verified inference mode.

When `/multimodel` is active, use budget models for patch proposals and stronger
models for independent review. Role names do not prove availability, price or quality. Record actual
routes and usage, exclude the proposer and integrator from approval votes, and
never silently upgrade the implementation route. See
[Cross-Provider Review](../../docs/cross-provider-review.md).

Use a native custom subagent only when the installed host documents and
functionally verifies a separate provider/model and its effective permissions.
Otherwise use an explicit, locally verified external CLI capability. A config
entry is not evidence of a route. No hidden fallback: an unavailable requested
model returns blocked or failed; a replacement must be explicitly selected and
recorded. An unverified tool-calling model is only a text helper.

The main agent owns decisions and applies changes. External workers may not
edit source, run arbitrary shell, merge, commit, push, install dependencies, or
spawn other workers. Enforce limits in the runtime, not only in role text.
Use `agent-squad` for concurrency limits and `context-pack` for exported data.

## Alternative Runtime Pilots

Swarms or another programmatic runtime may be evaluated as an alternative
external worker for fixed roles, not a provider switch inside the native
parent's subagent tool. Export only the required operations and keep the
existing `subagent-result-merge` contract, source scope and parent ownership.
Start with synthetic data, explicit iteration/output/request limits and an
outer process deadline; an async timeout alone may leave work running.

A function exported over MCP proves that function path, not model delegation.
Separate server initialization, tool discovery, function invocation, actual
model execution and parent-to-worker execution in the result. No automatic
loops, global registration, new router or hidden provider fallback. Keep
library import side effects, credentials and telemetry inside reviewed private
runtime configuration. Do not stack frameworks without a measured benefit.

## Specialist Prompt Shape

```markdown
Specialist:
Question:
Scope:
Allowed files:
Forbidden files:
Evidence required:
Expected output:
Validation:
Task ID and base commit:
Snapshot state and hash:
Requested route and required runtime evidence:
Allowed tools and enforced permissions:
Timeout and retry budget:
Result: subagent-result-merge contract
```

## Output

Report:

- selected specialists;
- why each was needed;
- scope boundaries;
- result or next routing skill.
