---
name: codehealth-mcp
description: "Code health assessment qua CodeScene MCP — đánh giá structural maintainability, detect regression trước commit/PR. Score 1-10, tích hợp Claude Code."
origin: ECC
user-invocable: true
---

# CodeHealth MCP — Structural Maintainability Assessment

Tích hợp CodeScene vào Claude Code để đánh giá code health trước khi sửa/commit.

## Setup

```bash
# Set access token
export CS_ACCESS_TOKEN=your-codescene-token

# Thêm vào mcp-configs/mcp-servers.json
{
  "codescene": {
    "command": "npx",
    "args": ["@codescene/codehealth-mcp"],
    "env": { "CS_ACCESS_TOKEN": "${CS_ACCESS_TOKEN}" }
  }
}
```

**Không cần credentials trong repo.** Token chỉ qua env var.

## 4 tools có sẵn

| Tool | Dùng khi |
|------|---------|
| `code_health_review` | Trước khi sửa code — xem baseline |
| `code_health_score` | Sau khi sửa — detect regression |
| `pre_commit_code_health_safeguard` | Trước khi commit — block nếu score giảm |
| `analyze_change_set` | Trước khi mở PR — assess toàn branch |

## Score scale (1–10)

| Score | Màu | Ý nghĩa |
|-------|-----|---------|
| 9.0–10.0 | 🟢 Green | Healthy — safe to extend |
| 4.0–8.9 | 🟡 Yellow | Tech debt — tránh refactor lớn |
| 1.0–3.9 | 🔴 Red | Severe debt — giới hạn scope |

## Workflow chuẩn

```
1. code_health_review    # Xem baseline trước khi sửa
2. Sửa code (targeted)
3. code_health_score     # Check sau khi sửa
4. Lặp lại cho đến khi score không giảm
5. pre_commit_code_health_safeguard  # Trước commit
6. analyze_change_set    # Trước khi mở PR
```

**Không mark "done" nếu score regression.**

## Khi MCP không khả dụng

Skip check và tiếp tục — chỉ cần human approval tường minh.

## Source

`@codescene/codehealth-mcp` · https://codescene.com
