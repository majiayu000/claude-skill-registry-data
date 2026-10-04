---
name: text-in-image
description: >-
  Làm CHỮ trong ảnh AI đúng chính tả/dấu/ngắt-dòng cho SEOSONA Flow — chống rớt-chữ/rớt-dòng/sai-dấu.
  Chọn giữa Reserve→Overlay (AI chừa vùng, code dựng chữ vector — cách chuẩn) và bake-in an toàn (chữ
  ngắn, không dấu). Dùng khi cần poster/banner/thumbnail/logo có CHỮ đúng, khi ảnh vừa gen bị rối chữ,
  hoặc khi dựng workflow có chữ trên ảnh.
---

# SEOSONA Flow — Text in Image (chữ đúng, hết rớt-chữ)

Nguyên tắc gốc (blog typography): **image model KHÔNG tự soi lại chữ nó vẽ → đừng để model là nguồn
sự thật cho chữ.** Cho model quyết *nội dung + vị trí vùng chữ*; để **code deterministic dựng glyph**.

## Chọn 1 trong 2 chế độ

### Mode A — Reserve → Overlay (KHUYẾN NGHỊ, deterministic)
Chữ luôn đúng chính tả/dấu/kerning/ngắt-dòng. Dùng khi có thể overlay ở bước sau.
1. Prompt yêu cầu model render **vùng trống PHẲNG, KHÔNG chữ** (banner/sign/label) ở vị trí muốn — dùng `img_text_reserve`. Nhấn: *"no text, no letters, no typography inside it, generous padding"*.
2. Overlay chữ THẬT bằng font (Be Vietnam Pro): **Text Overlay tool** (`pages/text-overlay-tool.html`, nút "Overlay chữ" ở header) hoặc **node `text_overlay`** trong workflow (template "Poster chữ chuẩn (Reserve→Overlay)", "Thumbnail CTR").
3. Kiểm bằng skill image-qa / `TextIntegrity.compare`. Đổi copy → chỉ re-render overlay, KHÔNG sinh lại ảnh.

### Mode B — Bake-in an toàn (khi KHÔNG overlay được)
Giảm tối đa rủi ro model rối chữ:
- ≤ 3 từ / ≤ ~12 ký tự / MỘT text element / một dòng.
- **ALL-CAPS, chữ Latin phổ thông, KHÔNG dấu tiếng Việt** (â/ế/ữ dễ rối nhất).
- Quote chuỗi chính xác + nói literal: *the sign reads exactly "SALE"*.
- Font sans-serif đậm, tương phản cao, lề rộng, chữ nằm gọn trong khung (không lọt mép).
- Sinh N biến thể → chọn cái chữ đúng (khôi phục "nhiều lượt review").

## Quyết định nhanh
- Cần chữ dài / tiếng Việt có dấu / nhiều dòng → **Mode A bắt buộc**.
- Chỉ 1-3 từ tiếng Anh, không overlay được → Mode B + kiểm kỹ.
- Ảnh đã ra chữ rối → **chuyển sang Mode A** (đừng cố regenerate cầu may).

## Output contract
1. **Chế độ đã chọn** + lý do.
2. **Prompt** (Mode A: prompt chừa-vùng; Mode B: prompt bake-in ràng buộc) + chuỗi chữ literal.
3. **Bước overlay** (Mode A): tool/node nào, vị trí/font/màu/cỡ gợi ý.
4. **Kiểm**: dùng image-qa / TextIntegrity đối chiếu chuỗi đích.

## Cấm
- Để chữ dài / có dấu cho model tự render (gần như chắc chắn rối).
- Khẳng định "chữ đúng" khi chưa OCR-đối-chiếu.
