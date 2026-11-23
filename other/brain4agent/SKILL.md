---
name: brain4agent
description: 存取 agent 的长期工作记忆——项目上下文、决策、踩过的坑。用户问「之前/上次/记得/为什么这么定」类问题，或要求记住某个结论时使用。中文优先、零模型、单文件 SQLite。不用于通用知识问答，不联网检索。
---

# Brain4Agent 长期记忆

一个本地记忆库：把对话轮次存进单个 SQLite 文件，按会话检索。检索走 BM25，
核心路径**不调用任何模型**，因此没有 API key、没有冷启动、单次查询毫秒级。

## 何时用

- 用户问「之前那个 bug」「上次说的部署目录是什么」——**先查记忆再回答**。
- **动手改一个文件、或开始一个新任务之前**——先查一次这个目录/模块的历史，
  很多「为什么这么写」的答案在里面，而用户不会主动问。
- 用户说「记住这个」「记一下」——存进去。
- 用户问「为什么当初这么决定」——查记忆里的决策记录。

**不要**用它存通用知识、网页内容、或者用户没提过的东西。它只记这台机器上
发生过的事。

## 先确认可用

```sh
python -c "import brain4agent; print(brain4agent.__version__)"
```

导入失败说明没装。从仓库根目录装：

```sh
pip install -e ".[precise]"
```

`precise` extra 会带上 jieba 词典，检索 hit@1 从 0.825 提到 0.925。
不装也能用，只是精度低一些。

## 命令

数据库路径由 `BRAIN4AGENT_DB` 或 `--db` 指定；**同一次任务里要保持一致**，
用同一个文件。

```sh
# 存一问一答（存成一个会话）
brain4agent --db <db> exchange "用户问的" "assistant 答的"

# 存单条
brain4agent --db <db> add "内容" --session <id> --role user

# 检索（-k 返回几个会话）
brain4agent --db <db> search "查询" -k 3

# 主动回忆：读 stdin 的提示词，输出可直接注入上下文的相关记忆
# 没有相关内容时**什么都不输出**——这是常态，不要把它当失败
brain4agent --db <db> recall-context -k 3 < prompt.txt

# 统计 / 列出会话 / 删会话 / 只留最近 N 个
brain4agent --db <db> stats
brain4agent --db <db> sessions
brain4agent --db <db> forget <session_id>
brain4agent --db <db> prune --keep 100

# 批量导入 JSONL（每行一个对象，content 必填）
brain4agent --db <db> import conversations.jsonl
```

`python -m brain4agent ...` 与上面的 `brain4agent ...` 等价。

## 读结果：`corpus_missing` 比分数重要

`search` 输出里的两个缺失信号含义不同，**不要混用**：

- **`corpus has no:`** —— 问题里的词，整份语料都没有。这是**事实**，
  不是猜测。看到它基本可以判断「没记过这件事」。
- **`this session lacks:`** —— 这条会话没有这个词。只说明这条不匹配，
  **不代表**没记过。

```
1 sessions for '杭州测试机上装的是什么数据库'
  corpus has no: 数据库, 机上          <- 整个库里没有「数据库」这个词
  [ 4.81 cov=0.28] c060a5294037  session lacks: 数据库, 机上
```

`coverage` 是这条会话覆盖了问题多少内容，只用来排序，**不要**当置信度阈值。

## 它的边界（实测过，别指望更多）

- **同主题、不同事实的会话无法区分。** 库里如果有三段「根因在 X 文件」的对话，
  问「根因在哪」，它分不清你指哪个。这类问题要靠上下文说明具体是哪次，
  比如「keywords.py 那次」。
- **答案里没有具体值的题，检索帮不上忙。** 问「当时怎么处理的」，答案是
  「改了一行」这种，词面上区分不出来。
- **所以：返回多个结果时，读前三个，不要只看第一个。**

这些限制的完整数据在仓库的 `docs/decisions.md`，D-020 与 D-021。

## 供 agent 直接调用（MCP）

不需要 CLI 时可以配成 MCP server，工具名为 `b4a_remember` / `b4a_recall` /
`b4a_session` / `b4a_stats`：

```json
{"mcpServers": {"brain4agent": {
    "command": "python",
    "args": ["-m", "brain4agent.mcp_server"],
    "env": {"BRAIN4AGENT_DB": "/path/to/brain.db"}
}}}
```

`b4a_` 前缀是刻意的：`remember`、`recall` 这类名字会和别的记忆服务撞车。

## 回答用户时

查到东西就**引用具体内容**，别只说「我记得有这件事」。查到 `corpus has no`
就直说「没有记录过 X」，不要把「没找到」说成「没有」——这两者对用户是不同的。
