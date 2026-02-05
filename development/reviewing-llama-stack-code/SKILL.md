---
name: Reviewing Llama Stack Code
description: Use when reviewing code or PRs in the llama-stack repository (llamastack/llama-stack on GitHub). Provides specialized knowledge about Llama Stack's architecture, testing patterns (recordings folders), backward compatibility requirements, distributed system considerations, and code review focus areas specific to this project.
---

# Llama Stack Code Review Guidelines

This skill provides specialized knowledge for reviewing code in the Llama Stack project (https://github.com/llamastack/llama-stack).

## When to Use This Skill

Invoke this skill when:
- Reviewing pull requests in the llama-stack repository
- Analyzing code changes in llama-stack
- Providing feedback on llama-stack contributions
- Understanding llama-stack architecture patterns

## Critical: Recordings Folders

**MOST IMPORTANT**: Llama Stack uses `recordings/` folders containing JSON response files for CI testing.

### Review Approach for Recordings

- **Ignore all content** in `recordings/` folders and any JSON files within them
- **Do NOT review** the content of recording files - they are auto-generated test fixtures
- **Instead**: Verify that CI checks are passing
- **Focus on**: Actual code changes, not recorded responses

### Why This Matters

- Recording files can be hundreds or thousands of lines of JSON
- They are generated automatically and don't require human review
- Reviewing them wastes time and provides no value
- CI validates that recordings work correctly

### Example

```
# DO NOT review in detail:
tests/recordings/test_foo/response_1.json (500 lines of JSON)
tests/recordings/test_bar/response_2.json (800 lines of JSON)

# Instead, confirm:
✓ CI checks passing
✓ Test code changes are valid
✓ Actual implementation code is reviewed
```

## Llama Stack Architecture Patterns

### API Backward Compatibility

Llama Stack emphasizes API stability:
- Verify new API changes maintain backward compatibility
- Check that existing clients won't break
- Flag breaking changes explicitly and ensure they're intentional
- Validate deprecation paths are provided for removed features

### Distributed System Considerations

Llama Stack operates in distributed environments:
- **Race conditions**: Check for proper synchronization and locking
- **Eventual consistency**: Verify code handles delayed updates correctly
- **Network failures**: Ensure retries and timeout handling
- **Partial failures**: Check that failures in one component don't cascade

### Error Propagation

Errors must flow correctly across component boundaries:
- Verify errors include sufficient context for debugging
- Check that error types are appropriate for the abstraction level
- Ensure errors aren't swallowed or logged without handling
- Validate error messages are actionable for users

### Integration Points

Llama Stack has well-defined integration patterns:
- Verify new integrations follow established patterns
- Check that provider interfaces are implemented completely
- Ensure configuration handling is consistent
- Validate that new components integrate with existing telemetry/logging

### Performance for Distributed Workloads

Performance is critical at scale:
- Confirm performance impact is acceptable for distributed deployments
- Check for N+1 query problems in data access
- Verify caching strategies are appropriate
- Ensure batch operations are used where possible

## Review Checklist for Llama Stack PRs

Use this checklist in addition to standard code review criteria:

1. **Recordings**: Confirmed recordings folders ignored, CI status checked ✓
2. **Backward Compatibility**: API changes are backward compatible ✓
3. **Distributed Systems**: Race conditions, consistency, failures handled ✓
4. **Error Handling**: Errors propagate correctly with context ✓
5. **Integration Patterns**: Follows established patterns ✓
6. **Performance**: Acceptable impact for distributed workloads ✓
7. **Testing**: Tests cover distributed scenarios, not just happy path ✓

## Common Llama Stack Patterns

### Provider Interface Pattern

Llama Stack uses provider interfaces for extensibility:
```python
class MyProvider(BaseProvider):
    async def initialize(self):
        # Setup logic
        pass

    async def execute(self, request):
        # Implementation
        pass
```

Verify:
- All required methods are implemented
- Async patterns are used consistently
- Error handling follows provider conventions

### Configuration Pattern

Configuration is hierarchical and validated:
- Check that new config options are documented
- Verify defaults are sensible
- Ensure validation happens early with clear error messages

## Anti-Patterns to Flag

- **Blocking I/O**: Should use async patterns
- **Hardcoded timeouts**: Should be configurable
- **Missing telemetry**: New operations should emit metrics/logs
- **Tight coupling**: Components should use defined interfaces
- **Ignored recordings**: Don't spend time reviewing recording files

## Testing Expectations

Llama Stack has specific testing patterns:
- Unit tests for individual components
- Integration tests using the recordings pattern
- Distributed scenario tests for multi-component features
- Performance benchmarks for critical paths

Verify that:
- New features include appropriate test coverage
- Tests cover error cases, not just success paths
- Recordings are generated for integration tests (but don't review the recordings content)

## Documentation Standards

Code changes should include:
- API documentation for public interfaces
- Architecture decision context for significant changes
- Migration guides for breaking changes
- Performance characteristics for new features

## Final Recommendation

After reviewing a Llama Stack PR using these guidelines:

1. Summarize findings specific to Llama Stack patterns
2. Call out any violations of distributed system best practices
3. Confirm recordings folders were handled correctly (ignored, CI checked)
4. Note any backward compatibility concerns
5. Provide overall recommendation with Llama Stack context

Remember: The most common mistake is spending time reviewing recordings folder content. Always check CI status instead.
