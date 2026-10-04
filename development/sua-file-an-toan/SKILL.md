---
name: sua-file-an-toan
description: 'Quy tắc sửa file an toàn trong dự án JDX-Gamers Website. Dùng khi: replace_string_in_file, multi_replace_string_in_file, refactor code, đổi tên biến/class, xóa/thêm đoạn code. Tránh: mất tiếng Việt Unicode, replace sai vị trí, lặp nội dung, mất dòng code, lỗi encoding PowerShell.'
---

# Quy Tắc Sửa File An Toàn — JDX-Gamers Website

---

## Nguyên Tắc Cốt Lõi

1. **Đọc file trước khi sửa** — luôn `read_file` đoạn cần sửa, không sửa từ trí nhớ hay giả định
2. **oldString phải khớp 100%** — copy từ `read_file`, không tự gõ lại
3. **Tiếng Việt trong oldString** — xem mục riêng bên dưới
4. **Verify sau mỗi lần sửa** — `get_errors` sau mỗi lần replace

---

## Quy Tắc oldString (BẮT BUỘC)

### Độ dài ngữ cảnh
- Luôn bao gồm **ít nhất 3 dòng trước và 3 dòng sau** đoạn cần thay
- Nếu đoạn cần sửa xuất hiện nhiều lần trong file → mở rộng ngữ cảnh đến khi unique

### KHÔNG làm:
```
❌ oldString chứa "// ... existing code ..." hoặc "..."
❌ oldString chứa dòng bị truncate / rút gọn
❌ oldString tự gõ lại tiếng Việt từ trí nhớ
❌ oldString copy từ conversation summary (có thể đã bị rút gọn)
```

### PHẢI làm:
```
✅ Gọi read_file để lấy nội dung chính xác trước khi replace
✅ Copy nguyên văn từ output của read_file
✅ Bao gồm đủ dòng context để oldString là unique trong file
```

---

## Tiếng Việt & Unicode — Vấn Đề Quan Trọng

### Nguồn gốc lỗi
File `.tsx` trong dự án dùng **HTML entities** thay tiếng Việt trực tiếp để tránh PowerShell double-encode:
- `Đ` → `&#272;` / ký tự Unicode `\u0110`
- `ả` → `&#7843;` / `\u1ea3`
- Nhưng trong tool `replace_string_in_file`, agent truyền tham số dưới dạng JSON → Python xử lý Unicode bình thường

### Rủi ro khi sửa file có tiếng Việt

| Tình huống | Rủi ro | Cách xử lý |
|---|---|---|
| File lưu HTML entities (`&#272;`) | oldString dùng ký tự `Đ` → không khớp | Đọc file trước, dùng đúng dạng trong file |
| File lưu UTF-8 trực tiếp | oldString dùng HTML entity → không khớp | Đọc file trước, dùng đúng dạng trong file |
| Tool truyền JSON với `\u....` | Khớp ký tự Unicode → OK | Không vấn đề |

### Quy tắc thực hành
```
1. read_file đoạn cần sửa
2. Quan sát: file dùng HTML entities hay UTF-8 trực tiếp?
3. Dùng ĐÚNG dạng đó trong oldString
4. KHÔNG chuyển đổi tự ý giữa entities và ký tự Unicode
```

---

## ⛔ CẢNH BÁO: PowerShell Get-Content / Set-Content Phá Hủy Tiếng Việt

### Vấn đề
PowerShell 5.1 mặc định **đọc file UTF-8 no BOM như Windows-1252**, sau đó khi ghi lại bằng `Set-Content -Encoding UTF8` → mỗi byte UTF-8 multi-byte bị encode thêm một lần nữa → **tiếng Việt bị garbled trên browser**.

Ví dụ thực tế:
```
File gốc:  "Giám sát hóa đơn CQT"
Sau PS:    "GiÃ¡m sÃ¡t hÃ³a Ä'Æ¡n CQT"
```

### Lệnh TUYỆT ĐỐI KHÔNG DÙNG cho file có tiếng Việt

```powershell
# ❌ KHÔNG BAO GIỜ DÙNG — gây corrupt tiếng Việt
Get-Content file.tsx | Select-Object -First N | Set-Content -Encoding UTF8 file.tsx
(Get-Content file.tsx) | Set-Content file.tsx
Get-Content file.tsx | Out-File file.tsx
```

### Thay thế an toàn: dùng Node.js

```javascript
// ✅ ĐÚNG — Node.js xử lý UTF-8 chính xác
node -e "
const fs = require('fs');
const f = 'path/to/file.tsx';
const lines = fs.readFileSync(f, 'utf8').split('\n');
// Cắt N dòng đầu:
fs.writeFileSync(f, lines.slice(0, N).join('\n'), 'utf8');
"
```

### Cách phục hồi khi file đã bị corrupt

```bash
# Restore từ git commit gần nhất còn tốt
git restore --source=<commit-hash> path/to/file.tsx

# Sau đó mới dùng Node.js để sửa tiếp nếu cần
```

### Quy tắc chung khi cần thao tác file qua terminal
| Thao tác | Cách an toàn |
|---|---|
| Đọc & ghi lại file | Node.js `fs.readFileSync/writeFileSync` với `'utf8'` |
| Cắt N dòng đầu | Node.js `lines.slice(0, N).join('\n')` |
| Tìm kiếm trong file | `grep_search` tool (không qua PowerShell) |
| Sửa nội dung file | `replace_string_in_file` / `multi_replace_string_in_file` tool |
| Xem nội dung file | `read_file` tool (không qua PowerShell) |

---

## Quy Tắc multi_replace_string_in_file

### Khi nào dùng
- **≥ 2 thay đổi độc lập** trong cùng 1 file → dùng `multi_replace` thay vì gọi `replace` nhiều lần
- **Thay đổi ở các file khác nhau** → gọi song song trong cùng một lượt

### Thứ tự replacements
- Replacements được áp dụng **tuần tự từ trên xuống**
- Nếu replacement #1 xóa một đoạn mà replacement #2 cần làm context → sẽ fail
- **Rule:** Sắp xếp từ dưới file lên trên (bottom-to-top) để tránh offset vị trí

### Kiểm tra trước khi submit
```
Với mỗi replacement trong mảng:
✅ oldString unique trong file?
✅ newString không vô tình trùng/lặp với nội dung còn lại?
✅ Các replacements không conflict nhau (không cùng đụng 1 vùng)?
```

---

## Các Lỗi Hay Gặp & Cách Tránh

### 1. Mất đoạn code do replace thiếu
**Vấn đề:** oldString chứa `<Component` nhưng quên kèm `\n  prop1=...` → newString thay thế sai phần
```
❌ oldString: "<PTCardThongTin"
   → Thay thế đúng tag nhưng props bên dưới trở thành orphan (JSX lỗi)

✅ oldString: "<PTCardThongTin\n          isView={isView}\n          form={form}"
   → Khớp đủ context, newString giữ đủ props
```

### 2. Lặp nội dung do newString quá rộng
**Vấn đề:** newString bao gồm lại cả phần đã có trong oldString sau điểm thay thế
```
❌ oldString: "  {/* Row 2 */}\n  <div className="
   newString: "  {/* Row 2: Mã ĐT | Tên ĐT */}\n  <div className="items-end">
              \n  {/* Row 2: Mã ĐT | Tên ĐT */}"   ← lặp comment

✅ newString chỉ thay đúng phần cần đổi, không tự thêm content khác
```

### 3. Xóa nhầm import/export
**Vấn đề:** Khi xóa một block lớn, vô tình xóa theo import đang dùng chỗ khác
```
✅ Sau khi xóa block → grep_search tên symbol đã xóa để confirm không còn dùng ở đâu
✅ Sau đó mới xóa import tương ứng
```

### 5. Code thừa sau replace lớn (>50 dòng)
**Vấn đề:** oldString không bao hết phần cũ → newString được chèn vào nhưng phần cuối của oldString vẫn còn trong file → JSX/code thừa nằm ngoài function body → TypeScript KHÔNG báo lỗi, nhưng Vite/SWC báo runtime parse error
```
❌ oldString kết thúc tại dòng giữa chừng của component
   → newString chèn vào, phần code sau oldString vẫn còn
   → File có 2 lần đóng component hoặc JSX orphan
   → get_errors: 0 lỗi (TypeScript pass)
   → Vite runtime: "Unterminated regexp" hoặc parse error

✅ Với replace lớn (>50 dòng): bắt buộc bao hết toàn bộ đoạn cũ trong oldString
✅ Sau replace lớn: đọc lại 20 dòng cuối file để confirm không có code thừa
✅ Kiểm tra: đoạn code mới kết thúc đúng ở cuối file, không có JSX ngoài component
```

### 6. `get_errors` không đủ cho replace lớn
**Vấn đề:** TypeScript compiler không phát hiện JSX/code orphan ngoài function body. Chỉ Vite/SWC runtime mới bắt được.
```
✅ Với thay đổi nhỏ (1-10 dòng): get_errors là đủ
✅ Với replace lớn (>50 dòng hoặc rewrite toàn bộ function/component):
   → get_errors: kiểm tra TypeScript
   → ĐỌC LẠI cuối file: read_file 20 dòng cuối để verify cấu trúc
   → KIỂM TRA số dòng trước/sau: bất thường nếu file tăng quá nhiều
```

---

## Workflow Sửa File — Chuẩn

```
1. read_file đoạn cần sửa (đủ context, dư vài dòng)
2. Xác định chính xác oldString (unique, không rút gọn)
3. Chuẩn bị newString (không lặp, không thiếu)
4. Nếu ≥ 2 thay đổi → dùng multi_replace, sắp xếp bottom-to-top
5. Thực hiện replace
6. get_errors để verify TypeScript
7. **Nếu replace lớn (>50 dòng):** đọc lại 20 dòng cuối file (`read_file` endLine = tổng dòng) để verify không có code thừa
8. Nếu lỗi → đọc lại file, tìm nguyên nhân, không retry blind
```

---

## Checklist Trước Khi Submit Replace

- [ ] Đã `read_file` đoạn cần sửa trong phiên hiện tại (không dùng từ trí nhớ)
- [ ] oldString được copy nguyên văn từ `read_file`, không tự gõ lại
- [ ] oldString có ≥ 3 dòng context trước và sau
- [ ] oldString là unique trong file (không match nhiều chỗ)
- [ ] **oldString bao hết toàn bộ đoạn cần xóa** — không cắt ngang giữa chừng một block
- [ ] newString không tạo ra nội dung trùng lặp
- [ ] newString không làm mất code hợp lệ nào
- [ ] Tiếng Việt trong oldString dùng đúng dạng (entity vs UTF-8) như trong file gốc
- [ ] Nếu xóa symbol → kiểm tra còn dùng ở chỗ khác không trước khi xóa import
- [ ] Sau replace → `get_errors` confirm 0 lỗi TypeScript
- [ ] **Nếu replace lớn (>50 dòng):** `read_file` 20 dòng cuối để verify không có code/JSX thừa ngoài function
