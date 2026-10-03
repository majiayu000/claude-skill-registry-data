---
name: briefbound-code-structure-guard
description: "Use when active development or explicit refactoring has concrete code-structure risk: a source file is accumulating independently changing responsibilities, a class/component/function is hard to navigate or test, repeated changes touch distant sections, or the user asks to split a giant file; do not use for line count alone, generated/vendor/migration/schema/fixture files, or cohesive modules that remain easier to maintain together."
license: MIT
---

# Briefbound 代码结构守卫

## 目标

防止本轮开发继续制造多职责巨型文件。只提取稳定职责，不为压低行数制造薄包装、转发层或碎片目录。

## Briefbound task contract

- Context Boundary: 已对齐结果、当前开发 owner、目标文件、相邻模块、调用方、测试和允许写入范围。
- Output Contract: `STAY / CHECK / SPLIT` 判断；必要时完成最小职责拆分，并保持公共行为和验证证据。
- Allowed Action: 读取目标、调用方和测试；在授权 scope 内提取代码并验证；不重写模块、改变公共行为或全仓扫描。
- Success Evidence: 目标行为保持，提取单元具有可说明的职责和依赖边界，相关测试/类型/构建检查通过，且没有新增无价值抽象。
- Stop Condition: 行数是唯一信号、文件仍保持单一内聚职责、拆分会扩大用户范围、缺少行为保护，或需要公共 API/架构取舍。
- Route Out: 当前开发 owner、`briefbound-planning`、`briefbound-pr-review`、`briefbound-simplification-audit`、`briefbound-development-cleanup`、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或当前 owner，不接管功能、Bug、性能或普通审查。
- 用户可见内容默认中文，只报结构决策、修改、证据和风险；保留代码、命令、路径、API、skill 名和枚举；Route Out 仅以 Briefbound task contract 为准；有自然闸门时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 三档结构闸门

- `STAY`：职责内聚且修改位于同一行为边界。继续开发，不输出结构报告。
- `CHECK`：接近项目阈值、修改跨远距离区段或可能形成第二职责。检查 imports/exports、状态所有权、调用方和测试；证据不足即 `STAY`。
- `SPLIT`：至少存在两个独立信号，例如多个领域/层/生命周期混在一起、不同部分独立变化或复用、测试与所有权边界可分、反复修改造成导航或合并冲突。由本 skill 完成最小拆分。

优先使用项目规则；没有规则时，`函数约 75 行、类/组件约 300 行、源文件约 500 行` 只能触发 `CHECK`，不能单独触发 `SPLIT`。手写源文件超过约 800 行时优先检查，仍按职责判断。

默认排除 generated、vendor、migration、schema、fixture、快照、声明式数据和明确的单文件产物。

## 最小拆分

1. 读目标、直接调用方和最近测试，只定位本次职责，不扫描全仓排行榜。
2. 候选单元须能用一句话说明职责；仍共享大量私有状态时不拆。
3. 优先提取完整行为、领域服务、独立组件或适配边界。类型、常量和 helper 只有独立消费者或所有权时才成文件。
4. 保持公共 API、导入路径、错误语义和顺序；一次只移动解除当前风险的部分。
5. 运行最近行为测试及必要类型/构建检查；纯移动也检查 imports、初始化和 mock/patch 路径。

拆分没有降低耦合、认知负担或未来冲突时，撤销本轮自己的结构修改并保持 `STAY`。

## 低噪声约束

- 不默认生成规划文档、结构评分、长度榜、worktree、子 Agent 或严格 TDD。
- 不设统一行数硬门槛；普通 PR 仍由 `briefbound-pr-review` 主责。
