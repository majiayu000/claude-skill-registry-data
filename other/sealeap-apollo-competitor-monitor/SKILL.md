---
name: sealeap-apollo-competitor-monitor
description: "建立 Amazon 竞品核验、时间快照、价格与 Listing 变化记录，以及本地 HTML 总览。用于竞品监控、排名复盘、历史快照和变化分析；支持授权采集后导入 SQLite。"
license: "MIT; see LICENSE and NOTICE"
---

# Amazon 竞品快照与变化监控

建立 Amazon 竞品核验、时间快照、价格与 Listing 变化记录，以及本地 HTML 总览。用于竞品监控、排名复盘、历史快照和变化分析；支持授权采集后导入 SQLite。

## 执行流程

1. 核对站点和自有 ASIN，定义购买对象、结构、规格、价格单位和排除条件。
2. 先按细类目发现候选，再逐条核对返回 ASIN 和产品边界；未核验、失败和拒绝记录保留为候选。
3. 按 [快照输入](references/snapshot-input.md) 填写已有授权数据，用 `python3 scripts/snapshots.py import --db <本地.db> --input <snapshot.json>` 追加导入。
4. 用 `python3 scripts/snapshots.py report --db <本地.db> --output <新报告.html>` 生成快照与前后变化表，核对原值和时间。
5. 基于已确认变化提出 Listing 或广告建议，区分观察与解释；定时采集须按用户给定的范围、频率和成本接入实际可运行的数据源。

## 数据口径

- 固定 Amazon 站点、ASIN/类目/关键词、窗口、时区、币种、单位、分页与排序。英国站的 UK/GB 和各提供方站点编码在接口边界映射，原始代码保留。
- 原始记录和可见页面事实为 `FACT`，第三方销量、搜索量和流量推算为 `ESTIMATE`，分析参数为 `ASSUMPTION`，未获得信息为 `UNKNOWN`。标签按字段填写。
- 每条记录保留 `source`、`collected_at`、`data_period`、`marketplace`、`evidence_id`、`raw_field` 和 `limitations`。不要把采集时间当成数据统计期。
- 空值为 null，展示为“—”。零必须来自明确返回；请求失败、权限不足、无匹配和截断分别记录。评分或排名不是销量。
- 沿用用户授权的数据范围和费用上限；请求数量、站点或付费范围发生实质变化时再补足授权。密钥仅由现有连接器读取，不放进对话、命令示例、报告或版本库。

## 交付与验证

按 [执行手册](references/playbook.md) 组织字段、分析和验收；按 [工具路由](references/tool-routing.md) 取得数据。报告中的每个重要判断需关联证据，缺口影响决策时保留 `HOLD`。

许可与材料范围见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。
