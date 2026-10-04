---
name: atdd-guide
description: Acceptance Test Driven Development (ATDD) workflow for writing executable specifications before implementation, structuring tests with domain language, DSL, and protocol drivers, then driving TDD and production-like verification. Use when tasks require business-facing acceptance criteria, outside-in development, BDD/acceptance-first delivery, or requirement-to-test translation.
---

# ATDD Guide

## 目标

用验收测试（Acceptance Test）驱动开发，先定义“系统做什么（What）”，再实现“怎么做（How）”。始终从外部用户视角（outside-in）表达业务行为，避免 UI 细节耦合。

## 执行顺序

1. 锁定验收标准
   - 把需求拆成可断言的业务行为与边界条件。
   - 使用领域术语（Domain Language），避免 “click/fill field” 一类界面动作。
2. 先写可执行规格（Executable Specification）
   - 为每个 Acceptance Criteria 先写一个失败的验收测试。
   - 让测试场景原子化；每个用例独立准备数据，不共享状态。
3. 建立四层分离
   - Test Cases：业务场景与断言。
   - DSL（Domain Specific Language）：复用步骤与默认参数，只保留领域语义。
   - Protocol Drivers：把 DSL 翻译为 UI/API/RPC 等具体通道调用。
   - SUT：被测系统本体。
4. 用 TDD 落地内部实现
   - 在 Acceptance Test 失败的前提下，用 RED -> GREEN -> REFACTOR 完成细粒度实现。
   - 只写通过当前测试所需的最小代码。
5. 在 production-like 环境验证
   - 用与生产一致的部署方式、配置方式与基础设施工具运行验收测试。
   - 覆盖配置、依赖版本、启动流程等变更风险。
6. 记录证据并回归
   - 保存测试命令、结果与失败/修复链路。
   - 新需求新增 Acceptance Test，再进入下一轮。

## 强制规则

- 通过公共接口交互 SUT，禁止后门读写内部状态。
- 验收测试只验证行为，不验证内部实现细节。
- DSL 只承载领域概念，不泄漏技术细节。
- 不跳过失败阶段：必须先看到测试失败，再写实现。
- 外部依赖优先 stub/mock，保持可离线复现。

## 反模式

- 用 UI 操作步骤替代业务行为描述。
- 在测试中共享脆弱测试数据。
- 把协议细节硬编码进测试用例而不是 Driver。
- 仅做单元测试，不做端到端验收闭环。
- 在非 production-like 环境声称“已通过验收”。

## 协同技能

- 需要任务拆解时，先用 `planner`。
- 需要严格实现循环时，配合 `tdd-guide`。
- 需要交付门禁时，配合 `verification-loop`。
- 需要需求到文档落地时，配合 `req-to-dev`。

## 参考资料

需要详细检查清单与模板时，读取 `references/atdd-checklist.md`。
