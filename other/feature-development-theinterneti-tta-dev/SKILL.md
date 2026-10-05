---
name: Feature Development
description: Full-stack feature development workflow from API to UI with testing
---

# Feature Development Skill

## Overview

Orchestrates **Backend Engineer → Frontend Engineer → Testing Specialist** for complete full-stack features.

**Duration:** 4-6 hours (full feature)
**Personas Required:** 3 (Backend, Frontend, Testing)

## Workflow Stages

### Stage 1: API Development (@backend-engineer)

**Steps:**
1. Design API contract (endpoints, models)
2. Implement FastAPI endpoints with Pydantic models
3. Write unit tests (AAA pattern, 100% coverage)
4. Generate OpenAPI schema
5. Document API in Logseq

**Deliverables:**
- Working REST API endpoints
- Complete test suite
- OpenAPI schema for frontend
- API documentation

**Handoff:** Share API contract with frontend engineer

---

### Stage 2: UI Implementation (@frontend-engineer)

**Steps:**
1. Retrieve API contract from backend
2. Generate TypeScript types from OpenAPI
3. Create React components
4. Implement state management
5. Write component tests

**Deliverables:**
- Functional UI components
- Type-safe API integration
- React Testing Library tests
- Responsive design

**Handoff:** Notify testing specialist UI is ready

---

### Stage 3: E2E Validation (@testing-specialist)

**Steps:**
1. Write Playwright E2E tests
2. Run accessibility validation (WCAG AA)
3. Execute integration tests
4. Perform quality gate review

**Deliverables:**
- Comprehensive E2E test coverage
- Accessibility compliance verification
- Quality gate approval

**Success Criteria:**
- ✅ All backend tests pass
- ✅ All frontend tests pass
- ✅ E2E tests cover user flows
- ✅ Accessibility violations = 0
- ✅ Integration tests validate full stack
