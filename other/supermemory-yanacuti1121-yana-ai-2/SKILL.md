---
name: supermemory
description: Persistent memory + RAG + User Profile cho AI agents. #1 LongMemEval benchmark. Thay thế L1/L2 memory thủ công bằng API cloud chuẩn.
triggers:
  - supermemory
  - persistent memory
  - nhớ qua session
  - AI memory
  - long-term memory
  - user profile AI
  - RAG search
  - tìm kiếm ngữ nghĩa
  - agent memory
---

# supermemory — Memory Infrastructure for AI

**Source**: github.com/supermemoryai/supermemory ⭐24k  
**API**: api.supermemory.ai  
**MCP**: mcp.supermemory.ai/mcp  
**Benchmark**: #1 LongMemEval · LoCoMo · ConvoMem

## Setup nhanh (MCP — không cần cài local)

```bash
# Thêm MCP server vào Claude Code
npx -y install-mcp@latest https://mcp.supermemory.ai/mcp --client claude --oauth=yes
```

Hoặc thêm thủ công vào `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "supermemory": {
      "url": "https://mcp.supermemory.ai/mcp",
      "headers": {
        "Authorization": "Bearer sm_YOUR_API_KEY"
      }
    }
  }
}
```

Lấy API key: [app.supermemory.ai](https://app.supermemory.ai)

## 3 khả năng chính

### 1. Memory API — tự học từ conversation

```python
from supermemory import Supermemory
client = Supermemory(api_key=os.environ["SUPERMEMORY_API_KEY"])

# Lưu memory sau mỗi conversation
client.add(
    content="Anh Tâm thích Rust hơn Java, đang dùng Cloud Shell",
    container_tag="tam_profile",
    metadata={"type": "preference", "date": "2026-06-03"}
)

# Tìm context liên quan
context = client.profile(
    container_tag="tam_profile",
    query="thói quen làm việc"
)
print(context.profile)   # user profile tự generate
print(context.memories)  # relevant memories
```

### 2. RAG — tìm kiếm ngữ nghĩa

```python
# Upload tài liệu
client.add(content=open("guide.md").read(), container_tag="yamtam_docs")

# Search hybrid (semantic + keyword)
results = client.search(query="cách cài headroom", container_tag="yamtam_docs")
for r in results.results:
    print(r.content[:200])
```

### 3. User Profile — 50ms latency

```python
# Profile tự build từ memories, cập nhật liên tục
profile = client.profile(container_tag="tam_profile")
# → stable facts + recent activity combined
```

## Tích hợp với YAMTAM L1/L2

| YAMTAM hiện tại | Supermemory thay thế |
|---|---|
| `core/scripts/add-fact.sh` | `client.add(content, container_tag)` |
| L1 INDEX.md manual | `client.profile()` tự generate |
| grep search trong .md files | `client.search()` semantic |
| Session context bị mất | Persistent across sessions |

## Connectors (auto-sync)

```python
# Kết nối Google Drive → tự sync
client.connectors.create(type="google_drive", credentials=...)

# GitHub repo sync
client.connectors.create(type="github", repo="yana-ai")
```

Supported: Google Drive · Gmail · Notion · OneDrive · GitHub

## Install SDK

```bash
pip install supermemory        # Python
npm install supermemory        # TypeScript/Node
```

## Liên quan YAMTAM

- Thay thế `memory/` manual markdown files
- Persistent context qua nhiều session (không mất khi compaction)
- Search ngữ nghĩa qua toàn bộ project history
- User profile Tâm tự cập nhật theo thời gian
