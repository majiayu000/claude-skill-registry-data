---
name: headroom
description: Context compression for YAMTAM — nén JSON/structured tool output trước khi vào LLM. Hiệu quả với JSON (50-72% tiết kiệm); text thuần cần bản [all].
triggers:
  - headroom
  - compress context
  - nén context
  - giảm token
  - context quá dài
  - tool output lớn
  - context window full
---

# headroom — Context Compression

**Package**: `headroom-ai` v0.22.4 (PyPI + npm)
**License**: Apache 2.0
**Source**: github.com/chopratejas/headroom

## Hiệu quả thực tế (đã test v0.22.4)

| Input type | Kết quả |
|---|---|
| JSON phẳng (100 items) | **~72%** tiết kiệm ✅ |
| JSON lồng (50 items) | **~53%** tiết kiệm ✅ |
| Text thuần, git log | 0% — cần `[all]` extras |
| Conversation history | 0% — `protect_recent` giữ nguyên |

**Khi nào dùng:** API response, RAG chunks, MANIFEST/JSON lớn.
**Không nên dùng cho:** git log thuần, prose, file .md.

## Cách dùng đúng

### 1. JSON / API response (hoạt động tốt nhất)

```python
from headroom import compress
import json

# Nén JSON response trước khi đưa vào messages
data = json.dumps(large_api_response)
messages = [{"role": "user", "content": data}]

result = compress(messages, compress_user_messages=True, target_ratio=0.3)
print(f"{result.tokens_before:,} → {result.tokens_after:,} tokens ({result.compression_ratio*100:.1f}%)")

# Dùng messages đã nén
compressed = result.messages
```

### 2. Context gần đầy — auto compress khi cần

```python
from headroom import compress

# headroom chỉ nén khi tokens gần model_limit
# Mặc định: model="claude-sonnet-4-5", limit=200K
result = compress(messages)  # nén nếu > 80% limit

# Chỉ định model cụ thể
result = compress(messages, model="claude-opus-4-20250514")
```

### 3. Force compress (không quan tâm đến limit)

```python
result = compress(
    messages,
    compress_user_messages=True,  # compress cả user messages
    target_ratio=0.3,              # giữ lại 30% tokens
    protect_recent=0,              # không bảo vệ messages gần đây
)
```

### 4. Wrap Claude Code (cần `[all]`)

```bash
pip install "headroom-ai[all]"
headroom wrap claude        # wrap Claude Code — nén tự động
headroom proxy --port 8787  # drop-in proxy, zero code change
```

### 5. MCP Server

```bash
headroom mcp install
# Tools: headroom_compress, headroom_retrieve, headroom_stats
```

## Tích hợp YAMTAM hooks

```json
{
  "type": "command",
  "command": "headroom init hook ensure",
  "timeout": 15
}
```

## Install

```bash
pip install headroom-ai            # base: JSON compression
pip install "headroom-ai[all]"    # full: proxy + MCP + ML (text compression)
npm install headroom-ai            # TypeScript/Node
```

## Anti-Fake-Pass

- `compress(messages)` với messages nhỏ → 0% (bình thường, chưa cần nén)
- `compress_user_messages=True` bắt buộc để nén user messages
- Text thuần không nén được bằng base package — đừng ghi "60-95%" khi chưa test
- `compression_ratio` = 1 - (after/before), không phải phần trăm tiết kiệm trực tiếp
