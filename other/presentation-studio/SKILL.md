---
name: presentation-studio
description: "为尚未明确品类的 PPT、slide deck、演示文稿任务形成 brief，并路由到最合适的专业演示 Skill。Use for 需要先判断是技术讲解、管理决策、研究汇报、融资路演、数据报告还是教学课件；明确品类时直接使用对应专业 Skill。"
license: MIT
metadata:
  architecture: "thin-router"
  language: "zh-CN"
---

# PPT 编排器

本技能只负责澄清演示目标、形成统一 brief、选择一个主品类。实际 PPTX 读取、构建、编辑、渲染和基础检查交给环境中的 `Presentations`；不要复制底层生成流程。

## 最小 brief

在动手前明确会改变成品的字段。用户已给出的内容不要重复追问：

- 受众与其已有知识
- 看完后要理解、相信或决定什么
- 现场演讲还是自阅，时长和总页数
- 语言、技术深度、证据截至日期
- 可用资料、模板、品牌限制和可编辑性要求
- 是否需要演讲备注、问答准备或附录

缺少非关键字段时采用合理默认值并继续。需要跨技能传递时，使用 [统一契约](references/contracts.md)，只传紧凑字段，不复制全部上下文。

## 路由

- 技术体系、架构、机制、参数、产品或技术选型、企业技术培训：`technical-explainer-deck`
- 领导汇报、方案审批、资源选择、战略取舍：`executive-decision-deck`
- 论文、实验、学术会议、研究进展：`research-presentation`
- 融资、创业项目、投资人路演：`pitch-deck`
- KPI、经营复盘、周月季报、数据故事：`data-report-deck`
- 非技术型课程、工作坊、知识教学：`teaching-deck`
- 已有演示的审阅、评分、验收或修复：`deck-review`

若任务同时符合多个品类，按观众最终要做的事确定一个主品类；其他品类只提供模块。例如“向管理层解释芯片路线并申请预算”以 `executive-decision-deck` 为主，技术机制页借用 `technical-explainer-deck` 的页面模式。

## 输出

向后续流程交付：一个 `deck-brief`、主品类、需要复用的现有研究/数据 Skill，以及不超过一句话的路由理由。不要在编排器里展开视觉模板、生成代码或完整 QA 规则。

