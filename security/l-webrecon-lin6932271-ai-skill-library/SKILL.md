---
name: l-webrecon
description: "Web/API 的范围确定、低影响探测、权限与数据边界检查；在对应任务需要领域分流时使用。"
---

# Web 与安全测试入口

## 入口决策

Web/API 的范围确定、低影响探测、权限与数据边界检查。从目标与现有证据确定实际需要的分析模块。

先明确样本/目标、版本、允许的操作和希望得到的结果。不要把客户端状态当成服务端状态，或把静态线索当成业务结论。

## 按需要读取

- `pentest-tools`：读取 [技能正文](../pentest-tools/SKILL.md)。
- `api-security`：读取 [技能正文](../api-security/SKILL.md)。
- `network-analysis`：读取 [技能正文](../network-analysis/SKILL.md)。
- `code-audit`：读取 [技能正文](../code-audit/SKILL.md)。
- `cloud-k8s`：读取 [技能正文](../cloud-k8s/SKILL.md)。

只加载当前任务相关模块。工具可用性与运行条件以本机为准；缺少数据时保留已确认结论与下一步所需证据。
