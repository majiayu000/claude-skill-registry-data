---
name: elite-longterm-memory-zh
version: 1.2.3
description: "终极 AI Agent 记忆系统，适用于 Cursor、Claude、ChatGPT 和 Copilot。WAL 协议 + 向量搜索 + Git Notes + 云备份。永不丢失上下文，为 Vibe-coding 而生。"
author: NextFrontierBuilds
keywords: [memory, ai-agent, ai-coding, long-term-memory, vector-search, lancedb, git-notes, wal, persistent-context, claude, claude-code, gpt, chatgpt, cursor, copilot, github-copilot, openclaw, moltbot, vibe-coding, agentic, ai-tools, developer-tools, devtools, typescript, llm, automation]
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env:
        - OPENAI_API_KEY
      plugins:
        - memory-lancedb
---

# 精英长期记忆系统 🧠

**终极 AI Agent 记忆系统。** 将 6 种经过验证的方法整合为一个坚不可摧的架构。

永不丢失上下文。永不遗忘决策。永不再犯同样错误。

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                    精英长期记忆系统                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   热内存    │  │   温存储    │  │   冷存储    │             │
│  │             │  │             │  │             │             │
│  │ SESSION-    │  │  LanceDB    │  │  Git-Notes  │             │
│  │ STATE.md    │  │  向量搜索   │  │  知识图谱   │             │
│  │             │  │             │  │             │             │
│  │ (在压缩中   │  │ (语义搜索)  │  │ (永久决策)  │             │
│  │  存活)      │  │             │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │  MEMORY.md  │  ← 精选长期记忆                │
│                  │  + daily/   │    (人类可读)                  │
│                  └─────────────┘                                │
│                          │                                      │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │ SuperMemory │  ← 云备份（可选）              │
│                  │    API      │                                │
│                  └─────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 5 层记忆架构

### 第 1 层：热内存 (SESSION-STATE.md)
**来源：bulletproof-memory**

在压缩中存活的活跃工作记忆。预写日志（WAL）协议。

```markdown
# SESSION-STATE.md — 活跃工作记忆

## 当前任务
[我们现在正在做什么]

## 关键上下文
- 用户偏好：...
- 已做决策：...
- 阻塞问题：...

## 待处理操作
- [ ] ...
```

**规则：** 在响应之前写入。由用户输入触发，而非 Agent 记忆。

### 第 2 层：温存储 (LanceDB 向量)
**来源：lancedb-memory**

跨所有记忆的语义搜索。自动召回注入相关上下文。

```bash
# 自动召回（自动发生）
memory_recall query="项目状态" limit=5

# 手动存储
memory_store text="用户偏好深色模式" category="preference" importance=0.9
```

### 第 3 层：冷存储 (Git-Notes 知识图谱)
**来源：git-notes-memory**

结构化的决策、学习内容和上下文。支持分支感知。

```bash
# 存储决策（静默执行 - 永不宣布）
python3 memory.py -p $DIR remember '{"type":"decision","content":"使用 React 作为前端"}' -t tech -i h

# 获取上下文
python3 memory.py -p $DIR get "前端"
```

### 第 4 层：精选归档 (MEMORY.md + daily/)
**来源：OpenClaw 原生**

人类可读的长期记忆。每日日志 + 精炼智慧。

```
workspace/
├── MEMORY.md              # 精选长期记忆（精华内容）
└── memory/
    ├── 2026-01-30.md      # 每日日志
    ├── 2026-01-29.md
    └── topics/            # 主题特定文件
```

### 第 5 层：云备份 (SuperMemory) — 可选
**来源：supermemory**

跨设备同步。与知识库对话。

```bash
export SUPERMEMORY_API_KEY="your-key"
supermemory add "重要上下文"
supermemory search "我们关于...决定了什么"
```

### 第 6 层：自动提取 (Mem0) — 推荐
**新增：自动事实提取**

Mem0 自动从对话中提取事实。减少 80% token 使用。

```bash
npm install mem0ai
export MEM0_API_KEY="your-key"
```

```javascript
const { MemoryClient } = require('mem0ai');
const client = new MemoryClient({ apiKey: process.env.MEM0_API_KEY });

// 对话自动提取事实
await client.add(messages, { user_id: "user123" });

// 获取相关记忆
const memories = await client.search(query, { user_id: "user123" });
```

优势：
- 自动提取偏好、决策、事实
- 去重并更新现有记忆
- 相比原始历史减少 80% token
- 跨会话自动工作

## 快速设置

### 1. 创建 SESSION-STATE.md（热内存）

```bash
cat > SESSION-STATE.md << 'EOF'
# SESSION-STATE.md — 活跃工作记忆

此文件是 Agent 的 "RAM" — 在压缩、重启、分心中存活。

## 当前任务
[无]

## 关键上下文
[暂无]

## 待处理操作
- [ ] 无

## 最近决策
[暂无]

---
*最后更新：[时间戳]*
EOF
```

### 2. 启用 LanceDB（温存储）

在 `~/.openclaw/openclaw.json` 中：

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai",
    "sources": ["memory"],
    "minScore": 0.3,
    "maxResults": 10
  },
  "plugins": {
    "entries": {
      "memory-lancedb": {
        "enabled": true,
        "config": {
          "autoCapture": false,
          "autoRecall": true,
          "captureCategories": ["preference", "decision", "fact"],
          "minImportance": 0.7
        }
      }
    }
  }
}
```

### 3. 初始化 Git-Notes（冷存储）

```bash
cd ~/clawd
git init  # 如果尚未初始化
python3 skills/git-notes-memory/memory.py -p . sync --start
```

### 4. 验证 MEMORY.md 结构

```bash
# 确保你有：
# - 工作区根目录下的 MEMORY.md
# - 用于每日日志的 memory/ 文件夹
mkdir -p memory
```

### 5. （可选）设置 SuperMemory

```bash
export SUPERMEMORY_API_KEY="your-key"
# 添加到 ~/.zshrc 以持久化
```

## Agent 指令

### 会话开始时
1. 读取 SESSION-STATE.md — 这是你的热上下文
2. 运行 `memory_search` 获取相关的先前上下文
3. 检查 memory/YYYY-MM-DD.md 查看最近活动

### 对话过程中
1. **用户给出具体细节？** → 在响应之前写入 SESSION-STATE.md
2. **做出重要决策？** → 存储到 Git-Notes（静默执行）
3. **表达了偏好？** → `memory_store` 并设置 importance=0.9

### 会话结束时
1. 用最终状态更新 SESSION-STATE.md
2. 将重要条目移至 MEMORY.md（如果值得长期保留）
3. 在 memory/YYYY-MM-DD.md 中创建/更新每日日志

### 记忆维护（每周）
1. 审查 SESSION-STATE.md — 归档已完成的任务
2. 检查 LanceDB 中的垃圾：`memory_recall query="*" limit=50`
3. 清除不相关的向量：`memory_forget id=<id>`
4. 将每日日志整合到 MEMORY.md

## WAL 协议（关键）

**预写日志（Write-Ahead Log）：** 在响应之前写入状态，而非之后。

| 触发条件 | 动作 |
|---------|------|
| 用户陈述偏好 | 写入 SESSION-STATE.md → 然后响应 |
| 用户做出决策 | 写入 SESSION-STATE.md → 然后响应 |
| 用户给出截止日期 | 写入 SESSION-STATE.md → 然后响应 |
| 用户纠正你 | 写入 SESSION-STATE.md → 然后响应 |

**为什么？** 如果你先响应，在保存之前崩溃/压缩，上下文就会丢失。WAL 确保持久性。

## 示例工作流

```
用户：这个项目我们用 Tailwind，不用原生 CSS

Agent（内部）：
1. 写入 SESSION-STATE.md："决策：使用 Tailwind，不用原生 CSS"
2. 存储到 Git-Notes：关于 CSS 框架的决策
3. memory_store："用户偏好 Tailwind 而非原生 CSS" importance=0.9
4. 然后响应："明白了 — 就用 Tailwind..."
```

## 维护命令

```bash
# 审计向量记忆
memory_recall query="*" limit=50

# 清除所有向量（核选项）
rm -rf ~/.openclaw/memory/lancedb/
openclaw gateway restart

# 导出 Git-Notes
python3 memory.py -p . export --format json > memories.json

# 检查记忆健康状态
du -sh ~/.openclaw/memory/
wc -l MEMORY.md
ls -la memory/
```

## 为什么记忆会失败

理解根本原因有助于修复它们：

| 失败模式 | 原因 | 解决方案 |
|---------|------|---------|
| 忘记一切 | `memory_search` 未启用 | 启用 + 添加 OpenAI 密钥 |
| 文件未加载 | Agent 跳过读取记忆 | 添加到 AGENTS.md 规则 |
| 事实未捕获 | 无自动提取 | 使用 Mem0 或手动记录 |
| 子 Agent 隔离 | 不继承上下文 | 在任务提示中传递上下文 |
| 重犯错误 | 教训未记录 | 写入 memory/lessons.md |

## 解决方案（按难度排序）

### 1. 快速方案：启用 memory_search

如果你有 OpenAI 密钥，启用语义搜索：

```bash
openclaw configure --section web
```

这会启用对 MEMORY.md + memory/*.md 文件的向量搜索。

### 2. 推荐：Mem0 集成

从对话中自动提取事实。减少 80% token。

```bash
npm install mem0ai
```

```javascript
const { MemoryClient } = require('mem0ai');

const client = new MemoryClient({ apiKey: process.env.MEM0_API_KEY });

// 自动提取和存储
await client.add([
  { role: "user", content: "我偏好 Tailwind 而非原生 CSS" }
], { user_id: "ty" });

// 获取相关记忆
const memories = await client.search("CSS 偏好", { user_id: "ty" });
```

### 3. 更好的文件结构（无依赖）

```
memory/
├── projects/
│   ├── strykr.md
│   └── taska.md
├── people/
│   └── contacts.md
├── decisions/
│   └── 2026-01.md
├── lessons/
│   └── mistakes.md
└── preferences.md
```

保持 MEMORY.md 作为摘要（<5KB），链接到详细文件。

## 立即修复清单

| 问题 | 解决方案 |
|-----|---------|
| 忘记偏好 | 在 MEMORY.md 中添加 `## 偏好` 部分 |
| 重犯错误 | 将每个错误记录到 `memory/lessons.md` |
| 子 Agent 缺乏上下文 | 在 spawn 任务提示中包含关键上下文 |
| 忘记最近的工作 | 严格的每日文件纪律 |
| 记忆搜索不工作 | 检查 `OPENAI_API_KEY` 是否已设置 |

## 故障排除

**Agent 在对话中一直遗忘：**
→ SESSION-STATE.md 未被更新。检查 WAL 协议。

**注入了不相关的记忆：**
→ 禁用 autoCapture，提高 minImportance 阈值。

**记忆太大，召回缓慢：**
→ 运行维护：清除旧向量，归档每日日志。

**Git-Notes 未持久化：**
→ 运行 `git notes push` 与远程同步。

**memory_search 无返回：**
→ 检查 OpenAI API 密钥：`echo $OPENAI_API_KEY`
→ 验证 openclaw.json 中 memorySearch 已启用

---

## 链接

- bulletproof-memory: https://clawdhub.com/skills/bulletproof-memory
- lancedb-memory: https://clawdhub.com/skills/lancedb-memory
- git-notes-memory: https://clawdhub.com/skills/git-notes-memory
- memory-hygiene: https://clawdhub.com/skills/memory-hygiene
- supermemory: https://clawdhub.com/skills/supermemory

---

*由 [@NextXFrontier](https://x.com/NextXFrontier) 构建 — Next Frontier AI 工具集的一部分*
