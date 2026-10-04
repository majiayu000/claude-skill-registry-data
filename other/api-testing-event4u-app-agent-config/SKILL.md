---
model_tier: medium
name: api-testing
description: "Use when writing API endpoint tests — integration tests, contract validation, response assertions, mocked external services — even when the user says 'test this route' without naming API testing."
domain: quality
workspaces:
  - engineering
packs:
  - engineering-base
---

# api-testing

## When to use

Use this skill when writing or reviewing API endpoint tests — integration tests,
contract validation, response structure checks, or external service mocking.

## Procedure: Write API tests

1. **Understand the endpoint** — Read the controller, form request, and existing tests. Understand expected behavior, edge cases, and auth requirements before writing anything.
2. **Set up test data** — Use seeders (preferred) or factories. Mock external services with `Http::fake()`.
3. **Enumerate test cases** — Run the [`test-case-discovery`](../test-case-discovery/SKILL.md) funnel first; cover success, validation errors, authorization failures, and edge cases — floor per behavior: 1 happy + 1 boundary + 1 error (+1 abuse case; on data-returning endpoints the three `broken-access-control` negative tests are mandatory).
4. **Assert response** — Check status code, JSON structure, data values. Use `assertJsonStructure()`.
5. **Verify** — Run the test. Must pass. Check no flaky assertions (no time-dependent, no random ordering).

### Example

```php
describe('GET /api/v1/projects', function () {
    it('returns paginated projects for authenticated user', function () {
        $user = loginAsTestUser();

        $response = $this->getJson('/api/v1/projects');

        $response->assertOk()
            ->assertJsonStructure([
                'data' => [['id', 'title', 'status']],
                'meta' => ['current_page', 'per_page', 'total'],
            ]);
    });

    it('returns 401 for unauthenticated request', function () {
        $this->getJson('/api/v1/projects')
            ->assertUnauthorized();
    });

    it('returns 403 when user lacks permission', function () {
        loginAsRestrictedUser();

        $this->getJson('/api/v1/projects')
            ->assertForbidden();
    });
});
```

## Test categories

### Happy path

Test the expected success scenario with valid input:

```php
it('creates a project', function () {
    loginAsTestUser();

    $this->postJson('/api/v1/projects', [
        'title' => 'New Project',
        'customer_id' => $customerId,
    ])
        ->assertCreated()
        ->assertJsonPath('data.title', 'New Project');

    $this->assertDatabaseHas('projects', ['title' => 'New Project']);
});
```

### Validation

Test that invalid input is rejected with correct error messages:

```php
it('rejects project without title', function () {
    loginAsTestUser();

    $this->postJson('/api/v1/projects', [
        'customer_id' => $customerId,
    ])
        ->assertUnprocessable()
        ->assertJsonValidationErrors(['title']);
});
```

### Authorization

Test that unauthorized access is blocked:

```php
it('prevents non-owner from updating project', function () {
    $otherUser = loginAsOtherUser();

    $this->putJson("/api/v1/projects/{$project->id}", [
        'title' => 'Hijacked',
    ])
        ->assertForbidden();
});
```

### Edge cases

Test boundary conditions:

```php
it('handles empty collection', function () {
    loginAsTestUser();

    $this->getJson('/api/v1/projects')
        ->assertOk()
        ->assertJsonCount(0, 'data');
});

it('paginates large result sets', function () {
    loginAsTestUser();

    $this->getJson('/api/v1/projects?per_page=5')
        ->assertOk()
        ->assertJsonPath('meta.per_page', 5);
});
```

## Response contract validation

### Assert JSON structure

```php
// Verify response shape (keys exist)
$response->assertJsonStructure([
    'data' => ['id', 'title', 'status', 'created_at'],
]);

// Verify exact values
$response->assertJsonPath('data.status', 'active');

// Verify collection count
$response->assertJsonCount(3, 'data');
```

### Assert response types

```php
// When strict typing matters
$data = $response->json('data');
expect($data['id'])->toBeInt();
expect($data['title'])->toBeString();
expect($data['total'])->toBeString(); // Money as string, not float
```

### Filter noisy responses

When a failing test dumps the full JSON body, narrow the diagnosis with `jq` or `grep`
instead of scrolling the whole payload:

```bash
# Extract only the failing assertion path
echo "$RESPONSE_JSON" | jq '.data.status, .errors'

# Targeted log scan
rg --json 'API call failed' storage/logs/laravel.log | jq -r '.data.lines.text'
```

## External service mocking

```php
it('handles external API failure gracefully', function () {
    Http::fake([
        'external-api.com/*' => Http::response(null, 500),
    ]);

    loginAsTestUser();

    $this->postJson('/api/v1/sync')
        ->assertStatus(502)
        ->assertJsonPath('message', 'External service unavailable');
});
```

## Test checklist per endpoint

| Category | Tests needed |
|---|---|
| **Auth** | Unauthenticated (401), unauthorized (403) |
| **Validation** | Missing fields, wrong types, boundary values |
| **Happy path** | Success with valid input, correct status code |
| **Response** | JSON structure, field types, pagination meta |
| **Side effects** | Database changes, events dispatched, jobs queued |
| **Edge cases** | Empty results, large payloads, concurrent access |

## Bridge to UI verification

API tests cover the contract layer. When an endpoint feeds a UI surface (Livewire component, Blade-rendered page, SPA route), complement the API test with a thin UI probe: a `livewire test` for wired components, or a Playwright spec / browser `screenshot` for the rendered shell. Never assume the UI works just because the API test is green.

## Output format

1. Test file in the project’s test framework (Pest, Jest, pytest) covering happy path, validation, auth, and edge cases
2. Test names as readable sentences describing expected behavior
3. Mocked external services where applicable

## Auto-trigger keywords

- API test
- endpoint test
- integration test
- response validation
- contract testing

## Gotcha

- Don't test framework internals (e.g., "does Laravel return 422 on validation error") — test YOUR validation rules.
- Always seed test data explicitly — don't rely on data from other tests (parallel execution).
- Mock external APIs with `Http::fake()` — never hit real services in tests.
- The model forgets to assert response structure, only checking status codes — always check both.

## Do NOT

- Do not hardcode IDs or timestamps — use factories or seeders.
- Do not skip auth tests — always test both authenticated and unauthenticated.
- Do not assert entire JSON responses — assert only meaningful fields.
- Do not use `Http::fake()` without also testing the real integration path.

## Anti-bruteforce — diagnose before retry

When a test fails, do not retry blindly with tweaked assertions until something passes. Diagnose the root cause first: print the actual response shape once, compare it to the contract, then write a targeted fix. Trial-and-error retries hide real regressions.

## Clarification guard — ambiguous contract → ask

If the endpoint contract is ambiguous (unclear status code, optional fields, error envelope shape), do not assume. Ask the user or check the OpenAPI spec / route definition before writing assertions — never guess the response shape from the route name.

## The HTTP-assertion idiom, per ecosystem

The examples above are Laravel's. The *shape* they teach — assert the status,
then the body contract, then the side effect, and keep one behavior per test —
transfers unchanged; the API does not. Resolve the runner with
`resolve_toolchain` and read its `ecosystems`:

| `ecosystems` | Request + assertion surface |
|---|---|
| `php` | `$this->getJson(...)` / `assertStatus` / `assertJsonPath` |
| `js` | `supertest` or the framework's own test client, with `expect(res.status)` |
| `python` | `httpx.AsyncClient` / framework `TestClient`; `assert res.status_code` |
| `go` | `httptest.NewServer` + `net/http`, or the router's own `ServeHTTP` |

Whatever the surface, the negative tests are not optional: unauthenticated,
not-owner and cross-tenant each get their own case, per `broken-access-control`.
