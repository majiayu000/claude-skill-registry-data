---
name: coverage-analyzer
description: |
  WHEN: Coverage analysis, finding untested files, test prioritization, coverage gap identification
  WHAT: Line/Branch/Function coverage + untested file list + priority by importance + improvement roadmap
  WHEN NOT: Test generation → test-generator, Test quality → code-reviewer
---

# Coverage Analyzer Skill

## Purpose
Analyzes project test coverage and identifies areas lacking tests. Recommends code to test with priority.

## When to Use
- Coverage analysis requests
- Finding untested files
- Coverage improvement guidance
- Verifying critical code test status

## Workflow

### Step 1: Check Coverage Status
```
Analyzing test environment...

**Test Runner**: Jest
**Test Files**: 45
**Coverage Report**: coverage/lcov-report/
**Current Coverage**: 68%
```

### Step 2: Select Analysis Type
**AskUserQuestion:**
```
"What coverage analysis do you need?"
Options:
- Overall coverage status
- Find untested files
- Low coverage files
- Critical code test status
- Coverage improvement priorities
```

## Analysis Types

### Untested File Detection
```
Targets:
- src/**/*.ts
- src/**/*.tsx
- lib/**/*.ts

Excluded:
- *.d.ts (type definitions)
- *.test.ts (test files)
- index.ts (barrel files)
- *.config.ts (config files)
```

**Results Format:**
```
## Untested Files (15)

### High Priority (Business Logic)
| File | Lines | Complexity | Recommendation |
|------|-------|------------|----------------|
| src/utils/payment.ts | 120 | HIGH | Needs immediate tests |
| src/services/auth.ts | 85 | HIGH | Needs immediate tests |

### Medium Priority (Utilities)
| File | Lines | Complexity | Recommendation |
|------|-------|------------|----------------|
| src/utils/format.ts | 45 | MEDIUM | Tests recommended |

### Low Priority (Simple Code)
| File | Lines | Complexity | Recommendation |
|------|-------|------------|----------------|
| src/constants/index.ts | 20 | LOW | Optional |
```

### Coverage Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| Line Coverage | Executed lines ratio | > 80% |
| Branch Coverage | Executed branches ratio | > 75% |
| Function Coverage | Executed functions ratio | > 85% |
| Statement Coverage | Executed statements ratio | > 80% |

**Analysis Results:**
```
### Overall Status
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Lines | 68% | 80% | WARNING |
| Branches | 55% | 75% | CRITICAL |
| Functions | 72% | 85% | WARNING |

### Low Coverage Files (< 50%)
| File | Lines | Branches | Impact |
|------|-------|----------|--------|
| src/services/payment.ts | 23% | 10% | HIGH |
| src/components/Form.tsx | 45% | 30% | MEDIUM |
```

### Critical Code Analysis
**Priority Criteria:**
| Criteria | Description | Weight |
|----------|-------------|--------|
| Business Logic | Payment, auth, data processing | HIGH |
| Usage Frequency | Import count | MEDIUM |
| Complexity | Cyclomatic Complexity | MEDIUM |
| Change Frequency | git log based | LOW |

```
### CRITICAL (Must Test)
| File | Importance | Coverage | Recommendation |
|------|------------|----------|----------------|
| src/services/payment.ts | CRITICAL | 23% | Add tests immediately |
| src/utils/auth.ts | CRITICAL | 0% | Create test file |

### HIGH (Should Test)
| File | Importance | Coverage | Recommendation |
|------|------------|----------|----------------|
| src/hooks/useCart.ts | HIGH | 45% | Add edge cases |
```

### Improvement Priorities
```
## Coverage Improvement Priorities

### Priority 1: High Importance + Low Coverage
Needs immediate tests

| File | Current | Expected Gain | Effort |
|------|---------|---------------|--------|
| src/services/payment.ts | 23% | +57% → 80% | 3 hours |
| src/utils/auth.ts | 0% | +80% → 80% | 2 hours |

### Priority 2: High Usage Frequency
Frequently used utilities

| File | Current | Imports | Effort |
|------|---------|---------|--------|
| src/utils/format.ts | 45% | 32 | 1 hour |
| src/hooks/useApi.ts | 60% | 28 | 1 hour |

### Priority 3: High Complexity
Bug-prone code

| File | Current | Complexity | Effort |
|------|---------|------------|--------|
| src/components/Form.tsx | 45% | 15 | 2 hours |

### Expected Results
Current: 68%
After Priority 1: 75%
After Priority 2: 80%
After Priority 3: 85%
```

## Response Template
```
## Test Coverage Analysis Results

**Project**: [name]

### Overall Status
| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Lines | 68% | 80% | -12% |
| Branches | 55% | 75% | -20% |
| Functions | 72% | 85% | -13% |

### Untested Critical Files (5)
1. `src/services/payment.ts` - Payment logic (CRITICAL)
2. `src/utils/auth.ts` - Auth utilities (HIGH)
3. `src/hooks/useCart.ts` - Cart hook (HIGH)

### Low Coverage Files (< 50%)
1. `src/components/CheckoutForm.tsx` - 45%
2. `src/services/api.ts` - 38%

### Recommended Actions
1. [ ] Add payment.ts unit tests (expected +5% overall)
2. [ ] Create auth.ts test file (expected +3% overall)
3. [ ] Improve CheckoutForm component tests

### Next Steps
Use `test-generator` skill to auto-generate tests for these files.
```

## Best Practices
1. **Meaningful Coverage**: Focus on critical code, not just numbers
2. **Gradual Improvement**: Don't aim for 100% at once
3. **Branch Coverage**: More important than line coverage
4. **Test Quality**: Avoid meaningless tests just for coverage
5. **CI Integration**: Fail build on coverage decrease

## Integration
- `test-generator` skill: Auto-generate missing tests
- `code-reviewer` skill: Test quality review
- `/generate-tests` command: Execute test generation

## Notes
- Uses coverage report files (lcov, coverage.json) if available
- Estimates based on file analysis if no report
- 100% coverage is not the goal, focus on critical code
