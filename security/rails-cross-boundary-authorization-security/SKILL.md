---
name: rails-cross-boundary-authorization-security
description: Design and review authorization as a composed security boundary across controllers, services, jobs, APIs, Action Cable, engines, operational commands, events, tenants, and caches.
license: MIT
---
# Rails Cross-Boundary Authorization and Security Composition

## Purpose
Use this skill when one security-sensitive operation can be reached through more than one execution boundary, or when authorization state must cross controllers, services, jobs, APIs, realtime channels, engines, maintenance commands, events, or cached results.

## Activate when
Activate for cross-entry-point authorization, controller/service authorization parity, tenant context propagation, background re-authorization, API and Action Cable authorization composition, engine authorization, operational-command authorization, event consumer authorization, capability propagation, denial-contract consistency, authorization caching, or authorization audit behavior.

## Core contract
Authentication establishes an actor. Authorization decides whether that actor or execution identity may perform a specific action on a specific resource in an explicit context. Security composition means every entry point reaches an equivalent authoritative decision boundary without trusting a weaker caller.
Never treat a controller check as proof that a service, job, event consumer, engine, task, or channel is authorized. Never treat possession of an identifier, Global ID, signed token, role name, or tenant ID as authorization by itself.

## Repository inspection
Resolve Ruby/Rails and authorization dependency versions. Identify the authoritative policy/ability/permission mechanism. Build the call graph for the protected operation across controllers, services, jobs, events, API endpoints, Action Cable, engines, tasks, and scheduled workflows. Inspect resource lookup, tenant scope, actor/context propagation, caches, audit events, and denial semantics.

## Authorization composition model
Model a protected operation as authorize(actor, action, resource, context) -> allow or deny. Make actor, action, resource, tenant/account, resource state, delegated authority, service identity, and relevant execution context explicit.

## Resource resolution
Authorization and resource lookup must be composed deliberately. Prefer resolving an authorized scope before object access when tenant or ownership isolation matters. Avoid broad object lookup followed by a late policy check when lookup itself reveals cross-boundary existence.

## Controller and service parity
When a service is callable from multiple entry points, its security contract cannot depend on one controller. Either authorize the application operation at the service boundary or require an explicit authorized capability/context and enforce that contract.

## Background re-authorization
Background execution happens after the originating request. Membership, ownership, resource state, role, or account status may change. Re-resolve security-sensitive context at execution time rather than serializing bearer authorization state.

## API composition
APIs need authentication, context/tenant establishment, authorized resource resolution, action authorization, validation, side effect, and deliberate denial semantics. HTTP status alone is not a substitute for a coherent authorization contract.

## Realtime composition
Action Cable or other realtime boundaries need authorization at the connection, subscription/resource, and sensitive action levels as appropriate. A valid connection must not automatically confer access to every stream or mutation.

## Engine composition
Mountable engines and Railties run inside a host but may have independent controllers, routes, policies, and resources. Keep engine authorization explicit and do not assume host controller checks automatically cover engine entry points.

## Operational and administrative commands
Rake tasks, runner commands, and maintenance workflows may bypass HTTP authentication entirely. Sensitive operational commands need explicit operator identity, environment gates, authorization/capability checks, and audit evidence when the threat model requires them.

## Event and message consumers
Asynchronous consumers may execute long after the originating authorization decision. Carry stable business identity/context as needed, but re-evaluate current authorization or business ownership at the consumer boundary for sensitive effects.

## Capability propagation
A capability may be passed across layers when its scope, lifetime, audience, and authorization basis are explicit. Prefer narrow capability objects or context contracts over ambient current-user globals or serialized bearer credentials.

## Denial semantics
Different boundaries may map denial to 403, 404, discarded job, rejected subscription, skipped event, or command failure. The mapping should preserve the security intent and avoid unnecessary existence disclosure.

## Authorization caching
Authorization results are security-sensitive cached state. Define cache identity using actor, tenant/context, action, resource, and relevant policy version/state. Define invalidation or bounded TTL when membership, ownership, role, or resource state can change.

## Audit and evidence
Audit sensitive decisions at the boundary where the actual allow/deny outcome is authoritative. Avoid emitting secrets or excessive payloads. Record enough actor/context/resource/action information to support operational investigation.

## Security testing strategy
Test each entry point and the shared authorization boundary. Include cross-tenant access, stale membership, revoked permissions, direct service invocation, delayed jobs, event replay, engine routes, operational commands, realtime subscriptions, cache staleness, and denial semantics.

## Anti-patterns / failure modes
Avoid controller-only authorization, duplicated policy logic, ambient authorization state, trusting serialized roles or tenant IDs, signing without authorization, Global ID as permission, unscoped object lookup, stale background authorization, cache hits after revocation, engines assumed secure because the host is secure, maintenance tasks assumed trusted, and inconsistent bypass paths.

## Reference example

Authorization re-checked at the execution boundary, because the controller check proves nothing once the job runs later.

```ruby
class DestroyTenantResourceJob < ApplicationJob
  def perform(actor_id, resource_id)
    actor = User.find(actor_id)
    resource = Resource.find(resource_id)

    # The job re-authorizes: the controller's check happened in another request,
    # possibly hours ago, under different records.
    raise AuthorizationError, "cross-tenant access" unless resource.tenant_id == actor.tenant_id

    resource.destroy!
  end
end

class ResourcesController < ApplicationController
  def destroy
    resource = current_tenant.resources.find(params[:id])
    DestroyTenantResourceJob.perform_later(current_user.id, resource.id)
    head :accepted
  end
end
```

## Agent review checklist
- [ ] authoritative authorization mechanism identified
- [ ] all entry points mapped
- [ ] actor/action/resource/context explicit
- [ ] resource lookup is security-aware
- [ ] tenant isolation composed
- [ ] service calls cannot bypass authorization
- [ ] background execution re-authorizes where required
- [ ] API/realtime/engine/task boundaries reviewed
- [ ] capability propagation is explicit and bounded
- [ ] denial semantics are deliberate
- [ ] authorization cache identity/invalidation reviewed
- [ ] sensitive decisions are auditable
- [ ] cross-boundary regression tests exist

## Verification
Resolve versions -> identify authoritative authorization mechanism -> map every entry point -> define shared actor/action/resource/context contract -> inspect resource lookup and tenant scope -> secure each boundary -> test stale/revoked/cross-tenant scenarios -> verify denial/cache/audit behavior -> run repository validation -> inspect CI evidence.

## Source foundation
- https://guides.rubyonrails.org/security.html
- https://guides.rubyonrails.org/action_cable_overview.html
- https://guides.rubyonrails.org/engines.html
- https://guides.rubyonrails.org/active_job_basics.html

## Rails cross-boundary authorization/security changes

For authorization or security changes spanning multiple execution boundaries:
- resolve Ruby/Rails and authorization dependency versions first;
- identify the repository's one authoritative authorization mechanism;
- map every entry point for the protected operation, including controllers, services, jobs, APIs, realtime channels, engines, tasks, scheduled workflows, and event consumers;
- define actor, action, resource, tenant/account, state, and execution context explicitly;
- prefer authorized resource scopes before object resolution where lookup itself is security-sensitive;
- do not rely on controller authorization to protect direct service, job, task, event, engine, or realtime callers;
- re-authorize sensitive work when execution is delayed or permissions can change after enqueue/publication;
- treat Global IDs, signed tokens, tenant IDs, role names, and serialized context as identity/input, not authorization by themselves;
- define deliberate denial behavior per boundary without unnecessary existence disclosure;
- review authorization caches for complete keys, tenant isolation, policy inputs, invalidation, and bounded freshness;
- emit audit evidence at the authoritative decision boundary when required, without secrets;
- test cross-tenant, revoked, stale, direct-invocation, replay, cache-staleness, and alternate-entry-point scenarios;
- do not introduce a second authorization framework unless repository evidence requires it.
