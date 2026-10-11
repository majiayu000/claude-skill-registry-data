---
name: proactive-agent-lite
description: 轻量主动代理增强。用于在不显著增加 token 的前提下引入 4 个高价值机制：VBR（先验证再汇报）、Autonomous vs Prompted Cron 区分、工具迁移检查清单、会话压缩恢复流程。适用于避免“改了文本没改机制”、减少自动任务失效、提高会话连续性。
---

# Proactive Agent Lite

只接入高价值、低噪音模块，不启用高频心跳与重主动策略。

## 1) VBR（Verify Before Reporting）

当准备说“已完成/已修复”前，先执行：

1. 验证机制是否真的变更（不是只改文案）
2. 验证行为是否符合目标（实际跑通）
3. 记录证据（命令输出/文件变更/任务日志）

未验证，不报“完成”。

## 2) Cron 架构区分

为每个定时任务先判定类型：

- **Prompted（提示型）**：需要主会话关注/交互
- **Autonomous（自治型）**：后台脚本可独立完成

默认把“必须发生”的维护任务做成 Autonomous，避免“有提醒没执行”。

## 3) Tool Migration Checklist

迁移工具/脚本时必须全量检索并更新：

- cron 任务
- `ops/` 脚本
- `AGENTS.md` / `TOOLS.md` / `HEARTBEAT.md`
- 相关 skills 与模板

迁移完成后做双验证：

- 旧路径不可用或不再被调用
- 新路径可执行且有日志证据

## 4) Compaction Recovery（压缩恢复）

触发条件：上下文压缩、会话丢失、用户问“刚聊到哪”。

恢复顺序：

1. 读取 `memory/YYYY-MM-DD.md`（今日/昨日）
2. 读取 `MEMORY.md`（主会话）
3. 读取 `memory/archives/*.md`（周归档）
4. 读取 `memory/memory.db`（主检索源）

恢复后先给简短确认，再继续任务。

## 5) 不接入项（当前阶段）

- 高频 heartbeat 驱动的主动触发
- “尝试 10 种方法”硬性指标
- 全量自演化/自改写机制

这些功能待周末复盘后再评估。

## 6) 安全与成本

- 外部机制引入先扫描再接入（semgrep/trufflehog/pip-audit/本地正则）
- 任何主动流程不得绕过用户边界与审批规则
- 日常优先中短回复，避免主动机制造成 token 噪音

## References

- `references/adoption-notes.md`
