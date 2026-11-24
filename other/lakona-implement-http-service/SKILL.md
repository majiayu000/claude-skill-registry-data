---
name: lakona-implement-http-service
description: Implement or update complete Lakona Application HTTP services in Server.Hotfix. Use when adding an operations endpoint, webhook, payment callback, or other request/response route; changing LakonaHttpService or LakonaHttpEndpoint declarations; selecting listener exposure; fixing HTTP manifest-to-Hotfix binding; or validating raw-body, cancellation, idempotency, status, and response behavior.
---

# Implement a Lakona HTTP Service

Implement Application HTTP as its own traffic plane: the initial Hotfix
generation freezes one route manifest whose host-assigned endpoint slots select
generation-pinned handlers returning materialized responses. Keep framework
hosting mechanics separate from product policy.

## Workflow

1. Read project instructions and any project HTTP architecture guidance.
   Detect the installed Lakona version, stable App project, Hotfix project,
   listener configuration, neighboring HTTP services, and tests. Complete this
   step when the actual project conventions and validation commands are known.
2. Define the product boundary from the request and repository evidence:
   caller, route purpose, listener exposure, authentication assumptions,
   timeout behavior, idempotency needs, and durable state owner. Ask for a
   product decision only when a security or business choice cannot be inferred
   safely. Classify the work as either a behavior-only change that preserves
   service/method/route identity and is eligible for in-process Hotfix reload,
   or a manifest change that requires a process restart.
3. Search all `[LakonaHttpService]` and `[LakonaHttpEndpoint]` declarations
   plus listener service names. Update an existing binding in place and
   preserve its service name, HTTP method, and route by default. Change that
   identity only when the requested protocol change is intentional and the
   restart requirement is explicit. Complete this step when service names and
   listener/method/route keys are collision-free.
4. Read [http-service-shapes.md](references/http-service-shapes.md) before
   editing a contract, handler, listener, signed request, or durable webhook.
5. Define or evolve one top-level public sealed
   `[LakonaHttpService("...")]` class in Hotfix. Annotate each public handler
   with `[LakonaHttpEndpoint(method, route)]`, accept `LakonaHttpCall`, and
   return exactly `ValueTask<LakonaHttpResponse>`. Application HTTP has no
   stable App interface or user-authored numeric method id.
6. Implement product behavior in the same Hotfix class. Use `call.Request`,
   `call.CancellationToken`, actors, and concrete HotfixComponent Store/Util
   dependencies. Stable infrastructure interfaces for configuration, secrets,
   and third-party clients remain valid; do not introduce a stable business
   Store interface merely to reach Hotfix logic. Use `lakona-implement-component`
   for resource initialization already required by the task. Treat method and
   route changes as protocol changes that require a process restart after the
   new Hotfix build.
7. Apply edge semantics explicitly. Validate bounded inputs, verify signatures
   against `RawBody`, authorize from trusted identity or stable dependencies,
   choose product status and headers, and route durable acceptance through an
   application-owned inbox or Store. An Actor may serialize the mutation, but
   its memory alone is not durable. Complete this step when retries and partial
   failure cannot silently duplicate state changes.
8. Expose the service only on the intended
   `Lakona:Http:Listeners[].Services` entries. Keep bind address, trusted edge,
   certificates, proxies, and authentication mechanism as explicit deployment
   or stable-host policy.
9. Reuse focused handler tests for affected success, rejection, cancellation,
   and idempotency behavior; add tests where coverage is missing. Use startup
   or integration coverage when listener
   isolation, generated publication, dependency activation, or request
   snapshot behavior cannot be proven by a unit test.
10. Validate the discovered stable App and Hotfix build graph, directly or
    through focused tests that build the same configuration, and
    run applicable repository guards. Complete the task only when generated
    validation accepts the service and runtime validation accepts its complete
    manifest and tested behavior supports every claimed outcome.

## Non-Negotiable Boundaries

- Business exceptions deriving from `System.Exception`, directly or indirectly,
  may remain in Hotfix and use `new` with runtime data. Do not mark them with
  `[HotfixComponent]` or register their error codes and inner exceptions in DI.
  Remove a mistaken marker when `LAKONA20060` reports it. For older versions
  reporting `LAKONA20037` on exceptions, upgrade and verify build plus loading;
  do not use component registration as a workaround.
- Application HTTP carries product request/response work without creating a
  Game Session, callback channel, resume flow, or reliable-push stream.
- Keep route declarations and product behavior together in Hotfix. Keep
  `Program.cs` as an infrastructure composition root.
- Use the detached request snapshot and return a materialized
  `LakonaHttpResponse`; framework adapters own ASP.NET request and response
  objects.
- Observe `call.CancellationToken` in asynchronous and nested work so the
  generation lease can drain at the mandatory request deadline.
- Reserve `/_lakona/**` for Management HTTP and select listeners through their
  configured service sets.
- Preserve exact raw request bytes until signature verification completes.
- Back durable webhook acceptance with an application-owned inbox or Store. An
  authoritative Actor may coordinate the operation only when the durable write
  completes before success; a successful in-memory return is not durability.
- Do not add dynamic `EndpointDataSource` publication, a catch-all application
  router, or a manifest-validation bypass to make route changes reloadable.
  Treat dynamic manifests as future framework architecture work rather than an
  application workaround.
- Follow the repository's `ValueTask` conventions and keep analyzer diagnostics
  enabled.

## Validation Scope

Apply the validation steps to affected contracts, reusing existing coverage and
adding tests only where meaningful coverage is missing. For non-behavioral,
low-impact edits, use relevant static checks. A test command may also satisfy
the build when it covers the same graph and configuration. Once relevant checks
and required stage gates pass, stop unless new changes, failures, or a concrete
unresolved risk justify more verification. Report any unverified outcomes.

## Completion Report

Report the Hotfix manifest change, handler behavior, listener exposure,
security and idempotency decisions, tests, and builds. Distinguish compile-time
shape validation, unit-tested product behavior, and runtime listener/manifest
validation. State `Hot reload eligible: yes/no` and
`Process restart required: yes/no`.
