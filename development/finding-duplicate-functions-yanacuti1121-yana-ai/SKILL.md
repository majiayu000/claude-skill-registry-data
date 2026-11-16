---
name: finding-duplicate-functions
description: "Use when auditing a codebase for semantic code duplication — functions that serve the same purpose but were implemented independently. Triggers on: 'find duplicate functions', 'semantic duplicates', 'duplicate code audit', 'same intent different implementation', 'consolidate functions', 'codebase duplication', 'redundant functions', 'llm-generated duplicates', 'function deduplication', 'duplicate detection'."
source: obra/superpowers-lab (MIT) — superpowers-lab/skills/finding-duplicate-functions
tier: TIER 3 — PRODUCTIVITY
---

# Finding Duplicate-Intent Functions
# Source: obra/superpowers-lab (MIT) — github.com/obra/superpowers-lab

Phát hiện duplicate **về mục đích** chứ không phải syntactic copy-paste.
LLM-generated codebases thường tạo hàm mới thay vì reuse hàm cũ — skill này tìm ra chúng.

---

## Khi nào dùng

- Codebase lớn với nhiều LLM-generated code (yamtam 3460+ skills)
- Có cảm giác "hàm này mình đã viết rồi"
- Muốn refactor trước khi codebase thêm phức tạp
- Sau khi merge nhiều PRs từ nhiều agents

---

## 5-Phase Workflow

```
Phase 1: EXTRACT    — enumerate tất cả functions/methods
Phase 2: CATEGORIZE — Haiku phân loại theo domain
Phase 3: SPLIT      — tách kết quả theo category
Phase 4: DETECT     — Opus tìm semantic duplicates per category
Phase 5: REPORT     — prioritized markdown report
```

**Quan trọng:** Dùng **Haiku cho categorize** (cheap), **Opus cho detect** (cần độ chính xác cao).
Không skip categorize — analyze toàn bộ catalog cùng lúc gây noise.

---

## Phase 1 — Extract Function Catalog

```bash
# JavaScript/TypeScript
grep -rn "^function \|^const .* = \(.*\) =>\|^async function \|^\s*[a-zA-Z].*([^)]*) {" \
  src/ --include="*.ts" --include="*.js" \
  | grep -v "test\|spec\|mock" \
  | awk -F: '{print $1 ":" $2 " " $3}' \
  > /tmp/function-catalog.txt

# Python
grep -rn "^def \|^    def \|^async def " src/ --include="*.py" \
  | grep -v "test_\|_test" \
  > /tmp/function-catalog.txt

# Count
wc -l /tmp/function-catalog.txt
```

---

## Phase 2 — Categorize by Domain (Haiku)

Prompt Haiku với từng batch 50-100 functions:

```
Categorize these functions into domain groups (utilities, validation,
error-handling, path-manipulation, string-transforms, date-formatting,
api-calls, data-transforms, auth, other).
Output JSON: { "category": ["file:line funcname", ...] }

Functions:
[paste batch from catalog]
```

---

## Phase 3 — Split by Category

```bash
# Sau khi Haiku trả về JSON
python3 -c "
import json, sys
data = json.load(sys.stdin)
for cat, funcs in data.items():
    with open(f'/tmp/category-{cat}.txt', 'w') as f:
        f.write('\n'.join(funcs))
    print(f'{cat}: {len(funcs)} functions')
" < /tmp/categorized.json
```

---

## Phase 4 — Detect Duplicates per Category (Opus)

Với mỗi category file, đọc source của từng function và hỏi Opus:

```
These functions are all in the [category] domain.
Identify groups of functions that have the SAME INTENT but different implementations.
"Same intent" means: given the same input, they should return equivalent output,
even if the code looks completely different.

For each duplicate group, list:
1. Which functions are duplicates
2. Which one is the "best" to keep (most complete, best tested)
3. Confidence: HIGH / MEDIUM / LOW

Functions with source code:
[paste function bodies]
```

---

## Phase 5 — Report Format

```markdown
# Duplicate Function Report — [date]

## HIGH PRIORITY (consolidate first)

### Group: URL parameter parsing
- `src/utils/url.ts:42 parseQueryParams` ← KEEP (has tests)
- `src/api/helpers.ts:18 extractUrlParams` ← REMOVE
- `src/lib/routing.ts:95 getQueryString` ← REMOVE
Confidence: HIGH

## MEDIUM PRIORITY

...

## Low Priority / Review Manually

...
```

---

## Target Areas (xuất hiện duplicate nhiều nhất)

```
Utilities                — string trim, case convert, deep clone
Validation               — email/URL/phone format check
Error formatting         — error message builders
Path manipulation        — join, resolve, normalize
String transforms        — slugify, truncate, escape
Date formatting          — humanize, relative time, ISO convert
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu dùng Opus cho Phase 2 (tốn token, không cần)
❌ FAIL nếu skip categorize và analyze toàn bộ cùng lúc (too noisy)
❌ FAIL nếu consolidate function chưa có test coverage
✅ PASS khi: survivor function có tests + callers đã được update + removed functions deleted
```

## Verification trước khi delete

```bash
# Kiểm tra test coverage của survivor
npx jest --coverage --testPathPattern="path/to/survivor" 2>/dev/null | grep -A5 "Coverage"

# Tìm tất cả callers của function sẽ bị remove
grep -rn "extractUrlParams\|getQueryString" src/ --include="*.ts"
```

## See also
- `refactor-patterns` — safe refactoring patterns
- `coding-standards` — code quality gate

