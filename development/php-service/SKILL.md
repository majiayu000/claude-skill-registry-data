---
model_tier: medium
name: php-service
description: "Use when the user says 'create service', 'new service class', or needs a PHP service following SOLID principles with proper DI and repository usage."
domain: engineering
workspaces:
  - engineering
packs:
  - php
trust:
  level: professional
install:
  default: false
  removable: true
---

# php-service

## When to use

Use when creating a new service, extracting business logic from a controller, or refactoring into a service layer.

Do NOT use when:
- Controllers (use `laravel` skill)
- DTOs (use `laravel-dto` skill for Laravel/PHP; framework-native skill for other stacks)
- Models (use `eloquent` skill)

## When to create a service

✅ Multiple steps needing orchestration (save + calculate + notify)
✅ Business rules beyond FormRequest
✅ Logic reused across controllers, jobs, commands
✅ Complex calculations or transformations

❌ Simple CRUD — `$model->update($request->validated())` stays in controller
❌ One-liner logic — no class for a single Eloquent call

## Procedure: Create a service

### Step 0: Inspect

1. Read `./agents/` and `AGENTS.md` for service conventions.
2. Check existing services — match naming, structure, DI patterns.
3. Check for repositories — see `php/patterns/repositories.md` guideline.

### Step 1: Create the class

1. Location: `app/Services/{Domain}/` or `app/Modules/{Module}/App/Services/`.
2. `declare(strict_types=1)`, proper namespace.
3. Constructor inject dependencies (repositories, other services).
4. Max 4 constructor dependencies — if more, split the service.

### Step 2: Implement methods

1. One responsibility per method.
2. Delegate data access to repositories.
3. Use DTOs for structured data.
4. Use `Math` helper for calculations — never raw arithmetic.

### Step 3: Wire up

```php
// Controller
public function __invoke(
    UpdateProjectRequest $request,
    Project $project,
    ProjectService $projectService,
): ProjectResource {
    $dto = UpdateProjectDTO::fromRequest($request);
    return ProjectResource::make($projectService->update($project, $dto));
}
```

## Conventions

→ See guideline `php/patterns/service-layer.md` for full service layer conventions.

### Validate

- Run PHPStan on the service — must pass at level 9.
- Verify single responsibility: service does one thing, no mixed concerns.
- Confirm all dependencies are constructor-injected (no `app()` or facades in service).
- Run affected tests — must pass.

## Output format

1. Service class with constructor injection and single responsibility
2. Repository dependency if data access is needed

## Gotcha

- Don't create "god services" with 10+ methods — split by responsibility.
- Don't inject `Request` into services — pass specific data.
- Services are framework-agnostic — no HTTP/request logic.

## Do NOT

- Do NOT inject `Request` or `Controller` into services — services are framework-agnostic.
- Do NOT create services with more than one responsibility — split them.

## Auto-trigger keywords

- service class
- business logic
- service layer
- dependency injection
