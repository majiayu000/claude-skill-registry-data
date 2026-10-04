---
name: clean-architecture-llm
description: Design LLM-powered modules with Clean Architecture boundaries, SOLID, DRY, KISS, and provider-agnostic ports/adapters. Use when adding prompt workflows, model/provider clients, tool orchestration, AI review automation, agent skills, or other LLM-backed capabilities.
---

# Clean Architecture for LLM Modules

Use this skill before implementing or reviewing any LLM-backed behavior. It
keeps provider SDKs, prompt construction, orchestration, and business logic in
the right places so LLM integrations remain testable and replaceable.

## Profile keys consumed

- `architecture.source_root`, `architecture.bounded_contexts`, `architecture.shared_context`
- `make.ci`, `make.tests`

## Context

Use this skill for:

- New LLM provider integrations or model clients
- Prompt workflows, prompt factories, or prompt templates
- Agent/tool orchestration and AI review automation
- LLM-backed command/query handlers, subscribers, processors, or CLI commands
- Refactors that move LLM logic out of controllers, handlers, or domain classes
- Code reviews for LLM feature maintainability and architecture boundaries

Pair this skill with:

- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) for domain/application/infrastructure patterns
- [code-organization](../code-organization/SKILL.md) for placement, names, and class-type directories
- [testing-workflow](../testing-workflow/SKILL.md) for deterministic unit and integration tests
- [documentation-sync](../documentation-sync/SKILL.md) when behavior or onboarding docs change
- [ci-workflow](../ci-workflow/SKILL.md) before committing or opening a PR

## Task

Design LLM modules so:

- Domain code remains provider-agnostic and prompt-free.
- Application code owns use cases, ports, DTOs, and orchestration.
- Infrastructure code owns provider SDKs, HTTP clients, retries, timeouts, and
  model-specific configuration.
- Prompts are composed through named factories/templates, not inline strings
  hidden inside handlers.
- Tests use deterministic provider doubles, fixtures, and contract assertions
  instead of live model calls.

## Layer Rules

| Layer          | Owns                                                                                                   | Must Not Own                                                             |
| -------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| Domain         | Business rules, value objects, entities, domain events                                                 | Provider names, prompts, tokens, HTTP clients, SDK classes, model IDs    |
| Application    | Use cases, command/query handlers, ports, request/response DTOs, provider-neutral prompt factories     | Direct SDK calls, environment reads, logging secrets, live network calls |
| Infrastructure | Provider adapters, SDK/HTTP clients, auth, retries, timeouts, rate-limit handling, telemetry exporters | Business rules, domain decisions, prompt policy decisions                |
| Interface/API  | Controllers, processors, CLI commands, serializers                                                     | Prompt assembly, provider choice, retry policy, domain decisions         |
| Tooling/Docs   | Agent skills, examples, review checklists, planning specs                                              | Runtime secrets or production-only behavior                              |

## Execution Steps

### 1. Classify the Capability

Write down the business use case in provider-neutral language:

- Bad: "Call OpenAI to score a user."
- Good: "Evaluate whether a registration risk profile requires additional
  verification."

If the behavior is not business logic and only supports developer workflow,
place it under tooling/docs rather than runtime application code.

### 2. Define the Port First

Create an Application-layer interface that describes the capability, not the
vendor API. The interface should accept typed request objects and return typed
response objects.

Here, "port" means the provider-neutral Application-layer interface role. Put
the interface in an existing class-type directory that matches its
responsibility, such as `Provider/`, `Validator/`, or `Resolver/`, or get
explicit approval before introducing a new `Port/` directory. The module lives
inside one of the contexts listed in `architecture.bounded_contexts`, under
`architecture.source_root`:

```text
<source_root>/{Context}/
├── Application/
│   ├── DTO/{Capability}Request.php, {Capability}Response.php
│   ├── Factory/{Capability}PromptFactory.php
│   ├── {PortDirectory}/{Capability}EvaluatorInterface.php
│   └── CommandHandler/{Action}{Entity}CommandHandler.php
└── Infrastructure/
    ├── Adapter/{Provider}{Capability}Evaluator.php
    ├── Factory/{Provider}RequestFactory.php
    └── Parser/{Provider}{Capability}ResponseParser.php
```

Required:

- Use specific names such as `RegistrationRiskEvaluatorInterface`, not
  `LlmService`.
- Keep provider names out of the interface.
- Use immutable request/response DTOs or value objects.
- Document failure modes with domain/application exceptions.

Forbidden:

- Raw `array` payloads without typed structure.
- Provider SDK request classes in Application or Domain code.
- Methods named after vendor endpoints such as `createChatCompletion()`.

### 3. Keep Prompt Construction Explicit

Prompts are behavior. Treat them as named collaborators.

Use one of these patterns:

- `Factory`: builds prompt/request objects from typed inputs.
- `Strategy`: chooses a prompt or model policy for a use case.
- `Template`: stores stable prompt text with named variables.
- `Pipeline`: performs validation, redaction, prompt creation, provider call,
  response parsing, and policy checks in separate steps when the workflow is
  complex.

Rules:

- Do not concatenate large prompt strings inside handlers or controllers.
- Keep prompt variables explicit and typed.
- Centralize shared prompt fragments to avoid drift — in the shared-kernel
  context named by `architecture.shared_context` when one exists and several
  bounded contexts consume them.
- Record prompt versioning when output affects user-visible or persisted state.

### 4. Isolate Provider Details in Adapters

Infrastructure adapters implement Application ports and translate between typed
application DTOs and provider SDK/HTTP payloads.

Adapters must own:

- Provider SDK/HTTP client usage
- Authentication headers or SDK credentials
- Timeout, retry, and rate-limit behavior
- Provider-specific error mapping
- Provider response parsing and schema validation

Adapters must not own:

- Business decisions
- Domain state transitions
- Prompt policy choices that belong to the use case
- Direct persistence unless the port explicitly represents persistence

### 5. Apply SOLID, DRY, and KISS

SOLID:

- Single Responsibility: split orchestration, prompt creation, provider calls,
  parsing, and persistence.
- Open/Closed: add providers by adding adapters or strategies, not by editing
  every caller.
- Liskov Substitution: each provider adapter must satisfy the same port
  contract and failure semantics.
- Interface Segregation: create narrow ports per capability.
- Dependency Inversion: Application code depends on interfaces, Infrastructure
  depends on Application contracts.

DRY:

- Share prompt fragments, schema definitions, redaction policies, and response
  parsers through named collaborators.
- Avoid duplicate model ID, timeout, token limit, or retry constants.

KISS:

- Start with one narrow port and one adapter.
- Add Strategy, Pipeline, or Decorator only when there is real branching,
  repeated cross-cutting behavior, or measurable complexity.
- Prefer boring typed DTOs over dynamic generic payload builders.

### 6. Make Failures Deterministic

LLM calls are probabilistic, but application behavior must not be.

Required:

- Map provider errors to application exceptions.
- Set explicit timeout and retry policy.
- Give retries clear limits; never wrap non-idempotent side effects in a retry
  without an explicit idempotency guard.
- Validate provider responses before using them.
- Define fallback behavior for invalid, empty, or unsafe output.
- Do not hide provider failures behind silent defaults — surface and fix the
  root cause.

### 7. Test Without Live Models

Unit and integration tests (run via the target mapped by `make.tests`) must
not call live providers.

Use:

- In-memory adapters for success and failure paths.
- Contract tests that every provider adapter must satisfy.
- Fixtures for provider payloads and parsed responses.
- Prompt factory tests that assert required variables and redaction.
- Response parser tests for malformed, partial, and unsafe output.
- Failure-path tests for timeout, retry exhaustion, invalid output, and unsafe
  output.

Live smoke tests, if needed, must be opt-in, isolated, and excluded from default
CI unless explicitly approved.

### 8. Protect Privacy and Observability

Required:

- Redact tokens, credentials, PII, and prompt-sensitive data from logs.
- Log stable metadata: provider, model alias, latency, status, retry count, and
  request correlation ID.
- Avoid logging full prompts or raw responses unless an approved redaction path
  exists.
- Keep model names, temperature, token limits, and timeouts in configuration,
  not hardcoded in handlers.

### 9. Verify Before PR

Before opening a PR, confirm:

- Domain has no LLM provider, prompt, SDK, HTTP, or token concepts.
- Application owns ports and typed request/response contracts.
- Infrastructure implements provider adapters and maps errors.
- Prompt construction is explicit and test-covered.
- No live provider calls run in default tests.
- README/onboarding/docs mention new LLM workflows when relevant.
- The target mapped by `make.ci` (or the documented required subset) has been
  run — see [ci-workflow](../ci-workflow/SKILL.md). Fix failures at the root
  cause: never add suppression annotations, lower quality thresholds, or edit
  `deptrac.yaml`.

PR evidence to attach (or request when reviewing):

- Links to the Application port and DTOs, and to the Infrastructure adapter.
- Links to prompt factory/template tests and provider response parser tests.
- Links to docs/onboarding updates when behavior changes, or a clear
  explanation for a narrower docs-only validation path.

## Design Patterns

| Pattern   | Use When                                                        | Avoid When                                             |
| --------- | --------------------------------------------------------------- | ------------------------------------------------------ |
| Adapter   | Wrapping provider SDK/HTTP APIs behind an Application port      | Business rules are being hidden in Infrastructure      |
| Strategy  | Selecting model, provider, prompt, or safety policy by use case | There is only one fixed path                           |
| Factory   | Building prompts, provider requests, or typed DTOs from inputs  | It only forwards parameters without construction logic |
| Decorator | Adding retries, metrics, caching, or redaction around a port    | It changes business behavior unexpectedly              |
| Pipeline  | A workflow has several ordered, independently testable steps    | A simple handler would stay clearer                    |

## Anti-Patterns

- `LlmService`, `AiManager`, `PromptHelper`, or other catch-all classes.
- Provider SDK classes imported by Domain or Application use cases.
- Prompt strings assembled inline in controllers, processors, subscribers, or
  command handlers.
- Static/global provider clients.
- Hidden environment reads inside use cases.
- Bare arrays for request/response payloads.
- Live model calls in unit tests or default CI.
- Logging full prompts, raw user data, access tokens, or provider responses.
- Provider-specific model IDs hardcoded across multiple classes.
- Silent fallback when the provider returns invalid or unsafe output.

## Related Skills

- [implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md) - Layer patterns the LLM module must respect
- [code-organization](../code-organization/SKILL.md) - Class-type directory placement for ports, adapters, factories
- [testing-workflow](../testing-workflow/SKILL.md) - Running and debugging the deterministic test suite
- [documentation-sync](../documentation-sync/SKILL.md) - Keeping docs aligned with new LLM workflows
- [ci-workflow](../ci-workflow/SKILL.md) - Driving the full quality suite to green before the PR
