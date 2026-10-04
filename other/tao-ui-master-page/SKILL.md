---
name: tao-ui-master-page
description: 'Tạo Master Page. Cấu trúc: Header→Filters→Table→Pagination, cột Thao tác (Xem/Sửa/Nhân bản/Xóa), table header bg-[#f8f9fa], data-qa bắt buộc. Luôn load kèm tao-ui-giao-dien + filter-phan-trang.'
---

# Master Page

> Foundation: `tao-ui-giao-dien`. Logic: `filter-phan-trang`. Kiểm tra: `check-master-page.cjs`.

## Cấu Trúc: Header → Filters → Table → Pagination → Dialogs (ngoài CardContent)

### Header
```tsx
<div className='flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3'>
  <div><h1 className='text-xl font-semibold text-gray-900'>Tiêu đề</h1><p className='text-sm text-gray-500'>Mô tả</p></div>
  <div className='flex gap-2'>
    <Button data-qa='btn_lam_moi' className='btn-secondary' disabled={refreshing} onClick={refetch}>
      <RefreshCw className={cn('h-4 w-4', refreshing && 'animate-spin')} /> Làm mới</Button>
    <Button data-qa='btn_them_moi' className='btn-primary' onClick={openCreate}><Plus className='h-4 w-4' /> Thêm mới</Button>
  </div>
</div>
```

### Filters
```tsx
<div className='flex flex-wrap gap-3 items-end'>
  <Input data-qa='i_tim_kiem' className='flex-1 min-w-[200px]' placeholder='Tìm kiếm...' value={search} onChange={e => setSearch(e.target.value)} />
  {/* DatePicker: w-[150px], Select: w-[160-200px] */}
</div>
```

### Table
```tsx
<div className='overflow-x-auto'>
  <Table>
    <TableHeader className='bg-[#f8f9fa]'>
      <TableRow>
        <TableHead className='text-center w-[60px]'>STT</TableHead>
        <TableHead>Tên</TableHead>
        <TableHead className='text-right'>Số tiền</TableHead>
        <TableHead className='text-center w-[140px]'>Thao tác</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      {loading ? <PageLoader colSpan={4} /> :
       items.length === 0 ? <div className='py-12 text-center text-gray-500'>Không có dữ liệu</div> :
       items.map((item, i) => (
         <TableRow key={item.id} className='hover:bg-gray-50'>
           <TableCell className='text-center'>{startIndex + i + 1}</TableCell>
           <TableCell>{item.name}</TableCell>
           <TableCell className='text-right'>{formatCurrency(item.amount)}</TableCell>
           <TableCell>{/* ActionCell */}</TableCell>
         </TableRow>
       ))}
    </TableBody>
  </Table>
</div>
```

### Cột Thao Tác: Xem → Sửa → Nhân bản → Xóa (thứ tự cứng)

> **QUAN TRỌNG:** Không có cột "Thao tác" visible trong table. Action buttons hiện dạng overlay khi hover row, neo vào cột sticky phải `width=0` để luôn ở mép phải viewport.

**Pattern KetoanApp (DmTable) — header:**
```tsx
{/* Cột neo sticky phải — width=0, không hiển thị */}
<DmTableHead className='sticky right-0 z-30 bg-[#f0f2f6]' style={{ width: 0, minWidth: 0, padding: 0, border: 'none' }} />
```

**Pattern KetoanApp (DmTable) — body row:**
```tsx
{/* Cột neo sticky phải — width=0, action hiện khi hover row */}
<DmTableCell className='sticky right-0 z-20 bg-transparent' style={{ width: 0, minWidth: 0, padding: 0, border: 'none', overflow: 'visible' }}>
  <div className='absolute right-0 top-0 bottom-0 flex items-center opacity-0 group-hover:opacity-100 transition-opacity duration-150 bg-gradient-to-l from-white via-white/90 to-transparent pl-12 pr-2'>
    <DmRowActions actions={getRowActions(item)} />
  </div>
</DmTableCell>
```

**Pattern shadcn/ui Table:**
```tsx
<TableHead className='w-0 sticky right-0 z-20 bg-[#f8f9fa]' style={{ padding: 0, border: 'none' }} />
<TableCell className='sticky right-0 z-10 bg-transparent' style={{ width: 0, minWidth: 0, padding: 0, border: 'none', overflow: 'visible' }}>
  <div className='absolute right-0 top-0 bottom-0 flex items-center opacity-0 group-hover:opacity-100 transition-opacity duration-150 bg-gradient-to-l from-white via-white/90 to-transparent pl-12 pr-2'>
    <Button variant='ghost' size='sm' className='icon-primary' ...><Eye className='h-4 w-4'/></Button>
    ...
  </div>
</TableCell>
```

| Icon | Class | data-qa |
|------|-------|---------|
| `Eye` | `icon-primary` | `btn_xem_{id}` |
| `Pencil` | `icon-warning` | `btn_sua_{id}` |
| `Copy` | `icon-success` | `btn_nhan_ban_{id}` |
| `Trash2` | `icon-danger` | `btn_xoa_{id}` |

```tsx
<Button variant='ghost' size='sm' className='icon-primary' data-qa={`btn_xem_${id}`} title='Xem' onClick={view}><Eye className='h-4 w-4'/></Button>
<Button variant='ghost' size='sm' className='icon-warning' data-qa={`btn_sua_${id}`} title='Sửa' onClick={edit}><Pencil className='h-4 w-4'/></Button>
<Button variant='ghost' size='sm' className='icon-danger' data-qa={`btn_xoa_${id}`} title='Xóa' onClick={del}><Trash2 className='h-4 w-4'/></Button>
```
> Xóa **phải** qua `ConfirmDialog`, không gọi API trực tiếp. `variant='ghost' size='sm'` + `title`.

### Pagination & Dialogs
```tsx
<PagingUtils currentPage={} totalItems={} itemsPerPage={} onPageChange={} onItemsPerPageChange={} pageSizeOptions={[10,20,50,100]} />
{/* Dialogs NGOÀI CardContent */}
<ConfirmDialog open={delOpen} onConfirm={handleDelete} variant='destructive' />
```

---

## PAGE_ID + PAGE_FEATURES (BẮT BUỘC)

> **Mọi trang Master Page PHẢI khai báo `PAGE_ID` và `PAGE_FEATURES` để sơ đồ dự án và export menu permission hoạt động.**

```tsx
// Metadata cho so do du an
export const PAGE_ID = 'ten-page-id'  // phai khop navItem.id trong NavMenu
export const PAGE_FEATURES = [
  { label: 'Làm mới',         code: 'btn-refresh' },
  { label: 'Tạo mới...',      code: 'btn-create' },
  { label: 'Xem chi tiết',    code: 'row-view' },
  { label: 'Sửa',             code: 'row-edit' },
  { label: 'Xóa',             code: 'row-delete' },
]
// ---
```

- `PAGE_ID` phải khớp với `navItem.id` trong `NavMenu` portal tương ứng
- `PAGE_FEATURES` liệt kê TẤT CẢ các nút/thao tác thực tế có trong trang
- `code` prefix: `btn-` cho nút toolbar/header, `row-` cho action trên dòng, `batch-` cho thao tác hàng loạt
- Đặt ở đầu file, ngay trước `export function XxxPage()`
- Xem chi tiết tại `export-menu-page-permission/SKILL.md`

---

## Script
```bash
node .claude/skills/tao-ui-master-page/check-master-page.cjs src/modules/.../pages/XxxPage.tsx
node .claude/skills/tao-ui-master-page/check-master-page.cjs "src/modules/CrmApp/**/pages/*Page.tsx"
```
16 checks → JSON `summary.allPassed`. Exit 0=pass.
