---
name: lizard-complexity
description: "Run Lizard against production source to enforce per-function cyclomatic complexity (CCN), NLOC, and parameter-count thresholds - language-agnostic (30+ languages). Scoped to production code via `-x\"./tests/*\"`; test complexity is reviewed separately. Use when a codebase spans several languages and needs one complexity gate across all of them, or when a function has grown unreviewable and the team wants a numeric threshold in CI."
metadata:
  keywords: "lizard, cyclomatic-complexity, ccn, code-metrics, quality-gate"
  version: "1.1.5"
---

# lizard-complexity

Lizard analyzes source code per function for **NLOC** (non-comment LoC),
**CCN** (cyclomatic complexity), token count, and parameter count
across 30+ languages including C/C++, Java, Python, JavaScript, Go,
Rust, TypeScript, Swift, Kotlin (per the [Lizard README]). Default CCN
warning threshold is 15.

## When to use

- Polyglot codebase where per-language linters give inconsistent
  complexity metrics.
- Adding a CCN ceiling to CI without buying a commercial scanner.
- One-off audit of "where is the most complex code?" before a
  refactor.

## Step 1 - Install

```bash
pip install lizard
```

Or run the standalone script:

```bash
python lizard.py path/to/code
```

Per the [Lizard README], no external deps required.

## Step 2 - Baseline scan

```bash
lizard src/
```

Default output groups by file with per-function NLOC/CCN/token/param
counts. Default warning threshold: CCN ≥ 15.

## Step 3 - Set production-only thresholds

```bash
lizard src/ \
  -x"./tests/*" \
  -x"./vendor/*" \
  -C 10 \
  -L 100 \
  -a 5
```

| Flag | Meaning |
|---|---|
| `-x PATTERN` | Exclude (must include `tests/**` for production-only scope) |
| `-C N` | CCN warning threshold (default 15; tighten to 10 for new codebases) |
| `-L N` | Max function NLOC (default 1000; tighten to 80 - 100) |
| `-a N` | Max parameter count (5 = "if you need more, pass an object") |

## Step 4 - CSV/XML for CI

```bash
# CSV for grep / jq pipelines
lizard src/ -x"./tests/*" -C 10 --csv > lizard.csv

# XML for CI parsers (cppncss-style)
lizard src/ -x"./tests/*" -C 10 -X > lizard.xml

# HTML for human review
lizard src/ -x"./tests/*" -C 10 -H > lizard.html
```

## Step 5 - Fail CI on warnings

```bash
lizard src/ -x"./tests/*" -C 10 -L 100 -a 5 -w
EXIT=$?
if [ "$EXIT" -ne 0 ]; then
  echo "Complexity threshold breached. See report."
  exit 1
fi
```

`-w` prints warnings only (clang/gcc style). Lizard exits non-zero
when any function exceeds the configured threshold.

## Step 6 - Per-language scope

```bash
# Only Python
lizard src/ -l python -C 10

# Only TypeScript + JS
lizard src/ -l typescript -l javascript -C 10
```

Useful when a polyglot repo has language-specific budgets (e.g.,
Python tolerates higher CCN than C).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Run on whole repo including tests | Test setup helpers ("create user with 12 fields") look complex; tests get refactored away from clarity | Always exclude `tests/`, `spec/` (Step 3) |
| Set CCN threshold to default (15) | Too lax for new code | Start at 10 for new code; track existing code as baseline |
| Block PRs on absolute count | Legacy code can't add a single line | Diff-only: scan PR-changed functions only with `git diff --name-only` filter |
| Refactor for CCN at expense of clarity | Splitting a clear linear function into 4 helpers raises overall complexity | Use CCN as a smell signal, not a hard rule |
| Skip parameter-count guard | "God functions" with 12 args slip through | `-a 5` enforces object-arg style |

## Limitations

- Lizard's CCN counts decision points (if/else/case/&&/\|\|/?:); doesn't
  reflect cognitive complexity (nesting depth weight). Use SonarQube /
  `sonarqube-maintainability-gate` for cognitive
  complexity if needed.
- No per-class metrics for OO code beyond per-method.

## References

- [Lizard README] - CLI reference, language list, threshold flags

[Lizard README]: https://github.com/terryyin/lizard
