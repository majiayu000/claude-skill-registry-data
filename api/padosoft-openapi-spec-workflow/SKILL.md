---
name: padosoft-openapi-spec-workflow
description: >-
  Use this skill when changing a shared OpenAPI contract that other projects consume — adding or editing a
  field, an endpoint or a response schema in a spec package, or bumping and publishing it — and whenever the
  user says the mock and the real API disagree, a client method is missing a new parameter, the generated
  document fails to build, or a consumer broke after a spec release: it walks the places that must stay in
  sync (schema, mocks and per-tenant overrides, endpoint, client, tests), the changeset and version bump, and
  the build-and-call verification loop. Do not use it to implement the endpoint in the API that serves it
  (padosoft-hono-api-conventions) nor for its security review.
license: MIT
compatibility: >-
  A spec-first repository that publishes an OpenAPI contract plus a typed client, with a mock server. Assumes
  Node.js 18+/Bun and, for the release flow, Changesets.
metadata:
  version: 0.2.0
  author: Padosoft
  summary: A published contract other projects depend on — change it in every place, once.
  profiles: api, node
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: openapi, spec, schema, zod, mock, client, changeset, contract, versioning
---

# OpenAPI spec workflow

In a spec-first repository the contract is published and **other projects depend on it**. A field added in
one place and forgotten in four others does not fail here: it fails in the consumer, after the release.

This skill is the sync list and the verification loop.

---

## 1. Before touching anything: what kind of change is it?

| Change | Bump | Consumers |
|---|---|---|
| New optional field, new endpoint | **minor** | Keep working |
| Bug fix, mock or doc update | **patch** | Keep working |
| Field removed, type changed, field made required | **major** | **Break** — announce it |

Making an optional field required is a breaking change even though nothing is deleted. If you are about to
do it, say so before writing code: it is usually cheaper to add a second field.

## 1b. Where the contract comes from, and what it must not invent

A specification maintained by hand, next to the routes rather than from them, drifts the moment a route, a
permission or a path parameter changes — and nothing fails.

- **Generate the first contract from the same concrete route table the server uses.** That catches an
  omitted route and a method/path mismatch immediately, which is exactly what review does not catch.
- **Keep the transport generator separate from the domain schemas.** Generic placeholders are useful for
  discovery, and they must never be mistaken for a complete versioned payload contract or for proof that a
  client can be generated from it.
- **Reference the versioned schema, never hand-write a second copy of a payload in the spec.** A duplicated
  shape is a new source of drift with nothing to keep it aligned. Model the transport envelope locally and
  point at the schema package for the rest. An endpoint whose domain response is not settled stays visibly
  generic — better than a plausible contract nobody validated.
- **A documented route has to be reachable from the real boot path.** Handler tests can be complete while
  the route is dead, because the HTTP shell only delegates a narrower prefix. Keep the prefix allowlist and
  the route registry aligned, and cover the boot itself — this matters most for the provisioning and
  administrative endpoints, where "documented but unreachable" looks identical to "implemented".
- **The specification cannot describe a stream's vocabulary.** It documents the endpoint; it says nothing
  about which event types exist or what they carry. Keep a small event-type registry as the single source
  for the asynchronous description, and have the stream adapter consume that same vocabulary — otherwise a
  consumer discovers a transport with no stable message semantics.
- **Some invariants no generated schema can express**: cross-field rules, rejection of unknown fields,
  references to host-held secrets, comparators that are only valid in combination. Those belong in a source
  validator that runs before execution, with the runtime check kept as defence in depth.

## 2. The sync list

A change to a schema touches **more than one file**. Walk the list; the ones that do not apply, say so.

1. **The schema** — the type definition itself.
2. **The mock data**, including the **per-tenant overrides**. This is the step that gets forgotten: the
   default mock is updated, the per-client ones are not, and the client tests pass while one tenant serves a
   response without the field. Every mock carries the new field, **including optional ones**.
3. **The mock index/map**, when a file is added or removed — not when a field is added to an existing one.
4. **The endpoint definition**, so it points at the updated schema. Update the description too.
5. **The mock controller**, when it builds the response **by hand** instead of spreading the fixture: a
   manually built object silently drops the new field.
6. **The typed client**: a new query parameter must reach the method signature *and* its documentation.
7. **The tests**: cover the new field. If there is no test for that endpoint, write one.

## 3. Changeset and release

Every new feature, new endpoint or breaking change gets a changeset **before the commit**.

```markdown
---
"@scope/openapi-spec": minor
"@scope/api-client": patch
---

What changed, in one line that a consumer can read.
```

The changeset text ends up in the consumers' changelog: write it for someone who has not seen the PR.

## 4. Verification loop

Do not trust the build alone — a contract that compiles can still serve the wrong document.

```bash
# 1. build (this is slow: ask the user before running it)
bun run build

# 2. mock server in the background
bun run mock &

# 3. the generated document must actually serve
curl -fsS localhost:{port}/openapi.json | head -5

# 4. call the endpoint you touched and look at the field
curl -fsS "localhost:{port}/v1/{endpoint}" | grep -o '{new_field}'
```

Step 3 is the one that catches the real failures: the code compiles, and the document generation throws at
runtime.

## 5. Verify the commit contents

```bash
git show --stat HEAD
```

Compare the file count against what you expected to change. **`git add -A` silently skips files excluded by
`.gitignore`**, with no error and no warning.

*This happened:* a generic `logs/` pattern, written for runtime logs, swallowed a source directory named
`otel/logs/`. Build, server and tests were green locally; the files were simply absent from the commit, and
the endpoint did not exist for anyone else.

If files are missing:

1. `git status --short` and compare with the expected list.
2. `git check-ignore -v <path>` to confirm why.
3. If they are legitimate sources, add a **negation** to `.gitignore` (`!**/otel/logs/`). Do **not** use
   `git add -f`: it fixes this commit and leaves the trap armed for every future file in that folder.

---

## Gotchas

- **Tightening a schema breaks the fixtures written under the looser one.** Making a field mandatory
  exposes every previously accepted but semantically invalid fixture at the API boundary. They are
  dependents of the contract and are updated in the same change — see **`padosoft-contract-changes`**.

- **The per-tenant mocks are the ones that get forgotten.** The default one is right there; the overrides are
  in another folder.
- **A mock controller that builds the response by hand** drops new fields without failing anything.
- **A "literal" path segment is not a version.** When a path segment is fixed by an external standard (the
  `/v1/` of the OTLP protocol, a webhook path a provider calls), it does not migrate with your API version.
  Write it down next to the route, or someone will "fix" it during the v2 migration.
- **Mounting a route with an empty path string is not the same as `"/"`.** One of the two produces a doubled
  slash in the generated document or in the route index, and the mismatch surfaces far from the cause. Decide
  which one each layer wants, and comment it.
- **Lenient in the request, strict in the response.** An invalid optional input (a bad language code) is
  treated as absent and resolved by the server fallback — never a 422 caused by that field alone. The same
  field in a response stays strict: the documented contract does not bend.
- **A schema wrapper that swallows errors is not introspectable.** A "catch"-style wrapper hides the
  underlying type from the document generator and the build fails with an unknown-type error: declare the
  type and enum metadata explicitly, so the generated document is identical to the strict one.
- **Ask before the full build.** It is slow, and the user often has more edits queued.

## Checklist before committing

- [ ] Bump level decided (major/minor/patch) and breaking changes announced
- [ ] Schema updated
- [ ] Default mock **and** every per-tenant override carry the new field
- [ ] Mock index updated (only if a file was added/removed)
- [ ] Endpoint points at the updated schema, description current
- [ ] Mock controller returns the field (check if it builds the object by hand)
- [ ] Client method and its docs updated for new parameters
- [ ] Tests cover the new field; created if absent
- [ ] Changeset written, readable by a consumer
- [ ] Build + mock + real call verified
- [ ] `git show --stat HEAD` matches the expected file count

## Final report

```
Change: {what} on {endpoint/schema}     Bump: major|minor|patch
Synced: schema · mocks ({n}, tenants: {which}) · index · endpoint · controller · client · tests
Not applicable: {steps, with reason}
Verification: build PASS | openapi.json 200 | field present in the response
Changeset: {file}
Commit: {n} files, matching the expected list
Breaking for consumers: {no | yes, which and who was told}
```
