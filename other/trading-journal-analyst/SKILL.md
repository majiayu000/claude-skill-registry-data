---
name: trading-journal-analyst
description: Paste your trading history (CSV / broker export / list of trades) and AI extracts hidden behavioral biases, implicit rules, and compares your actual behavior vs an ideal shadow strategy. Inspired by HKUDS/Vibe-Trading Shadow Account Analysis (MIT).
origin: yana-ai — inspired by HKUDS/Vibe-Trading (MIT)
license: MIT
version: 1.0.0
triggers:
  - /trading-journal-analyst
  - /tja
  - phân tích nhật ký giao dịch
  - journal giao dịch
  - trading journal
  - phân tích hành vi giao dịch
  - bias giao dịch
---

# /trading-journal-analyst

Paste lịch sử giao dịch của anh vào. AI sẽ tìm ra điều anh không nhìn thấy trong chính mình: bán lời quá sớm, giữ lỗ quá lâu, chạy theo momentum, overtrade. Sau đó so sánh anh thực sự làm gì vs anh nên làm gì.

```
/trading-journal-analyst
[paste danh sách giao dịch hoặc CSV]

/tja --bias-only   → chỉ phân tích bias, bỏ qua số liệu chi tiết
/tja --compare     → bật Shadow Strategy Comparison
```

**Input được chấp nhận:**
- CSV xuất từ broker (同花顺, 东财, Futu, SSI, VPS, MBS, CSV tự lập)
- Danh sách giao dịch tự nhập theo format: `[ngày] [mã CK] [mua/bán] [giá] [số lượng]`
- Text mô tả ("tháng 3 tôi mua VNM ở 72, bán ở 75, mua MWG ở 45...")

---

## Khi nào dùng

- Nhìn lại quý/năm giao dịch và muốn hiểu mình thực sự hoạt động như thế nào
- Cảm giác "biết đúng nhưng làm sai" và muốn tìm pattern cụ thể
- Muốn rút ra implicit rules từ hành vi thực tế để cải thiện

## Khi nào KHÔNG dùng

- Không có lịch sử giao dịch cụ thể (chỉ ý định mua/bán)
- Muốn phân tích một cổ phiếu (dùng `/vic` hoặc `/irt`)
- Trading kỹ thuật ngắn hạn trong ngày

---

## 5 Bước phân tích

### Bước 1 — Parse & Chuẩn hóa

Chuyển input về format chuẩn:

| Ngày | Mã CK | Hành động | Giá | Số lượng | Giá trị |
|------|-------|----------|-----|---------|---------|

Làm sạch: bỏ duplicate, xử lý split/dividend nếu có, tính P&L từng vị thế.

**Tạo danh sách vị thế đã đóng:**
- Entry date, exit date, holding period (ngày)
- Entry price, exit price
- P&L (VND/USD + %)
- Lý do exit (nếu có trong ghi chú)

---

### Bước 2 — Behavior Profiling

Tính các chỉ số hành vi:

| Chỉ số | Giá trị | Baseline tham chiếu | Nhận xét |
|--------|---------|-------------------|---------|
| Win rate | | 40–55% là bình thường | |
| Avg win % | | | |
| Avg loss % | | | |
| Win/Loss ratio | | >1.5 là tốt | |
| Avg holding (winner) | ngày | | |
| Avg holding (loser) | ngày | | |
| Largest single loss | | | |
| Worst drawdown | | | |
| Số lần giao dịch/tháng | | | |
| Tỷ lệ cắt lỗ đúng hạn | | | |

**Phân phối theo thời gian:** có pattern theo tháng/quý không? (ví dụ: overtrade tháng bull market)

---

### Bước 3 — Phát hiện 4 Bias cốt lõi

#### Bias 1 — Disposition Effect (bán lời sớm, giữ lỗ lâu)
```
Dấu hiệu:
  - Avg holding (winner) < Avg holding (loser)
  - Tỷ lệ win/loss ratio thấp dù win rate cao
  - Nhiều lần bán lúc +5~10% rồi cổ phiếu tiếp tục tăng

Tính toán:
  PGR (Proportion of Gains Realized) vs PLR (Proportion of Losses Realized)
  Disposition coefficient = PGR / PLR
  > 1.0 = có disposition effect
  > 1.5 = nghiêm trọng
```

#### Bias 2 — Overtrading (giao dịch quá nhiều)
```
Dấu hiệu:
  - Số giao dịch/tháng vượt quá "cần thiết"
  - Nhiều giao dịch lãi nhỏ + phí giao dịch ăn mòn profit
  - Turnover cao mà không cải thiện P&L

Tính toán:
  Chi phí giao dịch thực tế / Total P&L
  > 15% → overtrading đáng kể
  > 30% → phí đang giết chết account

Câu hỏi cốt lõi: "Nếu không giao dịch gì trong period X, account sẽ thế nào?"
```

#### Bias 3 — Momentum Chasing (mua muộn đỉnh)
```
Dấu hiệu:
  - Nhiều lần mua sau khi cổ phiếu đã tăng 15-20%+
  - Entry point thường là sau breakout nổi bật trên tin tức
  - Đa phần lệnh vào sau ngày volume đột biến

Tính toán:
  Price change từ đáy gần nhất đến entry point (trung bình)
  > 15% = có xu hướng mua momentum
  > 30% = nghiêm trọng
```

#### Bias 4 — Anchoring (bám vào giá tham chiếu)
```
Dấu hiệu:
  - Thường set stop-loss ở giá mua (thay vì % hợp lý)
  - "Chờ về giá mua rồi bán" khi bị lỗ
  - Target profit đặt ở số tròn (50, 100, +20%)

Nhận dạng:
  Xem pattern exit price vs entry price
  Nhiều exit ở đúng giá mua ± 0-2% = anchoring
```

---

### Bước 4 — Trích xuất Implicit Rules

Từ lịch sử thực tế, rút ra các quy tắc ẩn anh đang áp dụng mà không biết:

**Format:**
```
Quy tắc ẩn được phát hiện:
  IF [điều kiện] THEN [hành động] (tần suất: X/Y lần)

Ví dụ:
  IF cổ phiếu đã tăng >15% trong tuần THEN mua vào (8/12 lần)
  IF lỗ >8% THEN giữ tiếp không cắt (11/15 lần)
  IF thị trường xanh mạnh THEN giao dịch nhiều hơn 2x (pattern Q1 và Q3)
  IF vừa có lãi lớn THEN mua ngay không nghiên cứu kỹ (6/8 lần sau đó lỗ)
```

Sắp xếp theo tần suất và tác động P&L.

---

### Bước 5 — Shadow Strategy Comparison (với `--compare`)

Xây dựng "chiến lược bóng" — phiên bản lý tưởng của anh nếu không bị bias:

```
Shadow Strategy Rules (từ best practices):
  - Cắt lỗ: -8% từ entry, không ngoại lệ
  - Giữ lời: không bán dưới 3 tuần nếu thesis vẫn nguyên vẹn
  - Không mua nếu cổ phiếu đã tăng >20% từ đáy 52 tuần
  - Tối đa 2 giao dịch mới/tháng

Backtest shadow strategy vs actual:
  Kết quả thực:  P&L = [X]
  Shadow result: P&L = [Y]
  Chênh lệch:    [Z] — do [bias chính gây ra]
```

**Đoạn đường bị bỏ lỡ:** liệt kê 3–5 giao dịch cụ thể mà shadow strategy sẽ xử lý khác và kết quả tốt hơn bao nhiêu.

---

## Output chuẩn

```markdown
## Trading Journal Analysis — [Tên/Giai đoạn]

*Giai đoạn: [từ — đến] | [N] giao dịch | [N] cổ phiếu*

---

### Tổng quan hiệu suất

| Chỉ số | Giá trị | Nhận xét |
|--------|---------|---------|
| Tổng P&L | | |
| Win rate | | |
| Avg win / Avg loss | | |
| Avg holding winner | | |
| Avg holding loser | | |
| Chi phí giao dịch | | |

---

### Bias Report

**Disposition Effect**
- Disposition coefficient: [X]
- Mức độ: Không đáng kể / Trung bình / Nghiêm trọng
- Bằng chứng cụ thể: [2–3 giao dịch điển hình]
- Thiệt hại ước tính: [VND/USD]

**Overtrading**
- Giao dịch/tháng: [X] (baseline: Y)
- Chi phí / P&L: [X]%
- Tháng overtrade nhiều nhất: [tháng, lý do thị trường]

**Momentum Chasing**
- Avg price change trước entry: [X]%
- Số lần mua sau tin nóng: [X/N]
- Pattern: [mô tả cụ thể]

**Anchoring**
- Số lần exit ở giá mua: [X/N]
- Số lần "chờ về vốn": [X]
- Stop-loss pattern: [đặt ở đâu thường xuyên]

---

### Implicit Rules đang vận hành

| Quy tắc ẩn | Tần suất | P&L impact |
|-----------|---------|------------|
| [rule 1] | X/Y lần | +/- [Z] |
| [rule 2] | X/Y lần | +/- [Z] |
| [rule 3] | X/Y lần | +/- [Z] |

---

### Shadow Comparison (nếu bật --compare)

| | Thực tế | Shadow | Chênh lệch |
|---|---------|--------|-----------|
| P&L | | | |
| Max drawdown | | | |
| Win rate | | | |

**Top 3 giao dịch shadow xử lý tốt hơn:**
1. [mã CK, ngày, thực tế vs shadow]
2.
3.

---

### Kết luận & Cam kết

**Bias lớn nhất cần sửa ngay:** [tên bias]
**1 quy tắc cụ thể để thay đổi:** [quy tắc]
**Chỉ số theo dõi tháng tới:** [chỉ số]

> Ghi vào journal: "Từ [ngày], tôi cam kết [hành động cụ thể]"
```

---

## Nguyên tắc

- **Dữ liệu thực, không suy đoán**: nếu không có đủ giao dịch để tính toán một bias → nói rõ "không đủ dữ liệu" thay vì ước chừng
- **Số liệu > cảm giác**: bias chỉ được xác nhận khi có pattern thống kê, không phải 1–2 giao dịch
- **Không phán xét**: mục tiêu là nhận diện pattern, không phải chê anh giao dịch tệ

## Skills liên quan

- `value-investing-checklist` — `/vic` — checklist trước khi ra quyết định mua
- `investment-research-team` — `/irt` — 4 agent phân tích cổ phiếu song song
- `council-of-minds` — 6 nhân vật cho quyết định khó
