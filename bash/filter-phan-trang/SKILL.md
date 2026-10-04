---
name: filter-phan-trang
description: 'Quy tắc filter và phân trang cho trang danh sách. Dùng khi: tạo trang list có search/filter/pagination, server-side pagination, useDebounce 800ms, PagingUtils component, sessionStorage currentPage, localStorage pageSize, reset page=1 khi filter đổi, nút Làm mới.'
---

# Filter & Phân Trang

## Kiến Trúc: Page → Hook → API Service

## Phân Loại
| Loại | Khi dùng | Dấu hiệu |
|------|----------|----------|
| Server-side (ưu tiên) | Backend hỗ trợ | API có `page`/`limit`, response có `total` |
| Client-side (tạm thời) | Dataset < 50 | API trả thẳng `data: []` |

## Cơ Chế Filter
- **State:** `{ status, searchTerm, dateFrom, dateTo, page, limit }`
- **Khi filter đổi →** reset `page=1`, clear `currentPage` sessionStorage, trigger API
- **Debounce searchTerm:** 800ms qua `useDebounce` từ `@/shared/hooks/useDebounce`

## Storage
- `sessionStorage`: `'{featureName}.currentPage'` — giữ trang hiện tại
- `localStorage`: `'app_page_size'` — PagingUtils tự quản lý

```ts
import { getPageSizeFromStorage } from '@/shared/utils/PagingUtils';
const [itemsPerPage] = useState(() => getPageSizeFromStorage(10));
```

## Pagination Component — BẮT BUỘC
```tsx
import { PagingUtils } from '@/shared/utils'; // hoặc '@/shared/utils/PagingUtils'

<PagingUtils currentPage={} totalItems={} itemsPerPage={} onPageChange={} onItemsPerPageChange={} />
```

## Nút Làm Mới (Refresh)
```tsx
<Button variant='outline' onClick={onRefresh} disabled={refreshing}>
  <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
  {refreshing ? 'Đang tải...' : 'Làm mới'}
</Button>
```
- ✅ Reset page=1, giữ filter + limit
- ❌ KHÔNG reset filter về default, KHÔNG gọi API trực tiếp

## Page Change
```ts
handlePageChange = (p) => { setCurrentPage(p); setFilters(prev=>({...prev,page:p})); saveToStorage(p); }
handleItemsPerPageChange = (s) => { setItemsPerPage(s); setCurrentPage(1); setFilters(prev=>({...prev,limit:s,page:1})); clearStorage(); }
```

## useEffect Dependencies
```ts
useEffect(() => { fetchData(); }, [
  debouncedSearchTerm,  // ✅ debounced, KHÔNG dùng filters.searchTerm
  filters.status, filters.dateFrom, filters.dateTo, filters.page, filters.limit
]);
```

## Anti-Patterns
- ❌ Tự viết button pagination thủ công
- ❌ Dùng `Pagination` từ MUI, AntD, Bootstrap
- ✅ Luôn dùng `<PagingUtils>`

## Page Size
- Default: `10`, Options: `[10, 20, 50, 100]`

---

## Script Kiểm Tra

```bash
# 1 page (auto-detect hook cùng feature)
node .claude/skills/filter-phan-trang/check-pagination.cjs src/modules/.../pages/XxxPage.tsx

# Nhiều page
node .claude/skills/filter-phan-trang/check-pagination.cjs "src/modules/CrmApp/**/pages/*Page.tsx"
```

12 checks: `pagingUtilsImport`(err), `noExternalPagination`(err), `noCustomPagination`(err), `getPageSizeFromStorage`(warn), `useDebounceForSearch`(warn), `sessionStoragePage`(warn), `resetPageOnFilterChange`(err), `refreshButton`(info), `refreshResetsPage`(info), `debouncedInUseEffect`(err), `pageSizeLocalStorage`(info), `pageSizeOptions`(info).

Output JSON → `summary.allPassed`. Exit 0 = pass, 1 = có lỗi.
