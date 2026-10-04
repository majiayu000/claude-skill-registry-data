---
name: cach-refactor-kien-truc-doc-lap
description: 'Quy trình refactor portal thành độc lập: phân tích dependencies vào src/shared, copy chính xác các file cần thiết vào portal/shared + portal/styles, cập nhật imports @/shared thành relative. Dùng khi: muốn tách 1 portal thành repo độc lập, tách KiemThuApp/KetoanApp/BaseIndexApp thành module tự chủ. CHỈ COPY FILE LIÊN QUAN, cấm copy toàn bộ.'
---

# Cách Refactor Portal Thành Kiến Trúc Độc Lập

> **Mục tiêu:** Biến 1 portal (vd: KiemThuApp) từ phụ thuộc vào `src/shared` và `src/styles` thành module tự chủ với bản sao shared code riêng.

## Scripts Tự Động (3 scripts trong `scripts/`)

Tất cả scripts chạy từ **project root**. `<PortalPath>` = đường dẫn tương đối, VD: `src/modules/KiemThuApp`.

| # | Script | Mục đích |
|---|--------|----------|
| B1 | `scripts/analyze-deps.cjs <PortalPath>` | Phân tích tự động tất cả dependencies |
| B2 | `scripts/copy-shared.cjs <PortalPath>` | Copy chính xác file vào portal |
| B3 | `scripts/update-imports.cjs <PortalPath>` | Cập nhật `@/shared/` → relative |

### Workflow nhanh

```bash
SKILL=.claude/skills/cach-refactor-kien-truc-doc-lap/scripts
PORTAL=src/modules/{PortalName}

# B1: Phân tích
node $SKILL/analyze-deps.cjs $PORTAL

# B2: EDIT copy-shared.cjs dựa trên output B1, sau đó chạy
node $SKILL/copy-shared.cjs $PORTAL

# B3: Cập nhật imports
node $SKILL/update-imports.cjs $PORTAL
```

---

## Tổng Quan Quy Trình (4 bước)

```
B1: Phân tích dependencies → B2: Copy file chính xác → B3: Cập nhật imports → B4: Verify + Commit
```

---

## Bước 1: Phân Tích Dependencies

### 1.1 Chạy script `analyze-deps.cjs`

```bash
node .claude/skills/cach-refactor-kien-truc-doc-lap/scripts/analyze-deps.cjs src/modules/{PortalName}
```

Script tự động:
- Quét toàn bộ file `.ts/.tsx` trong portal (trừ `docs/`)
- Tìm tất cả `import ... from '@/shared/...'`
- Trace đệ quy internal dependencies (barrel `export *`, relative imports)
- In ra danh sách đầy đủ file cần copy + danh sách FLAT

### 1.2 Phân loại imports theo nhóm

| Nhóm | Pattern | Cách copy |
|------|---------|-----------|
| **services/api** | `@/shared/services/api` | Copy TOÀN BỘ thư mục `api/` (tightly coupled, các file import lẫn nhau) |
| **services khác** | `@/shared/services/Xxx` | Chỉ copy file cụ thể |
| **utils** | `@/shared/utils` (barrel) | Chỉ copy file được import cụ thể (vd: FormatUtils, PagingUtils, ValidationUtils...) |
| **hooks** | `@/shared/hooks/useXxx` | Chỉ copy file cụ thể |
| **components/ui** | `@/shared/components/ui/xxx` | Copy từng component + utils.ts (cn) |
| **components/common** | `@/shared/components/common` (barrel) | Chỉ copy component được import cụ thể |
| **contexts** | `@/shared/contexts/Xxx` | Chỉ copy file cụ thể |
| **constants** | `@/shared/constants/xxx` | Chỉ copy file cụ thể |
| **types** | `@/shared/types/xxx` | Chỉ copy file cụ thể |
| **features** | `@/shared/features/xxx` | Copy toàn bộ feature (thường nhỏ) |
| **styles** | `@/styles/xxx` | Chỉ copy file CSS cụ thể |

### 1.3 Nguyên tắc trace

Script `analyze-deps.cjs` tự động trace đệ quy:
1. File trong `services/api/` tự tham chiếu lẫn nhau → tự động phát hiện hết
2. File `components/common/` import từ `components/ui/` → tự động thêm
3. File `contexts/` import từ `services/` hoặc `types/` → tự động trace tiếp

**Kết quả:** Dùng danh sách FLAT ở cuối output làm input cho bước copy.

---

## Bước 2: Copy File Chính Xác

### Quy tắc vàng
- ✅ **CHỈ copy file được import** — không copy toàn bộ thư mục trừ `api/` và features nhỏ
- ✅ **LUÔN tạo barrel `index.ts`** cho `components/common/` và `utils/` — các file khác import từ barrel này
- ✅ **Copy cả file dependencies** — nếu file A import file B, copy cả B
- ❌ **Cấm copy toàn bộ** `src/shared/` — sinh rác, khó maintain

### Cấu trúc thư mục đích

```
src/modules/{PortalName}/
  shared/          ← Tạo mới, chứa bản sao của src/shared (chỉ file cần thiết)
    services/
      api/         ← TOÀN BỘ (tightly coupled)
      PermissionService.ts
      permissionMappings/
    utils/
      FormatUtils.ts
      PagingUtils.tsx
      ...
    hooks/
      useDebounce.ts
    components/
      ui/
        utils.ts   ← cn() helper
        button.tsx
        ...
      common/
        ConfirmDialog.tsx
        ...
    contexts/
      PermissionContext.tsx
      PortalContainerContext.tsx
    constants/
      app-type.constants.ts
    types/
      permission.types.ts
    features/
      login-popup-notification/
  styles/          ← Tạo mới, chứa CSS files cần thiết
    globals.css
```

### 2.2 Chạy script `copy-shared.cjs`

> ⚠️ **Trước khi chạy:** Mở `scripts/copy-shared.cjs`, điều chỉnh danh sách file (các mảng `API_FILES`, `UI_FILES`, ...) dựa trên output của `analyze-deps.cjs`.

```bash
node .claude/skills/cach-refactor-kien-truc-doc-lap/scripts/copy-shared.cjs src/modules/{PortalName}
```

Script copy chính xác từng file từ `src/shared/` và `src/styles/` vào `{PortalName}/shared/` và `{PortalName}/styles/`.

---

## Bước 3: Cập Nhật Import Paths

### 3.1 Chạy script `update-imports.cjs`

```bash
node .claude/skills/cach-refactor-kien-truc-doc-lap/scripts/update-imports.cjs src/modules/{PortalName}
```

### 3.2 Công thức tính relative path

Script tự tính: từ file có độ sâu `D` (số cấp thư mục từ portal root đến file):

```
prefix = '../'.repeat(D) + 'shared/'
@/shared/xxx → {prefix}xxx
```

Ví dụ kết quả sau khi chạy script:
| File (trong KiemThuApp) | Depth | `@/shared/utils` → |
|------------------------|-------|-------------------|
| `layout/KiemThuPortal.tsx` | 1 | `../shared/utils` |
| `features/bugs/pages/BugsPage.tsx` | 3 | `../../../shared/utils` |
| `shared/components/ui/dialog.tsx` | 3 | `../../../shared/contexts/PortalContainerContext` |
| `features/yeu-cau-phan-mem/sw-requests/services/X.ts` | 4 | `../../../../shared/services/api` |

---

## Bước 4: Verify & Commit

### 4.1 Kiểm tra không còn `@/shared/` imports

```bash
grep -rn "from ['\"]@/shared/" src/modules/{PortalName}/ --include="*.ts" --include="*.tsx"
# Kết quả phải = 0 matches
```

### 4.2 Kiểm tra TypeScript

```bash
npx tsc --noEmit
```

### 4.3 Kiểm tra các file còn thiếu

Duyệt từng file đã copy, kiểm tra xem có import nào trỏ đến file không tồn tại không.

### 4.4 Commit

```bash
git add src/modules/{PortalName}/
git commit -m "Refactor {PortalName}: copy shared dependencies, update imports to relative"
```

---

## Lưu Ý Quan Trọng

1. **Không copy toàn bộ** — mỗi portal có nhu cầu khác nhau về shared code
2. **Trace kỹ dependencies** — bỏ sót 1 file → lỗi build
3. **UI components dùng chung** — `button`, `dialog`, `select`, `table`... thường được dùng nhiều
4. **API layer là tightly coupled** — luôn copy toàn bộ `services/api/`
5. **Contexts cần trace kỹ** — `PermissionContext` kéo theo `PermissionService` + `permissionMappings/`
6. **Không đụng vào `src/shared/` gốc** — chỉ copy, không xóa, không sửa

---

## Checklist Sau Khi Refactor

- [ ] Không còn import `@/shared/` trong portal
- [ ] Tất cả file cần thiết đã được copy vào `portal/shared/`
- [ ] **Barrel `index.ts` export đủ tất cả component được import**
- [ ] **File mới copy được update-imports xử lý**
- [ ] TypeScript không báo lỗi
- [ ] Build / Vite dev không lỗi
- [ ] Commit + push lên repo portal
- [ ] Skill này được cập nhật nếu phát hiện pattern mới

---

## 🐛 Lỗi Thường Gặp & Cách Fix

### 1. `Failed to resolve import "xxx/components/common" — Does the file exist?`

**Nguyên nhân:** Copy file implementation nhưng thiếu barrel `index.ts`.

**Fix:** Tạo `portal/shared/components/common/index.ts` và `portal/shared/utils/index.ts`.
Script `copy-shared.cjs` đã tự động làm việc này từ commit `7b8b1cc5`.

---

### 2. `does not provide an export named 'SearchCombobox'`

**Nguyên nhân:** Barrel `index.ts` chỉ export các file ĐÃ copy, nhưng code vẫn import component chưa được copy. Xảy ra khi:
- Chạy B2 (copy) dựa trên phân tích thủ công, bỏ sót component
- Component được dùng trong code nhưng không bị phát hiện vì import qua barrel

**Fix:**
1. Tìm component bị thiếu: `grep -rn "from '.*shared/components/common'" src/modules/{Portal}/`
2. Copy component thiếu + dependencies của nó
3. Chạy lại `update-imports.cjs` để cập nhật imports trong file mới
4. Cập nhật barrel `index.ts`

**Phòng tránh:** Luôn chạy `analyze-deps.cjs` với tùy chọn trace tất cả import từ barrel trước khi copy.

---

### 3. `Failed to resolve import "xxx/components/ui/command"`

**Nguyên nhân:** Component mới copy (vd: `SearchCombobox`) import từ `@/shared/components/ui/command` — UI component chưa được copy.

**Fix:** Copy `command.tsx` từ `src/shared/components/ui/` và chạy `update-imports.cjs`.

**Nguyên tắc:** Với mỗi component common mới copy, **kiểm tra tất cả imports của nó** và copy tất cả dependencies.
