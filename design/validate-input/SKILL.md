---
name: validate-input
description: 'Quy tắc validate form input client-side trong SASUCO InvoiceEasy. Dùng khi: validate form trước khi gọi API, hiển thị inline error, toast tổng hợp lỗi, progressive helper messages realtime, dùng validateAllFields/showValidationErrorsToast/getEmailProgressMessage/getPhoneProgressMessage/getTaxCodeProgressMessage/getPasswordProgressMessage, validate onBlur, border đỏ khi lỗi, border xanh khi hợp lệ.'
---

# Quy Tắc Validate Input (Client-side) — SASUCO InvoiceEasy

## Quy Trình 2 Giai Đoạn

| Giai đoạn | Thời điểm | Feedback | Action |
|-----------|----------|----------|--------|
| **Giai đoạn 1 — Client** | Trước API | Inline errors + Toast tổng hợp | Dừng, không gọi API |
| **Giai đoạn 2 — Server** | Sau API | `ValidationErrorDialog` | Xem skill `tich-hop-api-ui` |

---

## Shared Utilities — BẮT BUỘC (từ `/shared/utils`)

| Hàm | Dùng cho |
|-----|---------|
| `validateRequired()`, `validateEmail()`, `validatePhone()` | Validate từng field |
| `validateTaxCode()`, `validateMinLength()`, `validateMaxLength()` | Validate nâng cao |
| `validateAllFields()` | Validate nhiều fields cùng lúc → object errors |
| `hasAnyError()`, `getAllErrorMessages()` | Kiểm tra và lấy danh sách lỗi |
| `showValidationErrorsToast()` | Toast bullet-list, duration 5s |

> ❌ KHÔNG tự viết lại validator — cần validator mới → cập nhật `ValidationUtils.ts`

---

## 2 Bước Validate

### Bước 1 — Real-time (onBlur)
```typescript
const handleBlur = (field: string) => {
  setTouched(prev => ({ ...prev, [field]: true }))
  // validate field đó → update errors[field]
}
```

### Bước 2 — Gate-keeper (onSubmit)
```typescript
const handleSubmit = () => {
  const errors = validateAllFields({ /* tất cả fields */ })
  setTouched(Object.keys(formData).reduce((acc, k) => ({...acc, [k]: true}), {}))
  if (hasAnyError(errors)) {
    setErrors(errors)
    showValidationErrorsToast(getAllErrorMessages(errors))
    return  // DỪNG — không gọi API
  }
  // Tiếp tục gọi API
}
```

---

## Visual Feedback States

| State | Border | Icon | Message |
|-------|--------|------|---------|
| Chưa touched | default xám | — | — |
| Touched + Valid | `border-success` xanh | ✓ CheckCircle | `text-success` |
| Touched + Invalid | `border-destructive` đỏ | ✗ XCircle | `text-destructive` |

```tsx
<input
  className={cn('invoice-input', 
    touched.email && errors.email && 'border-destructive',
    touched.email && !errors.email && 'border-success'
  )}
  onBlur={() => handleBlur('email')}
/>
{touched.email && errors.email && (
  <p className='text-xs text-destructive flex items-center gap-1'>
    <AlertCircle className='h-3 w-3' />{errors.email}
  </p>
)}
```

---

## Progressive Helper Messages

Hiển thị feedback **realtime theo keystroke** — import từ `/shared/utils/MessageProgressHelper`:

| Helper | Field |
|--------|-------|
| `getEmailProgressMessage(value, touched)` | Email |
| `getPhoneProgressMessage(value, touched)` | Số điện thoại |
| `getTaxCodeProgressMessage(value, touched)` | MST |
| `getCitizenIdProgressMessage(value, touched)` | CCCD/CMND |
| `getUsernameProgressMessage(value, touched)` | Username |
| `getPasswordProgressMessage(value, touched)` | Password |
| `getConfirmPasswordProgressMessage(value, original, touched)` | Xác nhận mật khẩu |
| `getLengthProgressMessage(value, min, max, fieldName, touched)` | Field có giới hạn độ dài |
| `getBankAccountProgressMessage(value, touched)` | Số tài khoản |
| `getUrlProgressMessage(value, touched)` | URL |
| `getWebsiteProgressMessage(value, touched)` | Website |

**Quy tắc message rỗng:**
> Khi field trống (chưa nhập gì), `MessageProgressHelper` trả về message `''` (chuỗi rỗng).
> UI component **phải kiểm tra `&& progress.message`** trước khi render thẻ `<p>` — tránh DOM rỗng.
> Điều này áp dụng cho TẤT CẢ các hàm getXxxProgressMessage. Chỉ hiển thị message khi có nội dung thực sự.

**DmValidatedInput — Component dùng chung:**
> Cho email/phone/website, dùng `DmValidatedInput` (`@/modules/KetoanApp/components`) thay vì tự viết logic validate.
> Component tự xử lý `dirty` state nội bộ, border đổi màu, và progressive message.
> Xem `tao-ui-giao-dien-new` Section 3.1.1 để có pattern đầy đủ.

**Ánh xạ type → class Tailwind:**

| type | Message class | Border |
|------|--------------|--------|
| `info` | `text-muted-foreground` | default |
| `warning` | `text-warning` | default |
| `error` | `text-destructive` | `border-destructive` |
| `success` | `text-success` | `border-success` |

---

## Quy Tắc Cốt Lõi

- ✅ Validate toàn bộ fields cùng lúc khi submit (không validate từng field rồi return sớm)
- ✅ Dùng `showValidationErrorsToast()` — không dùng `toast.error()` đơn lẻ
- ❌ KHÔNG dùng HTML5 validation (`required`, `pattern`, `minlength`)
- ❌ KHÔNG dùng `ValidationErrorDialog` cho lỗi client

---

## Chuẩn Response Backend — Phát Hiện Vi Phạm

> Khi backend trả về response không đúng chuẩn → đó là **lỗi backend**, phải tạo bug để backend sửa.

### Chuẩn Response — Hành động (POST / PUT / DELETE)
```json
{
  "success": true | false,
  "data": <object> | null,
  "message": "Thông báo ngắn gọn hiển thị cho người dùng",
  "errorCode": "SNAKE_CASE_CODE_ĐỊNH_DANH",
  "errorDetails": null | <chi tiết kỹ thuật>
}
```

### Chuẩn Response — GET danh sách (phân trang)

`data` phải là object `PagingInfo<T>` với cấu trúc cố định:

```json
{
  "success": true,
  "data": {
    "items": [ /* mảng records */ ],
    "total": 100,
    "page": 1,
    "limit": 10,
    "totalPages": 10,
    "hasNext": true,
    "hasPrev": false
  },
  "message": null,
  "errorCode": null,
  "errorDetails": null
}
```

| Field | Kiểu | Mô tả |
|-------|------|-------|
| `items` | `T[]` | Danh sách records trang hiện tại |
| `total` | `number` | Tổng số records (TotalRecords) |
| `page` | `number` | Trang hiện tại (bắt đầu từ 1) |
| `limit` | `number` | Số items mỗi trang (PageSize) |
| `totalPages` | `number` | Tổng số trang |
| `hasNext` | `boolean` | Có trang tiếp theo |
| `hasPrev` | `boolean` | Có trang trước |

> ⚠️ **Phân biệt tham số request vs response:**  
> - Request gửi lên: `pageIndex` (trang hiện tại), `pageSize` (số items/trang)  
> - Response trả về: `page`, `limit` (không phải `pageIndex`/`pageSize`)

### Các vi phạm cần tạo bug Backend

| Vi phạm | Dấu hiệu phát hiện | Ví dụ sai |
|---------|-------------------|-----------|
| **message và errorCode lộn ngược** | `message` chứa mã code/debug text, `errorCode` chứa câu mô tả | `"message": "Mã thông điệp không tìm thấy: ..."`, `"errorCode": "Không có gói..."` |
| **errorCode không phải mã định danh** | `errorCode` là câu mô tả dạng text thay vì SCREAMING_SNAKE_CASE | `"errorCode": "Không có gói dịch vụ đang hoạt động."` |
| **HTTP status sai** | Lỗi nghiệp vụ trả 500, lỗi không tìm thấy trả 200 | Không có gói → 500 thay vì 404 |
| **message chứa nội dung debug** | Có dấu `:` chia thành 2 phần, phần đầu là text kỹ thuật | `"Mã thông điệp không tìm thấy: ..."` |
| **success=false nhưng data có giá trị** | `success: false` và `data` không null | Inconsistent state |
| **Phân trang thiếu field** | `data` không có đủ 7 fields: `items`, `total`, `page`, `limit`, `totalPages`, `hasNext`, `hasPrev` | `data` trả thẳng mảng `[]` hoặc thiếu `hasNext`/`hasPrev` |
| **Phân trang dùng sai tên field** | `data.pageIndex` thay vì `data.page`, `data.pageSize` thay vì `data.limit` | `{ pageIndex: 1, pageSize: 10 }` thay vì `{ page: 1, limit: 10 }` |
| **data là mảng thay vì PagingInfo** | `data` là `[...]` thay vì `{ items: [...], total, page, ... }` | Response GET danh sách trả `"data": [...]` |

### Quy tắc HTTP Status Code
| Tình huống nghiệp vụ | HTTP Status đúng |
|---------------------|-----------------|
| Không tìm thấy tài nguyên | `404 Not Found` |
| Dữ liệu đầu vào sai | `400 Bad Request` |
| Không có quyền | `403 Forbidden` |
| Lỗi server thực sự | `500 Internal Server Error` |
| Tạo thành công | `201 Created` |
| Cập nhật/xóa thành công | `200 OK` |

### Quy trình khi phát hiện vi phạm
1. **Xác nhận** bằng cách gọi API trực tiếp (qua browser fetch hoặc Playwright evaluate)
2. **Ghi lại** request/response đầy đủ làm evidence
3. **Tạo bug** bằng `mcp_kiemthu-mcp_create_bug` — không tự fix trên frontend
4. **KHÔNG** dùng `try/catch` hoặc logic đặc biệt để "che" lỗi backend — frontend phải xử lý đúng chuẩn, backend phải sửa

> ❌ KHÔNG tự ý map sai field để frontend hoạt động được khi backend trả sai
> ✅ Tạo bug → frontend hiển thị thông báo lỗi chung cho đến khi backend sửa

---


