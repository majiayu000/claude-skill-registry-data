---
name: export-menu-page-permission
description: 'Xuất cấu trúc menu & page permission của portal ra file JSON chuẩn. Tự quét source lấy PAGE_FEATURES, báo thiếu và khai báo bổ sung.'
---

# Export Menu & Page Permission

> ⚠️ Skill này **chỉ hướng dẫn cách chạy script** — không tự chạy.
> Toàn bộ nguyên tắc cấu trúc portal, menuCode và PAGE_FEATURES nằm trong file quy tắc:
> `rule-tao-json-menu-phan-quyen/export-cau-truc-phan-quyen.rule.md` (Agent phải đọc trước khi khai báo).

## Cách chạy script

```bash
# Chạy trực tiếp (interactive): chọn portal → Bước 1 kiểm tra cấu trúc → Bước 2 export
node .claude/skills/export-menu-page-permission/scripts/export-menu-page-permission.cjs

# Export 1 portal cụ thể (bỏ qua interactive)
node .claude/skills/export-menu-page-permission/scripts/export-menu-page-permission.cjs --portal invoice

# Export tất cả portal
node .claude/skills/export-menu-page-permission/scripts/export-menu-page-permission.cjs --all

# Sync permission mapping (tự động cập nhật PermissionMapping.{Portal}.ts)
node .claude/skills/export-menu-page-permission/scripts/export-menu-page-permission.cjs --portal invoice --sync-mapping
node .claude/skills/export-menu-page-permission/scripts/export-menu-page-permission.cjs --all --sync-mapping

# Liệt kê danh sách portal
node .claude/skills/export-menu-page-permission/scripts/export-menu-page-permission.cjs --list
```

Output: `.claude/skills/export-menu-page-permission/export-json/{shortName}_export_{ddMMyyyy}.json`

## Luồng khi chạy trực tiếp (interactive)

```
1. Hiển thị danh sách portal (1..N) → người dùng chọn portal
2. BƯỚC 1 — Kiểm tra điều kiện cấu trúc portal (file TopMenu/NavMenu, PAGE_ID + PAGE_FEATURES)
   ├── PASS → chuyển BƯỚC 2
   └── FAIL → DỪNG, báo Agent kiểm tra + khai báo lại đúng cấu trúc
3. BƯỚC 2 — Export JSON vào export-json/
```

## Khi nào Agent phải can thiệp

- Script báo "CHƯA có PAGE_FEATURES" → Agent đọc từng file page `.tsx` còn thiếu → khai báo `PAGE_ID` + `PAGE_FEATURES`.
- Portal còn trang nào chưa khai báo features → Agent phải báo cáo và tự khai báo lại đầy đủ, rồi chạy lại script.
- Sau khi khai báo xong → chạy `check-master-page.cjs` để kiểm tra tính đúng đắn.

## Tham chiếu

- Quy tắc chi tiết: `rule-tao-json-menu-phan-quyen/export-cau-truc-phan-quyen.rule.md`
- Kiểm tra PAGE_FEATURES: `.claude/skills/tao-ui-master-page/check-master-page.cjs`
