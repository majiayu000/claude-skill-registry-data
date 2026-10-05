---
name: sealeap-apollo-keyword-library
description: "由 Amazon ASIN 建立可追溯的竞品与关键词库，完成原始词保留、产品词根、R0–R3 相关性、L1–L4 意图层级、P0–P3 优先级及广告和 Listing 映射。"
license: "MIT; see LICENSE and NOTICE"
---

# Amazon ASIN 分层关键词库

由 Amazon ASIN 建立可追溯的竞品与关键词库，完成原始词保留、产品词根、R0–R3 相关性、L1–L4 意图层级、P0–P3 优先级及广告和 Listing 映射。

## 执行流程

1. 从输入或链接识别 ASIN 与站点；核对形态、用途、规格、材质、包数及功能硬边界。
2. 以直接竞品、标杆和新品分别发现候选，逐项核验详情与相关性，记录父子重复关系。
3. 按授权查询范围反查目标和竞品词；保留每个来源 ASIN、期别和原词，不按同词重复累加搜索量。
4. 标准化词条并关联重复组，再标记主词根、R/L/P 分类、分类证据与待验证项。
5. 把词映射到广告、Listing 或否定候选，输出可筛选词库和基于明细的总览。

## 数据口径

- 固定 Amazon 站点、ASIN/类目/关键词、窗口、时区、币种、单位、分页与排序。英国站的 UK/GB 和各提供方站点编码在接口边界映射，原始代码保留。
- 原始记录和可见页面事实为 `FACT`，第三方销量、搜索量和流量推算为 `ESTIMATE`，分析参数为 `ASSUMPTION`，未获得信息为 `UNKNOWN`。标签按字段填写。
- 每条记录保留 `source`、`collected_at`、`data_period`、`marketplace`、`evidence_id`、`raw_field` 和 `limitations`。不要把采集时间当成数据统计期。
- 空值为 null，展示为“—”。零必须来自明确返回；请求失败、权限不足、无匹配和截断分别记录。评分或排名不是销量。
- 沿用用户授权的数据范围和费用上限；请求数量、站点或付费范围发生实质变化时再补足授权。密钥仅由现有连接器读取，不放进对话、命令示例、报告或版本库。

## 交付与验证

按 [执行手册](references/playbook.md) 组织字段、分析和验收；按 [工具路由](references/tool-routing.md) 取得数据。报告中的每个重要判断需关联证据，缺口影响决策时保留 `HOLD`。

许可与材料范围见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。
