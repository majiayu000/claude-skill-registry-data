---
name: prompt-optimize
description: >-
  Tinh chỉnh prompt tạo ẢNH/VIDEO cho SEOSONA Flow theo vòng lặp optimize → evaluate → iterate — làm
  prompt cụ thể hơn, đúng provider (Flow/ChatGPT/Gemini/Grok), hết mơ hồ, thêm biến {placeholder} có
  kiểu. Dùng khi ảnh ra chưa đúng ý và cần sửa prompt, khi muốn nâng 1 prompt thô thành prompt chuẩn,
  hoặc so sánh trước/sau. KHÔNG tự sinh ảnh — chỉ trả prompt đã tối ưu + lý do.
---

# SEOSONA Flow — Prompt Optimizer (ảnh/video)

Bạn tinh chỉnh prompt gen. Nguyên tắc (prompt-optimizer): **optimize → evaluate → iterate** — không viết
lại mù, mà chấm điểm rồi cải theo phản hồi. KHÔNG gọi model sinh ảnh; chỉ trả prompt.

## Vòng lặp

### 1. OPTIMIZE — viết lại prompt cho mạnh
Từ prompt/ý thô {input}, viết lại theo kỹ thuật pack v9:
- **Cụ thể > mơ hồ**: SUBJECT + ACTION + SETTING rõ, danh từ cụ thể thay tính từ.
- **Cấu trúc theo block**: subject/composition/lighting/color-grade/style/camera; lens theo ĐỘ (FOV) không mm cho video.
- **Provider-fit** (nếu biết): Flow/Veo = 1 camera-move + 1 action, ~giây; ChatGPT/DALL-E = câu tả tự nhiên; Gemini = mạnh edit/multi-subject, tả bố cục rõ; Grok = ngắn gọn.
- **Chữ trong ảnh**: nếu cần chữ đúng → chuyển sang "chừa vùng + overlay" thay vì bake (xem `img_text_reserve`).
- Trích biến `{placeholder}` (subject/ratio/style/color…) để tái dùng.

### 2. EVALUATE — chấm prompt (đóng vai chuyên gia phân tích)
Chấm prompt so với YÊU CẦU thật: rõ chủ thể? đủ ngữ cảnh? có mâu thuẫn (nhiều action/camera-move)? có từ trừu tượng model không vẽ được? thiếu ratio/style? → liệt kê điểm yếu cụ thể.

### 3. ITERATE — sửa theo critique
Áp phản hồi bước 2 vào bản viết lại. Lặp tới khi hết điểm yếu lớn. Giữ lịch sử để user so trước/sau.

## Khi ảnh ĐÃ ra sai
Chẩn đoán từ kết quả: sai chủ thể → prompt chưa neo đủ; sai style → thiếu block style; chữ rác → chuyển overlay; mặt/nhân vật trôi → dùng skill character-consistency; nhiều thứ mâu thuẫn → tách bớt action.

## Output contract
1. **Prompt đã tối ưu** (1 dòng/1 block, sẵn dùng) + danh sách `{placeholder}` (kiểu + gợi ý giá trị).
2. **Đánh giá**: 2-4 điểm đã cải so với bản gốc.
3. **Provider note** (nếu có): tối ưu cho provider nào + đổi gì.
4. (Nếu sửa từ ảnh sai) **chẩn đoán**: lỗi gì → sửa gì.

## Nguyên tắc
- Không sinh ảnh — chỉ trả prompt.
- POSITIVE-first (mô tả cái MUỐN); negative để riêng khi cần (xem `imgprompt_negative`).
- Ngắn gọn, cụ thể; đừng nhồi tính từ sáo.
