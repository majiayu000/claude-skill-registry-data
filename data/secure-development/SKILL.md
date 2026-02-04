---
name: secure-development
description: Security best practices for production applications including PII protection, input validation, SQL injection prevention, XSS mitigation, and secure logging. Apply when handling user data, authentication, or external inputs.
type: skill
version: 1.0.0
---

# Secure Development Skill

Implement security best practices to protect user data and prevent common vulnerabilities.

## What This Skill Provides

- **PII Protection**: Hash sensitive data in logs, GDPR compliance
- **Input Validation**: Prevent SQL injection, XSS, command injection
- **Authentication**: Secure password storage, session management
- **Logging Security**: What to log, what to redact
- **OWASP Top 10**: Prevention strategies for common vulnerabilities

## When to Use

- Handling user authentication or authorization
- Logging user inputs (search queries, form data)
- Processing external data (API requests, file uploads)
- Storing sensitive information (passwords, tokens, PII)
- Regulatory compliance (GDPR, HIPAA, SOC 2)
- When user mentions: "security", "authentication", "PII", "GDPR", "vulnerability"

## Primitives Included

- **Instructions**: `pii-protection.instructions.md` - Hashing, redaction, compliance
- **Instructions**: `input-validation.instructions.md` - Prevent injection attacks
- **Instructions**: `secure-authentication.instructions.md` - Password storage, sessions

## Key Security Principles

### 1. Defense in Depth
Multiple layers of security - don't rely on single control

### 2. Fail Securely
When errors occur, fail to secure state (deny access, don't leak info)

### 3. Principle of Least Privilege
Grant minimum necessary permissions

### 4. Never Trust User Input
Validate, sanitize, and escape ALL external data

### 5. Security by Design
Build security in from the start, not as afterthought

## Critical: PII in Logs

**NEVER log raw user inputs that may contain PII.**

**Examples of PII**:
- Names, email addresses, phone numbers
- Search queries (may contain names/locations)
- IP addresses (GDPR considers PII)
- Credit card numbers, SSNs
- Medical information
- Location data

**Safe Logging Pattern**:
```typescript
import { createHash } from 'crypto';

// ❌ NEVER do this
logger.log({ query: userQuery, email: user.email });

// ✅ Hash PII, log metadata
const queryHash = createHash('sha256')
  .update(userQuery)
  .digest('hex')
  .substring(0, 16);

logger.log({ 
  queryHash,  // Can correlate same queries
  queryLength: userQuery.length,  // Metadata OK
  userId: user.id  // Non-PII identifier OK
});
```

## Example: Secure Search Endpoint

```typescript
router.post('/search', async (req, res) => {
  // 1. Validate input
  const schema = z.object({
    query: z.string().min(1).max(500),
    limit: z.number().int().min(1).max(100).optional()
  });
  
  const validated = schema.parse(req.body);
  
  // 2. Sanitize for SQL (use parameterized queries)
  const results = await db.query(
    'SELECT * FROM items WHERE name LIKE $1 LIMIT $2',
    [`%${validated.query}%`, validated.limit || 10]
  );
  
  // 3. Log securely (hash PII)
  logger.info({
    event: 'search',
    queryHash: hash(validated.query),
    resultCount: results.length,
    userId: req.user?.id
  });
  
  // 4. Return results (no sensitive internal data)
  res.json({ results });
});
```

## Dependencies

- Validation library: Zod, Joi, or class-validator
- Hashing: Node crypto module (SHA256)
- Password hashing: bcrypt or Argon2
- Session management: express-session with secure store

---

**Related Skills**: `claude-framework` (Security S-1 through S-5), `fullstack-expertise`
