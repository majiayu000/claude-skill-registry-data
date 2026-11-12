---
name: rails-node-integration
description: Use when a Rails backend talks to a Node.js service (Express, Fastify, NestJS, Hono, BFF, or a Node Sidekiq replacement) — choosing the integration mode (HTTP, JSON-RPC, shared Postgres, queue), typing and validating the contract on both sides, sending CSRF and session credentials cross-origin, mapping Rails validation errors into the Node service's problem-details envelope, and routing observability across the language boundary.
license: MIT
---

# Rails and Node Backend Integration

## Purpose

This skill owns the **Rails-to-Node backend boundary** — the contract between a Rails server and a sibling Node.js service. It does NOT own either side's internals: Rails Active Record, Action Controller, and other Rails skills own the server; the `node-`-prefixed skills in `node-agent-skills` own the Node service. This skill owns only the seam between them: the contract, the credentials, the error envelope, and the cross-language routing.

This skill is the **symmetric mirror** of `node-agent-skills/skills/node-ruby-integration`. Either side can take the lead; the other side is consulted as a secondary. When both packs are installed, load both. When only one pack is installed, do the work for the installed side and report the other side's follow-up with the companion skill that owns it.

## Activate when

- A Rails backend calls a Node service (Express, Fastify, NestJS, Hono) over HTTP, JSON-RPC, gRPC, or a queue.
- A Node service consumes Rails JSON (REST, JSON:API, GraphQL-over-HTTP).
- A monorepo has both a Rails app and a Node service and a task touches both.
- A Sidekiq job is being replaced by a Node BullMQ worker (or vice versa) and the contract between the two must be preserved.
- Cross-origin credentials (cookies, CSRF tokens) need to flow from a Node BFF to a Rails API.
- Rails validation errors need to be mapped into a Node service's `application/problem+json` envelope (or vice versa).
- Observability (traces, logs, correlation IDs) needs to propagate across the Rails/Node boundary.

## Repository inspection

Before implementing a Rails-Node change, inspect both sides:

- **Rails side**: routes (`config/routes.rb`), controllers (`app/controllers/`), serializers (`app/serializers/`, or `Blueprinter`/`ActiveModelSerializers`/`Panko`), auth (`app/controllers/concerns/authentication.rb`, `config/initializers/devise.rb`), `config/database.yml`, `config/cable.yml`, `config/sidekiq.yml`, `Gemfile`, `db/schema.rb`.
- **Node side**: `package.json` (deps, scripts), `tsconfig.json` (strict mode), the framework adapter directory (`node_modules/express`, etc.), the route handlers, the validation library (`zod`/`valibot`/`@hono/zod-openapi`), the auth middleware, the persistence layer (Prisma/Drizzle/pg/Sequelize), `pnpm-workspace.yaml` or `turbo.json` if monorepo.
- **Shared contract**: is there a shared OpenAPI/JSON Schema? A shared TypeScript package generated from Rails routes (`railsroutes` gem, `oas` generator)? A `packages/contracts/` directory in a monorepo?

Resolve both versions: Ruby/Rails from `Gemfile.lock` + `bundle exec rails -v`; Node from `package.json` + `node -v`.

## Decision rules

- **This pack owns the Rails side and the seam.** The seam is the contract: the request/response shapes, the credentials, the error envelope, the observability headers. The seam is NOT the Node service's internal architecture.
- **Companion pack owns the Node side.** For the Node service's HTTP handler, validation, persistence, and observability internals, defer to `node-agent-skills/skills/node-ruby-integration` (the symmetric seam) and the `node-`-prefixed skills it routes to.
- **Never copy a `node-` skill into this pack.** Cross-pack work composes by loading both packs' skills, never by duplication. `AGENTS.md` (Companion packs section) prohibits copying.
- **Pick the integration mode first.** The four common modes:
  | Mode | When | Owner on Rails side | Owner on Node side |
  |---|---|---|---|
  | HTTP REST / JSON API | Rails is the API authority, Node is a client | `rails-action-controller` + this skill | `node-rest-api-design` + `node-ruby-integration` |
  | JSON-RPC / gRPC | Tight, method-call-style contract | `rails-action-controller` (mounts the endpoint) + this skill | `node-rpc-contracts` + `node-ruby-integration` |
  | Shared Postgres | Both sides read/write the same DB | `rails-active-record` + this skill (coordination only) | `node-postgresql-persistence` + `node-ruby-integration` |
  | Queue (Sidekiq ↔ BullMQ) | Async cross-language work | `rails-active-job` + this skill | `node-queue-engineering` + `node-ruby-integration` |
- **Credentials and CSRF are a seam concern.** Cross-origin cookies require `SameSite=None; Secure`, `credentials: 'include'` on fetch, and a CSRF strategy that works cross-origin (token endpoint, double-submit, or session-cookie + custom header). Both sides must agree.
- **Error envelope is a seam concern.** Rails renders `422` with `errors: {field: [...]}` (Active Model errors). Node services commonly render `application/problem+json` (RFC 9457) with `detail` and `errors[].field`. The mapping is bi-directional and owned here.
- **Observability headers are a seam concern.** Pick a correlation ID convention (`X-Request-ID`, W3C `traceparent`) and propagate it on every cross-language call. Both sides must log the ID.
- **Schema generation is a seam concern.** If Rails is the API authority, generate a contract (OpenAPI / JSON Schema / TypeScript types) and consume it from Node. Do not hand-type the contract on the Node side; it will drift.

## Implementation or review procedure

1. **Classify the task**: which of the four integration modes? If unclear, the task is ambiguous — ask before implementing.
2. **Inspect both sides**: see Repository inspection above.
3. **Load the symmetric companion**: if `node-agent-skills` is installed, also load `node-agent-skills/skills/node-ruby-integration`. If not installed, finish the Rails side and report the Node-side follow-up with `node-ruby-integration` as the owning skill.
4. **Implement the seam on the Rails side**: controller action, serializer, auth concern, error renderer, observability concern.
5. **Cross-link the contract**: if you generate a schema from Rails, the Node side should consume it (and the Node side should fail its build if the schema is missing or stale).
6. **Verify on both sides**: run Rails tests for the controller/serializer; run Node tests for the consumer. If only one side's tests exist, that is the verification surface; document the gap.
7. **Document the contract**: apply the `rails-node-backend-seam` pattern (choose-and-record the integration mode, write authority, and correlation-ID convention), and record the decision where the consuming repository keeps architecture decisions. Reference the decision from `router/ROUTING.md`'s "Rails and Node cross-stack routing" section.

## Anti-patterns / failure modes

- **Hand-typing the Rails API contract in the Node service.** Drift is guaranteed. Generate the contract from Rails and consume it.
- **Letting Rails serialize errors as `422` ad-hoc JSON when the Node consumer expects `application/problem+json`.** Pick one envelope and render it on both sides. The Rails side can wrap Active Model errors into problem+json via a `ActiveModel::Errors`-to-`problem` concern.
- **Cross-origin cookies without `credentials: 'include'` on fetch AND `SameSite=None; Secure` on the Rails cookie.** The cookie is silently dropped; auth fails mysteriously.
- **CSRF token endpoint not exposed to the Node BFF.** The BFF cannot forward the CSRF token; mutating requests fail with `ActionController::InvalidAuthenticityToken`.
- **Correlation ID set on the Rails side but not propagated by the Node service.** Traces are broken across the boundary.
- **Shared Postgres without an explicit write-authority table.** Both sides write the same row; lost updates. Pick one side as the write authority for each table.
- **Loading this skill for a pure Rails task with no Node involvement.** This skill is the seam only; pure Rails work routes to `rails-active-record` / `rails-action-controller` etc.
- **Loading this skill for a pure Node task with no Rails involvement.** Pure Node work routes to `node-`-prefixed skills; this skill is not the primary.

## Verification

- The Rails controller exposes the seam endpoint with documented request/response shapes (test: integration test that posts a payload and asserts the rendered shape).
- The Node consumer's tests fail if the Rails-generated contract is missing or stale (test: `npm test` in the Node service after a contract regeneration).
- Cross-origin credentials round-trip (test: a Rails integration test that sets a cookie and a Node-side test that reads it via `credentials: 'include'`).
- Error envelope is consistent across the boundary (test: assert a Rails 422 response and a Node consumer's error mapper produce the same shape).
- Correlation ID propagates (test: Rails integration test sets `X-Request-ID`; Node consumer logs the same ID).
- Run `bin/verify-change` from the ruby pack and `npm test && npm run validate` from the node pack (if installed).

## Composition

### When both packs are installed

| Concern on the seam | Primary | Secondary |
|---|---|---|
| Choosing the integration mode | `rails-node-integration` (this skill) | `node-ruby-integration` (companion) |
| Rails controller action | `rails-action-controller` | `rails-node-integration` |
| Rails Active Record model shared with Node | `rails-active-record` | `node-postgresql-persistence` |
| Rails auth + cross-origin credentials | `rails-authentication` | `react-agent-skills/browser-authentication` (if React BFF); `node-ruby-integration` (if Node BFF) |
| Node service HTTP handler | `node-rest-api-design` (companion) | `node-ruby-integration` (companion) |
| Node service persistence | `node-postgresql-persistence` (companion) | `node-ruby-integration` (companion) |

### When only the ruby pack is installed

Do the Rails side and the seam. Report the Node-side follow-up with the owning companion skill (`node-ruby-integration` for the seam, `node-rest-api-design` for the HTTP handler, `node-postgresql-persistence` for the persistence layer). Do not improvise Node guidance from this pack.

## Reference example

The Rails side of an HTTP seam. Rails owns the contract and renders an RFC 9457 problem+json error envelope the Node consumer maps 1:1; the correlation ID echoes back across the boundary.

```ruby
# app/controllers/api/v1/refunds_controller.rb
module Api
  module V1
    class RefundsController < Api::BaseController
      before_action :set_order

      # POST /api/v1/orders/:order_id/refunds — called by the Node BFF with a
      # forwarded session cookie and CSRF token.
      def create
        refund = @order.refunds.create!(refund_params)
        render json: RefundSerializer.new(refund).as_json, status: :created
      rescue ActiveRecord::RecordInvalid => e
        render_problem(422, "https://example.com/errors/validation",
                        "Validation failed.",
                        e.record.errors.map { |attr, msg| { field: attr, message: msg } })
      end

      private

      def set_order
        @order = policy_scope(Order).find(params[:order_id])
      rescue ActiveRecord::RecordNotFound
        render_problem(404, "https://example.com/errors/not-found", "Order not found.", [])
      end

      def refund_params
        params.expect(order: { refunds_attributes: [[:amount_cents, :reason]] })
              .require(:refunds_attributes)
              .map { |attrs| attrs.permit(:amount_cents, :reason) }
      end
    end
  end
end

# app/controllers/concerns/problem_json.rb — the seam's error contract.
module ProblemJson
  extend ActiveSupport::Concern

  def render_problem(status, type, detail, errors)
    response.set_header("X-Request-ID", request.request_id) if request.request_id
    render json: { type:, title: Rack::Utils::HTTP_STATUS_CODES[status], status:, detail:, errors: },
           status:, content_type: "application/problem+json"
  end
end

# config/initializers/session_store.rb — the cross-origin cookie contract for
# a Node BFF on another origin. Without SameSite=None the browser silently
# drops the cookie and auth fails mysteriously.
# Rails.application.config.session_store :cookie_store,
#   cookie: { same_site: :none, secure: true, httponly: true }
```

The Node side of the same seam (owned by `node-agent-skills / node-ruby-integration`; shown here only as the contract this skill must satisfy):

```ts
// The Node BFF consumer: forwards credentials, maps the problem envelope.
const response = await fetch(`${railsBaseUrl}/api/v1/orders/${orderId}/refunds`, {
  method: "POST",
  credentials: "include",                       // session cookie crosses origins
  headers: {
    "Content-Type": "application/json",
    "X-CSRF-Token": csrfToken,                  // forwarded from the token endpoint
    "X-Request-ID": requestId,                  // correlation ID propagates
  },
  body: JSON.stringify({ order: { refunds_attributes: [{ amount_cents, reason }] } }),
});
if (!response.ok) {
  const problem = await response.json();       // RFC 9457 problem+json from Rails
  throw new RailsProblemError(problem.errors); // [{ field, message }]
}
```

## Source foundation

- Rails guides: `api_only.md`, `routing.md`, `action_controller_overview.md`, `serializers.html.erb` (Rails 8 ships `ActiveModel::Serializers::JSON`).
- RFC 9457 (Problem Details for HTTP APIs) — the canonical error envelope.
- RFC 9110 (HTTP Semantics) — `SameSite`, `credentials: 'include'`, `Vary`.
- W3C Trace Context (`traceparent` header) — the cross-language correlation ID standard.
- This pack's `data/cross-pack/node-agent-skills.snapshot.yml` (v3 addition) — the pinned companion snapshot.
- The companion pack's `docs/CROSS_PACK_SCHEMA.md` — the shared v3 schema.

## Agent review checklist

- [ ] Did you classify the integration mode before implementing?
- [ ] Did you inspect both the Rails and Node sides before writing code?
- [ ] Did you load the companion `node-ruby-integration` skill (or report the follow-up)?
- [ ] Did you generate the contract from the API authority and consume it on the client side?
- [ ] Are cross-origin credentials and CSRF handled on both sides?
- [ ] Is the error envelope consistent across the boundary?
- [ ] Does the correlation ID propagate?
- [ ] Did you run verifiers on both sides?
