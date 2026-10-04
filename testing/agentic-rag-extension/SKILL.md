---
name: agentic-rag-extension
description: |
  为 MODULAR-RAG-MCP-SERVER 添加 Agentic RAG 层并跑出真实评测数据。
  作者背景：应届生 + 无实习，目标 Agent 方向求职。

  使用场景：
  1. 用户说"加 Agent 层" / "实现 ReAct Agent" / "Agentic RAG" / "多步推理"
  2. 用户说"跑评测" / "出评测数字" / "Ragas 实测" / "对比指标"
  3. 用户说"继续扩建项目" / "Stage J" / "Stage K"
  4. 用户在新对话中提到这个 RAG 项目需要扩展

  该 skill 记录了所有背景知识、架构决策和实现细节，使 Codex 无需重新探索即可直接执行。
---

# Agentic RAG Extension Skill

## 快速上手

读本文件即可开工。详情按需查阅 references：

| 文件 | 内容 | 何时读 |
|------|------|------|
| [01-project-context.md](references/01-project-context.md) | 项目背景、目录结构、核心接口 | 第一次接触项目时，或需要了解现有代码结构 |
| [02-agent-architecture.md](references/02-agent-architecture.md) | Agent 层完整设计：类定义、文件树、实现顺序 | 实现 J1~J5 任何任务时必读 |
| [03-evaluation-plan.md](references/03-evaluation-plan.md) | 评测数据集格式、跑法、README 模板 | 实现 K1~K3 评测任务时必读 |

---

## 项目状态（已完成）

原项目 A~I 阶段 **68 个任务全部完成**，是一个完整的 Modular RAG MCP Server。

现在要新增两个阶段：

```
阶段 J：Agentic RAG Layer（ReAct Agent 层）
阶段 K：评测实跑与数据固化
```

---

## 阶段 J 任务清单

> 详细类定义和文件树见 [02-agent-architecture.md](references/02-agent-architecture.md)

| 任务 | 文件 | 关键产出 |
|------|------|--------|
| J1 | `src/agent/react_agent.py` + `tool_registry.py` + `agent_state.py` | ReActAgent 核心循环 |
| J2 | `src/agent/tools/*.py` | 5个原子工具（semantic/keyword/hybrid/summary/list） |
| J3 | `src/agent/memory/conversation_memory.py` | 多轮对话记忆 |
| J4 | `src/agent/reflection/self_checker.py` | 自反思 + 置信度打分 |
| J5 | `scripts/agent.py` + `src/observability/dashboard/pages/agent_chat.py` | CLI + Dashboard 聊天页 |

**实现优先级：J1 → J2 → J5（可演示）→ J3 → J4（进阶亮点）**

---

## 阶段 K 任务清单

> 详细格式和指令见 [03-evaluation-plan.md](references/03-evaluation-plan.md)

| 任务 | 产出 |
|------|------|
| K1 | `tests/fixtures/golden_test_set.json`（20+ QA 对） |
| K2 | 跑出 Dense / Sparse / Hybrid / Hybrid+Rerank 四模式对比数字 |
| K3 | 把数字写进 README 评测对比表 |

---

## 实现规则

1. **不重写现有代码**：Agent 层调用现有 `HybridSearch` / `DenseRetriever` / `SparseRetriever` 作为工具，不修改底层。
2. **依赖注入模式**：所有 Agent 类通过构造函数接受 `settings` 和组件，便于单元测试 mock。
3. **配置驱动**：在 `config/settings.yaml` 新增 `agent:` 节点（`max_turns`, `confidence_threshold` 等）。
4. **测试覆盖**：每个模块写单元测试（mock LLM + mock 工具），E2E 测试放 `tests/e2e/`。
5. **激活虚拟环境**：运行任何 Python 命令前先执行 `.\.venv\Scripts\Activate.ps1`（Windows）。

---

## DEV_SPEC 更新

实现任务前，在 `DEV_SPEC.md` 末尾追加以下排期节点（保持原有格式）：

```markdown
#### 阶段 J：Agentic RAG Layer

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| J1 | ReAct Agent 核心框架（推理-行动循环 + Tool 调度） | [ ] | | |
| J2 | 细粒度原子工具集（semantic/keyword/hybrid/summary/list） | [ ] | | |
| J3 | 多轮对话记忆（ConversationMemory + 查询改写） | [ ] | | |
| J4 | 自反思与置信度校验（SelfChecker + 幻觉检测） | [ ] | | |
| J5 | Agent 入口（CLI scripts/agent.py + Dashboard 聊天页） | [ ] | | |

#### 阶段 K：评测实跑与数据固化

| 任务编号 | 任务名称 | 状态 | 完成日期 | 备注 |
|---------|---------|------|---------|------|
| K1 | Golden Test Set 准备（20+ QA 对手工标注） | [ ] | | |
| K2 | 四模式检索对比实跑（Dense/Sparse/Hybrid/Hybrid+Rerank） | [ ] | | |
| K3 | 评测结果写入 README 对比表 | [ ] | | |
```

完成任务后将 `[ ]` 改为 `[x]` 并填写完成日期。

---

## 面试价值说明（背景知识）

以下是每个模块对求职的价值，可帮助判断优先级：

- **J1 ReAct**：ReAct 论文（Yao et al. 2023）是 Agent 方向必考题，有实现经验远强于"了解"
- **J2 原子工具**：展示对 Dense vs Sparse 检索的深度理解，而不只是用框架堆出来的
- **J4 SelfChecker**：幻觉检测是 2024-2025 最热的 RAG 改进方向，面试加分项
- **K2-K3 评测数字**：有具体数字的项目比没有数字的项目可信度高 10 倍
