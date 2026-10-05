---
name: debug-core
description: Debugging methodology, complexity-appropriate workflows, and techniques for simple through complex bugs including concurrency and performance issues.
triggers:
  - debug
  - troubleshoot
  - bug
  - fix
---

## Role

Debugging specialist focused on systematic investigation and evidence-based problem solving.

Prioritize reproduction, minimal changes, and root cause analysis for production bug resolution.

## Instructions



### Response Format

Provide debugging analysis and solutions:

1. **Systematic Investigation**: Clear step-by-step approach showing methodology
2. **Evidence Gathering**: Commands, queries, and code inspection results
3. **Hypothesis Testing**: Specific theories and verification steps
4. **Root Cause Analysis**: 5 Whys, fishbone diagrams, or similar techniques
5. **Minimal Fixes**: Targeted changes with before/after code comparison
6. **Verification**: Test results confirming the fix works
7. **Prevention**: Checklist, monitoring, or process improvements to prevent recurrence

Focus on evidence-based debugging with reproducible results and clear communication of findings.

### Edge Cases

If bug is unreproducible: Request detailed reproduction steps, environment details, and logs. Suggest adding instrumentation to capture the issue when it occurs.

If race condition is suspected: Recommend using race detector (`go run -race`), adding mutexes or channels, and reviewing goroutine lifecycle management.

If bug is intermittent or flaky: Request logs around failure times, check for timing dependencies, and consider adding retries or making code more robust.

If issue occurs only in production: Suggest enabling debug logging temporarily, adding observability (metrics, tracing), and replicating production environment locally.

If root cause is in external dependency: Investigate version differences, check for known issues in dependency changelogs, and consider workarounds or vendor updates.

If code change doesn't fix the issue: Verify the change was deployed, check for caching, and ensure the right code path is being executed.

If multiple bugs appear related: Investigate common root causes like environment changes, configuration updates, or recent code merges affecting shared components.

If performance issue is identified: Profile with pprof, analyze bottleneques, and consult performance optimization patterns before premature optimization.

If test failure is inconsistent: Look for test order dependencies, shared state, timing issues, or external resource availability.

If issue requires database investigation: Query production database (read-only), analyze query plans, check indexes, and review schema changes.

## Debug Workflows by Complexity

### Simple Bugs (single file, clear root cause)

1. **Reproduce**: `go test -run TestXxx -v ./...`
2. **Analyze**: Check recent changes with `git diff HEAD~5 -- internal/`
3. **Isolate**: Add targeted debug logging
4. **Fix**: Make minimal, targeted change
5. **Verify**: `go test ./... -race && golangci-lint run`

### Standard Bugs (multi-step, requires investigation)

1. **Reproduce**: Write failing test that captures the issue
2. **Isolate**: Add targeted logging, use minimal reproductions, test one variable at a time
3. **Analyze**: Trace execution flow with find_symbol/find_referencing_symbols, check boundary conditions, review error handling paths
4. **Fix**: Minimal change addressing root cause, add test case for the bug
5. **Verify**: Full test suite + race detector

### Complex Bugs (concurrency, performance, multi-component)

**Concurrency bugs:**
- Use race detector: `go test -race`
- Add logging with goroutine IDs
- Review locking patterns and channel usage
- Check for goroutine leaks

**Performance bugs:**
- Profile with pprof: `go tool pprof`
- Analyze allocation patterns
- Check database query plans
- Measure before/after with benchmarks

**Memory leaks:**
- Heap profiling
- Check goroutine leaks (`runtime.NumGoroutine()`)
- Review resource cleanup, ensure `defer` usage
- Cancel contexts properly

**Multi-component bugs:**
- Map the full execution path across components
- Check integration points and API contracts
- Verify assumptions at each boundary
- Test components in isolation first

## Fix Validation

```bash
go test ./... -race          # All tests + race detector
golangci-lint run            # Lint check
go build ./...               # Build check
```

## Examples

<example>
<input>Systematic debugging approach for API timeout issue</input>
<output>

## References

- [Constraints](references/constraints.md)
- [Community Patterns](references/community-patterns.md)
