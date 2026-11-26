---
name: laravel-testing-lord
description: Lord skill for Laravel 13 + Filament v5 testing mastery — Pest 3+, feature tests, Filament resource tests, API tests, database tests, and CI/CD.
triggers:
  - laravel testing lord
  - laravel testing
  - filament testing
  - pest php
  - laravel test
  - php testing
  - api testing
  - database testing
  - اختبار laravel
  - تست filament
personas:
  - QA
  - DEV
  - SRE
tech_stack:
  - laravel-13
  - filament-5
  - php-8-5
  - mysql-9-7
  - postgresql-19
lord: true

---

# Laravel Testing Lord

[OBJ] Mastery of testing for Laravel 13 + Filament v5 — Pest 3+, feature tests, Filament resource tests, API tests, database tests, and CI/CD integration.

[RULES]
1. [CMD] Query Context7 for Pest 3+ and Laravel testing docs. Use `/pestphp/pest` and `/laravel/framework` library IDs.
2. [REQ] Pest 3+: Use Pest 3+ for all backend tests. `describe()` blocks for grouping. `it()` for test cases. AAA pattern (Arrange-Act-Assert). One behavior per test.
3. [REQ] Two-Tier Testing: FAST tier — `artisan test --filter=<test>` (~5s, during iteration). FULL tier — `artisan test` (complete suite + coverage, before done). NEVER run full suite on every change.
4. [REQ] Filament Resource Tests: Use `Filament\Tables\Table` testing helpers. `->canSeeRecord()` / `->cannotSeeRecord()`. Test `Action` visibility via policy. Test form validation via `->fillForm()` + `->assertHasFormErrors()`.
5. [REQ] API Tests: `->assertJsonStructure(Resource::JSON_STRUCTURE)` for response shape. `->assertJsonPath()` for specific values. Test all CRUD operations. Test API versioning via `X-Api-Version` header. NEVER test without authentication context.
6. [REQ] Database Tests: `RefreshDatabase` trait for test isolation. `Database\Factories` for test data. NEVER hardcoded IDs or dates. Use `Model::factory()->create()` for test data. Test constraints (foreign keys, unique, not null).
7. [REQ] Coverage: 80% logic, 90% API, 70% total. Use `--coverage` in FULL tier. `XDEBUG_MODE=coverage` for accurate coverage. NEVER declare done without coverage report.
8. [REQ] Parallel Testing: `artisan test --parallel --exclude-group=serial` for fast parallel. `--group=serial` for tests that can't run in parallel (shared state, migrations). SQLite for fast tier, MySQL/PG for FULL tier.
9. [REQ] Mocking: Mock external services (`Http::fake()`, `Queue::fake()`, `Event::fake()`). Use `FakePlusLicenseService` pattern for swappable implementations. NEVER mock Eloquent models — use factories + in-memory DB.
10. [REQ] Vector Search Tests: Test `whereVectorSimilarTo()` with known embeddings. Test `AsVector` cast round-trip (set array → get array). Test MariaDB binary format vs PG JSON text. Mock embedding API in tests.
11. [REQ] Security Tests: Test authorization (policy gates) on every resource action. Test input validation (FormRequest). Test SQL injection prevention. Test XSS prevention. Test CSRF tokens. NEVER skip auth tests.
12. [REQ] Browser Testing: `pestphp/pest-plugin-browser` for E2E. Test critical user flows (login, CRUD, admin panel). Use `Laravel\Dusk` for JavaScript-dependent tests. NEVER rely only on unit tests for UI.
13. [REQ] CI/CD: Run FULL tier in CI. `--parallel` for speed. Upload coverage report. Fail on < 70% total. NEVER merge without green CI.

[WORKFLOWS]
1. Test a Filament Resource: Create `tests/Filament/Resources/UserResourceTest.php` → test list (`->canSeeRecord()`) → test create (`->fillForm()->call('create')->assertHasNoFormErrors()`) → test edit → test delete → test policy (`->cannotSeeRecord()` for unauthorized user) → test validation (`->fillForm(['email' => 'invalid'])->assertHasFormErrors(['email'])`).
2. Test an API Endpoint: Create `tests/Feature/Api/UserApiTest.php` → test index (`->getJson('/api/users')->assertJsonStructure(UserResource::JSON_STRUCTURE)`) → test store → test show → test update → test destroy → test auth (`->actingAs($user)`) → test validation → test versioning (`->withHeader('X-Api-Version', '2')`).
3. Test Vector Search: Create `tests/Feature/VectorSearchTest.php` → seed known embeddings → test `whereVectorSimilarTo()` returns correct order → test `AsVector` cast → test distance threshold → test with MariaDB binary format → mock embedding API.
