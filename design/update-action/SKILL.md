---
name: update-action
description: 'Cập nhật action trong cột thao tác của bảng dữ liệu master page KetoanApp. MẶC ĐỊNH áp dụng Pattern B: Edit + Xóa (Button) + Chức năng khác (DropdownMenu: Nhân bản + Ngừng/Kích hoạt). Hỗ trợ 3 pattern: Pattern B (mặc định), Pattern A (useDmRowActions chuẩn), Pattern C (useDmRowActions + extraActions). Đầu vào: chỉ rõ bảng nào (đường dẫn page).'
---

# Update Action — Cập Nhật Cột Thao Tác Bảng Dữ Liệu

> **Kế thừa:** `tao-master-page` (cấu trúc page), `tao-ui-giao-dien-new` (UI foundation), `dat-ten` (quy tắc data-qa).
> **Áp dụng cho:** Master Page trong KetoanApp (`src/modules/KetoanApp/features/**/pages/*Page.tsx`).

> **⚠️ MẶC ĐỊNH:** Khi user gọi `/update-action` cho 1 page, mặc định áp dụng **Pattern B**: Sửa (Button) + Xóa (Button) + Chức năng khác (DropdownMenu: Nhân bản, Ngừng/Kích hoạt). Chỉ dùng Pattern A/C khi user yêu cầu rõ ràng.

---

## 1. Xác Định Đầu Vào

Trước khi update, xác định rõ:

| Thông tin | Mô tả | Ví dụ |
|-----------|-------|-------|
| **Page file** | Đường dẫn tuyệt đối file Page cần sửa | `src/modules/KetoanApp/features/danh-muc/tien-te/pages/TienTePage.tsx` |
| **Pattern hiện tại** | Đang dùng `DmRowActions` hay Button thủ công? | `useDmRowActions` |
| **Action đích** | Mặc định Pattern B: Sửa + Xóa + DropdownMenu(Nhân bản, Toggle) | — |

### Cách xác định pattern hiện tại

Mở page file, tìm trong cột ghost action (`DmTableCell sticky right-0`):

| Dấu hiệu | Pattern |
|----------|---------|
| Có `<Button>` + `<DropdownMenu>` thủ công | **Pattern B** — Button thủ công (MẶC ĐỊNH) |
| Có `<DmRowActions actions={getRowActions(item)} />` | **Pattern A** — `useDmRowActions` |
| Có `<DmRowActions>` nhưng import thêm `DropdownMenu` | **Pattern C** — Hỗn hợp |

---

## 2. Ba Pattern Action

### Pattern B — Button Sửa + Xóa + DropdownMenu "Chức năng khác" (MẶC ĐỊNH)

> **Đây là pattern mặc định khi gọi `/update-action`.** Không cần user chỉ định.

Dùng khi: Cần đầy đủ Sửa / Xóa / Nhân bản / Toggle Active trong 1 layout gọn, chuyên nghiệp.

> File tham khảo: `src/modules/KetoanApp/features/danh-muc/tai-khoan-ket-chuyen/pages/CapTaiKhoanPage.tsx`

#### B.1 Imports cần có

```tsx
import { Button } from '@/shared/components/ui/button'
import { Pencil, Trash2, MoreHorizontal, Copy, Ban, CheckCircle } from 'lucide-react'
import {
  DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
} from '@/shared/components/ui/dropdown-menu'
```

> ⚠️ **KHÔNG import `DmRowActions` hoặc `useDmRowActions`** — Pattern B dùng Button thủ công hoàn toàn.

#### B.2 State & handlers cần có trong component

```tsx
// State cho dialog CRUD
const [dialogOpen, setDialogOpen] = useState(false)
const [selectedItem, setSelectedItem] = useState<XxxDto | null>(null)
const [cloneFrom, setCloneFrom] = useState<XxxDto | null>(null)

// State cho confirm delete
const [deleteItem, setDeleteItem] = useState<XxxDto | null>(null)
const [deleteOpen, setDeleteOpen] = useState(false)

// Hook dialog form — để lấy handleDelete, handleToggleActive
const { handleDelete, handleToggleActive } = useXxxDialogForm(null)

function handleEdit(item: XxxDto)   { setSelectedItem(item); setCloneFrom(null); setDialogOpen(true) }
function handleClone(item: XxxDto)  { setCloneFrom(item); setSelectedItem(null); setDialogOpen(true) }
function handleDeleteRow(item: XxxDto) { setDeleteItem(item); setDeleteOpen(true) }
function handleCreate()             { setSelectedItem(null); setCloneFrom(null); setDialogOpen(true) }
```

#### B.3 Ghost column với Button + DropdownMenu

```tsx
{/* Cột neo sticky phải — action hiện khi hover row */}
<DmTableCell className='sticky right-0 z-20 bg-transparent'
  style={{ width: 0, minWidth: 0, padding: 0, border: 'none', overflow: 'visible' }}>
  <div className='absolute right-0 top-0 bottom-0 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity duration-150 bg-gradient-to-l from-white via-white/90 to-transparent pl-16 pr-2'>

    {/* [1] Sửa — luôn có */}
    <Button variant='ghost' size='sm'
      className='icon-warning border rounded-lg bg-white'
      title='Sửa' data-qa={`btn_sua_${item.id}`}
      onClick={(e) => { e.stopPropagation(); handleEdit(item) }}>
      <Pencil className='h-4 w-4' />
    </Button>

    {/* [2] Xóa — luôn có */}
    <Button variant='ghost' size='sm'
      className='icon-danger border rounded-lg bg-white'
      title='Xóa' data-qa={`btn_xoa_${item.id}`}
      onClick={(e) => { e.stopPropagation(); handleDeleteRow(item) }}>
      <Trash2 className='h-4 w-4' />
    </Button>

    {/* [3] DropdownMenu — Chức năng khác */}
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant='ghost' size='sm'
          className='border rounded-lg bg-white'
          title='Chức năng khác' data-qa={`btn_khac_${item.id}`}>
          <MoreHorizontal className='h-4 w-4' />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align='end' className='w-40'>
        {/* Nhân bản */}
        <DropdownMenuItem onSelect={() => handleClone(item)}
          data-qa={`btn_nhan_ban_${item.id}`}>
          <Copy className='h-4 w-4' /> Nhân bản
        </DropdownMenuItem>
        {/* Toggle Active: Ngừng sử dụng / Kích hoạt */}
        <DropdownMenuItem
          onSelect={async () => {
            const ok = await handleToggleActive(item)
            if (ok) refetch()
          }}
          data-qa={`btn_toggle_active_${item.id}`}>
          {item.isActive ? (
            <><Ban className='h-4 w-4' /> Ngừng sử dụng</>
          ) : (
            <><CheckCircle className='h-4 w-4' /> Kích hoạt</>
          )}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>

  </div>
</DmTableCell>
```

#### B.4 Quy tắc icon variant trong Pattern B

| Action | Class | Icon |
|--------|-------|------|
| Sửa | `icon-warning border rounded-lg bg-white` | `Pencil` |
| Xóa | `icon-danger border rounded-lg bg-white` | `Trash2` |
| Chức năng khác (trigger) | `border rounded-lg bg-white` | `MoreHorizontal` |

---

### Pattern A — `useDmRowActions` (chuẩn, CRUD cơ bản)

Dùng khi: Chỉ cần Xem / Sửa / Nhân bản / Xóa — không có action đặc biệt. User phải chỉ định rõ nếu muốn dùng pattern này thay vì mặc định.

```tsx
// --- IMPORTS ---
import { useDmRowActions } from '@/shared/hooks'
import { DmRowActions } from '@/modules/KetoanApp/components'

// --- HOOK (trong component) ---
const getRowActions = useDmRowActions<XxxDto>({
  canView: true,    // true = hiện nút Xem (mặc định)
  canEdit: true,    // true = hiện nút Sửa
  canClone: true,   // true = hiện nút Nhân bản
  canDelete: true,  // true = hiện nút Xóa
  onView:   (item) => { setSelectedItem(item); setDialogOpen(true) },
  onEdit:   (item) => { setSelectedItem(item); setDialogOpen(true) },
  onClone:  (item) => { setCloneFrom(item); setSelectedItem(null); setDialogOpen(true) },
  onDelete: (item) => { setDeleteItem(item); setDeleteOpen(true) },
})

// --- TRONG GHOST COLUMN ---
<DmTableCell className='sticky right-0 z-20 bg-transparent'
  style={{ width: 0, minWidth: 0, padding: 0, border: 'none', overflow: 'visible' }}>
  <div className='absolute right-0 top-0 bottom-0 flex items-center opacity-0 group-hover:opacity-100 transition-opacity duration-150 bg-gradient-to-l from-white via-white/90 to-transparent pl-12 pr-2'>
    <DmRowActions actions={getRowActions(item)} />
  </div>
</DmTableCell>
```

**Tắt action**: set `canXxx: false`.

```tsx
// Ví dụ: không có Nhân bản
const getRowActions = useDmRowActions<XxxDto>({
  canClone: false,  // ← tắt
  onView: ..., onEdit: ..., onDelete: ...,
})
```

---

### Pattern C — `useDmRowActions` + `extraActions` (Toggle Active gọn)

Dùng khi: Vẫn muốn dùng `DmRowActions` cho các action chuẩn, nhưng cần thêm Toggle Active qua `extraActions`.

```tsx
import { useDmRowActions } from '@/shared/hooks'
import { DmRowActions } from '@/modules/KetoanApp/components'
import { Ban, CheckCircle } from 'lucide-react'

const { handleToggleActive } = useXxxDialogForm(null)

const getRowActions = useDmRowActions<XxxDto>({
  onView:   (item) => { setSelectedItem(item); setDialogOpen(true) },
  onEdit:   (item) => { setSelectedItem(item); setDialogOpen(true) },
  onClone:  (item) => { setCloneFrom(item); setSelectedItem(null); setDialogOpen(true) },
  onDelete: (item) => { setDeleteItem(item); setDeleteOpen(true) },
  extraActions: (item) => [{
    icon: item.isActive ? Ban : CheckCircle,
    label: item.isActive ? 'Ngừng sử dụng' : 'Kích hoạt',
    variant: 'warning',
    'data-qa': `btn_toggle_active_${item.id}`,
    onClick: async () => { const ok = await handleToggleActive(item); if (ok) refetch() },
  }],
})
```

> **Ưu điểm**: Code gọn, tận dụng `DmRowActions` có sẵn.
> **Nhược điểm**: Nếu có >2 action đặc biệt, nên dùng Pattern B (DropdownMenu) để tránh quá nhiều nút.

---

## 3. Quy Trình Update Action

### Bước 1: Đọc page hiện tại

```bash
# Đọc toàn bộ page file để xác định pattern hiện tại
read_file pagePath 1 999
```

Xác định:
- Đang dùng pattern nào? (A / B / C)
- Có những action nào hiện tại?
- Có state `cloneFrom` chưa? (cần cho Nhân bản)
- Có `handleToggleActive` trong hook dialog form chưa?

### Bước 2: Xác định thay đổi cần làm

| Yêu cầu | Pattern đích | Thay đổi |
|---------|-------------|----------|
| Thêm Nhân bản | A (bật `canClone: true`) | Thêm state `cloneFrom`, sửa `onClone` handler |
| Thêm Toggle Active | B hoặc C | Pattern B: thêm DropdownMenu; Pattern C: thêm `extraActions` |
| Thêm cả Nhân bản + Toggle Active | B | Dùng Button thủ công + DropdownMenu |
| Bỏ Xem (chỉ Sửa/Xóa) | A (tắt `canView: false`) | Set `canView: false` |
| Chuyển từ A sang B | B | Thay `DmRowActions` → Button + DropdownMenu |
| Chuyển từ B sang A | A | Thay Button + DropdownMenu → `DmRowActions` |

### Bước 3: Kiểm tra dependencies trước khi sửa

Trước khi sửa ghost column, đảm bảo các thứ sau đã có trong page:

| Thành phần | Cần cho action nào | Cách kiểm tra |
|-----------|-------------------|---------------|
| `cloneFrom` state | Nhân bản | Tìm `useState<XxxDto \| null>(null)` thứ 3 |
| `handleClone()` | Nhân bản | Tìm function `handleClone` |
| `handleToggleActive` | Toggle Active | Có trong return của `useXxxDialogForm(null)` |
| `deleteItem` + `deleteOpen` state | Xóa | Tìm `useState` cho delete |
| `ConfirmDialog` | Xóa | Tìm `<ConfirmDialog` cuối JSX |
| `DropdownMenu` import | Pattern B | Kiểm tra imports từ `dropdown-menu` |

Nếu thiếu → thêm vào trước khi sửa ghost column.

### Bước 4: Sửa ghost column

Thay toàn bộ block `<DmTableCell className='sticky right-0...'>` bằng pattern mới.

### Bước 5: Cập nhật PAGE_FEATURES (nếu có)

```tsx
export const PAGE_FEATURES = [
  { label: 'Làm mới', code: 'btn-refresh' },
  { label: 'Thêm mới', code: 'btn-create' },
  { label: 'Chỉnh sửa', code: 'row-edit' },
  { label: 'Xóa', code: 'row-delete' },
  { label: 'Nhân bản', code: 'row-clone' },                          // ← thêm nếu mới
  { label: 'Ngừng sử dụng / Kích hoạt', code: 'row-toggle-active' }, // ← thêm nếu mới
]
```

### Bước 6: Kiểm tra data-qa

| Action | data-qa pattern |
|--------|----------------|
| Sửa | `btn_sua_${item.id}` |
| Xóa | `btn_xoa_${item.id}` |
| Nhân bản | `btn_nhan_ban_${item.id}` |
| Chức năng khác (trigger) | `btn_khac_${item.id}` |
| Toggle Active | `btn_toggle_active_${item.id}` |

---

## 4. Các Trường Hợp Cụ Thể

### 4.1 Thêm Nhân Bản vào page chưa có

**Page hiện tại**: Dùng `useDmRowActions` với `onClone: () => { setSelectedItem(null); setDialogOpen(true) }` (clone rỗng, chưa copy data).

**Cần sửa**:
1. Thêm state: `const [cloneFrom, setCloneFrom] = useState<XxxDto | null>(null)`
2. Sửa `handleCreate`: `setCloneFrom(null)` trước khi mở dialog
3. Sửa `onClone`: `onClone: (item) => { setCloneFrom(item); setSelectedItem(null); setDialogOpen(true) }`
4. Thêm prop `cloneFrom` vào Dialog: `<XxxFormDialog ... cloneFrom={cloneFrom} />`
5. Kiểm tra Dialog đã hỗ trợ `cloneFrom` prop chưa (xem `edit-form-pattern.md` trong user memory)

### 4.2 Thêm Toggle Active (Ngừng sử dụng / Kích hoạt)

**Điều kiện**: DTO phải có field `isActive: boolean`.

**Pattern B — Thêm DropdownMenu**:

1. Thêm import `DropdownMenu`, `MoreHorizontal`, `Ban`, `CheckCircle`, `Copy`
2. Đảm bảo hook dialog form export `handleToggleActive`
3. Thay ghost column bằng Pattern B (Section 2.B.3)
4. Nếu chưa có `handleDelete` từ hook → destructure thêm
5. Thêm `ConfirmDialog` cho delete nếu chưa có

**Pattern C — Thêm extraActions**:

1. Thêm import `Ban`, `CheckCircle`
2. Thêm `extraActions` vào `useDmRowActions` (Section 2.C)
3. Đảm bảo hook dialog form export `handleToggleActive`

### 4.3 Bỏ bớt action

| Muốn bỏ | Cách làm |
|---------|---------|
| Xem | Set `canView: false` (Pattern A) hoặc xóa Button Xem (Pattern B) |
| Nhân bản | Set `canClone: false` (Pattern A) hoặc xóa DropdownMenuItem (Pattern B) |
| Xóa | Set `canDelete: false` (Pattern A) hoặc xóa Button Xóa (Pattern B) |
| Toggle Active | Xóa DropdownMenuItem (Pattern B) hoặc xóa `extraActions` (Pattern C) |

### 4.4 Chuyển từ Pattern A → Pattern B

Khi cần thêm Toggle Active hoặc action tùy chỉnh không có trong `useDmRowActions`:

1. Xóa import `DmRowActions`, `useDmRowActions`
2. Thêm import `DropdownMenu`, `MoreHorizontal`, `Ban`, `CheckCircle`, `Copy`, `Pencil`, `Trash2`
3. Thay `getRowActions` + `<DmRowActions>` bằng Button thủ công + DropdownMenu (Section 2.B.3)
4. Đảm bảo có `handleEdit`, `handleClone`, `handleDeleteRow`, `handleToggleActive`

---

## 5. Checklist Sau Khi Update

- [ ] Tất cả action có `data-qa` đúng format (`btn_{action}_{item.id}`)
- [ ] Icon đúng variant class (`icon-warning` cho Sửa, `icon-danger` cho Xóa)
- [ ] Button trong ghost column có `border rounded-lg bg-white`
- [ ] `cloneFrom` state được reset trong `handleCreate()`
- [ ] Dialog có prop `cloneFrom={cloneFrom}` (nếu có Nhân bản)
- [ ] `handleToggleActive` gọi `refetch()` sau khi thành công
- [ ] `ConfirmDialog` cho delete có đủ `open`, `onOpenChange`, `onConfirm`
- [ ] `PAGE_FEATURES` được cập nhật nếu thêm action mới
- [ ] Không import thừa (nếu bỏ `DmRowActions` thì xóa import)
- [ ] Code compile không lỗi

---

## 6. Ví Dụ Đầy Đủ

### Ví dụ 1: Page đang dùng Pattern A, thêm Toggle Active bằng Pattern C

**Trước**:
```tsx
const getRowActions = useDmRowActions<CurrencyDto>({
  onView: (item) => { setSelectedItem(item); setDialogOpen(true) },
  onEdit: (item) => { setSelectedItem(item); setDialogOpen(true) },
  onClone: () => { setSelectedItem(null); setDialogOpen(true) },
  onDelete: (item) => { setDeleteItem(item); setDeleteOpen(true) },
})
```

**Sau**:
```tsx
import { Ban, CheckCircle } from 'lucide-react'

const { handleDelete, handleBulkDelete, handleToggleActive } = useTTDialogForm(null)

const getRowActions = useDmRowActions<CurrencyDto>({
  onView: (item) => { setSelectedItem(item); setDialogOpen(true) },
  onEdit: (item) => { setSelectedItem(item); setDialogOpen(true) },
  onClone: (item) => { setCloneFrom(item); setSelectedItem(null); setDialogOpen(true) },
  onDelete: (item) => { setDeleteItem(item); setDeleteOpen(true) },
  extraActions: (item) => [{
    icon: item.isActive ? Ban : CheckCircle,
    label: item.isActive ? 'Ngừng sử dụng' : 'Kích hoạt',
    variant: 'warning',
    'data-qa': `btn_toggle_active_${item.id}`,
    onClick: async () => { const ok = await handleToggleActive(item); if (ok) refetch() },
  }],
})
```

### Ví dụ 2: Page chưa có action nào, tạo mới toàn bộ bằng Pattern B

Tham khảo toàn bộ file: `src/modules/KetoanApp/features/danh-muc/tai-khoan-ket-chuyen/pages/CapTaiKhoanPage.tsx`

Các phần cần có:
1. Imports: `Pencil`, `Trash2`, `MoreHorizontal`, `Copy`, `Ban`, `CheckCircle`, `DropdownMenu*`
2. State: `dialogOpen`, `selectedItem`, `cloneFrom`, `deleteItem`, `deleteOpen`
3. Handlers: `handleEdit`, `handleClone`, `handleDeleteRow`, `handleCreate`
4. Hook: `const { handleDelete, handleBulkDelete, handleToggleActive } = useXxxDialogForm(null)`
5. Ghost column: Button Sửa + Button Xóa + DropdownMenu (Nhân bản + Toggle Active)
6. `ConfirmDialog` cho delete
