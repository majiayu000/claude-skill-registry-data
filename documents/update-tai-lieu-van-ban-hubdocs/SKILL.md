---
name: update-tai-lieu-van-ban-hubdocs
description: "Đối chiếu & hiệu chỉnh tài liệu văn bản Hub Docs (doc-articles) theo màn hình portal thực tế. Dùng khi: sửa tài liệu markdown cho khớp URL/đường dẫn thực tế, đúng tên màn hình, đúng tên nút bấm/trường nhập; BE tạo tài liệu từ bộ API nhưng chưa sát với ghép chức năng trên giao diện; cần xác định tài liệu thuộc portal nào rồi đọc code React thực tế để hiệu chỉnh. ⚠️ BẮT BUỘC: user phải cung cấp docCode (1 bài viết) hoặc groupCode (danh sách bài viết); thiếu → KHÔNG thực hiện."
argument-hint: "docCode (mã tài liệu, VD: 1708202623) hoặc groupCode (mã nhóm, VD: cskh) + projectCode (VD: SSO). KHÔNG cung cấp docCode/groupCode → sẽ dừng, không làm việc."
---

# Update Tài Liệu Văn Bản Hub Docs — Đối Chiếu Với Màn Hình Portal Thực Tế

## Mục Đích

Tài liệu văn bản (doc-articles / Hub docs) do **BE tạo từ bộ API** nên thường **chưa sát và chưa đúng** với cách ghép chức năng trên màn hình portal (đường dẫn URL thật, tên màn hình, tên nút bấm, trường nhập, luồng thao tác). Skill này giúp:

1. Xác định tài liệu thuộc **portal nào** (từ `projectCode`).
2. Tìm **màn hình chức năng tương ứng** trong code React thực tế.
3. **Đối chiếu** và **hiệu chỉnh** lại nội dung markdown cho khớp giao diện thật.

> ⚠️ **Quan trọng:** Chỉ hiệu chỉnh **nội dung** (URL, tên màn hình, nút bấm, trường nhập, luồng). **KHÔNG đổi** `docCode` / `slug` / `title` — đây là định danh bài viết (BE đã tạo, dùng cho link liên kết).

---

## 🔒 Yêu Cầu Đầu Vào BẮT BUỘC (GATE — kiểm tra trước tiên)

> **KHÔNG CÓ docCode HOẶC groupCode → KHÔNG THỰC HIỆN NHIỆM VỤ.** Dừng lại và yêu cầu user cung cấp.

| Đầu vào | Ý nghĩa | Phạm vi xử lý |
|---------|---------|---------------|
| `docCode` | Mã 1 tài liệu duy nhất | Hiệu chỉnh **đúng 1 bài viết** |
| `groupCode` | Mã nhóm tài liệu | Lấy **danh sách bài viết** thuộc nhóm → hiệu chỉnh từng bài |

**Quy tắc:**

1. Ngay khi nhận nhiệm vụ → kiểm tra tham số đầu vào:
   - Có `docCode` → chuyển B0 (lấy 1 bài).
   - Có `groupCode` → chuyển B0 (lấy danh sách nhóm).
   - **Không có `docCode` và không có `groupCode`** → **DỪNG NGAY**, báo:
     ```
     🛑 THIẾU ĐẦU VÀO — CẦN CUNG CẤP
     Bạn phải cung cấp ít nhất 1 trong 2:
       - docCode: mã tài liệu cần sửa (VD: 1708202623)
       - groupCode: mã nhóm chứa danh sách tài liệu cần sửa (VD: cskh)
     Kèm theo projectCode (VD: SSO) để xác định portal.
     ```
   - **KHÔNG tự ý** dùng `slug`/`id`/tìm kiếm mô tả để thay thế khi thiếu docCode/groupCode.
2. Nếu có cả `docCode` lẫn `groupCode` → ưu tiên `docCode` (1 bài viết cụ thể).
3. `projectCode` nên cung cấp kèm; nếu thiếu → xác định qua `doc-get-projects-list` hoặc hỏi user.

---

## Bộ Tool MCP Hub Docs (nhóm doc-article)

| Tool | Mục đích | Khi nào dùng |
|------|---------|--------------|
| `mcp_hub_mcp_doc-get-projects-list` | Liệt kê tất cả project tài liệu active | Khi chưa biết `projectCode` |
| `mcp_hub_mcp_doc-get-project-context` | Lấy tên project, groups API | Xác định tên/đặc điểm project |
| `mcp_hub_mcp_doc-article-list-by-group` | Danh sách tóm tắt bài viết theo `groupCode` | Duyệt tài liệu của 1 nhóm |
| `mcp_hub_mcp_doc-article-search` | Tìm tài liệu semantic (UserGuide/BusinessRule/Changelog/TestGuide/Deployment) | Chưa biết id/slug, tìm theo nội dung |
| `mcp_hub_mcp_doc-article-business-search` | Tìm tài liệu Sale/CSKH (PricingPolicy/SalesGuide/PromotionGuide/FAQ) | Tài liệu thuộc nhóm kinh doanh/CSKH |
| `mcp_hub_mcp_doc-article-get` | Lấy **full content markdown** theo `slug`/`articleId` | **Bước đầu tiên** khi có slug |
| `mcp_hub_mcp_doc-article-get-by-doccode` | Lấy full content theo `docCode` | Khi biết mã tài liệu (VD: `1708202623`) |
| `mcp_hub_mcp_doc-article-detail` | Chi tiết theo `articleId` (ObjectId) | Khi biết `id` bài viết |
| `mcp_hub_mcp_doc-article-update` | Cập nhật bài viết theo `articleId`/`slug` (từng phần) | **Sau khi hiệu chỉnh** nội dung |
| `mcp_hub_mcp_doc-article-update-by-doccode` | Cập nhật bài viết theo `docCode` | Khi chỉ có `docCode` |
| `mcp_hub_mcp_doc-article-submit` | Upsert bài viết theo `slug` (tạo mới/cập nhật) | Cập nhật kèm chunks hoặc tạo mới |
| `mcp_hub_mcp_doc-article-delete` | Xóa bài viết (soft delete) | Khi bài viết không còn đúng / trùng |

> **API docs** (không phải tài liệu văn bản) — dùng `doc-check` skill: `doc-get-by-endpoint`, `doc-get-endpoint`, `doc-get-by-id`, `doc-search-api-docs`...

---

## Bảng Map projectCode → Portal

| projectCode (doc-articles) | Portal | Module path | Repo git |
|---------------------------|--------|-------------|----------|
| `SSO` | SSO | `src/modules/SsoApp/` | `jdx-portal-sso` |
| `INVOICE` | Invoice (Business) | `src/modules/InvoiceApp/` | `jdx-portal-invoice` |
| `ADMIN` | Admin | `src/modules/AdminApp/` | `jdx-portal-admin` |
| `PARTNER` | Partner | `src/modules/PartnerApp/` | `jdx-portal-partner` |
| `KETOAN` | Ketoan | `src/modules/KetoanApp/` | `jdx-portal-accounting` |
| `CRM` | CRM | `src/modules/CrmApp/` | `jdx-portal-crm` |
| `TAI_SAN` | TaiSan | `src/modules/TaiSanApp/` | `jdx-portal-taisan` |
| `KIEMTHU_API` | KiemThu | `src/modules/KiemThuApp/` | `jdx-portal-kiemthu` |
| `BASE_INDEX` | BaseIndex | `src/modules/BaseIndexApp/` | `jdx-portal-baseindex` |
| `QLCV` | (chưa có portal riêng — cần xác nhận) | — | — |

> Lấy danh sách chính xác tại runtime bằng `mcp_hub_mcp_doc-get-projects-list` (mỗi project có `Code`, `Name`).
> Nếu `projectCode` không có trong bảng → **DỪNG**, báo user xác định portal trước khi đọc code.

---

## Quy Trình Hiệu Chỉnh

### B0 — Kiểm tra đầu vào & lấy tài liệu

> ✅ Đã qua GATE: có `docCode` hoặc `groupCode`.

```text
- Có docCode      → mcp_hub_mcp_doc-article-get-by-doccode (projectCode, docCode) — 1 bài
- Có groupCode    → mcp_hub_mcp_doc-article-list-by-group (projectCode, groupCode) → danh sách bài → chọn bài cần sửa
- projectCode thiếu → mcp_hub_mcp_doc-get-projects-list (đối chiếu tên/Code) hoặc hỏi user
```

**Kết quả B0:** `projectCode` + `docCode` + `slug` + `title` + full `contentMarkdown` (đọc kỹ từng section).

> 🚫 CẤM dùng `doc-article-search` / `doc-article-business-search` (tìm theo mô tả) làm phương án thay thế khi thiếu docCode/groupCode — chỉ dùng sau khi đã có nhóm/bài từ docCode/groupCode.

### B1 — Xác định portal (từ projectCode)

- Tra bảng map ở trên (hoặc `doc-get-projects-list`).
- Ghi nhận `PORTAL_PATH = src/modules/{PortalApp}`.

### B2 — Tìm màn hình chức năng tương ứng

Cách tìm **bắt buộc** (tra cứu codebase = codebase-memory-mcp; 🚫 CẤM grep/file_search):

1. **Từ tiêu đề/nội dung tài liệu** → tìm page chứa từ khóa:
   - `search_graph(query='<từ khóa tiếng Việt trong title>')` → lọc `label=Function` trong `pages/`.
   - Fallback: `search_graph` theo tên nghiệp vụ (VD: "đăng nhập", "phân quyền", "hóa đơn").
2. **Xác nhận route thực tế**:
   - `read_file {PORTAL_PATH}/routes/routeConfig.tsx` → tìm `path` khớp page.
   - `read_file {PORTAL_PATH}/layout/NavMenu{Portal}.tsx` + `TopMenu{Portal}.tsx` → tìm **tên menu + thứ tự** đúng.
   - URL thực tế = `#/{prefix}/{path}` (prefix theo bảng PORTAL_CONFIG: kiem-thu, ketoan, business, admin...).
3. **Đọc code React thực tế** (đọc đúng file):
   - Page: `features/**/pages/*.tsx` (tiêu đề h1, nút, thanh filter, bảng).
   - Dialog: `features/**/dialogs/*.tsx` (các trường nhập, nút lưu, validate).
   - Hook/Service: `hooks/*.ts` + `services/*.ts` (params thật, message lỗi thật).

### B3 — Trích xuất dữ liệu thực tế

Lập bảng đối chiếu — **chỉ lấy từ code, không suy đoán**:

| Hạng mục | Nội dung tài liệu (BE) | Thực tế (code React) | Đúng/Sai |
|----------|------------------------|----------------------|:--------:|
| Đường dẫn URL | `ten-doanh-nghiep.jdx.vn`... | `https://.../#/sso/login`... | ✅/❌ |
| Tên màn hình | "Trang chính của phần mềm" | h1 thật, tên menu thật | ✅/❌ |
| Tên nút bấm | "Bấm nút Đăng nhập" | `data-qa`/label thật (`btn_*`) | ✅/❌ |
| Tên trường nhập | "Ô Tên đăng nhập" | `Label`/`placeholder` thật | ✅/❌ |
| Luồng thao tác | Bước 1→2→3... | Thứ tự thao tác thật | ✅/❌ |
| Option/danh mục | Các lựa chọn | `DOC_TYPE_OPTIONS`, dropdown thật | ✅/❌ |
| Message/trạng thái | Thông báo lỗi | `toast`/message thật | ✅/❌ |

### B4 — Hiệu chỉnh markdown

> 🔒 **BẮT BUỘC GIỮ CẤU TRÚC TỪNG PHẦN CỦA TÀI LIỆU BAN ĐẦU** — chỉ sửa nội dung trong từng phần, không thay đổi khung tài liệu.

**Giữ NGUYÊN (bắt buộc):**

- `docCode`, `slug`, `title` (định danh bài viết).
- **Cấu trúc heading cấp 2** (`## 1. ...`, `## 2. ...`) — giữ nguyên số lượng + tên section + thứ tự.
- **Cấu trúc con trong từng phần**: tiêu đề cấp 3 (`### ...`), danh sách bullet/numbered, bảng, blockquote, thứ tự các mục con.
- **Format link liên kết** `<docCode>-<slug>.article.md` giữ nguyên.

**Chỉ SỬA nội dung bên trong từng phần (giữ nguyên khung):**

- URL thật, tên màn hình thật, tên nút bấm/trường nhập (thay text cũ bằng text đúng — không đổi vị trí/độ sâu heading).
- Thứ tự bước đúng, option đúng, message đúng.
- Nếu 1 section có nội dung sai → **sửa ngay trong section đó**, không dời sang section khác.
- Nếu phát hiện thiếu màn hình/nút thật → bổ sung chi tiết **vào section tương ứng đang nói về thao tác đó** (không thêm section mới, không đổi thứ tự).

**Quy trình:**

1. Đọc toàn bộ `contentMarkdown` → liệt kê từng section (`## ...`) vào bảng đối chiếu.
2. **Đối chiếu xong 1 section → sửa 1 section** (giữ heading + khung, chỉ thay nội dung).
3. Sau khi sửa hết → rà lại: **số section / tên heading / thứ tự** phải **GIỐNG HỆT** bản gốc.
4. Dùng `replace_string_in_file` cho file markdown local hoặc soạn lại content khi gọi update API (giữ nguyên khung).

### B5 — Cập nhật lên Hub Docs

```text
mcp_hub_mcp_doc-article-update:
  projectCode, slug|articleId
  contentMarkdown: <nội dung đã hiệu chỉnh>
  isVerifiedFE: true          ← đánh dấu FE đã xác minh (hệ thống tự ghi feVerifiedAt)
```

- Không truyền `docCode`/`slug`/`title` nếu không đổi (giữ định danh).
- Sau khi update → gọi `doc-article-get` lại để **verify nội dung đã lưu đúng**.

### B6 — Báo cáo

```text
✅ Đã hiệu chỉnh tài liệu [title] (docCode, slug)
Portal: [SsoApp] | Màn hình: [tên + URL thật #/sso/...]
Đã sửa: [danh sách mục — VD: URL, tên nút Đăng nhập, bước 5]
Giữ nguyên: docCode/slug/title
Trạng thái: isVerifiedFE = true
```

---

## Quy Tắc Bắt Buộc

1. **🔒 BẮT BUỘC có `docCode` hoặc `groupCode` trước khi làm** — thiếu → DỪNG, báo user (xem mục GATE). Không tự ý thay bằng slug/id/search.
2. **Xác định đúng portal trước khi đọc code** — không suy đoán portal khi `projectCode` không rõ.
3. **Tra cứu codebase = codebase-memory-mcp** (`search_graph`, `trace_path`, `get_code_snippet`) — 🚫 CẤM grep_search/file_search.
4. **Đọc code React thực tế** (page/dialog/hook/service) trước khi kết luận — không tự suy diễn tên màn hình/nút.
5. **KHÔNG đổi** `docCode` / `slug` / `title` — chỉ hiệu chỉnh nội dung.
6. **🔒 GIỮ CẤU TRÚC TỪNG PHẦN tài liệu gốc** — số section / tên heading cấp 2 / thứ tự / cấu trúc con KHÔNG ĐỔI; chỉ thay nội dung bên trong từng phần.
7. **Giữ format link liên kết** giữa các bài: `[tên bài](<docCode>-<slug>.article.md)`.
8. **Cập nhật qua MCP** (không tự ghi DB) + đặt `isVerifiedFE=true` khi đối chiếu xong.
9. Nếu tài liệu không liên quan portal nào trong codebase (VD: `QLCV`) → **DỪNG, hỏi user**.
10. Mỗi lượt xử lý **tối đa 3 bài viết** (tránh rate limit); xong báo cáo checkpoint.

---

## Ví dụ

**Đầu vào hợp lệ:** `docCode=1708202623` + `projectCode=SSO`

1. Kiểm tra GATE: có `docCode` → tiếp tục.
2. `doc-article-get-by-doccode(SSO, 1708202623)` → slug=`sso-cskh-huong-dan-dang-nhap-he-thong`, đọc toàn bộ markdown.
3. Map: `SSO` → `SsoApp` (`src/modules/SsoApp/`).
4. Tìm màn hình: `search_graph('đăng nhập')` → `SsoApp` login page; đọc `routes/routeConfig.tsx` → URL `#/sso/login` (thực tế có thể khác).
5. Đọc `LoginPage.tsx` → tên nút thật (VD: `Đăng nhập`), trường thật (`Tên đăng nhập`/`Mật khẩu`), message lỗi thật.
6. Lập bảng đối chiếu từng section → sửa nội dung trong từng phần, **GIỮ NGUYÊN heading `## ...` + thứ tự + cấu trúc con**.
7. `doc-article-update(SSO, slug, contentMarkdown=mới, isVerifiedFE=true)`.
8. Verify lại + báo cáo.

**Đầu vào KHÔNG hợp lệ:** user chỉ nói "sửa tài liệu đăng nhập cho khớp màn hình" (không có docCode/groupCode):

→ **DỪNG NGAY**, báo:

```
🛑 THIẾU ĐẦU VÀO — CẦN CUNG CẤP
Bạn phải cung cấp ít nhất 1 trong 2:
  - docCode: mã tài liệu cần sửa (VD: 1708202623)
  - groupCode: mã nhóm chứa danh sách tài liệu (VD: cskh)
Kèm theo projectCode (VD: SSO) để xác định portal.
```
