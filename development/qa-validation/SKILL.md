---
name: qa-validation
description: Validate implementation against test cases and acceptance criteria. Use when checking if code works correctly, validating against user-provided test cases, or verifying acceptance criteria are met. Gets test cases from user input or previous workflow stages.
allowed-tools: Read, Grep, Glob, Bash
---

# QA Validation Skill

Validate implementation against test cases and acceptance criteria to ensure code works correctly.

## When to Use

This skill activates when:
- User provides test cases to validate against
- Checking if implementation meets acceptance criteria
- Verifying all scenarios work correctly
- After unit tests are generated to validate coverage
- User mentions "validate", "verify", "check", "QA"

## Validation Categories

### Functional Tests
- Core functionality works as expected
- Input/output contracts are honored
- Business logic is correct
- API responses match expected format

### Error Handling
- Errors are caught and handled gracefully
- Error messages are informative
- Recovery mechanisms work
- Edge cases don't crash the application

### Edge Cases
- Boundary conditions are handled
- Empty/null inputs don't crash
- Large inputs are processed correctly
- Concurrent operations work safely

### Acceptance Criteria
- User requirements are satisfied
- Feature behaves as specified
- Integration points work correctly
- Performance is acceptable

## Validation Process

1. **Gather Test Cases**:
   - From user-provided test cases in the request
   - From previous workflow stages (unit_test output)
   - From acceptance criteria in task description

2. **For Each Test Case, Validate**:
   - Functional requirements are met
   - Error handling works correctly
   - Edge cases are handled
   - Performance is acceptable

3. **Report Results**:
   - Pass/fail status for each test case
   - Issues found with specific details
   - Recommendations for fixes
   - Overall pass rate

## Output Format

```
## Validation Results

**Status**: PASSED / FAILED
**Pass Rate**: X%

### Scenarios Validated
1. [Scenario Name] - PASSED/FAILED
   - Details...

### Issues Found
1. [Issue Description]
   - Location: [file:line]
   - Severity: Critical/Warning/Info
   - Recommendation: [fix suggestion]

### Recommendations
1. [Actionable recommendation]
```

## Best Practices

- Be thorough in validation
- Document all findings clearly
- Prioritize critical issues
- Suggest actionable fixes
- Consider user experience
- Test both positive and negative scenarios
