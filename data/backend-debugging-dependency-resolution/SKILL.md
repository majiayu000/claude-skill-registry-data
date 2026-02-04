---
name: backend-debugging-dependency-resolution
description: Systematic approach to diagnose and resolve backend service issues including dependency conflicts, database schema mismatches, import errors, and middleware configuration problems in FastAPI applications.
---

# Backend Debugging and Dependency Resolution Skill

## Purpose

This skill provides a systematic methodology for diagnosing and resolving backend service issues in FastAPI applications, with particular focus on dependency conflicts, database schema mismatches, import errors, and middleware configuration problems.

## When to Use This Skill

This skill should be used when:
- FastAPI applications fail to start or respond with internal server errors
- Dependency version conflicts arise between FastAPI, Starlette, and related packages
- Database foreign key constraint violations occur
- Import-related errors prevent module loading
- Middleware configuration causes request processing failures
- Authentication or session management systems malfunction
- RAG agent or vector store integration fails

## Implementation Process

### Phase 1: Dependency Conflict Diagnosis

1. **Check version compatibility matrix**
   - Identify FastAPI version (e.g., 0.104.1)
   - Identify Starlette version and verify compatibility range
   - Identify anyio and other dependency versions
   - Consult official compatibility documentation

2. **Resolve dependency conflicts**
   - Install compatible versions (e.g., Starlette <0.28.0 for FastAPI 0.104.1)
   - Pin dependency versions in requirements.txt
   - Test with minimal dependency set first

3. **Verify resolution**
   - Test basic FastAPI functionality with simple endpoint
   - Confirm middleware stack processes requests without errors
   - Validate dependency compatibility with test client

### Phase 2: Database Schema Consistency

1. **Identify foreign key mismatches**
   - Check error messages for "ForeignKeyViolation" or "constraint violation"
   - Compare model definitions with actual database schema
   - Identify which table references which in foreign key relationships

2. **Fix relationship inconsistencies**
   - Update ForeignKey references to point to correct tables
   - Ensure relationship definitions match foreign key constraints
   - Update related model relationships accordingly

3. **Apply schema changes**
   - Drop and recreate tables if safe to do so (development)
   - Use Alembic migrations for production environments
   - Verify new relationships work correctly

### Phase 3: Import and Module Structure Resolution

1. **Diagnose import errors**
   - Identify missing module errors (e.g., "No module named 'embeddings'")
   - Trace import chains to find incorrect paths
   - Check for circular imports or namespace pollution

2. **Fix import paths**
   - Update import statements to reflect actual module structure
   - Use explicit imports instead of wildcard imports
   - Ensure all `__init__.py` files properly export required modules

3. **Validate module structure**
   - Test individual module imports in isolation
   - Verify `__init__.py` files contain proper exports
   - Confirm package structure matches import expectations

### Phase 4: Middleware and Configuration Fixes

1. **Diagnose middleware errors**
   - Look for "too many values to unpack" errors in middleware context
   - Check middleware stack construction and configuration
   - Verify middleware compatibility with FastAPI version

2. **Resolve configuration issues**
   - Remove conflicting middleware configurations
   - Ensure middleware is added in correct order
   - Validate middleware parameters and options

### Phase 5: System Integration Verification

1. **Test core components**
   - Verify RAG agent functionality with sample queries
   - Test authentication endpoints (registration, login, profile)
   - Confirm database connectivity and session management
   - Validate vector store integration

2. **Validate end-to-end flows**
   - Test complete user journey from authentication to content retrieval
   - Verify session persistence across requests
   - Confirm error handling and fallback mechanisms

## Validation Checklist

Before considering the debugging complete, verify:

- [ ] All dependency version conflicts resolved
- [ ] Database schema consistency achieved
- [ ] Import errors eliminated
- [ ] Middleware configuration fixed
- [ ] Core functionality tested (RAG, auth, sessions)
- [ ] Error handling working properly
- [ ] End-to-end flows functional
- [ ] No regressions introduced

## Critical Indicators

- **Dependency conflicts**: Look for "ValueError: too many values to unpack" in middleware context
- **Schema mismatches**: Check for "ForeignKeyViolation" or "constraint violation" errors
- **Import issues**: Watch for "No module named 'X'" errors
- **Middleware problems**: Monitor for errors in `build_middleware_stack` calls

## Expected Outcomes

Upon successful application of this skill:
- Backend services start without errors
- API endpoints respond with appropriate status codes
- Database operations complete successfully
- Authentication and session management work properly
- RAG agent processes queries and returns responses
- Frontend integration functions correctly
- Error handling provides meaningful feedback