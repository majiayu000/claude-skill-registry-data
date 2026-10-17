---
name: stack-minimality-evidence
description: Measure observable complexity, dependency, test, build, and database effects of changes in Ruby, Rails, React, TypeScript, and PostgreSQL without fabricating savings.
license: MIT
---
# Stack Minimality Evidence

## Purpose
Turn "this is smaller" into evidence that can be recomputed from the actual repository. This skill does not invent a counterfactual baseline.

## Activate when
Use for requests to measure diff size, dependency changes, test/build effects, query improvements, or other quantitative consequences of simplification.

## Repository inspection
Inspect the actual Git diff, lockfiles, test output, build artifacts, package metadata, and database query-plan evidence available to the repository.

## Decision rules
Measure only observable quantities:
- actual added and deleted lines and changed files;
- added or removed gems and npm packages using manifests and lockfiles;
- focused and full test runtime only when actually run;
- JavaScript and CSS bundle size only from an actual build;
- PostgreSQL behavior from real EXPLAIN ANALYZE, BUFFERS evidence;
- Rails query counts or allocations only when the repository has a reproducible measurement path.

Never convert external benchmark numbers into this project's measurements. Never calculate savings against code that was never implemented.

## Implementation procedure
1. Capture repository state before and after where possible.
2. Record exact commands and outputs.
3. Separate structural evidence from performance evidence.
4. Mark unmeasured effects as unknown.
5. Preserve the repository's existing benchmark and CI conventions.

## Anti-patterns / failure modes
- Fabricated line, token, cost, speed, or performance savings.
- Comparing different workloads or data sets as if they were equivalent.
- Calling an unmeasured optimization faster.
- Treating fewer files as proof of lower operational risk.
- Re-running unchanged checks only to make a report look stronger.

## Reference example

Structural evidence is recomputed from the actual working-tree diff, never from an imagined baseline. After removing `OrderTotalCalculator` (repository path shown as `/path/to/app`):

```bash
ruby bin/stack-minimality evidence /path/to/app
```

```json
{
  "schema_version": 1,
  "repository": "/path/to/app",
  "changed_files": 2,
  "added_lines": 2,
  "deleted_lines": 10,
  "file_delta": 2,
  "files": [
    {
      "path": "app/models/order.rb",
      "added": 2,
      "deleted": 1
    },
    {
      "path": "app/services/order_total_calculator.rb",
      "added": 0,
      "deleted": 9
    }
  ]
}
```

This proves the diff size only. It says nothing about runtime cost; a performance claim needs its own measured baseline and workload.

## Agent review checklist
- [ ] Metrics come from the actual repository.
- [ ] Comparable baseline and workload exist for performance claims.
- [ ] Hypothetical savings are not presented as measured.
- [ ] Commands and evidence are traceable.
- [ ] Unknown effects are explicitly identified.

## Verification
Recompute structural metrics from the same Git diff. Preserve raw performance evidence for claims that depend on runtime measurement.

## Source foundation
- https://ponytail.dev/
- https://github.com/DietrichGebert/ponytail
- Git and repository benchmark conventions
