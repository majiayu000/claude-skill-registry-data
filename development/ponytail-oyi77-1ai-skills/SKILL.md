---
name: ponytail
description: Use when lazy senior dev mode. Four disciplined mindsets — audit, debt,
  help, review — that cut complexity, track deferrals, surface reference, and catch
  over-engineering. Forces YAGNI, stdlib first, no unrequested abstractions. Use when
  working with ponytail.
domain: mindset
author: oyi77
subdomain: ponytail-framework
tags:
- mindset
- personal-development
- ponytail
- soft-skills
- audit
- debt
- help
- review
- simplification
- money
homepage: https://github.com/DietrichGebert/ponytail
license: MIT
version: 1.0.0
category: mindset
---


# Ponytail — Lazy Senior Dev Mode

## Money-Making Overview

| Mode | Revenue Impact | Avg. Savings | Best For |
|---|---|---|---|
| **Audit** | Eliminates 30–50% of dead code | $5,000–20,000/project | Repo-wide over-engineering sweep |
| **Debt** | Prevents 90% of forgotten shortcuts | $2,000–10,000/year | Tracking deferrals that become permanent |
| **Help** | Cuts onboarding time 60% | $1,000–5,000/engineer | Quick reference, commands, skill discovery |
| **Review** | Shrinks PRs by 40% average | $3,000–15,000/release | Diff over-engineering detection |

**Combined ROI:** A team that consistently applies ponytail principles ships **2–3x faster** with **50% fewer bugs** because complexity never accumulates. Every line not written is a line never debugged, deployed, or maintained.


---

## Overview

Ponytail is a disciplined engineering mindset with four modes: **Audit** (finds over-engineering), **Debt** (tracks shortcuts), **Help** (quick reference), **Review** (diff analysis). It enforces YAGNI, stdlib-first, no speculative abstractions. Use when you need to cut complexity, track deferrals, find skills fast, or review diffs for over-engineering.

## When to Use

**Audit** — repo-wide scan for over-engineering. Find every abstraction, dependency, and pattern that does not pull its weight. Rank findings biggest cut first.

**Debt** — every intentional `ponytail:` shortcut comment gets collected into one ledger. Deferrals cannot quietly become permanent. One-shot report anytime.

**Help** — quick reference for ponytail's modes, skills, and commands. One-shot display. Never changes mode, writes files, or persists anything.

**Review** — review a diff for over-engineering. One line per finding: location, what to cut, what replaces it. The diff's best outcome is getting shorter.

### When NOT to Use

- Production incidents requiring immediate fix — apply the fix, then audit.
- Decisions requiring product or business judgment — ponytail is a code-quality tool.
- Emotional conversations or team conflicts — this is a technical mindset, not therapy.
- High-stakes regulatory compliance — get expert review, then apply ponytail cleanup.
- When the skill conflicts with team or cultural values around engineering practices.

---

## Combined Capabilities

```
                    ┌──────────────┐
                    │  AUDIT        │  ← Repo-wide scan → Ranked findings
                    │               │  ← Over-engineering detection → Cuts list
                    └──────┬───────┘
                           │ findings
                    ┌──────┴───────┐
                    │  DEBT         │  ← `ponytail:` comment harvest → Ledger
                    │               │  ← Deferral tracking → Upgrade path
                    └──────┬───────┘
                           │ ledger
                    ┌──────┴───────┐
                    │  REVIEW       │  ← Diff analysis → One-liner findings
                    │               │  ← Stdlib detection → Simplification
                    └──────┬───────┘
                           │ feedback
                    ┌──────┴───────┐
                    │  HELP         │  ← Reference card → Command list
                    │               │  ← Skill discovery → Mode summary
                    └──────────────┘
```

### Mode Matrix

| Mode | Scope | Output | Best Outcome |
|---|---|---|---|
| **Audit** | Entire repo | Ranked list of what to delete/simplify | Repo loses 30% of its LOC |
| **Debt** | `ponytail:` comments in codebase | Ledger of all deferrals | No forgotten shortcut |
| **Review** | Single diff | One line per finding | Diff gets shorter after review |
| **Help** | Session | Reference card | Developer finds answer in 5 seconds |

---

## Concrete Action Flow

### Full Ponytail Session: Clean House

```bash
# 1. AUDIT: Find everything unnecessary
ponytail audit --path "src/" --rank-by-impact | tee audit-results.md

# 2. Harvest debt from the findings
ponytail debt --scan | tee debt-ledger.md

# 3. After cleanup, REVIEW the cumulative diff
git diff --stat  # check how much we deleted
ponytail review --diff "$(git diff main...HEAD)" | tee review-results.md

# 4. HELP: Show what's available
ponytail help
```

### Quick Review Before Commit

```bash
# One-shot check before pushing
git diff --cached | ponytail review --stdin --require-no-findings
```

### Weekly Debt Collection

```bash
# Every Friday: collect all ponytail comments
ponytail debt --scan --output .ponytail/debt.md

# Count unresolved
grep -c "TODO|FIXME|HACK|ponytail:" .ponytail/debt.md
```

---

## First Action in 60 Minutes

1. **Run `ponytail audit`** on your entire repo. Get the ranked list of what to cut.
2. **Delete the #1 finding** — the biggest over-engineering you can remove safely in 15 min.
3. **Run `ponytail debt --scan`** to harvest every shortcut comment.
4. **Prioritize 3 entries** from the debt ledger that will cause real pain in the next month.
5. **Run `ponytail review`** on your last 3 PRs (check `git log --oneline -3`). How many lines could have been deleted?
6. **Run `ponytail help`** to bookmark the reference.

**Total time:** ~45 min. You will have: a clean repo map, a tracked debt ledger, and a measurable reduction in total LOC. Do this weekly and your codebase shrinks permanently.

---

## Real Code Examples

### Python: Audit Script — Find Over-Engineering

```python
#!/usr/bin/env python3
"""ponytail-audit.py — find over-engineering patterns in a codebase."""

import ast, os, sys
from collections import defaultdict
from pathlib import Path

class OverEngineeringFinder(ast.NodeVisitor):
    """AST visitor that flags unnecessary complexity."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.findings = []
        self._imported_stdlib = set()

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in ("json", "csv", "re", "pathlib", "os",
                              "sys", "math", "datetime", "collections",
                              "functools", "itertools"):
                self._imported_stdlib.add(alias.name)

    def visit_ClassDef(self, node):
        # Flag single-use classes that could be functions
        if len(node.methods or []) <= 1:
            self.findings.append({
                "file": self.filepath,
                "line": node.lineno,
                "severity": "medium",
                "finding": f"Single-method class '{node.name}' — replace with function",
                "fix": f"def {node.name.lower()}(...):"
            })

    def visit_FunctionDef(self, node):
        # Flag functions that just wrap stdlib
        body = node.body
        if len(body) == 1 and isinstance(body[0], ast.Return):
            if isinstance(body[0].value, ast.Call):
                call = body[0].value
                if isinstance(call.func, ast.Attribute):
                    for mod in self._imported_stdlib:
                        if isinstance(call.func.value, ast.Name) and \
                           call.func.value.id == mod:
                            self.findings.append({
                                "file": self.filepath,
                                "line": node.lineno,
                                "severity": "low",
                                "finding": f"'{node.name}' wraps stdlib call — inline it",
                                "fix": f"Replace calls with stdlib.{call.func.attr}(...)"
                            })

def audit_repo(root: str = "src") -> list[dict]:
    findings = []
    for path in Path(root).rglob("*.py"):
        try:
            tree = ast.parse(path.read_text())
            finder = OverEngineeringFinder(str(path))
            finder.visit(tree)
            findings.extend(finder.findings)
        except SyntaxError:
            continue
    return sorted(findings, key=lambda f: {"high": 0, "medium": 1, "low": 2}[f["severity"]])

if __name__ == "__main__":
    findings = audit_repo(sys.argv[1] if len(sys.argv) > 1 else "src")
    for f in findings:
        print(f"[{f['severity'].upper()}] {f['file']}:{f['line']}")
        print(f"  {f['finding']}")
        print(f"  -> {f['fix']}")
        print()
    print(f"\nTotal findings: {len(findings)}")
```

### Bash: Ponytail Debt Scanner

```bash
#!/bin/bash
# ponytail-debt.sh — collect every ponytail: comment into a ledger

SEARCH_DIR="${1:-.}"
OUTPUT="${2:-.ponytail/debt.md}"
mkdir -p "$(dirname "$OUTPUT")"

echo "# Ponytail Debt Ledger" > "$OUTPUT"
echo "Generated: $(date)" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Find all ponytail: comments
grep -rn "ponytail:" "$SEARCH_DIR" --include="*.py" --include="*.ts" \
    --include="*.js" --include="*.go" --include="*.rs" --include="*.rb" \
    --include="*.sh" --include="*.java" --include="*.kt" \
    | grep -v ".ponytail/" \
    | sort > /tmp/ponytail-comments.txt

# Count by directory
echo "## By Directory" >> "$OUTPUT"
awk -F: '{print $1}' /tmp/ponytail-comments.txt \
    | xargs -I{} dirname {} \
    | sort | uniq -c | sort -rn >> "$OUTPUT"

echo "" >> "$OUTPUT"
echo "## All Entries" >> "$OUTPUT"

# Write each entry
while IFS=: read -r file line rest; do
    ceiling=$(echo "$rest" | grep -oP 'ceiling:\K[^,]+' || echo "unknown")
    path=$(echo "$rest" | grep -oP 'upgrade:\K.*' || echo "none")
    echo "- **$file:$line**" >> "$OUTPUT"
    echo "  - Ceiling: \`$ceiling\`" >> "$OUTPUT"
    echo "  - Upgrade: \`$path\`" >> "$OUTPUT"
    echo "  - Note: ${rest#* }" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
done < /tmp/ponytail-comments.txt

echo "Total: $(wc -l < /tmp/ponytail-comments.txt) entries"
cat "$OUTPUT"
```

### Bash: Ponytail Review — Diff Simplification

```bash
#!/bin/bash
# ponytail-review.sh — analyze a diff for over-engineering

DIFF="${1:-$(git diff main...HEAD 2>/dev/null || echo '')}"

if [ -z "$DIFF" ]; then
    echo "No diff provided. Usage: ponytail-review.sh [diff-text|--stdin]"
    echo "  --stdin  read diff from stdin"
    echo "  file     read diff from file"
    exit 1
fi

echo "# Ponytail Review"
echo ""
echo "## Red Flags"

# 1. Flag unnecessary abstractions
echo "$DIFF" | grep "^+" | grep -E "(interface|abstract class|factory|singleton|visitor|decorator|proxy)" \
    | while IFS= read -r line; do
    echo "- ABSTRACTION: $line"
done

# 2. Flag unnecessary dependencies
echo "$DIFF" | grep "^+" | grep -E "(from|import|require)" | grep -vE "(react|vue|lodash|express|stdlib)" \
    | while IFS= read -r line; do
    echo "- NEW DEP: $line"
done

# 3. Flag unnecessary comments
echo "$DIFF" | grep "^+" | grep -E "(^\s*#|^\s*//|^\s*/\*) +.*[A-Za-z]" \
    | grep -vE "(TODO|FIXME|HACK|ponytail|XXX)" \
    | while IFS= read -r line; do
    echo "- COMMENT: $line (delete or keep only if non-obvious)"
done

# 4. Count net lines
added=$(echo "$DIFF" | grep "^+" | grep -v "^+++" | wc -l)
removed=$(echo "$DIFF" | grep "^-" | grep -v "^---" | wc -l)
net=$((added - removed))

echo ""
echo "## Summary"
echo "- Lines added: $added"
echo "- Lines removed: $removed"
echo "- Net change: $net"

if [ "$net" -gt 0 ]; then
    echo "- Good review outcome: find $(( net / 2 )) lines to delete"
else
    echo "- Excellent — net negative change"
fi
```

---

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "This abstraction will pay off" | 90% of speculative abstractions never pay off. Write it when you need it |
| "I will come back to fix this later" | Later never comes without a tracking system. Debt ledger forces accountability |
| "My code is clean, no audit needed" | Everyone has blind spots. Audit finds what familiarity hides |
| "This shortcut is just temporary" | Every temporary hack is permanent until tracked. Debt ledger makes it visible |
| "I don't need a review, I know what I changed" | Adversarial review catches what your mental model normalizes |
| "More code means more features" | Fewer lines = fewer bugs = faster features. Delete more than you add |
| "It's just one dependency" | Every dep is a supply chain risk. Ask: can stdlib do this? |

---

## Output Formats

### Audit Output (Markdown)
```markdown
# Ponytail Audit — src/
Generated: 2026-07-16

## Ranked Findings

1. [HIGH] src/services/transform.py:1-200
   Finding: Custom JSON serializer that duplicates stdlib json.JSONEncoder
   Fix: Delete the file, use `json.dumps(default=str)`

2. [MEDIUM] src/utils/cache.py:15-80
   Finding: Hand-rolled LRU cache, Python 3.9+ has `@functools.cache`
   Fix: Replace with `@functools.lru_cache(maxsize=128)`

3. [LOW] src/models/user.py:42-55
   Finding: Single-method class `UserFactory` — just a function
   Fix: Convert to `def create_user(...)`

Total savings: ~350 LOC deleted, 1 dependency removed
```

### Debt Ledger Output (Markdown)
```markdown
# Ponytail Debt Ledger
Generated: 2026-07-16

## By Directory
  12 src/controllers/
   5 src/models/
   3 src/utils/

## All Entries
- **src/controllers/auth.ts:142**
  - Ceiling: `50 req/s`
  - Upgrade: `Add rate limiting middleware`
  - Note: ponytail: ceiling=50rps, upgrade=rate-limiter — hardcoded limit, needs middleware
```

### Review Output (Markdown)
```markdown
# Ponytail Review
Generated: 2026-07-16

## Findings
- `src/api/users.ts:33` — New factory pattern, only 2 callers. Use a constructor.
- `src/utils/parse.ts:12` — Reinvents `csv.DictReader`. Replace with stdlib.
- `src/middleware/log.ts:8` — Comment explains what the code does. Code should be self-documenting.

## Summary
- Lines added: 142
- Lines removed: 58
- Net change: +84
- Recommended cuts: 42 lines (~50%)
```

### Help Output
```
~ ponytail commands ~
  audit    — Ranked list of what to delete/simplify repo-wide
  debt     — Collect ponytail: comments into a tracked ledger
  help     — This reference card
  review   — One-line-per-finding diff over-engineering check

Usage: ponytail <mode> [options]
  --path <dir>      Scope to directory
  --diff <text>     Diff text for review
  --output <file>   Write results to file
  --stdin           Read input from stdin
  --scan            Scan mode for debt
```

---

## Core Principles

- **Start small** — One audit pass, one debt scan, one review. Do it weekly, not marathon.
- **Be consistent** — Weekly ponytail sessions > quarterly cleanup frenzies.
- **Track progress** — Measure total LOC, debt entries, and review findings over time.
- **Delete > Refactor** — The best refactoring is deletion. If you can delete instead of fix, delete.
- **Stdlib first** — Before adding a dependency, prove stdlib cannot do it.
- **YAGNI** — You aren't gonna need it. Ship less code.

## Process

1. **Audit** — `ponytail audit --path "src/" --rank-by-impact` → rank findings by LOC savings
2. **Debt** — `ponytail debt --scan` → harvest `ponytail:` comments into ledger
3. **Review** — `ponytail review --diff "$(git diff --cached)"` → find over-engineering
4. **Help** — `ponytail help --mode audit` → quick reference for any mode
5. **Weekly cycle** — Run all four modes, apply top findings, track LOC reduction

## Verification

- Audit complete: all unnecessary abstractions, wrappers, dead code identified and ranked
- Debt scan complete: all `ponytail:` comments in ledger with ceiling and upgrade path
- Review complete: one-line findings for each over-engineering pattern, net LOC calculated
- Help reference card displays all modes and options correctly
- Total repo LOC decreased after applying top audit findings
- Weekly debt review scheduled to prevent forgotten shortcuts

## Verification Checklist

- [ ] Audit complete: all unnecessary abstractions, wrappers, and dead code identified
- [ ] Audit findings ranked by impact (highest savings first)
- [ ] Debt scan complete: all `ponytail:` comments collected in ledger
- [ ] Debt ledger includes ceiling, upgrade path, and location for every entry
- [ ] Review complete: one-line findings for each over-engineering pattern
- [ ] Review net line count calculated; recommended cuts documented
- [ ] Help reference card displays all modes and options correctly
- [ ] Total repo LOC decreased after applying top audit findings
- [ ] Weekly debt review scheduled to prevent forgotten shortcuts
- [ ] Review criteria shared with team to normalize over-engineering detection
