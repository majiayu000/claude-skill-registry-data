---
name: "vibe-flow"
description: "独立开发者 Web/SaaS 项目专属 Vibe Coding 全流程。Invoke when starting a new web product project to run a complete 14-skill pipeline from idea to launch, with controlled feedback loops."
---

# Vibe-Flow 独立开发者全流程

## 适用范围
- 适用：独立开发者主导的 Web/SaaS、管理后台、内容平台、工具类产品
- 适用：需要快速从想法走到可上线版本，并持续迭代变现的项目
- 不适用：纯算法研究、一次性脚本、重硬件依赖项目（可部分借用）

## 核心理念
**前置决策固化 + 契约先行 + 规范底座 + AI执行 + 可控回流 = 全程心流、低返工、可持续迭代的商业项目**

## 三大特质
1. **主线顺序 + 可控回流**：默认按顺序推进；当触发变更条件时，允许回到指定阶段修正，避免无序返工
2. **纯独立开发者适配**：不需要团队、不需要产品/UI/运维配合，单人全栈能全部拿下
3. **深度绑定Vibe Coding**：决策类、设计类、规则类工作优先前置；编码阶段以实现为主，遇到未决策项先回写上游文档再实现

## 极简记忆版
商业→需求→原型→UI→架构→数据→接口→基建→拆任务→编码→测试→部署→文档→迭代

## 每阶段最小交付模板（必须）
每一步都按同一模板交付，避免“看起来做了，实际不可执行”：

1. **输入**：上游阶段产物（文档/图/清单）
2. **输出**：本阶段核心产物（文档或代码）
3. **验收标准（DoD）**：可验证、可打勾的完成标准
4. **存档路径**：统一落盘到 `docs/vibe-flow/`，建议命名 `NN-stage-name.md`

## 14项核心Skill（按开发顺序）

### 1. 商业立项 & 项目范围定义
- **参考**: [project-init](reference/project-init.md)
- **定位**：决定你做的是「产品」不是「作业」
- **产出**：项目立项书、范围边界清单、MVP规划
- **存档建议**：`docs/vibe-flow/01-project-init.md`

### 2. 结构化需求工程
- **参考**: [requirement-engineering](reference/requirement-engineering.md)
- **定位**：把模糊想法变成可落地、可开发的硬规则
- **产出**：主PRD + 各模块子需求文档
- **存档建议**：`docs/vibe-flow/02-requirements.md`

### 3. 业务交互原型设计
- **参考**: [interaction-design](reference/interaction-design.md)
- **定位**：先定「用户怎么操作」，再谈技术
- **产出**：完整可交互低保真原型、流程图表
- **存档建议**：`docs/vibe-flow/03-interaction.md`

### 4. 商业化UI视觉设计
- **参考**: [ui-design](reference/ui-design.md)
- **定位**：告别粗糙美工风，做出上线级产品颜值
- **产出**：高保真UI稿、全局设计规范文档、组件库规范
- **存档建议**：`docs/vibe-flow/04-ui-design.md`

### 5. 全栈系统架构设计
- **参考**: [architecture-design](reference/architecture-design.md)
- **定位**：区分「玩具项目」和「成熟项目」的分水岭
- **产出**：整体架构图、技术选型文档、全局架构设计手册
- **存档建议**：`docs/vibe-flow/05-architecture.md`

### 6. 领域数据建模
- **参考**: [data-modeling](reference/data-modeling.md)
- **定位**：一切业务的底层基石
- **产出**：ER图、数据库设计文档、建表规范
- **存档建议**：`docs/vibe-flow/06-data-model.md`

### 7. API契约优先设计
- **参考**: [api-contract](reference/api-contract.md)
- **定位**：单人全栈协作的核心契约
- **产出**：完整API文档、全局接口约束规范
- **存档建议**：`docs/vibe-flow/07-api-contract.md`

### 8. 企业级工程化基建
- **参考**: [engineering-setup](reference/engineering-setup.md)
- **定位**：给项目铺好「跑道和护栏」
- **产出**：项目基建模板、规范配置、公共基础库
- **存档建议**：`docs/vibe-flow/08-engineering.md`

### 9. 精细化任务拆解 & 单人项目管理
- **参考**: [task-breakdown](reference/task-breakdown.md)
- **定位**：把大项目拆成「可心流开发」的最小单元
- **产出**：结构化TodoList、迭代计划表、任务看板
- **存档建议**：`docs/vibe-flow/09-task-breakdown.md`

### 10. 沉浸式 Vibe-Coding 全栈编码
- **参考**: [vibe-coding](reference/vibe-coding.md)
- **定位**：你最核心的执行层能力
- **产出**：完整可运行业务代码、功能模块
- **存档建议**：`docs/vibe-flow/10-coding-log.md`

### 11. 全维度质量测试
- **参考**: [quality-testing](reference/quality-testing.md)
- **定位**：单人保障线上稳定性
- **产出**：测试报告、修复记录、稳定可运行版本
- **存档建议**：`docs/vibe-flow/11-quality.md`

### 12. 容器化 & 自动化部署运维
- **参考**: [deploy-ops](reference/deploy-ops.md)
- **定位**：独立开发者上线必备硬技能
- **产出**：部署脚本、运维配置、线上稳定环境
- **存档建议**：`docs/vibe-flow/12-deploy-ops.md`

### 13. 全链路项目文档沉淀
- **参考**: [doc-pipeline](reference/doc-pipeline.md)
- **定位**：把项目变成可复用资产
- **产出**：全套项目资产文档
- **存档建议**：`docs/vibe-flow/13-doc-pipeline.md`

### 14. 产品迭代 & 商业化运营
- **参考**: [product-iteration](reference/product-iteration.md)
- **定位**：独立开发者变现、长期存活的收尾能力
- **产出**：迭代方案、产品落地页、商业化配置
- **存档建议**：`docs/vibe-flow/14-product-iteration.md`

## 可控回流机制（强制）
出现以下情况时，必须回流，不允许“硬编码顶过去”：

1. **范围变化**：新增/删除核心功能，回到 1-2
2. **关键交互变化**：主流程或页面跳转改变，回到 3-4
3. **数据或接口变化**：实体关系或契约变化，回到 6-7
4. **架构风险暴露**：性能/安全/可用性不达标，回到 5
5. **测试或线上反馈失败**：缺陷集中或用户行为偏差，回到 9 并重走 10-14

## 使用指南

### 新项目启动流程
1. 按顺序加载每个参考文档
2. 完成每个环节的核心产出
3. 每阶段做一次 DoD 自检，通过后再进入下一步
4. 编码阶段以实现为主，遇到未决策项先回写上游文档再继续

### AI协作要点
- 前期：让AI帮忙分析、规划、设计
- 中期：让AI按契约生成代码
- 后期：让AI生成测试、文档、部署脚本

## 注意事项
- 默认顺序推进：先按主线走，不要在主线中频繁切换
- 触发即回流：满足回流条件时立即回到对应阶段修正
- 决策优先前置：编码阶段以实现为主，减少临场架构决策
- 契约先行：所有接口、数据模型提前定义
- 规范底座：工程化基建一次性搭完
