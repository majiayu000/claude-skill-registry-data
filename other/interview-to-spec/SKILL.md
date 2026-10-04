---
name: interview-to-spec
description: >-
  Chống brief mơ hồ khi gen ẢNH/VIDEO ở SEOSONA Flow — model PHỎNG VẤN người dùng tới khi đủ thông tin
  rồi mới viết spec/prompt (mượn pattern "interview-to-spec" của Claude prompt-library). Dùng khi yêu cầu
  gen còn thiếu (chủ thể/bối cảnh/tỉ lệ/phong cách/mục đích), trước khi sinh prompt hàng loạt, hoặc trong
  node prompt tự động. Kết quả: 1 spec đầy đủ + prompt cụ thể (đã qua anti-slop-visual).
---

# SEOSONA Flow — Interview-to-Spec (hỏi đủ rồi mới sinh)

Brief kiểu "tạo ảnh cô gái đẹp" = thiếu 80% thông tin → ảnh generic. Thay vì đoán, **PHỎNG VẤN có kỷ luật**
tới khi đủ, rồi mới viết spec + prompt. Mượn pattern prompt-library: *"interview me … until we have covered
everything, then write the spec."*

## Quy trình
1. **Hỏi theo checklist** (dưới), MỖI LƯỢT 2–4 câu, ưu tiên cái thiếu nhất. Đừng hỏi cái đã suy ra được.
2. **Đề xuất mặc định** cho mỗi câu (user gật/sửa nhanh hơn tự nghĩ): "Tỉ lệ 9:16 (reel) — ok chứ?".
3. **Dừng khi đủ**: khi mọi mục checklist có giá trị (hoặc user chốt "đủ rồi").
4. **Viết SPEC** (bảng dưới) → rồi **prompt cụ thể**, chạy qua [[anti-slop-visual]] (bỏ cụm sáo) trước khi gen.

## Checklist thông tin (hỏi tới khi đủ)
- **Mục đích**: đăng đâu (reel/thumbnail/ads/banner)? → quyết tỉ lệ + độ dày chữ.
- **Chủ thể**: ai/cái gì? đặc điểm cụ thể (tuổi, trang phục, biểu cảm, số lượng).
- **Bối cảnh**: ở đâu, thời gian, ánh sáng.
- **Phong cách**: 1 phong cách neo (ảnh thật 35mm / gouache / 3D…) — KHÔNG chồng nhiều.
- **Bảng màu / mood**: tông màu chủ đạo, cảm xúc.
- **Tỉ lệ + số lượng**: 9:16 | 16:9 | 1:1…; mấy biến thể.
- **Chữ trên ảnh?**: có/không; nếu có → dùng node Text Overlay (chữ vector, không bake) — xem [[text-in-image]].
- **Ràng buộc**: brand color/logo, cái CẦN TRÁNH (vd "không bóng nhựa", "không chữ tiếng Anh").

## Output — SPEC rồi prompt
| Trường | Giá trị |
|---|---|
| Mục đích / kênh | … |
| Chủ thể (cụ thể) | … |
| Bối cảnh + ánh sáng | … |
| Phong cách (1) | … |
| Màu / mood | … |
| Tỉ lệ · số lượng | … |
| Chữ trên ảnh | có/không (→ Text Overlay) |
| Tránh | … |

→ Sau spec: viết prompt **danh từ/chất liệu/thông số cụ thể**, chèn `{placeholder}` cho phần biến thiên,
qua anti-slop-visual, rồi mới gen (hoặc đưa vào node prompt của workflow).

## Lưu ý
- Với người Việt: hỏi bằng tiếng Việt, prompt gen có thể tiếng Anh (model ảnh mạnh tiếng Anh) trừ khi user muốn khác.
- Đừng phỏng vấn vô tận: 1–2 vòng là đủ cho đa số brief; user nói "đủ" thì dừng ngay.
