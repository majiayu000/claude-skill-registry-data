---
name: lsp-navigation
description: "Use when searching for where a function/class/variable is defined or referenced, before using grep on the codebase. Triggers on: 'where is X defined', 'find all uses of Y', 'what calls Z', 'go to definition', 'find references', searching for a symbol name across files."
---

# LSP Navigation Skill

Khi LSP available, tìm symbol/reference bằng LSP nhanh hơn grep và không đốt context.

## Vấn đề của grep khi tìm symbol

```bash
# Grep tìm function name → hàng nghìn match không liên quan
grep -r "handleAuth" .
# Kết quả: comments, strings, variable names, test mocks, log messages
# → Agent phải đọc từng file → đốt context
```

LSP hiểu ngữ nghĩa: nó biết `handleAuth` ở dòng 42 của `auth.ts` là declaration,
còn ở `login.ts` dòng 87 là call site — và phân biệt được.

## Khi nào dùng LSP vs grep

| Tình huống | Dùng gì |
|-----------|---------|
| Tìm nơi function được định nghĩa | LSP: go-to-definition |
| Tìm tất cả nơi function được gọi | LSP: find-references |
| Tìm text tự do (comment, string, log) | grep |
| Tìm pattern regex trong file | grep |
| Tìm tên file | find |
| Symbol rename — impact analysis | LSP: find-references trước |

## Workflow khi LSP available

### Step 1 — Kiểm tra LSP có available không

```bash
# Claude Code tự động dùng LSP nếu project có language server configured
# Kiểm tra có tsconfig/pyproject/go.mod không
ls tsconfig.json pyproject.toml go.mod Cargo.toml 2>/dev/null
```

Nếu có → LSP likely available. Dùng Claude Code's built-in symbol navigation.

### Step 2 — Tìm definition

Thay vì:
```bash
grep -r "functionName" . --include="*.ts"
```

Dùng Claude Code's go-to-definition trên symbol cụ thể.
Nó trả về: file + line number + context — không có noise.

### Step 3 — Tìm references

Thay vì:
```bash
grep -rn "functionName" . --include="*.ts" | head -50
```

Dùng find-references. Kết quả là danh sách call sites thật,
không phải tất cả chỗ có chuỗi ký tự đó.

### Step 4 — Fallback về grep khi cần

LSP không available hoặc project không có language server:

```bash
# Grep có scope — chỉ tìm trong thư mục liên quan
grep -rn "functionName" src/auth/ --include="*.ts" | head -20

# Không grep toàn repo một phát
# grep -r "functionName" .   ← tránh cái này
```

## Nguyên tắc grep tiết kiệm context

Khi phải dùng grep:

1. **Scope xuống directory nhỏ nhất** có thể chứa kết quả
2. **Dùng `--include`** để chỉ tìm đúng file type
3. **`| head -20`** — không dump vô hạn
4. **Tìm từ cụ thể** hơn: `handleAuthToken` thay vì `auth`
5. **Đọc kết quả trước khi mở file** — nhiều khi grep output đủ để hiểu

## Context budget reminder

Mỗi lần grep dump 500 dòng vào context = ~2000 token bị chiếm.
Với project lớn, 3–4 lần grep rộng = hết context budget cho actual work.

LSP navigation không chiếm context theo kiểu đó —
nó trả về danh sách file:line ngắn gọn, agent đọc file cụ thể khi cần.
