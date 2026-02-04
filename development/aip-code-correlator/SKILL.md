---
name: aip-code-correlator
description: Correlate AIP review findings with code locations in code-first API projects. Use when creating fix plans for code-generated OpenAPI specs, mapping spec paths to source code, or when user asks to find where an API endpoint is implemented. Works with NestJS, Fastify, and Express projects.
allowed-tools: Read, Grep, Glob, Task
---

# AIP Code Correlator

Map AIP review findings to code locations for code-first API projects.

## Preferred Approach: MCP Correlate Tool

**IMPORTANT**: If the `mcp__aip-reviewer__aip-correlate` tool is available, use it instead of manual correlation. The MCP tool:

- Takes a reviewId from `aip-review`
- Automatically detects framework from package.json
- Uses MCP sampling for accurate code location
- Batch processes all findings efficiently
- Returns ExtendedFinding[] with file:line references

```
Use mcp__aip-reviewer__aip-correlate with:
- reviewId: {review-id-from-aip-review}
- projectRoot: {absolute-path-to-project}
- specPath: {absolute-path-to-spec} (optional, for context extraction)
- framework: "nestjs" | "fastify" | "express" | "unknown" (optional hint)
- correlationLevel: "minimal" | "moderate" | "thorough" (optional, default: "moderate")
```

The manual process below is a fallback for when MCP tools are not available.

## When to Use (Manual Fallback)

Activate this skill when:

- Creating a fix plan after `aip-review` for a code-first project
- User asks "where is this endpoint implemented?"
- User wants to fix API issues and needs to know which files to modify
- Mapping OpenAPI spec paths to source code
- MCP correlate tool is not available

## Prerequisites

- AIP review findings (from `aip-review` MCP tool or review document)
- Access to project source code
- OpenAPI spec (to extract operation context)

## Correlation Process

### Step 1: Gather Inputs

**From MCP tool results:**
If `aip-review` was called, use the findings from that response.

**From review document:**
If working from `thoughts/api/reviews/*.md`, read the document to get:

- `spec_path` from frontmatter
- Findings list with `ruleId`, `path`, `severity`

### Step 2: Extract Operations from Findings

Parse each finding's `path` field to extract method and API path:

```
"GET /users/{id}" → method: GET, path: /users/{id}
"POST /orders"    → method: POST, path: /orders
```

Dedupe by method+path (multiple findings may target same endpoint).

### Step 3: Detect Framework

Read `package.json` in project root:

- `@nestjs/core` → NestJS (decorators: @Controller, @Get, @Post)
- `fastify` → Fastify (route methods: .get, .post, app.route)
- `express` → Express (router methods: router.get, app.get)

### Step 4: Find Code Locations

For each unique operation, spawn an `aip-code-locator` agent:

```
Task: aip-code-locator
Prompt: Find the code that implements this API operation:
  - method: GET
  - path: /users/{id}
  - operationId: getUserById (if available from spec)
  - framework: nestjs
  - rootDir: /project
```

Spawn up to 5 agents in parallel for efficiency.

### Step 5: Compile Extended Findings

For each finding, build this structure:

```json
{
  "finding": {
    "ruleId": "naming/plural-resources",
    "severity": "warning",
    "path": "GET /user/{id}",
    "message": "Resource name should be plural",
    "suggestion": "Rename to /users/{id}",
    "fix": { "type": "rename-path-segment", "..." }
  },
  "specContext": {
    "method": "GET",
    "path": "/user/{id}",
    "operationId": "getUser",
    "summary": "Get a user by ID",
    "tags": ["users"]
  },
  "codeLocations": [
    {
      "file": "src/users/users.controller.ts",
      "line": 42,
      "type": "controller",
      "confidence": "high",
      "snippet": "@Get(':id')\nasync getUser(@Param('id') id: string) { ... }",
      "reasoning": "@Get decorator matches, operationId in @ApiOperation"
    }
  ],
  "suggestedDiffs": {
    "specDiff": "...",
    "codeDiffs": [{ "file": "...", "diff": "...", "description": "..." }]
  }
}
```

### Step 6: Generate Suggested Diffs

For deterministic fixes, pre-populate code diffs using templates from [diff-templates.md](diff-templates.md).

| fix.type              | Code Diff                                         |
| --------------------- | ------------------------------------------------- |
| `rename-path-segment` | Update @Controller('user') → @Controller('users') |
| `rename-parameter`    | Update @Param name                                |
| `change-status-code`  | Add/update @HttpCode(201)                         |
| `remove-request-body` | Remove @Body() parameter                          |
| `add-parameter`       | Partial - provide template                        |
| `add-schema`          | No - too complex, guidance only                   |

### Step 7: Output Correlation

Write to `thoughts/api/correlations/{date}-{spec-name}.json`:

```json
{
  "extendedFindings": [
    /* ... */
  ],
  "framework": "nestjs",
  "generatedAt": "2024-01-15T10:30:00Z",
  "reviewPath": "thoughts/api/reviews/...",
  "specPath": "openapi.yaml",
  "summary": {
    "correlated": 6,
    "notFound": 2,
    "totalFindings": 8
  }
}
```

## Output Format

Report results to user:

```markdown
## Correlation Complete

| Operation       | Code Location                      | Confidence |
| --------------- | ---------------------------------- | ---------- |
| GET /users/{id} | src/users/users.controller.ts:42   | high       |
| POST /users     | src/users/users.controller.ts:28   | high       |
| GET /orders     | src/orders/orders.controller.ts:15 | medium     |

**Not found:** DELETE /admin/cache, GET /health

Correlation saved to: thoughts/api/correlations/2024-01-15-orders-api.json
```

## MCP Tools Reference

**aip-review**: Analyze OpenAPI spec against AIP rules. Returns findings with reviewId.

```
Call: mcp__aip-reviewer__aip-review with specPath or specUrl
Returns: { reviewId, findings[], summary, findingsPath, findingsUrl }
```

**aip-correlate**: Correlate AIP review findings with code locations.

```
Call: mcp__aip-reviewer__aip-correlate with reviewId, projectRoot, specPath, framework
Returns: { extendedFindings[], framework, summary, correlationPath }
```

**aip-apply-fixes**: Apply suggested fixes to spec (after correlation, to fix spec issues).

```
Call: mcp__aip-reviewer__aip-apply-fixes with reviewId, specPath/specUrl, writeBack, dryRun
Returns: { summary, downloadUrl, modifiedSpec }
```

## Agent Reference

**aip-code-locator**: Find code implementing a single API operation.

- Input: method, path, operationId, tags, rootDir, framework
- Output: CodeLocation[] with file:line, confidence, snippets

## File Locations

| Purpose            | Path                                                |
| ------------------ | --------------------------------------------------- |
| Review documents   | `thoughts/api/reviews/*.md`                         |
| Correlation output | `thoughts/api/correlations/*.json`                  |
| Code locator agent | `plugins/aip-api-design/agents/aip-code-locator.md` |
| Diff templates     | [diff-templates.md](diff-templates.md)              |

## Related

- Use `/api-plan` after correlation to create a fix plan
- Use `/api-validate` to verify fixes against the plan
- Use `aip-code-locator` agent directly for single operation lookup
- See `aip-knowledge` skill for AIP rule explanations
