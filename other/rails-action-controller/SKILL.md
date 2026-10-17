---
name: rails-action-controller
description: Use when implementing or reviewing Rails Action Controller HTTP boundaries including parameters, request and response semantics, sessions, cookies, callbacks, negotiation, conditional responses, streaming, and controller-level exception handling. Also covers routine controller actions, parameters, rendering, and redirects.
license: MIT
---

# Rails Action Controller

## Purpose

Treat Action Controller as the HTTP execution boundary between routing and application behavior.

The controller owns request interpretation, boundary input filtering, request-scoped state access, response construction, and controller-level HTTP lifecycle behavior. It should not become the owner of domain invariants, persistence workflows, authorization policy, external provider orchestration, or durable messaging merely because those concerns are reachable from an action.

## Activate when

- adding or changing Action Controller behavior beyond a simple CRUD action
- rendering Markdown responses with `render markdown:`
- changing params, strong parameters, nested input, or request metadata
- changing render, redirect, status, headers, content type, or response body behavior
- adding or changing sessions, cookies, or flash state
- adding or changing before_action, after_action, or around_action
- implementing HTML/JSON/XML or other request-format negotiation
- adding ETag, Last-Modified, conditional GET, or HTTP cache validators
- adding file downloads, streaming, or large response handling
- adding controller-level exception mapping with rescue_from
- debugging unexpected dispatch, double renders, missing responses, or request/response behavior

Simple CRUD actions, params handling, and status/render/redirect changes also route here; start them from `references/routine-changes.md`.

## Boundary ownership

| Concern | Controller owns | Prefer another boundary |
|---|---|---|
| HTTP parameter parsing/filtering | yes | domain validation for semantic rules |
| request metadata | yes | business identity derivation |
| authentication orchestration | boundary hook/collaborator | rails-authentication |
| authorization decision | invocation of existing policy | rails-security / policy boundary |
| persistence | orchestration | rails-active-record / database skill |
| business workflow | invocation | service/domain object |
| response mapping | yes | serializer/view for representation |
| sessions/cookies/flash | yes | auth/session subsystem for identity semantics |
| instrumentation | emit/observe | rails-observability |
| cache correctness | HTTP validator interaction | rails-caching |
| API provider calls | no | rails-api-integration |
| durable async work | enqueue/delegate | rails-active-job / messaging |
| route declaration | no | rails-routing |

## Repository inspection

Before changing a controller boundary, inspect:

1. Ruby and Rails versions.
2. config/routes.rb and the matching controller/action.
3. ApplicationController and inherited callbacks/modules.
4. Authentication and authorization hooks.
5. Existing parameter filtering conventions.
6. Request/response format conventions.
7. Session, cookie, and flash configuration.
8. Error handling and rescue_from mappings.
9. View/serializer/representation contracts.
10. HTTP cache validator and CDN/proxy conventions.
11. File/streaming/download helpers already used.
12. Request/integration/system tests and shared controller helpers.
13. Observability and log-filtering conventions.
14. Neighboring controllers for local conventions.

Resolve version-sensitive APIs before implementation. Newer Rails releases support params.expect; older supported versions may require require plus permit.

## Decision rules

1. Classify the change: request input and strong parameters, response/render/redirect contract, content negotiation, conditional GET, streaming and downloads, sessions/cookies/flash, controller callbacks, exception handling, or performance/testing.
2. Load the matching reference below before changing behavior. Routine controller action edits load `references/routine-changes.md` first and escalate only when a deeper boundary is in play.
3. Keep the controller a thin HTTP boundary: domain rules go to models or domain services, authorization to rails-authorization, and route shape to rails-routing.
4. Choose resource-loading placement from the request contract, not from a blanket style preference:
   - use a narrow `before_action` when the resource is a prerequisite shared by several actions or must exist before later callbacks/action execution;
   - use an action-local lookup when only one action needs it and that keeps the request flow clearer;
   - a memoized reader (`@resource ||= ...`) is permitted when lazy access or repeated access within the action genuinely simplifies the boundary, but it is not a default performance optimization;
   - never claim memoization is faster than a callback without workload-specific evidence.
5. For complex reads, prefer an explicit query/read boundary when the lookup becomes difficult to reason about, test, or scope in the controller.

## Critical invariants

- Do not use permit! merely to make an integration work.
- Strong parameters are an input boundary, not an authorization system and not a substitute for domain validation; never treat validation success as authorization.
- Do not infer authorization from the presence of a session value, route, header, cookie, or parameter.
- Do not catch StandardError broadly to turn unexpected failures into successful-looking responses.
- Do not enable cross-host redirects for untrusted input merely to preserve convenience behavior.
- Do not stream an unbounded database query, external provider, or object graph directly from a controller without a bounded producer and cleanup design.
- Keep controller callbacks narrow and action-scoped; they are request prerequisites, not business workflows or transactions.
- Resource loading is a boundary-placement decision, not a performance shortcut: callback-based loading and memoized readers must preserve the same authorization, tenant scope, failure semantics, and request contract.
- Do not treat `||=` memoization as inherently faster, cheaper, or more scalable; performance claims require a representative workload, baseline, and re-measurement.
- Use ETag/Last-Modified only when validator identity covers every representation dimension such as tenant, permission, and locale.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change reads request input, alters strong parameters or params.expect, or depends on request object semantics | [references/request-and-parameters.md](references/request-and-parameters.md) | Request boundary; Parameters and strong parameters; Request object semantics | `action-controller-request-boundary`, `strong-parameters-contract` |
| a change alters status codes, render/redirect behavior, formats, ETag/Last-Modified, or file/streaming responses | [references/responses.md](references/responses.md) | Response contract; Render and redirect semantics; Content negotiation; Conditional GET and HTTP cache validators; Streaming and downloads | `controller-response-contract`, `controller-content-negotiation`, `controller-streaming-download` |
| a change alters session/cookie/flash state, controller callbacks, rescue_from/exception mapping, or request security | [references/sessions-callbacks-exceptions.md](references/sessions-callbacks-exceptions.md) | Sessions, cookies, and flash; Controller callbacks; Exception handling; Security and privacy | `controller-session-cookie-boundary`, `action-controller-callback-contract`, `controller-exception-boundary` |
| a change has request-path performance impact or needs controller/request tests | [references/performance-and-testing.md](references/performance-and-testing.md) | Performance and capacity; Testing | `action-controller-testing` |
| the change is a routine controller action edit | [references/routine-changes.md](references/routine-changes.md) | Routine controller action changes | none |

## Reference example

A controller action with tenant-scoped lookup, strict strong parameters, and a declared exception-to-response mapping.

```ruby
class InvoicesController < ApplicationController
  before_action :set_invoice, only: %i[show update destroy]
  rescue_from ActiveRecord::RecordNotFound, with: :record_not_found

  def update
    if @invoice.update(invoice_params)
      render :show, status: :ok
    else
      render json: { errors: @invoice.errors }, status: :unprocessable_entity
    end
  end

  private

  def set_invoice
    # Scoped lookup: never Invoice.find(params[:id]) in a multi-tenant app.
    @invoice = current_account.invoices.find(params[:id])
  end

  def invoice_params
    params.require(:invoice).permit(:due_on, line_items_attributes: %i[id description amount _destroy])
  end

  def record_not_found
    head :not_found
  end
end
```

## Agent review checklist

- [ ] Rails/Ruby version resolved
- [ ] route/controller inheritance inspected
- [ ] authentication and authorization boundaries identified
- [ ] parameter contract is explicit
- [ ] request metadata is used only for HTTP concerns
- [ ] response status/body/format/headers are intentional
- [ ] redirects cannot create unsafe open redirects
- [ ] session/cookie payload is minimal
- [ ] callbacks are narrow and scoped
- [ ] supported formats are explicit
- [ ] conditional validators include required identity dimensions
- [ ] streaming/download lifecycle is bounded and authorized
- [ ] expected exceptions have explicit HTTP semantics
- [ ] sensitive values are not logged
- [ ] focused request tests cover failure and success paths
- [ ] cross-skill responsibilities remain explicit

## Failure modes

Avoid:

- forwarding all params into a model or service
- using validation success as authorization
- putting business workflows into before_action
- accepting arbitrary redirect_to params[:return_to]
- storing large/private state in cookie-backed sessions
- adding format branches without a contract
- generating cache validators from incomplete identity
- streaming without cleanup/backpressure/resource limits
- rescuing all exceptions into 200 OK
- assuming a hidden route provides security
- claiming caching or streaming improved performance without measurement.

## Verification

Run, as applicable:

1. focused request/controller tests
2. route verification when dispatch changed
3. security regression tests
4. serializer/view tests for representation changes
5. relevant observability/cache tests
6. bin/validate
7. the CI workflow for the branch.

Report actual test and CI evidence; never infer success from a clean diff.

## Source foundation

Primary current Rails sources:

- Rails Guide: Action Controller Overview — https://guides.rubyonrails.org/action_controller_overview.html
- ActionController::Parameters API — https://api.rubyonrails.org/classes/ActionController/Parameters.html
- ActionController::Redirecting API — https://api.rubyonrails.org/classes/ActionController/Redirecting.html
- ActionController::ConditionalGet API — https://api.rubyonrails.org/classes/ActionController/ConditionalGet.html
- ActionController::Rescue API — https://api.rubyonrails.org/classes/ActionController/Rescue.html

Framework behavior is interpreted against the repository's resolved Rails version and local conventions.

## Composition

This skill composes with rails-routing, rails-authentication, rails-security, rails-security-engineering, rails-api-integration, rails-observability, rails-caching, rails-active-storage, rails-active-job, rails-i18n, rails-test-engineering, ruby-clean-code, and ruby-tdd-refactoring.

## Rails Action Controller changes

For Action Controller and deep controller-boundary changes:
- inspect the Rails/Ruby version, routes, controller inheritance, ApplicationController callbacks, authentication/authorization, parameter filtering, request/response formats, session/cookie configuration, exception handling, cache validators, download/streaming code, observability, and request tests before implementation;
- classify the boundary as request input, response contract, session/cookie state, callback lifecycle, resource-loading placement, content negotiation, conditional response, streaming/download, or controller exception handling;
- use the smallest supported strong-parameter API for the resolved Rails version; prefer params.expect where supported and locally adopted, otherwise use require plus permit;
- treat every request value, header, cookie, session-derived identifier, redirect target, and file name as untrusted until its owning boundary validates or authorizes it;
- never forward raw params into persistence or domain code; strong parameters are an input boundary, not authorization;
- keep controller response contracts explicit: status, format, body/rendering, headers, redirects, empty-body semantics, and error representation;
- remember that redirect_to does not terminate Ruby execution; return when continuing the method could produce side effects or another response;
- preserve Rails open-redirect protections and never enable cross-host redirects for untrusted input;
- keep session/cookie payloads minimal, treat signed versus encrypted storage deliberately, and never use session/cookie presence as the authorization source;
- keep controller callbacks narrow and action-scoped; use them for request prerequisites, not business workflows, transactions, or large orchestration graphs;
- choose callback versus action-local resource loading from actual request prerequisites and local readability; memoized readers are an option for lazy access, not a repository-wide performance rule;
- when performance is claimed, measure callback versus memoized loading under the same representative workload rather than assuming `||=` avoids meaningful cost;
- define supported response formats explicitly and compose API wire contracts with rails-api-integration;
- use ETag/Last-Modified only when validator identity covers every representation dimension such as tenant, permission, locale, and other private variants;
- distinguish HTTP 304 transport behavior from application-state correctness and coordinate shared/private caching with rails-caching;
- authorize downloads before opening the source, bound producer/database work, and account for long-lived streams in request concurrency and runtime capacity;
- do not stream unbounded database/provider work directly from a controller without bounded production, timeout, disconnect, and cleanup semantics;
- use rescue_from only for expected errors with a stable HTTP contract and do not rescue StandardError broadly to hide programmer defects;
- coordinate error reporting with rails-observability rather than building one-controller global error handling;
- test status, content type, headers, redirect behavior, parameter rejection, authorization, callback scope, conditional 304 behavior, session/cookies, downloads, and expected/unexpected exception paths as applicable;
- never claim a controller contract is safe or performant without request-level evidence or focused regression tests.
