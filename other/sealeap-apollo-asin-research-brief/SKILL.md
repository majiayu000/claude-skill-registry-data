---
name: sealeap-apollo-asin-research-brief
description: "围绕一个 Amazon ASIN 整理商品事实、类目与竞品、历史趋势、关键词、评论、供应和风险，交付可离线打开的中文 HTML 研究简报。"
license: "MIT; see LICENSE and NOTICE"
---

# Amazon ASIN 深度调研简报

围绕一个 Amazon ASIN 整理商品事实、类目与竞品、历史趋势、关键词、评论、供应和风险，交付可离线打开的中文 HTML 研究简报。

## 执行流程

1. 核对 ASIN、站点、目标购买任务和数据窗口。
2. 按需求获取商品、变体、趋势、类目、关键词、相似品及评论证据，缺项逐项标记。
3. 区分市场机会、产品差异化与商业可行性；接口利润不替代完整采购和履约测算。
4. 将原始证据转成结构化 payload；用 `python3 scripts/render_report.py --input <payload.json> --output-dir <新目录>` 生成 HTML、Markdown 与数据副本。
5. 验证表格、缺失值、来源和结论一致；交付简报及最能改变判断的下一项证据。

## 数据口径

- 固定 Amazon 站点、ASIN/类目/关键词、窗口、时区、币种、单位、分页与排序。英国站的 UK/GB 和各提供方站点编码在接口边界映射，原始代码保留。
- 原始记录和可见页面事实为 `FACT`，第三方销量、搜索量和流量推算为 `ESTIMATE`，分析参数为 `ASSUMPTION`，未获得信息为 `UNKNOWN`。标签按字段填写。
- 每条记录保留 `source`、`collected_at`、`data_period`、`marketplace`、`evidence_id`、`raw_field` 和 `limitations`。不要把采集时间当成数据统计期。
- 空值为 null，展示为“—”。零必须来自明确返回；请求失败、权限不足、无匹配和截断分别记录。评分或排名不是销量。
- 沿用用户授权的数据范围和费用上限；请求数量、站点或付费范围发生实质变化时再补足授权。密钥仅由现有连接器读取，不放进对话、命令示例、报告或版本库。

## 交付与验证

按 [执行手册](references/playbook.md) 组织字段、分析和验收；按 [工具路由](references/tool-routing.md) 取得数据。报告中的每个重要判断需关联证据，缺口影响决策时保留 `HOLD`。

许可与材料范围见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。
