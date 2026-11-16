---
name: investment-research-team
description: 4-agent parallel investment research team modeled after legendary investors. business-analyst (Duan Yongping lens), financial-analyst (Buffett lens), industry-researcher (Munger lens), risk-assessor (Li Lu lens). team-lead synthesizes into a single verdict. Inspired by ai-berkshire (MIT).
origin: yana-ai — inspired by xbtlin/ai-berkshire (MIT)
license: MIT
version: 1.0.0
triggers:
  - /investment-research-team
  - /irt
  - nghiên cứu đầu tư
  - research đầu tư
  - phân tích cổ phiếu chuyên sâu
  - investment research team
---

# /investment-research-team

4 agent nghiên cứu song song, mỗi người nhìn từ một góc độ nhà đầu tư huyền thoại khác nhau. team-lead tổng hợp thành một kết luận duy nhất với mức độ thuyết phục rõ ràng.

```
/investment-research-team NVDA
/investment-research-team Vinamilk --horizon 5y
/irt Tesla --quick
```

---

## Khi nào dùng

- Muốn nghiên cứu sâu một công ty trước khi đưa ra quyết định lớn
- Cần nhiều góc nhìn độc lập về cùng một cổ phiếu
- Đã qua `/value-investing-checklist` và muốn đào sâu thêm

## Khi nào KHÔNG dùng

- Cần câu trả lời nhanh (dùng `/vic`)
- Trading kỹ thuật ngắn hạn
- Crypto, hàng hóa, bất động sản

---

## 4 Thành viên nhóm nghiên cứu

| Agent | Hình mẫu | Câu hỏi cốt lõi |
|-------|---------|----------------|
| **business-analyst** | 段永平 (Duan Yongping) | Mô hình kinh doanh có đúng không? Người dùng có thực sự cần không? |
| **financial-analyst** | Warren Buffett | Số liệu tài chính có thuyết phục không? Định giá có hợp lý? |
| **industry-researcher** | Charlie Munger | Ngành có cấu trúc tốt không? Cạnh tranh sẽ đi về đâu? |
| **risk-assessor** | 李录 (Li Lu) | Rủi ro dài hạn là gì? Ban lãnh đạo có đủ tầm không? |

---

## Quy trình phân tích

### Bước 1 — Phân công và thu thập song song

4 agent làm việc độc lập, không chia sẻ dữ liệu với nhau cho đến khi hoàn thành.

**business-analyst nhìn theo Duan Yongping:**
```
Duan Yongping (段永平): founder步步高, nhà đầu tư sớm vào NetEase và Apple.
Triết lý: "Làm điều đúng, đừng làm điều sai" — tập trung vào sự đơn giản và
tính đúng đắn của mô hình kinh doanh thay vì các chỉ số tài chính phức tạp.

Câu hỏi của business-analyst:
1. Công ty tạo ra giá trị gì cho người dùng? (không phải cổ đông)
2. Mô hình kinh doanh có đơn giản và dễ hiểu không?
3. Có hiệu ứng vô hình (flywheel) nào đang hoạt động?
4. 10 năm nữa công ty này có còn cần thiết không?
5. Nếu Duan bỏ 10 triệu USD vào đây hôm nay, ông có lo ngại gì?
```

**financial-analyst nhìn theo Buffett:**
```
Warren Buffett: nhà đầu tư giá trị, chairman Berkshire Hathaway.
Triết lý: ROE bền vững, FCF dồi dào, giá cả phải chăng so với nội tại.

Câu hỏi của financial-analyst:
1. ROE 5–10 năm? Tăng hay giảm?
2. Biên lợi nhuận gộp và ròng ổn định không?
3. FCF/Earnings ratio — lợi nhuận có được chuyển thành tiền mặt thực sự?
4. Nợ có kiểm soát được? Interest coverage bao nhiêu lần?
5. Tại mức giá hiện tại, yield on cost sau 10 năm là bao nhiêu (kịch bản cơ sở)?
```

**industry-researcher nhìn theo Munger:**
```
Charlie Munger: partner Buffett, "nghiện" mental models và đảo ngược vấn đề.
Triết lý: "Invert, always invert" — hiểu ngành bằng cách hỏi "điều gì sẽ giết chết công ty này?"

Câu hỏi của industry-researcher:
1. Cấu trúc ngành theo Porter 5 Forces — ai có quyền lực nhất?
2. Xu hướng ngành 10 năm tới: disruption đến từ đâu?
3. Điều gì sẽ giết chết công ty này? (Invert)
4. Công ty có vị thế tốt nhất trong ngành về mặt cơ cấu không?
5. Nếu Munger không mua công ty này, ông sẽ nói lý do gì?
```

**risk-assessor nhìn theo Li Lu:**
```
李录 (Li Lu): founder Himalaya Capital, học trò Buffett/Munger, chuyên thị trường châu Á.
Triết lý: xác suất + kết quả — rủi ro là "không biết cái gì không biết."

Câu hỏi của risk-assessor:
1. Rủi ro nào thị trường đang bỏ qua hoàn toàn?
2. Ban lãnh đạo có "tầm nhìn đạo đức" không (integrity + vision)?
3. Rủi ro địa chính trị, quy định nếu có?
4. Vòng tròn năng lực: có hiểu đủ để biết cái gì không biết không?
5. Kịch bản tệ nhất (tail risk) trông như thế nào?
```

---

### Bước 2 — Mỗi agent nộp báo cáo ngắn

Mỗi báo cáo gồm **3 phần**:

```markdown
### [Tên agent] — [Tên công ty]

**Phát hiện chính** (3–5 điểm):
- [điểm 1]
- [điểm 2]
- [điểm 3]

**Luận điểm tổng thể** (1–2 câu): [kết luận của agent]

**Tín hiệu cảnh báo** (nếu có): [điều làm agent lo ngại nhất]
```

---

### Bước 3 — team-lead tổng hợp

team-lead (không có "nhân cách" huyền thoại cụ thể — vai trò: synthesis + verdict):

```
Nguyên tắc của team-lead:
- Không san phẳng bất đồng — bất đồng là thông tin
- Nếu 3/4 agent có cùng một lo ngại → đó là rủi ro cốt lõi
- Nếu agent bất đồng nhau → trình bày điểm bất đồng, không giả vờ đồng thuận
- Kết luận phải là PASS / FAIL / GRAY — không phải "đáng để xem xét thêm"
```

---

## Output chuẩn

```markdown
## Investment Research: [Tên công ty] ([Mã CK])

*Ngày phân tích: [YYYY-MM-DD] | Giá tham chiếu: [___]*

---

### 📊 business-analyst (段永平 lens)

**Phát hiện chính:**
- Mô hình kinh doanh: [1 câu]
- Giá trị người dùng: [1 câu]
- Flywheel: [có/không, mô tả ngắn]
- Sức bền 10 năm: [đánh giá]
- Điểm lo ngại nhất: [1 câu]

**Kết luận business-analyst:** [Đây có phải mô hình kinh doanh đúng không?]

---

### 💰 financial-analyst (Buffett lens)

**Phát hiện chính:**
| Chỉ số | Giá trị | Xu hướng | Đánh giá |
|--------|---------|---------|---------|
| ROE TB 5Y | | | |
| Biên lợi nhuận gộp | | | |
| FCF Yield | | | |
| Nợ/EBITDA | | | |
| P/E vs ngành | | | |

**3 kịch bản định giá:**
- Lạc quan: [tăng trưởng X% → giá trị nội tại Y]
- Cơ sở: [tăng trưởng X% → giá trị nội tại Y]
- Bi quan: [tăng trưởng X% → giá trị nội tại Y]

**Kết luận financial-analyst:** [Giá có hợp lý so với nội tại?]

---

### 🏭 industry-researcher (Munger lens)

**Phát hiện chính:**
- Cấu trúc ngành: [tóm tắt Porter 5 Forces]
- Xu hướng 10 năm: [cơ hội hoặc mối đe dọa chính]
- Rủi ro disruption: [thấp/trung/cao — từ đâu?]
- Vị thế cạnh tranh: [top tier / trung bình / yếu]

**Invert test**: Điều gì sẽ giết chết công ty này?
→ [câu trả lời cụ thể]

**Kết luận industry-researcher:** [Ngành có cấu trúc cho phép kiếm tiền bền vững?]

---

### ⚠️ risk-assessor (Li Lu lens)

**Phát hiện chính:**
- Rủi ro thị trường đang bỏ qua: [1–2 điểm]
- Chất lượng ban lãnh đạo: [cao/trung/thấp + lý do]
- Rủi ro địa chính trị/quy định: [nếu có]
- Tail risk (kịch bản tệ nhất): [mô tả cụ thể]

**Kết luận risk-assessor:** [Có "cái gì không biết" đang ẩn nấp không?]

---

### 🎯 Tổng hợp — team-lead

**Điểm đồng thuận** (≥3/4 agent đồng ý):
- [điểm 1]
- [điểm 2]

**Điểm bất đồng** (nếu có):
- [agent A vs agent B về vấn đề gì]

**Rủi ro cốt lõi** (được ≥3 agent nhắc đến):
1. [rủi ro 1]
2. [rủi ro 2]

**Câu hỏi còn mở** (chưa có câu trả lời rõ):
- [câu hỏi cần thêm thông tin để quyết định]

---

### Phán quyết cuối

| Tiêu chí | Kết quả |
|---------|---------|
| Mô hình kinh doanh | ✅/❌/❓ |
| Tài chính | ✅/❌/❓ |
| Cấu trúc ngành | ✅/❌/❓ |
| Rủi ro | ✅/❌/❓ |

**Kết luận:**
✅ **PASS** — Đủ điều kiện nghiên cứu sâu / vào vị thế thử nghiệm
❌ **FAIL** — [lý do chính]
❓ **GRAY** — [điều quyết định, nhà đầu tư cần tự phán đoán]

**Mức độ thuyết phục:** Cao / Trung bình / Thấp
**Lý do:** [1–2 câu]

**Bước tiếp theo gợi ý:** [cụ thể — không phải "nghiên cứu thêm"]
```

---

## Quick Mode (`--quick`)

Chỉ chạy 2 agent: **financial-analyst + risk-assessor**

Dùng khi:
- Đã biết mô hình kinh doanh rồi
- Muốn check nhanh số liệu + rủi ro trước quyết định

Output ngắn hơn — bỏ section industry-researcher và business-analyst.

---

## Horizon flag (`--horizon`)

Mặc định: 5 năm

```
--horizon 3y   → short-term: tập trung vào momentum và catalyst gần
--horizon 5y   → medium-term: cân bằng tăng trưởng + định giá (default)
--horizon 10y  → long-term: ưu tiên moat và bền vững mô hình kinh doanh
```

---

## Nguyên tắc nhóm

```
1. Không san phẳng bất đồng — bất đồng giữa các agent là tín hiệu quan trọng
2. Số liệu từ nguồn — không ước tính thô
3. Kết luận rõ ràng — không "có thể cân nhắc"
4. Bài kiểm tra gương bắt buộc nếu kết quả là PASS
5. Rủi ro tail được đặt ngang hàng với luận điểm tích cực
```

---

## Skills liên quan

- `value-investing-checklist` — `/vic` — checklist 6 cổng Buffett trước khi chạy team
- `council-of-minds` — 6 nhân vật trí tuệ cho quyết định chiến lược
- `first-principles-thinker` — deconstruct mô hình kinh doanh từ gốc
