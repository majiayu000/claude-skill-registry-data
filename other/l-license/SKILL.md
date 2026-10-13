---
name: l-license
description: "授权/激活机制、客户端判断与服务器授权边界分析；在对应任务需要领域分流时使用。"
---

# 授权与激活分析入口

## 入口决策

授权/激活机制、客户端判断与服务器授权边界分析。从目标与现有证据确定实际需要的分析模块。

先明确样本/目标、版本、允许的操作和希望得到的结果。不要把客户端状态当成服务端状态，或把静态线索当成业务结论。

## 按需要读取

- `reverse-engineering`：读取 [技能正文](../reverse-engineering/SKILL.md)。
- `dotnet-reverse`：读取 [技能正文](../dotnet-reverse/SKILL.md)。
- `apk-reverse`：读取 [技能正文](../apk-reverse/SKILL.md)。
- `thick-client`：读取 [技能正文](../thick-client/SKILL.md)。

只加载当前任务相关模块。工具可用性与运行条件以本机为准；缺少数据时保留已确认结论与下一步所需证据。
