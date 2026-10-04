---
name: evidence-driven-valuation
description: 将点时可用的微观证据转换为经营变量，执行证据闸门、行业适配、特殊价值和独立反向估值；缺输入时报告缺口，不填默认假设，不做技术面。
---

# 证据驱动估值

事实 → 业务 → 数量/价格/成本/营运资金/资本开支 → 现金流。财报用于验证，不替代微观证据。不得用当前股价或同行倍数校准正向价值。

1. 接收 fundamental-signal-intake 合格账本；两 Skill 必须位于同一 skills 根目录。
2. 构建输入时读 [valuation-input-schema.md](references/valuation-input-schema.md)。仅接受 v2；旧日期、手填充分状态和顶层 provenance 不兼容，不能自动补默认值迁移。
3. 按 [causal-conversion.md](references/causal-conversion.md) 建可复算节点。不能被证据约束的参数只做明确条件分析或报告缺口。
4. 按 [evidence-gate.md](references/evidence-gate.md) 定义完整业务和阈值，再计算闸门。手填 pass 不能放行。
5. 按 [industry-routing.md](references/industry-routing.md) 选已实现方法；特殊股权、周期、新产品、资产、融资读 [special-valuations.md](references/special-valuations.md)。缺行业方法不能降级套倍数。
6. 运行 `python -B scripts/valuation_engine.py <input.json>`。失败不能绕过 evaluate/CLI 直接调用公式。
7. 独立价值完成后附加 reverse_valuation 与融资分析，不能回写正向价值。

交付闸门、经营桥、分业务方法与来源、情景价值及每股单位、特殊价值归属、反向条件、缺口和证伪条件。技术面完全分离。

仍需人工核验原文、独立性、重大业务完整性及区间依据。已知限制见 [audit-notes.md](references/audit-notes.md)。[synthetic-handoff.json](examples/synthetic-handoff.json) 是纯合成可运行样例，不是投资输入或通用参数模板。

