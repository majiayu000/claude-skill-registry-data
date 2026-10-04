---
name: ai-performance
description: "性能诊断助手适合technical、产品、市场营销、software在用户提出“性能哪里拖慢了”这类问题，需要快速拆解目标、判断重点并形成可执行结果时使用，帮助基于输入材料生成问题归因、服务改进建议、SOP 或 FAQ 清单。"
requiredEnvVars:
  - name: AISKILLS_API_KEY
    description: "从 AI Skills 官网 https://ai-skills.ai 获取API Key，用于运行时技能调用。"
---

# ai-performance 性能诊断助手

[快速开始](https://github.com/allinherog-star/ai-skills/tree/main#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)

[更多技能](https://ai-skills.ai)

### 概述

性能诊断助手用于回答「性能哪里拖慢了」、性能诊断、网站质量、体验指标，适合technical、产品、市场营销、software在明确业务目标、内容材料或分析对象后调用。
它会结合页面 URL、报告或问题描述、粘贴页面 URL、性能报告摘要、Core Web Vitals 指…等输入，整理关键上下文，并输出问题归因、服务改进建议、SOP 或 FAQ 清单，便于继续执行、复盘或交付。
能力定位补充：skills.sh all-time/hot 信号显示 performance 有用户需求；平台展示为 local_service_ops 业务助手目录，输出可复核诊断、建议或生产准备包。

### 什么时候使用

**适用场景**

- 用户提出“性能哪里拖慢了”这类问题，需要快速拆解目标、判断重点并形成可执行结果
- technical、产品、市场营销、software需要围绕性能诊断助手生成问题归因、服务改进建议、SOP 或 FAQ 清单
- 用户已经准备了诊断目标（说明要定位的性能、可用性、搜索、转化或上线检查目标。）、影响对象（说明受影响的用户、设备、页面类型、地区或业务场景。）、待诊断页面链接（填写公开可访问的待诊断页面、站点、报告或参考链接。），希望整理成可执行的分析或优化结果
- 用户需要把性能诊断助手相关材料转成清晰结论、优先级和下一步动作

### 调用方式

通过导出的 Python runner 直接调用 AI Skills API：

### 命令示例

**基础调用**

```bash
python3 scripts/run.py --params '{}'
```

**带常用参数调用**

```bash
python3 scripts/run.py --params '{"goal":"诊断目标"}'
```

### 参数说明

| 参数 | 类型 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| `goal` | string | 否 | - | 说明要定位的性能、可用性、搜索、转化或上线检查目标 |
| `audience` | string | 否 | - | 说明受影响的用户、设备、页面类型、地区或业务场景 |
| `materialUrl` | string | 否 | - | 填写公开可访问的待诊断页面、站点、报告或参考链接；需要传可访问的完整 URL |
| `materialFile` | string | 否 | - | 上传 Lighthouse 报告、性能截图、指标表、页面说明或技术排查资料 |
| `materialText` | string | 否 | - | 粘贴页面 URL、性能报告摘要、Core Web Vitals 指标、复现场景或网站质量问题 |
| `brandRequirements` | string | 否 | - | 补充设备网络、浏览器、时间范围、技术栈限制、不可改动项或复测要求 |

完整机器可读参数结构见 `references/form-schema.json`。

### 参数取值参考

当前技能没有需要额外查表的分类参数。

### 支持的输入格式

当前技能直接接收 JSON 参数；如果参数里包含链接字段，请传完整、可访问的 URL。

### 示例请求

下面的示例参数可直接传给 `scripts/run.py`，runner 会把它们发送给 AI Skills API。

```bash
python3 scripts/run.py --params '{"goal":"诊断目标"}'
```

等价的 `--params` JSON：

```json
{
  "goal": "诊断目标"
}
```

### 返回结果示例

```json
{
  "success": true,
  "data": {
    "message": "示例结果请以技能真实返回结构为准。"
  },
  "meta": {
    "executionTime": 842,
    "cached": false
  }
}
```

### 交付内容

- 问题归因、服务改进建议、SOP 或 FAQ 清单：围绕用户目标整理可直接阅读、复盘或交付的核心结果。
- 输入材料解读：结合诊断目标（说明要定位的性能、可用性、搜索、转化或上线检查目标。）、影响对象（说明受影响的用户、设备、页面类型、地区或业务场景。）、待诊断页面链接（填写公开可访问的待诊断页面、站点、报告或参考链接。）提炼关键上下文和判断依据。
- 下一步动作：给出优先级、执行建议或可继续加工的内容框架。

### 结果使用建议

- 先判断输出是否回答了用户关于「性能诊断助手」的核心问题。
- 再检查结果是否覆盖问题归因、服务改进建议、SOP 或 FAQ 清单，以及是否给出明确下一步动作。
- 如果输入材料较少，建议让用户补充目标、受众、限制条件或原始材料后再运行。

### 运行前准备

- `AISKILLS_BASE_URL`：默认 `https://ai-skills.ai`
- `AISKILLS_API_KEY`：必填，用于认证调用
- `AISKILLS_TENANT_ID`：默认 `default`
