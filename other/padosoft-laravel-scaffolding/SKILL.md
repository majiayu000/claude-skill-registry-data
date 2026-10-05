---
name: padosoft-laravel-scaffolding
description: >-
  Use this skill when adding something new to a Laravel application — an endpoint, a controller, a service, a
  CRUD backend, a queued job, a test — "make me the API for X", "add the CRUD for Y", "I need a service that
  does Z" — and whenever a piece added earlier is half-wired: a route that answers 404, a policy that is
  never called, a request class that validates nothing because the controller reads `all()`, a job that is
  dispatched but has no queue configured. It lists the files each piece touches, in order. Do not use it to
  review existing code (padosoft-laravel-conventions) or for the security review.
license: MIT
compatibility: >-
  Any Laravel version: the list is about which pieces have to exist and be wired, which has not changed.
  Paths are examples — read the repository layout first.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The code is the easy part — what gets forgotten is the wiring.
  profiles: laravel
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: laravel, scaffolding, controller, service, crud, api, formrequest, policy, test
---

# Laravel scaffolding

The code is the easy part. What gets forgotten is the **wiring**: the route, the policy, the binding, the
test — each of which fails in its own quiet way.

The conventions the generated code must follow are in **`padosoft-laravel-conventions`**; the checks it must
survive are in **`padosoft-laravel-security-review`**.

---

## 0. Ask first, in one batch

- **what**: endpoint, controller, service, CRUD, job, test;
- **which domain/module** it belongs to — and whether that module exists;
- **who may call it**: guest, authenticated, a role, an owner. This answer decides the policy, and it is the
  one most often left implicit;
- **the shape of input and output**, and whether the response is shared with a frontend that already expects
  a shape;
- **synchronous or queued**, and if queued, on which connection and queue.

If the answer to "who may call it" is "the authenticated user", ask the follow-up: *any* authenticated user,
or only the owner of the record? That distinction is the whole of `SEC-IDOR-001`.

## 1. Endpoint / controller — the file list

| # | File | Skipping it means |
|---|---|---|
| 1 | The route, in the right route file and group | 404, or worse: the route exists without the group's middleware |
| 2 | `FormRequest` | Validation lives in the controller, or nowhere |
| 3 | DTO | An untyped array crosses every boundary |
| 4 | Controller | — |
| 5 | Service / action | The logic is in the controller and is not testable without HTTP |
| 6 | Policy + `authorize()` **called** | A policy that exists and is never invoked is not a control |
| 7 | `JsonResource` / response shape | The model is serialised whole, including what should not leave |
| 8 | Feature test, happy **and** failure path | — |
| 9 | Route list check | The route answers on the verb and path you think |

Steps 1, 6 and 9 are the ones that fail silently: everything compiles, the endpoint answers, and the
authorisation was never asked.

```bash
php artisan route:list --path=<fragment>     # verb, path, middleware, action
```

Read the **middleware column**: that is where you see whether auth actually applies.

## 2. Service

```php
final class DoTheThing
{
    public function __construct(private readonly ThingRepository $repo) {}

    public function __invoke(DoTheThingData $data): Thing
    {
        // one responsibility; no HTTP, no request(), no auth() in here
    }
}
```

- **No `request()`, no `auth()`, no `session()` inside a service.** Whatever it needs arrives as an argument,
  or it cannot be called from a command, a job or a test.
- Register it in the container only if it needs binding; otherwise let autowiring do it.
- A service returning `bool` to mean "it worked" is usually hiding a failure the caller needs — see
  **`padosoft-failure-visibility`**.

## 3. CRUD backend

Beyond the endpoint list: for each of index / show / store / update / destroy, decide **who may** — they are
rarely the same answer — and whether destroy is a soft delete. If it is, every listing and count elsewhere
needs to know (`padosoft-laravel-conventions` §4).

For the listing: pagination from the start, not "for now it returns everything". The dataset that makes it a
problem arrives in production, not in the fixture.

## 4. Queued job

```bash
php artisan queue:work --queue=<name>    # does the queue you dispatched to actually have a worker?
```

- The job orchestrates, the service implements.
- Set `$tries`, `$backoff` and `$timeout` deliberately; the defaults are a decision you did not make.
- `failed()` handles the permanent failure — and that is a place people leave empty, so the failure becomes
  a row nobody reads.
- Dispatch **after commit** if the job reads a row the current transaction is writing.
- Retryable vs permanent: fail explicitly on a permanent error rather than throwing something the queue
  retries sixteen times.

## 5. Test

A test written together with the code, not after: see **`padosoft-test-integrity`** for what makes a test
real. The minimum here:

- the happy path;
- **the authorisation path** — a user who must not, gets a 403;
- **one failure path**, actually provoked;
- database state restored between tests, and your own teardown before the framework's.

---

## Before declaring it done

```bash
php artisan route:list --path=<fragment>   # route + middleware
grep -rn "authorize(" app/Http/Controllers/<Controller>.php
php artisan test --filter=<TestClass>
vendor/bin/pint --test && vendor/bin/phpstan analyse    # or the project's equivalents
```

## Gotchas

- **A route outside the right group** loses the group's middleware — auth included — and still answers 200.
- **A policy is not a control until `authorize()` is called.** Registering it is not enough.
- **A `FormRequest` that the controller ignores** (reading `all()` instead of `validated()`) validates and
  then hands over the unvalidated payload anyway.
- **A job dispatched to a queue with no worker** is a silent hole: everything returns 202, nothing runs.
- **Do not invent the layout.** Read where the neighbouring modules put their services, requests and routes
  before creating files: this list is the shape, the repository has the paths.

## Checklist

- [ ] Route in the right file **and group**; `route:list` shows the expected middleware
- [ ] FormRequest, and the controller reads `validated()` / the DTO — never `all()`
- [ ] Logic in the service; no `request()`/`auth()` inside it
- [ ] Policy written **and** `authorize()` called on the path
- [ ] Response through a resource, not the raw model
- [ ] Job: tries, backoff, timeout, `failed()`, after-commit dispatch if needed, worker on that queue
- [ ] Tests: happy, authorisation, one real failure path
- [ ] Pint and static analysis clean

## Final report

```
Created: <what>  ·  module: <where>
Files: route · request · dto · controller · service · policy · resource · test
Authorisation: <who may, and where it is enforced>
Queue: <name> · tries/backoff/timeout · worker verified: yes|no
route:list middleware: <what it shows>
Pint / static analysis / tests: PASS | FAIL <detail>
```
