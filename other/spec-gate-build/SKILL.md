---
name: spec-gate-build
description: >-
  Pattern kiến trúc lõi cho SEOSONA (hội tụ từ website-cloner / img2threejs / prompt-optimizer):
  author SPEC (JSON) → GATE (validate trước khi làm) → BUILD từng pass deterministic → VERIFY bằng
  visual/LLM-diff, chỉ tốn token cho phần phán xét. Dùng khi dựng thứ có cấu trúc (workflow, node-graph,
  trang, pipeline gen nhiều bước) và muốn chắc-đúng thay vì làm một phát rồi sửa.
---

# SEOSONA — Spec → Gate → Build → Verify

Nguyên tắc chủ đạo của toàn hệ: **"AI quyết NỘI DUNG · code deterministic dựng PIXEL"** + không làm-một-phát.
Áp cho mọi thứ có cấu trúc (workflow, pipeline gen, trang, asset-set).

## 4 bước (làm đủ, không nhảy cóc)

### 1. SPEC — viết đặc tả JSON cô đọng TRƯỚC
- Mục tiêu (1 câu), đầu ra mong đợi, ràng buộc, **out-of-scope** (nêu rõ cái KHÔNG làm).
- Với workflow: `{name, category_id, nodes:[{type,data}], edges}` đúng catalog (skill seosona-workflow-architect).
- Spec là hợp đồng — mọi bước sau chiếu về nó.

### 2. GATE — validate spec TRƯỚC khi build
- Kiểm spec đủ/hợp lệ chưa; thiếu thì HỎI hoặc giả định-ghi-rõ, KHÔNG build vội.
- Với workflow: `wf-framework/cli.js validate` = 0 error. Với gen: prompt đủ neo? provider hợp? chi phí ước lượng (CostEstimator) chấp nhận được?
- Gate FAIL → sửa spec, chưa build.

### 3. BUILD — làm từng PASS deterministic, nhỏ
- Chia thành pass độc lập (blockout → chi tiết → hoàn thiện), mỗi pass 1 trách nhiệm.
- Ưu tiên code/công cụ deterministic cho phần "dựng pixel/cấu trúc"; để model lo phần "quyết nội dung".
- Idempotent: làm lại 1 pass không phá pass khác (đổi copy chỉ re-render overlay, không sinh lại ảnh).

### 4. VERIFY — visual/LLM-diff, token CHỈ cho phán xét
- Đối chiếu kết quả từng pass với SPEC bằng 1 lượt review (skill image-qa cho ảnh; validate cho workflow).
- Pre-filter rẻ trước (JS: blur/black-frame/dup, byte-check) → chỉ gọi model/vision cho phần cần phán xét.
- Lệch spec → quay lại BUILD (hoặc SPEC nếu sai gốc). Lặp tới khi diff pass.

## Output contract
1. **SPEC** (JSON/bullet cô đọng) + out-of-scope.
2. **Kết quả GATE** (0 error / các giả định).
3. **Các PASS** đã build (mỗi pass = 1 đơn vị verify được).
4. **VERIFY**: diff vs spec + verdict; nếu chưa đạt → pass nào làm lại.

## Cấm
- Build khi chưa qua GATE.
- Khẳng định "xong/chạy được" khi chưa VERIFY.
- Gộp nhiều bước vào 1 pass không verify được.
- Tốn token model cho việc code làm được (đo/so/gate).
