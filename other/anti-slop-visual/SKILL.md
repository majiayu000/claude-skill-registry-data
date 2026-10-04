---
name: anti-slop-visual
description: >-
  Diệt "AI slop" trong PROMPT ẢNH/VIDEO của SEOSONA Flow — chuyển phương pháp no-ai-slop (liệt kê cụm
  tố-cáo cần cấm) từ văn xuôi sang THỊ GIÁC. Dùng khi viết/tinh prompt gen, review prompt trong kho, hoặc
  làm node prompt tự động: cấm token sáo rỗng (8k/masterpiece/trending on artstation), ép danh từ·chất
  liệu·ánh sáng·ống kính CỤ THỂ thay tính từ mơ hồ. Có eval.md để test rule bắn đúng.
---

# SEOSONA Flow — Anti-Slop cho prompt ẢNH/VIDEO

"AI slop" thị giác = prompt nhồi từ khoá hào nhoáng nhưng RỖNG → model trả ảnh generic, bóng nhựa, vô hồn.
Cách chữa (mượn no-ai-slop): **liệt kê cụm-tố-cáo cần cấm → vì sao slop → cách thay bằng cái CỤ THỂ.**

## Danh sách CẤM (tell → vì sao → thay bằng)

| Cụm slop (CẤM) | Vì sao rỗng | Thay bằng (cụ thể) |
|---|---|---|
| `8k, 4k, ultra HD, hyper-detailed` | không phải nội dung, chỉ là nhãn "đẹp" | mô tả chi tiết THẬT: "sợi vải lanh dệt thô", "vết xước trên đồng thau" |
| `masterpiece, best quality, award-winning` | tự khen, model bỏ qua/quá tay | bối cảnh/độ khó THẬT: "chân dung studio 1 đèn key mềm" |
| `trending on artstation, deviantart` | phong cách chung chung, sáo | tên chất liệu/kỹ thuật: "gouache trên giấy ráp", "in risograph 2 màu" |
| `cinematic lighting, dramatic lighting` (trần trụi) | ai cũng viết → vô nghĩa | hướng+chất sáng: "ngược sáng hoàng hôn, rim light viền tóc, đổ bóng dài" |
| `beautiful, stunning, gorgeous, epic` | tính từ cảm thán, 0 thông tin | danh từ + đặc điểm: "gò má cao, tàn nhang, mắt nâu bắt sáng" |
| `highly detailed, intricate details` | nói "chi tiết" ≠ có chi tiết | LIỆT KÊ chi tiết: "ren tay áo, cúc ngọc trai, chỉ khâu vàng" |
| `photorealistic, realistic` (đứng 1 mình) | model ảnh mặc định đã thực | thông số máy: "ống 85mm, khẩu f/1.8, DOF nông" |
| `perfect face, flawless skin` | gây bóng-nhựa/uncanny | "da tự nhiên có lỗ chân lông, catchlight trong mắt, KHÔNG làm mịn quá" |

## 4 nguyên tắc thay thế
1. **Danh từ/chất liệu > tính từ mơ hồ.** "áo len cáp xám" > "beautiful sweater".
2. **Số cụ thể > trừu tượng.** "3 nhân vật, tỉ lệ 9:16, 85mm" > "detailed scene".
3. **Phủ định CÓ NGÂN SÁCH — tối đa ~5 cụm, và ưu tiên viết lại thành khẳng định.**
   Phủ định ngắn, đúng chỗ thì hiệu quả ("KHÔNG bóng nhựa"). Nhưng một danh sách 40–80 thứ
   mình sợ thì phản tác dụng: model không phân biệt tốt ý phủ định, nên liệt kê
   `extra fingers, malformed hands, duplicated object` **làm tăng** xác suất chúng hiện ra.
   Cách chắc hơn: nói điều MÌNH MUỐN. "hai bàn tay đủ năm ngón, đặt rõ trên đùi" thay cho
   "no extra fingers, no malformed hands, no missing fingers".
4. **1 phong cách neo, không chồng 5 style.** Chọn 1 (gouache / risograph / film 35mm), tả sâu — đừng "cinematic + anime + oil painting + 8k".

## 3 luật về ĐỘ DÀI & PHẠM VI (thêm 2026-08, từ vụ prompt outpaint 950 từ)

**A. Đừng viết mục `NEGATIVE PROMPT:` cho provider chỉ có MỘT ô text.**
Flow, Nano Banana, Veo qua UI **không có trường negative riêng**. Cả khối đó bị đọc như
prompt **dương** — vừa vô hiệu, vừa dính đúng bẫy ở nguyên tắc 3. Negative prompt là khái
niệm của ComfyUI/SD có CFG hai nhánh, không phải của Flow.

**B. Trần độ dài thực dụng: 120–200 từ cho ảnh, 80–150 cho video.**
Dài hơn thì attention loãng. Kiểm nhanh: đếm tỉ lệ câu **chỉ đạo** so với câu **cấm đoán** —
dưới 50% chỉ đạo là prompt đã hỏng. (Prompt outpaint 950 từ nọ chỉ có ~15% chỉ đạo, phần
còn lại là ~85 lệnh cấm, nhiều cái lặp 3 lần.)

**C. Số kỹ thuật phải nằm trong khả năng THẬT của provider.**
Flow: tải tối đa **4K = 4096px**; ratio ảnh `16:9 4:3 1:1 3:4 9:16`, video `16:9 9:16`;
thời lượng `4s 6s 8s 10s`; tối đa 10 ảnh ref. Ghi `8K / 7680×4320` là token rác — model bỏ
qua và bạn tự đánh lừa mình là đã yêu cầu.

**Không tự mâu thuẫn.** `do not enhance` đứng cùng `increase sharpness` buộc model chọn một
bên, và bạn không kiểm soát được nó chọn bên nào.

**Việc code làm chắc thì đừng giao cho prompt.** Hai ca hay gặp nhất:
- *Giữ nguyên pixel vùng tâm* → không câu chữ nào làm được (model tái sinh toàn khung).
  Dùng node **Ghép ảnh** dán ảnh gốc đè lên.
- *Chữ đúng chính tả, đủ dấu tiếng Việt* → đừng để AI vẽ chữ. Reserve→Overlay, xem [[text-in-image]].

## Cách dùng
- **Viết prompt**: bỏ mọi cụm ở cột CẤM; với mỗi cụm định viết, hỏi "cái này thêm THÔNG TIN gì?" — không thì bỏ.
- **Review kho prompt** (BundledPrompts 410): quét `content` chứa cụm cấm → cờ để sửa.
- **Ghép**: dùng chung [[anti-slop-visual]] với skill viết prompt hiện có; đây là lớp LINT cuối trước khi gen.
- Test rule: xem `eval.md` (prompt bẩn mẫu → cờ kỳ vọng).

## Lưu ý scope
- Đây là kỷ luật **văn bản prompt** (thuần text, chạy được mọi nơi). KHÔNG phải bộ lọc ảnh. Chất lượng ẢNH
  đầu ra vẫn do model (Flow/Veo) + QA hình (skill image-qa/mllm-judge) lo.
