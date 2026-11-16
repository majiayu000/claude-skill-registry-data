---
name: value-investing-checklist
description: Buffett 6-gate checklist for any stock or company. Forces a hard pass/fail verdict with moat scoring, management trust rating, and margin of safety. No hedging, no "it depends". Inspired by ai-berkshire (MIT).
origin: yana-ai — inspired by xbtlin/ai-berkshire (MIT)
license: MIT
version: 1.0.0
triggers:
  - /value-investing-checklist
  - /vic
  - buffett checklist
  - kiểm tra cổ phiếu
  - phân tích đầu tư giá trị
  - checklist đầu tư
---

# /value-investing-checklist

Kiểm tra một công ty qua 6 cổng Buffett. Đầu ra là kết luận rõ ràng: ✅ Đạt / ❌ Không đạt / ❓ Vùng xám — không có "một mặt thì... mặt khác thì...".

```
/value-investing-checklist NVDA
/value-investing-checklist Vinamilk, FPT, MWG
/vic Tesla
```

---

## Khi nào dùng

- Muốn mua một cổ phiếu và cần checklist kỷ luật
- So sánh nhiều công ty trong cùng ngành
- Review lại luận điểm đầu tư đang nắm giữ

## Khi nào KHÔNG dùng

- Trading ngắn hạn / kỹ thuật (dùng chart)
- Tìm hiểu crypto, hàng hóa, trái phiếu
- Cần số liệu real-time để khớp lệnh

---

## Cảnh báo thiên kiến AI trước khi chạy

Trước khi phân tích, đánh giá **mức độ có thể nghiên cứu được** của công ty:

| Hạng | Đặc điểm | Điều chỉnh |
|------|---------|-----------|
| **A** | Lên sàn lâu, dữ liệu dồi dào | Tập trung kiểm tra luận điểm ngược chiều thị trường — tránh output "đúng mà vô nghĩa" |
| **B** | Dữ liệu hạn chế, cần ước tính | Ghi chú rõ chỉ tiêu nào là ước tính + độ tin cậy |
| **C** | Công ty nhỏ, thị trường mới nổi | Chỉ trả lời câu hỏi cốt lõi có thể xác minh được — không cố nhồi đủ 6 cổng |

> **Nguyên tắc**: ít dữ liệu ≠ không chắc. Sự chắc chắn đến từ bản chất mô hình kinh doanh, không phải số lượng báo cáo.

---

## 6 Cổng Checklist

### Cổng 1 — Vòng tròn năng lực (Ability Circle)

> "Never invest in a business you cannot understand." — Buffett

| Câu hỏi | Trả lời |
|---------|---------|
| Công ty kiếm tiền bằng cách nào? (1 câu) | |
| 10 năm nữa vẫn làm gì? | |
| Biến số nào quyết định thành công/thất bại? | |
| Hiểu ngành này từ nghiên cứu hay nghe đồn? | |

**Điểm ★ (1–5):**
- ★★★★★ Cực kỳ đơn giản, tính xác định 10 năm cao (kiểu Coca-Cola)
- ★★★★☆ Mô hình rõ nhưng có ngưỡng chuyên môn
- ★★★☆☆ Hiểu được nhưng ngành thay đổi nhanh
- ★★☆☆☆ Phức tạp, khó đoán 5 năm tới
- ★☆☆☆☆ Ngoài vòng tròn năng lực

**Điểm cứng**: không hiểu cách công ty kiếm tiền → **từ chối phân tích ngay**.

---

### Cổng 2 — Đây có phải mô hình kinh doanh tốt không?

> "I look for businesses in which I think I can predict what they're going to look like in ten to fifteen years' time." — Buffett

Số liệu **phải tra từ nguồn**, không ước tính thô:

| Chỉ số | Giá trị | Chuẩn tham chiếu | Đánh giá |
|--------|---------|-----------------|---------|
| ROE (trung bình 5 năm) | | >15% tốt, >20% xuất sắc | |
| Biên lợi nhuận gộp | | >40% = có định giá | |
| Free Cash Flow | | Dương liên tục ≈ lợi nhuận ròng | |
| Capex / Revenue | | <5% = nhẹ vốn | |

**Điểm ★ (1–5):**
- ★★★★★ FCF dồi dào, ROE >20%, capex nhẹ — kiếm tiền khi ngủ
- ★★★★☆ Mô hình tốt, chỉ số mạnh nhưng chưa đến top
- ★★★☆☆ Trung bình, cần theo dõi
- ★★☆☆☆ Biên thấp hoặc FCF âm có lý do
- ★☆☆☆☆ FCF âm liên tục >3 năm không có lý do cấu trúc → **Từ chối**

---

### Cổng 3 — Hào kinh tế có đủ sâu không?

> "The key to investing is to determine the competitive advantage of any given company." — Buffett

| Loại hào | Có không? | Bằng chứng cụ thể | Đang rộng hay hẹp lại? |
|---------|----------|-----------------|----------------------|
| Thương hiệu / định giá | | | |
| Chi phí chuyển đổi | | | |
| Hiệu ứng mạng lưới | | | |
| Lợi thế quy mô / chi phí | | | |
| Bằng sáng chế / công nghệ | | | |

**Bài kiểm tra nhanh**: Cho đối thủ 10,000 tỷ, họ có copy được không?

**Điểm ★ (1–5):**
- ★★★★★ Nhiều lớp hào chồng nhau và đang mở rộng
- ★★★★☆ Ít nhất 1 hào mạnh và ổn định
- ★★★☆☆ Có hào nhưng không sâu / xu hướng không rõ
- ★★☆☆☆ Hào đang bị xói mòn
- ★☆☆☆☆ Không có hào rõ ràng

---

### Cổng 4 — Ban lãnh đạo có đáng tin không?

> "We look for three things: intelligence, energy, and integrity. If they don't have the last one, the first two will kill you." — Buffett

| Kiểm tra | Đánh giá |
|---------|---------|
| Tỷ lệ cam kết đã thực hiện / tổng cam kết | |
| Phân bổ vốn: M&A, buyback, cổ tức — kết quả? | |
| Mức độ sở hữu cổ phần của CEO | |
| Tinh thần chủ sở hữu (founder vs hired CEO) | |
| Quản trị: giao dịch liên quan, goodwill, kiểm toán | |
| Công ty có chạy tốt nếu thiếu CEO hiện tại? | |

**Điểm ★ (1–5):**
- ★★★★★ Founder nắm quyền, phân bổ vốn xuất sắc, lợi ích hoàn toàn đồng hành cổ đông
- ★★★★☆ Lãnh đạo tốt, có vài điểm cần chú ý
- ★★★☆☆ Đủ năng lực nhưng có rủi ro quản trị nhỏ
- ★★☆☆☆ Có vấn đề về trung thực hoặc quản trị
- ★☆☆☆☆ Vấn đề trung thực nghiêm trọng → **Từ chối ngay**

---

### Cổng 5 — Giá có đủ rẻ không? (Biên an toàn)

> "Price is what you pay. Value is what you get." — Buffett

| Chỉ số | Giá trị | Phân vị lịch sử | Đánh giá |
|--------|---------|----------------|---------|
| P/E (TTM) | | | |
| Forward P/E | | | |
| P/B | | | |
| Tỷ suất cổ tức | | | |
| FCF Yield | | | |

**3 kịch bản định giá** (phải tính, không ước chừng):
- **Lạc quan**: tăng trưởng X%, P/E Y → giá hợp lý Z
- **Cơ sở**: tăng trưởng X%, P/E Y → giá hợp lý Z
- **Bi quan**: tăng trưởng X%, P/E Y → giá hợp lý Z

**Bài kiểm tra tâm lý**: Cổ phiếu mất 50%, anh dám mua thêm không?

**Điểm ★ (1–5):**
- ★★★★★ Dưới 50% giá trị nội tại — cơ hội hiếm
- ★★★★☆ Chiết khấu 30%, biên an toàn tốt
- ★★★☆☆ Định giá hợp lý, biên vừa phải
- ★★☆☆☆ Đắt so với nội tại
- ★☆☆☆☆ Đắt nghiêm trọng

---

### Cổng 6 — Kỷ luật vị thế (Position Discipline)

Kiểm tra tín hiệu cảm xúc:
- [ ] Mua vì FOMO hay vì phân tích?
- [ ] Mua vì người khác khuyên hay vì tự nghiên cứu?
- [ ] Nếu cổ phiếu bị đình chỉ giao dịch 5 năm, anh có chấp nhận không?
- [ ] Luận điểm mua có viết gọn trong 200 chữ không?

---

## Bài kiểm tra gương (Mirror Test)

Viết đầy đủ câu này trước khi mua:

> "Tôi mua [công ty] ở giá [___] vì:
> 1. Mô hình kinh doanh là ___, tôi hiểu nó;
> 2. Hào kinh tế là ___, đang rộng/hẹp ra;
> 3. Ban lãnh đạo ___, đáng/không đáng tin;
> 4. Giá hiện tại tương đương ___% giá trị nội tại, có/không có biên an toàn;
> 5. Nếu tôi sai, rủi ro giảm là kiểm soát được/không, vì ___."

**Không điền đủ 5 câu = không mua. Không có ngoại lệ.**

---

## Danh sách loại nhanh (bất kỳ điều nào = Từ chối)

- [ ] Không giải thích được công ty kiếm tiền bằng cách nào
- [ ] FCF âm >3 năm liên tiếp, không có lý do cấu trúc
- [ ] Lãnh đạo có tiền lệ trung thực kém
- [ ] Lợi thế cạnh tranh đang bị xói mòn không thể đảo ngược
- [ ] Lý do mua chủ yếu là "mọi người đang mua" hoặc "gần đây tăng tốt"
- [ ] Không chịu được tình huống khoản đầu tư về 0
- [ ] Không viết nổi luận điểm trong 200 chữ

---

## Bảng tổng hợp đầu ra

```markdown
## Checklist: [Tên công ty] ([Mã CK])

| Cổng | Tiêu chí | Điểm | Ghi chú |
|------|---------|------|---------|
| 1 | Vòng tròn năng lực | ★/5 | |
| 2 | Mô hình kinh doanh | ★/5 | |
| 3 | Hào kinh tế | ★/5 | |
| 4 | Ban lãnh đạo | ★/5 | |
| 5 | Biên an toàn | ★/5 | |
| 6 | Kỷ luật vị thế | ✅/❌ | |

**Điểm loại nhanh bị kích hoạt**: [có/không — nếu có liệt kê cái nào]

**Bài kiểm tra gương**: [đầy đủ / thiếu câu X]

### Kết luận
✅ **Đạt** (X/5 cổng) — có thể vào giai đoạn nghiên cứu sâu
❌ **Không đạt** — [lý do]
❓ **Vùng xám** — [điểm tranh luận chính, nhà đầu tư cần tự phán đoán gì]

**Rủi ro chính** (3–5 điểm):
1.
2.
3.
```

---

## Nguyên tắc cốt lõi

> "The first rule of investing is don't lose money. The second rule is don't forget the first rule." — Buffett

- **Thà bỏ qua còn hơn làm sai**: Checklist để loại bỏ lựa chọn tệ, không phải tìm lựa chọn tốt nhất
- **Trung thực với vòng tròn năng lực**: không hiểu thì nói không hiểu
- **Biên an toàn là tuyến sống còn**: công ty tốt mua giá đắt vẫn lỗ
- **Không bỏ qua bài kiểm tra gương**: không có ngoại lệ

## Skills liên quan

- `investment-research-team` — 4 agent phân tích song song (Buffett/Munger/段永平/李录 framework)
- `council-of-minds` — 6 nhân vật trí tuệ tranh luận quyết định khó
- `first-principles-thinker` — deconstruct từ gốc như Feynman
