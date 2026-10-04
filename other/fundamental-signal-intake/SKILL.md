---
name: fundamental-signal-intake
description: 为上市公司采集微观领先事实，建立点时可用、业务与驱动明确的证据账本和缺口清单；不做盈利预测、估值或技术面。
---

# 基本面微观信号采集

优先观察真实经营行为，财报用于对账验证。仅使用公开、授权或用户提供的数据。

1. 明确主体、完整业务边界、经营变量和带时区的研究截止时点。
2. 按需从 [source-matrix.md](references/source-matrix.md) 选择订单、成交价格、物流、库存位置、产能形成、交付验收、客户使用、招聘和政策执行信号。说明业务、驱动、领先关系及可能断裂环节，不全量拉取。
3. 对接来源时读 [provider-contract.md](references/provider-contract.md)，保留原始值、查询、来源和历史版本。
4. 按 [evidence-ledger.md](references/evidence-ledger.md) 建账。事实、公司声称、线索、冲突和缺失分开；未知不等于零，同源转载不算独立确认。
5. 运行 `python -B scripts/validate_ledger.py <ledger.json>`，失败账本不能作为合格输入交接。

时间必须含时区，不能只写日期。计算放在估值节点图，不接受 calculated 账本状态。校验通过不证明来源真实。

交付业务观察图、采集清单、账本、反证、冲突、缺口及访问限制。估值交给 evidence-driven-valuation；技术面交给独立量化代码。

