---
name: date-input
description: 'Quy tắc nhập liệu và hiển thị ngày tháng trong SASUCO InvoiceEasy. Dùng khi: thêm trường ngày tháng vào form hoặc filter, dùng DatePicker component, format yyyy-MM-dd trong state/API, format dd-MM-yyyy hiển thị cho user, tránh dùng input type=date, dataQa dt_ prefix, validate onBlur cho date field.'
---

# Quy Tắc Date Input — SASUCO InvoiceEasy

## Nguyên Tắc Cốt Lõi

| Layer | Format | Ví dụ |
|-------|--------|-------|
| **UI** (hiển thị cho user) | `dd-MM-yyyy` | `28-03-2026` |
| **State / Hook** | `yyyy-MM-dd` (ISO string) | `2026-03-28` |
| **API params** | `yyyy-MM-dd` (giữ nguyên từ state) | `2026-03-28` |

`DatePicker` tự xử lý chuyển đổi — **không cần** dùng `format()` / `parse()` thủ công.

---

## Component Bắt Buộc

```tsx
import { DatePicker } from '@/shared/components/common'

// ❌ CẤM
<input type="date" ... />
```

---

## Interface Props

```typescript
interface DatePickerProps {
  value: string              // ISO: 'yyyy-MM-dd' hoặc ''
  onChange: (iso: string) => void
  onBlur?: () => void
  className?: string         // ⚠️ Tên prop là 'className', KHÔNG phải 'inputClassName'
  placeholder?: string       // Mặc định: 'dd-MM-yyyy'
  disabled?: boolean
  id?: string
  dataQa?: string            // BẮT BUỘC khi cần test
}
```

---

## Dùng Trong Filter (Page)

```tsx
<DatePicker
  dataQa='dt_tu_ngay'
  value={tuNgay}
  onChange={setTuNgay}
  className='h-9 w-[150px]'
  placeholder='Từ ngày'
/>
<DatePicker
  dataQa='dt_den_ngay'
  value={denNgay}
  onChange={setDenNgay}
  className='h-9 w-[150px]'
  placeholder='Đến ngày'
/>
```

---

## Dùng Trong Dialog / Form

```tsx
<DatePicker
  id='ngay'
  dataQa='dt_ngay'
  value={form.ngay}
  onChange={(val) => setForm(prev => ({ ...prev, ngay: val }))}
  onBlur={() => validateField('ngay')}
  className='invoice-input'
/>
```

- **Validate on BLUR** — không validate onChange
- `dataQa` prefix: `dt_` — xem skill `tao-ui-giao-dien`

---

## State Pattern Trong Hook

```typescript
// Luôn dùng ISO string
const [tuNgay, setTuNgay] = useState<string>('2026-03-01')
const [denNgay, setDenNgay] = useState<string>('2026-03-31')

// Truyền thẳng vào API — không cần transform
const params = { dateFrom: tuNgay, dateTo: denNgay }
```

---


