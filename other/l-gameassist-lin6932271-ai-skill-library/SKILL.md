---
name: l-gameassist
description: "自有游戏、离线调试、状态与引擎分析；在对应任务需要领域分流时使用。"
---

# 游戏辅助分析入口

## 入口决策

自有游戏、离线调试、状态与引擎分析。从目标与现有证据确定实际需要的分析模块。

先明确样本/目标、版本、允许的操作和希望得到的结果。不要把客户端状态当成服务端状态，或把静态线索当成业务结论。

## 按需要读取

- `game-hacking`：读取 [技能正文](../game-hacking/SKILL.md)。
- `protocol-reverse`：读取 [技能正文](../protocol-reverse/SKILL.md)。
- `reverse-engineering`：读取 [技能正文](../reverse-engineering/SKILL.md)。
- `patch-rollback`：读取 [技能正文](../patch-rollback/SKILL.md)。

只加载当前任务相关模块。工具可用性与运行条件以本机为准；缺少数据时保留已确认结论与下一步所需证据。
