---
name: tao-layout-navmenu-topmenu
description: 'Quy tắc tạo NavMenu và TopMenu cho từng portal trong SASUCO InvoiceEasy, đảm bảo auto-discovery sơ đồ dự án hoạt động đúng. Dùng khi: tạo mới NavMenu/TopMenu cho portal, thêm menu item mới, thêm portal mới, cấu hình PAGE_TO_TOP_MENU, export NAV_MENU_ITEMS/NAV_EXTERNAL_ITEMS/TOP_MENU_ITEMS/PORTAL_META. BẮT BUỘC đọc khi muốn sơ đồ dự án tự động nhận diện trang/chức năng.'
---

# Quy Tắc NavMenu & TopMenu — SASUCO InvoiceEasy

> **Mục đích kép:** NavMenu/TopMenu vừa render UI điều hướng, vừa là **nguồn sự thật duy nhất** cho sơ đồ dự án auto-discover.
> Nếu export sai hoặc thiếu → sơ đồ dự án không nhận ra portal/trang đó.

---

## Kiến Trúc Tổng Quan

```
Mỗi Portal có:
  layout/
    TopMenu{Portal}.tsx   → Khai báo top-menu groups + PORTAL_META
    NavMenu{Portal}.tsx   → Khai báo nav items theo từng top-menu group
```

### Mối Quan Hệ Auto-Discovery

```
TopMenu exports:
  TOP_MENU_ITEMS     → danh sách tab top-level (id + label)
  PORTAL_META        → metadata portal (label, color, order)
  PAGE_TO_TOP_MENU   → (tùy chọn) map pageId → topMenuCode (khi không dùng path convention)

NavMenu exports:
  NAV_MENU_ITEMS     → Record<topMenuCode, pageId[]>
  NAV_EXTERNAL_ITEMS → (tùy chọn) pageId có path ngoài HashRouter

Page exports:
  PAGE_ID            → (tùy chọn) override id khi tên file không tự derive đúng
  PAGE_FEATURES      → (tùy chọn) danh sách tính năng với label tiếng Việt chính xác
```

---

## TopMenu — Interface Bắt Buộc

### Exports cần có trong mọi TopMenu

```typescript
/** Danh sách tab top-menu — auto-derive từ config, không sửa thủ công.
 * Cấu trúc bắt buộc: mảng { id, label } */
export const TOP_MENU_ITEMS: Array<{ id: string; label: string }> =
  MENU_CONFIG.map(({ id, label }) => ({ id, label }))

/** Metadata portal cho sơ đồ dự án auto-discover.
 * label: tên hiển thị | color: màu badge | order: thứ tự sắp xếp */
export const PORTAL_META = {
  label: 'Tên Portal',
  color: 'blue' as const,   // 'blue' | 'purple' | 'slate' | 'orange' | 'green'
  order: 2,                  // thứ tự portal trong sơ đồ dự án (1=Admin, 2=Invoice...)
}
```

### PAGE_TO_TOP_MENU — Khi nào cần?

> Chỉ cần khi portal **KHÔNG** dùng path URL convention để phân biệt top-menu.
> Portal có path dạng `/admin/system/xxx` → **không cần** vì sơ đồ dự án tự parse path.
> Portal có path dạng `/kiem-thu` (không có segment top-menu) → **bắt buộc** export.

```typescript
/** Mapping pageId → topMenuCode — dùng khi path không encode topMenuCode.
 * Khi thêm trang mới: chỉ cần bổ sung ở đây, sơ đồ dự án tự cập nhật. */
export const PAGE_TO_TOP_MENU: Record<string, string> = {
  dashboard:          'dashboard',
  'ten-trang-1':      'nhom-a',
  'ten-trang-2':      'nhom-a',
  'ten-trang-3':      'nhom-b',
}
```

### Pattern chuẩn TopMenu

```typescript
// ─── Cấu hình source of truth ──────────────────────────────────────────────
/** Khai báo ở đây → TOP_MENU_ITEMS tự derive, KHÔNG sửa thủ công 2 nơi */
const MENU_CONFIG = [
  { id: 'dashboard',    label: 'Dashboard',    icon: LayoutDashboard },
  { id: 'quan-ly',      label: 'Quản lý',      icon: Users },
  { id: 'bao-cao',      label: 'Báo cáo',      icon: BarChart3 },
  { id: 'cai-dat',      label: 'Cài đặt',      icon: Settings },
]

// ─── Exports cho sơ đồ dự án ───────────────────────────────────────────────
/** Auto-derive — không sửa thủ công */
export const TOP_MENU_ITEMS: Array<{ id: string; label: string }> =
  MENU_CONFIG.map(({ id, label }) => ({ id, label }))

export const PORTAL_META = {
  label: 'Tên Portal Hiển Thị',
  color: 'blue' as const,
  order: 2,
}
// ───────────────────────────────────────────────────────────────────────────

interface TopMenuXyzProps {
  activeMainMenu: string
  onMainMenuChange: (menu: string) => void
  mobileNavOpen?: boolean
  onMobileNavToggle?: () => void
}

export function TopMenuXyz({ activeMainMenu, onMainMenuChange, ... }: TopMenuXyzProps) {
  // ... render UI dùng MENU_CONFIG, activeMainMenu, onMainMenuChange
}
```

---

## NavMenu — Interface Bắt Buộc

### Exports cần có trong mọi NavMenu

```typescript
/** Map topMenuCode → danh sách pageId trong nhóm đó.
 * Auto-derive từ menuItems config — không sửa thủ công */
export const NAV_MENU_ITEMS: Record<string, string[]> = Object.fromEntries(
  Object.entries(menuItems).map(([k, v]) => [k, v.map(i => i.id)])
)
```

### NAV_EXTERNAL_ITEMS — Khi nào cần?

> Chỉ cần khi portal có menu item điều hướng **ra ngoài HashRouter** (sang portal khác, trang ngoài).
> Ví dụ: KetoanHKD có menu item mở trang BaseIndex (portal khác) → cần export `NAV_EXTERNAL_ITEMS`.

```typescript
/** Map pageId → { topMenuCode, path } cho các item điều hướng ngoài HashRouter.
 * Dùng khi menu item có prop `externalPath` thay vì `id` thông thường.
 * Sơ đồ dự án dùng để phát hiện cross-portal links. */
export const NAV_EXTERNAL_ITEMS: Record<string, { topMenuCode: string; path: string }> = (() => {
  const result: Record<string, { topMenuCode: string; path: string }> = {}
  Object.entries(NAV_ITEMS_BY_TOP_MENU).forEach(([topMenuCode, items]) => {
    items.forEach(item => {
      if (item.externalPath) result[item.id] = { topMenuCode, path: item.externalPath }
    })
  })
  return result
})()
```

### Pattern chuẩn NavMenu

```typescript
// ─── Cấu hình source of truth ──────────────────────────────────────────────
/** Khai báo ở đây → NAV_MENU_ITEMS tự derive.
 * Mỗi object trong mảng: { id, label, icon, disabled?, children? }
 * id phải khớp với pageId được dùng trong Router và Page file.
 */
const menuItems: Record<string, NavMenuItemXyz[]> = {
  dashboard: [
    { id: 'tong-quan',   label: 'Tổng quan',   icon: <LayoutDashboard className='h-4 w-4' /> },
  ],
  'quan-ly': [
    { id: 'khach-hang',  label: 'Khách hàng',  icon: <Users className='h-4 w-4' /> },
    { id: 'san-pham',    label: 'Sản phẩm',    icon: <Package className='h-4 w-4' /> },
  ],
  'bao-cao': [
    { id: 'doanh-thu',   label: 'Doanh thu',   icon: <BarChart3 className='h-4 w-4' /> },
  ],
}

// ─── Exports cho sơ đồ dự án ───────────────────────────────────────────────
/** Auto-derive — không sửa thủ công */
export const NAV_MENU_ITEMS: Record<string, string[]> = Object.fromEntries(
  Object.entries(menuItems).map(([k, v]) => [k, v.map(i => i.id)])
)
// ───────────────────────────────────────────────────────────────────────────

interface NavMenuXyzProps {
  activeMainMenu: string
  activePage: string
  onPageChange: (page: string) => void
  mobileNavOpen?: boolean
  onMobileNavClose?: () => void
}

export function NavMenuXyz({ activeMainMenu, activePage, onPageChange, ... }: NavMenuXyzProps) {
  // ... render UI dùng menuItems[activeMainMenu]
}
```

---

## Quy Tắc id — BẮT BUỘC Nhất Quán

> `id` trong NavMenu phải khớp hoàn toàn với `PAGE_ID` của page tương ứng.
> Nếu id không khớp → sơ đồ dự án **không** map được tính năng của trang đó.

### Format id

```
✅ ĐÚNG: kebab-case thuần
  'ban-hang'          → BanHangPage.tsx
  'khach-hang'        → KhachHangPage.tsx
  'invoice-management'→ InvoiceManagementPage.tsx
  'giam-sat-dong-bo-cqt' → GiamSatDongBoCqtPage.tsx

❌ SAI:
  'banHang'           → camelCase không được
  'ban_hang'          → underscore không được
  'BanHang'           → PascalCase không được
```

### Đảm bảo nhất quán 3 chiều

```
NavMenu id          =  Route path segment    =  Page PAGE_ID / tên file
'ban-hang'          =  /ban-hang             =  BanHangPage.tsx / PAGE_ID='ban-hang'
'invoice-management'=  /invoice-management   =  InvoiceManagementPage.tsx
```

---

## Thứ Tự Portal (PORTAL_META.order)

| Portal | color | order |
|--------|-------|-------|
| Admin | `'purple'` | `1` |
| Invoice (Business) | `'blue'` | `2` |
| Partner | `'slate'` | `3` |
| KiemThu | `'green'` | `4` |
| KetoanHKD | `'orange'` | `5` |
| BaseIndex | `'gray'` | `6` |

> Khi thêm portal mới: chọn `order` tiếp theo chưa có, chọn `color` chưa dùng.

---

## Khi Thêm Trang Mới vào Portal Hiện Tại

**Chỉ cần 2 bước:**

**Bước 1 — Thêm vào `menuItems` trong NavMenu:**
```typescript
// NavMenuXyz.tsx — thêm vào đúng nhóm top-menu
'quan-ly': [
  { id: 'khach-hang', label: 'Khách hàng', icon: <Users className='h-4 w-4' /> },
  { id: 'ten-trang-moi', label: 'Tên trang mới', icon: <IconMoi className='h-4 w-4' /> }, // ← thêm
],
```

**Bước 2 — Tạo file Page với đúng tên file (hoặc export PAGE_ID):**
```typescript
// TenTrangMoiPage.tsx — tên file auto-derive → 'ten-trang-moi'
// Nếu cần: export const PAGE_ID = 'ten-trang-moi'
export function TenTrangMoiPage() { ... }
```

> `NAV_MENU_ITEMS` tự động cập nhật (vì derive từ `menuItems`).
> Sơ đồ dự án tự nhận diện không cần thêm cấu hình nào khác.

---

## Khi Thêm Portal Hoàn Toàn Mới

1. Tạo `src/modules/{portalName}/layout/TopMenu{Portal}.tsx` — export `TOP_MENU_ITEMS`, `PORTAL_META`
2. Tạo `src/modules/{portalName}/layout/NavMenu{Portal}.tsx` — export `NAV_MENU_ITEMS`
3. Đặt route cho portal vào `App.tsx`
4. Sơ đồ dự án tự detect qua `import.meta.glob('**/layout/TopMenu*.tsx')` + `**/layout/NavMenu*.tsx`

> Không cần đăng ký thủ công vào file cấu hình nào của sơ đồ dự án.

---

## Checklist NavMenu/TopMenu

### TopMenu
- [ ] Export `TOP_MENU_ITEMS` (auto-derive từ config, không hardcode)
- [ ] Export `PORTAL_META` với `label`, `color`, `order` đúng
- [ ] Export `PAGE_TO_TOP_MENU` nếu portal không dùng path URL convention
- [ ] `order` trong `PORTAL_META` là duy nhất, không trùng với portal khác
- [ ] Không sửa `TOP_MENU_ITEMS` thủ công — chỉ sửa config source

### NavMenu
- [ ] Export `NAV_MENU_ITEMS` (auto-derive từ `menuItems`, không hardcode)
- [ ] Export `NAV_EXTERNAL_ITEMS` nếu có menu item điều hướng sang portal khác
- [ ] `id` trong `menuItems` dùng `kebab-case` thuần
- [ ] `id` khớp với tên file page (hoặc `PAGE_ID` export của page đó)
- [ ] Khi thêm menu item mới: chỉ sửa `menuItems`, không sửa `NAV_MENU_ITEMS` thủ công

### Nhất quán 3 chiều
- [ ] NavMenu `id` = Route path segment = Page `PAGE_ID`/tên file
- [ ] Kiểm tra không có pageId nào trong NavMenu mà không có file page tương ứng
- [ ] Kiểm tra không có pageId nào trong NavMenu mà thiếu `data-qa` action buttons

---

## Lỗi Phổ Biến & Cách Fix

| Lỗi | Nguyên nhân | Fix |
|-----|------------|-----|
| Sơ đồ dự án không hiện portal | `PORTAL_META` chưa export | Thêm `export const PORTAL_META = {...}` vào TopMenu |
| Sơ đồ dự án không hiện trang | `NAV_MENU_ITEMS` chưa export hoặc sai format | Kiểm tra `Object.fromEntries(Object.entries(menuItems).map(...))` |
| Trang hiện nhưng không có tính năng | Page thiếu `data-qa` trên các button | Thêm `data-qa='btn_...'` / `data-qa='row_...'` |
| Tính năng bị map sai trang | `id` trong NavMenu ≠ `PAGE_ID` của page | Đồng bộ id giữa NavMenu và page |
| Portal hiện nhưng thiếu trang | Trang chưa có trong `menuItems` NavMenu | Thêm item vào `menuItems` đúng nhóm top-menu |
| Cross-portal link không phát hiện | Thiếu `NAV_EXTERNAL_ITEMS` | Thêm export `NAV_EXTERNAL_ITEMS` từ `externalPath` items |
