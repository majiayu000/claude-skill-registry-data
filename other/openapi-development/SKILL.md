---
name: openapi-development
description: Contribute to the API Platform OpenAPI customization layer — endpoint factories, request/response/schema factories, and transformers — keeping the generated spec valid and diff-stable. Use when adding endpoint factories or processors, updating OpenAPI generation logic, or fixing OpenAPI validation errors (Spectral, OpenAPI diff, Schemathesis). Skip with a note when framework.api_platform is false.
---

# OpenAPI Development Skill

## Profile keys consumed

- `framework.api_platform`
- `architecture.source_root`
- `architecture.shared_context`
- `make.phpinsights`
- `quality.phpinsights.quality`
- `quality.phpinsights.architecture`
- `quality.phpinsights.style`
- `quality.phpinsights.complexity`
- `ci.workflows`

This skill applies only when `framework.api_platform` is a version
string; when it is `false`, skip with a capability-absent note.

**The OpenAPI layer** referenced throughout is
`<architecture.source_root>/<architecture.shared_context>/Application/OpenApi/`.
When `architecture.shared_context` is `null`, locate the `OpenApi`
directory under the Application layer of the bounded context that owns
API composition instead.

## Context (Input)

- Adding new OpenAPI endpoint factories under the OpenAPI layer's
  `Factory/Endpoint/` directory
- Adding/editing request/response/schema factories under `Factory/`
- Adding/editing transformers/processors that modify the generated spec
- Fixing OpenAPI validation errors from Spectral lint, OpenAPI diff, or
  Schemathesis runs

## Task (Function)

Develop and maintain OpenAPI specification generation in a way that:

- Keeps `quality.phpinsights.*` scores intact (defaults: quality,
  architecture, and style `100`; complexity `94` — raise-only floors: a
  profile may tighten them, never relax them; fix the code, never the
  thresholds)
- Preserves immutability when working with API Platform OpenAPI models
  (`with*()` methods)
- Produces a spec that passes Spectral and stays diff-stable

**Success Criteria**:

- The repository's spec-generation target produces the committed spec
  file, and its Spectral validation target passes (see
  Testing / Validation below for target discovery).

---

## Architecture Overview

The OpenAPI layer follows a layered customization approach:

```text
<architecture.source_root>/<architecture.shared_context>/Application/OpenApi/
├── Builder/               # Build common OpenAPI pieces
├── Extractor/             # Extract example values / payload fragments
├── Factory/               # Endpoint/Request/Response/Schema/UriParameter factories
├── Transformer/           # Transform/modify OpenAPI operations, parameters, responses
├── ValueObject/ + Enum/   # Strongly typed OpenAPI-related value objects
└── Factory/OpenApiFactory.php  # Main coordinator (decorator)
```

`config/services.yaml` decorates API Platform's OpenAPI factory with
the application's coordinator factory, which receives a tagged iterator
of endpoint factories. Upstream reference wiring:

```yaml # profile-example
# config/services.yaml — decorator + tagged iterator
App\Shared\Application\OpenApi\Factory\OpenApiFactory: ~  # decorates API Platform's OpenAPI factory
# arguments include: !tagged_iterator 'app.openapi_endpoint_factory'
```

---

## Key Principles (Keep Complexity Low)

1. **Single Responsibility**: one class = one transformation.
2. **Immutability**: prefer `with*()` methods; avoid mutating nested
   arrays unless API Platform forces it.
3. **OPERATIONS constant**: avoid chaining `withGet/withPost/...`
   repeatedly — loop over a constant with dynamic `with`/`get` calls:

   ```php
   private const OPERATIONS = ['Get', 'Post', 'Put', 'Patch', 'Delete'];

   private function transformPathItem(PathItem $pathItem): PathItem
   {
       foreach (self::OPERATIONS as $operation) {
           $pathItem = $pathItem->{'with' . $operation}(
               $this->transformOperation($pathItem->{'get' . $operation}())
           );
       }

       return $pathItem;
   }
   ```

4. **Readable guard clauses**: prefer early returns (`null` operation,
   non-array parameters) over deep nesting.
5. **Functional style**: `array_map`, `array_filter`, `array_keys` over
   procedural mutation with intermediate arrays.
6. **Small methods**: keep methods around 20 lines and cyclomatic
   complexity per method below 5; extract helpers that take explicit
   inputs, return transformed output, and mutate no external state.
7. **Avoid `empty()`**: use explicit checks — `$array === []` for
   arrays, `$value === ''` (with explicit `null` handling) for strings.

Never add suppression annotations to silence quality findings — refactor
to the root cause instead.

---

## How to Add New Components

### Adding a New Transformer

- Create a focused class under the OpenAPI layer's `Transformer/`
  directory.
- Implement a single public entry method, e.g.
  `transform(OpenApi $openApi): OpenApi`.
- Iterate paths using `array_keys($openApi->getPaths()->getPaths())`.
- Apply changes per `PathItem` using an `OPERATIONS` constant + dynamic
  `with`/`get` calls.
- **Do NOT create new directories** (e.g. `Augmenter/`, `Enricher/`,
  `Helper/`). New OpenAPI transformation classes belong in
  `Transformer/`. Do not duplicate the purpose of directories that
  already exist in the layer.

### Adding a New Endpoint Factory

- Implement the layer's endpoint-factory interface (e.g.
  `EndpointFactoryInterface`) under `Factory/Endpoint/`.
- It is auto-tagged by `_instanceof` in `config/services.yaml`.
- It will be invoked by the coordinator `OpenApiFactory`.

---

## Testing / Validation

The profile `make` map defines no logical keys for OpenAPI spec
generation or validation; discover the repository's targets in its
Makefile (and check `ci.workflows` for an OpenAPI validation workflow).
Note the gap if none exist. Run locally in this order — generate, lint,
diff, then property-based validation. Upstream reference targets:

```bash # profile-example
make generate-openapi-spec   # exports .github/openapi-spec/spec.yaml
make validate-openapi-spec   # Spectral lint via ./scripts/validate-openapi-spec.sh
make openapi-diff            # diff-stability / breaking-change check
make schemathesis-validate   # Schemathesis: Examples and Coverage phases
```

After code changes, run the target mapped by `make.phpinsights` to
confirm the `quality.phpinsights.*` floors still hold.

---

## Related Skills

- [complexity-management](../complexity-management/SKILL.md) for
  refactoring when PHPInsights fails
- [documentation-sync](../documentation-sync/SKILL.md) when spec changes
  require docs updates
