---
name: nick-supabase-reference
description: Supabase-first reference and implementation skill for Nick's app stack. Use when writing Supabase queries, auth flows, RLS policies, storage rules, realtime features, edge-function integrations, migrations, or debugging Supabase behavior. Prefer this instead of guessing Supabase APIs or patterns. Bias toward product-led implementation choices, trust-aware access control, MVP discipline, and using only the Supabase features the product actually needs.
---

# Nick Supabase Reference

Use this as the default Supabase implementation/reference skill for Nick.

## Core job

Provide correct, current, production-oriented Supabase patterns that serve the actual product.

Do not optimize for using every Supabase feature. Optimize for:
- correct implementation
- product-fit auth and access patterns
- trust-sensitive data handling
- MVP-speed execution
- minimal unnecessary complexity
- safe separation between client-safe and privileged operations

## Strategy-first implementation inputs

When available, anchor Supabase decisions to:
- ICP / buyer
- end user vs economic buyer
- core workflow
- product wedge
- activation moment
- monetization model
- trust / compliance sensitivity
- MVP boundaries

If these are unclear, state assumptions and choose the narrowest viable pattern.

## Primary domains

- queries and mutations
- auth setup and flows
- profile/bootstrap patterns
- RLS and policy design
- storage buckets and policies
- realtime subscriptions
- edge functions
- migration planning
- TypeScript typing patterns

## Non-negotiables

- Do not guess Supabase APIs or patterns.
- Prefer documented/current Supabase patterns.
- Flag deprecated or legacy approaches when noticed.
- Always think through auth and RLS together.
- Always consider bootstrap/profile logic after signup when relevant.
- Always distinguish server-only usage from client-safe usage.
- Never expose privileged keys in client code.
- Do not add storage, realtime, or edge functions unless the product actually benefits from them now.

## Product-led Supabase rules

### Auth should follow the product motion
Choose auth patterns based on the real product:
- self-serve product
- team / organization product
- operator/admin-heavy internal tool
- trust-sensitive or compliance-adjacent workflow

Clarify:
- who signs in
- what they must see first
- what record must exist after signup
- what access should exist before and after bootstrap completes

Do not treat auth as isolated from onboarding, roles, and first value.

### RLS should be understandable and justified
Design policies around real access needs:
- row owner
- tenant membership
- operator/admin exception
- public read vs authenticated read

Prefer simple, testable RLS over clever policy logic.

If policy logic starts becoming complicated, question:
- whether the role model is too complex
- whether the schema is overbuilt for the current stage
- whether a privileged server path is more appropriate than widening client permissions

### Queries should serve UI/workflow needs
Shape queries around:
- the page or flow using the data
- sorting/filtering/pagination needs
- empty/loading/error states
- realistic related data needs

Do not over-fetch just because it is convenient.
Do not blame queries first when the real issue is policy failure.

### Storage should be intentional
Use Storage only when the product truly needs files.
When it does, define:
- bucket purpose
- who can upload
- who can view
- public vs signed/private access
- cleanup or replacement behavior if relevant

Do not add file infrastructure by default.

### Realtime should earn its complexity
Use Realtime only when it materially improves the product, such as:
- live collaboration
- operator dashboards that need freshness
- activity feeds or status changes that matter in-session

Do not add Realtime just because it exists.
Polling or refresh-based UX may be enough for MVP.

### Edge Functions should have a reason
Use Edge Functions when you need:
- secure server-side integration work
- webhooks
- privileged orchestration
- secret-bearing calls
- logic that should not run in the client

Do not add functions for trivial logic that belongs in app/server code or SQL.

## Default workflow

1. Identify what Supabase feature is involved.
2. Identify whether the work is client-side, server-side, database-side, or edge-function-side.
3. Identify the real user roles and access model.
4. Identify the product reason for the implementation choice.
5. Choose the safest current pattern.
6. Provide code/config with notes on risks, common mistakes, and deprecations.

## Default output sections

For meaningful Supabase work, include:
- Goal
- Product context / assumption
- Recommended pattern
- Code/config
- Auth/RLS implications
- Common failure points
- Deprecated patterns to avoid (if relevant)

## Common product-sensitive implementation guidance

### Signup/bootstrap
Explicitly define:
- what happens immediately after signup
- whether a profile row is created
- whether organization membership is created
- whether onboarding state is stored
- what happens if bootstrap partially fails

A very common bug is "signup works but the app is unusable afterward." Prevent that.

### Team / multi-tenant products
Explicitly define:
- organization / workspace model
- membership table expectations
- tenant-scoped queries
- admin/operator exceptions
- invitation/bootstrap flows

Do not assume tenant isolation without proving it in policy logic.

### Internal/admin tools
Prefer:
- privileged server-side reads/writes where appropriate
- limited client exposure
- clear operator roles
- audit-aware access patterns

Not everything in an internal tool needs to be user-facing RLS-driven client access.

## What not to add too early

Do not add these by default unless justified:
- complex multi-role auth flows
- broad storage architecture
- realtime subscriptions across the app
- edge functions for ordinary CRUD
- complicated policy layers before the actual role model is stable
- client-side privileged logic disguised as convenience

## Debugging lens

When Supabase behavior is failing, check in this order:
1. wrong environment / wrong key usage
2. auth/session state mismatch
3. bootstrap/profile/membership record missing
4. RLS policy mismatch
5. query shape mismatch to UI assumptions
6. storage/realtime policy mismatch
7. deprecated or legacy pattern

## Quality bar

A strong Supabase response should:
- use current, safe patterns
- keep auth/RLS/schema/query logic aligned
- support the real product workflow
- avoid unnecessary feature complexity
- explain likely failure modes clearly

## References

Read these as needed:
- `references/query-patterns.md` for query and mutation guidance
- `references/auth-patterns.md` for auth and profile/bootstrap guidance
- `references/rls-reference.md` for policy patterns
- `references/storage-reference.md` for buckets and file access rules
- `references/realtime-reference.md` for subscriptions and live UI updates
- `references/edge-functions-reference.md` for function patterns
- `references/deprecations-and-pitfalls.md` for what to avoid

## Bundled scripts

- `scripts/generate-supabase-task-brief.sh` — create a structured implementation brief
- `scripts/generate-rls-review-checklist.sh` — create a policy review checklist
- `scripts/generate-auth-flow-checklist.sh` — create an auth/bootstrap checklist
