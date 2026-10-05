---
name: sealeap-apollo-sellersprite-reviews
description: "使用卖家精灵数据获取指定 ASIN 的评论列表，用于快速查看买家反馈。用于评论列表相关的 Amazon 数据查询、核验和分析。"
license: "MIT; see LICENSE and NOTICE"
---

# Amazon 卖家精灵 评论列表

获取指定 ASIN 的评论列表，用于快速查看买家反馈。

## 必要输入

站点 + ASIN + 评论筛选条件。补充统计窗口、输出数量和现有数据范围；不能由 ASIN 前缀推断站点。

## 工作流

1. 固定输入口径，先查看已有数据的范围与时效。
2. 按 [工具路由](references/tool-routing.md) 选择实际可用能力，确认当前 schema。
3. 检查请求状态、实际对象、时间、分页和完整性后再解释结果。
4. 按 [执行手册](references/playbook.md) 完成评论列表，关联原始证据。
5. 交付评论标题、内容、评分、评论人、时间和原始字段；附来源、统计期、缺失原因和可继续的验证动作。

## 数据口径

- 固定 Amazon 站点、ASIN/类目/关键词、窗口、时区、币种、单位、分页与排序。英国站的 UK/GB 和各提供方站点编码在接口边界映射，原始代码保留。
- 原始记录和可见页面事实为 `FACT`，第三方销量、搜索量和流量推算为 `ESTIMATE`，分析参数为 `ASSUMPTION`，未获得信息为 `UNKNOWN`。标签按字段填写。
- 每条记录保留 `source`、`collected_at`、`data_period`、`marketplace`、`evidence_id`、`raw_field` 和 `limitations`。不要把采集时间当成数据统计期。
- 空值为 null，展示为“—”。零必须来自明确返回；请求失败、权限不足、无匹配和截断分别记录。评分或排名不是销量。
- 沿用用户授权的数据范围和费用上限；请求数量、站点或付费范围发生实质变化时再补足授权。密钥仅由现有连接器读取，不放进对话、命令示例、报告或版本库。

## 交付边界

本 Skill 提供查询与分析，不修改 Listing、广告、收藏或店铺配置。数据不足时缩小结论范围；不能把调用成功当作市场判断成立。

许可与材料范围见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。
