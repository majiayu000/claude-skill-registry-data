---
name: huawei-cloud-cost-estimation-cn
description: >-
  估算华为云下单前费用，通过 hcloud 开通白名单内资源，并引导用户通过控制台处理退订。
  适用于华为云询价、预算、资源创建、退订指引或 hcloud 可用性检查。
compatibility: 需要 hcloud KooCLI 7.2+、对应的 IAM 权限和网络连接；依赖由用户自行安装配置
metadata:
  language: zh-CN
  translation_of: huawei-cloud-cost-estimation
  author: concept-git
  version: "3.3.0"
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/concept-git/cloud-concept-skills/tree/main/skills/zh-CN/huawei-cloud-cost-estimation-cn
    envVars:
      - {name: HUAWEICLOUD_SDK_AK, required: false}
      - {name: HUAWEICLOUD_SDK_SK, required: false}
      - {name: HUAWEICLOUD_SDK_REGION, required: false}
---

# 华为云询价与开通

社区维护，非华为云官方技能。依据当前 API 证据和命令帮助处理。

## 按任务查阅

判断或调用前，先读 `references/gotchas.md` 对应类别。表内路径相对 `references/`；只读相关段落，已读复用。

| 要做什么 | 读哪里 | 陷阱类别 |
| --- | --- | --- |
| 检查hcloud是否可用 | `cli-installation.md` | A |
| 报价／比价 | `pricing/commands.md` | A、B |
| 判断兼容性 | `lifecycle/concepts.md`：相关检查 | A、C |
| 查已有订单／处理报错 | 对应只读接口的当前帮助 | A、D |
| 准备登录方式 | `lifecycle/concepts.md`：登录选择 | E |
| 准备开通 | `lifecycle/concepts.md`；`lifecycle/commands.md` 中所选操作、依赖及支付字段 | A–D；涉及凭证加E |
| 退订／停用 | `lifecycle/concepts.md`：退订段，仅引导控制台 | — |

准备开通时，报价有缺项或变化才补读询价文件。账单和余额用账单只读技能或费用中心；其他云、白名单外写操作转对应控制台。

## 报价

1. 确定服务、区域、配置、数量、计费方式和周期／用量。影响选择的缺项一次问清；用户授权选择时，按预算和用途选择并说明依据。仅询价时说明 Linux／空 AZ／NA 假设，计费方式与时长由用户确定。
2. 按询价契约找到候选和产品计费映射。仅提交符合G03–G06 准入条件的项目；保留配置、来源、确切请求和匹配响应。
3. 分项展示已核实价格与缺项，核对合计／币种、注明查询日期。导出报价沿用相同证据及项目状态；这不是最终账单。

## 开通

1. 在白名单中找到操作，读当前帮助。通过只读查询核实依赖，各项附依据标为“支持／不兼容／待核实”。
2. 对完整配置和关联费用询价。费用待核实时说明可能收费并取得额外同意；已知不兼容仍须停止。
3. 构造明确包含支付、续费、登录选择的最终请求。按 G09／G12 核对条件字段，执行全局 `--dryrun`，将已检查请求版本与证据关联保存。
4. 展示配置、费用、执行顺序，将确认关联到该请求。正式调用单独执行，只移除全局 `--dryrun`；修改或失败按 G09–G11 处理。
5. 查询订单／支付与资源结果，报告已核实结果及待核实项，将返回编号与已检查请求、确认关联保存。

## 沟通与查阅

按用户语言通俗说明结论、依据和下一步。明确的只读工作连续完成，不反复求许可；长流程报告进度。仅询问缺失的决策和必要的购买确认。

- 权限失败：`references/iam-policies.md`。
- 字段关系不清：`references/pricing/rfq-models/rfq-core.yml`，再读当前计费模式对应模型。
