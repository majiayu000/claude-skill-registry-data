---
name: build-capability
description: >-
  Tham chiếu "tự dựng năng lực từ đầu" cho SEOSONA — chưng cất pattern từ build-your-own-x cho các thứ
  SEOSONA hay cần: CLI/sidecar, parser/interpreter (DSL workflow), local search (prompt/memory),
  storage/query layer. Dùng khi cần tự viết 1 công cụ nền (không phụ thuộc lib nặng), hiểu cách 1 hệ
  hoạt động để build lại gọn, hoặc scaffold năng lực mới đúng kiến trúc local-first.
---

# SEOSONA — Build Capability (tự dựng từ đầu, local-first)

Chưng cất build-your-own-x → 4 năng lực SEOSONA hay cần, luôn theo local-first + spec→gate→build.

## Năng lực & cách tiếp cận

### 1. CLI / local sidecar (Node/Go/Rust)
- Server + CLI trong 1 file, **zero-dep** (mẫu motion-anything `motion.js`). Nhận lệnh qua stdin/HTTP.
- Dùng cho: text-overlay batch, caption, reframe — thứ nặng chạy NGOÀI extension qua local-mcp-bridge.

### 2. Parser / interpreter (DSL workflow)
- Tokenize → parse → validate → execute. SEOSONA đã có ở `wf-framework` (schema/validate/operations).
- Mở rộng: thêm node-type = thêm entry catalog + handler executor + validate rule (KHÔNG bịa schema).

### 3. Local search (prompt-pack / memory)
- Inverted index đơn giản (token→entry) hoặc rank-then-load (MemoryStore đã làm: overlap × recency × tier).
- Cho: tìm prompt trong 364 entry, memory.search, template gallery filter. Không cần vector DB.

### 4. Storage / query layer
- chrome.storage.local + serialize (navigator.locks cross-context, đã có) + revision-check (WorkflowRepository).
- Query = load + filter/rank JS. IndexedDB (ImageStore) cho blob nặng.

## Nguyên tắc
- **Local-first**: không thêm cloud/lib nặng khi 1 file JS/CLI làm được.
- **Spec→gate→build** (skill spec-gate-build): viết spec, validate, build từng pass, verify.
- Tái dùng năng lực có sẵn (wf-framework, MemoryStore, ImageStore, local-mcp-bridge) trước khi viết mới.

## Output
- Kiến trúc gọn (1-2 câu) + các module/pass + điểm cắm vào hệ có sẵn + cách verify.
