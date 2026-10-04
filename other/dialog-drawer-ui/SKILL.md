---
name: dialog-drawer-ui
description: 'Tạo Dialog hoặc Right Drawer cho CRUD danh mục/nghiệp vụ. Đầu vào: chọn loại hiển thị (dialog/right drawer, mặc định dialog), mô tả giao diện, endpoint API. Sau khi tạo UI xong → tự động test create + update từng bản ghi → báo cáo field sai/thiếu so với BE. Kế thừa tao-dialog-new/SKILL.md cho dialog, dùng Sheet component cho drawer.'
argument-hint: 'Mô tả UI cần tạo + loại hiển thị. VD: Tạo dialog loại hàng hóa với fields code, name, unit, price, dùng dialog (mặc định)'
---

# Dialog / Drawer UI — Tạo + Tự Động Test

> **Mục tiêu:** Tạo UI CRUD (dialog hoặc right drawer) → tự động test create + update → báo cáo field sai/thiếu so với BE DTO.
> **Foundation:** `tao-dialog-new/SKILL.md` (dialog pattern) + `tao-ui-giao-dien-new/SKILL.md` (UI foundation)
> **Drawer:** Dùng `Sheet` component từ `@/shared/components/ui/sheet` (side='right')

---

## Quy Trình Tổng Quan

```
[1] Xác định loại hiển thị (dialog / right drawer, mặc định dialog)
[2] Phân tích yêu cầu → xác định fields, pattern
[3] Load API DTO từ BE nếu có endpoint
[4] Tạo UI (types → services → hooks → dialog/drawer)
[5] TỰ ĐỘNG TEST: Test create 1 bản ghi → Test update từng bản ghi
[6] Đối chiếu field UI vs BE DTO → Báo cáo field sai/thiếu
[7] Sửa nếu có lỗi → Báo cáo tổng kết
```

---

## 1. Xác Định Loại Hiển Thị

### 1.1 Hỏi người dùng (BẮT BUỘC)

```
Hỏi: "Bạn muốn hiển thị form dạng Dialog (popup giữa màn hình) hay Right Drawer (trượt từ phải sang)?"
  → Không trả lời → mặc định: Dialog
  → "dialog" → dùng Dialog pattern
  → "drawer" / "right drawer" → dùng Sheet (right drawer) pattern
```

### 1.2 So sánh 2 loại

| Tiêu chí | Dialog | Right Drawer |
|----------|--------|-------------|
| Vị trí | Giữa màn hình, popup | Trượt từ phải, chiếm 40-50% màn hình |
| Component | `Dialog + DialogContent` | `Sheet + SheetContent (side='right')` |
| Phù hợp | Form vừa/nhỏ, CRUD danh mục, nghiệp vụ | Form dài, cần không gian dọc, xem nhanh |
| maxWidth | `'600px'` / `'920px'` | `w-[500px] sm:max-w-[600px]` |
| Overlay | Có (mặc định Dialog) | Có (mặc định Sheet) |
| Body scroll | `overflow-y-auto` trong DialogContent | Toàn bộ Sheet scroll tự nhiên |
| Header | `DialogHeader` | Custom div trong SheetContent |
| Footer | `DialogFooter` / `DmDialogFooter` | Custom div sticky bottom |

---

## 2. UI Pattern

### 2.1 Pattern A — Dialog (kế thừa `tao-dialog-new/SKILL.md`)

> **Tham khảo đầy đủ:** `tao-dialog-new/SKILL.md` — chọn Pattern A (Danh Mục CRUD) hoặc Pattern B (Full-Screen Nghiệp Vụ).
> Tại đây chỉ tóm tắt, chi tiết xem file gốc.

**Dialog Wrapper (Danh Mục CRUD):**
```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/shared/components/ui/dialog'
import { Button } from '@/shared/components/ui/button'
import { X } from 'lucide-react'
import { DmDialogFooter } from '@/modules/KetoanApp/components'

<Dialog open={open} onOpenChange={onOpenChange}>
  <DialogContent maxWidth='920px' className='max-h-[90vh] flex flex-col gap-0 p-0 overflow-hidden'>
    <DialogHeader className='flex-none px-5 py-3 border-b border-[#B7BCC3]'>
      <div className='flex items-center gap-2'>
        <DialogTitle className='text-[20px] font-bold text-gray-900 shrink-0'>
          {isCreate ? 'Thêm mới' : isView ? 'Xem chi tiết' : 'Chỉnh sửa'} {tên đối tượng}
        </DialogTitle>
        <Button variant='ghost' size='sm'
          className='ml-auto h-7 w-7 p-0 text-gray-400 hover:text-gray-600 rounded-[8px]'
          onClick={() => onOpenChange(false)} data-qa='btn_dong_dialog'>
          <X className='h-4 w-4' />
        </Button>
      </div>
    </DialogHeader>

    <div className='flex-1 min-h-0 overflow-y-auto px-5 py-4'>
      {/* Form fields — xem `tao-dialog-new/SKILL.md` Section 1.5 */}
    </div>

    <DmDialogFooter
      onClose={() => onOpenChange(false)}
      onSubmit={() => doSubmit(false)}
      onSubmitAndNew={() => doSubmit(true)}
      isReadonly={isReadonly}
      submitLabel='Lưu'
      submitAndNewLabel='Lưu & Thêm mới'
      closeLabel='Đóng'
    />
  </DialogContent>
</Dialog>
```

### 2.2 Pattern B — Right Drawer (Sheet)

> **Dùng khi:** Người dùng chọn "right drawer". Form trượt từ phải sang, phù hợp form dài, cần xem nhanh context bên trái.

**Drawer Wrapper:**
```tsx
import { Sheet, SheetContent } from '@/shared/components/ui/sheet'
import { Button } from '@/shared/components/ui/button'
import { X, Loader2 } from 'lucide-react'
import {
  DmFormField, DmFormInput, DmFormTextarea,
  DmFieldValue, DmGroupInput,
} from '@/modules/KetoanApp/components'

<Sheet open={open} onOpenChange={onOpenChange}>
  <SheetContent
    side='right'
    className='w-[500px] sm:max-w-[600px] p-0 gap-0 flex flex-col h-full [&>button:first-child]:hidden'
  >
    {/* ── Header ── */}
    <div className='flex items-center justify-between px-5 py-3 border-b border-[#B7BCC3] flex-shrink-0'>
      <span className='text-[20px] font-bold text-gray-900'>
        {isCreate ? 'Thêm mới' : isView ? 'Xem chi tiết' : 'Chỉnh sửa'} {tên đối tượng}
      </span>
      <Button variant='ghost' size='sm'
        className='h-7 w-7 p-0 text-gray-400 hover:text-gray-600 rounded-[8px]'
        onClick={() => onOpenChange(false)} data-qa='btn_dong_drawer'>
        <X className='h-4 w-4' />
      </Button>
    </div>

    {/* ── Body (fill available space, scroll y) ── */}
    <div className='flex-1 min-h-0 overflow-y-auto px-5 py-4'>
      <form id='xxx-form' onSubmit={(e) => { e.preventDefault(); doSubmit(false) }}>
        <div className='space-y-4'>
          {/* Form fields — dùng DmFormField giống dialog */}
          <DmFormField label='Mã' required error={errors.code}>
            {isReadonly ? <DmFieldValue value={f.code as string} />
              : <DmFormInput data-qa='i_code'
                  value={(f.code as string) ?? ''}
                  onChange={(e) => updateField('code', e.target.value)}
                  onBlur={() => handleBlur('code')} />}
          </DmFormField>

          <DmFormField label='Tên' required error={errors.name}>
            {isReadonly ? <DmFieldValue value={f.name as string} />
              : <DmFormInput data-qa='i_name'
                  value={(f.name as string) ?? ''}
                  onChange={(e) => updateField('name', e.target.value)}
                  onBlur={() => handleBlur('name')} />}
          </DmFormField>

          {/* ... các field khác */}
        </div>
      </form>
    </div>

    {/* ── Footer (sticky bottom) ── */}
    <div className='flex items-center justify-end gap-2 px-5 py-3 border-t border-[#B7BCC3] flex-shrink-0 bg-white'>
      {isView ? (
        <Button className='btn-secondary' data-qa='btn_dong' onClick={() => onOpenChange(false)}>Đóng</Button>
      ) : (
        <>
          <Button className='btn-secondary' data-qa='btn_huy' disabled={submitting}
            onClick={() => onOpenChange(false)}>Hủy</Button>
          <Button className='btn-primary' data-qa='btn_luu' type='submit' disabled={submitting}
            onClick={() => doSubmit(false)}>
            {submitting && <Loader2 className='animate-spin h-4 w-4 mr-2' />}
            {submitting ? 'Đang lưu...' : isCreate ? 'Tạo mới' : 'Lưu'}
          </Button>
        </>
      )}
    </div>
  </SheetContent>
</Sheet>
```

### 2.3 So sánh Dialog vs Drawer Code

| Thành phần | Dialog | Right Drawer |
|-----------|--------|-------------|
| Container | `Dialog` + `DialogContent` | `Sheet` + `SheetContent side='right'` |
| Header | `DialogHeader` + `DialogTitle` | Custom `div` + `span` |
| Header border | `border-b border-[#B7BCC3]` | `border-b border-[#B7BCC3]` |
| Body | `flex-1 min-h-0 overflow-y-auto px-5 py-4` | `flex-1 min-h-0 overflow-y-auto px-5 py-4` |
| Footer | `DmDialogFooter` (có sẵn) | Custom div sticky bottom |
| Nút X | `Button variant='ghost' size='sm'` | `Button variant='ghost' size='sm'` |
| Ẩn nút X mặc định | không cần (Dialog có nút X riêng) | `[&>button:first-child]:hidden` |
| Width | `maxWidth='920px'` | `w-[500px] sm:max-w-[600px]` |
| data-qa close | `btn_dong_dialog` | `btn_dong_drawer` |
| Layout form | `grid grid-cols-5` (dialog lớn) | `space-y-4` (xếp dọc, drawer hẹp) |

> ⚠️ **Drawer layout:** Vì drawer hẹp hơn dialog, nên field xếp **dọc** (`space-y-4`) thay vì grid ngang. Mỗi field chiếm full width.

---

## 3. Tạo Code Theo Loại Hiển Thị

### 3.1 Quy trình chung (giống `tao-dialog-new`)

```
[B1] Xác định shortName (SN) từ tên feature
[B2] Tạo types: {SN}.types.api.ts + {SN}.types.ui.ts
[B3] Tạo services: {SN}ApiService.ts
[B4] Tạo hooks: use{SN}.dlg.form.ts
[B5] Tạo UI: {SN}Dialog.tsx HOẶC {SN}Drawer.tsx (tùy chọn)
[B6] Tạo barrel: index.ts
```

### 3.2 Đặt tên file theo loại

| Loại | File name |
|------|----------|
| Dialog | `{SN}Dialog.tsx` |
| Right Drawer | `{SN}Drawer.tsx` |

> **Cả dialog và drawer dùng CHUNG:** types, services, hooks. Chỉ khác file UI.

### 3.3 Props Interface (dùng chung)

```tsx
interface Props {
  open: boolean
  onOpenChange: (v: boolean) => void
  initialData?: XxxDto | null
  viewOnly?: boolean
  onSuccess?: () => void
}
```

---

## 4. Tự Động Test Sau Khi Tạo UI

> ⚠️ **BẮT BUỘC:** Sau khi tạo xong UI, PHẢI tự động test. Không bỏ qua bước này.

### 4.1 Test Create — Tạo 1 Bản Ghi Mới

**Mục tiêu:** Kiểm tra UI có submit được không, BE có nhận đủ fields không, response có lỗi không.

**Các bước:**
```
1. Mở dialog/drawer ở chế độ Create
2. Điền đầy đủ TẤT CẢ các field (kể cả optional)
3. Submit
4. Kiểm tra response:
   - Success → ✅ OK
   - Validation error → ghi lại field nào bị lỗi
   - Server error → ghi lại message
5. Nếu success → mở lại ở chế độ View → kiểm tra HIỂN THỊ:
   - Tất cả field đã submit có hiển thị đúng giá trị không?
   - Field nào hiển thị sai → ghi lại
```

### 4.2 Test Update — Sửa Từng Bản Ghi

**Mục tiêu:** Kiểm tra submit update, field có bị mất khi update không.

**Các bước:**
```
1. Mở dialog/drawer ở chế độ Edit với bản ghi vừa tạo
2. Thay đổi ít nhất 1 field (vd: đổi tên)
3. Submit update
4. Kiểm tra response → ghi lại lỗi nếu có
5. Mở lại View → kiểm tra field đã sửa có hiển thị đúng không
```

### 4.3 Đối Chiếu UI vs BE DTO

**Mục tiêu:** Phát hiện field UI có mà BE không có, hoặc BE có mà UI thiếu.

**Các bước:**
```
1. Đọc file types: {SN}.types.api.ts → lấy danh sách field từ DTO
2. Đọc file types: {SN}.types.ui.ts → lấy danh sách field từ FormState
3. Đọc file UI → lấy danh sách field hiển thị trong form
4. So sánh:
   - Field trong DTO nhưng KHÔNG trong FormState → báo "UI thiếu field"
   - Field trong FormState nhưng KHÔNG trong DTO → báo "UI thừa field"
   - Field trong FormState nhưng KHÔNG hiển thị trong UI → báo "field chưa render"
```

### 4.4 Báo Cáo Kết Quả Test

Sau khi test, tạo báo cáo dạng:

```markdown
## 📊 Báo Cáo Test UI: {Tên Dialog/Drawer}

### 1. Test Create
| Field | Giá trị test | Kết quả submit | Ghi chú |
|-------|-------------|----------------|---------|
| code  | "TEST001"   | ✅ OK          |         |
| name  | "Test name" | ✅ OK          |         |
| ...   | ...         | ...            |         |

### 2. Test Update
| Field | Giá trị cũ | Giá trị mới | Kết quả | Ghi chú |
|-------|-----------|-------------|---------|---------|
| name  | "Test name" | "Updated" | ✅ OK   |         |

### 3. Đối Chiếu UI ↔ BE DTO
| Field | DTO | FormState | UI render | Trạng thái |
|-------|-----|-----------|-----------|------------|
| code  | ✅  | ✅        | ✅        | ✅ OK      |
| name  | ✅  | ✅        | ✅        | ✅ OK      |
| desc  | ✅  | ❌        | ❌        | ⚠️ THIẾU  |

### 4. Tổng Kết
- ✅ Pass: X/X tests
- ⚠️ Warning: Y field thiếu/thừa
- ❌ Fail: Z lỗi

### 5. Hành Động Đề Xuất
- [ ] Thêm field "desc" vào FormState và UI render
- [ ] Tạo inbox yêu cầu BE bổ sung field "xyz"
```

---

## 5. Quy Ước Chung Cho Cả Dialog & Drawer

| Quy ước | Giá trị |
|---------|---------|
| **Title** | `text-[20px] font-bold text-gray-900` |
| **Header border** | `border-b border-[#B7BCC3]` |
| **Footer border** | `border-t border-[#B7BCC3]` |
| **Body padding** | `px-5 py-4` |
| **Input height** | `h-8` (DmFormInput mặc định) |
| **Input rounding** | `rounded-[8px]` |
| **Font size** | `text-[13px]` |
| **Validate** | onBlur + DmFormField `error={errors.x}` |
| **View mode** | `DmFieldValue` / `DmTabFieldValue` (không dùng disabled input) |
| **Error dialog** | `ValidationErrorDialog` |
| **data-qa prefix** | `i_`=input, `sel_`=select, `chk_`=checkbox, `r_`=radio, `btn_`=button |
| **Hook logic** | Tất cả logic trong hooks, UI chỉ render |
| **Reset state** | `useEffect` theo `[open, initialData?.id]` — KHÔNG giữ data cũ khi mở lại |

---

## 6. Cấu Trúc File

```
features/{nhom}/{ten-feature}/
├── types/
│   ├── {SN}.types.api.ts       ← Enums + DTO từ BE
│   └── {SN}.types.ui.ts        ← FormState, initial values, errors type
├── services/
│   └── {SN}ApiService.ts       ← CRUD API
├── hooks/
│   └── use{SN}.dlg.form.ts    ← Hook dùng chung cho dialog & drawer
├── dialogs/
│   └── {SN}Dialog.tsx          ← Dialog component (nếu chọn dialog)
│   └── {SN}Drawer.tsx          ← Drawer component (nếu chọn drawer)
├── pages/
│   └── {SN}Page.tsx            ← Master page
└── index.ts                    ← Barrel exports (export cả Dialog + Drawer nếu có cả 2)
```

---

## 7. Checklist Trước Khi Báo Cáo Hoàn Thành

- [ ] Đã hỏi người dùng chọn dialog hay drawer (mặc định dialog nếu không trả lời)
- [ ] Chọn đúng pattern (A: Danh Mục / B: Nghiệp Vụ) nếu dùng dialog
- [ ] `maxWidth` / `width` đúng theo loại hiển thị
- [ ] 3 mode hoạt động: View / Create / Edit
- [ ] `isReadonly` flag cho tất cả fields
- [ ] Validate onBlur + inline error message
- [ ] `ValidationErrorDialog` cho lỗi server
- [ ] `data-qa` đầy đủ (prefix `btn_dong_dialog` hoặc `btn_dong_drawer`)
- [ ] View mode hiển thị `<div>` / `DmFieldValue` (không dùng disabled input)
- [ ] Nút X close custom (ẩn mặc định Radix/Sheet nếu cần)
- [ ] Hook không gọi API trực tiếp từ UI
- [ ] Types đủ fields từ DTO BE (đã đối chiếu)
- [ ] Barrel `index.ts` export
- [ ] **ĐÃ TEST CREATE:** submit thành công, hiển thị đúng
- [ ] **ĐÃ TEST UPDATE:** submit thành công, không mất field
- [ ] **ĐÃ ĐỐI CHIẾU UI ↔ BE DTO:** không field nào sai/thiếu
- [ ] **ĐÃ BÁO CÁO** kết quả test đầy đủ

---

## 8. Ví Dụ Prompt Mẫu

```
"Tạo form loại hàng hóa với fields: code, name, unit, price, description.
Dùng right drawer. Endpoint: /api/v1/inventory-items"
```

→ Agent sẽ:
1. Hỏi: chọn dialog hay drawer? → user nói "drawer" → chọn Right Drawer
2. Tạo types, services, hooks
3. Tạo `InventoryItemDrawer.tsx` với Sheet component
4. Test create: điền code="HH001", name="Hàng 1", unit="Cái", price=100000
5. Test update: sửa price thành 200000
6. Đối chiếu field: DTO có `description` không? FormState đã có chưa?
7. Báo cáo kết quả
