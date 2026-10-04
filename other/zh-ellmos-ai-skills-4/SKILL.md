---
name: model-strategy
version: 2.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-06-13
description: 多模型编排与模型切换策略。基于评分的模型选择、跨 Agent 委派（Gemini、Codex、Ollama）、Advisor 配对、升级触发器、权限矩阵与成本效率优化。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="model-strategy banner">

> **中文** — `model-strategy` 官方中文版本。


# 模型切换策略（中文）

> 多模型编排：基于评分的模型选择、跨 Agent 委派、Advisor 配对、升级触发器以及成本效率优化

---

## 1. 模型目录

### Claude（可通过 Agent 工具作为 Subagent 调用）

```
Level 4 (Reviewer):   Opus 4.8  — advisor, math review     [user only: /model, /advisor]
Level 3 (Strategist): Opus 4.6  — architecture, concepts   [subagent: model:"opus"]
Level 3 (Creative):   Fable 5   — creative texts, stories  [subagent: model:"fable"]
Level 2 (Workhorse):  Sonnet 4.6— implementation, debug    [subagent: model:"sonnet"]
Level 1 (Fast):       Haiku 4.5 — boilerplate, formatting  [subagent: model:"haiku"]
```

### 外部 Agent（伴侣脚本 / SSH）

```
Level 2-3: Gemini 3.5 pro  — research, scientific databases [agy-companion CLI]
Level 2:   Gemini 3.5 flash— fast research                  [agy-companion CLI]
Level 2-3: Codex 5.5 (GPT) — code review, code generation   [codex-companion CLI]
Level 2:   Codex 4.5 (GPT) — simpler code tasks             [codex-companion CLI]
```

### 本地模型（无需 Token，24/7 常驻）

```
Level 1-2: Ollama (Qwen 3.5:35b-a3b) — Haiku-to-Sonnet level [<ollama-host>:11434]
           Invocation: SSH + curl http://<ollama-host>:11434/v1/chat/completions
           Or: delegation via an agent-system control API (if available)
```

### 可达性矩阵

| 模型 | LLM 可启动 | 调用路径 | 约束条件 |
|-------|---------------|-----------------|-------------|
| Sonnet 4.6 | 是 | `Agent(model:"sonnet")` | — |
| Opus 4.6 | 是 | `Agent(model:"opus")` | — |
| Haiku 4.5 | 是 | `Agent(model:"haiku")` | — |
| Fable 5 | 是 | `Agent(model:"fable")` | — |
| Opus 4.8 | 仅限 Advisor | 会话中的 `advisor()` | 用户必须设置 `/advisor` |
| Gemini 3.5 | 是 (Bash) | `companion-for-agy "prompt"` | 仅限 Windows，stdout 变通方案 |
| Codex 5.5/4.5 | 是 (Bash) | `node codex-companion.mjs task "prompt"` | 需要身份验证 |
| Ollama | 是 (SSH/curl) | 通过 SSH + curl 访问 Ollama 主机 API | VPN/Tailscale 必须处于活动状态 |
| Opus 4.8 作为主模型 | 否 | 用户：`/model opus 4.8` | 仅限用户操作 |
| Fable 5 作为主模型 | 否 | 用户：`/model fable` | 仅限用户操作 |

---

## 2. 评分计算

```
Dimensions (0-10):
  CLARITY     : How unambiguous is the task?
  COMPLEXITY  : How many components?
  CREATIVITY  : New solutions needed?
  CONTEXT     : How much prior knowledge?
  CRITICALITY : How important is perfection?

SCORE = (10 - CLARITY) + COMPLEXITY + CREATIVITY + CONTEXT + CRITICALITY
```

### 评分阈值

| 分数 | 模型 | 示例 |
|-------|-------|----------|
| 0-8 | Ollama（本地主机） | Prompt 生成、摘要、简单文本 |
| 9-12 | Haiku | `__init__.py`、格式化、样板代码 |
| 13-22 | Sonnet | 代码实现、Bug 修复、标准代码 |
| 13-22 | Gemini 3.5 | 研究、文献检索、科学数据库 |
| 13-22 | Codex 5.5 | 代码生成（Luau、Node.js）、计算脚本 |
| 23-28 | Sonnet + Advisor 审查 | 包含质量检查的复杂代码 |
| 23-35 | Fable 5 | 创意文本、营销、故事创作 |
| 29-40 | Opus 4.6 | 架构、策略、论文撰写 |
| 35-50 | Opus 4.6 + Advisor | 证明、架构决策、统计学 |
| 40-50 | Opus 4.8（用户建议） | 数学证明工作、极高严谨度 |

---

## 3. 跨 Agent 委派

### 针对不同任务选择哪个外部 Agent？

| 任务 | 最佳 Agent | 理由 |
|------|-----------|--------|
| 科学文献检索 | Gemini 3.5 pro | 原生 OpenAlex/arXiv/PubMed Skill |
| 代码审查（第二意见） | Codex 5.5 | 独立视角 |
| 简单文本生成 | Ollama（本地主机） | 无需 Token，24/7 常驻 |
| 创意文本、营销 | Fable 5 | 最强创意输出 |
| 数学证明 | Opus 4.8 (Advisor) | 最高分析深度 |

### 排除项（已记录的弱点）

- **Gemini：** 不适用于数学审查/证明工作（在 2026-06-07 的证明审查中记录过方向性错误）
- **Codex 4.5：** 仅在 5.5 不可用时使用；否则始终使用 5.5

### 调用路径

> 请将占位符 `<host>`、`<ollama-host>`、`<tailscale-ip>`、`<user>` 和 `~/.ssh/<key>` 替换为您自己的基础设施配置。

**Gemini (via companion-for-agy):**
```
companion-for-agy --researcher --json --timeout 120000 "research prompt"
```

**Codex (via codex-companion):**
```
node "~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs" task --effort high "code prompt"
```

**Ollama on a remote host (via SSH):**
```
ssh -i ~/.ssh/<key> <user>@<tailscale-ip> "curl -s http://localhost:11434/v1/chat/completions -d '{\"model\":\"qwen3.5:35b-a3b\",\"messages\":[{\"role\":\"user\",\"content\":\"Prompt\"}]}'"
```

**Delegation to an agent system with tools (example):**
```
curl -s -X POST http://<host>:8081/api/chat -H "Content-Type: application/json" -d '{"prompt": "...", "chat_id": "claude-delegate"}'
```

---

## 4. Advisor 配对

### 运行机制

`advisor()` 是一个**会话级工具** — Advisor 模型由用户通过 `/advisor` 设置，而非通过程序设置。这产生了以下配对模式：

| 模式 | 运行方式 | 适用场景 |
|---------|--------------|-------------|
| **会话 Advisor** | 用户设置 `/advisor opus 4.8`，Agent 调用 `advisor()` | 证明/架构的标准模式 |
| **编排器作为审查员** | Opus 主模型审查 Sonnet Subagent 的输出 | 编排器能力强于 Worker |
| **对抗 Agent** | Agent A 执行任务，Agent B 进行对抗性检查 | 独立验证，双重视角 |
| **用户建议** | Agent 建议：“请使用 opus 4.8 + advisor 完成此任务” | 当前会话能力不足时 |

### 何时建议使用 Advisor？

- 数学证明工作（分数 ≥ 35）
- 具有长期影响的架构决策
- 统计方法学 / 实验设计
- 经过 2 次以上未成功的 Debug 循环后的复杂 Bug

### 何时不应使用 Advisor？

- 常规代码、内容、格式化（分数 < 23）
- 简单功能实现
- 明确定义且非关键的任务

---

## 5. 升级触发器

### Ollama -> Haiku
- 需要文件访问
- 需要代码分析

### Haiku -> Sonnet
- 影响超过 2 个文件
- 需要在多个方案间做出抉择
- 发生意外错误
- 请求删除操作

### Sonnet -> Opus
- 需要架构决策
- 需要集成 3 个或更多系统
- 需求矛盾/不明确
- 需要战略规划

### Sonnet -> Gemini（横向）
- 需要科学研究
- 书目/参考文献验证

### Sonnet -> Codex（横向）
- 作为第二意见的代码审查
- Advisor 负载过高（备用审查员）

### Opus -> Opus + Advisor
- 需要证明审查
- 关键架构决策
- 统计方法学

### 降级
- 概念已定义 -> 由 Sonnet 接管实现
- 任务简单/重复 -> 由 Haiku 接管
- 仅限文本、无需工具访问 -> 由 Ollama 接管

---

## 6. 权限矩阵

| 操作 | Ollama | Haiku | Sonnet | Opus | Gemini | Codex |
|-----------|--------|-------|--------|------|--------|-------|
| 读取文件 | - | 是 | 是 | 是 | 是* | 是* |
| 写入文件 | - | 是 | 是 | 是 | 是* | 是* |
| 删除文件 | - | - | 是** | 是 | - | - |
| 系统命令 | - | - | 是** | 是 | 是* | 是* |
| 架构决策 | - | - | - | 是 | - | - |
| 网络研究 | - | - | 是 | 是 | 是 | - |
| 调用 advisor() | - | - | 是 | 是 | - | - |

*通过伴侣脚本在其自身的沙盒模式中执行
**需要用户确认

---

## 7. 成本效率

### 通过路由节省 Token

| 任务类型 | 无路由 | 有路由 | 节省比例 |
|-----------|-----------------|--------------|---------|
| 简单/琐碎 | Opus Token | Ollama（免费） | 100% |
| 样板代码 | Opus Token | Haiku Token | ~80% |
| 标准代码 | Opus Token | Sonnet Token | ~50% |
| 研究 | Claude Token | Gemini Token | ~70%（不同预算） |
| 代码审查 | advisor() Token | Codex Token | ~60%（不同预算） |

---

## 8. 黄金法则

> "Opus 思考，Sonnet 构建，Haiku 执行，Ollama 节省。Gemini 研究，Codex 审查，Fable 叙述。"

---

## 更新日志

### 2.0.0 (2026-06-12)
- 跨 Agent 委派：将 Gemini、Codex、Ollama（本地主机）作为路由目标
- Advisor 配对：4 种模式（会话 Advisor、编排器作为审查员、对抗 Agent、用户建议）
- 可达性矩阵：记录了 LLM 可启动与仅限用户的区别
- 新增 Ollama（Qwen 3.5:35b-a3b，Haiku 到 Sonnet 级别）作为 Level 1-2
- 横向升级：Sonnet -> Gemini（研究），Sonnet -> Codex（审查）
- 记录排除项（Gemini 不适用于数学）
- 评分阈值扩展至所有模型

### 1.0.0 (2026-03-15)
- 从 BACH v3.8.0 (ing-strategie v2.0.0) 移植

---

*从 BACH v3.8.0 移植 | 扩展跨 Agent + Advisor v2.0.0*
