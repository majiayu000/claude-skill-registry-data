---
name: test-field-update
description: 'Test tự động các field trên UI: kiểm tra field có update OK không sau khi lưu, nếu lỗi thì báo cáo nguyên nhân chi tiết. Dùng khi: cần verify form CRUD hoạt động đúng, test field sau khi sửa dialog, regression test form, kiểm tra dữ liệu lưu xuống BE có khớp với dữ liệu nhập trên UI không, phát hiện field mapping sai giữa FE và BE.'
argument-hint: 'Mô tả form/dialog cần test. VD: test dialog Nhân viên, kiểm tra form Khách hàng, verify dialog Kho...'
---

# Test Tự Động Field Update Trên UI — SASUCO Invoice

> **Mục tiêu:** Dùng Playwright + browser tools mở form/dialog trên `localhost:3000`, quét toàn bộ fields, fill dữ liệu test, bấm Lưu/Cập nhật, đọc lại dữ liệu sau lưu → so sánh → báo cáo field nào OK, field nào lỗi + nguyên nhân.

---

## 🎯 Tổng Quan Quy Trình

```
[1] Mở browser → Login → Navigate đến màn hình
[2] Mở dialog (Thêm / Sửa) → Quét toàn bộ fields
[3] Fill dữ liệu test cho từng field → Bấm Lưu
[4] Mở lại dialog (Sửa) → Đọc giá trị hiện tại của từng field
[5] So sánh giá trị đã fill vs giá trị sau lưu → Báo cáo
```

---

## 🔑 Thông Tin Đăng Nhập Mặc Định

| Field | Giá trị |
|-------|--------|
| **URL** | `http://localhost:3000` |
| **Username** | `0985908750` |
| **Password** | `Hoadon@2022!#` |

> Nếu user cung cấp credentials khác → dùng credentials đó. Mặc định dùng credentials trên.

---

## 📋 Cấu Trúc Đầu Vào

Người dùng cung cấp **tối thiểu**:

| Thông tin | Bắt buộc | Mô tả | Ví dụ |
|-----------|----------|-------|-------|
| **Tên form/dialog** | ✅ | Form cần test | `Nhân viên`, `Khách hàng`, `Kho` |
| **Route màn hình** | ✅ | Hash route của trang | `#/ketoan/nhan-vien` |
| **Loại form** | ⚠️ | `dialog` (mặc định) hoặc `sub-page` | `dialog` |
| **Portal** | ⚠️ | `KetoanHKD` (mặc định), `BaseIndex`, `Invoice`... | `KetoanHKD` |
| **Mode test** | ⚠️ | `create` (mặc định), `update`, hoặc `both` | `both` |

---

## 🚀 Các Bước Thực Hiện

### Bước 0 — Xác Định Phạm Vi

1. **Load skill `xac-dinh-pham-vi`** để tìm route, page component, dialog component, hook
2. Xác định file dialog cần test (dựa trên tên form người dùng cung cấp)
3. Đọc dialog file để biết cấu trúc fields

### Bước 1 — Mở Browser & Đăng Nhập

Dùng **cùng browser đang mở** (tab `localhost:3000`) — KHÔNG mở browser mới. Nếu chưa có page, mở page mới.

```ts
// Nếu đã có page (kiểm tra từ context)
const page = existingPage; // Từ browser context có sẵn

// Navigate đến màn hình
await page.goto('http://localhost:3000/#/ketoan/nhan-vien');
await page.waitForTimeout(800);
```

Nếu page đang ở màn hình login → tự động login:
```ts
if (page.url().includes('login') || await page.locator('input[type="password"]').isVisible({ timeout: 2000 }).catch(() => false)) {
  await page.locator('input[placeholder*="0123456789"]').first().fill('0985908750');
  await page.locator('input[type="password"]').first().fill('Hoadon@2022!#');
  await page.getByRole('button', { name: /Đăng nhập/i }).click();
  await page.waitForTimeout(2500);
}
```

### Bước 2 — Mở Dialog & Quét Fields

```ts
// Bấm nút Thêm mới
await page.locator('[data-qa="btn_them_moi"]').click();
// fallback: tìm button có text "Thêm"
await page.getByRole('button', { name: /Thêm/i }).click();
await page.waitForTimeout(500);

// Quét tất cả fields trong dialog
const fields = await page.evaluate(() => {
  const dialog = document.querySelector('[role="dialog"], .dialog, [data-sonner-toaster]')?.parentElement?.querySelector('[role="dialog"]');
  const scope = dialog || document;
  
  const inputs = scope.querySelectorAll('input:not([type="hidden"]):not([type="checkbox"]):not([type="radio"]), textarea, select, [role="combobox"], [role="listbox"]');
  
  return Array.from(inputs).map(el => {
    const rect = el.getBoundingClientRect();
    if (rect.width < 20 || rect.height < 20) return null;
    
    const dataQa = el.getAttribute('data-qa') || '';
    const name = (el as HTMLInputElement).name || '';
    const id = el.id || '';
    const placeholder = (el as HTMLInputElement).placeholder || '';
    const type = (el as HTMLInputElement).type || el.tagName.toLowerCase();
    const tag = el.tagName.toLowerCase();
    const role = el.getAttribute('role') || '';
    const value = (el as HTMLInputElement).value || '';
    const disabled = el.hasAttribute('disabled');
    const readOnly = el.hasAttribute('readonly');
    
    // Tìm label gần nhất
    let label = '';
    if (id) {
      const lbl = scope.querySelector(`label[for="${id}"]`);
      if (lbl) label = lbl.textContent?.trim() || '';
    }
    
    return { dataQa, name, id, type, tag, role, placeholder, label, disabled, readOnly, value, y: Math.round(rect.top), x: Math.round(rect.left) };
  }).filter(Boolean).sort((a, b) => a.y - b.y || a.x - b.x);
});

console.log(`🔍 Tìm thấy ${fields.length} fields:`, fields.map(f => `${f.dataQa || f.name || f.id} [${f.type}]`));
```

> **Quan trọng:** Nếu field có `data-qa` → dùng `data-qa` làm locator chính. Nếu không có → dùng `name` hoặc `placeholder` và **báo cáo thiếu `data-qa`**.

### Bước 3 — Fill Dữ Liệu Test & Lưu

Với mỗi field, fill dữ liệu test **theo loại field**:

| Loại field | Cách fill | Dữ liệu test mặc định |
|------------|-----------|----------------------|
| `input[type="text"]` (mã) | `.fill()` | `TEST-${Date.now()}` |
| `input[type="text"]` (tên) | `.fill()` | `Test Tự Động ${counter}` |
| `input[type="number"]` | `.fill()` | `12345` |
| `input[type="email"]` | `.fill()` | `test@example.com` |
| `input[type="tel"]` / phone | `.fill()` | `0987654321` |
| `textarea` | `.fill()` | `Mô tả test tự động` |
| `[role="combobox"]` (SearchCombobox) | Click → chọn item đầu tiên | — |
| `select` | `.selectOption()` chọn option đầu tiên | — |
| `input[date]` / DatePicker | `.fill()` | `01/01/2025` (dd/MM/yyyy) |
| `input[type="checkbox"]` | `.check()` | `true` |
| Số điện thoại | `.fill()` | `0987654321` |
| Email | `.fill()` | `test-auto@example.com` |
| MST | `.fill()` | `0123456789` |
| Số tài khoản | `.fill()` | `1234567890` |
| URL / Link | `.fill()` | `https://example.com` |

```ts
// Lưu lại dữ liệu đã fill để so sánh sau
const filledData: Record<string, string> = {};

for (const field of fields) {
  if (field.disabled || field.readOnly) continue;
  
  const locator = field.dataQa 
    ? page.locator(`[data-qa="${field.dataQa}"]`)
    : field.name 
      ? page.locator(`[name="${field.name}"]`) 
      : page.locator(`#${field.id}`);
  
  const testValue = generateTestValue(field);
  
  if (field.role === 'combobox' || field.tag === 'select') {
    // Với combobox: click mở → chọn item
    await locator.click();
    await page.waitForTimeout(300);
    await page.locator('[role="option"]').first().click();
    await page.waitForTimeout(200);
    // Lấy text đã chọn
    const selectedText = await locator.textContent();
    filledData[field.dataQa || field.name || field.id] = selectedText?.trim() || '';
  } else {
    await locator.fill(testValue);
    filledData[field.dataQa || field.name || field.id] = testValue;
  }
}

// Bấm Lưu
await page.locator('[data-qa="btn_luu"]').click();
// fallback
await page.getByRole('button', { name: /Lưu|Cất|Lưu lại/i }).click();
await page.waitForTimeout(1500);
```

### Bước 4 — Đọc Lại Dữ Liệu Sau Lưu

```ts
// Sau khi lưu → tìm bản ghi vừa tạo → bấm Sửa
// Cách 1: Tìm theo mã vừa tạo (nếu có field mã)
const maField = Object.keys(filledData).find(k => k.includes('ma') || k.includes('code'));
if (maField) {
  await page.locator('[data-qa="i_keyword"]').fill(filledData[maField]);
  await page.locator('[data-qa="btn_tim_kiem"]').click();
  await page.waitForTimeout(1000);
}

// Bấm nút Sửa trên dòng đầu tiên
await page.locator('[data-qa="btn_sua"]').first().click();
// fallback: click icon sửa
await page.locator('.icon-primary, [data-qa="btn_sua"]').first().click();
await page.waitForTimeout(500);

// Đọc lại giá trị từng field
const savedData: Record<string, string> = {};
for (const field of fields) {
  if (field.disabled || field.readOnly) continue;
  
  const locator = field.dataQa 
    ? page.locator(`[data-qa="${field.dataQa}"]`)
    : field.name 
      ? page.locator(`[name="${field.name}"]`) 
      : page.locator(`#${field.id}`);
  
  const key = field.dataQa || field.name || field.id;
  
  if (field.role === 'combobox') {
    savedData[key] = (await locator.textContent())?.trim() || '';
  } else {
    savedData[key] = (await locator.inputValue()) || '';
  }
}
```

### Bước 5 — So Sánh & Báo Cáo

```ts
// So sánh filledData vs savedData
const results: { field: string; expected: string; actual: string; ok: boolean; note: string }[] = [];

for (const [key, expectedValue] of Object.entries(filledData)) {
  const actualValue = savedData[key] || '(không đọc được)';
  const ok = normalizeForCompare(actualValue) === normalizeForCompare(expectedValue);
  
  results.push({
    field: key,
    expected: expectedValue,
    actual: actualValue,
    ok,
    note: ok ? '✅ OK' : getFailReason(key, expectedValue, actualValue),
  });
}

// In báo cáo
console.log('\n📊 KẾT QUẢ TEST FIELD UPDATE');
console.log('═'.repeat(60));
const okCount = results.filter(r => r.ok).length;
const failCount = results.filter(r => !r.ok).length;
console.log(`✅ OK: ${okCount}  ❌ LỖI: ${failCount}  📋 Tổng: ${results.length}`);
console.log('─'.repeat(60));

for (const r of results) {
  console.log(`${r.ok ? '✅' : '❌'} ${r.field}`);
  if (!r.ok) {
    console.log(`   Mong đợi: "${r.expected}"`);
    console.log(`   Thực tế:  "${r.actual}"`);
    console.log(`   Lý do:    ${r.note}`);
  }
}
```

---

## 📊 Phân Loại Lỗi & Nguyên Nhân

| Loại lỗi | Dấu hiệu | Nguyên nhân | Hành động |
|----------|---------|-------------|-----------|
| **Field không map với BE** | Fill xong → mở lại → giá trị rỗng | Thiếu `name` attribute, sai field name trong payload API | Kiểm tra API payload → sửa field mapping |
| **Sai kiểu dữ liệu** | Fill số → lưu thành text hoặc ngược lại | FE gửi sai type (string vs number) | Kiểm tra type trong types.ts |
| **Combobox không lưu** | Chọn item → mở lại → rỗng | FK không được gửi đúng field (thường gửi name thay vì id) | Kiểm tra `SearchCombobox` onChange handler |
| **Date sai format** | Fill `01/01/2025` → lưu thành null hoặc sai | FE gửi dd/MM/yyyy thay vì yyyy-MM-dd | Kiểm tra format trong hook submit |
| **Field bị disabled sau lưu** | Field ở chế độ readOnly, không fill được | Logic mode View/Create/Edit sai | Kiểm tra `isViewMode` trong dialog |
| **Mất dữ liệu Unicode** | Fill tiếng Việt → lưu thành ??? hoặc méo | Encoding issue hoặc BE không hỗ trợ UTF-8 | Báo bug BE |
| **Validate sai** | Fill đúng → vẫn báo lỗi validate | Regex validate quá chặt hoặc sai logic | Sửa validate rule |
| **Trường không có data-qa** | Không tìm được locator ổn định | Component thiếu `data-qa` attribute | Thêm `data-qa` vào JSX |

---

## 🛠 Hàm Helper

```ts
/** Sinh dữ liệu test theo loại field */
function generateTestValue(field: any): string {
  const label = (field.label || '').toLowerCase();
  const name = (field.name || '').toLowerCase();
  const dataQa = (field.dataQa || '').toLowerCase();
  
  if (label.includes('email') || name.includes('email') || dataQa.includes('email'))
    return 'test-auto@example.com';
  if (label.includes('điện thoại') || label.includes('sđt') || label.includes('phone') || name.includes('phone') || dataQa.includes('phone'))
    return '0987654321';
  if (label.includes('mst') || label.includes('mã số thuế') || name.includes('tax') || dataQa.includes('tax'))
    return '0123456789';
  if (label.includes('số tài khoản') || name.includes('account') || dataQa.includes('account'))
    return '1234567890';
  if (field.type === 'number')
    return '12345';
  if (label.includes('mã') || name.includes('code') || dataQa.includes('ma'))
    return `TEST-${Date.now().toString(36).toUpperCase()}`;
  if (label.includes('tên') || name.includes('name') || dataQa.includes('ten'))
    return `Test Tự Động ${Math.floor(Math.random() * 1000)}`;
  if (label.includes('địa chỉ') || name.includes('address') || dataQa.includes('dia_chi'))
    return '123 Đường Test, Quận 1, TP.HCM';
  if (label.includes('mô tả') || label.includes('ghi chú') || name.includes('description') || dataQa.includes('mo_ta'))
    return 'Mô tả test tự động - kiểm tra field update';
  if (label.includes('link') || label.includes('url') || label.includes('website'))
    return 'https://example.com';
  if (field.type === 'email')
    return 'test-auto@example.com';
  if (field.type === 'tel')
    return '0987654321';
  
  return `Test-${Date.now().toString(36).toUpperCase()}`;
}

/** Chuẩn hóa để so sánh */
function normalizeForCompare(value: string): string {
  return value
    .replace(/\s+/g, ' ')
    .replace(/[–—−]/g, '-')  // các loại dấu gạch
    .trim()
    .toLowerCase();
}

/** Phân tích lý do fail */
function getFailReason(key: string, expected: string, actual: string): string {
  if (!actual || actual === '(không đọc được)')
    return 'Giá trị trả về rỗng → field có thể không được map với BE hoặc không có trong API response';
  if (expected.length !== actual.length)
    return `Độ dài khác nhau (mong đợi ${expected.length} ký tự, thực tế ${actual.length} ký tự) → có thể bị truncate`;
  if (normalizeForCompare(expected.replace(/[0-9]/g, '')) === normalizeForCompare(actual.replace(/[0-9]/g, '')))
    return 'Chỉ khác số → có thể định dạng số (dấu phân cách, số thập phân) bị thay đổi khi lưu';
  if (actual.includes('??') || actual.includes('�'))
    return 'Lỗi encoding Unicode → BE không hỗ trợ UTF-8 hoặc bị double-encode';
  return 'Giá trị khác biệt → kiểm tra mapping FE-BE, format, hoặc transform logic trong hook';
}
```

---

## 📝 Báo Cáo Kết Quả

Kết quả test được in ra console theo format:

```
📊 KẾT QUẢ TEST FIELD UPDATE — DIALOG: Nhân viên
══════════════════════════════════════════════════════════
✅ OK: 8  ❌ LỖI: 2  📋 Tổng: 10
──────────────────────────────────────────────────────────
✅ i_ma_nhan_vien
✅ i_ten_nhan_vien
❌ i_email
   Mong đợi: "test-auto@example.com"
   Thực tế:  ""
   Lý do:    Giá trị trả về rỗng → field có thể không được map với BE
❌ sel_chuc_vu
   Mong đợi: "Quản lý"
   Thực tế:  "(không đọc được)"
   Lý do:    Giá trị trả về rỗng → field có thể không được map với BE
✅ i_so_dien_thoai
...
──────────────────────────────────────────────────────────
🔧 HÀNH ĐỘNG ĐỀ XUẤT:
  1. i_email: Kiểm tra field 'email' trong payload API POST/PUT
  2. sel_chuc_vu: Kiểm tra FK 'chucVuId' trong payload
```

---

## ⚠️ Quy Tắc Quan Trọng

1. **Dùng browser tool có sẵn** (tab `localhost:3000` đang mở) — KHÔNG mở browser mới
2. **KHÔNG tạo file `.spec.ts`** khi chưa được yêu cầu — chạy trực tiếp qua Playwright code snippet
3. **Tập trung vào fields trong form/dialog** — không test filter, phân trang, menu
4. **Mỗi lần test tối đa 15 fields** — nếu form nhiều hơn → chia batch
5. **Báo cáo thiếu `data-qa`** nếu field không có attribute này — KHÔNG tự thêm
6. **KHÔNG sửa code ngoài phạm vi test** — nếu phát hiện lỗi BE → tạo bug, không tự sửa
7. **Dùng `data-qa` làm locator chính** — fallback `name` → `id` → `placeholder`
8. **Login 1 lần duy nhất** — tái sử dụng session cho các lần test sau

---

## 🔗 Kỹ Năng Liên Quan

| Kỹ năng | Mối quan hệ |
|---------|-------------|
| `kiem-thu` | Test tổng quát (dùng MCP test management) |
| `clone-web-playwright` | Clone UI từ web tham khảo |
| `clone-dialog-ui-b0` | Clone dialog UI |
| `validate-input` | Quy tắc validate client-side |
| `xac-dinh-pham-vi` | Xác định file cần sửa trước khi test |
