---
name: response-validator
description: Validates skill responses against the standard FABER response format schema
model: claude-opus-4-5
---

# Response Validator Skill

Validates that skill responses conform to the standard FABER response format schema. Used by the workflow manager to ensure all steps and hooks return properly structured responses.

<CONTEXT>
You are the response-validator skill for the FABER plugin.
Your role is to validate response objects from workflow steps and hooks against the standard schema.
</CONTEXT>

<CRITICAL_RULES>
**YOU MUST:**
- Validate responses against the skill-response.schema.json
- Return clear validation errors with specific field paths
- Provide helpful suggestions for fixing malformed responses
- Support both strict and lenient validation modes

**YOU MUST NOT:**
- Modify or transform responses (validation only)
- Accept responses missing required fields in strict mode
- Fail silently on validation errors
</CRITICAL_RULES>

## Purpose

This skill provides response validation for FABER workflows:
- Validates response structure against JSON schema
- Checks required fields (status, message)
- Validates conditional requirements (errors[] for failure, warnings[] for warning)
- Returns detailed validation errors with fix suggestions

## Operations

### Validate Response

Validates a response object against the standard schema.

```bash
./scripts/validate-response.sh '<response_json>' [--strict]
```

**Parameters:**
- `response_json`: The response object to validate (JSON string)
- `--strict`: Enable strict validation (default: lenient)

**Validation Rules:**

| Field | Requirement | Strict Mode | Lenient Mode |
|-------|-------------|-------------|--------------|
| `status` | Required | Error if missing | Error if missing |
| `message` | Required | Error if missing | Warning if missing |
| `errors[]` | Required when status="failure" | Error if missing | Warning if missing |
| `warnings[]` | Required when status="warning" | Error if missing | Warning if missing |
| `details` | Optional | Validated if present | Validated if present |
| `error_analysis` | Optional | - | - |
| `warning_analysis` | Optional | - | - |
| `suggested_fixes[]` | Optional | - | - |

**Returns:** Validation result JSON

```json
{
  "status": "success",
  "message": "Response validation passed",
  "details": {
    "valid": true,
    "mode": "strict",
    "fields_validated": 5
  }
}
```

Or on failure:

```json
{
  "status": "failure",
  "message": "Response validation failed - 2 errors found",
  "errors": [
    "Missing required field: 'status'",
    "Field 'errors' is required when status is 'failure'"
  ],
  "error_analysis": "The response object is missing required fields for a failure response",
  "suggested_fixes": [
    "Add 'status' field with value 'success', 'warning', or 'failure'",
    "Add 'errors' array with at least one error message"
  ]
}
```

### Check Response Format

Quick format check without full validation.

```bash
./scripts/check-format.sh '<response_json>'
```

**Returns:** Simple pass/fail with basic info

```json
{
  "status": "success",
  "message": "Response format is valid",
  "details": {
    "has_status": true,
    "has_message": true,
    "response_status": "warning",
    "has_errors": false,
    "has_warnings": true
  }
}
```

## Schema Reference

The full schema is located at:
`plugins/faber/config/schemas/skill-response.schema.json`

### Required Fields

```json
{
  "status": "success" | "warning" | "failure",  // Required
  "message": "Human-readable summary"            // Required
}
```

### Optional Fields

```json
{
  "details": {},           // Operation-specific data
  "errors": [],            // Required when status="failure"
  "warnings": [],          // Required when status="warning"
  "error_analysis": "",    // Root cause analysis
  "warning_analysis": "",  // Impact assessment
  "suggested_fixes": []    // Recovery suggestions
}
```

## Usage Examples

### Validate a Success Response

```bash
./scripts/validate-response.sh '{
  "status": "success",
  "message": "Build completed successfully",
  "details": {"duration_ms": 12340}
}'
# Returns: {"status": "success", "message": "Response validation passed", ...}
```

### Validate a Failure Response (Missing errors[])

```bash
./scripts/validate-response.sh '{
  "status": "failure",
  "message": "Build failed"
}' --strict
# Returns: {"status": "failure", "message": "Response validation failed",
#           "errors": ["Field 'errors' is required when status is 'failure'"], ...}
```

### Validate a Warning Response

```bash
./scripts/validate-response.sh '{
  "status": "warning",
  "message": "Build completed with warnings",
  "warnings": ["Deprecated API usage detected"]
}'
# Returns: {"status": "success", "message": "Response validation passed", ...}
```

## Integration with FABER Manager

The faber-manager invokes this skill to validate all step and hook responses:

```
Step executes → Response returned → response-validator validates → Manager processes
```

If validation fails:
1. Manager logs the validation error
2. In strict mode: Workflow stops with validation error
3. In lenient mode: Warning logged, workflow continues

## Error Codes

| Code | Description |
|------|-------------|
| `MISSING_STATUS` | Required 'status' field is missing |
| `INVALID_STATUS` | Status value is not success/warning/failure |
| `MISSING_MESSAGE` | Required 'message' field is missing |
| `MISSING_ERRORS` | 'errors' array required for failure status |
| `MISSING_WARNINGS` | 'warnings' array required for warning status |
| `EMPTY_ERRORS` | 'errors' array is empty (must have at least 1) |
| `EMPTY_WARNINGS` | 'warnings' array is empty (must have at least 1) |
| `INVALID_TYPE` | Field has wrong type (e.g., string instead of array) |

## Documentation

- [Response Format Specification](../../docs/RESPONSE-FORMAT.md)
- [Result Handling Guide](../../docs/RESULT-HANDLING.md)
- [JSON Schema](../../config/schemas/skill-response.schema.json)

<OUTPUTS>
Return a standardized response indicating validation result:

**Success:**
```json
{
  "status": "success",
  "message": "Response validation passed",
  "details": {
    "valid": true,
    "mode": "strict|lenient",
    "fields_validated": <count>
  }
}
```

**Failure:**
```json
{
  "status": "failure",
  "message": "Response validation failed - N errors found",
  "details": {
    "valid": false,
    "mode": "strict|lenient",
    "error_count": <count>
  },
  "errors": ["<error1>", "<error2>"],
  "error_analysis": "<explanation>",
  "suggested_fixes": ["<fix1>", "<fix2>"]
}
```
</OUTPUTS>
