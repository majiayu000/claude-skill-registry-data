---
name: notepad-debug-api-error
description: "Reference doc: Debugging API Errors in Simpler.Grants.gov"
---

# Debugging API Errors in Simpler.Grants.gov

Use this notepad when debugging error responses from the API.

## Error Flow

```
Service/Route code
  → raise_flask_error(status_code, message, validation_issues=[...])
    → ValidationErrorDetail(type=ValidationErrorType.XXX, message="...", field="...")
      → JSON response to frontend
        → Frontend maps `type` string to localized message via i18n
```

## Error Response Format

```json
{
  "message": "Error description",
  "data": {},
  "status_code": 422,
  "errors": [
    {
      "type": "fieldRequired",
      "message": "This field is required",
      "field": "opportunity_title"
    }
  ]
}
```

## Common Status Codes

| Code | When | Log Level |
|------|------|-----------|
| 400 | Bad request / malformed input | `info` |
| 401 | Not authenticated | `info` |
| 403 | Authenticated but not authorized | `info` |
| 404 | Resource not found | `info` |
| 422 | Validation failure | `info` |
| 500 | Unexpected server error | `error`/`exception` |

**Key:** ALL 4xx errors log at `info` level (not `warning` or `error`). This prevents false alerting on client errors.

## How to Raise Errors

```python
from src.api.response import raise_flask_error, ValidationErrorDetail
from src.validation.validation_constants import ValidationErrorType

# Simple not found
raise_flask_error(404, message="Opportunity not found")

# Validation error with details
raise_flask_error(
    422,
    message="Validation failed",
    validation_issues=[
        ValidationErrorDetail(
            type=ValidationErrorType.FIELD_REQUIRED,
            message="Opportunity title is required",
            field="opportunity_title",
        ),
        ValidationErrorDetail(
            type=ValidationErrorType.INVALID_VALUE,
            message="Close date must be in the future",
            field="close_date",
        ),
    ],
)

# Authorization (ALWAYS check after 404 to prevent info leakage)
entity = get_entity(db_session, entity_id)
if entity is None:
    raise_flask_error(404, message="Not found")  # ← 404 first
if not can_access(user, entity):
    raise_flask_error(403, message="Not authorized")  # ← then 403
```

## ValidationErrorType Enum

The `type` field is the API↔frontend contract. The frontend maps these to localized messages.

Common types from `src.validation.validation_constants.ValidationErrorType`:
- `FIELD_REQUIRED` — missing required field
- `INVALID_VALUE` — value doesn't meet constraints
- `DUPLICATE_VALUE` — unique constraint violation
- `NOT_FOUND` — referenced entity doesn't exist

## Frontend Error Handling

The frontend maps `type` strings to translations in `messages/en/index.ts`:
```typescript
Errors: {
  fieldRequired: "This field is required",
  invalidValue: "The value provided is not valid",
  // ...
}
```

## Debugging Checklist

- [ ] Check the `type` field in the error response — it drives frontend behavior
- [ ] Check log level: 4xx should be `info`, 5xx should be `error`
- [ ] Verify 404 check comes before 403 check (prevent info leakage)
- [ ] Check that `ValidationErrorDetail` includes the correct `field` name
- [ ] Verify the frontend has a translation for the error `type`
- [ ] Check structured logs: `logger.info("Action failed", extra={"entity_id": str(id), "error_type": error.type})`
