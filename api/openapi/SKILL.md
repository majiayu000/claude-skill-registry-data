---
model_tier: medium
name: openapi
description: "Use when documenting APIs — OpenAPI/Swagger, PHP attributes, Redocly validation, versioned specs — even when the user just says 'document this endpoint' without naming OpenAPI."
domain: engineering
workspaces:
  - engineering
packs:
  - engineering-base
---

# openapi

## When to use

Use this skill when adding or updating API documentation, writing OpenAPI annotations on controllers, or validating API specs.

## Procedure: Add OpenAPI documentation

1. **Gather context** — read `agents/reference/docs/controller.md` for OpenAPI patterns, `agents/settings/contexts/api-versioning.md` for versioning, and check 2-3 existing controllers for annotation style.
2. **Detect tooling** — check `composer.json` for `l5-swagger` or `laravel-openapi`, look for `@OA\` vs `#[OA\` syntax in existing controllers, find the config file.
3. **Write annotations** — add `#[OA\...]` attributes to the controller method. Include path, summary, tags, all parameters, and all response codes (200, 401, 403, 404, 422).
4. **Define schemas** — create or reuse `#[OA\Schema]` for request/response types. Use `$ref` for shared types.
5. **Validate** — run the spec validation (`npx @redocly/cli lint` or `php artisan l5-swagger:generate`). Fix any errors.
6. **Verify accuracy** — compare the documented request/response with the actual controller + FormRequest + Resource to ensure they match.

## OpenAPI attributes

### Detection

Check the project for OpenAPI tooling:
- Look for `darkaonline/l5-swagger` or `vyuldashev/laravel-openapi` in `composer.json`.
- Check for `@OA\` or `#[OA\` annotations in controllers.
- Look for `config/l5-swagger.php` or similar config files.

### PHP 8 attribute syntax

Modern Laravel projects use PHP 8 attributes instead of docblock annotations:

```php
#[OA\Get(
    path: '/projects',
    summary: 'List all projects',
    tags: ['Projects'],
    parameters: [
        new OA\Parameter(
            name: 'page',
            in: 'query',
            required: false,
            schema: new OA\Schema(type: 'integer'),
        ),
    ],
    responses: [
        new OA\Response(
            response: 200,
            description: 'Successful operation',
        ),
    ],
)]
public function __invoke(ListProjectsRequest $request): ProjectCollection
{
    // ...
}
```

### Conventions

- Place OpenAPI attributes **directly on the controller method**.
- **Paths are relative to the server URL.** If the server is configured as `http://host/api/v1`,
  then `path: '/projects'` resolves to `/api/v1/projects`. Never repeat the server prefix in the path.
- Use **tags** matching the resource name (e.g., `Projects`, `Users`).
- Document **all parameters** — path, query, and header.
- Document **all response codes** — 200, 201, 401, 403, 404, 422.
- Use **schema references** (`$ref`) for reusable types.

## Response documentation

### Resource schemas

Define reusable schemas for API Resources:

```php
#[OA\Schema(
    schema: 'Project',
    properties: [
        new OA\Property(property: 'id', type: 'integer'),
        new OA\Property(property: 'name', type: 'string'),
        new OA\Property(property: 'status', type: 'string', enum: ['active', 'archived']),
    ],
)]
```

### Pagination schema

Document paginated responses with `meta` and `links`:

```php
#[OA\Response(
    response: 200,
    description: 'Paginated list',
    content: new OA\JsonContent(
        properties: [
            new OA\Property(property: 'data', type: 'array', items: new OA\Items(ref: '#/components/schemas/Project')),
            new OA\Property(property: 'meta', ref: '#/components/schemas/PaginationMeta'),
        ],
    ),
)]
```

## Validation with Redocly

If the project uses Redocly for OpenAPI validation:

```bash
# Validate the spec
npx @redocly/cli lint openapi.yaml

# Preview documentation
npx @redocly/cli preview-docs openapi.yaml
```

Check for `.redocly.yaml` or `redocly.yaml` config in the project root.

## Versioned documentation

When the API uses URL-based versioning (e.g., `/api/v1/`, `/api/v2/`):

- The version prefix is typically part of the **server URL**, not the individual endpoint paths.
- Check the OpenAPI server configuration to understand what prefix is already included.
- When creating a v2 endpoint, add new documentation — don't modify v1 docs.
- Mark deprecated endpoints with `deprecated: true`.


## Output format

1. OpenAPI annotations as PHP attributes on controllers/models
2. Spec validation passing via Redocly

## Auto-trigger keywords

- OpenAPI
- Swagger
- API documentation
- PHP attributes
- Redocly

## Gotcha

- OpenAPI attributes must match the actual endpoint behavior — stale docs are worse than no docs.
- The model tends to define response schemas that don't match the Resource class output.
- Don't document internal endpoints in the public API spec.

## Do NOT

- Do NOT skip OpenAPI documentation when creating new endpoints.
- Do NOT document internal/private endpoints that are not part of the public API.
- Do NOT use docblock `@OA\` annotations when the project uses PHP 8 attributes.
- Do NOT hardcode example values that contain real customer data.
- Do NOT create documentation that contradicts the actual implementation.
