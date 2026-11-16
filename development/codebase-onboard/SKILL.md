---
name: codebase-onboard
description: "Use when asked to understand, tour, or onboard to a codebase. Triggers on: 'onboard', 'explain codebase', 'walk me through the code', 'new to this project', 'codebase overview', 'how is this structured', 'give me a tour', 'tổng quan codebase', 'giải thích project', 'entry point', 'where to start reading'."
---

# Codebase Onboard Skill
# Source: Lum1104/Understand-Anything (MIT) — 6-agent pipeline pattern adapted for YAMTAM
# Tier: TIER 3 — PRODUCTIVITY

Tạo guided tour của codebase bằng pipeline 4 bước tuần tự.
Không đọc tất cả file — đọc đúng file, đúng thứ tự, đủ để hiểu.

## Pipeline (sequential — mỗi bước dùng output của bước trước)

```
Step 1: project-scanner      → structure map + entry points
Step 2: architecture-analyzer → patterns + key abstractions + data flow
Step 3: dependency-mapper    → internal call graph + external deps
Step 4: tour-builder         → guided narrative + reading order
```

## Khi nào dùng

- Người mới vào project lần đầu
- Claude Code session mới trên repo chưa quen
- "What is this codebase / where do I start?"
- Onboard agent mới vào YAMTAM workflow

**Do NOT use for:** debugging cụ thể, code review, refactor. Dùng `/debug` hoặc `/code-review`.

---

## Step 1 — Project Scanner

**Mục tiêu:** Map cấu trúc thư mục + tìm entry points thực sự (không đoán).

```bash
# 1a. Structure overview (top-level + 1 level deep)
find . -maxdepth 2 -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -not -path '*/.claude/*' | sort | head -80

# 1b. Entry point candidates
# Node.js / TS
grep -r '"main"\|"scripts"' package.json 2>/dev/null | head -10

# Python
find . -name "main.py" -o -name "__main__.py" -o -name "app.py" 2>/dev/null | head -5

# Generic
find . -maxdepth 2 -name "*.sh" -perm /111 2>/dev/null | head -10

# 1c. Config files (tìm constraints quan trọng)
ls -la .env* tsconfig* pyproject* Makefile Dockerfile* 2>/dev/null

# 1d. File count by type
find . -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.sh" \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10
```

**Output:** danh sách entry points + file type breakdown.

---

## Step 2 — Architecture Analyzer

**Mục tiêu:** Tìm pattern kiến trúc thực tế (không assume MVC hay microservice).

```bash
# 2a. Tìm top-level modules (theo số file hoặc import count)
find . -maxdepth 3 -name "*.ts" -o -name "*.py" 2>/dev/null \
  | grep -v node_modules | grep -v .git \
  | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -15

# 2b. Import graph (Python)
grep -rh "^import\|^from" --include="*.py" . 2>/dev/null \
  | grep -v "node_modules\|.git" | sort | uniq -c | sort -rn | head -20

# 2c. Import graph (TypeScript)
grep -rh "^import" --include="*.ts" . 2>/dev/null \
  | grep -v "node_modules\|.git" | sort | uniq -c | sort -rn | head -20

# 2d. Đọc 5 file quan trọng nhất (entry + largest + most-imported)
# Đọc từng file, tóm tắt responsibility trong 2 câu
```

**Output:** kiến trúc tổng thể + key abstractions (class, module, layer chính).

---

## Step 3 — Dependency Mapper

**Mục tiêu:** Internal call graph + external deps quan trọng.

```bash
# 3a. External dependencies
cat package.json 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
deps = list(d.get('dependencies', {}).keys())
dev  = list(d.get('devDependencies', {}).keys())
print('PROD:', deps[:15])
print('DEV:', dev[:10])
" 2>/dev/null

# Python
cat requirements.txt 2>/dev/null | grep -v "^#" | head -20

# 3b. Internal module coupling (files with most imports OF them)
grep -rh "from \.\|require(" --include="*.ts" --include="*.py" --include="*.js" \
  . 2>/dev/null | grep -v node_modules \
  | grep -oE "['\"]\.\/[^'\"]+['\"]|from [a-z_]+\.[a-z_]+" \
  | sort | uniq -c | sort -rn | head -15

# 3c. API surface (exported symbols)
grep -rh "^export " --include="*.ts" . 2>/dev/null | grep -v node_modules \
  | grep -oE "export (default |const |function |class |type )[A-Z][a-zA-Z]+" \
  | sort | uniq | head -20
```

**Output:** dependency graph text + top coupled modules.

---

## Step 4 — Tour Builder

**Mục tiêu:** Tạo guided tour từ kết quả 3 bước trên. Format cố định.

### Output format bắt buộc

```markdown
## Codebase Tour: [Project Name]

### 1. Mục đích (1 đoạn)
[Project làm gì, cho ai, vấn đề gì nó giải quyết]

### 2. Kiến trúc tổng quan
[Text diagram — dùng → và | không dùng box art phức tạp]

Ví dụ:
  CLI entry → Command parser → Core engine → Output formatter
                                    ↓
                             Plugin system → [plugin-a] [plugin-b]

### 3. Entry points — đọc theo thứ tự này

| Thứ tự | File | Tại sao đọc trước |
|--------|------|------------------|
| 1 | `src/main.ts` | Bootstrap — wires everything together |
| 2 | `src/core/engine.ts` | Core logic — understand this = understand 60% |
| 3 | `core/rules/00-meta-rule-enforcer.md` | Configuration layer |
| 4 | `core/hooks/guard-destructive.sh` | Extension pattern example |
| 5 | `tests/integration/basic.test.ts` | Expected behaviors |

### 4. Common workflows (với file paths)

**Workflow 1: [tên]**
```
User action → file:line → file:line → output
```

**Workflow 2: [tên]**
```
Trigger → file:line → file:line → side effect
```

**Workflow 3: [tên]**
```
Event → file:line → file:line → result
```

### 5. Gotchas & non-obvious constraints

- **[Pattern tên]:** [Giải thích tại sao không obvious]
- **[Convention tên]:** [Ví dụ cụ thể]
- **[Footgun tên]:** [Cách tránh]
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu output chỉ có structure cây thư mục — không phải tour
❌ FAIL nếu "entry points" là guess (main.ts mà không verify file tồn tại)
❌ FAIL nếu workflow không có file paths cụ thể
❌ FAIL nếu architecture diagram là boilerplate (không reflect codebase thực)
❌ FAIL nếu 5 file đọc đầu tiên không được justify cụ thể
✅ PASS khi: architecture diagram + 5 files + 3 workflows + 3 gotchas đều có evidence
```

## See also
- `codegraph` MCP: symbol-level navigation sau khi có tour tổng thể
- `ingest-repo`: deep semantic indexing nếu codebase phức tạp
- `session-context`: save tour vào L1 để dùng lại
