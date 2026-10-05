---
name: sealeap-apollo-ads-demo
description: "生成可独立打开的 Amazon 广告规则演示页，使用明确标注的合成 Campaign 指标比较规则命中与拟调整状态。用于广告规则、阈值或 Dry Run 教学演示。"
license: "MIT; see LICENSE and NOTICE"
---

# Amazon 广告规则离线演示

生成可独立打开的 Amazon 广告规则演示页，使用明确标注的合成 Campaign 指标比较规则命中与拟调整状态。用于广告规则、阈值或 Dry Run 教学演示。

## 执行流程

1. 确认演示目标与输出位置，合成数据和用户真实报表分别使用。
2. 用 `python3 scripts/build_demo.py --output <新文件.html>` 生成页面；此脚本不联网，不连接账户。
3. 调整最低点击、最低花费、最高 ACOS 等参数，查看命中原因与拟暂停项；阈值是教学参数。
4. 核验指标分母、零订单、刷新后参数状态和输出文件，记录仅完成离线演示的验证范围。

## 数据口径

- 固定 Amazon 站点、ASIN/类目/关键词、窗口、时区、币种、单位、分页与排序。英国站的 UK/GB 和各提供方站点编码在接口边界映射，原始代码保留。
- 原始记录和可见页面事实为 `FACT`，第三方销量、搜索量和流量推算为 `ESTIMATE`，分析参数为 `ASSUMPTION`，未获得信息为 `UNKNOWN`。标签按字段填写。
- 每条记录保留 `source`、`collected_at`、`data_period`、`marketplace`、`evidence_id`、`raw_field` 和 `limitations`。不要把采集时间当成数据统计期。
- 空值为 null，展示为“—”。零必须来自明确返回；请求失败、权限不足、无匹配和截断分别记录。评分或排名不是销量。
- 沿用用户授权的数据范围和费用上限；请求数量、站点或付费范围发生实质变化时再补足授权。密钥仅由现有连接器读取，不放进对话、命令示例、报告或版本库。

## 交付与验证

按 [执行手册](references/playbook.md) 组织字段、分析和验收；按 [工具路由](references/tool-routing.md) 取得数据。报告中的每个重要判断需关联证据，缺口影响决策时保留 `HOLD`。

本集合提供离线规则演示文件生成器。真实 ERP 与 Amazon Ads 写入需要另行接入并验证。

许可与材料范围见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。
