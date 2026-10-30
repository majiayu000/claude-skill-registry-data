---
name: deerflow
description: "ByteDance's open-source super agent harness — spawns parallel sub-agents, Docker sandbox execution, persistent long-term memory, modular skills (research/report/slides). Built on LangChain + LangGraph. Triggers on: 'deerflow', 'deer-flow', 'bytedance agent', 'super agent harness', 'LangGraph agent orchestration', 'multi-hour agent tasks', 'spawn sub-agents', 'agent sandbox docker', 'persistent agent memory', 'agent skills system', 'AI research orchestrator', 'long-running agent tasks', 'agent with memory', 'langgraph orchestrator', 'IM channel agent integration'."
origin: bytedance/deer-flow (Apache-2.0)
license: Apache-2.0
version: "1.0.0"
compatibility: "yana-ai >= 0.41.0"
allowed-tools: Bash, Read, Write, WebFetch
---

# DeerFlow — ByteDance Super Agent Harness
# Source: bytedance/deer-flow (Apache-2.0)
# Tier: TIER 2 — CORRECTNESS

Framework điều phối agent phức tạp, chạy nhiều giờ — sub-agents song song, sandbox Docker, memory dài hạn.

**Do NOT use for:** `terminal--langgraph` (raw LangGraph patterns, không phải DeerFlow framework), `tencent--agent-memory` (memory-only, không có orchestration).

---

## Kiến trúc

```
User request
      ↓
Lead Agent (LangGraph state machine)
      ├─ spawn Sub-Agent A (research)     ← scoped context + tools + termination
      ├─ spawn Sub-Agent B (web search)   ← parallel execution
      └─ spawn Sub-Agent C (code exec)    ← Docker sandbox
             ↓
      Aggregate results
             ↓
      Persistent Memory (long-term user profile)
             ↓
      Output: report / slides / web page / code
```

**Tech stack:** Python 3.12+ · LangChain · LangGraph · TypeScript frontend · Docker · MCP servers

---

## Cài đặt

```bash
# Yêu cầu: Python 3.12+, Node 22+, Docker (optional nhưng khuyến nghị)
git clone https://github.com/bytedance/deer-flow
cd deer-flow

# Backend
cp conf.yaml.example conf.yaml
# Chỉnh conf.yaml: LLM provider, API keys, tool configs

pip install -r requirements.txt

# Frontend
cd web
npm install
npm run build
cd ..

# Khởi động (local)
make dev
# → Backend: http://localhost:8000
# → Frontend: http://localhost:3000
```

```bash
# Docker (production)
docker compose up -d
```

---

## Cấu hình LLM

```yaml
# conf.yaml
llm:
  # Claude (Anthropic)
  provider: anthropic
  model: claude-sonnet-4-6
  api_key: ${ANTHROPIC_API_KEY}

  # Hoặc DeepSeek (chi phí thấp hơn)
  provider: deepseek
  model: deepseek-chat
  api_key: ${DEEPSEEK_API_KEY}

  # Local (Ollama / vLLM)
  provider: openai  # compatible API
  base_url: http://localhost:11434/v1
  model: llama3.2
  api_key: ollama
```

---

## Sub-agent spawning

```python
from deerflow import Agent, SubAgent

# Lead agent tự động spawn sub-agents theo task
lead = Agent(
    name="research-lead",
    max_subagents=5,       # tối đa 5 sub-agents song song
    sandbox=True,          # Docker sandbox cho code execution
    memory=True,           # persistent memory
)

# Sub-agent được spawn với scoped context
class WebResearchAgent(SubAgent):
    tools = ["web_search", "web_browse"]
    max_steps = 20
    termination = "found_sufficient_sources OR steps_exhausted"

# Run task — DeerFlow tự decompose + route
result = await lead.run(
    "Research the latest developments in LLM reasoning and write a 5000-word report"
)
# → Có thể chạy 30-60 phút
# → Output: structured report với citations
```

---

## Sandbox execution

```python
# Code được execute trong Docker container isolated
from deerflow.sandbox import DockerSandbox

sandbox = DockerSandbox(
    image="python:3.12-slim",
    volumes={
        "/uploads": "/workspace/uploads",   # read input files
        "/workspace": "/workspace/code",    # write area
        "/outputs": "/workspace/outputs",   # agent collects results
    },
    network=False,   # no outbound for sandboxed tasks
    memory_limit="512m",
    timeout=300,     # 5 phút per code execution
)

# Agent gọi sandbox khi cần execute code
result = await sandbox.run("python analysis.py --input data.csv")
# → stdout + stderr + output files
```

---

## Persistent memory

```python
from deerflow.memory import UserProfile

# Memory tự động update sau mỗi session
profile = UserProfile(user_id="tam")

# Agent đọc context từ memory
context = await profile.get_context()
# → {
#     "preferences": {"language": "vi", "report_style": "concise"},
#     "expertise": ["AI", "distributed systems", "Vietnam tech"],
#     "recent_topics": ["LLM reasoning", "agent frameworks"]
#   }

# Memory update sau session
await profile.update({
    "recent_session": "Deep research on DeerFlow architecture",
    "decisions": ["Chose DeerFlow over AutoGen for multi-hour tasks"]
})
```

---

## Skills system

```
Built-in skills (modular, loadable):
  deep-research    — multi-source research với citations
  report-gen       — markdown/PDF report từ research results
  slide-creator    — PowerPoint/Keynote generation
  web-page-gen     — HTML page từ content
  code-analysis    — static analysis + refactoring suggestions

Custom skill template:
  deerflow/skills/my-skill/
    __init__.py
    skill.yaml     # name, description, tools required
    handler.py     # async def run(context, inputs) → outputs
```

---

## IM channel integration

```yaml
# conf.yaml — kết nối vào team chat
integrations:
  telegram:
    bot_token: ${TELEGRAM_BOT_TOKEN}
    allowed_users: ["tam_username"]

  slack:
    bot_token: ${SLACK_BOT_TOKEN}
    app_token: ${SLACK_APP_TOKEN}

  feishu:              # Lark — phổ biến ở ByteDance internals
    app_id: ${FEISHU_APP_ID}
    app_secret: ${FEISHU_APP_SECRET}
```

---

## Observability

```python
# LangSmith tracing (debug agent reasoning)
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..."

# Langfuse (self-hosted alternative)
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
```

---

## Security — local deployment

```
⚠ ByteDance's own warning:
  "Deploy only in trusted networks by default"
  "For public deployment: add IP allowlist + authentication gateway"

Recommended setup:
  □ Behind VPN or internal network
  □ Nginx reverse proxy với basic auth
  □ Docker network isolation (no --network=host)
  □ Sandbox code execution (Docker-in-Docker cần cẩn thận)
```

---

## So sánh với các framework khác

| Feature | DeerFlow | AutoGen | CrewAI | LangGraph alone |
|---------|---------|---------|--------|----------------|
| Built-in sandbox | ✅ Docker | ❌ | ❌ | ❌ |
| Persistent memory | ✅ | Partial | Partial | Manual |
| IM integration | ✅ 5+ | ❌ | ❌ | ❌ |
| Skills system | ✅ | ❌ | ✅ | ❌ |
| Multi-hour tasks | ✅ designed for | Partial | Partial | ✅ |
| Observability | LangSmith/Langfuse | ✅ | Partial | LangSmith |
| Production-ready | ✅ ByteDance scale | ✅ | ✅ | DIY |

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu dùng cho simple 1-turn tasks (overkill — dùng direct API call)
❌ FAIL nếu sandbox không isolate network khi execute untrusted code
❌ FAIL nếu persistent memory không update sau session (stale profile)
❌ FAIL nếu sub-agents vượt max_subagents limit (resource exhaustion)
✅ PASS khi: lead agent hoàn thành 10-step research task trong 1 run
✅ PASS khi: memory profile persist đúng sau restart (check DB file)
```

## See also

- `terminal--langgraph` — raw LangGraph patterns (DeerFlow builds on top)
- `tencent--agent-memory` — memory hierarchy chi tiết (bổ sung cho DeerFlow memory)
- `subagent-policy.md` — Yana AI subagent spawn rules (khác DeerFlow model)
- `04-sandbox-isolation-law.md` — sandbox isolation requirements
