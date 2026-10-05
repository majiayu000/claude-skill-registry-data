---
name: sealeap-apollo-price-discounts
description: "读取 Amazon Seller Central 价格折扣数据，核对活动与 SKU，并生成指定 SKU 的折扣变更计划。用于查折扣、批量折扣审查或准备已授权变更；默认只读与草稿。"
license: "MIT; see LICENSE and NOTICE"
---

# Amazon 价格折扣核查与计划

读取 Amazon Seller Central 价格折扣数据，核对活动与 SKU，并生成指定 SKU 的折扣变更计划。用于查折扣、批量折扣审查或准备已授权变更；默认只读与草稿。

## 执行流程

1. 确认目标店铺、站点和当前授权会话；不存在默认店铺或默认账号。
2. 读取活动/商品明细与当前校验状态，折扣比例直接取活动字段；实时 Offer 价格仅作补充。
3. 用 `python3 scripts/discount_plan.py --input <discounts.json> --output <plan.json>` 生成离线计划，检查 SKU 与活动唯一性、前值和百分比。
4. 用户已明确授权提交时，重新读取活动并比对计划前值，通过当前可用的官方界面或已验证接口精确修改目标字段。
5. 回读目标 SKU 与其他 SKU，分别报告提交接受、配置保存、审核状态及前台价格同步状态。

## 数据口径

- 固定 Amazon 站点、ASIN/类目/关键词、窗口、时区、币种、单位、分页与排序。英国站的 UK/GB 和各提供方站点编码在接口边界映射，原始代码保留。
- 原始记录和可见页面事实为 `FACT`，第三方销量、搜索量和流量推算为 `ESTIMATE`，分析参数为 `ASSUMPTION`，未获得信息为 `UNKNOWN`。标签按字段填写。
- 每条记录保留 `source`、`collected_at`、`data_period`、`marketplace`、`evidence_id`、`raw_field` 和 `limitations`。不要把采集时间当成数据统计期。
- 空值为 null，展示为“—”。零必须来自明确返回；请求失败、权限不足、无匹配和截断分别记录。评分或排名不是销量。
- 沿用用户授权的数据范围和费用上限；请求数量、站点或付费范围发生实质变化时再补足授权。密钥仅由现有连接器读取，不放进对话、命令示例、报告或版本库。

## 交付与验证

按 [执行手册](references/playbook.md) 组织字段、分析和验收；按 [工具路由](references/tool-routing.md) 取得数据。报告中的每个重要判断需关联证据，缺口影响决策时保留 `HOLD`。

许可与材料范围见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。
