---
name: authz-review
description: Review an app's object-level and function-level access control (BOLA/IDOR, broken function-level authorization, mass assignment) route by route, then write a two-user test the developer can run against their own local or dev app. Use after adding or changing routes that take object IDs, tenant or user identifiers, or admin-only actions, when a user asks "can one user see another user's data", or as part of ship-check.
allowed-tools: Bash, Read, Grep, Glob
---

# NightVision Authorization Review

Broken access control is the most common serious flaw in apps built quickly: every route works for the user who wrote it, and nobody tries one user's ID with another user's session. This skill finds those gaps in the code and gives the developer a test that proves or disproves them.

What this is and is not: it is a code review plus a test the developer runs against an environment they own. It is not a NightVision scan result. Report what you found as review findings, never as NightVision findings, and never claim a route is safe because the review did not flag it.

## Workflow

1. **Inventory the routes.** If the repo has an OpenAPI spec from Source Intelligence, start from it: every operation is listed with its source file and line. After a `run-app-security-scan` run the spec is in `.nightvision/` (its path is `api_discovery.attached_spec_file` in `.nightvision/manifest.json`); a manual `nightvision openapi extract` writes `openapi-spec.yml` by default. Otherwise generate one with the `source-intelligence` skill, or read the router or controller definitions directly.
2. **Pick the routes that matter.** Keep any route that:
   - takes an object identifier in the path, query or body (`{id}`, `orderId`, `user_id`, `slug`, `fileKey`, a tenant or org ID);
   - lists or searches records;
   - creates or updates records from a request body;
   - performs an admin, billing, export, invite, role-change or delete action.
3. **Trace each route to its data access.** Open the handler at its file and line and follow it to the query. For each route record:
   - how the caller's identity is established (session, token, middleware), or that it is not;
   - whether the lookup is scoped to the caller (`owner_id`, `tenant_id`, a policy call, a row-level security policy), where, and whether the check runs before the data is used or returned;
   - for list routes, whether results are filtered by the caller;
   - for create and update routes, whether body fields are allowlisted or bound wholesale onto the model (mass assignment of `role`, `owner_id`, `tenant_id`, `is_admin`, `price`);
   - for privileged actions, whether a server-side role check exists.
4. **Classify each route** as `enforced` (scoped in the query or by a central policy that covers it), `missing` (no check you can find), or `unclear` (the check lives somewhere you could not follow, such as dynamic middleware or a database policy you cannot read). Do not upgrade `unclear` to `enforced`.
5. **Report** a table: method and path, identifier, how access is checked with `file:line`, and the verdict. Put `missing` first, then `unclear`.
6. **Write the two-user test** (see below) for every `missing` and `unclear` route, plus a sample of `enforced` ones.
7. **Fix only when asked**, using the patterns below, then rerun the test.

## The two-user test

Write a small script, `authz-test.sh` or the project's own test framework, that:

1. Takes two sessions for two ordinary test accounts from environment variables (`USER_A_TOKEN`, `USER_B_TOKEN`, or two cookie jars). The developer supplies these accounts; never create accounts in or point the test at an environment the developer does not own, and never at production.
2. As user A, creates or finds a resource and captures its ID.
3. As user B, tries to read, update and delete that ID, and lists the collection looking for it.
4. Passes only when every cross-user request is refused (403 or 404) and A's object never appears in B's list.
5. For privileged actions, calls them as an ordinary user and expects a refusal.
6. For mass assignment, sends `role`, `owner_id` or `tenant_id` in an update body and confirms the stored record did not change.

Print the exact request and response status for every failure, so the developer can see the gap without reading the script.

## Fix patterns

- Scope the query to the caller rather than checking after the fetch: `Order.objects.get(id=id, owner=request.user)`, `where: { id, ownerId: session.userId }`, `findByIdAndOwnerId`.
- Prefer one central policy layer (Django permissions, Pundit or CanCanCan, Spring `@PreAuthorize` with a domain check, ASP.NET resource-based authorization, CASL) over per-route `if` checks.
- Return 404 for objects the caller cannot see, so IDs do not leak which records exist.
- Allowlist writable fields with a serializer, DTO or form object.
- On Supabase or Postgres row-level security, the policy is the check: confirm RLS is enabled on the table and the policy compares to `auth.uid()`.
- Unguessable IDs (UUIDs) slow enumeration but are not access control; still add the check.

## Related skills

`secure-build` covers access-control rules to follow while writing code. `ship-check` runs this review as part of finishing an app. `app-security-scan` runs a NightVision DAST scan of the running app.
