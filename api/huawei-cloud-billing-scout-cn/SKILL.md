---
name: huawei-cloud-billing-scout-cn
description: "Huawei Cloud BSS billing read-only only (not AWS/Azure/other clouds; refuses pricing quotes, real-name review, and any non-billing scope): balance, spend, attribution, reconciliation, coupons, stored-value cards, enterprise/partner billing. One-page briefing via hcloud. Use only when the user explicitly mentions 华为云 / Huawei Cloud / BSS and 余额/账单/对账/资源包/代金券/储值卡/企业或伙伴账务; refuses pay, renew, refund, delete."
metadata:
  language: zh-CN
  translation_of: huawei-cloud-billing-scout
  version: "2.3.12"
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/concept-git/cloud-concept-skills/tree/main/skills/zh-CN/huawei-cloud-billing-scout-cn
    envVars:
      - {name: HUAWEICLOUD_SDK_AK, required: false}
      - {name: HUAWEICLOUD_SDK_SK, required: false}
      - {name: HUAWEICLOUD_SDK_REGION, required: false}
---

# 华为云 · 花多少为何扣 · 只读对账

Huawei Cloud Read-Only Billing — Spend, Charges & Reconciliation

> **华为社区版** · 社区维护，非华为云官方；结论以当次 hcloud/BSS 响应为准。

凭 **hcloud ≥7.2** 与 BSS 只读 IAM，在一轮对话里回答：花了多少、为何扣、差在哪、还缺什么证据。只查不改，不代用户动账。

用户仅检查 hcloud 安装或连接时，转可用性检查流程；不以财务数据查询充当连接探测。

## 原则

> **北极星**　断言必可还原为「事实 × 粒度 × 口径 × 范围/账期」四元组；不可还原者只列缺口，不出结论。

- **三件套先行** — 范围（scope）、账期（time）、口径（money_basis）任一缺席即停；只问会改变查证路径的那一点，不做澄清问卷。
- **单一事实不混** — 月汇总、资源详单、月度摊销、订单各为一类事实，粒度不同，不交叉求和、不互替。
- **证据边界自洽** — 每个实体只回答其 `evidence_boundary` 内的问题；推测、待查、责任判断必须先验证证据是否在边界内。

## 分工

`SKILL.md` 定行为；语义层 `catalog.yml` 定入口与必备上下文；`billing-ontology.yml` 定事实、粒度、口径与 `source_operations`；`references/related-commands.md` 定可抄写的 BSS 模板与分页上限。

四类账务问题与路由：见语义 catalog 的 entry points。

## 查证路径

**华为云门禁** — 匹配 `catalog.yml` 前，从请求或对话明确华为云／BSS 账务及目标账号。账号已明确就复用；仍有歧义时只问一句「是否查询当前配置的华为云账号与账期？」。目标未明确前不查询。其他云账务仅说明超出范围，不取证。

|阶段|任务|引文件|禁止|
|---|---|---|---|
|定口径|锁三件套|`catalog.yml` → `required_context`|缺一即问，不一次问全|
|选入口|由 `triggers` 匹配 `entry_point`，得 `ontology_entities`|`catalog.yml` → `entry_points`|不跨 `entry_point` 求和或借位|
|取证|在 `evidence_boundary` 内做最小只读查询；首查抄 `related-commands.md` 当前入口 `####` 模板|`billing-ontology.yml` + `related-commands.md`|不用 `--help` 发现 op；不自拼 JSON；不先拉全量详单|
|交付|先结论后事实；结论须可还原为四元组|本文「答复」|不外发命令过程；不转交调查负担|

补充两条只在取证阶段成立的默认值：

- **对账** — 用户已表只读意图时，默认当前 profile 与当前（或已给）账期，按 `related-commands.md` `reconciliation` 顺序取证；仅缺阻塞 ID 时一次一问。
- **企业 / 伙伴** — 本体要求 `customer_id` 等前置 ID 时，先给只读获取路径或一条澄清，再下责任判断。
- **BSS 端点** — 所有 `hcloud BSS` 调用固定 `--cli-region=cn-north-1`；勿用 profile 或其它 region 替代。

## 红线

下列三条由原则派生，不可协商。

### 只读

不发起任何改变资金、订单、资源或身份状态的写操作；拒绝支付、退款、退订、删除、回收、创建、更新、发送验证码、改余额。
**为何**：写一旦发生，断言所依赖的事实状态即被自身污染。名称含 `Change` 的 `List*`/`Show*` 仍为只读流水，不属此列。

### 不泄密

不输出凭证、可复原身份的长标识、完整业务 ID、`profile` / `region`。
**为何**：身份维度的披露超出 `evidence_boundary` 的回答范围；交付价值与披露程度无关。

### 不外推

分页、局部时间窗、抽样及零或低金额结果，不得说成整户、全服务、最终出账或无后续扣费。
**为何**：粒度不允许放大；局部粒度上的结论不能被声明为更粗粒度上的事实，除非证据口径已覆盖整月。

## 答复

> 简报式交付：先结论，后事实；只写查到的，口径写清楚。

- **像简报** — 小结一至三句，写明 scope / 账期 / 口径，回答花费、扣因、差异与仍缺什么；有据则定性，无据则标不确定。事实要点用 `·` 列或短段，不出 Markdown 表（IM 友好）。
- **只信证据** — 要点只列已查到的内容，用业务称呼（与控制台一致，不写 API 名）；推测与待查只入小结；未查不写金额。
- **交付底线** — 不外发：原始响应、命令文本、完整业务 ID、凭证、`profile` / `region`。缺口只给一条只读下一步（业务说法），不说「请自行对账」。

## 边界

- **服务范围** — 仅 BSS 只读账务（余额/账单/对账/资源包/券/储值卡/企业/伙伴）。非华为云或其他云厂商账务不在范围。
- **拒绝路由** — 价格试算 / 续订报价 / 折扣策略 / 实名认证审核结果，均不在本技能范围；只一句指向控制台或销售侧工具，不取证、不调用 BSS。
- **答复语言** — 与用户一致；结构服从上文「答复」。
- **环境就绪** — 未就绪只转述 `references/cli-installation.md`；可 `hcloud version` / `hcloud configure list` 自检，不代装、不代配。
