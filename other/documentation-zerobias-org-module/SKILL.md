---
name: documentation
description: Module documentation standards and templates. Use when writing READMEs, API documentation, or user-facing guides.
---

# Documentation Rules

## 🚨 CRITICAL RULES (Immediate Failure)

### 1. USERGUIDE.md is Mandatory
- MUST be in all caps: USERGUIDE.md
- MUST contain credential acquisition instructions
- MUST map credentials to connection profile fields
- Full and complete for client use

### 2. No Proactive Documentation Creation
- NEVER create documentation unless requested
- NEVER create README.md proactively
- Only update docs when explicitly asked

## 🟡 STANDARD RULES

### USERGUIDE.md Structure
```markdown
# {Service Name} Module User Guide

## Authentication Setup

### Obtaining Credentials
1. Navigate to {service URL}
2. Go to Settings > API Keys (or relevant path)
3. Generate new API key with required permissions
4. Copy the generated key

### Connection Profile Configuration
Map your credentials to the connection profile:
- `token`: Your API key from step 3
- `baseUrl`: (Optional) Custom API endpoint

### Required Permissions/Scopes
- Read access to resources
- Write access for modifications
- (List specific scopes if applicable)
```

### README.md Updates
Only update when:
- Special requirements exist (billable operations, admin-only)
- Breaking changes introduced
- User explicitly requests

Special requirements format:
```markdown
## Special Requirements

### deleteRepository
- **Required Permissions**: Admin access to repository
- **Billing**: Uses billable API endpoint (check your plan)
```

### Code Comments
- NO comments unless specifically requested
- Exception: Document rule exceptions
- Exception: Special requirements for operations

When comments are needed:
```typescript
// Exception: Using snake_case to match external API exactly
// Standard rule: camelCase (see implementation-rules.md)
```

## 🟢 GUIDELINES

### Documentation Quality
- Clear, concise language
- Step-by-step instructions
- Real examples where helpful
- Avoid technical jargon

### Version Documentation
- Don't document version in files
- Gradle + zbb handle versioning (the `version` job in `zbb-publish-reusable.yml` bumps changed packages atomically before the matrix publishes)
- No manual version updates

### API Documentation
- Document in OpenAPI spec, not separate files
- Use clear operation descriptions
- Include parameter constraints
- Document response formats

### Internal Documentation
Store in `.localmemory/{module}/_work/`:
- product-model.md - Product understanding
- reasoning/ - Decision logs
- test-responses/ - API samples

### Migration Guides
Only create when:
- Breaking changes introduced
- Major version update
- User requests guide

## 📝 EXCEPTIONS LOG

### When to Add Comments
- Explaining non-obvious rule exceptions
- Documenting security requirements
- Clarifying complex business logic
- When user explicitly requests

### Documentation Overrides
User may request:
- Verbose documentation
- Inline code comments
- Detailed examples
- Tutorial-style guides