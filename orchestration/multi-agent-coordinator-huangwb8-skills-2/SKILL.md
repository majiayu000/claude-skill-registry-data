---
name: multi-agent-coordinator
description: 用于执行包含独立任务的实施计划，将任务分派给新的子代理，并在任务之间进行协调与审查。
metadata:
  short-description: 多代理协调与编排
  keywords:
    - multi-agent-coordinator
    - 多代理
    - 协调器
    - 并行处理
    - 任务编排
    - 工作流
    - 任务分发
    - 结果聚合
    - subagent-driven-development
    - coordination
  category: 架构设计
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
---

# Multi-Agent Coordinator - 多代理协调专家

## 核心原则（Subagent-Driven Development）

- 任务拆分要原子：每个任务有明确输入/输出/验收标准
- 每个任务用“全新子代理”：降低上下文污染与确认偏差
- 任务之间强制门禁：至少一次代码审查；必要时补回归测试
- 若上游分析已把某个 agent 标记为 `required`，该 agent 必须真的进入调度链；缺失时停止推进
- 结果必须可聚合：统一术语、接口约定、日志口径与错误处理风格

## 何时使用

- 用户给出明确实施计划/任务清单，需要并行推进
- 任务跨度大（多文件/多模块/多领域），单线程容易遗漏或拖慢
- 需要严格质量门禁（合并前必须审查、必须验证）

## 输入

- 计划来源：用户文字 / `PLAN.md` / issue 列表 / TODO 列表
- 约束：时间、兼容性、目录边界、不可破坏性要求
- 验收：测试要求、性能目标、行为回归标准

## 输出

- 一个可执行的“任务编排表”（任务 → 负责人子代理 → 依赖 → 验收）
- 一份 `dispatch_manifest`，明确哪些 agent 属于 `required / preferred / optional`
- 一组 `dispatch_receipts` 或缺失说明，证明 required agent 是否真的被调用
- 每个任务的结果摘要（改动点、风险、验证）
- 最终聚合报告（P0/P1/P2 风险 + 下一步）

## 工作流

1. 读取计划并生成任务清单
   - 将大任务拆成 3-15 个原子任务
   - 为每个任务写清：目标、范围、验收、风险、依赖

2. 选择协调模式
   - orchestrator：默认；中心协调器分派任务并统一口径
   - peer-to-peer：小团队/低耦合；允许子代理互相同步但必须记录决定
   - pipeline：强依赖链；按阶段推进（例如：设计→实现→测试→文档）

3. 分派任务（可并行）
   - 先读取上游 `dispatch_gate`
   - 若 `dispatch_gate.can_proceed = false`，立即停止，不要绕过 required agent 继续执行
   - 若 `dispatch_gate.can_proceed = true`，优先调度 `required_agents`，再补 `preferred_agents`
   - 并行仅限“文件/模块不重叠”或“改动可安全合并”的任务
   - 明确要求：输出必须包含（a）改动说明（b）验证方式（c）潜在回滚点

4. 任务间门禁（强制）
   - 对每个任务结果做快速审查：安全/正确性/一致性/边界条件
   - 必要时补回归测试或最小验证步骤

5. 聚合与冲突解决
   - 先合并“口径/接口/命名/日志风格”，再合并代码
   - 如出现冲突：优先保持正确性与可读性；无法判定时暂停并向用户确认
   - required agent 未产生 receipt 时，不能把任务标记为已完成

6. 最终交付检查
   - 关键路径功能可跑通
   - 无明显安全/路径越界/敏感信息泄露
   - 产出文档与代码一致（如有）

## 协调器自检清单

- [ ] 任务拆分是否避免重叠修改同一文件？
- [ ] 是否为每个任务定义了可验证的验收标准？
- [ ] 并行任务是否有清晰的依赖边界？
- [ ] 每个任务是否经过最小审查与验证？
- [ ] 聚合后是否统一了术语与接口风格？
- [ ] `required_agents` 是否都在 `dispatch_manifest` 中出现并拿到 receipt？

## 约束

<!-- BEGIN COMMON CONSTRAINTS -->
<!-- Source-Hash: sha256:15120201e9e0c7569517261d57ecefb63ac279c26ed13876f8e95b6dc35854d3 -->
<!-- Template-ID: skill-common-constraints; Template-Version: 1; Sync-Policy: exact-block -->

### 公共硬约束

本块由 `docs/templates/skill-common-constraints.md` 统一维护；每个 `SKILL.md` 的 `## 约束` 必须逐字同步本块，不得在副本中改写公共规则。

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- `bensz-collect-bugs` 是一个 Agent Skill；仅将 Bensz Agent Skill 或 Bensz 基础设施本身的设计缺陷交给它。先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。

<!-- End of canonical common constraints. -->
<!-- END COMMON CONSTRAINTS -->
