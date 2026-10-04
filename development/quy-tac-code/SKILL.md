---
name: quy-tac-code
description: 'Quy tắc code TypeScript và React cho dự án JDX-Gamers Website (JGameApp). Dùng khi: viết TypeScript (tránh any, strict typing), tổ chức React hooks, useEffect dependencies, performance memo/callback, import order, barrel exports, comments tiếng Việt, tránh console.log, không refactor ngoài phạm vi yêu cầu, an toàn khi sửa file.'
---

# Quy Tắc Code — JDX-Gamers Website

## TypeScript

| Quy tắc | Chi tiết |
|---------|---------|
| ❌ Cấm `any` | Dùng `unknown` rồi narrow type |
| ❌ Hạn chế `as X` | Chỉ khi chắc chắn kiểu |
| ✅ Explicit return type | Cho functions public/exported |
| ✅ `interface` cho object shapes | `type` cho union/alias |
| ✅ `enum / as const` | Cho tập giá trị cố định |
| ✅ Optional chaining `?.` | Thay vì kiểm tra thủ công |
| ✅ Nullish coalescing `??` | Thay `||\` khi có falsy 0/"" |

**Types tổ chức:** Mỗi domain entity có interface riêng trong `/types/`. Tách UI types (FormData) ≠ API types (Request/Response).

---

## React & Hooks

- **Pages / Components / Dialogs:** Chỉ render UI — **không** chứa business logic
- **Hooks:** Chứa toàn bộ state management và business logic  
- File `.tsx` > 500 dòng → tách thành sub-components
- Không gọi API trực tiếp từ component — phải qua hook
- Custom hook phải có tiền tố `use`
- Mỗi hook có một trách nhiệm rõ ràng
- Các file giao diện `.tsx` không viết trực tiếp code logic, chỉ chứa JSX và gọi hook để lấy data/logic

**useEffect:**
- Luôn khai báo đầy đủ dependencies
- Luôn có cleanup khi subscribe/timer/listener
- Không dùng `useEffect` để sync state — dùng `useMemo`

**Performance:**
- `React.memo()` khi component render nhiều với props ít thay đổi
- `useMemo/useCallback` chỉ khi đo được lợi ích
- Debounce search input ≥ 300ms (chuẩn dự án: 800ms)

---

## Import Order (BẮT BUỘC)

```typescript
// 1. React & third-party libraries
// 2. Shared utilities/components  (@/shared/...)
// 3. Feature types                (../types)
// 4. Feature services             (../services)
// 5. Feature hooks                (../hooks)
// 6. Feature components           (../components)
```

---

## Barrel Exports

- Mỗi folder (`types/`, `hooks/`, `services/`, `components/`) **phải có** `index.ts`
- Import từ folder: `from '../types'` — không import từ file cụ thể bên trong

---

## Comments & Logging

- **Tất cả comments phải bằng tiếng Việt**
- JSDoc bắt buộc cho functions public trong services, hooks, shared utils
- ❌ **TUYỆT ĐỐI KHÔNG** dùng `console.log` / `console.error`
- ✅ Dùng `ApiLogger` (`info`, `warn`, `error`, `debug`)

```typescript
// ✅ Đúng
ApiLogger.info('Bắt đầu tải danh sách hóa đơn')
ApiLogger.error('Lỗi hệ thống:', error)

// ❌ Sai
console.log(...)
```

---

## An Toàn Khi Sửa Code

- Code đang hoạt động ổn định → **KHÔNG sửa** trừ khi có yêu cầu
- Chỉ sửa trong phạm vi chức năng được yêu cầu
- **KHÔNG tự ý refactor** khi không có task rõ ràng
- **File mới:** `create_file` | **File đã tồn tại:** `replace_string_in_file`
- Không thêm thư viện mới khi chưa được đồng ý

### ⛔ KHÔNG Tự Ý Sửa File Khác Khi Được Yêu Cầu Sửa File Cụ Thể

- Khi user yêu cầu sửa **file A**, chỉ sửa **đúng file A** — không lan sang file B, C dù có liên quan
- Nếu phát hiện file khác cũng cần sửa → **DỪNG LẠI**, báo cáo và chờ user xác nhận trước khi sửa
- **Không tự ý "fix" hay "cải thiện"** những file không nằm trong yêu cầu

### ⛔ Tôn Trọng Yêu Cầu Trước Đó — Không Tự Ý Sửa Lại

- Khi user đã yêu cầu sửa một field/theo một cách cụ thể (VD: "chỉ hiển thị tài khoản X, không gọi API tài khoản"), **giữ nguyên cách đó** — không tự ý sửa lại thành cách mặc định (VD: gọi API tài khoản)
- **Nguyên tắc:** Yêu cầu sau ghi đè quy tắc mặc định. Không "sửa lại cho đúng chuẩn" nếu user đã yêu cầu khác đi
- Ví dụ: Số tài khoản — mặc định gọi API `TaiKhoanApiService` để hiển thị. Nhưng nếu user đã yêu cầu "chỉ hiển thị tài khoản ngân hàng" hoặc "không gọi API", thì **giữ nguyên**, không tự ý sửa thành gọi API

---

## Error Handling

| Loại lỗi | Hiển thị | Log |
|---------|---------|-----|
| Client validation | Inline + Toast tổng hợp | Không |
| Server (4xx) | `ValidationErrorDialog` | Không |
| System (≥ 500) | Toast lỗi chung | `ApiLogger.error()` |
| Unexpected catch | Toast lỗi chung | `ApiLogger.error()` |

---

## Route URL Convention (JGameApp)

- Toàn bộ route khai báo trong **1 file duy nhất** `src/modules/JGameApp/routes/routeConfig.tsx` (mảng `routeConfig`,
  không rải rác nhiều nơi) — path không có prefix `/jgame` (được mount tại `/jgame/*` ở `App.tsx` root).
- Mỗi route là 1 object `{ path, element, pageId, requireAuth?, guestOnly?, requireShopOwner?, requireAffiliate?, requireAdmin? }`,
  `element` luôn là component đã `lazy()` khai báo ở đầu file.
- **Điều hướng:** dùng `<Link to="/jgame/...">` hoặc `useNavigate()` của `react-router-dom` — không có hook điều hướng riêng theo pageId như dự án cũ.
- Thêm route mới: khai báo `lazy()` import ở đầu file + thêm 1 object vào mảng `routeConfig`, đặt đúng nhóm comment
  (Storefront/Account/Admin/...) đã có trong file.

---

## Checklist Nhanh

- [ ] Không `any` trong code mới
- [ ] Không `console.log` / `console.error`
- [ ] Không business logic trong `.tsx`
- [ ] Không API call trực tiếp từ component
- [ ] Đã dùng lại từ `/shared/` nếu có
- [ ] Comments bằng tiếng Việt
- [ ] `index.ts` được cập nhật khi thêm file mới
- [ ] Không refactor ngoài phạm vi yêu cầu
- [ ] Route mới đã khai báo `lazy()` + thêm object vào `routeConfig` trong `routes/routeConfig.tsx`

---


