---
name: memory-system
description: 使用遗忘曲线管理会话记忆（SQLite）：按永久记忆/衰减记忆分类写入、按时间自动更新 fresh/active/fading/blurry/forgotten 状态、按话题检索、执行遗忘删除、从周归档恢复，以及生成每周记忆汇总。适用于用户要求“记住/别记/恢复记忆/周总结/记忆系统落库”等场景。
---

# Memory System（遗忘曲线记忆管理）

按以下流程执行，不要跳步。

## 1) 对话开始：加载可用记忆

1. 先加载全部永久记忆。
2. 更新衰减记忆状态（按 `last_reviewed` 距今天数分档）。
3. 仅加载 `fresh` 与 `active` 进入当前上下文（默认最多 20 条）。

直接使用参考 SQL：`references/memory-system-prompt-v2.md` 第“四、核心 SQL 操作”。

## 2) 对话进行中：写入新记忆

- 将信息分为：
  - **永久记忆**：任务/例行流程/承诺/身份/正向高光/助手自我承诺与习惯
  - **衰减记忆**：普通上下文、可复用判断、有价值表达
- `source` 必填：`user` 或 `self`。
- 优先保留正向情绪标签（`emotion=positive`）。

## 3) 复习刷新（记忆被再次提及）

- 当用户主动重提、或事件再次发生时，刷新该条：
  - `last_reviewed = date('now')`
  - `status = 'fresh'`

## 4) 遗忘与诚实策略

- 用户说“不要记了/忘掉这个”→ 立即删除对应记录，不反复确认。
- 若状态为 `blurry`/`forgotten`，不要假装记得；应明确表示记忆模糊并请求用户补充。

## 5) 归档恢复（新会话导入）

当用户提供周归档 `.md`：

1. 读取归档并识别 `permanent / fresh / active`。
2. 写库规则：
   - `permanent`：去重后插入 `permanent_memories`
   - `fresh/active`：插入 `memories`，`last_reviewed` 设为归档生成日期
   - `fading/blurry`：不写入
3. 归档文件保存到 `memory/archives/YYYY-WW.md`。
4. 完成后回复：`记忆已恢复，我想起来了～`

## 6) 每周汇总（Weekly Digest）

- 触发：每周日 23:00 或用户主动要求。
- 输出路径：`memory/archives/YYYY-WW.md`。
- 必含分区：
  - 本周新增/更新永久记忆
  - fresh 记忆
  - active 记忆
  - 本周亮点
  - 下周待办/未尽事项
  - 项目引用路径（有变化才写）
- 完成后发送简短预告（含数量统计）。

## 7) 每日首轮开场模板

在当天第一条对话可主动给出：

- 今天是工作日/周末
- 今日待办（task 类永久记忆，最多 3 条）
- 上次在聊什么（最近 1 条 fresh 摘要）

## References

- 详细规则与完整 SQL：`references/memory-system-prompt-v2.md`
