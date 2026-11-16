---
name: open-notebook
description: "Use when asked to set up a self-hosted NotebookLM, build a private knowledge base from PDFs/videos/web, generate AI podcasts from documents, or run a local research assistant with multiple AI providers. Triggers on: 'open-notebook', 'self-hosted notebooklm', 'private notebooklm', 'local knowledge base', 'research notebook AI', 'AI podcast generator', 'document Q&A self-hosted', 'notebooklm alternative', 'open source notebooklm', 'knowledge base từ PDF', 'tóm tắt tài liệu riêng tư'."
---

# Open Notebook Skill
# Source: lfnovo/open-notebook (MIT) — self-hosted NotebookLM with 18+ AI providers
# Tier: TIER 3 — PRODUCTIVITY

NotebookLM tự host: privacy-first, multi-model, full REST API.
Hỗ trợ PDF, video, audio, web pages → Q&A + podcast tự động.

**Do NOT use for:** `rag-architect` (RAG pipeline custom), `deep-research` (web research agent).

---

## Khi nào dùng

- Cần NotebookLM nhưng không muốn data lên Google
- Tổ chức research từ nhiều nguồn (PDF, YouTube, web, audio)
- Generate podcast từ tài liệu (1-4 speakers, custom voice)
- Knowledge base nội bộ cho team, dùng model local (Ollama)

---

## Cài đặt nhanh (Docker)

```bash
# 1. Lấy docker-compose
curl -O https://raw.githubusercontent.com/lfnovo/open-notebook/main/docker-compose.yml

# 2. Set encryption key
export OPEN_NOTEBOOK_KEY=$(openssl rand -hex 32)

# 3. Chạy
docker compose up -d

# UI tại: http://localhost:8502
```

### Với Ollama (100% local, không cần API key)

```bash
# Thêm vào docker-compose.yml environment:
OPENAI_API_BASE=http://host.docker.internal:11434/v1
OPENAI_API_KEY=ollama
DEFAULT_MODEL=ollama/llama3.2

docker compose up -d
```

### Với Anthropic / OpenAI

```yaml
# docker-compose.yml environment:
ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
OPENAI_API_KEY: ${OPENAI_API_KEY}
DEFAULT_MODEL: claude-sonnet-4-6  # hoặc gpt-4o
```

---

## REST API Patterns

```python
import httpx

BASE = "http://localhost:8502/api"

# Tạo notebook mới
nb = httpx.post(f"{BASE}/notebooks", json={"title": "AI Research 2025"}).json()
nb_id = nb["id"]

# Thêm source — URL
httpx.post(f"{BASE}/notebooks/{nb_id}/sources", json={
    "type": "url",
    "content": "https://arxiv.org/abs/2501.12345"
})

# Thêm source — PDF
with open("paper.pdf", "rb") as f:
    httpx.post(f"{BASE}/notebooks/{nb_id}/sources/upload",
               files={"file": f})

# Chat với notebook
response = httpx.post(f"{BASE}/notebooks/{nb_id}/chat", json={
    "message": "Tóm tắt các điểm chính trong tài liệu này"
}).json()
print(response["answer"])
```

---

## Generate Podcast từ tài liệu

```python
# Tạo podcast từ notebook (2 speakers mặc định)
podcast = httpx.post(f"{BASE}/notebooks/{nb_id}/podcast", json={
    "speakers": 2,
    "duration": "short",   # short | medium | long
    "language": "vi"       # Vietnamese support
}).json()

# Download audio
audio_url = podcast["audio_url"]
```

---

## Multi-source Research Workflow

```python
sources = [
    {"type": "url",     "content": "https://example.com/article"},
    {"type": "youtube", "content": "https://youtube.com/watch?v=ID"},
    {"type": "text",    "content": "Ghi chú thủ công của tôi..."},
]

for src in sources:
    httpx.post(f"{BASE}/notebooks/{nb_id}/sources", json=src)

# Đợi index xong rồi query
result = httpx.post(f"{BASE}/notebooks/{nb_id}/chat", json={
    "message": "So sánh quan điểm các nguồn về chủ đề X"
}).json()
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu dùng Google NotebookLM cho data nhạy cảm — dùng self-hosted
❌ FAIL nếu quên set OPEN_NOTEBOOK_KEY — data không được mã hóa
❌ FAIL nếu expose port 8502 ra internet mà không có auth proxy
✅ PASS khi: UI load tại localhost:8502, source được index, chat trả lời đúng ngữ cảnh
```

## See also
- `rag-architect` — xây RAG pipeline tùy chỉnh từ đầu
- `deep-research` — agent research web tự động
- `agent-reach` — đọc nguồn từ Twitter/Reddit/YouTube để đưa vào notebook
- `mem0` — long-term memory cho agent
