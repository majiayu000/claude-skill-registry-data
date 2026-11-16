---
name: token-capped-workflow
description: "Design a task workflow under an explicit token cap (e.g. 10k total) — allocate budget per phase, verify the most critical part first, and degrade gracefully when the cap nears. Use when asked to 'giới hạn token', 'làm trong 10k token', 'token cap cho task này', 'budget workflow', 'tiết kiệm chi phí cho task', 'cheap mode', or 'work within a token limit'. Do NOT use for: choosing response length/depth — see token-budget-advisor. Do NOT use for: auditing context window bloat — see context-budget. Do NOT use for: cost-per-value scoring — see token-roi."
tier: TIER 4 — TOKEN OPTIMIZATION
source: yana-ai (anh Tâm prompt pack, 2026-06-10)
---

# Token-Capped Workflow — Làm việc trong hạn mức token

Giới hạn tổng chi phí token cho một tác vụ cụ thể, ép ưu tiên kiểm chứng
phần quan trọng nhất trước, và xuống cấp có kiểm soát khi gần chạm trần.

> Prompt gốc: *"Tạo workflow cho task này, nhưng giới hạn tổng chi phí ở
> khoảng 10k token, ưu tiên kiểm chứng phần quan trọng nhất trước."*

---

## Khi nào dùng

- Task lặp lại nhiều lần (batch) — tiết kiệm nhân theo số lần chạy
- Session sắp cạn budget nhưng việc chưa xong
- Task exploratory chưa chắc đáng đầu tư — cap thấp để thăm dò
- Chạy trên backup stack có quota chặt (Groq/Gemini free tier)

## Phân bổ chuẩn cho cap 10k

```
┌──────────────────────────────────────────────┐
│ 1. SCOPE      ~10%  (1k)  — đọc đề, chốt phạm vi│
│ 2. VERIFY-CORE ~30% (3k)  — kiểm phần QUAN TRỌNG │
│                            NHẤT trước tiên       │
│ 3. EXECUTE    ~40%  (4k)  — làm phần chính       │
│ 4. CHECK      ~15%  (1.5k)— verify kết quả       │
│ 5. RESERVE    ~5%   (0.5k)— dự phòng lỗi         │
└──────────────────────────────────────────────┘
```

**Verify-first là bắt buộc:** phần quan trọng nhất phải được kiểm chứng
TRƯỚC khi tiêu token vào phần phụ. Hết budget giữa chừng mà core đã
verify = vẫn có giá trị. Hết budget mà core chưa check = công cốc.

## Kỹ thuật tiết kiệm theo bước

| Bước | Kỹ thuật |
|------|----------|
| Đọc file | Read có `offset/limit`, grep trước đọc sau — không đọc cả file |
| Search | Grep với pattern hẹp, `head_limit` — không dump cả output |
| Sinh code | Diff/edit thay vì viết lại cả file |
| Báo cáo | Bullet ngắn, bỏ giải thích lặp — kết quả trước, lý do 1 câu |
| Lặp | Không re-read file vừa edit; không re-run lệnh đã có kết quả |

## Checkpoint trần

```
50% cap — tự hỏi: core đã verify chưa? Chưa → dừng EXECUTE, quay lại VERIFY
80% cap — chỉ còn được: hoàn thiện + báo cáo. Không mở thêm phạm vi mới
100% cap — DỪNG. Báo: đã làm gì, còn gì, cần thêm bao nhiêu token để xong
```

Vượt cap không xin phép = vi phạm. Báo trước, đợi quyết định.

## Format khai báo đầu task

```markdown
## Token Plan — <task>
Cap: 10k | Core cần verify trước: <phần X — vì sao nó quan trọng nhất>
Phân bổ: scope 1k · verify 3k · execute 4k · check 1.5k · reserve 0.5k
Ngoài phạm vi (không tiêu token): <liệt kê>
```

## Anti-Fake-Pass

```
❌ Nhận cap nhưng không khai báo Token Plan trước khi làm
❌ "Ước lượng" token bằng cảm giác sau khi đã vượt — checkpoint phải
   diễn ra TẠI 50%/80%, không phải hồi tưởng cuối task
❌ Hết budget rồi im lặng bỏ bước CHECK — phải báo rõ bước nào bị cắt
❌ Verify phần dễ trước (cho nhanh) thay vì phần quan trọng nhất
❌ Lách cap bằng cách tách thành nhiều request nhỏ không khai báo
   (vi phạm 60-token-budget-velocity-law)
```

## See also

- `token-budget-advisor` — chọn độ sâu câu trả lời theo ý user
- `context-budget` — audit context window bị phình do components
- `token-roi` — tính ROI trước khi nhận task đắt
- `token-budget-policy.md` / `60-token-budget-velocity-law.md` — luật cứng
