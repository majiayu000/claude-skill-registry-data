---
name: Multi-Tenant Validator
description: Tenant isolation
version: 1.0.0
category: security
---

# Multi-Tenant Safety Skill

## Rules

- ALWAYS include schoolId in queries
- Unique constraints scoped by schoolId
- Verify session before operations

## Checklist

- [ ] schoolId in all queries
- [ ] Unique constraints scoped
- [ ] Session verified
