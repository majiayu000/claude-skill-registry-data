---
name: preventing-error-exposure
description: Prevent leaking database errors and P-codes to clients. Use when implementing API error handling or user-facing error messages.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Security: Error Exposure Prevention

This skill teaches Claude how to handle Prisma errors securely by transforming detailed database errors into user-friendly messages while preserving debugging information in logs.

---

<role>
This skill prevents leaking sensitive database information (P-codes, table names, column details, constraints) to API clients while maintaining comprehensive server-side logging for debugging.
</role>

<when-to-activate>
This skill activates when:
- Implementing API error handlers or middleware
- Working with try/catch blocks around Prisma operations
- Building user-facing error responses
- Setting up logging infrastructure
- User mentions error handling, error messages, or API responses
</when-to-activate>

<overview>
Prisma errors contain detailed database information including:
- P-codes (P2002, P2025, etc.) revealing database operations
- Table and column names exposing schema structure
- Constraint names showing relationships
- Query details revealing business logic

**Security Risk:** Exposing this information helps attackers:
- Map database schema
- Identify validation rules
- Craft targeted attacks
- Discover business logic

**Solution Pattern:** Transform errors for clients, log full details server-side.

Key capabilities:
1. P-code to user message transformation
2. Error sanitization removing sensitive details
3. Server-side logging with full context
4. Production-ready error middleware
</overview>

<workflow>
## Standard Workflow

**Phase 1: Error Detection**
1. Wrap Prisma operations in try/catch
2. Identify error type (Prisma vs generic)
3. Extract P-code if present

**Phase 2: Error Transformation**
1. Map P-code to user-friendly message
2. Remove database-specific details
3. Generate safe generic message for unknown errors
4. Preserve error context for logging

**Phase 3: Response and Logging**
1. Log full error details server-side (P-code, stack, query)
2. Return sanitized message to client
3. Include generic error ID for support correlation
</workflow>

<conditional-workflows>
## Production vs Development

**Development Environment:**
- Log full error details including stack traces
- Optionally include P-codes in API response for debugging
- Show detailed validation errors
- Enable query logging

**Production Environment:**
- NEVER expose P-codes to clients
- Log errors with correlation IDs
- Return generic user messages
- Monitor error rates for P2024 (connection timeout)
- Alert on P2002 spikes (potential brute force)

## Framework-Specific Patterns

**Next.js App Router:**
```typescript
export async function POST(request: Request) {
  try {
    const data = await request.json()
    const result = await prisma.user.create({ data })
    return Response.json(result)
  } catch (error) {
    return handlePrismaError(error)
  }
}
```

**Express/Fastify:**
```typescript
app.use((err, req, res, next) => {
  if (isPrismaError(err)) {
    const { status, message, errorId } = transformPrismaError(err)
    logger.error({ err, errorId, userId: req.user?.id })
    return res.status(status).json({ error: message, errorId })
  }
  next(err)
})
```
</conditional-workflows>

<examples>
## Example 1: Error Transformation Function

**Pattern: P-code to User Message**

```typescript
import { Prisma } from '@prisma/client'

function transformPrismaError(error: unknown) {
  const errorId = crypto.randomUUID()

  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    switch (error.code) {
      case 'P2002':
        return {
          status: 409,
          message: 'A record with this information already exists.',
          errorId,
          logDetails: {
            code: error.code,
            meta: error.meta,
            target: error.meta?.target
          }
        }

      case 'P2025':
        return {
          status: 404,
          message: 'The requested resource was not found.',
          errorId,
          logDetails: {
            code: error.code,
            meta: error.meta
          }
        }

      case 'P2003':
        return {
          status: 400,
          message: 'The provided reference is invalid.',
          errorId,
          logDetails: {
            code: error.code,
            meta: error.meta,
            field: error.meta?.field_name
          }
        }

      case 'P2014':
        return {
          status: 400,
          message: 'The change violates a required relationship.',
          errorId,
          logDetails: {
            code: error.code,
            meta: error.meta
          }
        }

      default:
        return {
          status: 500,
          message: 'An error occurred while processing your request.',
          errorId,
          logDetails: {
            code: error.code,
            meta: error.meta
          }
        }
    }
  }

  if (error instanceof Prisma.PrismaClientValidationError) {
    return {
      status: 400,
      message: 'The provided data is invalid.',
      errorId,
      logDetails: {
        type: 'ValidationError',
        message: error.message
      }
    }
  }

  return {
    status: 500,
    message: 'An unexpected error occurred.',
    errorId,
    logDetails: {
      type: error?.constructor?.name,
      message: error instanceof Error ? error.message : 'Unknown error'
    }
  }
}
```

## Example 2: Production Error Handler

**Pattern: Middleware with Logging**

```typescript
import { Prisma } from '@prisma/client'
import { logger } from './logger'

export function handlePrismaError(error: unknown, context?: Record<string, unknown>) {
  const { status, message, errorId, logDetails } = transformPrismaError(error)

  logger.error({
    errorId,
    ...logDetails,
    context,
    stack: error instanceof Error ? error.stack : undefined,
    timestamp: new Date().toISOString()
  })

  return {
    status,
    body: {
      error: message,
      errorId
    }
  }
}

export async function createUser(data: { email: string; name: string }) {
  try {
    return await prisma.user.create({ data })
  } catch (error) {
    const { status, body } = handlePrismaError(error, {
      operation: 'createUser',
      email: data.email
    })
    throw new ApiError(status, body)
  }
}
```

## Example 3: Environment-Aware Error Handling

**Pattern: Development vs Production**

```typescript
const isDevelopment = process.env.NODE_ENV === 'development'

function formatErrorResponse(error: unknown, errorId: string) {
  const { status, message, logDetails } = transformPrismaError(error)

  const baseResponse = {
    error: message,
    errorId
  }

  if (isDevelopment && error instanceof Prisma.PrismaClientKnownRequestError) {
    return {
      ...baseResponse,
      debug: {
        code: error.code,
        meta: error.meta,
        clientVersion: Prisma.prismaVersion.client
      }
    }
  }

  return baseResponse
}
```

## Example 4: Specific Field Error Extraction

**Pattern: P2002 Constraint Details**

```typescript
function extractP2002Details(error: Prisma.PrismaClientKnownRequestError) {
  if (error.code !== 'P2002') return null

  const target = error.meta?.target as string[] | undefined

  if (!target || target.length === 0) {
    return 'A record with this information already exists.'
  }

  const fieldMap: Record<string, string> = {
    email: 'email address',
    username: 'username',
    phone: 'phone number',
    slug: 'identifier'
  }

  const fieldName = target[0]
  const friendlyName = fieldMap[fieldName] || 'information'

  return `A record with this ${friendlyName} already exists.`
}

function transformPrismaError(error: unknown) {
  if (error instanceof Prisma.PrismaClientKnownRequestError && error.code === 'P2002') {
    const message = extractP2002Details(error)
    return {
      status: 409,
      message,
      errorId: crypto.randomUUID(),
      logDetails: { code: 'P2002', target: error.meta?.target }
    }
  }
}
```
</examples>

<output-format>
## Error Response Format

**Client Response (JSON):**
```json
{
  "error": "User-friendly message without database details",
  "errorId": "uuid-for-correlation"
}
```

**Server Log (Structured):**
```json
{
  "level": "error",
  "errorId": "uuid-for-correlation",
  "code": "P2002",
  "meta": { "target": ["email"] },
  "context": { "operation": "createUser", "userId": "123" },
  "stack": "Error stack trace...",
  "timestamp": "2025-11-21T10:30:00Z"
}
```

**Development Response (Optional Debug):**
```json
{
  "error": "User-friendly message",
  "errorId": "uuid-for-correlation",
  "debug": {
    "code": "P2002",
    "meta": { "target": ["email"] },
    "clientVersion": "6.0.0"
  }
}
```
</output-format>

<constraints>
## Security Requirements

**MUST:**
- Transform ALL Prisma errors before sending to clients
- Log full error details server-side with correlation IDs
- Remove P-codes from production API responses
- Remove table/column names from client messages
- Remove constraint names from client messages
- Use generic messages for unexpected errors

**SHOULD:**
- Include error IDs for support correlation
- Monitor error rates for security patterns
- Use structured logging for error analysis
- Implement field-specific messages for P2002
- Differentiate 404 (P2025) from 400/500 errors

**NEVER:**
- Expose P-codes to clients in production
- Include error.meta in API responses
- Show Prisma stack traces to clients
- Reveal table or column names
- Display constraint names
- Return raw error.message to clients

## Common P-codes to Handle

**P2002** - Unique constraint violation
- Status: 409 Conflict
- Message: "A record with this information already exists"

**P2025** - Record not found
- Status: 404 Not Found
- Message: "The requested resource was not found"

**P2003** - Foreign key constraint violation
- Status: 400 Bad Request
- Message: "The provided reference is invalid"

**P2014** - Required relation violation
- Status: 400 Bad Request
- Message: "The change violates a required relationship"

**P2024** - Connection timeout
- Status: 503 Service Unavailable
- Message: "Service temporarily unavailable"
- Action: Log urgently, indicates connection pool exhaustion
</constraints>

<validation>
## Security Checklist

After implementing error handling:

1. **Verify No P-codes Exposed:**
   - Search API responses for "P20" pattern
   - Test each error scenario
   - Check production logs vs API responses

2. **Confirm Logging Works:**
   - Trigger known errors (P2002, P2025)
   - Verify errorId appears in both logs and response
   - Confirm full error details in logs only

3. **Test Error Scenarios:**
   - Unique constraint violation (create duplicate)
   - Not found (query non-existent record)
   - Foreign key violation (invalid reference)
   - Validation error (missing required field)

4. **Review Environment Behavior:**
   - Production: No P-codes, no meta, no stack
   - Development: Optional debug info
   - Logs: Full details in both environments
</validation>

---

## Integration with SECURITY-input-validation

Error exposure prevention works with input validation:

1. **Input Validation** (SECURITY-input-validation skill):
   - Validate data before Prisma operations
   - Return validation errors with field-level messages
   - Prevent malformed data reaching database

2. **Error Transformation** (this skill):
   - Handle database-level errors
   - Transform Prisma errors to user messages
   - Log server-side for debugging

**Pattern:**
```typescript
async function createUser(input: unknown) {
  const validation = userSchema.safeParse(input)

  if (!validation.success) {
    return {
      status: 400,
      body: {
        error: 'Invalid user data',
        fields: validation.error.flatten().fieldErrors
      }
    }
  }

  try {
    return await prisma.user.create({ data: validation.data })
  } catch (error) {
    const { status, body } = handlePrismaError(error)
    return { status, body }
  }
}
```

Validation catches format issues, error transformation handles database constraints.

## Related Skills

**Error Handling and Validation:**

- If sanitizing error messages for user display, use the sanitizing-user-inputs skill from typescript for safe error formatting
- If customizing Zod validation errors, use the customizing-errors skill from zod-4 for user-friendly error messages
