---
name: sealeap-apollo-product-research
description: "开展 Amazon 需求、竞争、关键词、评论、供应、完整成本与市场进入判断，输出来源可追溯的 Markdown、离线 HTML 和结构化数据；用于品类调研或选品评审。"
license: "MIT; see LICENSE and NOTICE"
---

# Amazon 选品研究与决策报告

开展 Amazon 需求、竞争、关键词、评论、供应、完整成本与市场进入判断，输出来源可追溯的 Markdown、离线 HTML 和结构化数据；用于品类调研或选品评审。

## 执行流程

1. 固定站点、购买任务、规格单位、预算、风险约束与观察期，冻结类目背景池和直接竞争样本。
2. 保存商品、父子体、词、历史和评论证据；原始值与标准化值并存，核对请求范围与实际覆盖。
3. 计算可比样本内价格带、品牌份额、新品表现与交叉维度，缺失不伪装成零。
4. 把 VOC 转成可实现的差异化假设，供应报价统一规格、MOQ、税费、运费与交付条款。
5. 分别评估需求、产品和商业可行性，展示成本与现金下行情景，给出 GO/HOLD/NO-GO 及证据。
6. 按 [报告输入](references/report-input.md) 写统一 payload，使用 `python3 scripts/render_report.py --input <payload.json> --output-dir <新目录>` 渲染并校验交付。

## 数据口径

- 固定 Amazon 站点、ASIN/类目/关键词、窗口、时区、币种、单位、分页与排序。英国站的 UK/GB 和各提供方站点编码在接口边界映射，原始代码保留。
- 原始记录和可见页面事实为 `FACT`，第三方销量、搜索量和流量推算为 `ESTIMATE`，分析参数为 `ASSUMPTION`，未获得信息为 `UNKNOWN`。标签按字段填写。
- 每条记录保留 `source`、`collected_at`、`data_period`、`marketplace`、`evidence_id`、`raw_field` 和 `limitations`。不要把采集时间当成数据统计期。
- 空值为 null，展示为“—”。零必须来自明确返回；请求失败、权限不足、无匹配和截断分别记录。评分或排名不是销量。
- 沿用用户授权的数据范围和费用上限；请求数量、站点或付费范围发生实质变化时再补足授权。密钥仅由现有连接器读取，不放进对话、命令示例、报告或版本库。

## 交付与验证

按 [执行手册](references/playbook.md) 组织字段、分析和验收；按 [工具路由](references/tool-routing.md) 取得数据。报告中的每个重要判断需关联证据，缺口影响决策时保留 `HOLD`。

许可与材料范围见 [LICENSE](LICENSE) 和 [NOTICE](NOTICE)。
