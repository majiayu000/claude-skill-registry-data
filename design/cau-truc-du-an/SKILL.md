---
name: cau-truc-du-an
description: 'Cấu trúc thư mục dự án JDX-Gamers Website — module duy nhất JGameApp, phân vùng Public/Account, cấu trúc feature, layer services/hooks/pages. Dùng khi: tạo feature mới, tổ chức file, xác định đặt file vào đâu trong src/modules/JGameApp.'
---

# Cấu Trúc Dự Án JDX-Gamers Website

> **Cập nhật:** 2026-09-01 — Phản ánh đúng trạng thái hiện tại: chỉ 1 module `JGameApp`.

## Cấu Trúc Gốc

```
src/
├── modules/
│   └── JGameApp/     # Module DUY NHẤT — website game/store JDX-Gamers
├── shared/            # Thư viện dùng chung root (rất tối giản: lib/utils, components/ui, .gitkeep services/utils)
├── styles/            # CSS toàn cục
├── App.tsx             # Root component + HashRouter, lazy-load JGamePortal tại /jgame/*
└── main.tsx            # Entry point
```

> ⚠️ **QUAN TRỌNG:** `src/modules/` chỉ có 1 module là `JGameApp`, 1 repo duy nhất. KHÔNG có kiến trúc đa-portal/đa-repo (những tài liệu cũ nhắc tới InvoiceApp/AdminApp/KetoanApp/... là từ dự án khác — không áp dụng ở đây, xem `Website/.claude/skills/_archived-sasuco/`).

## Cấu Trúc Chi Tiết JGameApp

Chi tiết đầy đủ (layout, contexts, mocks, phân vùng Public vs Account) xem tại
`Website/.claude/system-architect/00-tong-quan-kien-truc.md` — đây là nguồn xác thực chính, luôn đọc file đó trước khi quyết định đặt file mới ở đâu. Tóm tắt:

```
JGameApp/
├── contexts/          # AuthContext (độc lập, không qua SSO), CartContext
├── layout/            # JGamePortal (shell gốc), StorefrontLayout/Header/Footer, Require* guards
├── mocks/             # toàn bộ dữ liệu giả — chưa có backend thật
├── routes/routeConfig.tsx   # TOÀN BỘ route khai báo trong 1 file duy nhất
├── shared/            # services/api, components/ui, hooks, utils riêng của JGameApp
└── features/
    ├── Public/         # xem được KHÔNG cần đăng nhập (home, catalog, auth, static-pages, playtime, accessories, tasks)
    └── Account/
        ├── User/       # hành trình giao dịch/quản lý tài khoản khách hàng
        ├── Admin/      # quản trị JGame (role=admin)
        ├── ShopOwner/  # Kênh Người Bán
        └── Partner/    # Đối tác tiếp thị liên kết
```

## Cấu Trúc Feature (trong `features/Public/{ten}` hoặc `features/Account/{Nhom}/{ten}`)

```
{ten-tinh-nang}/
├── types/           # TypeScript interfaces, enums
├── services/        # Gọi API / mock (qua shared/services/api)
├── hooks/           # Business logic (React hooks) — hậu tố .page.*.ts hoặc .dlg.form.ts theo vai trò
├── components/      # UI component con (không có logic)
├── pages/           # Trang route (không có logic)
└── index.ts         # Barrel export (khi cần)
```

4 domain `playtime`, `accessories`, `order`, `tasks` có trang ở cả `Public` (duyệt/xem trước) lẫn `Account/User` (xác nhận/thanh toán) — được phép import chéo `types`/`services` cùng domain giữa 2 vùng, không nhân bản logic. Xem chi tiết nguyên tắc phân vùng trong `system-architect/00-tong-quan-kien-truc.md`.

---

## Kiến Trúc Phân Tầng (khuyến nghị)

```
Pages / Components  ← Chỉ render UI
        ↓ chỉ gọi hooks
      Hooks          ← Business logic + state
        ↓ chỉ gọi services
    API/Mock Services ← Gọi backend (hiện là lớp mock, xem mock-gate-va-api.md)
        ↓ dùng shared utilities
  apiCall() / buildJGameUrl() / các helper trong shared/services/api
```

**Nghiêm cấm:**
- ❌ Gọi API/mock trực tiếp trong Pages / Components
- ❌ Viết business logic trong Pages / Components
- ❌ Hardcode URL API

---

## Shared — BẮT BUỘC Dùng Trước Khi Tạo Mới

Ưu tiên dùng `src/modules/JGameApp/shared/` (services/api, components/ui, hooks, utils) trước — đây là shared thực sự dùng cho module JGameApp. `src/shared/` ở root hiện rất tối giản (chỉ `lib/utils.ts` và vài component `ui/` cơ bản: button, card, badge) — không có `services/api` hay `utils` thực thi (chỉ `.gitkeep`), không import nhầm từ đó mong đợi các hàm nghiệp vụ.

---

## Tài liệu liên quan

- `Website/.claude/system-architect/00-tong-quan-kien-truc.md` — kiến trúc chi tiết, nguồn xác thực chính.
- `Website/.claude/business-rules/` — nghiệp vụ chi tiết từng phân hệ.
- `Website/.claude/skills/_archived-sasuco/` — tài liệu/skill từ dự án cũ (SASUCO InvoiceEasy, kiến trúc 9-portal đa-repo), không áp dụng cho JDX-Gamers, giữ lại chỉ để tham khảo lịch sử.
