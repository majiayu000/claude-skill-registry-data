---
name: tao-ui-dialog
description: 'Quy tắc tạo Dialog/Form. Cấu trúc: DialogHeader+DialogContent+DialogFooter, 3 mode (View/Create/Edit), maxWidth bắt buộc, nút X custom, validate onBlur, input lỗi border-destructive, input số type=text inputMode=numeric, SearchCombobox FK, view mode div. Load kèm tao-ui-giao-dien (foundation).'
---

# Dialog / Form

> Foundation: `tao-ui-giao-dien`. Kiểm tra: `check-dialog.cjs` (tự động chạy trong `check-all.cjs`).

## maxWidth — BẮT BUỘC
| Form | maxWidth | className |
|------|----------|-----------|
| Nhỏ ≤4 fields | — | `max-h-[90vh]` |
| Trung bình CRUD | `'600px'` | `w-[600px] max-h-[90vh] overflow-y-auto` |
| Lớn | `'800px'` | `w-[800px] max-h-[90vh]` |
| Nhiều tab | `'920px'` | `w-[920px] max-h-[90vh]` |
| In A4 | `'210mm'` | `w-[210mm] max-h-[92vh] p-0` |

### ⚠️ CÁCH DÙNG ĐÚNG (kinh nghiệm thực tế)

> **DialogContent KHÔNG truyền `maxWidth` prop → bị giới hạn `sm:max-w-lg` = 512px, MỌI `w-[...]` trong className đều KHÔNG hiệu lực!**

```
❌ SAI — chỉ có className w-[...], không có maxWidth → dialog luôn 512px dù khai 900px
<DialogContent className='w-[900px] max-h-[92vh] overflow-y-auto'>

❌ SAI — nhét maxWidth vào className string (không phải prop) → vẫn không hiệu lực
<DialogContent className='maxWidth="800px" w-[800px] max-h-[92vh]'>

✅ ĐÚNG — truyền maxWidth prop + className w-[...] KHỚP nhau
<DialogContent maxWidth='900px' className='w-[900px] max-h-[92vh] overflow-y-auto'>
```

**Quy tắc:**
1. `maxWidth` là **prop riêng** của `DialogContent` (nhập qua inline style) — KHÔNG được nhét vào `className`.
2. Giá trị `maxWidth` phải **KHỚP** với `w-[...]` trong className (VD: `maxWidth='900px'` ↔ `w-[900px]`).
3. Mọi dialog có `w-[...]` bắt buộc kèm `maxWidth` tương ứng — nếu không, width không hiệu lực (bị fallback 512px).

## Cấu Trúc

> ⚠️ **Title dialog:** Luôn dùng `text-[20px]` cho `DialogTitle` — đồng nhất trên tất cả dialog.

```tsx
<DialogContent maxWidth='600px' className='w-[600px] max-h-[90vh] overflow-y-auto'>
  <DialogHeader>
    <div className='flex items-center justify-between'>
      <DialogTitle className='text-[20px]'>{mode === 'view' ? 'Xem chi tiết' : mode === 'edit' ? 'Chỉnh sửa' : 'Thêm mới'}</DialogTitle>
      <Button variant='ghost' size='sm' data-qa='btn_dong_dialog' onClick={() => onOpenChange(false)}><X className='h-4 w-4'/></Button>
    </div>
  </DialogHeader>

  <div className='space-y-4 py-4'>
    {/* Input fields */}
  </div>

  <DialogFooter className='flex justify-end gap-3 pt-4 border-t'>
    {mode === 'view'
      ? <Button className='btn-secondary' data-qa='btn_dong' onClick={() => onOpenChange(false)}>Đóng</Button>
      : <>
          <Button className='btn-secondary' data-qa='btn_huy' disabled={submitting} onClick={() => onOpenChange(false)}>Hủy</Button>
          <Button className='btn-primary' data-qa='btn_luu' type='submit' disabled={submitting}>
            {submitting && <Loader2 className='animate-spin h-4 w-4 mr-2'/>}
            {submitting ? 'Đang lưu...' : mode === 'create' ? 'Tạo mới' : 'Lưu'}
          </Button>
        </>
    }
  </DialogFooter>
</DialogContent>
```

## Footer — Quy Tắc Button

> **Áp dụng cho cả `DmDialogFooter` và `DialogFooter` inline.**

| Nút | Class | Màu sắc |
|-----|-------|---------|
| **Lưu** / **Tạo mới** / **Lưu & Thêm** | `btn-primary` | `bg-[#1565C0] text-white` (primary) |
| **Hủy** / **Đóng** | `btn-secondary` | `bg-white border border-gray-300 text-gray-700` |
| **Xóa** | `btn-danger` | `bg-[#f44336] text-white` (phải kèm `ConfirmDialog`) |

**Dùng `DmDialogFooter` (khuyến nghị cho KetoanApp):**

```tsx
import { DmDialogFooter } from '@/modules/KetoanApp/components'

<DmDialogFooter
  isView={isReadonly}
  isCreate={isCreate}
  submitting={submitting}
  onClose={() => onOpenChange(false)}
  onSave={doSubmit}
  onSaveAndAdd={doSubmitAndAdd}    // chỉ hiện khi isCreate=true
/>
```

- `isView`: [Đóng]
- `isCreate`: [Hủy] ── [Lưu] [Lưu & Thêm]
- Edit (không isCreate, không isView): [Hủy] ── [Lưu]

> **⚠️ TUYỆT ĐỐI KHÔNG dùng `variant='outline'` cho nút Lưu.** Phải dùng `className='btn-primary rounded-[8px]'`.

## Input Fields
- **Validate onBlur** — KHÔNG validate onChange
- **Lỗi:** `border-destructive` + `<AlertCircle className='h-3 w-3'/>` inline
- **Input số:** `type='text' inputMode='numeric'` + `text-right`
- **Textarea:** `className='invoice-textarea'`
- **FK field:** `<SearchCombobox dataQa='cmb_...' />`
- **View mode:** `<div className='px-3 py-2 text-gray-900'>` (KHÔNG dùng input disabled)
- **DatePicker:** `data-qa='dt_...'`

## Địa Chỉ (Vị Trí Địa Lý) — Dùng `DmAddressFields`

> Khi dialog có tab "Địa chỉ khác" hoặc form chứa trường địa chỉ (Tỉnh/TP, Quận/Huyện, Xã/Phường), dùng component `DmAddressFields` từ `@/modules/KetoanApp/components`.

**Cấu trúc 4 field:**
| Field | Loại | Nguồn dữ liệu |
|-------|------|--------------|
| Quốc gia | Input disabled | Mặc định "Việt Nam" |
| Tỉnh/Thành phố | Select | API `/api/base/v1/provinces` |
| Quận/Huyện | Select | API `/api/base/v1/communes?provinceId=X` |
| Xã/Phường | Select | API `/api/base/v1/communes?provinceId=X` |

**Sử dụng trong `DmShippingAddressTab`:**
```tsx
import { DmAddressFields } from '@/modules/KetoanApp/components'

<DmAddressFields
  formData={f}
  updateField={updateField}
  isReadonly={isReadonly}
  showLabels={false}        // ẩn label khi dùng trong tab có title riêng
  dataQaPrefix='i'          // → data-qa='i_province', 'i_district', 'i_ward'
/>
```

**Sử dụng độc lập (có label):**
```tsx
<DmAddressFields
  formData={f}
  updateField={updateField}
  isReadonly={isReadonly}
  showLabels={true}         // hiển thị label "Tỉnh/Thành phố", "Quận/Huyện", "Xã/Phường"
  gridCols='grid-cols-2'    // layout 2 cột
  dataQaPrefix='addr'
/>
```

**Lưu ý:**
- `DmAddressFields` tự quản lý việc gọi API qua hook `useAddressData` — không cần truyền props loadOptions
- Khi chọn tỉnh → tự reset quận/huyện và xã/phường
- Khi chọn quận/huyện → tự reset xã/phường
- Nếu chưa chọn tỉnh, select Quận/Huyện và Xã/Phường hiển thị "Chưa có dữ liệu"

## 2 Cột: `grid grid-cols-2 gap-4`, field rộng thêm `col-span-2`

## Nhiều Tab: `maxWidth='920px'`, `<Tabs>` trong body, `data-qa='tab_...'`

---

## Quy Tắc Field Thiếu — Cấm Tự Thêm Vào Type

> ⚠️ **TUYỆT ĐỐI CẤM:** Tự ý thêm field vào type DTO (`.types.api.ts`). Nếu UI có field mà BE chưa có → **phải yêu cầu BE bổ sung**, không tự thêm vào type.
> Lý do: BE và FE phải thống nhất DTO. FE tự thêm field → API lỗi hoặc bỏ qua field → mất dữ liệu.

---

## Reset State Khi Đóng/Mở Lại Dialog (BẮT BUỘC)

> ⚠️ **Khi dialog đóng rồi mở lại, state phải theo `initialData` mới, KHÔNG được giữ giá trị cũ.**

| Tình huống | Hành vi đúng | Hành vi sai |
|-----------|-------------|------------|
| Đóng dialog → mở lại với record khác | Form reset về giá trị từ `initialData` mới | ❌ Form vẫn giữ giá trị record cũ |
| Đóng dialog → mở lại để tạo mới | Form trắng, `autoFillCode()` chạy lại | ❌ Form còn data cũ từ lần edit trước |
| Đóng dialog → mở lại View cùng record | Form hiển thị đúng `initialData` | ❌ Form hiển thị data cũ đã bị sửa (chưa save) |

**Pattern đúng trong hook (truyền `open` vào hook):**
```tsx
// Hook nhận thêm `open` để reset mỗi lần dialog mở
export function useXxxDialogForm(initialData: XxxDto | null, onSuccess, onClose, cloneMode, open: boolean) {
  const [formData, setFormData] = useState<XxxFormState>(() => buildInitial(initialData))

  // Reset khi dialog mở HOẶC initialData/cloneMode thay đổi
  useEffect(() => {
    if (open === false) return          // <-- QUAN TRỌNG: không reset khi đóng dialog
    setFormData(buildInitial(initialData))
    setErrors({})
    setTouched({})
    setServerError(null)
    setServerErrorOpen(false)
    setSubmitting(false)
  }, [initialData, cloneMode, open])    // <-- open là key dependency
}
```

**Gọi từ component:**
```tsx
const hookData = useXxxDialogForm(
    isClone ? cloneFrom : (editMode ? initialData : null),
    () => { onOpenChange(false); onSuccess?.() },
    () => onOpenChange(false),
    isClone,
    open,    // <-- truyền open từ props
)
```

> **Nguyên nhân lỗi phổ biến #1:** Hook chỉ dùng `useState(initial)` — component không unmount khi đóng dialog (chỉ ẩn), nên `useState` không chạy lại. Khi mở dialog với record mới, state vẫn là giá trị cũ.
>
> **Nguyên nhân lỗi phổ biến #2:** `useEffect` chỉ có `[initialData, cloneMode]` — khi đóng dialog tạo mới rồi mở lại tạo mới, `initialData` vẫn là `null` và `cloneMode` vẫn là `false`, không thay đổi → useEffect không chạy. **Phải thêm `open` vào deps để reset mỗi lần dialog mở.**

---

## Script Kiểm Tra (tự động trong check-all.cjs)

```bash
# Chạy riêng 1 portal / feature
node .claude/skills/checklist-sau-code/scripts/check-for-skill/check-dialog.cjs src/modules/KiemThuApp
node .claude/skills/checklist-sau-code/scripts/check-for-skill/check-dialog.cjs src/modules/KiemThuApp features/release-versions
```

**3 checks phát hiện:**

| # | Lỗi | Severity |
|---|-----|:--------:|
| 1 | `DialogContent` có `w-[...]` NHƯNG thiếu prop `maxWidth` → width không hiệu lực (bị giới hạn `sm:max-w-lg` 512px) | 🔴 HIGH |
| 2 | Cú pháp sai: `maxWidth=` nằm TRONG className string (phải là prop riêng) | 🔴 HIGH |
| 3 | `maxWidth="X"` KHÁC `w-[X]` trong className (2 giá trị không khớp) | 🟡 WARNING |

> Exit 0 = PASS. Script được đăng ký trong `check-all.cjs` (mảng `checks`) → tự chạy mỗi lần review.
