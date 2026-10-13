---
name: l-reverse
description: "按样本格式路由二进制、移动端、JS 和协议逆向任务；在对应任务需要领域分流时使用。"
---

# 逆向分析入口

## 入口决策

按样本格式路由二进制、移动端、JS 和协议逆向任务。从目标与现有证据确定实际需要的分析模块。

先明确样本/目标、版本、允许的操作和希望得到的结果。不要把客户端状态当成服务端状态，或把静态线索当成业务结论。

## 按需要读取

- `reverse_flow_skill`：读取 [技能正文](../reverse_flow_skill/SKILL.md)。
- `apk-reverse`：读取 [技能正文](../apk-reverse/SKILL.md)。
- `js-reverse`：读取 [技能正文](../js-reverse/SKILL.md)。
- `dotnet-reverse`：读取 [技能正文](../dotnet-reverse/SKILL.md)。
- `protocol-reverse`：读取 [技能正文](../protocol-reverse/SKILL.md)。
- `reverse-engineering`：读取 [技能正文](../reverse-engineering/SKILL.md)。

只加载当前任务相关模块。工具可用性与运行条件以本机为准；缺少数据时保留已确认结论与下一步所需证据。
