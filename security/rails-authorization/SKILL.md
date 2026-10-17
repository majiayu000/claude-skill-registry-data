---
name: rails-authorization
description: Design and review authorization as an explicit Rails policy, resource-scope, tenant, and execution-boundary contract.
license: MIT
---

# Rails Authorization Engineering

Authorization answers what an already identified actor is allowed to do to a resource in a context. Authentication establishes identity; authorization establishes permission. Do not merge the two contracts.

## Purpose

Treat authorization as an explicit server-side permission boundary covering actor, action, resource, tenant, context, execution boundary, and denial semantics.

## Activate when

Use this skill for policy objects, Pundit, CanCanCan, custom authorization, roles or permissions, protected controller/service/job/API/Action Cable actions, object-level authorization and IDOR prevention, tenant isolation, collection authorization, contextual permissions, authorization caching, auditability, and security regression work.

## Repository inspection

Before changing authorization:

1. Resolve Ruby, Rails, and authorization dependency versions.
2. Identify the authoritative authorization mechanism already used.
3. Locate policy/ability/permission classes and base abstractions.
4. Inspect controller, service, job, API, mailer, and realtime entry points.
5. Identify tenant/account ownership boundaries.
6. Inspect routes and resource lookup before authorization.
7. Inspect tests and factories for existing authorization contracts.
8. Search for bypasses such as direct find-by-ID, ad-hoc role checks, and unscoped queries.
9. Inspect background-job and cached-result paths.
10. Preserve repository conventions unless there is evidence they are unsafe.

Do not introduce a second authorization framework merely because it is familiar.

## Authorization model

Model authorization as:

authorize(actor, action, resource, context) -> allow | deny

Context may include tenant/account, organization membership, resource state, ownership, delegated authority, time, feature state, or service identity. Keep policy inputs explicit and avoid hidden global state.

## Policy boundary

A policy should own a coherent permission decision, not persistence, rendering, authentication, or unrelated workflows.

Good policy responsibilities include action permission, ownership, role/capability checks, state-dependent permission, contextual constraints, and policy composition.

Avoid policies that mutate resources or perform network calls.

## Object-level authorization

Resource lookup and authorization must be composed deliberately.

A direct Model.find(id) followed by authorization can still expose cross-tenant existence through lookup behavior. Prefer an authorized relation or equivalent tenant/resource boundary before resolving the object.

The exact API depends on the authorization library and resolved version.

## Collection authorization

Authorizing one member does not authorize a collection.

Define a separate scope contract for index/list endpoints, search, exports, reports, associations, dashboards, and background enumeration.

The collection scope must be enforced at the data-access boundary, not merely filtered after loading rows.

## Tenant isolation

Treat tenant/account membership as a security boundary.

For every tenant-owned resource determine the authoritative tenant identifier, actor membership check, resource tenant relationship, cross-tenant lookup behavior, nested association behavior, background-job behavior, cache-key isolation, and export/report isolation.

Never trust a client-supplied tenant ID as proof of tenancy.

## Roles, permissions, and contextual authorization

Prefer capabilities that express the actual operation over scattered role-name conditionals.

Distinguish role, permission/capability, ownership, and contextual condition. Do not turn every business condition into a global role.

## State-dependent authorization

Authorization often depends on resource state such as draft/published, active/suspended, or open/closed.

Keep authorization state checks aligned with the domain invariant. If a state transition is security-sensitive, enforce the invariant transactionally where necessary.

## Controllers and APIs

Authorization must happen server-side before the protected side effect.

1. Authenticate the actor.
2. Establish tenant/context.
3. Resolve an authorized resource scope.
4. Authorize the action.
5. Validate input.
6. Perform the side effect.
7. Return the deliberate denial/not-found contract.

Do not use frontend route guards as authorization.

GraphQL endpoints reach the same records through many query paths, so authorizing the `/graphql` controller action is not enough. Enforce the policy on every type, field, mutation, and list. The graphql-ruby hooks are in the GraphQL reference of `rails-api-integration`; this skill still owns the decision.

Verify denial with tests, not by trying an action by hand. For each protected action, a test as an actor without permission must observe the deliberate outcome: Pundit's `Pundit::NotAuthorizedError`, CanCanCan's `CanCan::AccessDenied`, or the repository's own denial response. A manual console or browser check proves nothing for the next change.

## Service objects and domain workflows

A service invoked from multiple entry points must not assume that the controller already authorized it.

Choose an explicit boundary: authorize at the service boundary for security-sensitive application operations, or require an already-authorized capability/context and make that contract explicit.

Do not silently trust a caller because a controller normally calls the service.

## Background jobs

Jobs run outside the original request authorization context.

Never serialize live credentials merely to carry authorization. Pass stable identifiers, re-resolve actor/tenant/resource state at execution time, and re-authorize the operation.

Define behavior for deleted, disabled, or membership-revoked actors. For destructive jobs, stale authorization must fail closed.

## Action Cable and realtime

Authorize connection identity, channel subscription, stream/resource access, and actions that mutate state.

A valid WebSocket connection is not blanket authorization for every stream or action. Re-check resource authorization when the security boundary changes.

## Webhooks and service identities

Inbound webhooks need authenticity verification and an explicit authorization model. A valid signature proves origin according to the integration contract; it does not automatically grant arbitrary application privileges.

Service-to-service identities should have bounded capabilities.

## Authorization versus validation and strong parameters

These are separate controls:

- strong parameters: which input fields may be assigned;
- validation: whether data is structurally/domain-valid;
- authorization: whether this actor may perform the operation.

Passing strong parameters never implies permission.

## Fail closed

For security-sensitive operations, missing actor, unknown tenant, missing policy, ambiguous ownership, and stale membership must deny according to an explicit safe failure contract.

Do not convert authorization exceptions into success or silently skip authorization because a policy is unavailable.

## TOCTOU and transactional boundaries

If authorization depends on mutable state, identify the gap between permission check and mutation.

Examples include membership revoked after authorization, ownership changed, or approval state changed.

For security-critical invariants, combine authorization with the appropriate transaction, lock, and database constraint strategy. Authorization alone is not a concurrency primitive.

## Caching

Never cache an authorization decision without including every input that can change the decision.

Cache identity may need actor, tenant, action, resource/version, permission version, and policy/context version.

When membership, role, ownership, or policy state changes, define invalidation semantics. Prefer short-lived caching when invalidation is difficult.

## Audit and observability

Record security-relevant authorization outcomes where required: actor, tenant, action, resource type/id, decision, reason/category, and correlation ID.

Do not log secrets or sensitive request data merely to explain a denial. Use bounded reason codes rather than arbitrary policy internals.

## Testing strategy

Test both allow and deny paths.

Required categories include actor/resource ownership, cross-tenant access, collection scope, role/capability boundaries, resource state, missing/disabled actor, direct service invocation, background-job re-authorization, API authorization, Action Cable subscription/action authorization, stale membership, authorization-cache invalidation, concurrent state changes where relevant, IDOR regression, and enumeration-safe denial behavior.

Prefer policy/unit tests for decision logic and request/system tests for boundary wiring.

## Reference example

Authorization as objects: a policy answering one question per method, and a scope that owns the query boundary.

```ruby
class InvoicePolicy
  def initialize(user, invoice)
    @user = user
    @invoice = invoice
  end

  def show?    = owner? || @user.admin?
  def destroy? = false          # invoices are voided, never destroyed

  private

  def owner? = @invoice.user_id == @user.id
end

class InvoiceScope
  def initialize(user, scope)
    @user = user
    @scope = scope
  end

  def resolve
    @user.admin? ? @scope.all : @scope.where(user_id: @user.id)
  end
end

# Controller usage:
#   head :forbidden unless InvoicePolicy.new(current_user, @invoice).show?
#   @invoices = InvoiceScope.new(current_user, Invoice).resolve
```

## Agent review checklist

- Is authentication distinct from authorization?
- Is there one authoritative authorization mechanism?
- Are resource lookup and authorization safely composed?
- Is collection scoping enforced at the query boundary?
- Is tenant isolation explicit?
- Are jobs, services, and realtime independently protected?
- Are denial semantics deliberate?
- Does mutable authorization state create a TOCTOU risk?
- Are authorization caches correctly keyed and invalidated?
- Are allow and deny paths executable tests?
- Is the change limited to the requested boundary?

## Verification

For an authorization change:

identify mechanism
-> inspect lookup/scope boundaries
-> define permission and tenant contracts
-> protect service/job/API/realtime boundaries
-> test allow/deny and regression cases
-> run security/contract validation
-> inspect CI evidence

Do not claim authorization safety without verifying the actual repository path.

## Source foundation

Primary Rails security guidance:
https://guides.rubyonrails.org/security.html

The repository may use Pundit, CanCanCan, Rails-native mechanisms, or custom policy code. Framework/library APIs must be verified against resolved dependency versions.

Related skills: rails-authentication, rails-security, rails-security-engineering, rails-action-controller, rails-active-record, rails-active-job, rails-action-cable, rails-database-engineering, rails-test-engineering.

## Rails authorization changes

For authorization changes:
- resolve the Ruby/Rails and authorization-library versions and identify the repository's authoritative mechanism before implementation;
- keep authentication and authorization separate; authentication establishes identity while authorization establishes permission;
- inspect resource lookup and collection scopes for IDOR and cross-tenant enumeration before adding policy checks;
- treat tenant/account membership as a security boundary and never trust a client-supplied tenant identifier as proof;
- reuse the existing Pundit, CanCanCan, custom policy, or capability mechanism instead of creating a parallel policy engine;
- authorize services, jobs, APIs, and Action Cable independently when they can be invoked outside the original controller request;
- re-resolve mutable membership/resource state in background jobs and fail closed when authorization is stale;
- keep strong parameters, validation, and authorization as distinct controls;
- review TOCTOU windows when authorization depends on mutable state and coordinate with transactions, locks, and database constraints;
- include tenant, actor, action, resource, and relevant permission version in authorization cache identity and define invalidation;
- never log credentials or sensitive policy inputs merely to explain an authorization decision;
- add deterministic allow/deny, cross-tenant, collection-scope, direct-service, job, API/realtime, and IDOR regression tests;
- verify the actual repository contract and report only observed validation evidence.

## Authentication and authorization boundary

authentication and authorization remain separate concerns: authentication establishes identity and session state; authorization decides permitted actions within that context.
