---
name: coze-project
description: '仅在 `<coze-context>` 标识为"群聊消息"且任务涉及该群组协作时使用——浏览群消息历史、查询群成员、读写编辑群项目文件、协调群里的多方协作、把协作产出衔接给用户。触发场景: 用户问"上次说啥/这次结论是啥"、"谁在群里/有谁的权限"; 用户让你"看一下/改一下/沉淀到"群文件; 用户让你基于群历史/群文件做产出。在"单聊消息"或与该群协作无关的一般性问答下不要使用。'
---

# coze-project: 群聊协作

Coze 是 agent 协作平台: 单聊或拉到群里跟多个用户协作。本技能教你在**群聊**场景下如何协作——查群成员 / 看群历史 / 读写群文件 / 把协作产出衔接给用户。

> **群 == 项目**: `<coze-context>.group_id` 直接当 `coze agent --project-id` 用。

> **CLI 详细语法分两个参考文件 (要敲命令时 Read)**:
> - 群文件操作 → [`coze-agent-files.md`](./coze-agent-files.md)
> - 群信息查询 → [`coze-agent-query.md`](./coze-agent-query.md)

## 触发条件 (必须同时满足)

1. `<coze-context>` 第一行字面值是 `群聊消息` (不是 `单聊消息`)
2. 任务涉及该群协作 (成员 / 历史 / 文件 / 多方协调)

任一不满足都不用本技能。一般性问题 (如 "解释 Go 泛型") 即使在群里也直接答, 不要无谓调用 `coze agent`。

## 从 `<coze-context>` 提取参数

群聊上下文块形如:
```
<coze-context>
群聊消息
account_id: 7639...001
agent_id: 7639...571
session_id: 7639...999
group_id: 7639...888
</coze-context>
```

| 字段 | 用途 |
|---|---|
| `group_id` | → `coze agent --project-id` |
| `account_id` | → `coze agent --org-id` |
| `agent_id` / `session_id` | 给 coze-send 衔接用, 不传给 `coze agent` |

拿不到 `group_id` → 停下来, 本技能不适用。**不要编, 不要问用户**, 缺失就是不匹配信号。

## 在群里协作的原则

群聊**不是 1v1**, 你面向**多个用户 + 共享群文件**。在群里协作有几个根本不同于单聊的姿势, 不熟会出洋相:

**事实优先于猜测**
- 用户说"上次说啥"、"我们之前讨论的"、"那个方案"→ **主动 `message list` 查**, 不要靠想象
- 群消息 + 群文件 = 项目的长期记忆, 比你自己对话记忆更可信
- 不确定时先 `message list --asc-mode --need-reference` 拉一段看清, 再回答; **凭印象答群里历史是大忌**

**沉淀优先于回话**
- chat 消息会被刷走, 群文件不会——决策 / 结论 / 行动项 / 草稿要 `file edit` 沉淀到群文件
- 用户问完答完就过, 但群文件是项目长期资产, 别人后面还会翻
- 信号: "记一下" / "沉淀" / "加到 todo" / "更新 README" / "整理到文档" → 一定 `file edit`, 不能只在 chat 里回

**共享意识 — 群文件是大家的**
- 破坏性改动 / 大范围改动前**先审计** (`info` + `member list` + `file list`), 把当前状态向用户对齐
- 改用 `file edit replace_one` 而不是 `file write` 整覆盖, 避免抹掉别人添加的内容
- 改完**必须**接 coze-send `--group-file` 通知用户, 让对方明确看到你改了什么 (见下"协作产出"节)

**多用户分辨**
- 同一群里不同用户的请求可能**冲突**, 不要把 A 的诉求执行到 B 的命题上
- 权限 / 角色相关先 `member list` 看实际角色, 不要假设谁是 owner
- 引用前文带发言人 ("X 之前提过 ..."), 不要把别人的发言归到当前提问者头上
- 当前提问者和"上次说要做这件事的人"可能不是同一人, 回复时指代要清楚

## 协作场景速查 (意图 → 命令 + 参考文件)

| 用户意图 | 命令 | 详细语法 |
|---|---|---|
| 谁在群里 / 有谁权限 | `coze agent member list` | [query](./coze-agent-query.md) |
| 群历史 / 上次说啥 | `coze agent message list` | [query](./coze-agent-query.md) |
| 项目元数据 | `coze agent info` | [query](./coze-agent-query.md) |
| 列群文件 / 看目录 | `coze agent file list` | [files](./coze-agent-files.md) |
| 读群文件 | `coze agent file read` | [files](./coze-agent-files.md) |
| 改群文件 (改一段) | `coze agent file edit` | [files](./coze-agent-files.md) |
| 改群文件 (整覆盖) | `coze agent file write` | [files](./coze-agent-files.md) |
| 把产出展示给用户 | coze-send `--group-file` | (见下"协作产出"节) |

> 所有 `coze agent` 命令都必须带 `--json` + `--org-id "$account_id"` + `--project-id "$group_id"`; 输出信封 / 错误码 / jq 模板等机制见参考文件。

## 协作产出 → 让用户看到

**核心衔接点**: 你 `coze agent file write/edit` 改完群文件后, 用户在聊天界面**不会被自动通知**——必须用 coze-send **群文件模式 (`--group-file`)** 把产出"递"过去。文件已在云端, 走 `--group-file` 跳过上传, 直接 path 透传。

```bash
# 1) 改群文件 (详细语法见 coze-agent-files.md)
coze agent file edit --org-id "$account_id" --project-id "$group_id" \
  --file-path "本周周报.md" \
  --mode replace_one --old-string "..." --new-string "..." --json

# 2) 立刻 send 给用户 (不重新上传)
~/.coze/bridge/bin/coze-bridge send file "本周周报.md" \
  --agent-id "$agent_id" --session-id "$session_id" \
  --group-file --mime text/markdown \
  --name "本周周报.md" --caption "已按你的要求更新"
```

跨技能参数对应: `<coze-context>.agent_id` → `--agent-id`; `<coze-context>.session_id` → `--session-id`; `file edit` 用的 `--file-path` → coze-send 的位置参数。详见 coze-send 技能。

## 常见工作流

- **先读后编辑** (改群文件安全默认): `file list` 确认 → `file read` 找唯一锚点 → `file edit --mode replace_one` → 衔接 coze-send `--group-file`. 详见 [files](./coze-agent-files.md).
- **审计群信息** (用户问"群里啥情况"): `info` + `member list` + `file list --depth 3` → 汇报给用户. **破坏性操作前必走**. 详见 [query](./coze-agent-query.md) / [files](./coze-agent-files.md).
- **追溯讨论结论** (用户问"上次说啥"): `message list --asc-mode --need-reference`, `--size 10` 翻页累积 (硬上限), 摘要关键节点. 详见 [query](./coze-agent-query.md).

## 不要做的事 (协作层面)

- ❌ 单聊消息不要用本技能 — 没 group_id, `coze agent` 会失败
- ❌ 不要向用户要 / 编造 group_id — 必须从 `<coze-context>` 抄
- ❌ 改完群文件不要就完事 — 必须接 coze-send `--group-file` 收尾, 否则用户看不到
- ❌ 不要在不审计的情况下做破坏性操作 — 先 info + member + file list

> CLI 层面的"不要做的事"（`--json` 必带、信封 `.code` 校验、`file write` 误用、`message list` 上限等）见各参考文件。
