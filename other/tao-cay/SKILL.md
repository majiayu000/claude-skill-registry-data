---
name: tao-cay
description: 'Chuyển đổi danh sách phẳng thành hiển thị dạng cây dựa trên parentId và grade. Rule: grade=1 thì font bold toàn hàng; grade≥2 thì cột đầu tiên lùi phải (grade-1)*INDENT, các cột khác giữ nguyên. Dùng khi: hiển thị danh sách đơn vị tổ chức dạng cây, combobox phân cấp, bảng dữ liệu có quan hệ cha-con.'
argument-hint: 'Mô tả dữ liệu cần chuyển sang cây. VD: Danh sách đơn vị tổ chức có field parentId + grade, hiển thị trong TableSearchCombobox với cột đầu là Mã đơn vị.'
---

# Chuyển Dữ Liệu Phẳng Sang Dạng Cây (`tao-cay`)

> **Áp dụng cho:** `TableSearchCombobox`, `DmTable`, bất kỳ danh sách phẳng nào có quan hệ cha-con.
> **Dữ liệu cần có:** `id`, `parentId` (null = root), `grade` (1 = gốc, 2/3... = cấp con).

---

## 0. Quy Tắc Hiển Thị Cây

| Grade | Kiểu hàng | Cột đầu tiên | Các cột còn lại |
|-------|-----------|-------------|-----------------|
| **1** | **Font bold toàn hàng** | Giữ nguyên | Giữ nguyên |
| **≥ 2** | Font thường | **Lùi phải** `(grade - 1) × INDENT_PX` | Giữ nguyên |

> **INDENT_PX** = 20px (mặc định). Có thể điều chỉnh theo ngữ cảnh.

---

## 1. Pattern Cho `TableSearchCombobox`

`TableSearchCombobox` không hỗ trợ CSS per-row, nhưng có thể giả lập visual cây qua text:

### 1.1 Indent cột đầu tiên (code)

Dùng non-breaking space `\u00A0` lặp `(grade - 1) × 4` lần trước giá trị `code`:

```typescript
const INDENT = '\u00A0\u00A0\u00A0\u00A0' // 4 non-breaking spaces = ~1 level
const indentCode = INDENT.repeat((item.grade ?? 1) - 1) + item.code
```

### 1.2 Bold cho grade = 1

Trong combobox dùng **Unicode bold** cho toàn bộ text (cả code và name):

```typescript
function toBold(s: string): string {
  const boldMap: Record<string, string> = {
    '0':'𝟬','1':'𝟭','2':'𝟮','3':'𝟯','4':'𝟰','5':'𝟱','6':'𝟲','7':'𝟳','8':'𝟴','9':'𝟵',
    'A':'𝗔','B':'𝗕','C':'𝗖','D':'𝗗','E':'𝗘','F':'𝗙','G':'𝗚','H':'𝗛','I':'𝗜','J':'𝗝',
    'K':'𝗞','L':'𝗟','M':'𝗠','N':'𝗡','O':'𝗢','P':'𝗣','Q':'𝗤','R':'𝗥','S':'𝗦','T':'𝗧',
    'U':'𝗨','V':'𝗩','W':'𝗪','X':'𝗫','Y':'𝗬','Z':'𝗭',
    'a':'𝗮','b':'𝗯','c':'𝗰','d':'𝗱','e':'𝗲','f':'𝗳','g':'𝗴','h':'𝗵','i':'𝗶','j':'𝗷',
    'k':'𝗸','l':'𝗹','m':'𝗺','n':'𝗻','o':'𝗼','p':'𝗽','q':'𝗾','r':'𝗿','s':'𝘀','t':'𝘁',
    'u':'𝘂','v':'𝘃','w':'𝘄','x':'𝘅','y':'𝘆','z':'𝘇',
    'À':'𝗔̀','Á':'𝗔́','Â':'𝗔̂','Ã':'𝗔̃','È':'𝗘̀','É':'𝗘́','Ê':'𝗘̂',
    'Ì':'𝗜̀','Í':'𝗜́','Ò':'𝗢̀','Ó':'𝗢́','Ô':'𝗢̂','Õ':'𝗢̃',
    'Ù':'𝗨̀','Ú':'𝗨́','Ỳ':'𝗬̀','Ý':'𝗬́',
    'à':'𝗮̀','á':'𝗮́','â':'𝗮̂','ã':'𝗮̃','è':'𝗲̀','é':'𝗲́','ê':'𝗲̂',
    'ì':'𝗶̀','í':'𝗶́','ò':'𝗼̀','ó':'𝗼́','ô':'𝗼̂','õ':'𝗼̃',
    'ù':'𝘂̀','ú':'𝘂́','ỳ':'𝘆̀','ý':'𝘆́',
    'Đ':'𝗗','đ':'𝗱','Ă':'𝗔','ă':'𝗮','Ư':'𝗨','ư':'𝘂',
    'Ơ':'𝗢','ơ':'𝗼','Ạ':'𝗔̣','ạ':'𝗮̣','Ả':'𝗔̉','ả':'𝗮̉',
    'Ấ':'𝗔̂́','ấ':'𝗮̂́','Ầ':'𝗔̂̀','ầ':'𝗮̂̀','Ẩ':'𝗔̂̉','ẩ':'𝗮̂̉',
    'Ẫ':'𝗔̂̃','ẫ':'𝗮̂̃','Ậ':'𝗔̣̂','ậ':'𝗮̣̂',
    'Ắ':'𝗔̆́','ắ':'𝗮̆́','Ằ':'𝗔̆̀','ằ':'𝗮̆̀','Ẳ':'𝗔̆̉','ẳ':'𝗮̆̉',
    'Ẵ':'𝗔̆̃','ẵ':'𝗮̆̃','Ặ':'𝗔̣̆','ặ':'𝗮̣̆',
    'Ẻ':'𝗘̉','ẻ':'𝗲̉','Ẽ':'𝗘̃','ẽ':'𝗲̃','Ẹ':'𝗘̣','ẹ':'𝗲̣','Ế':'𝗘̂́','ế':'𝗲̂́',
    'Ề':'𝗘̂̀','ề':'𝗲̂̀','Ể':'𝗘̂̉','ể':'𝗲̂̉','Ễ':'𝗘̂̃','ễ':'𝗲̂̃','Ệ':'𝗘̣̂','ệ':'𝗲̣̂',
    'Ỉ':'𝗜̉','ỉ':'𝗶̉','Ĩ':'𝗜̃','ĩ':'𝗶̃','Ị':'𝗜̣','ị':'𝗶̣',
    'Ỏ':'𝗢̉','ỏ':'𝗼̉','Ọ':'𝗢̣','ọ':'𝗼̣','Ố':'𝗢̂́','ố':'𝗼̂́','Ồ':'𝗢̂̀','ồ':'𝗼̂̀',
    'Ổ':'𝗢̂̉','ổ':'𝗼̂̉','Ỗ':'𝗢̂̃','ỗ':'𝗼̂̃','Ộ':'𝗢̣̂','ộ':'𝗼̣̂',
    'Ớ':'𝗢́','ớ':'𝗼́','Ờ':'𝗢̀','ờ':'𝗼̀','Ở':'𝗢̉','ở':'𝗼̉','Ỡ':'𝗢̃','ỡ':'𝗼̃','Ợ':'𝗢̣','ợ':'𝗼̣',
    'Ủ':'𝗨̉','ủ':'𝘂̉','Ũ':'𝗨̃','ũ':'𝘂̃','Ụ':'𝗨̣','ụ':'𝘂̣',
    'Ứ':'𝗨́','ứ':'𝘂́','Ừ':'𝗨̀','ừ':'𝘂̀','Ử':'𝗨̉','ử':'𝘂̉','Ữ':'𝗨̃','ữ':'𝘂̃','Ự':'𝗨̣','ự':'𝘂̣',
    ' ': ' ', '-':'-', '.':'.', ',':',', '/':'/', '(':'(', ')':')',
  }
  return s.split('').map(c => boldMap[c] ?? c).join('')
}
```

> ⚠️ Nếu quá nhiều ký tự tiếng Việt → chỉ bold phần code (mã), không bold name.

### 1.3 Code hoàn chỉnh cho `loadOptions` trong TableSearchCombobox

```typescript
const INDENT = '\u00A0\u00A0\u00A0\u00A0'

const loadTreeOptions = useCallback(async (keyword: string): Promise<TableComboboxRow[]> => {
  // 1. Lấy toàn bộ dữ liệu (hoặc đủ lớn)
  const r = await ApiService.getAll()
  const allItems = r.data?.items ?? []

  // 2. Lọc theo keyword
  const kw = (keyword ?? '').toLowerCase().trim()
  const filtered = kw
    ? allItems.filter(o => (o.code ?? '').toLowerCase().includes(kw) || (o.name ?? '').toLowerCase().includes(kw))
    : allItems

  // 3. Nhóm theo parentId
  const childrenMap = new Map<string | null, typeof allItems>()
  for (const o of filtered) {
    const pk = o.parentId ?? null
    if (!childrenMap.has(pk)) childrenMap.set(pk, [])
    childrenMap.get(pk)!.push(o)
  }

  // 4. Sắp xếp theo grade
  for (const [, group] of childrenMap) {
    group.sort((a, b) => (a.grade ?? 99) - (b.grade ?? 99))
  }

  // 5. Flatten — ÁP DỤNG QUY TẮC CÂY
  const result: TableComboboxRow[] = []
  const visited = new Set<string>()

  function flatten(nodes: typeof allItems, ancestorsLast: boolean[]) {
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i]
      if (visited.has(node.id)) continue
      visited.add(node.id)

      const g = node.grade ?? 1
      const isGrade1 = g === 1

      // Áp dụng indent cột đầu tiên (code) theo grade
      const indentCode = INDENT.repeat(g - 1) + (node.code ?? '')

      // Áp dụng bold cho grade 1
      const displayCode = isGrade1 ? toBold(indentCode.trim()) : indentCode
      const displayName = isGrade1 ? toBold(node.name ?? '') : (node.name ?? '')

      result.push({
        value: node.id,
        cells: { code: displayCode, name: displayName },
      })

      const childNodes = childrenMap.get(node.id)
      if (childNodes && childNodes.length > 0) {
        flatten(childNodes, [...ancestorsLast, i === nodes.length - 1])
      }
    }
  }

  const roots = childrenMap.get(null) ?? []
  flatten(roots, [])

  // Node mồ côi
  for (const o of filtered) {
    if (!visited.has(o.id)) flatten([o], [])
  }

  return result
}, [])
```

---

## 2. Pattern Cho `DmTable` (Có Expand/Collapse)

### 2.1 Import icon

```typescript
import { SquareMinus, SquarePlus } from 'lucide-react'
```

> Dùng `SquarePlus` / `SquareMinus` thay vì `ChevronRight` / `ChevronDown`.
> `SquarePlus` ⊞ = đang đóng, `SquareMinus` ⊟ = đang mở.

### 2.2 State expand + toggle

```typescript
const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set())

// Khởi tạo tất cả group mở khi load data lần đầu
const groupsInitialized = useRef(false)
useEffect(() => {
  if (treeNodes.length === 0 || groupsInitialized.current) return
  setExpandedIds(new Set(treeNodes.map(n => n.id)))
  groupsInitialized.current = true
}, [treeNodes])

const toggleExpand = useCallback((id: string) => {
  setExpandedIds(prev => {
    const next = new Set(prev)
    if (next.has(id)) next.delete(id)
    else next.add(id)
    return next
  })
}, [])
```

### 2.3 Render hàng trong bảng

```tsx
// Trong render row:
const isGrade1 = (item.grade ?? 1) === 1
const indentPx = ((item.grade ?? 1) - 1) * 20
const hasChildren = (item.children?.length ?? 0) > 0
const expanded = expandedIds.has(item.id)

<DmTableRow className={isGrade1 ? 'font-bold' : ''}>
  <DmTableCell className='text-center'>
    {hasChildren ? (
      <button onClick={() => toggleExpand(item.id)}>
        {expanded ? <SquareMinus className='h-4 w-4' /> : <SquarePlus className='h-4 w-4' />}
      </button>
    ) : null}
  </DmTableCell>
  <DmTableCell style={{ paddingLeft: indentPx }}>{item.code}</DmTableCell>
  <DmTableCell>{item.name}</DmTableCell>
</DmTableRow>
```

### 2.4 Toggle mở/đóng tất cả (nút trên toolbar)

```tsx
// Import thêm: SquareMinus, SquarePlus (đã import ở 2.1)

const allExpanded = treeNodes.length > 0 && treeNodes.every(n => expandedIds.has(n.id))

const toggleAll = useCallback(() => {
  if (allExpanded) {
    setExpandedIds(new Set())
  } else {
    setExpandedIds(new Set(treeNodes.map(n => n.id)))
  }
}, [allExpanded, treeNodes])

// Trong toolbar:
<Button onClick={toggleAll} title={allExpanded ? 'Thu gọn tất cả' : 'Mở rộng tất cả'}>
  {allExpanded ? <SquareMinus className='h-4 w-4' /> : <SquarePlus className='h-4 w-4' />}
</Button>
```

### 2.5 Pattern cũ: Bảng phẳng không expand (grade hiển thị indent)

Khi **không có** tính năng expand/collapse, chỉ hiển thị indent theo grade:

```tsx
const isGrade1 = (item.grade ?? 1) === 1
const indentPx = ((item.grade ?? 1) - 1) * 20

<DmTableRow className={isGrade1 ? 'font-bold' : ''}>
  <DmTableCell style={{ paddingLeft: indentPx }}>{item.code}</DmTableCell>
  <DmTableCell>{item.name}</DmTableCell>
</DmTableRow>
```

---

## 3. Cấu Trúc Dữ Liệu Yêu Cầu

```typescript
interface TreeNode {
  id: string
  code: string
  name: string
  parentId: string | null   // null = root
  grade?: number             // 1 = gốc, 2/3... = cấp con
}
```

---

## 4. Checklist Áp Dụng

- [ ] Kiểm tra DTO có field `parentId` và `grade` không
- [ ] Dùng `getAll()` (pageSize lớn) thay vì `list()` để có đủ dữ liệu dựng cây
- [ ] Áp dụng `INDENT.repeat(grade - 1)` cho cột đầu tiên
- [ ] Áp dụng `toBold()` cho grade = 1
- [ ] Sắp xếp theo `grade` trong mỗi nhóm
- [ ] Nếu có expand/collapse → dùng `SquarePlus` ⊞ / `SquareMinus` ⊟ từ `lucide-react` (KHÔNG dùng `ChevronRight`/`ChevronDown`)
- [ ] Khởi tạo `expandedIds` bằng `useRef` flag để chỉ set 1 lần, tránh re-render liên tục ghi đè user action
