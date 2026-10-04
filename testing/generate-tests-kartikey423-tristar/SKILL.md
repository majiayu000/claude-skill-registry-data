---
name: generate-tests
description: Generate test files for TriStar code. Auto-detects TypeScript or Python and produces appropriate test patterns. Supports test-after (default) and TDD modes.
allowed-tools: Read, Write, Glob, Grep
context: fork
---

# Generate Tests Skill

## Prime Directive

**"Every line of code deserves a test that proves it works."**

Generate comprehensive tests for TriStar source files. Auto-detect the language and apply the appropriate test framework patterns.

## Arguments

- Target file path(s) or directory
- `--mode=test-after` (default) - Generate tests for existing code
- `--mode=tdd` - Generate test stubs first, implementation comes later

## Process

### Step 1: Understand Target

Read the target file(s). Determine:
- Language: TypeScript (.ts, .tsx) or Python (.py)
- Type: Component, Hook, Service, Model, Route, Utility
- Layer: Designer / Hub / Scout / Shared
- Dependencies: What does it import? What does it call?

### Step 2: Discover Conventions

Check existing test files for patterns:
- Glob `tests/` directory for existing test files
- Read 1-2 existing test files to match style
- Identify test framework (Jest + RTL for frontend, pytest for backend)
- Match naming convention and file organization

### Step 3: Choose Test Type

Based on the target:
- **Component** (.tsx): Jest + React Testing Library
- **Hook** (.ts with use prefix): renderHook pattern
- **Service** (.py in services/): pytest with AsyncMock
- **Model** (.py in models/): Pydantic validation tests
- **Route** (.py in api/): pytest + httpx AsyncClient
- **Utility** (.ts or .py): Simple unit tests

### Step 4: Generate Tests

Using the appropriate template from `templates/`:
- `templates/jest-unit.md` for TypeScript/React
- `templates/pytest-unit.md` for Python/FastAPI

Generate tests covering:
- Happy path (normal operation)
- Validation errors (invalid input)
- Edge cases (boundary values, empty data, null)
- Error handling (API failures, timeouts)
- TriStar domain rules (fraud detection thresholds, rate limits, state transitions)

### Step 5: Write Test Files

Write test files to the appropriate location:
- Frontend: `tests/unit/frontend/` mirroring src/ structure
- Backend: `tests/unit/backend/` mirroring src/ structure
- Integration: `tests/integration/`

### Step 6: Report

Output a summary:
- Files generated
- Test count per file
- Coverage areas (what is tested)
- Gaps (what could not be auto-tested)

## Test Naming Convention

- **TypeScript**: `<ComponentName>.test.tsx` or `<module>.test.ts`
- **Python**: `test_<module>.py`
- **Test function names**: `test_<what>_when_<condition>_then_<expected>`

## Templates

- `templates/jest-unit.md` - Jest + React Testing Library patterns
- `templates/pytest-unit.md` - pytest + httpx patterns
