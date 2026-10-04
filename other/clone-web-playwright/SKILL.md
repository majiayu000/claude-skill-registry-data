---
name: clone-web-playwright
description: 'Dùng Playwright mở trình duyệt, truy cập trang web (có authentication), chụp ảnh và trích xuất toàn bộ thông tin UI/UX: bố cục, form fields, bảng dữ liệu, buttons, menu, filter, phân trang, tabs, dialogs... để làm tài liệu thiết kế front-end. Dùng khi: user cung cấp URL cần clone, cần phân tích giao diện web có sẵn, muốn tái tạo UI từ web tham khảo, cần snapshot toàn bộ màn hình nghiệp vụ. Kế thừa skill ve-theo-template cho phần ánh xạ UI → SASUCO conventions.'
argument-hint: 'URL trang web cần clone. VD: https://actasp.misa.vn/app/BA/BADepositWithdraw/BADepositWithdrawList/Deposit'
---

# Clone Web Bằng Playwright — SASUCO InvoiceEasy

> **Mục tiêu:** Dùng Playwright mở trình duyệt thật, truy cập trang web đích (kể cả có authentication), tự động chụp ảnh & trích xuất cấu trúc UI → tạo tài liệu phân tích đầy đủ để làm front-end.

---

## 🚀 Chế Độ Tối Ưu Token (MẶC ĐỊNH)

> **LUÔN DÙNG chế độ tối ưu.** Mục tiêu: giảm 80% token output, tăng tốc xử lý.

### Nguyên tắc tối ưu:

| Hạng mục | ❌ Cũ (đầy đủ) | ✅ Mới (tối ưu) |
|----------|---------------|-----------------|
| **Ảnh chụp** | 7 ảnh (fullpage, header, filter, table, pagination, sidebar, form) | **Chỉ 2 ảnh** (fullpage + form-subpage) — để user tham khảo, AI không cần xem |
| **Field keys** | `label, type, name, id, placeholder, required, readOnly, disabled, maxLength, className` | **`l, t, r, ro, ph, y, x`** (label, type, required, readOnly, placeholder, top, left) |
| **Button keys** | `text, tag, className, title, backgroundColor, color` | **`t, y, x`** (text, top, left) |
| **Table** | Headers + sampleRows + rowCount đầy đủ | **Chỉ `cols + rows + type`**, dedup cột trùng liên tiếp |
| **Phân vùng** | Không | **Tách filter fields (y < 150) vs form fields**, layout regions `{y, h}` |
| **API** | method, url, headers, postData, responseBody, status, timestamp | **Chỉ `m + u`** (method, url) |
| **Output size** | ~50KB+ | ~5-10KB (giảm ~80%) |

### Template script tối ưu:

> **Luôn kế thừa từ `e2e/clone-optimized.ts`** — đây là bản mẫu gốc. Copy và chỉ sửa `CONFIG.targetUrl` + `CONFIG.outputDir`.

### Cấu trúc thư mục đầu ra (tối ưu):

```
exports/clone-results/
├── auth.json                          ← 🔑 Session DÙNG CHUNG (tất cả clone)
├── <ten-trang-1>/
│   ├── screenshots/
│   │   ├── fullpage.png               ← Ảnh toàn trang (user xem)
│   │   └── form-subpage.png          ← Ảnh form (nếu có sub-page)
│   ├── analysis/
│   │   ├── page-structure.md          ← Báo cáo tổng hợp
│   │   ├── fields-inventory.md        ← Kiểm kê fields
│   │   ├── table-columns.md           ← Cột bảng
│   │   ├── buttons-actions.md         ← Nút & hành động
│   │   └── api-list.json              ← API endpoints (chỉ method+url)
│   └── raw/
│       ├── page-snapshot.json         ← Dữ liệu thô (đã tối ưu key)
│       └── form-snapshot.json         ← Dữ liệu form (nếu có)
└── <ten-trang-2>/
    └── ...
```

---

## ⚠️ Hạn Chế Model

| Model | Hỗ trợ view_image? | Cách làm việc |
|-------|-------------------|---------------|
| **Claude Sonnet** | ✅ CÓ | Phân tích ảnh chụp trực tiếp từ `view_image` |
| **DeepSeek V4 Pro** | ❌ KHÔNG | Chỉ phân tích dữ liệu text từ `page-snapshot.json` |

> Khi dùng DeepSeek: **bỏ qua bước xem ảnh**, tập trung vào dữ liệu text trong `raw/page-snapshot.json` và `analysis/api-list.json`. Ảnh chụp vẫn được lưu để user tự xem.

---

## 🔑 Quản Lý Session (Tự Động)

### 🔄 Daemon Mode — KHÔNG ĐĂNG NHẬP LẠI (DÙNG MẶC ĐỊNH)

> **Mỗi lần clone không cần đăng nhập lại.** Browser được giữ mở vĩnh viễn qua daemon.

**Nguyên lý:**
1. Chạy daemon **1 lần duy nhất** → mở browser, đăng nhập thủ công
2. Session được lưu vào `exports/clone-results/auth.json` (dùng chung)
3. Daemon giữ browser luôn mở, tự động refresh session mỗi 30s
4. Các script clone **connect vào daemon qua CDP port 9222** — không mở browser mới
5. Sau khi clone xong, browser vẫn mở sẵn cho lần clone tiếp theo

```
┌─────────────────────────────────────────┐
│  DAEMON (chạy 1 lần, giữ browser mở)     │
│  npx tsx e2e/playwright-daemon.ts        │
│  🌐 CDP: http://localhost:9222           │
│  💾 Session: exports/clone-results/auth.json │
└────────────┬────────────────────────────┘
             │ connectOverCDP
     ┌───────┼───────┬──────────────┐
     ▼       ▼       ▼              ▼
  clone1  clone2  clone3  ...   (không cần đăng nhập lại)
```

**Khởi động daemon (chỉ 1 lần):**

```powershell
# Terminal 1 — Chạy daemon, để nguyên cửa sổ này
npx tsx e2e/playwright-daemon.ts

# Terminal 2 — Chạy các script clone (không cần đăng nhập)
npx tsx e2e/clone-phieuchi.ts
npx tsx e2e/clone-tien-gui.ts
```

**Dừng daemon:** Bấm `Ctrl+C` ở terminal daemon. Session được lưu tự động.

### Session File Dùng Chung

| File | Vị trí | Mục đích |
|------|--------|----------|
| `auth.json` | `exports/clone-results/auth.json` | **Dùng chung** cho tất cả script clone |

> **Bảo mật:** `auth.json` chứa token, không commit vào git. Đã có trong `.gitignore`.

### Cơ chế tự động

```
Lần 1: Daemon khởi động → đăng nhập thủ công → lưu auth.json
       ↓
       Browser LUÔN MỞ, session tự refresh mỗi 30s
       ↓
Lần 2+: Script clone connect CDP → dùng browser có sẵn → không cần đăng nhập
        Nếu session hết hạn → browser redirect về login → đăng nhập lại trên daemon
```

---

## 🎯 Phát Hiện Framework Grid

Nhiều web không dùng `<table>` HTML mà dùng grid component:

| Framework | CSS Selector | Cách trích xuất |
|-----------|-------------|-----------------|
| **DevExtreme** | `.dx-datagrid` | Headers: `.dx-header-row td[role="columnheader"]`; Rows: `tr.dx-data-row`; Cells: `td` |
| **AG Grid** | `.ag-root` | Headers: `.ag-header-cell-text`; Rows: `.ag-row` |
| **MUI DataGrid** | `.MuiDataGrid-root` | Headers: `.MuiDataGrid-columnHeader`; Rows: `.MuiDataGrid-row` |
| **Ant Table** | `.ant-table` | Dùng `<table>` chuẩn |
| **Custom div-table** | `[role="grid"]` | Headers: `[role="columnheader"]`; Rows: `[role="row"]` |

> **Script luôn thử `<table>` trước, nếu null → thử các selector grid framework.**

---

## Tổng Quan Quy Trình

```
[Pha 0] Chuẩn bị môi trường  →  [Pha 1] Mở browser & xác thực  →  [Pha 2] Quét & chụp UI  →  [Pha 3] Phân tích & tạo báo cáo
```

---

## Pha 0 — Chuẩn Bị Môi Trường

### 0.1 — Xác định thông tin đầu vào

Trước khi bắt đầu, thu thập từ user:

| Thông tin | Bắt buộc? | Mô tả |
|-----------|-----------|-------|
| **URL đích** | ✅ CÓ | URL đầy đủ của trang cần clone |
| **Credentials** | ⚠️ Nếu có auth | Username + password để đăng nhập |
| **Hướng dẫn đăng nhập** | ⚠️ Nếu có auth | Mô tả cách đăng nhập: chọn tenant, nhập mã xác thực... |
| **Tên dự án/danh mục** | Không bắt buộc | Để đặt tên file báo cáo |

### 0.2 — Tạo script Playwright (CHẾ ĐỘ TỐI ƯU)

> **BẮT BUỘC:** Copy từ `e2e/clone-optimized.ts` làm bản mẫu, chỉ sửa `CONFIG.targetUrl` và `CONFIG.outputDir`.

Script được tạo trong thư mục `e2e/` với tên `clone-<ten-trang>.ts`. Script sẽ tự động:

1. Mở browser (headless: false để user thấy và can thiệp nếu cần)
2. Điều hướng đến URL đích
3. Đợi user đăng nhập thủ công (nếu cần) — tái sử dụng session nếu có
4. **Chỉ chụp 2 ảnh**: fullpage + form-subpage (nếu có)
5. Trích xuất cấu trúc DOM với **key tối ưu** (`l, t, r, ro, ph, y, x`)
6. Tự động phân vùng: filter fields (y < 150) vs form fields
7. Dedup table columns
8. Lưu kết quả ra thư mục `exports/clone-results/`

---

## Pha 1 — Mở Browser & Xác Thực

> **Mặc định dùng Daemon Mode.** Chỉ cần đăng nhập 1 lần, các lần clone sau không cần đăng nhập lại.

### Bước 1.0: Khởi động Daemon (CHỈ 1 LẦN)

```powershell
# Terminal 1 — Mở daemon, giữ browser luôn chạy
npx tsx e2e/playwright-daemon.ts
```

- Browser mở ra → **đăng nhập thủ công** vào MISA
- Sau khi login, daemon tự lưu session vào `exports/clone-results/auth.json`
- Daemon giữ browser mở, tự refresh session mỗi 30s
- **Để nguyên terminal này**, không tắt

### Bước 1.1: Chạy script clone (connect vào daemon)

```powershell
# Terminal 2 — Chạy clone, script tự connect vào daemon qua CDP
npx tsx e2e/clone-<ten-trang>.ts
```

Script tự động:
1. Phát hiện daemon đang chạy (port 9222) → connect qua `chromium.connectOverCDP()`
2. Nếu daemon không chạy → fallback: tự mở browser mới + dùng shared auth.json
3. Điều hướng đến URL đích
4. Nếu bị redirect về login → báo user đăng nhập lại trên daemon
5. Quét UI, chụp ảnh, trích xuất dữ liệu
6. **Không đóng browser** (vì browser là của daemon)

### Bước 1.2: Xử lý authentication

Có 2 chế độ:

| Chế độ | Khi dùng | Cách làm |
|--------|----------|----------|
| **Daemon (mặc định)** | Luôn dùng | Browser mở sẵn, session auto-refresh, clone script connect CDP |
| **Standalone (fallback)** | Daemon không chạy | Script tự mở browser, dùng shared `auth.json`, **giữ browser mở** sau khi xong |

> **Không cần nhập credentials vào script.** MISA dùng 2FA + tenant selection → luôn đăng nhập thủ công 1 lần trên daemon.

---

## Pha 2 — Quét & Chụp UI

### Bước 2.1: Chụp ảnh toàn trang

```typescript
// Chụp full page
await page.screenshot({ 
  path: join(OUTPUT_DIR, 'screenshots', 'fullpage.png'), 
  fullPage: true 
});
```

### Bước 2.2: Phân vùng & chụp từng khu vực

Dùng `page.evaluate()` để tìm các vùng chính trong DOM và chụp riêng:

```typescript
// Tìm các vùng chính bằng CSS selector phổ biến
const regions = await page.evaluate(() => {
  const findRegion = (selectors: string[]) => {
    for (const sel of selectors) {
      const el = document.querySelector(sel);
      if (el) return { selector: sel, rect: el.getBoundingClientRect() };
    }
    return null;
  };

  return {
    // Header / toolbar
    header: findRegion([
      '.toolbar', '.page-header', '.header', '[class*="header"]',
      '[class*="toolbar"]', '.ant-page-header', '.top-bar'
    ]),
    // Filter area
    filter: findRegion([
      '.filter', '.search-area', '.filter-bar', '[class*="filter"]',
      '[class*="search"]', '.ant-form'
    ]),
    // Main table
    table: findRegion([
      'table', '.table', '.grid', '.data-grid', '[class*="table"]',
      '[class*="grid"]', '.ant-table', '.dx-datagrid'
    ]),
    // Form / dialog (nếu đang mở)
    form: findRegion([
      '.modal', '.dialog', '.drawer', '[role="dialog"]',
      '[class*="modal"]', '[class*="dialog"]', '.ant-modal'
    ]),
    // Footer / pagination
    footer: findRegion([
      '.pagination', '.pager', '.footer', '[class*="pagination"]',
      '[class*="pager"]', '.ant-pagination'
    ]),
    // Sidebar / menu
    sidebar: findRegion([
      '.sidebar', '.menu', '.nav', '[class*="sidebar"]',
      '[class*="menu"]', '[class*="nav"]', '.ant-menu'
    ]),
  };
});

// Chụp từng vùng
for (const [name, region] of Object.entries(regions)) {
  if (region) {
    const el = page.locator(region.selector).first();
    if (await el.isVisible()) {
      await el.screenshot({ path: join(OUTPUT_DIR, 'screenshots', `${name}.png`) });
    }
  }
}
```

### Bước 2.3: Trích xuất cấu trúc DOM

#### 2.3.1 — Trích xuất Form Fields

```typescript
const fields = await page.evaluate(() => {
  const results: any[] = [];
  
  // Tìm tất cả input, select, textarea trong form hoặc dialog
  const formElements = document.querySelectorAll(
    'form input, form select, form textarea, ' +
    '[role="dialog"] input, [role="dialog"] select, [role="dialog"] textarea, ' +
    '.modal input, .modal select, .modal textarea, ' +
    'input:not([type="hidden"]), select, textarea'
  );

  formElements.forEach((el) => {
    const input = el as HTMLInputElement;
    // Tìm label gần nhất
    let label = '';
    const id = input.id;
    if (id) {
      const labelEl = document.querySelector(`label[for="${id}"]`);
      if (labelEl) label = labelEl.textContent?.trim() || '';
    }
    if (!label) {
      // Tìm label trong parent
      const parent = input.closest('td, .field, .form-group, .form-item, .ant-form-item');
      if (parent) {
        const labelEl = parent.querySelector('label, .label, .field-label');
        if (labelEl) label = labelEl.textContent?.trim() || '';
      }
    }

    results.push({
      tag: input.tagName.toLowerCase(),
      type: input.getAttribute('type') || 'text',
      name: input.getAttribute('name') || '',
      id: input.id || '',
      placeholder: input.getAttribute('placeholder') || '',
      label: label,
      required: input.hasAttribute('required') || input.getAttribute('aria-required') === 'true',
      readonly: input.hasAttribute('readonly') || input.getAttribute('aria-readonly') === 'true',
      disabled: input.hasAttribute('disabled'),
      maxLength: input.getAttribute('maxlength') || '',
      className: input.className || '',
      dataQa: input.getAttribute('data-qa') || '',
      options: [], // Sẽ điền nếu là select
    });

    // Nếu là select, lấy options
    if (input.tagName === 'SELECT') {
      const select = input as HTMLSelectElement;
      const last = results[results.length - 1];
      last.options = Array.from(select.options).map(o => ({
        value: o.value,
        text: o.text,
      }));
    }
  });

  return results;
});
```

#### 2.3.2 — Trích xuất Table Columns

```typescript
const tableInfo = await page.evaluate(() => {
  // Tìm table đầu tiên có dữ liệu
  const tables = document.querySelectorAll('table, [role="grid"], .table, .grid');
  for (const table of tables) {
    // Lấy headers
    const headers: string[] = [];
    const headerRow = table.querySelector('thead tr, .header-row, [class*="header"]');
    if (headerRow) {
      headerRow.querySelectorAll('th, .column-header').forEach(th => {
        headers.push(th.textContent?.trim() || '');
      });
    }
    if (headers.length === 0) continue;

    // Lấy dữ liệu mẫu (3 dòng đầu)
    const sampleRows: string[][] = [];
    const tbody = table.querySelector('tbody');
    if (tbody) {
      const rows = tbody.querySelectorAll('tr');
      for (let i = 0; i < Math.min(3, rows.length); i++) {
        const cells: string[] = [];
        rows[i].querySelectorAll('td').forEach(td => {
          cells.push(td.textContent?.trim() || '');
        });
        sampleRows.push(cells);
      }
    }

    return { headers, sampleRows, rowCount: tbody?.querySelectorAll('tr').length || 0 };
  }
  return null;
});
```

#### 2.3.3 — Trích xuất Buttons & Actions

```typescript
const buttons = await page.evaluate(() => {
  const results: any[] = [];
  const buttonElements = document.querySelectorAll(
    'button, a.btn, [role="button"], ' +
    '.toolbar button, .header button, .action-bar button, ' +
    '[class*="btn"]:not([class*="btn-"])'
  );

  buttonElements.forEach((el) => {
    const btn = el as HTMLElement;
    const text = btn.textContent?.trim() || btn.getAttribute('aria-label') || '';
    if (!text || text.length > 50) return; // Bỏ qua text quá dài

    const style = window.getComputedStyle(btn);
    results.push({
      text: text,
      tag: btn.tagName.toLowerCase(),
      type: btn.getAttribute('type') || '',
      className: btn.className || '',
      title: btn.getAttribute('title') || '',
      icon: btn.querySelector('svg, i, [class*="icon"]') ? 'CÓ' : 'KHÔNG',
      backgroundColor: style.backgroundColor,
      color: style.color,
      position: btn.getBoundingClientRect(),
    });
  });

  return results;
});
```

#### 2.3.4 — Trích xuất Menu / Navigation

```typescript
const navigation = await page.evaluate(() => {
  const nav: any = {};

  // Sidebar menu
  const sidebarItems: string[] = [];
  document.querySelectorAll(
    '.sidebar a, .menu a, '.nav a, ' +
    '[class*="sidebar"] a, [class*="menu-item"], ' +
    '.ant-menu-item'
  ).forEach(el => {
    const text = el.textContent?.trim();
    if (text) sidebarItems.push(text);
  });
  if (sidebarItems.length > 0) nav.sidebar = sidebarItems;

  // Breadcrumb
  const breadcrumb: string[] = [];
  document.querySelectorAll(
    '.breadcrumb *, [class*="breadcrumb"] *'
  ).forEach(el => {
    const text = el.textContent?.trim();
    if (text && text.length < 50) breadcrumb.push(text);
  });
  if (breadcrumb.length > 0) nav.breadcrumb = breadcrumb;

  // Tabs
  const tabs: string[] = [];
  document.querySelectorAll(
    '.tab, [role="tab"], .nav-tabs li, ' +
    '[class*="tab-"]:not([class*="table"])'
  ).forEach(el => {
    const text = el.textContent?.trim();
    if (text) tabs.push(text);
  });
  if (tabs.length > 0) nav.tabs = tabs;

  return nav;
});
```

### Bước 2.4: Lưu dữ liệu thô

```typescript
const snapshot = {
  url: page.url(),
  title: await page.title(),
  timestamp: new Date().toISOString(),
  fields: fields,
  table: tableInfo,
  buttons: buttons,
  navigation: navigation,
  apiRequests: apiRequests,
};

writeFileSync(
  join(OUTPUT_DIR, 'raw', 'page-snapshot.json'),
  JSON.stringify(snapshot, null, 2)
);

// Lưu API requests riêng
writeFileSync(
  join(OUTPUT_DIR, 'analysis', 'api-requests.json'),
  JSON.stringify(apiRequests, null, 2)
);
```

---

## Pha 3 — Phân Tích & Tạo Báo Cáo

### Bước 3.1: Phân tích tổng thể

Dựa trên dữ liệu đã thu thập, agent phân tích:

1. **Loại trang:** Master Page / Form Page / Dashboard / Detail Page / Sub Page?
2. **Bố cục:** Mấy vùng chính? Bố trí ra sao?
3. **Công nghệ:** Nhận diện framework (React, Angular, ASP.NET, DevExtreme, Ant Design...)?

### Bước 3.2: Tạo báo cáo `page-structure.md`

```markdown
# Phân Tích Trang: <Tên trang>

**URL:** `<url>`
**Ngày clone:** <ngày>
**Tiêu đề trang:** <title>

## 1. Tổng Quan

- **Loại UI:** Master Page (bảng danh sách + filter)
- **Framework nhận diện:** DevExtreme / Ant Design / Custom
- **Bố cục:** Header → Filter → Toolbar → Table → Pagination

## 2. Cấu Trúc Trang

| Vùng | Vị trí | Mô tả |
|------|--------|-------|
| Header | Trên cùng | Tiêu đề + breadcrumb + user menu |
| Filter | Dưới header | Ô search + dropdown filter + nút Lọc |
| Toolbar | Trên bảng | Nút Thêm mới, Xuất Excel, Làm mới |
| Table | Giữa | Bảng danh sách dữ liệu chính |
| Pagination | Dưới bảng | Phân trang + chọn page size |

## 3. Fields (form/dialog)

| # | Label | Kiểu | Bắt buộc | Ghi chú |
|---|-------|------|----------|---------|
| 1 | Mã | text | ✅ | Tự sinh hoặc nhập |
| 2 | Tên | text | ✅ | |
| ... | ... | ... | ... | ... |

## 4. Bảng (table columns)

| # | Tên cột | Kiểu dữ liệu | Căn lề | Format |
|---|---------|-------------|--------|--------|
| 1 | Mã | text | left | - |
| 2 | Số tiền | number | right | Currency |
| ... | ... | ... | ... | ... |

## 5. Buttons & Actions

| Nút | Vị trí | Màu sắc | Hành động |
|-----|--------|---------|-----------|
| Thêm mới | Toolbar | Primary/Xanh | Mở dialog tạo mới |
| Sửa | Table row | Warning/Vàng | Mở dialog chỉnh sửa |
| ... | ... | ... | ... |

## 6. Navigation

- **Breadcrumb:** `<path>`
- **Tabs:** (nếu có)
- **Sidebar:** (nếu có)

## 7. API Endpoints Phát Hiện

| Method | URL | Mục đích |
|--------|-----|----------|
| GET | /api/... | Lấy danh sách |
| POST | /api/... | Tạo mới |
| ... | ... | ... |
```

### Bước 3.3: Tạo báo cáo fields, columns, buttons riêng

- `fields-inventory.md`: Danh sách chi tiết từng field kèm validation
- `table-columns.md`: Cấu trúc cột kèm format
- `buttons-actions.md`: Tất cả nút kèm hành vi

### Bước 3.4: Gợi ý ánh xạ sang SASUCO

Sau khi có báo cáo, agent ánh xạ sang SASUCO conventions (kế thừa skill `ve-theo-template` Pha 2 & 3):

| Phát hiện từ web clone | Ánh xạ SASUCO |
|------------------------|---------------|
| Input text | `<Input>` |
| Input số | `type='text' inputMode='numeric' text-right` |
| Select/Dropdown danh mục | `<SearchCombobox>` |
| Select/Dropdown enum | `<Select>` |
| Date picker | `<DatePicker>` |
| Table | PagingUtils + formatCurrency/formatDate |
| Nút xanh | `btn-primary` |
| Nút đỏ | `btn-danger` |

---

## Script Mẫu Hoàn Chỉnh

```typescript
// e2e/clone-<ten-trang>.ts
import { chromium } from 'playwright';
import { writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const CONFIG = {
  targetUrl: '<URL_DO_USER_CUNG_CAP>',
  outputDir: 'exports/clone-results/<ten-trang>',
  waitForAuth: true,       // true = đợi user login thủ công
  authTimeout: 300_000,    // 5 phút
  viewport: { width: 1440, height: 900 },
};

async function main() {
  // Tạo thư mục
  for (const sub of ['screenshots', 'analysis', 'raw']) {
    mkdirSync(join(CONFIG.outputDir, sub), { recursive: true });
  }

  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage({ viewport: CONFIG.viewport });

  // Bắt API calls
  const apiRequests: any[] = [];
  page.on('request', (req) => {
    const url = req.url();
    if (url.includes('/api/') || url.includes('/odata/') || url.includes('/Services/')) {
      apiRequests.push({
        method: req.method(),
        url,
        postData: req.postData(),
        timestamp: Date.now(),
      });
    }
  });

  // Điều hướng
  console.log(`🌐 Đang mở: ${CONFIG.targetUrl}`);
  await page.goto(CONFIG.targetUrl, { waitUntil: 'domcontentloaded' });

  // Đợi auth nếu cần
  if (CONFIG.waitForAuth) {
    const targetPath = new URL(CONFIG.targetUrl).pathname;
    console.log('⏳ Vui lòng đăng nhập trên browser...');
    try {
      await page.waitForURL(`**${targetPath}**`, { timeout: CONFIG.authTimeout });
    } catch {
      console.log('⚠️ Không detect được URL đích. Tiếp tục với URL hiện tại...');
    }
  }

  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(2000);
  console.log('✅ Trang đã sẵn sàng!');

  // === CHỤP ẢNH ===
  await page.screenshot({ path: join(CONFIG.outputDir, 'screenshots', 'fullpage.png'), fullPage: true });
  console.log('📸 Đã chụp fullpage');

  // === TRÍCH XUẤT ===
  const snapshot = await page.evaluate(() => {
    // --- Fields ---
    const fields: any[] = [];
    document.querySelectorAll('input:not([type="hidden"]), select, textarea').forEach((el: any) => {
      const id = el.id;
      let label = '';
      if (id) {
        const lbl = document.querySelector(`label[for="${id}"]`);
        if (lbl) label = lbl.textContent?.trim() || '';
      }
      fields.push({
        tag: el.tagName, type: el.type || 'text', name: el.name || '',
        id, placeholder: el.placeholder || '', label,
        required: el.required || false, readonly: el.readOnly || false,
        disabled: el.disabled || false,
      });
    });

    // --- Table ---
    let tableInfo: any = null;
    const tables = document.querySelectorAll('table');
    for (const t of tables) {
      const headers: string[] = [];
      t.querySelectorAll('thead th').forEach(th => headers.push(th.textContent?.trim() || ''));
      if (headers.length === 0) continue;
      const rows: string[][] = [];
      t.querySelectorAll('tbody tr').forEach((tr, i) => {
        if (i >= 3) return;
        const cells: string[] = [];
        tr.querySelectorAll('td').forEach(td => cells.push(td.textContent?.trim() || ''));
        rows.push(cells);
      });
      tableInfo = { headers, sampleRows: rows, totalRows: t.querySelectorAll('tbody tr').length };
      break;
    }

    // --- Buttons ---
    const buttons: any[] = [];
    document.querySelectorAll('button, [role="button"]').forEach((el: any) => {
      const text = el.textContent?.trim();
      if (text && text.length < 50) {
        buttons.push({ text, className: el.className, title: el.title || '' });
      }
    });

    // --- Navigation ---
    const nav: any = {};
    const breadcrumb: string[] = [];
    document.querySelectorAll('[class*="breadcrumb"] *').forEach((el: any) => {
      const t = el.textContent?.trim();
      if (t && t.length < 50) breadcrumb.push(t);
    });
    if (breadcrumb.length) nav.breadcrumb = breadcrumb;

    const tabs: string[] = [];
    document.querySelectorAll('[role="tab"]').forEach((el: any) => {
      const t = el.textContent?.trim();
      if (t) tabs.push(t);
    });
    if (tabs.length) nav.tabs = tabs;

    return { title: document.title, fields, table: tableInfo, buttons, navigation: nav };
  });

  // Lưu
  writeFileSync(join(CONFIG.outputDir, 'raw', 'page-snapshot.json'), JSON.stringify({ ...snapshot, url: page.url(), timestamp: new Date().toISOString() }, null, 2));
  writeFileSync(join(CONFIG.outputDir, 'analysis', 'api-requests.json'), JSON.stringify(apiRequests, null, 2));
  
  console.log('✅ Hoàn thành! Dữ liệu đã lưu vào:', CONFIG.outputDir);
  console.log(`   - ${snapshot.fields.length} fields`);
  console.log(`   - ${snapshot.table?.headers?.length || 0} table columns`);
  console.log(`   - ${snapshot.buttons.length} buttons`);
  console.log(`   - ${apiRequests.length} API requests`);

  // 🔄 Giữ browser mở để tái sử dụng cho lần clone tiếp theo (không đóng)
  console.log('🔄 Browser vẫn mở — để tái sử dụng. Đóng tab này khi không cần nữa.');
}

main().catch(console.error);
```

---

## Hướng Dẫn Sử Dụng Cho Agent

### Khi user yêu cầu clone web:

1. **Kiểm tra daemon đã chạy chưa:**
   ```powershell
   # Kiểm tra port 9222 có đang listen không
   netstat -ano | findstr :9222
   ```
   - Nếu **chưa có** → báo user chạy daemon: `npx tsx e2e/playwright-daemon.ts`
   - Daemon sẽ mở browser → user đăng nhập thủ công MISA 1 lần

2. **Xác định thông tin:**
   - URL đầy đủ của trang cần clone (user thường cung cấp sẵn)
   - Tên viết tắt cho trang (để đặt tên thư mục output)
   - **Không cần hỏi credentials** (MISA luôn dùng đăng nhập thủ công)

3. **Tạo script clone** — copy từ `e2e/clone-optimized.ts`, sửa `CONFIG.targetUrl` + `CONFIG.outputDir`.

4. **Chạy script clone:**
   ```powershell
   npx tsx e2e/clone-<ten-trang>.ts
   ```
   Script tự connect vào daemon qua CDP port 9222 → không mở browser mới → không cần đăng nhập.

5. **Sau khi script chạy xong:**
   - Đọc file `raw/page-snapshot.json`
   - Đọc file `analysis/api-list.json`
   - Đọc ảnh trong `screenshots/` bằng `view_image` (nếu model hỗ trợ)
   - Các file `.md` phân tích đã được `writeAnalysisFiles()` tự sinh

6. **Trình bày kết quả cho user:**
   - Tổng quan bố cục trang
   - Danh sách fields, table columns, buttons
   - API endpoints phát hiện được
   - Gợi ý ánh xạ sang SASUCO conventions

7. **Không tắt daemon** — để dùng cho lần clone tiếp theo. Chỉ tắt khi user yêu cầu.

---

## 🪶 Tối Ưu Token (DeepSeek / Model Không Có Vision)

### Vấn Đề

Script clone gốc tạo ~50KB text + ~1MB ảnh → đưa vào context AI rất tốn token.

### Nguyên Nhân Tốn Token

| Nguồn | % Token | Giải pháp |
|-------|---------|-----------|
| Ảnh chụp (PNG) | ~50% | ❌ Không đọc ảnh, chỉ lưu file cho user |
| ClassName CSS dài | ~15% | ❌ Bỏ hoàn toàn |
| Style (backgroundColor, color…) | ~10% | ❌ Bỏ hoàn toàn |
| Navigation (sidebar, breadcrumb) | ~10% | ❌ Bỏ (chỉ cần tabs) |
| API response body | ~10% | ❌ Chỉ lấy URL + method |
| JSON key dài (className, backgroundColor…) | ~5% | → Key ngắn (l, t, r, ph, y, x) |

### Format Output Tối Ưu

```json
// page-snapshot.json (chỉ ~3KB thay vì ~30KB)
{
  "url": "...",
  "layout": { "filter": {"y":50}, "table": {"y":150} },
  "filterFields": [{"l":"Tìm kiếm","t":"text"}],
  "table": {"cols":["Ngày HT","Số CT",...],"rows":0,"type":"MISA"},
  "buttons": ["Thêm (Ctrl+1)","Nhập Excel","Hủy","Đồng ý"],
  "tabs": ["Thu tiền","Chi tiền",...]
}
```

**Key convention:**
- `l` = label, `t` = type, `r` = required (1/0), `ro` = readOnly (1/0)
- `ph` = placeholder, `y` = top, `x` = left
- `cols` = column headers, `rows` = row count

### Số Vùng / Ảnh Chụp Tối Thiểu

| Vùng | Có chụp? | Dùng cho AI? |
|------|----------|-------------|
| **fullpage** | ✅ CÓ | ❌ Chỉ để user xem |
| **form-subpage** | ✅ CÓ | ❌ Chỉ để user xem |
| Header | ❌ BỎ | - |
| Sidebar | ❌ BỎ | - |
| Filter riêng | ❌ BỎ | - |
| Table riêng | ❌ BỎ | - |
| Pagination riêng | ❌ BỎ | - |

### Áp Dụng

Dùng script `e2e/clone-optimized.ts` thay vì script đầy đủ:

```powershell
npx tsx e2e/clone-optimized.ts
```

Output giảm **~92% token** (50KB → 3KB) so với script clone gốc.

---

## Cấu Trúc File Output

```
exports/clone-results/<ten-trang>/
├── screenshots/
│   ├── fullpage.png
│   ├── header.png
│   ├── filter.png
│   ├── table.png
│   └── dialog-<ten>.png
├── analysis/
│   ├── page-structure.md       ← Báo cáo tổng hợp chính
│   ├── fields-inventory.md     ← Kiểm kê fields
│   ├── table-columns.md        ← Cấu trúc cột bảng
│   ├── buttons-actions.md      ← Nút & hành động
│   └── api-requests.json       ← API calls đã bắt
└── raw/
    └── page-snapshot.json      ← Dữ liệu thô đầy đủ
```

---

## Xử Lý Các Tình Huống Đặc Biệt

| Tình huống | Cách xử lý |
|-----------|-----------|
| Web dùng iframe | Dùng `page.frameLocator()` để truy cập iframe |
| Web lazy-load | Scroll toàn trang trước khi chụp |
| Dialog/Bật popup | Click nút để mở dialog → chụp → đóng |
| Web có nhiều tab | Click từng tab → chụp từng tab |
| Table ảo hóa (virtual scroll) | Scroll từ từ để load hết dữ liệu |
| Xác thực 2 lớp (2FA) | Luôn dùng chiến lược A (đăng nhập thủ công) |
| DevExtreme dx-datagrid (MISA) | Dùng selector `.dx-header-row td` cho headers, `tr.dx-data-row` cho rows |
| AG Grid | Dùng selector `.ag-header-cell-text` cho headers, `.ag-row .ag-cell` cho cells |
| MUI DataGrid | Dùng selector `.MuiDataGrid-columnHeader`, `.MuiDataGrid-cell` |
| Session hết hạn | Script tự phát hiện redirect → xóa `auth.json` → yêu cầu đăng nhập lại |
| `page.evaluate` lỗi `__name` (esbuild) | Dùng `page.evaluate(string)` thay vì arrow function; polyfill `__name`, `__defProp`, `__esm` |
