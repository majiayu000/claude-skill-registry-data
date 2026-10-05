---
name: review-perf
description: Performance analysis for algorithmic complexity, memory leaks, N+1 queries, and render issues. Use when code feels slow, after adding loops/queries, or before scaling up.
argument-hint: '[--staged | --unpushed | --changed | --all]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Performance

Performance analysis for common bottlenecks and inefficiencies.

## Usage

```
/review-perf                  # Review context-related code
/review-perf --staged         # Review staged changes
/review-perf --unpushed       # Review files changed across all unpushed commits
/review-perf --changed        # Review unstaged changes
/review-perf --all            # Full codebase audit (parallel agents)
```

## Scope

| Flag | Scope | Method |
|------|-------|--------|
| (none) | Context-related code | Files from the current conversation context: any files the user has discussed, opened, or that you have read/edited in this session. If no conversation context exists, ask the user to specify files or use `--staged`/`--changed`/`--all`. |
| `--staged` | Staged changes | `git diff --cached --name-only` |
| `--unpushed` | Files changed across unpushed commits | `git diff --name-only $(git rev-list HEAD --not --remotes \| tail -1)^..HEAD` |
| `--changed` | Unstaged changes | `git diff --name-only` |
| `--all` | Full codebase | Glob source files, parallel agents |

`--unpushed` derives its range from `git rev-list HEAD --not --remotes` (oldest unpushed commit's parent → HEAD). If nothing is unpushed, or there is no remote/upstream (or the range walks back to the root commit) so it can't be determined reliably, stop and ask the user to pick another scope.

## Gotchas
- Default scope (no flag) uses conversation context, which may be stale from an earlier part of the session. The review silently targets the wrong files if context has shifted.
- Blindly adding `useMemo`/`useCallback` to fix re-render warnings can worsen performance on simple components — memoization has overhead and only helps when the memoized value is expensive or the child does reference equality checks.

## Workflow

1. **Determine scope** based on flags (see Scope table above)
2. **Review each file** against all 5 categories in the Performance Checklist below: Algorithmic Complexity, Database/Query Patterns, Memory Management, UI/Render Performance, Network/IO
3. **Parallelize** if scope has >5 files: spawn one sub-agent per category, each scanning all files for that category. Merge results and deduplicate.

   Dispatch workers that return findings without editing files. Disable delegation tools where supported; read-only access alone does not prevent delegation. Any coordinating role needs explicit subtasks, a descendant limit, and a stopping condition in its brief.
4. **Classify severity** for each finding:
   - **Critical**: User-facing slowdown, data loss risk, or resource exhaustion (e.g., memory leak, N+1 on hot path)
   - **High**: Measurable inefficiency on a common code path but not immediately user-visible (e.g., O(n²) on lists typically < 100 items but growing)
   - **Medium**: Suboptimal pattern that could become a problem at scale (e.g., missing pagination, sequential requests that could be parallel)
   - **Suggestion**: Optimization opportunity with marginal current impact
5. **Report findings** grouped by severity using the Output Format below

## Performance Checklist

### Algorithmic Complexity

- Nested loops over the same collection (O(n²) or worse) — replace with a lookup map
- Repeated expensive calculations inside a loop — hoist outside
- Array scans that could exit early — use `.find()` or equivalent

### Database/Query Patterns

- Queries inside loops (N+1) — use eager loading / batch fetch
- Loading all rows without a LIMIT — add pagination
- `SELECT *` when only a few columns are needed — select explicitly
- Missing indexes on columns used in WHERE, ORDER BY, JOIN, or foreign keys

### Memory Management

- Connections or file handles opened without a `finally`/close — always close in `finally`
- Caches with no size or TTL bound — use LRU or TTL-bounded cache
- Event listeners added without a corresponding removal — return cleanup in `useEffect`

### UI/Render Performance

- Inline object/function literals passed as props causing reference churn — memoize with `useMemo`/`useCallback`
- Long lists rendered without virtualization — use a virtualized list component
- Heavy synchronous computation on the main thread — offload to a web worker or chunk the work

### Network/IO

- Sequential `await` calls for independent requests — use `Promise.all`
- The same request fired multiple times without deduplication — use SWR/React Query or a request cache

For annotated BAD/GOOD code examples for each category, see `references/perf-checklist.md`.

## Output Format

```markdown
## Performance Review: {scope}

### Critical (user-facing slowdown)
- {file}:{line} - {issue type}: {description}
  **Impact:** {why it matters}
  **Fix:** {solution with code example}

### High Priority
- {file}:{line} - {issue}
  **Fix:** {solution}

### Medium Priority
- {file} - {issue}

### Suggestions
- {optimization opportunity}
```

## Examples

**Staged changes introduce N+1 query:**
> /review-perf --staged

Reviews staged files and catches a new user list endpoint that queries posts per user in a loop. Reports it as Critical with the impact ("100 users = 101 queries") and provides a fix using eager loading with `include`.

**Full audit finds memory leak in dashboard:**
> /review-perf --all

Parallel agents scan the full codebase by category. Finds an event listener in the dashboard component that is never cleaned up on unmount, plus an unbounded in-memory cache growing with every API call.

## Troubleshooting

### False positive on a rarely-executed code path
**Solution:** If the flagged code runs only during initialization or in admin-only flows, note the expected data size in a code comment. Re-run the review and the context will help distinguish hot paths from cold ones.

### Cannot determine algorithmic complexity without runtime data
**Solution:** Add a brief comment with the expected input size (e.g., `// n is typically < 50`) so static analysis can assess impact. For uncertain cases, use `/perf-test` to measure actual performance with realistic data.

## Notes

- Focus on measurable impact, not micro-optimizations
- Consider data size - O(n²) on 10 items is fine, on 10,000 is not
- For `--all`, use parallel agents per category
- Database issues often have the highest impact
- UI issues matter most for user-facing code
