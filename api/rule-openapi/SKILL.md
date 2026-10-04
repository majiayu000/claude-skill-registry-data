---
name: rule-openapi
description: MANDATORY when editing files matching ["api/src/api/**/*_schemas.py", "api/src/api/**/*_routes.py", "api/openapi.yaml", "api/openapi.json", "api/src/api/__init__.py"]. OpenAPI spec generation, schema documentation, and versioning conventions
---

# OpenAPI Rules

## Source of Truth

The OpenAPI document is generated from Flask/APIFlask blueprints and Marshmallow schemas. ALWAYS make schema and route changes in Python code and regenerate the spec — NEVER hand-edit `openapi.yaml` / `openapi.json`.

## Operation Metadata

ALWAYS attach `@blueprint.doc(summary=..., description=..., responses=[...], security=...)` to every route. ALWAYS list all expected status codes in `responses` (including 401, 403, 404, 422). ALWAYS group operations by `tags` matching the domain (e.g., `Opportunities`, `Users`).

Correct:
```python
@user_blueprint.post("/<uuid:user_id>/saved-opportunities")
@user_blueprint.input(SaveOpportunityRequestSchema)
@user_blueprint.output(SaveOpportunityResponseSchema)
@user_blueprint.doc(
    summary="Save an opportunity",
    responses=[200, 401, 403, 404, 422],
    security=jwt_or_api_user_key_security_schemes,
    tags=["Users"],
)
```

## Schemas

ALWAYS define request/response schemas in `*_schemas.py`. ALWAYS add `metadata={"description": "..."}` to every field. ALWAYS mark required fields with `required=True`. ALWAYS use unique schema names (global namespace) — names feeding `generate_pagination_schema()` MUST be distinct. NEVER use string booleans as example values.

## Versioning

ALWAYS version APIs by URL prefix (`/v1/`, `/v2/`). NEVER break existing fields in a published version — add new fields or a new version. Deprecations MUST be marked with `deprecated=True` and a deprecation note in the description.

## Security Schemes

ALWAYS register security schemes centrally. ALWAYS pair `security=...` on `@blueprint.doc` with the matching auth decorator (see `api-auth.mdc`). NEVER omit the security scheme for authenticated endpoints.

## Examples and Descriptions

ALWAYS include human-readable descriptions on schemas, fields, and operations — the generated spec is the public API contract and consumer documentation. NEVER rely on field names alone.

## Spec Validation in CI

ALWAYS run a spec linter (e.g., Spectral) in CI and block merges on errors. ALWAYS commit the regenerated spec alongside code changes so diffs are reviewable.

---

## Related Rules

- **`api-routes.mdc`** — decorator stack and response handling
- **`api-form-schema.mdc`** — Marshmallow schema patterns
- **`api-validation.mdc`** — validation error shape
- **`api-auth.mdc`** — security scheme registration
- **`api-constants.mdc`** — enum exposure in schemas

## Specialist Validation

**Simple (add description, new field):** None.
**Moderate (new endpoint, new schema):** Invoke `codebase-conventions-reviewer`.
**Complex (new API version, breaking deprecation, new security scheme):** Invoke `architecture-strategist` and `security-sentinel`.
