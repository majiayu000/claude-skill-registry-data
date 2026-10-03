---
name: python-development
description: Build, review, debug, and maintain production Python applications, services, libraries, CLIs, and automation. Use for Python code, pytest, typing, packaging, dependency management, asyncio, FastAPI, Django, data access, and Python performance or reliability work.
---

# Python Development

Act as the Python engineer responsible for code that will be deployed, maintained, and diagnosed under pressure. Prefer explicit contracts, small composable units, typed boundaries, deterministic tests, and the project's existing tooling over clever abstractions.

## Execution Workflow

1. **Discover the project contract.** Inspect `pyproject.toml`, lockfiles, Python version, source layout, test configuration, lint/type-check commands, and deployment entry points. Do not introduce a second package manager or formatter.
2. **Define the boundary.** State inputs, outputs, error behavior, side effects, performance expectations, and resource ownership. Parse untrusted input at the edge and pass validated domain values inward.
3. **Implement the smallest cohesive change.** Use modules by responsibility, dependency injection for I/O boundaries, and explicit exception handling. Preserve compatibility unless a breaking change is requested.
4. **Test and verify.** Test public behavior, failure paths, and regressions. Run the repository formatter, linter, type checker, and targeted tests before broader tests.
5. **Report delivery.** Summarize behavior, validation, assumptions, and operational risks.

## Step 0: Ground the Task Before Writing Code

State these facts before implementing when they are not obvious from the repository:

1. **Change objective:** What behavior must be true when this work is complete?
2. **Entry point and callers:** Which command, API, worker, library function, or scheduled job invokes it?
3. **Data contract:** What trusted and untrusted values cross the boundary? Which values are optional, bounded, or sensitive?
4. **Failure contract:** Which failures are expected, how are they represented, and who is responsible for retrying or displaying them?
5. **Verification:** Which tests and commands will prove the change works?

Do not answer a request with only a code snippet when the request requires a repository change. Inspect the relevant modules, tests, configuration, and established patterns first. If a consequential fact cannot be discovered, state the assumption in the plan and keep the design reversible.

## Project Discovery Checklist

Before changing a Python project, inspect rather than guess:

- `pyproject.toml`, `setup.cfg`, `tox.ini`, or `pytest.ini` for Python support, dependencies, tools, test markers, and package layout.
- Lockfiles and CI workflow files for the approved dependency tool and the commands CI actually executes.
- Application startup, configuration loading, logging, health checks, and exception middleware for the service contract.
- Nearby implementation and test files for naming, sync/async, fixtures, factories, and error conventions.
- Database migrations, model/query code, and API schemas before changing persisted or public data.

If the repository already uses `uv`, Poetry, pip-tools, Hatch, Pydantic, Django, FastAPI, SQLAlchemy, or another tool, follow its local conventions. Do not impose a preferred stack.

## Design Before Implementation

Write a concise implementation plan using this format:

```markdown
## Python Change Plan

**Objective:** <observable behavior>
**Affected boundary:** <HTTP / CLI / worker / library / database>
**Inputs and validation:** <schema, limits, defaults>
**Success result:** <return value or response>
**Expected failures:** <error code/type and caller behavior>
**Side effects:** <DB, files, queue, network>
**Tests:** <unit, integration, regression cases>
```

Choose a design using these rules:

| Situation | Preferred approach | Avoid |
|---|---|---|
| Pure business rule | Typed function with no I/O | Framework model or global access in the rule |
| External service | Small client/protocol with timeout and translated errors | Calling HTTP directly throughout services |
| Multi-step write | Explicit service method and transaction | Transaction spanning a remote request |
| Untrusted payload | Parse/validate once at the boundary | Passing `dict[str, Any]` across layers |
| Background work | Explicit job input/output and idempotency key | Reusing a request handler in a worker |

## Python Code Patterns

### Model valid data explicitly

Use types that make invalid states difficult to represent. Keep wire parsing separate from business logic.

```python
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("amount must not be negative")
        if len(self.currency) != 3:
            raise ValueError("currency must be an ISO-4217 code")
```

Do not use a dataclass as an unvalidated HTTP/JSON parser unless the project deliberately provides that behavior. Validate the wire format first, then construct the domain value.

### Keep I/O at the edge

```python
class PaymentGateway(Protocol):
    async def charge(self, *, account_id: str, amount: Money, idempotency_key: str) -> str: ...


class ChargeAccount:
    def __init__(self, gateway: PaymentGateway, repository: AccountRepository) -> None:
        self._gateway = gateway
        self._repository = repository

    async def execute(self, command: ChargeCommand) -> ChargeResult:
        account = await self._repository.get_required(command.account_id)
        receipt = await self._gateway.charge(
            account_id=account.id,
            amount=command.amount,
            idempotency_key=command.idempotency_key,
        )
        return ChargeResult(receipt_id=receipt)
```

Use a protocol only at a meaningful dependency boundary. Do not create interfaces for simple, internal utilities with a single implementation.

### Translate errors once

At an infrastructure boundary, translate provider-specific failures into stable application errors. At an HTTP/CLI boundary, translate application errors into a user-facing response. Do not expose `requests`, SQL driver, ORM, or traceback details as public contracts.

## Async and Background-Work Rules

Before using async, determine whether the slow operation is asynchronous I/O, blocking I/O, or CPU work. Keep one concurrency model per path where practical.

- Give every outbound call a timeout and a cancellation path.
- Retry only failures proven transient; use capped exponential backoff and an idempotency strategy.
- Do not create unbounded tasks with `create_task`, unbounded semaphores, or unbounded queues.
- Never suppress cancellation. Perform required cleanup and re-raise `CancelledError`.
- For a background job, define a durable input, idempotency behavior, retry policy, dead-letter/alert path, and observability fields.

## API, Database, and Security Gates

For every endpoint, message consumer, CLI input, or uploaded file:

- [ ] Validate shape, type, size, range, and ownership at the boundary.
- [ ] Authenticate identity and authorize the requested resource/action where relevant.
- [ ] Use a stable success and error shape matching existing project conventions.
- [ ] Set pagination or hard limits for collection reads and uploads.
- [ ] Parameterize queries and evaluate query count, indexes, isolation, and transaction scope.
- [ ] Redact secrets and personal data from logs, errors, traces, and test fixtures.
- [ ] Set timeouts and size limits for all remote or streamed operations.

## Test Design

Name the test cases before implementation. A production change normally needs the following when applicable:

| Test type | Proves | Example |
|---|---|---|
| Unit | Domain decision and invariant | Reject a negative amount before any gateway call |
| Adapter integration | Real contract with a DB/client/framework | Query uses expected transaction and maps a missing row |
| API/CLI | Validation and public error response | Invalid payload returns the project's validation error shape |
| Regression | The reported defect cannot return | Duplicate event does not create a second record |

Use test names that describe behavior: `test_charge_rejects_duplicate_idempotency_key`. Assert observable results and collaborator effects, not private method calls. For time, randomness, UUIDs, and environment values, inject or freeze them.

## Package, Configuration, and Release Discipline

Treat packaging and configuration as production interfaces.

### Dependencies and environments

- Add a library only after checking standard library and existing dependencies. Prefer a maintained package with compatible license, Python support window, and an actual need.
- Add runtime dependencies to the runtime group and test/lint tools to development groups according to the existing package manager.
- Update the lockfile with the approved command. Never hand-edit dependency resolution files.
- Keep the source importable in a clean environment. Do not rely on the repository root, an editable local install, or untracked environment variables.
- Pin or constrain dependencies according to repository policy, and call out a dependency that materially expands the attack surface or runtime footprint.

### Configuration

Use one typed configuration boundary. It should validate required values once, provide secure defaults only where a default is genuinely safe, and distinguish development convenience from production requirements.

```python
@dataclass(frozen=True)
class Settings:
    database_url: str
    request_timeout_seconds: float

    @classmethod
    def from_environment(cls, env: Mapping[str, str]) -> "Settings":
        database_url = env.get("DATABASE_URL")
        if not database_url:
            raise ConfigurationError("DATABASE_URL is required")
        return cls(
            database_url=database_url,
            request_timeout_seconds=float(env.get("REQUEST_TIMEOUT_SECONDS", "5")),
        )
```

Do not read `os.environ` throughout the application or silently coerce malformed values. Update safe environment documentation/config templates without placing real credentials in the repository.

### Observability

For a new operation, decide what an on-call engineer needs to answer: Did it run? For whom/which resource? How long did it take? Did a dependency fail? Can the request/job be correlated? Emit structured, redacted fields using project conventions. Add metrics for volume, latency, and error rate when the operation is critical or high-volume. Do not log every internal detail merely because structured logging exists.

## Review Checklist for Python Changes

Review the final diff using these questions:

### Correctness

- Is every public return value/error outcome handled by callers?
- Is ordering, timezone, decimal precision, encoding, locale, or pagination behavior explicit where relevant?
- Does a retry or duplicate message/request produce a correct result?
- Can partially completed side effects leave data inconsistent, and is there a transaction or recovery plan?

### Security

- Is all external data validated and constrained before use?
- Can an identifier be changed to access another tenant/resource?
- Are SQL, paths, shell arguments, templates, redirects, uploads, and deserialization safe?
- Could error messages, logs, traces, or test fixtures expose secrets or personal data?

### Maintainability

- Does each function have one responsibility and a comprehensible name?
- Are dependencies passed explicitly at meaningful boundaries?
- Are comments explaining why a surprising choice is necessary rather than narrating code?
- Would a failing test identify the broken business behavior, not an implementation detail?

### Operations

- Are client timeouts and limits explicit?
- Is a newly expensive query, loop, file operation, or remote call bounded?
- Does the change need a migration, backfill, feature flag, staged rollout, dashboard, or alert?

## Anti-Patterns to Reject

Reject or correct these even if they make a short patch look simpler:

- A catch-all exception that logs then returns a success-like empty result.
- Global clients/configuration created at import time with no lifecycle control.
- A synchronous ORM/HTTP client called from a hot async path.
- A list endpoint that loads an entire table or relationship into memory.
- A retry loop with no limit, no timeout, or no idempotency consideration.
- A test that asserts a mock was called but cannot prove the user-visible outcome.
- A new dependency or framework layer added solely to avoid writing a small clear function.
- A migration that is unsafe for existing data, lacks rollback thinking, or assumes deployment is instantaneous.

## Required Output

For a code task, produce this before or alongside the implementation:

```markdown
## Implementation Summary

### Plan
- Objective:
- Files and responsibilities:
- Assumptions:

### Contract and Failure Handling
- Input validation:
- Success behavior:
- Expected errors:
- Side effects / idempotency:

### Verification
- Tests added or changed:
- Commands run and result:
- Not run and why:

### Risks / Follow-up
- Migration, rollout, performance, or observability notes:
```

## Production Rules

- Target the Python version declared by the project. Use type hints at public module, function, class, and data-boundary interfaces.
- Keep `Any` at unavoidable integration boundaries only. Narrow unknown values through validation; never use `Any` merely to silence failures.
- Use `dataclass` for simple in-process data and the project’s schema/validation library for external data. Use `default_factory` for mutable defaults.
- Prefer domain-specific exceptions and preserve causes with `raise DomainError(...) from exc`. Do not catch bare `Exception` without an intentional recovery or translation strategy.
- Keep imports side-effect free. Defer connections, configuration validation, and expensive work to an explicit startup lifecycle.
- Make time, randomness, environment access, and external I/O injectable or isolated so tests are deterministic.

## Async, I/O, and Data Safety

- Use `async def` for asynchronous I/O, not as a default. Do not block the event loop with synchronous clients, CPU-heavy work, or `time.sleep`.
- Propagate cancellation; clean up and re-raise `asyncio.CancelledError`. Bound concurrency, queues, retries, and timeouts.
- Scope clients, files, transactions, and task groups with context managers. Close resources deterministically.
- Validate requests, environment values, messages, and files before domain logic. Use parameterized queries, explicit transaction boundaries, pagination, and configured outbound timeouts.
- Keep HTTP handlers and ORM/framework objects thin. Do not log credentials, tokens, personal data, or full untrusted payloads.

## Testing and Quality Gates

- Use focused `pytest` fixtures and fakes at I/O seams. Test behavior rather than private implementation.
- Cover invalid input, authorization, timeout, retry, transaction, and idempotency cases when relevant.
- Keep tests independent: no execution order, shared mutable state, wall-clock dependence, or live third-party services in the default suite.
- Run project-configured formatting, linting, type checking, and tests. Report every command not run and why.

## Common Failure Modes

- Mutable default arguments or shared fixture state -> use factories and isolate state per request/test.
- Broad exception handling -> catch known failures, preserve causes, and translate only at the appropriate boundary.
- Missing request timeouts -> configure connect/read/total timeouts explicitly.
- Async code calling blocking work -> use async clients, intentionally offload work, or use synchronous architecture consistently.
- Dynamic SQL, shell strings, paths, or deserialization -> parameterize, validate, constrain paths, and use safe parsers.

## Delivery Format

Provide changed modules and behavior; data/error contracts; tests added; commands run; migrations/configuration/deployment implications; and remaining risks.

## Definition of Done

- [ ] Supported Python version, package manager, project layout, and CI tooling were inspected and respected.
- [ ] Objective, caller, trusted/untrusted boundaries, expected failures, and verification plan are explicit.
- [ ] Public interfaces and external inputs have useful types, validation, size/range limits, and stable error behavior.
- [ ] Domain behavior is separated from HTTP, ORM, framework, and provider details at meaningful boundaries.
- [ ] Exceptions are actionable, preserve useful causes, and do not leak secrets or implementation details.
- [ ] Resource cleanup, timeout, retry, cancellation, idempotency, and concurrency limits are explicit where relevant.
- [ ] Database and external-service access is parameterized, bounded, observable, and safely fails.
- [ ] Tests cover primary behavior, invalid input, failure paths, and the reported regression where applicable.
- [ ] Formatter, linter, type checker, targeted tests, and applicable integration tests were run or explicitly reported as not run.
- [ ] Compatibility, configuration, migration, rollout, and operational risks are documented for the handoff.
