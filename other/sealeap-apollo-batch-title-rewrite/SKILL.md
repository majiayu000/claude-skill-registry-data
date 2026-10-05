---
name: sealeap-apollo-batch-title-rewrite
description: "批量改写 Amazon Item name 与 Item highlights，核对商品事实、站点和类目规则，并生成标题与亮点长度检查结果。用于 75 字符标题改写、商品亮点或批量上传前审查。"
license: "MIT; see LICENSE and NOTICE"
---

# Amazon 批量标题与商品亮点

批量改写 Amazon Item name 与 Item highlights，核对商品事实、站点和类目规则，并生成标题与亮点长度检查结果。用于 75 字符标题改写、商品亮点或批量上传前审查。

## 执行流程

1. 保留输入文件与 SKU/ASIN 映射，确认站点、类目、父子体及所用官方模板。
2. 先核对当时适用的官方规则，再设 title_max、highlight_max、计数方式及规则来源；不能把 US 规则自动扩展到所有站点和媒介类目。
3. 标题优先产品身份、结构和关键规格；亮点补充可验证的材质、兼容条件、用途与差异。
4. 用 `python3 scripts/check_titles.py --input <改写.csv> --policy <policy.json> --output <检查.csv>` 做离线逐行检查。
5. 对词义、促销用语、品牌规范、重复、父子关系与当前类目模板做人工式复核；只交付草稿，按已授权范围另行提交。

## 数据口径

- 固定 Amazon 站点、ASIN/类目/关键词、窗口、时区、币种、单位、分页与排序。英国站的 UK/GB 和各提供方站点编码在接口边界映射，原始代码保留。
- 原始记录和可见页面事实为 `FACT`，第三方销量、搜索量和流量推算为 `ESTIMATE`，分析参数为 `ASSUMPTION`，未获得信息为 `UNKNOWN`。标签按字段填写。
- 每条记录保留 `source`、`collected_at`、`data_period`、`marketplace`、`evidence_id`、`raw_field` 和 `limitations`。不要把采集时间当成数据统计期。
- 空值为 null，展示为“—”。零必须来自明确返回；请求失败、权限不足、无匹配和截断分别记录。评分或排名不是销量。
- 沿用用户授权的数据范围和费用上限；请求数量、站点或付费范围发生实质变化时再补足授权。密钥仅由现有连接器读取，不放进对话、命令示例、报告或版本库。

## 交付与验证

按 [执行手册](references/playbook.md) 组织字段、分析和验收；按 [工具路由](references/tool-routing.md) 取得数据。报告中的每个重要判断需关联证据，缺口影响决策时保留 `HOLD`。

许可与材料范围见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。
