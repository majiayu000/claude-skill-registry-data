---
name: page-dialog-conventions
description: 'Quy tắc Page/Dialog/Component (`**/page/*.tsx`, `**/dialog/*.tsx`, `**/component/*.tsx`) trong SASUCO InvoiceEasy — maxWidth dialog, nút X, data-qa attribute. Dùng khi: tạo hoặc sửa file `.page.tsx` / `Dialog.tsx` / component UI.'
---

# Page / Dialog / Component Conventions — SASUCO InvoiceEasy

## Page — Quy Tắc

- **Không có business logic** trong file `.page.tsx` — chỉ orchestration
- Chỉ import hooks, components, dialogs — không import service hoặc apiCall
- Lazy load dialog khi cần, không import dialog không dùng
- Route được register trong `routeConfig.tsx` của portal tương ứng

## Dialog — Quy Tắc

- `maxWidth` prop là **BẮT BUỘC** — không chỉ dùng `className='max-w-...'`

| Kích thước | `maxWidth` | `className` |
|-----------|-----------|-------------|
| Hành động nhanh | `'400px'` | `'w-[400px] max-h-[90vh]'` |
| CRUD nhỏ-vừa | `'480px'` | `'w-[480px] max-h-[90vh]'` |
| CRUD mặc định | `'600px'` | `'w-[600px] max-h-[90vh] overflow-y-auto'` |
| Nhiều field | `'800px'` | `'w-[800px] max-h-[90vh]'` |
| Nhiều tab/cột | `'920px'` | `'w-[920px] max-h-[90vh]'` |

- **Nút X custom** góc trên phải: `variant='ghost'`, `data-qa='btn_dong_dialog'`, `aria-label='Đóng'` — BẮT BUỘC
- Ba mode: `view` / `create` / `edit` — footer buttons thay đổi theo mode
- Footer: nút phụ (`btn-secondary`) bên trái, nút chính (`btn-primary`) bên phải
- `disabled={saving}` cho cả nút submit và nút Hủy khi đang gọi API

## Component — Quy Tắc

- Nhận data qua props, emit action qua callback props
- Không có useState cho business state (chỉ UI state: hover, open...)
- Không gọi hook của feature parent trực tiếp — nhận qua props

## data-qa Attribute (BẮT BUỘC)

| Element | Pattern | Ví dụ |
|---------|---------|-------|
| Input text | `inp_{ten_field}` | `data-qa='inp_ten_san_pham'` |
| Button thêm mới | `btn_them_moi` | |
| Button lưu | `btn_luu` | |
| Button xóa row | `btn_xoa_{id}` | |
| Dropdown / ComboBox | `cbx_{ten_field}` | `data-qa='cbx_loai_san_pham'` |
| DatePicker | `dt_{ten_field}` | `data-qa='dt_ngay_hoa_don'` |

> UI chi tiết (buttons, icon classes, format): load skill `tao-ui-giao-dien`.
> Dialog: load skill `tao-ui-dialog`.
> Master page: load skill `tao-ui-master-page`.
