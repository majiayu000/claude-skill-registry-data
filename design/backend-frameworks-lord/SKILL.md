---
name: backend-frameworks-lord
always: true
description: Architect-level command of Laravel, Filament, Nova, Django, Spring Boot, Express, NestJS, Rails, ASP.NET Core.
triggers:
  - backend frameworks lord
  - command

---
[SKILL] backend-frameworks-lord
[OBJ] Design server-side apps and admin panels across Laravel, Filament, Nova, Django, Spring Boot, Express, NestJS, Rails, ASP.NET Core.
[RULES]
1. [CMD] IDs: Laravel `/laravel/docs`, Django `/websites/djangoproject_en_5_2`, Spring Boot `/spring-projects/spring-boot`, Express `/expressjs/express`, NestJS `/websites/nestjs`, Rails `/websites/guides_rubyonrails_v8_0`, ASP.NET Core `/dotnet/aspnetcore.docs`; Filament `/filamentphp/filament`; Filament Shield `/bezhansalleh/filament-shield`; Laravel Nova `/websites/nova_laravel_v5`; Laravel multi-tenancy `/spatie/laravel-multitenancy`, `/archtechx/tenancy`; Prisma `/prisma/web` source `/prisma/prisma`; MariaDB `mariadb-lord`; page sections `page-sections-lord`.
2. [REQ] Pillar coverage: request lifecycle, DI/IoC, data access/ORM, validation/serialization, auth/authz, API design, async/background work, testing, performance/operations.
3. [REQ] Query framework ID with full question + topic (routing, orm, validation, authentication).
4. [REQ] Framework choice: compare language ecosystem, concurrency model, ORM, deployment target, team skills.
5. [REQ] Laravel + MariaDB + multi-tenancy: query `backend-frameworks-lord`, `mariadb-lord`, and the chosen tenancy package; choose database-per-tenant vs schema-per-tenant vs table-per-tenant based on isolation, scale, and ops cost.
6. [REQ] Filament/Nova + MariaDB + multi-tenancy: use `mariadb-lord` for engine/security; Filament tenancy via panel tenant model + `filament-shield` RBAC; Nova tenancy via global scopes or tenant-aware policies.
7. [REQ] Landing/page builder in Laravel: query `page-sections-lord` for the standard Page + StaticPage + Filament Builder pattern; query `frontend-frameworks-lord` for section component rendering.
8. [REQ] Cite version-specific APIs when named; otherwise prefer latest stable major.
9. [REQ] Laravel Architecture Patterns (ranked by complexity):
   1. Simple: Controller + Model + FormRequest (Laravel default — small apps)
   2. Medium: + Service Layer + Repository + API Resource (medium apps)
   3. Advanced: + DTO/Value Objects + Custom Builders + Custom Casts + API Versioning (large apps)
   4. Enterprise: + DDD (Domains/) + Actions/ + Modular (Concord) + Event-Driven (enterprise apps)
10. [REQ] Pattern Selection Matrix (choose based on project type):
   - eCommerce / Multi-vendor → Modular (Concord) like Bagisto (41 packages, EAV, 22 locales)
   - CRM / SaaS → DDD + Service Layer like Monica (Account→Vault hierarchy, WebAuthn)
   - API-first / Headless → Repository + DTO + API Resources + Versioning like Koel (header-based versioning, cursor pagination)
   - Wiki / Content platform → Feature-based + Activity Logging like BookStack (jhfa content filtering, MFA)
   - Admin Panel → Filament + Plugin System + Clusters (see `filament-plugins` tech-stack)
11. [REQ] Service Layer Rules (Monica pattern): `BaseService` with `rules(): array` + `permissions(): array` + `execute(array $data)`. Permission dependencies: each permission requires simpler permissions (e.g. `author_must_be_vault_manager` requires `vault_must_belong_to_account` + `author_must_belong_to_account`). `QueuableService` for async: `ShouldQueue` + `handle()` + `$tries = 1`. Validate via `validateRules(array $data): bool`.
12. [REQ] Repository Rules (Bagisto/Krayin/Koel pattern): `model(): string` returning Contract interface (NOT Model class directly). Prettus L5 (`prettus/l5-repository`) for caching + criteria, OR custom base with `auth(): Authenticatable` helper. `paginate()` accepts `PaginationStrategy` (cursor vs offset). `fieldSearchable` array for searchable fields.
13. [REQ] DTO Rules (Koel pattern): `app/Values/` folder for value objects. FormRequest with `toDto(): SomeData` for conversion. Named arguments in DTO constructors. `SongUpdateData::make(title:, artistName:, ...)`. ⛔ NEVER pass raw `array $data` between Service layers.
14. [REQ] API Design Rules (Koel pattern): `JsonResource` with `JSON_STRUCTURE` + `PAGINATION_JSON_STRUCTURE` + `CURSOR_PAGINATION_JSON_STRUCTURE` constants. Header-based versioning: `X-Api-Version` → `routes/api.{version}.php`. `RouteServiceProvider::loadVersionAwareRoutes(string $type)`. Cursor pagination for large datasets (>10k rows), offset for standard. `PaginationStrategyResolver` selects based on request.
15. [REQ] Multi-Tenancy Rules (Monica/Bagisto pattern): Hierarchical: Account → Vault with VIEW(300)/EDIT(200)/MANAGE(100) permissions + pivot table. Channel-based: each Channel has currency/locale/theme separate. ⛔ NEVER trust tenant isolation without global scope. ⛔ NEVER expose one tenant's data to another. Query `laravel-security` tech-stack for full rules.
16. [REQ] Three-Component Model (Bagisto enterprise pattern): Contract (Interface) + Model (Eloquent) + Proxy (Facade-like). `model(): string` in Repository returns Contract. Eases testing + mocking + decoupling. Use for enterprise apps with >20 models.
17. [REQ] Activity Logging (BookStack pattern): `ActivityLogger` for all create/update/delete. `ActivityService::add(ActivityType::X, $entity)`. Activity assertions in tests: `assertActivityExists(ActivityType::COMMENT_CREATE)`. Audit trail for compliance.
18. [REQ] AI Integration (Bagisto/Krayin pattern): Laravel AI SDK (`laravel/ai`) for native `whereVectorSimilarTo()` + `->stream()`. Custom `MagicAIService` with system prompt templates + recursive call prevention (`static $isExtracting`). Treat LLM outputs as untrusted — validate schema. Query `laravel-ai` tech-stack.
19. [REQ] Testing (query `laravel-testing` tech-stack): Pest 3+ for new, PHPUnit 11+ for legacy. Two-tier FAST/FULL. Factories per model. Security test suite. Translation consistency. E2E with Playwright. Multi-DB matrix. Parallel + serial.
20. [REQ] Security (query `laravel-security` tech-stack): ACL config-driven or filament-shield. Content filtering (HTMLPurifier + SVG sanitize). Rate limiting. Security headers. UUID primary keys. FormRequest validation. RBAC policies + gates.

21. [REQ] Command Object Pattern (Invoice Ninja): Decompose complex service methods into command classes with execute() + 
ollback(). CommandBus runs sequence with Saga-style rollback. Better testability than monolithic services.
22. [REQ] Contract-First Design (Prisma): Emit machine-readable JSON schema + TypeScript stubs from API contracts. Enables AI agent understanding + frontend type safety. contract.json + contract.d.ts artifacts.
23. [REQ] Numbered Package Layering (Prisma): Prefix packages with layer numbers (1-core, 2-runtime, 3-managers) to encode dependency direction and prevent circular deps.
24. [REQ] Fine-Grained Hook Lifecycle (Fastify): pre_receive → pre_validation → pre_handler → post_handler → post_response → on_error. More granular than middleware. Use for guardian/policy pipelines.
25. [REQ] Scoped Managers (Filament): app()->scoped() for request-isolated service instances. Prevents state leakage in Octane/Swoole. Flush at request boundary.
26. [REQ] Manifest-Driven Composition (Remix): Auto-generate umbrella package re-exports from manifest.json. Single-package distribution while maintaining modularity.
27. [REQ] AI-Assisted Filament Workflow: Boost + Compass + FilaCheck pipeline. Boost loads context → AI generates code → FilaCheck validates. See 	ech-stack/laravel-ai-workflow.md and workflows/29-filament-ai-workflow.md.
